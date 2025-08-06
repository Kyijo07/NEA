import json
import pygame

WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
TILE_SIZE = 40
SCREEN_SIZE = (800, 800)

characters = pygame.sprite.Group()
walls = pygame.sprite.Group()


class Wall(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.width = TILE_SIZE
        self.height = TILE_SIZE
        self.image = pygame.surface.Surface((TILE_SIZE, TILE_SIZE))
        self.image.fill(WHITE)
        pygame.draw.rect(self.image, (0, 0, 0), (0, 0, self.width, self.height))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


class Character(pygame.sprite.Sprite):
    def __init__(self, x, y, conn=None):
        super().__init__()
        self.width = TILE_SIZE
        self.height = TILE_SIZE
        self.image = pygame.image.load("rocket.png")
        self.image_orig = pygame.image.load("rocket.png")
        self.image_orig = pygame.transform.scale(self.image_orig, (self.width, self.height))
        self.image = pygame.transform.scale(self.image, (self.width, self.height))
        # self.image = pygame.surface.Surface((TILE_SIZE,TILE_SIZE))
        # self.image.fill(WHITE)
        # pygame.draw.rect(self.image,colour,(0,0,self.width,self.height))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.direction = "UP"
        self.connection = conn

    def rotate(self):
        angle = 0
        if self.direction == "DOWN":
            angle = 180
        elif self.direction == "LEFT":
            angle = 90
        elif self.direction == "RIGHT":
            angle = 270

        self.image = pygame.transform.rotate(self.image_orig, angle)

    def tell_server(self):
        if self.connection != None:
            packet = {"command": "MOVE", "data": {"xPos": self.rect.x, "yPos": self.rect.y}}
            self.connection.send(json.dumps(packet).encode())

    def move(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP]:
            self.rect.y -= 3
            self.direction = "UP"
            self.rotate()
            if pygame.sprite.spritecollide(self, walls, False):
                self.rect.y += 3
            if self.rect.y < 0:
                self.rect.y = 0
            self.tell_server()
        if keys[pygame.K_DOWN]:
            self.rect.y += 3
            self.direction = "DOWN"
            self.rotate()
            if pygame.sprite.spritecollide(self, walls, False):
                self.rect.y -= 3
            if self.rect.y > SCREEN_SIZE[1] - self.height:
                self.rect.y = SCREEN_SIZE[1] - self.height
            self.tell_server()
        if keys[pygame.K_LEFT]:
            self.rect.x -= 3
            self.direction = "LEFT"
            self.rotate()
            if pygame.sprite.spritecollide(self, walls, False):
                self.rect.x += 3
            if self.rect.x < 0:
                self.rect.x = 0
            self.tell_server()

        if keys[pygame.K_RIGHT]:
            self.rect.x += 3
            self.direction = "RIGHT"
            self.rotate()
            if pygame.sprite.spritecollide(self, walls, False):
                self.rect.x -= 3
            if self.rect.x > SCREEN_SIZE[0] - self.width:
                self.rect.x = SCREEN_SIZE[0] - self.width
            self.tell_server()
