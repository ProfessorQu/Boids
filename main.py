import pygame

from flock import Flock
from profiler import profile
from elements import InputBox

pygame.init()

# ---------- VARIABLES ----------
# Set the canvas and bounds
world_size = width, height = (1000, 1000)

# Background color
bg_color = pygame.Color(0, 26, 51)

# Boid settings
boid_size = 5
num_types = 3

# Line settings/colors
line_color = pygame.Color(0, 0, 0)
line_length = 1.5

# Cell color
cell_color = pygame.Color(0, 77, 0)

# Initialize display
screen = pygame.display.set_mode(world_size)
clock = pygame.time.Clock()

cell_size = 100


alignment_input = InputBox(
    name="Alignment:",
    position=(10, 10),
    font_size=32,
    init_value="0",
)
cohesion_input = InputBox(
    name="Cohesion:",
    position=(10, 35),
    font_size=32,
    init_value="0"
)
seperation_input = InputBox(
    name="Seperation:",
    position=(10, 60),
    font_size=32,
    init_value="0"
)


# Create the flock
flock = Flock(
    num_boids=25,
    num_types=num_types,
    world_size=world_size,
    cell_size=cell_size,
    max_speed=1,
    perception=2,
    field_of_view=360,
    avoid_dist=20,
    other_avoid_mult=1.1,
    other_avoid_dist=40,
    alignment_factor=0,
    cohesion_factor=0,
    seperation_factor=0,
    turn_margin=100,
    turn_factor=1.5,
    loop_bounds=True,
)


# ---------- DRAW ----------
def draw():
    """Draw everything to the screen
    """
    screen.fill(bg_color)

    # Draw boids
    for boid in flock.boids:
        pos = tuple(boid.pos)
        next_pos = tuple(boid.pos + boid.dir * line_length)

        pygame.draw.circle(screen, boid.color, pos, boid_size)
        pygame.draw.line(screen, line_color, pos, next_pos)

    # Draw cells
    for y in range(0, width, cell_size):
        pygame.draw.line(screen, cell_color,
                         (y, 0), (y, width))

    for x in range(0, width, cell_size):
        pygame.draw.line(screen, cell_color,
                         (0, x), (width, x))

    alignment_input.draw(screen)
    cohesion_input.draw(screen)
    seperation_input.draw(screen)


# ---------- LOOP ----------
@profile
def main():
    """The main function
    """
    running = True
    while running:
        # Let the program run at 30 fps
        # clock.tick(60)

        # Check for events
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                running = False
            elif e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE:
                running = False

            seperate = seperation_input.update(e)

            if seperate is not None:
                try:
                    seperate = float(seperate)
                    flock.seperation = seperate
                except ValueError:
                    pass

            print(flock.seperation)

        # Update boids
        flock.update_boids()

        # Draw everything
        draw()
        pygame.display.update()


if __name__ == '__main__':
    main()
