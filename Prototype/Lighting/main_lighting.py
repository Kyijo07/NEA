import pygame
import math


class Light:
    def __init__(self, x, y, radius, color=(255, 255, 255)):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color


class Wall:
    def __init__(self, x1, y1, x2, y2):
        self.x1, self.y1 = x1, y1
        self.x2, self.y2 = x2, y2


def line_intersect(x1, y1, x2, y2, x3, y3, x4, y4):
    """Check if ray intersects wall"""
    denom = (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4)
    if abs(denom) < 0.001:
        return None

    t = ((x1 - x3) * (y3 - y4) - (y1 - y3) * (x3 - x4)) / denom
    u = -((x1 - x2) * (y1 - y3) - (y1 - y2) * (x1 - x3)) / denom

    if t >= 0 and 0 <= u <= 1:
        return x1 + t * (x2 - x1), y1 + t * (y2 - y1)
    return None


def is_in_shadow(light_x, light_y, pixel_x, pixel_y, walls):
    """Check if pixel is in shadow"""
    for wall in walls:
        hit = line_intersect(light_x, light_y, pixel_x, pixel_y,
                             wall.x1, wall.y1, wall.x2, wall.y2)
        if hit:
            # Check if wall blocks the light
            wall_dist = math.sqrt((hit[0] - light_x) ** 2 + (hit[1] - light_y) ** 2)
            pixel_dist = math.sqrt((pixel_x - light_x) ** 2 + (pixel_y - light_y) ** 2)
            if wall_dist < pixel_dist - 1:
                return True
    return False


def render_lightmap(screen, lights, walls):
    """Simple lightmap rendering"""
    width, height = screen.get_size()

    # Start with dark background
    screen.fill((20, 20, 20))

    # For each pixel, calculate lighting
    for x in range(0, width, 2):  # Skip pixels for speed
        for y in range(0, height, 2):
            total_light = [20, 20, 20]  # Ambient light

            for light in lights:
                # Distance to light
                dx = x - light.x
                dy = y - light.y
                distance = math.sqrt(dx * dx + dy * dy)

                # Check if within light radius
                if distance < light.radius and not is_in_shadow(light.x, light.y, x, y, walls):
                    # Calculate light intensity with falloff
                    intensity = 1.0 - (distance / light.radius)
                    intensity = intensity * intensity  # Square falloff

                    # Add light contribution
                    total_light[0] = min(255, total_light[0] + light.color[0] * intensity * 0.5)
                    total_light[1] = min(255, total_light[1] + light.color[1] * intensity * 0.5)
                    total_light[2] = min(255, total_light[2] + light.color[2] * intensity * 0.5)

            # Draw 2x2 block for performance
            color = (int(total_light[0]), int(total_light[1]), int(total_light[2]))
            pygame.draw.rect(screen, color, (x, y, 2, 2))


pygame.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("2D Lightmap")
clock = pygame.time.Clock()

# Create walls
walls = [
    Wall(200, 200, 400, 200),
    Wall(400, 200, 400, 400),
    Wall(400, 400, 200, 400),
    Wall(200, 400, 200, 200),

    Wall(500, 150, 650, 180),
    Wall(150, 450, 300, 470),
]

# Create lights
lights = [
    Light(300, 300, 150, (255, 200, 100)),
    Light(600, 250, 120, (100, 150, 255)),
]

mouse_light = Light(0, 0, 100, (123, 2, 34))

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Update mouse light
    mouse_light.x, mouse_light.y = pygame.mouse.get_pos()

    # Render
    all_lights = lights + [mouse_light]
    render_lightmap(screen, all_lights, walls)

    # Draw walls for reference
    for wall in walls:
        pygame.draw.line(screen, (100, 100, 100), (wall.x1, wall.y1), (wall.x2, wall.y2), 2)

    # Draw lights
    for light in all_lights:
        pygame.draw.circle(screen, light.color, (int(light.x), int(light.y)), 3)

    pygame.display.flip()
    clock.tick(30)

pygame.quit()
