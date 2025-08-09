#!/usr/bin/env python3
"""
Focused test for the synchronization bug
"""

import asyncio
import json
import requests
import websockets
import uuid

BACKEND_URL = "https://91522345-49d4-43aa-8217-1f59e9996956.preview.emergentagent.com/api"

async def test_sync_bug():
    """Test the reported synchronization bug"""
    session = requests.Session()
    session.headers.update({
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    })
    
    print("🔍 TESTING ROOM CREATOR SYNCHRONIZATION BUG")
    print("=" * 60)
    
    # Step 1: Create room (TesterA)
    print("Step 1: Creating room with TesterA...")
    payload = {"player_name": "TesterA"}
    response = session.post(f"{BACKEND_URL}/rooms/create", json=payload)
    
    if response.status_code != 200:
        print(f"❌ Failed to create room: {response.status_code}")
        return False
    
    room_data = response.json()
    room_code = room_data["room_code"]
    creator_id = room_data["player_id"]
    print(f"✅ Room created: {room_code}, Creator ID: {creator_id}")
    
    # Step 2: Connect WebSocket as TesterA
    print("Step 2: Connecting WebSocket as TesterA...")
    ws_url_a = f"wss://049635f0-6eb8-4a9b-8b77-1b9642323842.preview.emergentagent.com/api/ws/{creator_id}"
    
    async with websockets.connect(ws_url_a) as ws_a:
        # Clear initial connected message
        await ws_a.recv()  # connected message
        
        # Send join_room
        await ws_a.send(json.dumps({"type": "join_room", "room_code": room_code}))
        
        # Get room_state
        room_state_msg = None
        for _ in range(5):
            try:
                response = await asyncio.wait_for(ws_a.recv(), timeout=3.0)
                msg = json.loads(response)
                if msg.get("type") == "room_state":
                    room_state_msg = msg
                    break
            except asyncio.TimeoutError:
                continue
        
        if not room_state_msg:
            print("❌ TesterA did not receive room_state")
            return False
        
        room_data_ws = room_state_msg.get("room", {})
        players_count_ws = len(room_data_ws.get("players", {}))
        current_player_id_ws = room_data_ws.get("current_player_id")
        
        print(f"✅ TesterA received room_state: {players_count_ws} players, current_player_id={current_player_id_ws}")
        
        # Step 3: Join room with TesterB via REST
        print("Step 3: Joining room with TesterB via REST...")
        payload = {"room_code": room_code, "player_name": "TesterB"}
        response = session.post(f"{BACKEND_URL}/rooms/join", json=payload)
        
        if response.status_code != 200:
            print(f"❌ Failed to join room: {response.status_code}")
            return False
        
        join_data = response.json()
        joiner_id = join_data["player_id"]
        print(f"✅ TesterB joined: {joiner_id}, room_status={join_data['room_status']}")
        
        # Step 4: Connect TesterB WebSocket
        print("Step 4: Connecting TesterB WebSocket...")
        ws_url_b = f"wss://049635f0-6eb8-4a9b-8b77-1b9642323842.preview.emergentagent.com/api/ws/{joiner_id}"
        
        async with websockets.connect(ws_url_b) as ws_b:
            # Clear initial connected message for B
            await ws_b.recv()  # connected message
            
            # Send join_room for B
            await ws_b.send(json.dumps({"type": "join_room", "room_code": room_code}))
            
            # Collect messages from both sockets
            messages_a = []
            messages_b = []
            
            # Collect messages for a few seconds
            for _ in range(10):
                try:
                    msg_a = await asyncio.wait_for(ws_a.recv(), timeout=1.5)
                    messages_a.append(json.loads(msg_a))
                    print(f"   A received: {json.loads(msg_a).get('type')}")
                except asyncio.TimeoutError:
                    pass
                
                try:
                    msg_b = await asyncio.wait_for(ws_b.recv(), timeout=1.5)
                    messages_b.append(json.loads(msg_b))
                    print(f"   B received: {json.loads(msg_b).get('type')}")
                except asyncio.TimeoutError:
                    pass
            
            # Analyze messages
            player_joined_a = [msg for msg in messages_a if msg.get("type") == "player_joined"]
            player_joined_b = [msg for msg in messages_b if msg.get("type") == "player_joined"]
            room_state_b = [msg for msg in messages_b if msg.get("type") == "room_state"]
            
            print(f"\n📊 Message Analysis:")
            print(f"   TesterA received {len(messages_a)} messages: {[msg.get('type') for msg in messages_a]}")
            print(f"   TesterB received {len(messages_b)} messages: {[msg.get('type') for msg in messages_b]}")
            
            # CRITICAL BUG DETECTION: Check for inconsistent player counts
            bug_detected = False
            players_seen_by_a = None
            players_seen_by_b = None
            
            if player_joined_a:
                # Get the latest player_joined message for A
                latest_joined_a = player_joined_a[-1]
                room_in_joined_a = latest_joined_a.get("room", {})
                players_seen_by_a = len(room_in_joined_a.get("players", {}))
                current_player_id_a = room_in_joined_a.get("current_player_id")
                print(f"   TesterA (creator) sees: {players_seen_by_a}/2 players, current_player_id={current_player_id_a}")
                print(f"   TesterA player_joined message: {json.dumps(latest_joined_a, indent=2)}")
            
            if room_state_b:
                room_in_state_b = room_state_b[0].get("room", {})
                players_seen_by_b = len(room_in_state_b.get("players", {}))
                current_player_id_b = room_in_state_b.get("current_player_id")
                print(f"   TesterB (joiner) sees: {players_seen_by_b}/2 players, current_player_id={current_player_id_b}")
                print(f"   TesterB room_state message: {json.dumps(room_state_b[0], indent=2)}")
            
            # DETECT THE REPORTED BUG
            if players_seen_by_a and players_seen_by_b:
                if players_seen_by_a != players_seen_by_b:
                    bug_detected = True
                    print(f"\n🚨 BUG DETECTED: Player count mismatch!")
                    print(f"   Creator (TesterA) sees: {players_seen_by_a}/2 players")
                    print(f"   Joiner (TesterB) sees: {players_seen_by_b}/2 players")
                    print(f"   This matches the reported bug: 'criador da sala vê 1/2 e não consegue jogar enquanto o outro vê 2/2'")
                else:
                    print(f"\n✅ Both players see consistent player count: {players_seen_by_a}/2")
            
            # Step 5: Test that creator (X) can get_question
            print("\nStep 5: Testing creator can get_question...")
            await ws_a.send(json.dumps({
                "type": "get_question",
                "room_code": room_code,
                "cell_index": 0
            }))
            
            # Check if creator receives question
            question_received = False
            question = None
            
            for _ in range(5):
                try:
                    response = await asyncio.wait_for(ws_a.recv(), timeout=3.0)
                    msg = json.loads(response)
                    if msg.get("type") == "question":
                        question_received = True
                        question = msg.get("question")
                        print(f"✅ Creator received question: {question.get('id') if question else 'None'}")
                        break
                except asyncio.TimeoutError:
                    continue
            
            if not question_received:
                print(f"❌ Creator (TesterA) could not get question - this confirms the reported bug!")
                bug_detected = True
            
            # Final assessment
            if bug_detected:
                print(f"\n🚨 SYNCHRONIZATION BUG CONFIRMED!")
                print(f"   The reported issue exists: creator and joiner see different player counts")
                return False
            else:
                print(f"\n✅ NO SYNCHRONIZATION BUG DETECTED")
                print(f"   Both players see consistent state and creator can play")
                return True

if __name__ == "__main__":
    result = asyncio.run(test_sync_bug())
    print(f"\nTest result: {'PASSED' if result else 'FAILED'}")