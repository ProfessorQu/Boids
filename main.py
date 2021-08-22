import pygame

from boids import Boids

pygame.init()

# Set the canvas and bounds
world_size = width, height = (1000, 1000)

# Initiate colors
bg_color = pygame.Color(0, 100, 200)

boid_color = pygame.Color(200, 0, 0)
boid_size = 5
num_types = 10

line_color = pygame.Color(0, 0, 0)
line_length = 1.5

cell_color = pygame.Color(0, 255, 0)

# Initialize display
screen = pygame.display.set_mode(world_size)
clock = pygame.time.Clock()

cell_size = 100

# Create the boids object
boids = Boids(
    num_boids=200,
    num_types=num_types,
    world_size=world_size,
    max_speed=5,
    perception=2,
    field_of_view=360,
    avoid_distance=20,
    cell_size=cell_size,
    alignment_factor=0.1,
    cohesion_factor=0.005,
    seperation_factor=0.1
)


def draw():
    """Draw everything to the screen
    """
    screen.fill(bg_color)

    # Draw boids
    for boid in boids.boids:
        pos = tuple(boid.pos)
        next_pos = tuple(boid.pos + boid.steer * line_length)

        color = pygame.Color(0, 0, 0)
        scaler = 360 / num_types
        color.hsla = (boid.type * scaler, 100, 50, 100)

        pygame.draw.circle(screen, color, pos, boid_size)
        pygame.draw.line(screen, line_color, pos, next_pos)

    # Draw cells
    # for y in range(0, width, cell_size):
        # pygame.draw.line(screen, cell_color,
        # (y, 0), (y, width))

    # for x in range(0, width, cell_size):
        # pygame.draw.line(screen, cell_color,
        # (0, x), (width, x))


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            break

    boids.update_boids()
    draw()

    pygame.display.update()
    clock.tick(30)
