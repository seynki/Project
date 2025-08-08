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

@api_router.post("/rooms/join", response_model=JoinRoomResponse)
async def join_room(request: JoinRoomRequest):
    """Join an existing game room"""
    room_code = request.room_code.upper()
    
    if room_code not in rooms:
        raise HTTPException(status_code=404, detail="Sala não encontrada")
    
    room = rooms[room_code]
    
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
