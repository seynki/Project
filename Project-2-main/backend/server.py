from fastapi import FastAPI, APIRouter, WebSocket, WebSocketDisconnect, HTTPException
from dotenv import load_dotenv
from starlette.middleware.cors import CORSMiddleware
from motor.motor_asyncio import AsyncIOMotorClient
import os
import logging
from pathlib import Path
from pydantic import BaseModel, Field
from typing import List, Dict, Optional
import uuid
from datetime import datetime
import json

# Import our game models and manager
from models import Player, GameRoom, CreateRoomRequest, JoinRoomRequest, AnswerRequest, CellClickRequest
from game_manager import game_manager

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

# Helper function to update player stats
async def update_player_stats(player_name: str, won: bool = False):
    """Update player statistics in database"""
    player_data = await db.players.find_one({"name": player_name})
    
    if not player_data:
        # Create new player
        player = Player(
            name=player_name,
            games=1,
            wins=1 if won else 0,
            losses=0 if won else 1,
            points=1 if won else 0,
            win_rate=100.0 if won else 0.0
        )
        await db.players.insert_one(player.dict())
    else:
        # Update existing player
        new_games = player_data["games"] + 1
        new_wins = player_data["wins"] + (1 if won else 0)
        new_losses = player_data["losses"] + (0 if won else 1)
        new_points = player_data["points"] + (1 if won else 0)
        new_win_rate = (new_wins / new_games) * 100 if new_games > 0 else 0.0
        
        await db.players.update_one(
            {"name": player_name},
            {"$set": {
                "games": new_games,
                "wins": new_wins,
                "losses": new_losses,
                "points": new_points,
                "win_rate": new_win_rate,
                "updated_at": datetime.utcnow()
            }}
        )

# Game API endpoints
@api_router.post("/game/create-room")
async def create_room(request: CreateRoomRequest):
    """Create a new game room"""
    room = game_manager.create_room(request.player_name)
    return {"success": True, "room_code": room.code, "room": room.dict()}

@api_router.post("/game/join-room")
async def join_room(request: JoinRoomRequest):
    """Join an existing game room"""
    room = game_manager.join_room(request.room_code, request.player_name)
    if not room:
        raise HTTPException(status_code=404, detail="Room not found or full")
    
    # Broadcast room update to all connected clients
    await game_manager.broadcast_to_room(request.room_code, {
        "type": "room_update",
        "room": room.dict()
    })
    
    return {"success": True, "room": room.dict()}

@api_router.get("/game/room/{room_code}")
async def get_room(room_code: str):
    """Get room information"""
    room = game_manager.get_room(room_code)
    if not room:
        raise HTTPException(status_code=404, detail="Room not found")
    return {"room": room.dict()}

@api_router.post("/game/click-cell")
async def click_cell(request: CellClickRequest):
    """Handle cell click to generate question"""
    result = game_manager.handle_cell_click(request.room_code, request.player_name, request.cell_index)
    if "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])
    
    # Get updated room
    room = game_manager.get_room(request.room_code)
    
    # Broadcast to all clients in room
    await game_manager.broadcast_to_room(request.room_code, {
        "type": "question_generated",
        "question": result["question"],
        "selected_cell": request.cell_index,
        "room": room.dict()
    })
    
    return result

@api_router.post("/game/submit-answer")
async def submit_answer(request: AnswerRequest):
    """Handle answer submission"""
    result = game_manager.handle_answer(request.room_code, request.player_name, request.answer)
    if "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])
    
    # Get updated room
    room = game_manager.get_room(request.room_code)
    
    # Update player stats if game finished
    if result.get("winner"):
        await update_player_stats(result["winner"], won=True)
        # Update loser stats
        if room.player1["name"] != result["winner"]:
            await update_player_stats(room.player1["name"], won=False)
        else:
            await update_player_stats(room.player2["name"], won=False)
    
    # Broadcast result to all clients in room
    await game_manager.broadcast_to_room(request.room_code, {
        "type": "answer_result",
        "result": result,
        "room": room.dict()
    })
    
    return result

@api_router.post("/game/reset/{room_code}")
async def reset_game(room_code: str):
    """Reset the game in a room"""
    success = game_manager.reset_game(room_code)
    if not success:
        raise HTTPException(status_code=404, detail="Room not found")
    
    room = game_manager.get_room(room_code)
    
    # Broadcast reset to all clients
    await game_manager.broadcast_to_room(room_code, {
        "type": "game_reset",
        "room": room.dict()
    })
    
    return {"success": True}

@api_router.get("/players/ranking")
async def get_ranking():
    """Get global player ranking"""
    players = await db.players.find().sort("points", -1).limit(50).to_list(50)
    return {"ranking": players}

# WebSocket endpoint for real-time communication
@app.websocket("/ws/{room_code}")
async def websocket_endpoint(websocket: WebSocket, room_code: str):
    await websocket.accept()
    game_manager.add_connection(room_code, websocket)
    
    try:
        while True:
            # Keep connection alive and handle any incoming messages
            data = await websocket.receive_text()
            message = json.loads(data)
            
            # Handle different message types if needed
            if message.get("type") == "ping":
                await websocket.send_json({"type": "pong"})
                
    except WebSocketDisconnect:
        game_manager.remove_connection(room_code, websocket)

# Add your routes to the router instead of directly to app
@api_router.get("/")
async def root():
    return {"message": "Jogo da Velha Histórico - Multiplayer Online!"}

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
