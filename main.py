from typing import List, Tuple
import pygame

from boids import Flock, profile
from elements import InputBox, Button

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
def draw(flock, inputs):
    """Draw everything to the screen
    """
    SCREEN.fill(BG_COLOR)

    # Draw boids
    for boid in flock.boids:
        pos = tuple(boid.pos)
        next_pos = tuple(boid.pos + boid.dir * LINE_LENGTH)

        pygame.draw.circle(SCREEN, boid.color, pos, boid.size)
        pygame.draw.line(SCREEN, LINE_COLOR, pos, next_pos)

    # Draw cells
    for y in range(0, width, cell_size):
        pygame.draw.line(SCREEN, CELL_COLOR,
                         (y, 0), (y, width))

    for x in range(0, width, cell_size):
        pygame.draw.line(SCREEN, CELL_COLOR,
                         (0, x), (width, x))

    # Draw inputs (inputboxes, buttons)
    for input_ in inputs:
        input_.draw(SCREEN)


@profile
def setup():
    """The main function
    """
    pygame.init()

    # Create inputs
    font_size = 20

    input_args = [
        (InputBox, "Alignment:", 0.1, "alignment"),
        (InputBox, "Cohesion:", 0.1, "cohesion"),
        (InputBox, "Seperation", 0.1, "seperation"),

        (InputBox, "Max Speed:", 1, "max_speed"),

        (InputBox, "Avoid Distance", 20, "avoid_dist"),
        (InputBox, "Other Avoid Distance", 40, "other_avoid_dist"),
        (InputBox, "Other Avoid Multiplier:", 1.1, "other_avoid_mult"),

        (InputBox, "Perception:", 2, "perception"),
        (InputBox, "Field of View", 270, "field_of_view"),

        (Button, "Reset", 2, reset)
    ]

    inputs = create_inputs(input_args, font_size, 10, 25)

    # Create the flock
    flock = Flock(
        num_boids=100,
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

    # Return the inputs and the flock
    return inputs, flock


def run(inputs: dict, flock: Flock):
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

            # Check for inputs
            for input_, attr_name in inputs.items():
                if type(input_) == Button:
                    if attr_name == reset and input_.pressed(e):
                        reset(flock)

                elif type(input_) == InputBox:
                    var = input_.update(e)

                    if var is not None:
                        setattr(flock, attr_name, var)

        # Update boids
        flock.update_boids()

        # Draw everything
        draw(flock, inputs)
        pygame.display.update()


def reset(flock: Flock):
    """Reset the boids

    Args:
        flock (Flock): the flock of boids to reset
    """
    flock.reset_boids(len(flock.boids), num_types)


def create_inputs(args: List[Tuple[object, str, int, str]],
                  font_size: int,
                  x_offset: int, y_offset: int):
    """Create inputs according to a list of options

    Args:
        args (List[Tuple[object, str, int, str]]): class, name, init val, var
        font_size (int): the size of the font
        x_offset (int): the offset on the x-axis
        y_offset (int): the offset on the y-axis

    Returns:
        dict: the inputs all added into a dict
    """
    inputs = {}
    # Enumerate over all the args
    for i, arg in enumerate(args, 1):
        class_ = arg[0]

        # Create a InputBox
        if class_ == InputBox:
            # Extract args
            name = arg[1]
            init_value = arg[2]
            var = arg[3]

            # Create instance
            instance = class_(
                name=name,
                position=(x_offset, y_offset * i),
                font_size=font_size,
                init_value=init_value
            )

            # Add instance to inputs
            inputs[instance] = var

        # Create a Button
        elif class_ == Button:
            # Extract args
            name = arg[1]
            bound_size = arg[2]
            var = arg[3]

            # Create instance
            instance = class_(
                name=name,
                position=(x_offset, y_offset * i),
                font_size=font_size,
                bound_size=bound_size
            )

            # Add instance to inputs
            inputs[instance] = var

    # Return the inputs
    return inputs


if __name__ == '__main__':
    # ---------- SETUP ----------
    inputs, flock = setup()
    # ---------- LOOP ----------
    run(inputs, flock)
