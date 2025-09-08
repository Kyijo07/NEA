import json
import pygame
import socket
import threading

from game_classes import SCREEN_SIZE, TILE_SIZE, walls, bullets, characters, Wall, Character
from game_classes import WHITE, BLACK

HOST = '127.0.0.1'
PORT = 50000

with open('../World Generation/example.txt', 'r') as file:
    MAP = file.read()

type(MAP)

Waiting = True


def recv_from_server(conn):
    global Waiting
    while True:
        data = conn.recv(1024)
        if data:
            packet = json.loads(data.decode())
            print(packet)
            if packet["command"] == "START":
                Waiting = False
            if packet["command"] == "SETUP":
                c = Character(int(packet["data"]["PlayerX"]), int(packet["data"]["PlayerY"]), conn)
                characters.add(c)
                enemy = Character(int(packet["data"]["EnemyX"]), int(packet["data"]["EnemyY"]))
                characters.add(enemy)
            if packet["command"] == "MOVE":
                enemy.rect.x = packet["data"]["xPos"]
                enemy.rect.y = packet["data"]["yPos"]


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))
threading.Thread(target=recv_from_server, args=(s,)).start()

pygame.display.init()
pygame.font.init()
screen = pygame.display.set_mode(SCREEN_SIZE)
clock = pygame.time.Clock()


def wait_screen():
    global Waiting
    text = "Waiting for the other player to connect"
    f = pygame.font.SysFont("Arial", 24)
    output = f.render(text, True, BLACK)
    running = True
    while Waiting:
        screen.fill(WHITE)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                Waiting = False
        screen.blit(output, (200, 400))
        pygame.display.update()
    return running


y = 0
for row in MAP:
    x = 0
    for cell in row:
        if cell == "1":
            w = Wall(x * TILE_SIZE, y * TILE_SIZE)
            walls.add(w)
        x += 1
    y += 1

running = wait_screen()

player = characters.sprites()[0]

while running:
    screen.fill(WHITE)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            keys = pygame.key.get_pressed()
            if keys[pygame.K_SPACE]:
                player.fire()

    player.move()
    bullets.update()
    walls.draw(screen)
    bullets.draw(screen)
    characters.draw(screen)
    clock.tick(60)
    pygame.display.update()
