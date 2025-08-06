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


class SimpleLightmap:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        # Very low resolution for speed
        self.scale = 8  # 8x8 pixel blocks
        self.lm_width = width // self.scale
        self.lm_height = height // self.scale
        self.surface = pygame.Surface((self.lm_width, self.lm_height))

    def line_intersect(self, x1, y1, x2, y2, x3, y3, x4, y4):
        """Fast line intersection check"""
        denom = (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4)
        if abs(denom) < 0.01:
            return False

        t = ((x1 - x3) * (y3 - y4) - (y1 - y3) * (x3 - x4)) / denom
        u = -((x1 - x2) * (y1 - y3) - (y1 - y2) * (x1 - x3)) / denom

        return t > 0 and 0 <= u <= 1

    def render(self, lights, walls):
        """Super fast lightmap rendering"""
        # Clear
        self.surface.fill((20, 20, 20))

        # Process in large blocks for speed
        for x in range(self.lm_width):
            for y in range(self.lm_height):
                # Convert to world coordinates
                world_x = x * self.scale + self.scale // 2
                world_y = y * self.scale + self.scale // 2

                light_r, light_g, light_b = 20, 20, 20  # Ambient

                # Check each light
                for light in lights:
                    dx = world_x - light.x
                    dy = world_y - light.y
                    distance = math.sqrt(dx * dx + dy * dy)

                    if distance < light.radius:
                        # Quick shadow check - only test a few walls
                        in_shadow = False
                        for wall in walls[:6]:  # Limit wall checks
                            if self.line_intersect(light.x, light.y, world_x, world_y,
                                                   wall.x1, wall.y1, wall.x2, wall.y2):
                                in_shadow = True
                                break

                        if not in_shadow:
                            # Simple linear falloff
                            intensity = (1.0 - distance / light.radius) * 0.8
                            light_r = min(255, light_r + light.color[0] * intensity)
                            light_g = min(255, light_g + light.color[1] * intensity)
                            light_b = min(255, light_b + light.color[2] * intensity)

                # Set pixel color
                color = (int(light_r), int(light_g), int(light_b))
                self.surface.set_at((x, y), color)

        # Scale up with nearest neighbor (fast)
        return pygame.transform.scale(self.surface, (self.width, self.height))


pygame.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Fast 2D Lightmap")
clock = pygame.time.Clock()

lightmap = SimpleLightmap(800, 600)

# Fewer walls
walls = [
    Wall(200, 200, 400, 200),
    Wall(400, 200, 400, 400),
    Wall(400, 400, 200, 400),
    Wall(200, 400, 200, 200),
    Wall(500, 150, 650, 180),
]

# Fewer lights
lights = [
    Light(300, 300, 200, (255, 200, 100)),
    Light(600, 250, 150, (100, 150, 255)),
]

mouse_light = Light(0, 0, 120, (255, 255, 255))

running = True
frame_count = 0

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Update mouse light
    mouse_light.x, mouse_light.y = pygame.mouse.get_pos()

    # Dark background
    screen.fill((10, 10, 15))

    # Render lightmap every 3rd frame
    if frame_count % 3 == 0:
        all_lights = lights + [mouse_light]
        lightmap_surface = lightmap.render(all_lights, walls)

    # Apply lightmap
    screen.blit(lightmap_surface, (0, 0), special_flags=pygame.BLEND_ADD)

    # Draw walls
    for wall in walls:
        pygame.draw.line(screen, (60, 60, 60), (wall.x1, wall.y1), (wall.x2, wall.y2), 2)

    # Draw lights
    for light in lights + [mouse_light]:
        pygame.draw.circle(screen, light.color, (int(light.x), int(light.y)), 4)

    # FPS counter
    fps = int(clock.get_fps())
    font = pygame.font.Font(None, 36)
    fps_text = font.render(f"FPS: {fps}", True, (255, 255, 255))
    screen.blit(fps_text, (10, 10))

    pygame.display.flip()
    clock.tick(60)
    frame_count += 1

pygame.quit()