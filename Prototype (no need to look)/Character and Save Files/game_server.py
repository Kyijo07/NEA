import json
import socket
import threading
import time

HOST = '127.0.0.1'
PORT = 50000


def recv_from_client(conn, client_list):
    while True:
        data = conn.recv(1024)
        if data:
            print(data.decode())
            packet = json.loads(data.decode())
            for client in client_list:
                if client != conn:
                    client.send(json.dumps(packet).encode())


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((HOST, PORT))
client_list = []
player_positions = [(200, 200), (500, 500)]
print("Server is listening on port", PORT)
s.listen(1)
while True:
    conn, addr = s.accept()
    client_list.append(conn)
    print("New Connection from ", addr)
    threading.Thread(target=recv_from_client, args=(conn, client_list)).start()
    if len(client_list) % 2 == 1:
        player_pos = player_positions[0]
        enemy_pos = player_positions[1]
    else:
        player_pos = player_positions[1]
        enemy_pos = player_positions[0]
    message = {"command": "SETUP", "data": {"PlayerX": player_pos[0], "PlayerY": player_pos[1], "EnemyX": enemy_pos[0],
                                            "EnemyY": enemy_pos[1]}}
    conn.send(json.dumps(message).encode())
    time.sleep(1)
    if len(client_list) == 2:
        message = {"command": "START"}
        for c in client_list:
            c.send(json.dumps(message).encode())
