from pydantic import BaseModel, Field
from typing import List, Optional, Dict
from datetime import datetime
import uuid

class Player(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    name: str
    games: int = Field(default=0)
    wins: int = Field(default=0)
    losses: int = Field(default=0)
    points: int = Field(default=0)
    win_rate: float = Field(default=0.0)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

class GameRoom(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    code: str
    player1: Optional[Dict] = None
    player2: Optional[Dict] = None
    current_player: str = Field(default="X")
    board: List[Optional[str]] = Field(default_factory=lambda: [None] * 9)
    board_colors: List[Optional[str]] = Field(default_factory=lambda: [None] * 9)
    game_status: str = Field(default="waiting")  # waiting, playing, finished
    winner: Optional[str] = None
    current_question: Optional[Dict] = None
    selected_cell: Optional[int] = None
    score: Dict = Field(default_factory=lambda: {
        "playerX": {"correct": 0, "incorrect": 0},
        "playerO": {"correct": 0, "incorrect": 0}
    })
    used_questions: List[int] = Field(default_factory=list)
    created_at: datetime = Field(default_factory=datetime.utcnow)

class CreateRoomRequest(BaseModel):
    player_name: str

class JoinRoomRequest(BaseModel):
    room_code: str
    player_name: str

class AnswerRequest(BaseModel):
    room_code: str
    player_name: str
    answer: str
    cell_index: int

class CellClickRequest(BaseModel):
    room_code: str
    player_name: str
    cell_index: int