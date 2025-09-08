import pygame
import sys

# Initialize pygame
pygame.init()

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60

# Colors
WHITE = (255, 255, 255)
BLUE = (0, 100, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)


class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = 40
        self.height = 40
        self.speed = 5
        self.color = BLUE

    def move(self, dx, dy):
        # Update position
        self.x += dx * self.speed
        self.y += dy * self.speed

        # Keep player on screen
        if self.x < 0:
            self.x = 0
        elif self.x > SCREEN_WIDTH - self.width:
            self.x = SCREEN_WIDTH - self.width

        if self.y < 0:
            self.y = 0
        elif self.y > SCREEN_HEIGHT - self.height:
            self.y = SCREEN_HEIGHT - self.height

    def draw(self, screen):
        # Draw the character as a rectangle
        pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height))

def main():
    # Create screen
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Moving Character")
    clock = pygame.time.Clock()

    # Create player
    player = Player(SCREEN_WIDTH // 2 - 20, SCREEN_HEIGHT // 2 - 20)

    # Game loop
    running = True
    while running:
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Handle continuous key presses
        keys = pygame.key.get_pressed()
        dx, dy = 0, 0

        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            dx = -1
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            dx = 1
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            dy = -1
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            dy = 1

        # Update player position
        player.move(dx, dy)

        # Draw everything
        screen.fill(WHITE)
        player.draw(screen)

        # Add instructions
        font = pygame.font.Font(None, 36)
        text = font.render("Use Arrow Keys or WASD to move.", True, BLACK)
        screen.blit(text, (10, 10))

        # Update display
        pygame.display.flip()
        clock.tick(FPS)

    # Quit
    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()