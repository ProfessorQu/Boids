import pygame
import boids

pygame.init()

# Set the canvas and bounds
canvas_size = (800, 800)
bounds_size = 50

width = canvas_size[0]
height = canvas_size[1]

bounds = {
    "min_x": width / bounds_size,
    "max_x": width - width / bounds_size,
    "min_y": height / bounds_size,
    "max_y": height - height / bounds_size
}

# Initiate colors
bg_color = (0, 100, 200)
bounds_color = (100, 200, 100)

boid_color = (200, 200, 0)
boid_size = 5

line_color = (0, 0, 0)

# Initialize display
screen = pygame.display.set_mode(canvas_size)
clock = pygame.time.Clock()

# Initialize boids
num_boids = 50
turn_factor = 1
speed_limit = 3
perception = 50
avoidance = 1

flock = boids.create_flock(num_boids, canvas_size, perception, avoidance)


def draw():
    """Draw everything to the screen
    """
    screen.fill(bg_color)

    # Draw bounds
    pygame.draw.line(
        screen, bounds_color,
        (bounds["min_x"], bounds["min_y"]),
        (bounds["max_x"], bounds["min_y"])
    )
    pygame.draw.line(
        screen, bounds_color,
        (bounds["min_x"], bounds["max_y"]),
        (bounds["max_x"], bounds["max_y"])
    )
    pygame.draw.line(
        screen, bounds_color,
        (bounds["max_x"], bounds["min_y"]),
        (bounds["max_x"], bounds["max_y"])
    )
    pygame.draw.line(
        screen, bounds_color,
        (bounds["min_x"], bounds["min_y"]),
        (bounds["min_x"], bounds["max_y"])
    )

    # boid_1 = flock[0]
    # pygame.draw.circle(screen, (50, 50, 50), (boid_1.x, boid_1.y), 100)

    # Draw boids
    for boid in flock:
        pos = tuple(boid.pos)
        next_pos = tuple(boid.pos + boid.steer)

        pygame.draw.circle(screen, boid_color, pos, boid_size)
        pygame.draw.line(screen, line_color, pos, next_pos)


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            break

    draw()
    boids.update(flock, bounds, turn_factor, speed_limit, True)

    pygame.display.update()
    clock.tick(60)
