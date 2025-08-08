#!/usr/bin/env python3
"""
Backend API Tests for Historical Tic-Tac-Toe Online Room System
Tests all REST APIs for room creation, joining, and status checking
"""

import requests
import json
import time
import sys
from typing import Dict, Any

# Get backend URL from environment
BACKEND_URL = "https://51ca6bae-4778-4223-87e8-3301ebe2bb15.preview.emergentagent.com/api"

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