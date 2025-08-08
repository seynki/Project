import random
import string
from typing import Dict, Optional, List
from datetime import datetime
import asyncio
from models import GameRoom, Player
from questions import QUESTIONS

class GameManager:
    def __init__(self):
        self.rooms: Dict[str, GameRoom] = {}
        self.connections: Dict[str, List] = {}  # room_code -> [websockets]
        
    def generate_room_code(self) -> str:
        """Generate a unique 6-character room code"""
        while True:
            code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
            if code not in self.rooms:
                return code
    
    def create_room(self, player_name: str) -> GameRoom:
        """Create a new game room"""
        code = self.generate_room_code()
        room = GameRoom(
            code=code,
            player1={
                "name": player_name,
                "symbol": "X"
            }
        )
        self.rooms[code] = room
        self.connections[code] = []
        return room
    
    def join_room(self, room_code: str, player_name: str) -> Optional[GameRoom]:
        """Join an existing room"""
        if room_code not in self.rooms:
            return None
            
        room = self.rooms[room_code]
        
        # Check if room is full
        if room.player1 and room.player2:
            return None
            
        # Add player2
        if room.player1 and not room.player2:
            room.player2 = {
                "name": player_name,
                "symbol": "O"
            }
            room.game_status = "playing"
            
        return room
    
    def get_room(self, room_code: str) -> Optional[GameRoom]:
        """Get room by code"""
        return self.rooms.get(room_code)
    
    def get_random_question(self, used_questions: List[int]) -> Dict:
        """Get a random question that hasn't been used"""
        available = [q for q in QUESTIONS if q["id"] not in used_questions]
        if not available:
            available = QUESTIONS
        return random.choice(available)
    
    def handle_cell_click(self, room_code: str, player_name: str, cell_index: int) -> Dict:
        """Handle cell click - generate question"""
        room = self.rooms.get(room_code)
        if not room:
            return {"error": "Room not found"}
            
        # Validate player turn
        current_symbol = room.current_player
        current_name = room.player1["name"] if current_symbol == "X" else room.player2["name"]
        
        if player_name != current_name:
            return {"error": "Not your turn"}
            
        # Check if cell is clickable
        if room.board[cell_index] is not None and room.board_colors[cell_index] != "red":
            return {"error": "Cell not available"}
            
        # Generate question
        question = self.get_random_question(room.used_questions)
        room.current_question = question
        room.selected_cell = cell_index
        
        return {"success": True, "question": question}
    
    def check_winner(self, board: List, board_colors: List) -> Optional[str]:
        """Check if there's a winner"""
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
    
    def handle_answer(self, room_code: str, player_name: str, answer: str) -> Dict:
        """Handle answer submission"""
        room = self.rooms.get(room_code)
        if not room or not room.current_question:
            return {"error": "No active question"}
            
        question = room.current_question
        is_correct = answer == question["correctAnswer"]
        cell_index = room.selected_cell
        
        # Update board
        current_symbol = room.current_player
        room.board[cell_index] = current_symbol
        room.board_colors[cell_index] = "green" if is_correct else "red"
        
        # Update score
        player_key = "playerX" if current_symbol == "X" else "playerO"
        if is_correct:
            room.score[player_key]["correct"] += 1
        else:
            room.score[player_key]["incorrect"] += 1
            
        # Add to used questions
        room.used_questions.append(question["id"])
        
        # Check for winner
        winner = self.check_winner(room.board, room.board_colors)
        if winner:
            room.game_status = "finished"
            winner_name = room.player1["name"] if winner == "X" else room.player2["name"]
            room.winner = winner_name
            
        elif all(cell is not None for cell in room.board):
            # Check for draw
            room.game_status = "finished"
            room.winner = None
            
        else:
            # Switch player
            room.current_player = "O" if current_symbol == "X" else "X"
            
        # Clear current question
        room.current_question = None
        room.selected_cell = None
        
        return {
            "success": True,
            "correct": is_correct,
            "correct_answer": question["correctAnswer"] if not is_correct else None,
            "winner": room.winner if room.game_status == "finished" else None,
            "game_status": room.game_status
        }
    
    def reset_game(self, room_code: str) -> bool:
        """Reset game in room"""
        room = self.rooms.get(room_code)
        if not room:
            return False
            
        room.board = [None] * 9
        room.board_colors = [None] * 9
        room.current_player = "X"
        room.game_status = "playing"
        room.winner = None
        room.current_question = None
        room.selected_cell = None
        room.score = {
            "playerX": {"correct": 0, "incorrect": 0},
            "playerO": {"correct": 0, "incorrect": 0}
        }
        room.used_questions = []
        
        return True
        
    def add_connection(self, room_code: str, websocket):
        """Add websocket connection to room"""
        if room_code not in self.connections:
            self.connections[room_code] = []
        self.connections[room_code].append(websocket)
    
    def remove_connection(self, room_code: str, websocket):
        """Remove websocket connection from room"""
        if room_code in self.connections:
            if websocket in self.connections[room_code]:
                self.connections[room_code].remove(websocket)
    
    async def broadcast_to_room(self, room_code: str, message: Dict):
        """Broadcast message to all connections in room"""
        if room_code not in self.connections:
            return
            
        disconnected = []
        for websocket in self.connections[room_code]:
            try:
                await websocket.send_json(message)
            except:
                disconnected.append(websocket)
        
        # Remove disconnected websockets
        for ws in disconnected:
            self.connections[room_code].remove(ws)

# Global game manager instance
game_manager = GameManager()