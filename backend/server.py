from fastapi import FastAPI, APIRouter, WebSocket, WebSocketDisconnect, HTTPException
from fastapi.responses import JSONResponse
from dotenv import load_dotenv
from starlette.middleware.cors import CORSMiddleware
from motor.motor_asyncio import AsyncIOMotorClient
import os
import logging
from pathlib import Path
from pydantic import BaseModel, Field
from typing import List, Dict, Optional
import uuid
import json
import random
import string
from datetime import datetime


ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

# MongoDB connection
mongo_url = os.environ['MONGO_URL']
client = AsyncIOMotorClient(mongo_url)
db = client[os.environ['DB_NAME']]

# Create the main app without a prefix
app = FastAPI()

# Create a router with the /api prefix
api_router = APIRouter(prefix="/api")

# In-memory storage for game rooms and connections
rooms: Dict[str, Dict] = {}
connections: Dict[str, WebSocket] = {}

# Define Models
class StatusCheck(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    client_name: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)

class StatusCheckCreate(BaseModel):
    client_name: str

class CreateRoomRequest(BaseModel):
    player_name: str

class JoinRoomRequest(BaseModel):
    room_code: str
    player_name: str

class CreateRoomResponse(BaseModel):
    room_code: str
    player_id: str

class JoinRoomResponse(BaseModel):
    room_code: str
    player_id: str
    room_status: str

# Game Models
class GameBoard(BaseModel):
    board: List[Optional[str]] = Field(default_factory=lambda: [None] * 9)
    board_colors: List[Optional[str]] = Field(default_factory=lambda: [None] * 9)
    current_player: str = "X"
    game_status: str = "waiting"  # waiting, playing, won, draw
    winner: Optional[str] = None

class GameRoom(BaseModel):
    room_code: str
    players: Dict[str, str] = Field(default_factory=dict)  # player_id -> player_name
    player_symbols: Dict[str, str] = Field(default_factory=dict)  # player_id -> X/O
    board: GameBoard = Field(default_factory=GameBoard)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    current_question: Optional[Dict] = None
    selected_cell: Optional[int] = None
    current_player_id: Optional[str] = None

def generate_room_code() -> str:
    """Generate a unique 6-character room code"""
    while True:
        code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
        if code not in rooms:
            return code

async def broadcast_to_room(room_code: str, message: Dict):
    """Send a message to all players in a room"""
    if room_code not in rooms:
        return
    
    room = rooms[room_code]
    for player_id in room["players"]:
        if player_id in connections:
            try:
                await connections[player_id].send_text(json.dumps(message))
            except:
                # Connection is dead, remove it
                if player_id in connections:
                    del connections[player_id]

# Add your routes to the router instead of directly to app
@api_router.get("/")
async def root():
    return {"message": "Tic-Tac-Toe Historical Game API"}

@api_router.post("/status", response_model=StatusCheck)
async def create_status_check(input: StatusCheckCreate):
    status_dict = input.dict()
    status_obj = StatusCheck(**status_dict)
    _ = await db.status_checks.insert_one(status_obj.dict())
    return status_obj

@api_router.get("/status", response_model=List[StatusCheck])
async def get_status_checks():
    status_checks = await db.status_checks.find().to_list(1000)
    return [StatusCheck(**status_check) for status_check in status_checks]

@api_router.post("/rooms/create", response_model=CreateRoomResponse)
async def create_room(request: CreateRoomRequest):
    """Create a new game room"""
    room_code = generate_room_code()
    player_id = str(uuid.uuid4())
    
    # Create new room
    room_data = {
        "room_code": room_code,
        "players": {player_id: request.player_name},
        "player_symbols": {player_id: "X"},  # First player is always X
        "board": {
            "board": [None] * 9,
            "board_colors": [None] * 9,
            "current_player": "X",
            "game_status": "waiting",
            "winner": None
        },
        "created_at": datetime.utcnow(),
        "current_question": None,
        "selected_cell": None,
        "current_player_id": player_id
    }
    
    rooms[room_code] = room_data
    
    # Save to database
    await db.game_rooms.insert_one({
        **room_data,
        "_id": room_code,
        "created_at": room_data["created_at"]
    })
    
    return CreateRoomResponse(room_code=room_code, player_id=player_id)

async def load_room_from_db(room_code: str) -> Optional[Dict]:
    """Load room data from database if not in memory"""
    if room_code in rooms:
        return rooms[room_code]
    
    # Try to load from database
    db_room = await db.game_rooms.find_one({"_id": room_code})
    if db_room:
        # Convert back to memory format
        room_data = {
            "room_code": db_room["room_code"],
            "players": db_room["players"],
            "player_symbols": db_room["player_symbols"],
            "board": db_room["board"],
            "created_at": db_room["created_at"],
            "current_question": db_room.get("current_question"),
            "selected_cell": db_room.get("selected_cell"),
            "current_player_id": db_room.get("current_player_id")
        }
        rooms[room_code] = room_data
        return room_data
    
    return None

@api_router.post("/rooms/join", response_model=JoinRoomResponse)
async def join_room(request: JoinRoomRequest):
    """Join an existing game room"""
    room_code = request.room_code.upper()
    
    # Load room from memory or database
    room = await load_room_from_db(room_code)
    if not room:
        raise HTTPException(status_code=404, detail="Sala não encontrada")
    
    if len(room["players"]) >= 2:
        raise HTTPException(status_code=400, detail="Sala está cheia")
    
    player_id = str(uuid.uuid4())
    room["players"][player_id] = request.player_name
    room["player_symbols"][player_id] = "O"  # Second player is always O
    
    # If room is full, start the game
    if len(room["players"]) == 2:
        room["board"]["game_status"] = "playing"
    
    # Update database
    await db.game_rooms.update_one(
        {"_id": room_code},
        {"$set": {"players": room["players"], "player_symbols": room["player_symbols"]}}
    )
    
    return JoinRoomResponse(
        room_code=room_code, 
        player_id=player_id,
        room_status=room["board"]["game_status"]
    )

@api_router.get("/rooms/{room_code}/status")
async def get_room_status(room_code: str):
    """Get current room status"""
    room_code = room_code.upper()
    
    if room_code not in rooms:
        raise HTTPException(status_code=404, detail="Sala não encontrada")
    
    room = rooms[room_code]
    return {
        "room_code": room_code,
        "players": room["players"],
        "player_count": len(room["players"]),
        "game_status": room["board"]["game_status"],
        "board": room["board"]
    }

# Include the router in the main app
app.include_router(api_router)

@app.websocket("/api/ws/{player_id}")
async def websocket_endpoint(websocket: WebSocket, player_id: str):
    """WebSocket endpoint for real-time game communication"""
    await websocket.accept()
    connections[player_id] = websocket
    
    try:
        while True:
            # Receive message from client
            data = await websocket.receive_text()
            message = json.loads(data)
            
            message_type = message.get("type")
            room_code = message.get("room_code")
            
            if message_type == "join_room":
                # Player joined a room, send initial state
                if room_code in rooms:
                    room = rooms[room_code]
                    await websocket.send_text(json.dumps({
                        "type": "room_state",
                        "room": room
                    }))
                    
                    # Notify other players
                    await broadcast_to_room(room_code, {
                        "type": "player_joined",
                        "player_name": room["players"].get(player_id, "Unknown"),
                        "player_count": len(room["players"])
                    })
            
            elif message_type == "make_move":
                # Player makes a move
                cell_index = message.get("cell_index")
                selected_answer = message.get("selected_answer")
                question = message.get("question")
                
                if room_code in rooms:
                    room = rooms[room_code]
                    
                    # Validate it's the player's turn
                    if room["current_player_id"] != player_id:
                        await websocket.send_text(json.dumps({
                            "type": "error",
                            "message": "Não é sua vez!"
                        }))
                        continue
                    
                    # Process the move
                    await process_game_move(room_code, player_id, cell_index, selected_answer, question)
            
            elif message_type == "get_question":
                # Client requests a question for a cell
                cell_index = message.get("cell_index")
                
                if room_code in rooms:
                    room = rooms[room_code]
                    
                    # Set current question and selected cell
                    from questions import get_random_question
                    question = get_random_question()
                    
                    room["current_question"] = question
                    room["selected_cell"] = cell_index
                    
                    # Send question to the current player
                    await websocket.send_text(json.dumps({
                        "type": "question",
                        "question": question,
                        "cell_index": cell_index
                    }))
                    
                    # Notify other player that someone is answering
                    await broadcast_to_room(room_code, {
                        "type": "player_answering",
                        "player_name": room["players"][player_id],
                        "cell_index": cell_index
                    })
    
    except WebSocketDisconnect:
        # Handle disconnection
        if player_id in connections:
            del connections[player_id]
        
        # Find and clean up room
        for room_code, room in rooms.items():
            if player_id in room["players"]:
                # Notify other players
                await broadcast_to_room(room_code, {
                    "type": "player_disconnected",
                    "player_name": room["players"][player_id]
                })
                
                # Remove player from room
                del room["players"][player_id]
                if player_id in room["player_symbols"]:
                    del room["player_symbols"][player_id]
                
                # If room is empty, clean it up
                if not room["players"]:
                    del rooms[room_code]
                    await db.game_rooms.delete_one({"_id": room_code})
                break

async def process_game_move(room_code: str, player_id: str, cell_index: int, selected_answer: str, question: Dict):
    """Process a player's move and update game state"""
    if room_code not in rooms:
        return
    
    room = rooms[room_code]
    board = room["board"]
    
    # Check if answer is correct
    is_correct = selected_answer == question["correctAnswer"]
    
    # Update board
    player_symbol = room["player_symbols"][player_id]
    board["board"][cell_index] = player_symbol
    board["board_colors"][cell_index] = "green" if is_correct else "red"
    
    # Check for winner
    winner_symbol = check_winner(board["board"], board["board_colors"])
    if winner_symbol:
        board["game_status"] = "won"
        board["winner"] = winner_symbol
        
        # Find winner player
        winner_player_id = None
        for pid, symbol in room["player_symbols"].items():
            if symbol == winner_symbol:
                winner_player_id = pid
                break
    elif all(cell is not None for cell in board["board"]):
        board["game_status"] = "draw"
    else:
        # Switch turns
        current_symbol = room["player_symbols"][player_id]
        next_symbol = "O" if current_symbol == "X" else "X"
        board["current_player"] = next_symbol
        
        # Find next player
        for pid, symbol in room["player_symbols"].items():
            if symbol == next_symbol:
                room["current_player_id"] = pid
                break
    
    # Clear current question
    room["current_question"] = None
    room["selected_cell"] = None
    
    # Update database
    await db.game_rooms.update_one(
        {"_id": room_code},
        {"$set": {"board": board}}
    )
    
    # Broadcast updated game state
    await broadcast_to_room(room_code, {
        "type": "game_update",
        "room": room,
        "move": {
            "player_id": player_id,
            "player_name": room["players"][player_id],
            "cell_index": cell_index,
            "is_correct": is_correct,
            "answer": selected_answer,
            "correct_answer": question["correctAnswer"]
        }
    })

def check_winner(board: List[Optional[str]], board_colors: List[Optional[str]]) -> Optional[str]:
    """Check if there's a winner on the board"""
    winning_lines = [
        [0, 1, 2], [3, 4, 5], [6, 7, 8],  # rows
        [0, 3, 6], [1, 4, 7], [2, 5, 8],  # columns
        [0, 4, 8], [2, 4, 6]  # diagonals
    ]
    
    for line in winning_lines:
        a, b, c = line
        if (board[a] and 
            board[a] == board[b] == board[c] and
            board_colors[a] == board_colors[b] == board_colors[c] == "green"):
            return board[a]
    
    return None

app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

@app.on_event("shutdown")
async def shutdown_db_client():
    client.close()
