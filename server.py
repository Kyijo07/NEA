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


def send_packet(conn, packet):
    try:
        conn.send((json.dumps(packet) + "\n").encode())
    except:
        if conn in clients:
            clients.remove(conn)


def broadcast(packet, skip_conn=None):
    for c in list(clients):
        if c != skip_conn:
            send_packet(c, packet)


def handle_client(conn, player_id):
    buffer = ""
    while True:
        try:
            data = conn.recv(4096).decode()
            if not data:
                break
            buffer += data
            while "\n" in buffer:
                line, buffer = buffer.split("\n", 1)
                if not line.strip():
                    continue
                packet = json.loads(line)
                if packet["command"] == "MOVE":
                    players[player_id] = packet["data"]
                    # broadcast updated position to others
                    broadcast({"command": "UPDATE_POS", "data": {player_id: packet["data"]}}, skip_conn=conn)
        except Exception as e:
            print(f"Client {player_id} disconnected: {e}")
            break

    # cleanup after disconnect
    if conn in clients:
        clients.remove(conn)
    if player_id in players:
        del players[player_id]


def main():
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
        send_packet(conn, setup_packet)

        threading.Thread(target=handle_client, args=(conn, player_id), daemon=True).start()


if __name__ == "__main__":
    main()
