import pygame
from boids import Boids

pygame.init()

# Set the canvas and bounds
world_size = width, height = (500, 500)

# Initiate colors
bg_color = (0, 100, 200)

boid_color = (200, 200, 0)
boid_size = 5

line_color = (0, 0, 0)

cell_color = (0, 255, 0)

# Initialize display
screen = pygame.display.set_mode(world_size)
clock = pygame.time.Clock()

cell_size = 50

boids = Boids(
    num_boids=20,
    world_size=world_size,
    max_speed=5,
    perception=2,
    view_angle=0.5,
    avoid_distance=20,
    cell_size=cell_size,
    alignment_factor=0.5,
    cohesion_factor=0.005,
    seperation_factor=0.5
)


def draw():
    """Draw everything to the screen
    """
    screen.fill(bg_color)

    # Draw boids
    for boid in boids.boids:
        pos = tuple(boid.pos)
        next_pos = tuple(boid.pos + boid.steer)

        pygame.draw.circle(screen, boid_color, pos, boid_size)
        pygame.draw.line(screen, line_color, pos, next_pos)

    for y in range(0, width, cell_size):
        pygame.draw.line(screen, cell_color,
                         (y, 0), (y, width))

    for x in range(0, width, cell_size):
        pygame.draw.line(screen, cell_color,
                         (0, x), (width, x))


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            break

    draw()
    boids.update_boids()

    pygame.display.update()
    clock.tick(30)
