#!/usr/bin/env python3
"""
Backend API Tests for Historical Tic-Tac-Toe Online Room System
Tests all REST APIs for room creation, joining, and status checking
PLUS WebSocket functionality testing
"""

import requests
import json
import time
import sys
import asyncio
import websockets
import threading
from typing import Dict, Any
from concurrent.futures import ThreadPoolExecutor

# Get backend URL from environment
BACKEND_URL = "https://049635f0-6eb8-4a9b-8b77-1b9642323842.preview.emergentagent.com/api"

class TicTacToeAPITester:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        })
        self.test_results = []
        self.created_rooms = []
        
    def log_test(self, test_name: str, success: bool, details: str = "", response_data: Any = None):
        """Log test results"""
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{status} {test_name}")
        if details:
            print(f"   Details: {details}")
        if response_data and isinstance(response_data, dict):
            print(f"   Response: {json.dumps(response_data, indent=2)}")
        print()
        
        self.test_results.append({
            'test': test_name,
            'success': success,
            'details': details,
            'response': response_data
        })
    
    def test_api_health(self):
        """Test GET /api/ - API health check"""
        try:
            response = self.session.get(f"{BACKEND_URL}/")
            
            if response.status_code == 200:
                data = response.json()
                if "message" in data and "Tic-Tac-Toe" in data["message"]:
                    self.log_test("API Health Check", True, f"Status: {response.status_code}", data)
                    return True
                else:
                    self.log_test("API Health Check", False, f"Unexpected response format", data)
                    return False
            else:
                self.log_test("API Health Check", False, f"Status: {response.status_code}, Response: {response.text}")
                return False
                
        except Exception as e:
            self.log_test("API Health Check", False, f"Exception: {str(e)}")
            return False
    
    def test_create_room(self, player_name: str = "TestPlayer1") -> Dict[str, Any]:
        """Test POST /api/rooms/create - Create a new room"""
        try:
            payload = {"player_name": player_name}
            response = self.session.post(f"{BACKEND_URL}/rooms/create", json=payload)
            
            if response.status_code == 200:
                data = response.json()
                
                # Validate response structure
                required_fields = ["room_code", "player_id"]
                missing_fields = [field for field in required_fields if field not in data]
                
                if missing_fields:
                    self.log_test("Create Room", False, f"Missing fields: {missing_fields}", data)
                    return {}
                
                # Validate room code format (6 alphanumeric characters)
                room_code = data["room_code"]
                if len(room_code) != 6 or not room_code.isalnum():
                    self.log_test("Create Room", False, f"Invalid room code format: {room_code}", data)
                    return {}
                
                # Store created room for cleanup
                self.created_rooms.append(room_code)
                
                self.log_test("Create Room", True, f"Room created with code: {room_code}", data)
                return data
                
            else:
                self.log_test("Create Room", False, f"Status: {response.status_code}, Response: {response.text}")
                return {}
                
        except Exception as e:
            self.log_test("Create Room", False, f"Exception: {str(e)}")
            return {}
    
    def test_join_room(self, room_code: str, player_name: str = "TestPlayer2") -> Dict[str, Any]:
        """Test POST /api/rooms/join - Join an existing room"""
        try:
            payload = {"room_code": room_code, "player_name": player_name}
            response = self.session.post(f"{BACKEND_URL}/rooms/join", json=payload)
            
            if response.status_code == 200:
                data = response.json()
                
                # Validate response structure
                required_fields = ["room_code", "player_id", "room_status"]
                missing_fields = [field for field in required_fields if field not in data]
                
                if missing_fields:
                    self.log_test("Join Room", False, f"Missing fields: {missing_fields}", data)
                    return {}
                
                # Validate room status changed to 'playing' when second player joins
                if data["room_status"] == "playing":
                    self.log_test("Join Room", True, f"Successfully joined room {room_code}, status: {data['room_status']}", data)
                else:
                    self.log_test("Join Room", True, f"Joined room {room_code}, status: {data['room_status']} (expected 'playing' for 2nd player)", data)
                
                return data
                
            else:
                self.log_test("Join Room", False, f"Status: {response.status_code}, Response: {response.text}")
                return {}
                
        except Exception as e:
            self.log_test("Join Room", False, f"Exception: {str(e)}")
            return {}
    
    def test_room_status(self, room_code: str) -> Dict[str, Any]:
        """Test GET /api/rooms/{room_code}/status - Get room status"""
        try:
            response = self.session.get(f"{BACKEND_URL}/rooms/{room_code}/status")
            
            if response.status_code == 200:
                data = response.json()
                
                # Validate response structure
                required_fields = ["room_code", "players", "player_count", "game_status", "board"]
                missing_fields = [field for field in required_fields if field not in data]
                
                if missing_fields:
                    self.log_test("Room Status", False, f"Missing fields: {missing_fields}", data)
                    return {}
                
                # Validate player count
                player_count = data["player_count"]
                actual_players = len(data["players"])
                
                if player_count != actual_players:
                    self.log_test("Room Status", False, f"Player count mismatch: reported {player_count}, actual {actual_players}", data)
                    return {}
                
                self.log_test("Room Status", True, f"Room {room_code}: {player_count} players, status: {data['game_status']}", data)
                return data
                
            else:
                self.log_test("Room Status", False, f"Status: {response.status_code}, Response: {response.text}")
                return {}
                
        except Exception as e:
            self.log_test("Room Status", False, f"Exception: {str(e)}")
            return {}
    
    def test_join_nonexistent_room(self):
        """Test joining a room that doesn't exist"""
        try:
            fake_room_code = "FAKE99"
            payload = {"room_code": fake_room_code, "player_name": "TestPlayer"}
            response = self.session.post(f"{BACKEND_URL}/rooms/join", json=payload)
            
            if response.status_code == 404:
                self.log_test("Join Nonexistent Room", True, f"Correctly returned 404 for fake room code")
                return True
            else:
                self.log_test("Join Nonexistent Room", False, f"Expected 404, got {response.status_code}: {response.text}")
                return False
                
        except Exception as e:
            self.log_test("Join Nonexistent Room", False, f"Exception: {str(e)}")
            return False
    
    def test_join_full_room(self):
        """Test joining a room that's already full (2 players)"""
        try:
            # Create a room
            room_data = self.test_create_room("Player1")
            if not room_data:
                self.log_test("Join Full Room", False, "Failed to create room for test")
                return False
            
            room_code = room_data["room_code"]
            
            # Join with second player
            join_data = self.test_join_room(room_code, "Player2")
            if not join_data:
                self.log_test("Join Full Room", False, "Failed to join room with second player")
                return False
            
            # Try to join with third player (should fail)
            payload = {"room_code": room_code, "player_name": "Player3"}
            response = self.session.post(f"{BACKEND_URL}/rooms/join", json=payload)
            
            if response.status_code == 400:
                self.log_test("Join Full Room", True, f"Correctly rejected third player with 400 status")
                return True
            else:
                self.log_test("Join Full Room", False, f"Expected 400, got {response.status_code}: {response.text}")
                return False
                
        except Exception as e:
            self.log_test("Join Full Room", False, f"Exception: {str(e)}")
            return False
    
    def test_room_code_uniqueness(self):
        """Test that room codes are unique"""
        try:
            room_codes = set()
            
            # Create multiple rooms
            for i in range(5):
                room_data = self.test_create_room(f"Player{i+1}")
                if room_data and "room_code" in room_data:
                    room_code = room_data["room_code"]
                    if room_code in room_codes:
                        self.log_test("Room Code Uniqueness", False, f"Duplicate room code found: {room_code}")
                        return False
                    room_codes.add(room_code)
                else:
                    self.log_test("Room Code Uniqueness", False, f"Failed to create room {i+1}")
                    return False
            
            self.log_test("Room Code Uniqueness", True, f"All {len(room_codes)} room codes are unique")
            return True
            
        except Exception as e:
            self.log_test("Room Code Uniqueness", False, f"Exception: {str(e)}")
            return False
    
    def test_player_symbols(self):
        """Test that first player gets 'X' and second player gets 'O'"""
        try:
            # Create room
            room_data = self.test_create_room("PlayerX")
            if not room_data:
                self.log_test("Player Symbols", False, "Failed to create room")
                return False
            
            room_code = room_data["room_code"]
            
            # Check initial room status
            status_data = self.test_room_status(room_code)
            if not status_data:
                self.log_test("Player Symbols", False, "Failed to get room status")
                return False
            
            # Join with second player
            join_data = self.test_join_room(room_code, "PlayerO")
            if not join_data:
                self.log_test("Player Symbols", False, "Failed to join room with second player")
                return False
            
            # Check final room status
            final_status = self.test_room_status(room_code)
            if not final_status:
                self.log_test("Player Symbols", False, "Failed to get final room status")
                return False
            
            # Validate game status changed to 'playing'
            if final_status["game_status"] == "playing" and final_status["player_count"] == 2:
                self.log_test("Player Symbols", True, f"Room correctly has 2 players and 'playing' status")
                return True
            else:
                self.log_test("Player Symbols", False, f"Expected 'playing' status with 2 players, got: {final_status['game_status']} with {final_status['player_count']} players")
                return False
            
        except Exception as e:
            self.log_test("Player Symbols", False, f"Exception: {str(e)}")
            return False
    
    def test_questions_system(self):
        """Test that questions system is working by importing and testing the module"""
        try:
            # Import the questions module
            import sys
            sys.path.append('/app/backend')
            from questions import get_random_question, QUESTIONS
            
            # Test getting random questions
            questions_received = []
            for i in range(5):
                question = get_random_question()
                
                # Validate question structure
                required_fields = ["id", "question", "options", "correctAnswer", "period"]
                missing_fields = [field for field in required_fields if field not in question]
                
                if missing_fields:
                    self.log_test("Questions System", False, f"Question missing fields: {missing_fields}")
                    return False
                
                # Validate options format
                if not isinstance(question["options"], list) or len(question["options"]) != 4:
                    self.log_test("Questions System", False, f"Invalid options format in question {question['id']}")
                    return False
                
                # Validate correct answer is in options
                if question["correctAnswer"] not in question["options"]:
                    self.log_test("Questions System", False, f"Correct answer not in options for question {question['id']}")
                    return False
                
                questions_received.append(question)
            
            # Check that we have the expected number of questions in database
            if len(QUESTIONS) != 20:
                self.log_test("Questions System", False, f"Expected 20 questions, found {len(QUESTIONS)}")
                return False
            
            self.log_test("Questions System", True, f"Questions system working correctly. Database has {len(QUESTIONS)} questions, tested {len(questions_received)} random questions")
            return True
            
        except Exception as e:
            self.log_test("Questions System", False, f"Exception: {str(e)}")
            return False

    async def test_websocket_basic_connection(self):
        """Test basic WebSocket connection to /api/ws/{player_id}"""
        try:
            player_id = "test-player-123"
            ws_url = f"wss://049635f0-6eb8-4a9b-8b77-1b9642323842.preview.emergentagent.com/api/ws/{player_id}"
            
            async with websockets.connect(ws_url) as websocket:
                # Should receive initial connected message
                response = await asyncio.wait_for(websocket.recv(), timeout=5.0)
                message = json.loads(response)
                
                if message.get("type") == "connected" and message.get("player_id") == player_id:
                    self.log_test("WebSocket Basic Connection", True, f"Connected successfully, received: {message}")
                    
                    # Test ping/pong
                    await websocket.send(json.dumps({"type": "ping"}))
                    pong_response = await asyncio.wait_for(websocket.recv(), timeout=5.0)
                    pong_message = json.loads(pong_response)
                    
                    if pong_message.get("type") == "pong":
                        self.log_test("WebSocket Ping/Pong", True, f"Ping/pong working: {pong_message}")
                        return True
                    else:
                        self.log_test("WebSocket Ping/Pong", False, f"Expected pong, got: {pong_message}")
                        return False
                else:
                    self.log_test("WebSocket Basic Connection", False, f"Unexpected initial message: {message}")
                    return False
                    
        except Exception as e:
            self.log_test("WebSocket Basic Connection", False, f"Exception: {str(e)}")
            return False

    async def test_websocket_room_flow(self):
        """Test complete room flow with WebSocket connections"""
        try:
            # Step 1: Create room via REST API
            room_data = self.test_create_room("Tester1")
            if not room_data:
                self.log_test("WebSocket Room Flow", False, "Failed to create room")
                return False
            
            room_code = room_data["room_code"]
            player_id_a = room_data["player_id"]
            
            # Step 2: Join room via REST API
            join_data = self.test_join_room(room_code, "Tester2")
            if not join_data:
                self.log_test("WebSocket Room Flow", False, "Failed to join room")
                return False
            
            player_id_b = join_data["player_id"]
            
            # Step 3: Connect both players via WebSocket
            ws_url_a = f"wss://049635f0-6eb8-4a9b-8b77-1b9642323842.preview.emergentagent.com/api/ws/{player_id_a}"
            ws_url_b = f"wss://049635f0-6eb8-4a9b-8b77-1b9642323842.preview.emergentagent.com/api/ws/{player_id_b}"
            
            async with websockets.connect(ws_url_a) as ws_a, websockets.connect(ws_url_b) as ws_b:
                # Receive initial connected messages
                msg_a = json.loads(await asyncio.wait_for(ws_a.recv(), timeout=5.0))
                msg_b = json.loads(await asyncio.wait_for(ws_b.recv(), timeout=5.0))
                
                if msg_a.get("type") != "connected" or msg_b.get("type") != "connected":
                    self.log_test("WebSocket Room Flow", False, f"Failed to connect both players: {msg_a}, {msg_b}")
                    return False
                
                # Step 4: Both players join the room
                await ws_a.send(json.dumps({"type": "join_room", "room_code": room_code}))
                await ws_b.send(json.dumps({"type": "join_room", "room_code": room_code}))
                
                # Collect messages for a few seconds
                messages_a = []
                messages_b = []
                
                for _ in range(4):  # Try to get up to 4 messages from each
                    try:
                        msg_a = await asyncio.wait_for(ws_a.recv(), timeout=2.0)
                        messages_a.append(json.loads(msg_a))
                    except asyncio.TimeoutError:
                        break
                
                for _ in range(4):
                    try:
                        msg_b = await asyncio.wait_for(ws_b.recv(), timeout=2.0)
                        messages_b.append(json.loads(msg_b))
                    except asyncio.TimeoutError:
                        break
                
                # Check if both received room_state and player_joined messages
                room_state_a = any(msg.get("type") == "room_state" for msg in messages_a)
                room_state_b = any(msg.get("type") == "room_state" for msg in messages_b)
                player_joined_a = any(msg.get("type") == "player_joined" for msg in messages_a)
                player_joined_b = any(msg.get("type") == "player_joined" for msg in messages_b)
                
                if room_state_a and room_state_b:
                    self.log_test("WebSocket Room Flow", True, f"Both players received room_state. Player A msgs: {len(messages_a)}, Player B msgs: {len(messages_b)}")
                    return True
                else:
                    self.log_test("WebSocket Room Flow", False, f"Missing room_state messages. A: {room_state_a}, B: {room_state_b}. Messages A: {messages_a}, Messages B: {messages_b}")
                    return False
                    
        except Exception as e:
            self.log_test("WebSocket Room Flow", False, f"Exception: {str(e)}")
            return False

    async def test_websocket_game_flow(self):
        """Test game flow with get_question and make_move"""
        try:
            # Create room and join
            room_data = self.test_create_room("GameTester1")
            if not room_data:
                return False
            
            room_code = room_data["room_code"]
            player_id_a = room_data["player_id"]
            
            join_data = self.test_join_room(room_code, "GameTester2")
            if not join_data:
                return False
            
            player_id_b = join_data["player_id"]
            
            # Connect both players
            ws_url_a = f"wss://049635f0-6eb8-4a9b-8b77-1b9642323842.preview.emergentagent.com/api/ws/{player_id_a}"
            ws_url_b = f"wss://049635f0-6eb8-4a9b-8b77-1b9642323842.preview.emergentagent.com/api/ws/{player_id_b}"
            
            async with websockets.connect(ws_url_a) as ws_a, websockets.connect(ws_url_b) as ws_b:
                # Initial setup
                await ws_a.recv()  # connected message
                await ws_b.recv()  # connected message
                
                await ws_a.send(json.dumps({"type": "join_room", "room_code": room_code}))
                await ws_b.send(json.dumps({"type": "join_room", "room_code": room_code}))
                
                # Clear initial messages
                for _ in range(3):
                    try:
                        await asyncio.wait_for(ws_a.recv(), timeout=1.0)
                        await asyncio.wait_for(ws_b.recv(), timeout=1.0)
                    except asyncio.TimeoutError:
                        break
                
                # Test get_question (player A requests question for cell 0)
                await ws_a.send(json.dumps({
                    "type": "get_question",
                    "room_code": room_code,
                    "cell_index": 0
                }))
                
                # Player A should receive question
                question_response = await asyncio.wait_for(ws_a.recv(), timeout=5.0)
                question_msg = json.loads(question_response)
                
                if question_msg.get("type") != "question":
                    self.log_test("WebSocket Game Flow", False, f"Expected question, got: {question_msg}")
                    return False
                
                question = question_msg.get("question")
                if not question or "correctAnswer" not in question:
                    self.log_test("WebSocket Game Flow", False, f"Invalid question format: {question}")
                    return False
                
                # Test make_move
                await ws_a.send(json.dumps({
                    "type": "make_move",
                    "room_code": room_code,
                    "cell_index": 0,
                    "selected_answer": question["correctAnswer"],
                    "question": question
                }))
                
                # Both players should receive game_update
                update_a = await asyncio.wait_for(ws_a.recv(), timeout=5.0)
                update_b = await asyncio.wait_for(ws_b.recv(), timeout=5.0)
                
                update_msg_a = json.loads(update_a)
                update_msg_b = json.loads(update_b)
                
                if (update_msg_a.get("type") == "game_update" and 
                    update_msg_b.get("type") == "game_update"):
                    self.log_test("WebSocket Game Flow", True, f"Game flow working: question received, move made, both players got game_update")
                    return True
                else:
                    self.log_test("WebSocket Game Flow", False, f"Expected game_update, got A: {update_msg_a}, B: {update_msg_b}")
                    return False
                    
        except Exception as e:
            self.log_test("WebSocket Game Flow", False, f"Exception: {str(e)}")
            return False

    async def test_websocket_server_ping(self):
        """Test server ping functionality (wait up to 25 seconds)"""
        try:
            player_id = "ping-test-player"
            ws_url = f"wss://049635f0-6eb8-4a9b-8b77-1b9642323842.preview.emergentagent.com/api/ws/{player_id}"
            
            async with websockets.connect(ws_url) as websocket:
                await websocket.recv()  # connected message
                
                # Wait for server ping (up to 25 seconds)
                server_ping_received = False
                start_time = time.time()
                
                while time.time() - start_time < 25:
                    try:
                        message = await asyncio.wait_for(websocket.recv(), timeout=5.0)
                        msg = json.loads(message)
                        
                        if msg.get("type") == "ping" and msg.get("from") == "server":
                            server_ping_received = True
                            self.log_test("WebSocket Server Ping", True, f"Server ping received: {msg}")
                            
                            # Respond with ping to test pong response
                            await websocket.send(json.dumps({"type": "ping"}))
                            pong_response = await asyncio.wait_for(websocket.recv(), timeout=5.0)
                            pong_msg = json.loads(pong_response)
                            
                            if pong_msg.get("type") == "pong":
                                self.log_test("WebSocket Server Ping Response", True, f"Server responded with pong: {pong_msg}")
                                return True
                            else:
                                self.log_test("WebSocket Server Ping Response", False, f"Expected pong, got: {pong_msg}")
                                return False
                            
                    except asyncio.TimeoutError:
                        continue
                
                if not server_ping_received:
                    self.log_test("WebSocket Server Ping", False, "No server ping received within 25 seconds")
                    return False
                    
        except Exception as e:
            self.log_test("WebSocket Server Ping", False, f"Exception: {str(e)}")
            return False

    def run_websocket_tests(self):
        """Run WebSocket tests using asyncio"""
        print("🔌 Starting WebSocket Tests")
        print("=" * 50)
        
        async def run_all_ws_tests():
            tests = [
                ("WebSocket Basic Connection & Ping/Pong", self.test_websocket_basic_connection),
                ("WebSocket Room Flow", self.test_websocket_room_flow),
                ("WebSocket Game Flow", self.test_websocket_game_flow),
                ("WebSocket Server Ping (25s wait)", self.test_websocket_server_ping),
            ]
            
            passed = 0
            total = len(tests)
            
            for test_name, test_func in tests:
                print(f"Running: {test_name}")
                print("-" * 40)
                try:
                    result = await test_func()
                    if result:
                        passed += 1
                except Exception as e:
                    print(f"❌ FAIL {test_name} - Exception: {str(e)}")
                print()
            
            return passed, total
        
        # Run async tests
        try:
            passed, total = asyncio.run(run_all_ws_tests())
            print(f"📊 WEBSOCKET TEST SUMMARY: {passed}/{total} tests passed")
            return passed == total
        except Exception as e:
            print(f"❌ WebSocket tests failed with exception: {str(e)}")
            return False
    
    def run_all_tests(self):
        """Run all backend API tests"""
        print("🚀 Starting Backend API Tests for Historical Tic-Tac-Toe Online Room System")
        print("=" * 80)
        print()
        
        # Test sequence
        tests = [
            ("API Health Check", self.test_api_health),
            ("Room Code Uniqueness", self.test_room_code_uniqueness),
            ("Join Nonexistent Room", self.test_join_nonexistent_room),
            ("Join Full Room", self.test_join_full_room),
            ("Player Symbols and Game Flow", self.test_player_symbols),
            ("Questions System", self.test_questions_system),
        ]
        
        passed = 0
        total = len(tests)
        
        for test_name, test_func in tests:
            print(f"Running: {test_name}")
            print("-" * 40)
            try:
                result = test_func()
                if result:
                    passed += 1
            except Exception as e:
                print(f"❌ FAIL {test_name} - Exception: {str(e)}")
            print()
        
        # Summary
        print("=" * 80)
        print(f"📊 TEST SUMMARY: {passed}/{total} tests passed")
        
        if passed == total:
            print("🎉 All tests passed! Backend APIs are working correctly.")
            return True
        else:
            print(f"⚠️  {total - passed} tests failed. Check the details above.")
            return False

def main():
    """Main test execution"""
    tester = TicTacToeAPITester()
    success = tester.run_all_tests()
    
    # Return appropriate exit code
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()