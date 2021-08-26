from typing import Tuple
import pygame

TXT_COLOR = pygame.Color(100, 100, 100)


class Button:
    """A button that you can press
    """

    # Instantiate colors
    NORMAL = pygame.Color(50, 100, 150)
    HOVER = pygame.Color(150, 200, 250)

    def __init__(
        self, name: str,
        font_size: int,
        position: Tuple[int, int],
        bound_size: int
    ):
        """The initial method

        Args:
            name (str): what will be displayed on the button
            font_size (int): the font size of the name
            position (Tuple[int, int]): the position of the button
            bound_size (int): the size of the bounds around the name
        """
        # Set the name and font
        self.name = name.encode('utf-8')
        self.font = pygame.font.Font(pygame.font.get_default_font(), font_size)

        self.name_surface = self.font.render(self.name, True, TXT_COLOR)

        # Create the name rectangle
        self.rect = pygame.Rect(
            position[0] + bound_size,
            position[1] + bound_size,
            self.name_surface.get_width(),
            self.name_surface.get_height()
        )

        # Create the button rectangle
        self.button_rect = pygame.Rect(
            self.rect.x - bound_size,
            self.rect.y - bound_size,
            self.rect.w + bound_size,
            self.rect.h + bound_size
        )

    def draw(self, screen: pygame.Surface):
        """Draw the button on the screen

        Args:
            screen (pygame.Surface): the screen to draw on
        """
        # Get the color
        color = Button.NORMAL
        if self.button_rect.collidepoint(pygame.mouse.get_pos()):
            color = Button.HOVER

        # Draw the button
        pygame.draw.rect(screen, color, self.button_rect)

        # Draw the text
        screen.blit(self.name_surface, self.rect)

    def pressed(self, event: pygame.event.Event):
        """Check if the button is pressed

        Args:
            event (pygame.event.Event): the event to check

        Returns:
            bool: if the button is pressed
        """
        # Check if the mouse button is down
        # And if the mouse is on top of the button
        if (
            event.type == pygame.MOUSEBUTTONDOWN and
            self.button_rect.collidepoint(event.pos)
        ):
            return True
