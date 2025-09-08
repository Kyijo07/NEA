import pygame
import math


class Light:
    def __init__(self, x, y, radius, colour=(255, 255, 255)):
        self.x = x
        self.y = y
        self.radius = radius
        self.colour = colour


class Wall:
    def __init__(self, x1, y1, x2, y2):
        self.x1, self.y1 = x1, y1
        self.x2, self.y2 = x2, y2


def line_intersect(x1, y1, x2, y2, x3, y3, x4, y4):
    denom = (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4)
    if abs(denom) < 0.001:
        return None
    t = ((x1 - x3) * (y3 - y4) - (y1 - y3) * (x3 - x4)) / denom
    u = -((x1 - x2) * (y1 - y3) - (y1 - y2) * (x1 - x3)) / denom
    if t >= 0 and 0 <= u <= 1:
        return x1 + t * (x2 - x1), y1 + t * (y2 - y1)
    return None


def is_in_shadow(light_x, light_y, px, py, walls):
    for wall in walls:
        hit = line_intersect(light_x, light_y, px, py, wall.x1, wall.y1, wall.x2, wall.y2)
        if hit:
            wall_dx, wall_dy = hit[0] - light_x, hit[1] - light_y
            px_dx, px_dy = px - light_x, py - light_y
            if wall_dx * wall_dx + wall_dy * wall_dy < px_dx * px_dx + px_dy * px_dy:
                return True
    return False


def render_lightmap(screen, lights, walls, step=8):
    """Pixelated lightmap: bigger step = chunkier look"""
    width, height = screen.get_size()
    surface = pygame.Surface((width // step, height // step))
    surface.lock()

    for x in range(0, width, step):
        for y in range(0, height, step):
            total_r, total_g, total_b = 20, 20, 20  # Ambient

            for light in lights:
                dx, dy = x - light.x, y - light.y
                dist_sq = dx * dx + dy * dy

                if dist_sq < light.radius * light.radius:
                    if not is_in_shadow(light.x, light.y, x, y, walls):
                        distance = math.sqrt(dist_sq)
                        falloff = 1.0 - (distance / light.radius)
                        intensity = falloff * falloff * 0.6

                        total_r = min(255, total_r + light.colour[0] * intensity)
                        total_g = min(255, total_g + light.colour[1] * intensity)
                        total_b = min(255, total_b + light.colour[2] * intensity)

            surface.set_at((x // step, y // step), (int(total_r), int(total_g), int(total_b)))

    surface.unlock()
    # Nearest-neighbor scaling -> chunky pixels
    scaled = pygame.transform.scale(surface, (width, height))
    screen.blit(scaled, (0, 0))



def main():
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Pixelated 2D Lightmap")
    clock = pygame.time.Clock()

    walls = [
        Wall(200, 200, 400, 200),
        Wall(400, 200, 400, 400),
        Wall(400, 400, 200, 400),
        Wall(200, 400, 200, 200),
        Wall(500, 150, 650, 180),
        Wall(150, 450, 300, 470),
    ]

    lights = [
        Light(300, 300, 180, (255, 200, 100)),
        Light(600, 250, 150, (100, 150, 255)),
    ]

    mouse_light = Light(0, 0, 120, (255, 0, 0))

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        mouse_light.x, mouse_light.y = pygame.mouse.get_pos()

        all_lights = lights + [mouse_light]
        render_lightmap(screen, all_lights, walls, step=6)  # << Pixelation level

        # Draw walls
        for wall in walls:
            pygame.draw.line(screen, (80, 80, 80), (wall.x1, wall.y1), (wall.x2, wall.y2), 2)

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()


if __name__ == "__main__":
    main()
