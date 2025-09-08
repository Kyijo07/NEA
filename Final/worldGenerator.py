import pygame
import math
import random
from typing import List, Tuple


class Tiles:
    def __init__(self, size, colour):
        self.file = file
        self.size = size
        self.image = pygame.image.load(file)
        self.rect = self.image.get_rect()
        self.tiles = []
        self.load()
        self.colour = colour


class PerlinNoise:
    def __init__(self, seed: int = None):
        # seed: An integer to initialize the random number generator.
        # Using the same seed will produce the same noise pattern every time.
        # If None is provided, a random seed will be used.

        random.seed(seed)

        # Create a permutation table (often called 'p' in Perlin noise implementations)
        # This is a shuffled array of integers from 0-255 which creates pseudorandomness
        # without actually using random numbers during noise generation
        self.perm = list(range(256))  # Create a list of numbers from 0 to 255
        random.shuffle(self.perm)  # Randomly shuffle the list based on our seed

        # Double the permutation table to avoid having to use modulo in the noise function
        # This prevents the need for bounds checking later
        self.perm += self.perm

        # Define gradient vectors - these are unit vectors pointing in 8 different directions
        # Perlin noise uses these gradients to compute dot products with distance vectors
        # These gradients provide the "flow" direction at each grid point
        self.gradients = [
            (1, 1),  # Northeast
            (-1, 1),  # Northwest
            (1, -1),  # Southeast
            (-1, -1),  # Southwest
            (1, 0),  # East
            (-1, 0),  # West
            (0, 1),  # North
            (0, -1)  # South
        ]

    def _fade(self, t: float) -> float:
        # Fade function to smooth interpolation between grid points.
        # This creates a smooth transition between values rather than a linear one.
        # Ken Perlin developed this specific function (6t^5 - 15t^4 + 10t^3) known as
        # "smootherstep" to replace the original cubic function. It has zero first and
        # second derivatives at t=0 and t=1, which creates smoother transitions.
        # t: A value between 0 and 1 representing position between grid points
        # Returns a smoothed version of t that has a gentler transition near the endpoints
        # 6t^5 - 15t^4 + 10t^3 (Smootherstep function)
        # When plotted, this creates an S-shaped curve that smoothly transitions from 0 to 1
        return t * t * t * (t * (t * 6 - 15) + 10)

    def _lerp(self, a: float, b: float, t: float) -> float:
        # Linear interpolation between two values.

        # Calculates a value between a and b based on t:
        # When t = 0, the result is a
        # When t = 1, the result is b
        # When t is between 0 and 1, the result is a proportional mix of a and b

        # a: The first value (when t = 0)
        # b: The second value (when t = 1)
        # t: A value between 0 and 1 controlling the interpolation

        # Returns the interpolated value between a and b
        return a + t * (b - a)

    def _dot_product(self, grad: Tuple[int, int], x: float, y: float) -> float:
        # Compute the dot product between a gradient vector and a distance vector.

        # The dot product measures how much two vectors align. In Perlin noise, this measures
        # how much the random gradient "flows" in the direction of the point we're evaluating.

        # grad: A gradient vector (one of our 8 predefined directions)
        # x: The x-component of the distance vector
        # y: The y-component of the distance vector

        # Returns the dot product of the gradient and distance vectors

        # The dot product is simply (grad.x * x + grad.y * y)
        # This creates higher values when the vectors align and lower values when they don't
        return grad[0] * x + grad[1] * y

    def _get_gradient(self, x: int, y: int) -> Tuple[int, int]:
        # Get a gradient vector from the permutation table based on coordinates.

        # This function deterministically selects one of our 8 gradient vectors based on the
        # coordinates. The same coordinates will always return the same gradient, but different
        # coordinates will appear to have randomly selected gradients.

        # x: The x grid coordinate
        # y: The y grid coordinate

        # Returns one of the 8 predefined gradient vectors

        # Use the permutation table to hash the coordinates to a value
        # First, take the x coordinate modulo 256 to get an index in our permutation table
        # Then, add the y coordinate and look up that index in the permutation table
        # This creates a unique hash based on both x and y
        hash_val = self.perm[(self.perm[x % 256] + y) % 256] % 8

        # Use the hash to select one of our 8 gradient vectors
        return self.gradients[hash_val]

    def noise(self, x: float, y: float) -> float:

        # Generate a Perlin noise value at coordinates (x, y).

        # This is the core Perlin noise algorithm. For any point in space, it:
        # 1. Determines which grid cell the point is in
        # 2. Calculates the contribution from each of the 4 corners of that cell
        # 3. Interpolates between those values to get a final smooth noise value

        # x: The x-coordinate to evaluate noise at
        # y: The y-coordinate to evaluate noise at

        # Returns a noise value between 0 and 1

        # Step 1: Determine the grid cell coordinates by flooring the input coordinates
        # This identifies which integer grid cell the point falls within
        x0 = math.floor(x)  # Integer part of x (grid cell x-coordinate)
        y0 = math.floor(y)  # Integer part of y (grid cell y-coordinate)
        x1 = x0 + 1  # Grid coordinate of cell to the right
        y1 = y0 + 1  # Grid coordinate of cell above

        # Step 2: Calculate the relative position within the cell (0 to 1 in each dimension)
        # These are the fractional parts of our coordinates
        sx = x - x0  # Fraction of the way from left to right
        sy = y - y0  # Fraction of the way from bottom to top

        # Step 3: Apply the fade function to smooth the interpolation
        # This changes linear interpolation to a smoother, more natural curve
        u = self._fade(sx)
        v = self._fade(sy)

        # Step 4: Get the gradient vectors for each of the four corners of the grid cell
        # Each corner gets a pseudorandom but consistent gradient direction
        g00 = self._get_gradient(x0, y0)  # Bottom-left corner
        g10 = self._get_gradient(x1, y0)  # Bottom-right corner
        g01 = self._get_gradient(x0, y1)  # Top-left corner
        g11 = self._get_gradient(x1, y1)  # Top-right corner

        # Step 5: Calculate the dot product between each gradient and the vector from the corner to our point.
        # This measures how much the gradient "flows" toward our point.

        # Distance vector from bottom-left corner to our point is (sx, sy)
        n00 = self._dot_product(g00, sx, sy)

        # Distance vector from bottom-right corner to our point is (sx-1, sy)
        # The -1 is because we're 1 unit to the left of the bottom-right corner in x
        n10 = self._dot_product(g10, sx - 1, sy)

        # Distance vector from top-left corner to our point is (sx, sy-1)
        # The -1 is because we're 1 unit below the top-left corner in y
        n01 = self._dot_product(g01, sx, sy - 1)

        # Distance vector from top-right corner to our point is (sx-1, sy-1)
        # We're 1 unit left and 1 unit down from the top-right corner
        n11 = self._dot_product(g11, sx - 1, sy - 1)

        # Step 6: Interpolate along the x-axis first
        # Blend between left and right influence on the bottom edge
        nx0 = self._lerp(n00, n10, u)

        # Blend between left and right influence on the top edge
        nx1 = self._lerp(n01, n11, u)

        # Step 7: Interpolate along the y-axis to get the final result
        # Blend between bottom and top results
        result = self._lerp(nx0, nx1, v)

        # Step 8: Scale the result from [-1, 1] to [0, 1] for easier use
        # Perlin noise naturally produces values between -1 and 1, so we normalize
        return (result + 1) * 0.5

    def generate_noise_map(self, width: int, height: int, scale: float = 1.0) -> List[List[float]]:
        # Generate a 2D grid of noise values.

        # This method creates a 2D array filled with Perlin noise values, which can be used
        # for terrain generation, textures, or other procedural content.

        # width: The width of the noise map in pixels/cells
        # height: The height of the noise map in pixels/cells
        # scale: Controls the zoom level of the noise:
        # Smaller values (e.g., 0.1) create zoomed-out, big features
        # Larger values (e.g., 50.0) create zoomed-in, detailed patterns

        # Returns a 2D list where each value is a noise value between 0 and 1

        # Prevent division by zero by enforcing a minimum scale
        if scale <= 0:
            scale = 0.0001

        # Initialize an empty 2D list filled with zeros to store our noise values
        # The list is indexed as [y][x] which matches how images are typically indexed
        noise_map = [[0 for _ in range(width)] for _ in range(height)]

        # Generate a noise value for each cell in the grid
        for y in range(height):
            for x in range(width):
                # Apply scaling to coordinates to control noise frequency
                # Dividing by scale makes a smaller scale value create larger, smoother features
                # This is because points that are close together in the grid become
                # further apart in the noise space when scale is small
                sample_x = x / scale
                sample_y = y / scale

                # Get the noise value at these scaled coordinates
                noise_value = self.noise(sample_x, sample_y)

                # Store the result in our 2D grid
                noise_map[y][x] = noise_value

        return noise_map


if __name__ == "__main__":
    pygame.init()
    s_width, s_height = 20, 20
    screen = pygame.display.set_mode((s_width, s_height))
    # Create a new Perlin noise generator with a specific seed
    # Using the same seed will always produce the same noise pattern
    seed = None
    perlin = PerlinNoise(seed)

    # Define the dimensions of our noise map
    width, height = 20, 20
    world = pygame.Surface((width, height))

    # Set the scale of the noise:
    # Small values (e.g., 10.0) create large, smooth features
    # Large values (e.g., 100.0) create small, detailed features
    scale = 10.0
    print(seed)

    # Generate our noise map with the defined parameters
    noise_map = perlin.generate_noise_map(width, height, scale)
    with open('../Prototype (no need to look)/World Generation/example.txt', 'w') as file:
        file.write(str(noise_map))
    clock = pygame.time.Clock()
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        world.fill((0, 0, 0))
        pygame.display.flip()
        pygame.display.update()
        clock.tick(60)
        print(clock.get_fps())
    pygame.quit()
