import pygame

from flock import Flock
from profiler import profile
from input_box import InputBox, show_error_message

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

input_font = pygame.font.Font(None, 32)
alignment_input = InputBox(
    (10, 10, 200, input_font.get_height() + 5),
    input_font,
    "1"
)

# Create the flock
flock = Flock(
    num_boids=25,
    num_types=num_types,
    world_size=world_size,
    cell_size=cell_size,
    max_speed=1,
    perception=2,
    field_of_view=45,
    avoid_distance=20,
    other_avoid_mult=1.1,
    other_avoid_dist=40,
    alignment_factor=0.1,
    cohesion_factor=0.005,
    seperation_factor=0.1,
    turn_margin=100,
    turn_factor=1.5,
    loop_bounds=True,
    follow_mouse=0,
    mouse_follow_types=[]
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

            # ----- WIP -----
            # alignment = alignment_input.update(e)

            # if alignment is not None:
                # print(alignment)
                # try:
                # float(alignment)
                # except ValueError:
                # show_error_message(screen, (100, 100, 800, 800),
                # (255, 0, 0),
                # input_font,
                # "Error: invalid value for alignment",
                # (0, 0, 0))

        # Update boids
        flock.update_boids()

        # Draw everything
        draw()
        pygame.display.update()


if __name__ == '__main__':
    main()
