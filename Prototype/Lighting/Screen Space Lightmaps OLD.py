import pygame
import math


class Lightmap:
    def __init__(self, width, height):
        self.width = width
        self.height = height

        # Create the lightmap surface
        self.lightmap = pygame.Surface((width, height), pygame.SRCALPHA)

        # Set ambient light
        self.ambient_color = (30, 30, 30)

        # List to store lights
        self.lights = []

        # List to store obstacles (can be rectangles or polygons)
        self.obstacles = []

        # List to store polygon obstacles (triangle, pentagon, etc)
        self.polygon_obstacles = []

    def add_light(self, x, y, radius, color):
        """Add a simple light source"""
        self.lights.append({
            "x": x,
            "y": y,
            "radius": radius,
            "color": color
        })

    def add_rectangle(self, rect):
        """Add a rectangular obstacle"""
        self.obstacles.append({
            "type": "rectangle",
            "rect": rect
        })

    def add_polygon(self, points, color=(70, 70, 90)):
        """Add a polygon obstacle defined by its points"""
        # Calculate centroid (average of all points)
        center_x = sum(x for x, y in points) / len(points)
        center_y = sum(y for x, y in points) / len(points)

        self.polygon_obstacles.append({
            "type": "polygon",
            "points": points,
            "center": (center_x, center_y),
            "color": color
        })

    def update(self):
        """Update the lightmap"""
        # Fill with ambient light
        self.lightmap.fill(self.ambient_color)

        # Draw each light as a simple circle
        for light in self.lights:
            # Create a temporary surface for this light
            light_surface = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
            light_surface.fill((0, 0, 0, 0))  # Transparent

            # Draw the light
            pygame.draw.circle(
                light_surface,
                light["color"],
                (light["x"], light["y"]),
                light["radius"]
            )

            # Cast shadows from rectangular obstacles
            for obstacle in self.obstacles:
                self._cast_shadow_from_rectangle(light_surface, light, obstacle["rect"])

            # Cast shadows from polygon obstacles
            for polygon in self.polygon_obstacles:
                self._cast_shadow_from_polygon(light_surface, light, polygon)

            # Add this light to the lightmap
            self.lightmap.blit(light_surface, (0, 0), special_flags=pygame.BLEND_RGBA_ADD)

    def _cast_shadow_from_rectangle(self, surface, light, obstacle):
        """Cast a shadow from a rectangular obstacle"""
        light_x, light_y = light["x"], light["y"]

        # Calculate each corner of the rectangle
        corners = [
            (obstacle.noise, obstacle.y),  # Top-left
            (obstacle.noise + obstacle.width, obstacle.y),  # Top-right
            (obstacle.noise + obstacle.width, obstacle.y + obstacle.height),  # Bottom-right
            (obstacle.noise, obstacle.y + obstacle.height)  # Bottom-left
        ]

        # Cast shadow from each edge
        for i in range(len(corners)):
            # Get current corner and next corner
            current = corners[i]
            next_idx = (i + 1) % len(corners)
            next_corner = corners[next_idx]

            # Create vector from light to each corner
            dx1 = current[0] - light_x
            dy1 = current[1] - light_y
            dx2 = next_corner[0] - light_x
            dy2 = next_corner[1] - light_y

            # Normalize and extend to create shadow points
            length = max(self.width, self.height)
            dist1 = max(1, math.sqrt(dx1 * dx1 + dy1 * dy1))
            dist2 = max(1, math.sqrt(dx2 * dx2 + dy2 * dy2))

            shadow_x1 = current[0] + (dx1 / dist1) * length
            shadow_y1 = current[1] + (dy1 / dist1) * length
            shadow_x2 = next_corner[0] + (dx2 / dist2) * length
            shadow_y2 = next_corner[1] + (dy2 / dist2) * length

            # Draw shadow quad
            pygame.draw.polygon(
                surface,
                (0, 0, 0, 255),  # Black, opaque
                [current, next_corner, (shadow_x2, shadow_y2), (shadow_x1, shadow_y1)],
                0  # Fill
            )

    def _cast_shadow_from_polygon(self, surface, light, polygon):
        """Cast a shadow from a polygon obstacle"""
        light_x, light_y = light["x"], light["y"]
        points = polygon["points"]

        # Cast shadow from each edge
        for i in range(len(points)):
            # Get current point and next point
            current = points[i]
            next_idx = (i + 1) % len(points)
            next_point = points[next_idx]

            # Create vector from light to each point
            dx1 = current[0] - light_x
            dy1 = current[1] - light_y
            dx2 = next_point[0] - light_x
            dy2 = next_point[1] - light_y

            # Normalize and extend to create shadow points
            length = max(self.width, self.height)
            dist1 = max(1, math.sqrt(dx1 * dx1 + dy1 * dy1))
            dist2 = max(1, math.sqrt(dx2 * dx2 + dy2 * dy2))

            shadow_x1 = current[0] + (dx1 / dist1) * length
            shadow_y1 = current[1] + (dy1 / dist1) * length
            shadow_x2 = next_point[0] + (dx2 / dist2) * length
            shadow_y2 = next_point[1] + (dy2 / dist2) * length

            # Draw shadow quad
            pygame.draw.polygon(
                surface,
                (0, 0, 0, 255),  # Black, opaque
                [current, next_point, (shadow_x2, shadow_y2), (shadow_x1, shadow_y1)],
                0  # Fill
            )

    def apply(self, target_surface):
        """Apply lightmap to target surface"""
        target_surface.blit(self.lightmap, (0, 0), special_flags=pygame.BLEND_RGB_MULT)

    def draw_obstacles(self, surface):
        """Draw all obstacles to the given surface"""
        # Draw rectangular obstacles
        for obstacle in self.obstacles:
            pygame.draw.rect(surface, (70, 70, 90), obstacle["rect"])

        # Draw polygon obstacles
        for polygon in self.polygon_obstacles:
            pygame.draw.polygon(surface, polygon["color"], polygon["points"])


def main():
    pygame.init()

    # Set up display
    width, height = 640, 480
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Simple Lightmap Demo with Different Shapes")

    # Create game world
    world = pygame.Surface((width, height))

    # Create lightmap
    lightmap = Lightmap(width, height)

    # Add rectangular obstacles
    lightmap.add_rectangle(pygame.Rect(300, 186, 190, 149))
    lightmap.add_rectangle(pygame.Rect(150, 64, 176, 168))

    # Add a triangle obstacle
    triangle_points = [(400, 300), (470, 350), (420, 380)]
    lightmap.add_polygon(triangle_points, color=(21, 28, 28))

    # Add a pentagon obstacle
    pentagon_points = []
    pentagon_center = (200, 150)
    pentagon_radius = 40
    for i in range(5):
        angle = 2 * math.pi * i / 5 - math.pi / 2  # Start at top
        x = pentagon_center[0] + pentagon_radius * math.cos(angle)
        y = pentagon_center[1] + pentagon_radius * math.sin(angle)
        pentagon_points.append((x, y))
    lightmap.add_polygon(pentagon_points, color=(31, 90, 224))

    # Add a star obstacle
    star_points = []
    star_center = (500, 150)
    outer_radius = 40
    inner_radius = 20
    for i in range(10):
        angle = 2 * math.pi * i / 10 - math.pi / 2  # Start at top
        radius = outer_radius if i % 2 == 0 else inner_radius
        x = star_center[0] + radius * math.cos(angle)
        y = star_center[1] + radius * math.sin(angle)
        star_points.append((x, y))
    lightmap.add_polygon(star_points, color=(209, 74, 78))

    # Add a light
    lightmap.add_light(150, 400, 150, (44, 38, 58))

    # Add a light
    lightmap.add_light(450, 100, 130, (162, 183, 10))

    # Create a movable light
    movable_light = {"x": 320, "y": 240, "radius": 30, "color": (174, 235, 51)}
    lightmap.add_light(movable_light["x"], movable_light["y"],
                       movable_light["radius"], movable_light["color"])

    clock = pygame.time.Clock()
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False

        # Update movable light with mouse position
        mouse_x, mouse_y = pygame.mouse.get_pos()
        movable_light["x"] = mouse_x
        movable_light["y"] = mouse_y
        lightmap.lights[2]["x"] = mouse_x
        lightmap.lights[2]["y"] = mouse_y

        # Draw world
        world.fill((255, 255, 255))  # Background

        # Draw obstacles
        lightmap.draw_obstacles(world)

        # Copy world to screen
        screen.blit(world, (0, 0))

        # Update and apply lighting
        lightmap.update()
        lightmap.apply(screen)

        # Draw text instructions
        font = pygame.font.SysFont(None, 24)
        text = font.render("Move mouse to control the light", True, (255, 255, 255))
        screen.blit(text, (10, 10))

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()


if __name__ == "__main__":
    main()
