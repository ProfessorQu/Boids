import pygame

from boids import Flock

# ---------- VARIABLES ----------
# Set the canvas and bounds
world_size = width, height = (1000, 1000)

# Background color
BG_COLOR = pygame.Color(0, 26, 51)

# Boid settings
BOID_SIZE = 5
num_types = 3

# Line settings/colors
LINE_COLOR = pygame.Color(0, 0, 0)
LINE_LENGTH = 1.5

# Cell color
CELL_COLOR = pygame.Color(0, 77, 0)

# Initialize display
SCREEN = pygame.display.set_mode(world_size)
CLOCK = pygame.time.Clock()

cell_size = int((world_size[0] + world_size[1]) / 20)


# ---------- DRAW ----------
def draw(flock):
    """Draw everything to the screen
    """
    SCREEN.fill(BG_COLOR)

    # Draw boids
    for boid in flock.boids:
        pos = tuple(boid.pos)
        next_pos = tuple(boid.pos + boid.dir * LINE_LENGTH)

        pygame.draw.circle(SCREEN, boid.color, pos, BOID_SIZE)
        pygame.draw.line(SCREEN, LINE_COLOR, pos, next_pos)

    # Draw cells
    for y in range(0, width, cell_size):
        pygame.draw.line(SCREEN, CELL_COLOR,
                         (y, 0), (y, width))

    for x in range(0, width, cell_size):
        pygame.draw.line(SCREEN, CELL_COLOR,
                         (0, x), (width, x))


def get_flock():
    """The main function
    """
    pygame.init()

    # Return the flock
    return Flock(
        num_boids=150,
        num_types=num_types,
        world_size=world_size,
        cell_size=cell_size,
        max_speed=15,
        perception=2,
        field_of_view=270,
        avoid_dist=20,
        other_avoid_mult=1.5,
        other_avoid_dist=40,
        alignment_factor=0.05,
        cohesion_factor=0.005,
        seperation_factor=0.05,
        turn_margin=100,
        turn_factor=1.5,
        loop_bounds=False
    )


def run(flock: Flock):
    """Run the simulation

    Args:
        inputs (dict): the inputs to render and use
        flock (Flock): the flock to simulate
    """

    running = True
    while running:
        # Let the program run at 30 fps
        CLOCK.tick(30)

        # Check for events
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                running = False
            elif e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE:
                running = False

        # Update boids
        flock.update_boids()

        # Draw everything
        draw(flock)
        pygame.display.update()


def reset(flock: Flock):
    """Reset the boids

    Args:
        flock (Flock): the flock of boids to reset
    """
    flock.reset_boids(len(flock.boids), num_types)


if __name__ == '__main__':
    # ---------- SETUP ----------
    flock = get_flock()
    # ---------- LOOP ----------
    run(flock)
