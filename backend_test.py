import requests
import sys
import json
from datetime import datetime

class TicTacToeAPITester:
    def __init__(self, base_url="http://localhost:8001"):
        self.base_url = base_url
        self.tests_run = 0
        self.tests_passed = 0
        self.room_code = None
        self.player1_name = f"TestPlayer1_{datetime.now().strftime('%H%M%S')}"
        self.player2_name = f"TestPlayer2_{datetime.now().strftime('%H%M%S')}"

    def run_test(self, name, method, endpoint, expected_status, data=None):
        """Run a single API test"""
        url = f"{self.base_url}/{endpoint}"
        headers = {'Content-Type': 'application/json'}

        self.tests_run += 1
        print(f"\n🔍 Testing {name}...")
        
        try:
            if method == 'GET':
                response = requests.get(url, headers=headers, timeout=10)
            elif method == 'POST':
                response = requests.post(url, json=data, headers=headers, timeout=10)

            success = response.status_code == expected_status
            if success:
                self.tests_passed += 1
                print(f"✅ Passed - Status: {response.status_code}")
                try:
                    response_data = response.json()
                    print(f"   Response: {json.dumps(response_data, indent=2)[:200]}...")
                    return True, response_data
                except:
                    return True, {}
            else:
                print(f"❌ Failed - Expected {expected_status}, got {response.status_code}")
                try:
                    error_data = response.json()
                    print(f"   Error: {error_data}")
                except:
                    print(f"   Error: {response.text}")
                return False, {}

        except Exception as e:
            print(f"❌ Failed - Error: {str(e)}")
            return False, {}

    def test_root_endpoint(self):
        """Test the root API endpoint"""
        success, response = self.run_test(
            "Root API Endpoint",
            "GET",
            "api/",
            200
        )
        if success and 'total_questions' in response:
            if response['total_questions'] == 100:
                print(f"✅ Confirmed: API has {response['total_questions']} questions")
                return True
            else:
                print(f"❌ Expected 100 questions, got {response['total_questions']}")
                return False
        return success

    def test_create_room(self):
        """Test creating a game room"""
        success, response = self.run_test(
            "Create Game Room",
            "POST",
            "api/game/create-room",
            200,
            data={"player_name": self.player1_name}
        )
        if success and 'room_code' in response:
            self.room_code = response['room_code']
            print(f"✅ Room created with code: {self.room_code}")
            return True
        return success

    def test_join_room(self):
        """Test joining a game room"""
        if not self.room_code:
            print("❌ No room code available for join test")
            return False
            
        success, response = self.run_test(
            "Join Game Room",
            "POST",
            "api/game/join-room",
            200,
            data={"room_code": self.room_code, "player_name": self.player2_name}
        )
        if success and 'room' in response:
            room = response['room']
            if room.get('player1') and room.get('player2'):
                print(f"✅ Both players joined successfully")
                return True
        return success

    def test_get_room(self):
        """Test getting room information"""
        if not self.room_code:
            print("❌ No room code available for get room test")
            return False
            
        success, response = self.run_test(
            "Get Room Information",
            "GET",
            f"api/game/room/{self.room_code}",
            200
        )
        if success and 'room' in response:
            room = response['room']
            print(f"✅ Room info retrieved - Status: {room.get('game_status')}")
            return True
        return success

    def test_click_cell(self):
        """Test clicking a cell to generate question"""
        if not self.room_code:
            print("❌ No room code available for cell click test")
            return False
            
        success, response = self.run_test(
            "Click Cell (Generate Question)",
            "POST",
            "api/game/click-cell",
            200,
            data={
                "room_code": self.room_code,
                "player_name": self.player1_name,
                "cell_index": 0
            }
        )
        if success and 'question' in response:
            question = response['question']
            print(f"✅ Question generated: {question.get('question', '')[:50]}...")
            return True
        return success

    def test_submit_answer(self):
        """Test submitting an answer"""
        if not self.room_code:
            print("❌ No room code available for answer test")
            return False
            
        # First click a cell to get a question
        click_success, click_response = self.run_test(
            "Click Cell for Answer Test",
            "POST",
            "api/game/click-cell",
            200,
            data={
                "room_code": self.room_code,
                "player_name": self.player1_name,
                "cell_index": 1
            }
        )
        
        if not click_success or 'question' not in click_response:
            print("❌ Failed to generate question for answer test")
            return False
            
        question = click_response['question']
        correct_answer = question['correctAnswer']
        
        # Submit the correct answer
        success, response = self.run_test(
            "Submit Answer",
            "POST",
            "api/game/submit-answer",
            200,
            data={
                "room_code": self.room_code,
                "player_name": self.player1_name,
                "answer": correct_answer
            }
        )
        
        if success and 'correct' in response:
            if response['correct']:
                print(f"✅ Answer submitted correctly")
                return True
            else:
                print(f"❌ Answer marked as incorrect when it should be correct")
                return False
        return success

    def test_ranking_endpoint(self):
        """Test the ranking endpoint"""
        success, response = self.run_test(
            "Get Player Ranking",
            "GET",
            "api/players/ranking",
            200
        )
        if success and 'ranking' in response:
            ranking = response['ranking']
            print(f"✅ Ranking retrieved with {len(ranking)} players")
            return True
        return success

    def test_reset_game(self):
        """Test resetting a game"""
        if not self.room_code:
            print("❌ No room code available for reset test")
            return False
            
        success, response = self.run_test(
            "Reset Game",
            "POST",
            f"api/game/reset/{self.room_code}",
            200
        )
        if success and response.get('success'):
            print(f"✅ Game reset successfully")
            return True
        return success

def main():
    print("🎮 Starting Tic-Tac-Toe Historical Game API Tests")
    print("=" * 60)
    
    # Initialize tester
    tester = TicTacToeAPITester()
    
    # Run all tests
    tests = [
        tester.test_root_endpoint,
        tester.test_ranking_endpoint,
        tester.test_create_room,
        tester.test_join_room,
        tester.test_get_room,
        tester.test_click_cell,
        tester.test_submit_answer,
        tester.test_reset_game
    ]
    
    for test in tests:
        try:
            test()
        except Exception as e:
            print(f"❌ Test failed with exception: {str(e)}")
            tester.tests_run += 1
    
    # Print final results
    print("\n" + "=" * 60)
    print(f"📊 FINAL RESULTS")
    print(f"Tests Run: {tester.tests_run}")
    print(f"Tests Passed: {tester.tests_passed}")
    print(f"Success Rate: {(tester.tests_passed/tester.tests_run)*100:.1f}%")
    
    if tester.tests_passed == tester.tests_run:
        print("🎉 ALL TESTS PASSED!")
        return 0
    else:
        print("⚠️  SOME TESTS FAILED!")
        return 1

if __name__ == "__main__":
    sys.exit(main())