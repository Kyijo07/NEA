from worldGenerator import PerlinNoise
import pygame

colours = {}

seed = None
perlin = PerlinNoise(seed)
noise_map = perlin.generate_noise_map(500, 500, 10)
counter = 0
for i in noise_map:
    for noise in i:
        counter += 1
        if 0 <= noise <= 0.33:
            R = 35 + 112.12 * noise
            G = 47 + 366.67 * noise
            B = 207 - 457.58 * noise
        elif 0.33 <= noise <= 0.66:
            R = 72 + 175.76 * (noise - 0.33)
            G = 168 - 112.12 * (noise - 0.33)
            B = 56 + 254.55 * (noise - 0.33)
        else:
            R = 130 + 367.65 * (noise - 0.66)
            G = 131 + 364.71 * (noise - 0.66)
            B = 140 + 338.24 * (noise - 0.66)
        colour = R, G, B
        colours[counter] = colour
print(colours)

# Initialize Pygame
pygame.init()

# Set up display
screen_width, screen_height = 500, 500
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Coloured Tiles")


# Function to draw tiles
def draw_tiles(screen, colours, tile_size=1):
    for i, colour in enumerate(colours.values()):
        x = (i % screen_width) * tile_size
        y = (i // screen_height) * tile_size
        pygame.draw.rect(screen, colour, (x, y, tile_size, tile_size))


# Main game loop
clock = pygame.time.Clock()
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Fill the screen with white
    screen.fill((255, 255, 255))

    # Draw the tiles
    draw_tiles(screen, colours)

    # Update the display
    pygame.display.flip()
    pygame.display.update()
    clock.tick()
    print(clock.get_fps())

# Quit Pygame
pygame.quit()
quit()
