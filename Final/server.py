import json
import socket
import threading
import random

HOST = '127.0.0.1'
PORT = 50000

clients = []
players = {}  # player_id -> position
world_seed = random.randint(1, 1000000)  # generate world once

start_positions = [(200, 200), (500, 500)]  # adjust for more players

def broadcast(packet, skip_conn=None):
    for c in clients:
        if c != skip_conn:
            try:
                c.send(json.dumps(packet).encode())
            except:
                clients.remove(c)

def handle_client(conn, player_id):
    while True:
        try:
            data = conn.recv(1024)
            if not data:
                break
            packet = json.loads(data.decode())
            if packet["command"] == "MOVE":
                players[player_id] = packet["data"]
                # broadcast updated position to others
                broadcast({"command": "UPDATE_POS", "data": {player_id: packet["data"]}}, skip_conn=conn)
        except Exception as e:
            print(f"Client {player_id} disconnected: {e}")
            clients.remove(conn)
            del players[player_id]
            break

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((HOST, PORT))
s.listen()
print(f"Server listening on {HOST}:{PORT}, World Seed: {world_seed}")

player_count = 0
while True:
    conn, addr = s.accept()
    player_count += 1
    player_id = player_count
    clients.append(conn)
    px, py = start_positions[(player_id - 1) % len(start_positions)]
    players[player_id] = {"x": px, "y": py}

    # Send setup info
    setup_packet = {
        "command": "SETUP",
        "data": {
            "PlayerID": player_id,
            "PlayerX": px,
            "PlayerY": py,
            "WorldSeed": world_seed
        }
    }
    conn.send(json.dumps(setup_packet).encode())

    threading.Thread(target=handle_client, args=(conn, player_id), daemon=True).start()
