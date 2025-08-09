from fastapi import FastAPI, APIRouter, WebSocket, WebSocketDisconnect, HTTPException, Depends
from fastapi.responses import JSONResponse
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
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
from datetime import datetime, timedelta
from typing import List, Dict, Optional
import asyncio
import jwt
from passlib.context import CryptContext
from questions import get_random_question

# Rankings model
class PlayerRanking(BaseModel):
    player_id: str
    username: str
    points: int = 0
    games_played: int = 0
    games_won: int = 0
    win_rate: float = 0.0
    last_played: Optional[datetime] = None


def json_serializable(obj):
    """Make objects JSON serializable"""
    if isinstance(obj, datetime):
        return obj.isoformat()
    elif isinstance(obj, dict):
        return {k: json_serializable(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [json_serializable(item) for item in obj]
    else:
        return obj

async def safe_send_json(websocket: WebSocket, data: dict):
    """Safely send JSON data through WebSocket"""
    try:
        serializable_data = json_serializable(data)
        await websocket.send_text(json.dumps(serializable_data))
    except Exception as e:
        logger.error(f"Error sending WebSocket message: {e}")
        raise


ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

# MongoDB connection
mongo_url = os.environ['MONGO_URL']
client = AsyncIOMotorClient(mongo_url)
db = client[os.environ['DB_NAME']]

# Collections
users_collection = db['users']
rankings_collection = db['rankings']

# Authentication configuration
SECRET_KEY = os.environ.get('JWT_SECRET_KEY', 'your-secret-key-change-in-production')
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
security = HTTPBearer()

# Create the main app without a prefix
app = FastAPI()

# Create a router with the /api prefix
api_router = APIRouter(prefix="/api")

# In-memory storage for game rooms and connections
rooms: Dict[str, Dict] = {}
connections: Dict[str, WebSocket] = {}

# WebSocket keepalive configuration (optional)
WS_SERVER_PING = os.environ.get('WS_SERVER_PING', 'true').lower() == 'true'
WS_SERVER_PING_INTERVAL = int(os.environ.get('WS_SERVER_PING_INTERVAL', '20'))  # seconds

# Define Models

# Authentication Models
class LoginRequest(BaseModel):
    username: str
    password: str

class RegisterRequest(BaseModel):
    username: str
    password: str
    confirm_password: str

class LoginResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user_id: str
    username: str

class User(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    username: str
    hashed_password: str
    created_at: datetime = Field(default_factory=datetime.utcnow)

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
                await safe_send_json(connections[player_id], message)
            except Exception as e:
                logger.warning(f"Broadcast failed to {player_id}: {e}")
                # Connection is dead, remove it
                if player_id in connections:
                    del connections[player_id]

# Add your routes to the router instead of directly to app

# Authentication endpoints
@api_router.post("/auth/login", response_model=LoginResponse)
async def login(request: LoginRequest):
    """Login endpoint"""
    user = await authenticate_user(request.username, request.password)
    if not user:
        raise HTTPException(status_code=401, detail="Usuário ou senha incorretos")
    
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.id}, expires_delta=access_token_expires
    )
    
    return LoginResponse(
        access_token=access_token,
        user_id=user.id,
        username=user.username
    )

@api_router.post("/auth/register", response_model=LoginResponse)
async def register(request: RegisterRequest):
    """Register new user endpoint"""
    import re
    
    # Validate passwords match
    if request.password != request.confirm_password:
        raise HTTPException(status_code=400, detail="As senhas não coincidem")
    
    # Check password length
    if len(request.password) < 6:
        raise HTTPException(status_code=400, detail="A senha deve ter pelo menos 6 caracteres")
    
    # Validate username is a person's name (letters, spaces, accents only)
    name_pattern = r'^[a-zA-ZÀ-ÿ\s\'-]+$'
    if not re.match(name_pattern, request.username.strip()) or len(request.username.strip()) < 2:
        raise HTTPException(status_code=400, detail="Digite apenas nomes de pessoas (letras e espaços)")
    
    # Check if username already exists
    existing_user = await get_user_by_username(request.username.lower())
    if existing_user:
        raise HTTPException(status_code=400, detail="Este nome já está em uso")
    
    # Create new user
    hashed_password = get_password_hash(request.password)
    user = User(
        username=request.username.lower().strip(),
        hashed_password=hashed_password
    )
    
    try:
        await db.users.insert_one({
            "id": user.id,
            "username": user.username,
            "hashed_password": user.hashed_password,
            "created_at": user.created_at
        })
        
        # Create access token for immediate login
        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            data={"sub": user.id}, expires_delta=access_token_expires
        )
        
        return LoginResponse(
            access_token=access_token,
            user_id=user.id,
            username=user.username
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail="Erro ao criar usuário")

@api_router.post("/auth/create-test-user")
async def create_test_user():
    """Create a test user (remove in production)"""
    username = "admin"
    password = "123456"
    
    # Check if user already exists
    existing_user = await get_user_by_username(username)
    if existing_user:
        return {"message": "Usuário de teste já existe", "username": username}
    
    # Create new user
    hashed_password = get_password_hash(password)
    user = User(
        username=username,
        hashed_password=hashed_password
    )
    
    await db.users.insert_one({
        "id": user.id,
        "username": user.username,
        "hashed_password": user.hashed_password,
        "created_at": user.created_at
    })
    
    return {"message": "Usuário de teste criado", "username": username, "password": password}

# Health check
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
    logger.info(f"Room created {room_code} by player {player_id} ({request.player_name})")
    
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
        logger.warning(f"Join failed - room not found: {room_code} ({request.player_name})")
        raise HTTPException(status_code=404, detail="Sala não encontrada")
    
    if len(room["players"]) >= 2:
        logger.warning(f"Join failed - room full: {room_code} ({request.player_name})")
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
        {"$set": {
            "players": room["players"],
            "player_symbols": room["player_symbols"],
            "board": room["board"]
        }}
    )
    logger.info(f"Player joined room {room_code}: {player_id} ({request.player_name}) - players={len(room['players'])}")
    
    return JoinRoomResponse(
        room_code=room_code, 
        player_id=player_id,
        room_status=room["board"]["game_status"]
    )

@api_router.get("/rooms/{room_code}/status")
async def get_room_status(room_code: str):
    """Get current room status"""
    room_code = room_code.upper()
    
    # Load room from memory or database
    room = await load_room_from_db(room_code)
    if not room:
        raise HTTPException(status_code=404, detail="Sala não encontrada")
    
    return {
        "room_code": room_code,
        "players": room["players"],
        "player_count": len(room["players"]),
        "game_status": room["board"]["game_status"],
        "board": room["board"]
    }

# Include the router in the main app
app.include_router(api_router)

async def _server_keepalive(player_id: str):
    """Optional server-side keepalive pings to client"""
    try:
        while True:
            if player_id not in connections:
                break
            ws = connections.get(player_id)
            if ws is None:
                break
            try:
                await safe_send_json(ws, {"type": "ping", "from": "server"})
            except Exception as e:
                logger.warning(f"Keepalive ping failed for {player_id}: {e}")
                break
            await asyncio.sleep(WS_SERVER_PING_INTERVAL)
    except asyncio.CancelledError:
        pass

@app.websocket("/api/ws/{player_id}")
async def websocket_endpoint(websocket: WebSocket, player_id: str):
    """WebSocket endpoint for real-time game communication"""
    await websocket.accept()
    connections[player_id] = websocket
    logger.info(f"WS connected: player_id={player_id}")

    keepalive_task = None
    if WS_SERVER_PING:
        keepalive_task = asyncio.create_task(_server_keepalive(player_id))
    
    try:
        # Send initial ping to confirm connection
        await safe_send_json(websocket, {"type": "connected", "player_id": player_id})
        
        while True:
            # Receive message from client
            data = await websocket.receive_text()
            message = json.loads(data)
            
            message_type = message.get("type")
            room_code = message.get("room_code")
            logger.debug(f"WS message from {player_id}: type={message_type} room={room_code}")
            
            if message_type == "ping":
                # Heartbeat ping - respond with pong
                await safe_send_json(websocket, {"type": "pong"})
                continue
            
            elif message_type == "join_room":
                # Player joined a room, send initial state
                room = await load_room_from_db(room_code)
                if room:
                    # Se ao conectar só existir 1 player, garanta que o current_player_id aponte para o X (criador)
                    if len(room["players"]) == 1:
                        try:
                            # encontrar jogador com símbolo X
                            x_player_id = next((pid for pid, sym in room["player_symbols"].items() if sym == "X"), None)
                            if x_player_id:
                                room["current_player_id"] = x_player_id
                        except Exception as e:
                            logger.warning(f"Failed to set current_player_id on join_room: {e}")
                    await safe_send_json(websocket, {
                        "type": "room_state",
                        "room": room
                    })
                    
                    # Notify other players
                    await broadcast_to_room(room_code, {
                        "type": "player_joined",
                        "player_name": room["players"].get(player_id, "Unknown"),
                        "player_count": len(room["players"]),
                        "room": room
                    })
                else:
                    await safe_send_json(websocket, {
                        "type": "error",
                        "message": "Sala não encontrada"
                    })
            
            elif message_type == "make_move":
                # Player makes a move
                cell_index = message.get("cell_index")
                selected_answer = message.get("selected_answer")
                question = message.get("question")
                
                room = await load_room_from_db(room_code)
                if room:
                    # Validate it's the player's turn
                    if room["current_player_id"] != player_id:
                        await safe_send_json(websocket, {
                            "type": "error",
                            "message": "Não é sua vez!"
                        })
                        continue
                    
                    # Process the move
                    await process_game_move(room_code, player_id, cell_index, selected_answer, question)
            
            elif message_type == "get_question":
                # Client requests a question for a cell
                cell_index = message.get("cell_index")
                subject = message.get("subject", "historia")  # Default to historia for backward compatibility
                
                room = await load_room_from_db(room_code)
                if room:
                    # Set current question and selected cell based on subject
                    if subject == "quimica":
                        question = get_random_question(subject="quimica")
                    else:  # default to historia
                        question = get_random_question(subject="historia")
                    
                    room["current_question"] = question
                    room["selected_cell"] = cell_index
                    room["subject"] = subject  # Store subject in room
                    
                    # Send question to the current player
                    await safe_send_json(websocket, {
                        "type": "question",
                        "question": question,
                        "cell_index": cell_index,
                        "subject": subject
                    })
                    
                    # Notify other player that someone is answering
                    await broadcast_to_room(room_code, {
                        "type": "player_answering",
                        "player_name": room["players"][player_id],
                        "cell_index": cell_index,
                        "subject": subject
                    })
    
    except WebSocketDisconnect:
        # Handle disconnection
        logger.info(f"WS disconnected: player_id={player_id}")
        if player_id in connections:
            del connections[player_id]
        
        # Find room and mark player as disconnected, but don't remove immediately
        for room_code, room in rooms.items():
            if player_id in room["players"]:
                # Notify other players
                await broadcast_to_room(room_code, {
                    "type": "player_disconnected",
                    "player_name": room["players"][player_id]
                })
                break
    except Exception as e:
        logger.error(f"WS error for {player_id}: {e}")
        raise
    finally:
        if keepalive_task:
            keepalive_task.cancel()

async def process_game_move(room_code: str, player_id: str, cell_index: int, selected_answer: str, question: Dict):
    """Process a player's move and update game state"""
    room = await load_room_from_db(room_code)
    if not room:
        return
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
        
        # Find next player deterministically (prioritize existing order)
        for pid, symbol in room["player_symbols"].items():
            if symbol == next_symbol:
                room["current_player_id"] = pid
                break
    
    # Clear current question
    room["current_question"] = None
    room["selected_cell"] = None
    
    # Update database (persist both board and current_player_id)
    await db.game_rooms.update_one(
        {"_id": room_code},
        {"$set": {"board": board, "current_player_id": room["current_player_id"]}}
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

# Ranking management functions
async def update_player_ranking(player_id: str, username: str, won: bool = False):
    """Update player ranking after a game"""
    ranking = await rankings_collection.find_one({"player_id": player_id})
    
    if ranking:
        # Update existing ranking
        new_games_played = ranking["games_played"] + 1
        new_games_won = ranking["games_won"] + (1 if won else 0)
        new_points = ranking["points"] + (3 if won else 1)  # 3 points for win, 1 for participation
        new_win_rate = (new_games_won / new_games_played) * 100
        
        await rankings_collection.update_one(
            {"player_id": player_id},
            {"$set": {
                "games_played": new_games_played,
                "games_won": new_games_won,
                "points": new_points,
                "win_rate": round(new_win_rate, 1),
                "last_played": datetime.utcnow()
            }}
        )
    else:
        # Create new ranking entry
        new_ranking = {
            "player_id": player_id,
            "username": username,
            "points": 3 if won else 1,
            "games_played": 1,
            "games_won": 1 if won else 0,
            "win_rate": 100.0 if won else 0.0,
            "last_played": datetime.utcnow()
        }
        await rankings_collection.insert_one(new_ranking)

async def get_rankings():
    """Get top rankings sorted by points"""
    cursor = rankings_collection.find().sort("points", -1).limit(20)
    rankings = []
    async for ranking in cursor:
        rankings.append({
            "id": str(ranking["_id"]),
            "name": ranking["username"],
            "points": ranking["points"],
            "games": ranking["games_played"],
            "wins": ranking["games_won"],
            "winRate": ranking["win_rate"]
        })
    return rankings

app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Authentication Functions
def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a password against its hash"""
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    """Hash a password"""
    return pwd_context.hash(password)

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    """Create a JWT access token"""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

async def get_user_by_username(username: str) -> Optional[User]:
    """Get user from database by username"""
    user_data = await db.users.find_one({"username": username.lower()})
    if user_data:
        return User(**user_data)
    return None

async def authenticate_user(username: str, password: str) -> Optional[User]:
    """Authenticate user with username and password"""
    user = await get_user_by_username(username.lower())
    if not user or not verify_password(password, user.hashed_password):
        return None
    return user

async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)) -> User:
    """Get current user from JWT token"""
    try:
        payload = jwt.decode(credentials.credentials, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("sub")
        if user_id is None:
            raise HTTPException(status_code=401, detail="Token inválido")
    except jwt.PyJWTError:
        raise HTTPException(status_code=401, detail="Token inválido")
    
    user_data = await db.users.find_one({"id": user_id})
    if user_data is None:
        raise HTTPException(status_code=401, detail="Usuário não encontrado")
    return User(**user_data)
@api_router.get("/rankings")
async def get_global_rankings():
    """Get global rankings"""
    try:
        rankings = await get_rankings()
        return {"rankings": rankings}
    except Exception as e:
        logger.error(f"Error getting rankings: {e}")
        raise HTTPException(status_code=500, detail="Error getting rankings")

# Logging setup
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@app.on_event("shutdown")
async def shutdown_db_client():
    client.close()