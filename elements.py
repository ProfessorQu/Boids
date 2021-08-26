from typing import Tuple
import pygame

TXT_COLOR = pygame.Color(100, 100, 100)


class InputBox(object):
    """An inputbox where you can input a number
    """
    # Instantiate colors
    INACTIVE = pygame.Color(50, 100, 150)
    ACTIVE = pygame.Color(150, 200, 250)

    BG_COLOR = pygame.Color(0, 0, 0)

    def __init__(
        self, name: str,
        position: Tuple[int, int],
        font_size: int, init_value: str
    ):
        """The initial method

        Args:
            name (str): what will be displayed to the left of the input
            position (Tuple[int, int]): the position of the input
            font_size (int): the font size of the name
            init_value (str): the initial value in the box
        """
        self.txt = str(init_value).encode('utf-8')
        self.font = pygame.font.Font(pygame.font.get_default_font(), font_size)

        self.name_surface = self.font.render(name, True, TXT_COLOR)
        self.txt_surface = self.font.render(self.txt, True, TXT_COLOR)

        self.rect = pygame.Rect(
            position[0],
            position[1],
            self.name_surface.get_width(),
            self.name_surface.get_height()
        )

        self.box_rect = pygame.Rect(
            self.rect.x + self.name_surface.get_width() + 5,
            self.rect.y,
            self.txt_surface.get_width() + 10,
            self.name_surface.get_height()
        )

        self.active = False

    def draw(self, screen: pygame.Surface):
        """Draw the input box

        Args:
            screen (pygame.Surface): the screen to draw on
        """
        # Get the color
        color = InputBox.ACTIVE if self.active else InputBox.INACTIVE

        # Draw the input box
        pygame.draw.rect(screen, color, self.box_rect, 1)

        # Draw the text
        screen.blit(self.name_surface, self.rect)
        screen.blit(self.txt_surface,
                    (self.box_rect.x + 5, self.box_rect.y + 2))

    def update(self, event: pygame.event.Event):
        """Update the input according to what event happened

        Args:
            event (pygame.event.Event): the event that happened

        Returns:
            float: the value of the text in the box
        """
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.active = bool(self.box_rect.collidepoint(event.pos))

        if event.type == pygame.KEYDOWN and self.active:
            if event.key == pygame.K_BACKSPACE:
                self.txt = self.txt[:-1]

                if len(self.txt) == 0:
                    self.txt = b"0"
            else:
                letter = event.unicode
                if letter.isnumeric():
                    if len(self.txt) == 1 and self.txt[0] == 48:
                        self.txt = letter.encode('utf-8')
                    else:
                        self.txt += letter.encode('utf-8')
                elif letter == "." and b"." not in self.txt:
                    self.txt += letter.encode('utf-8')

        self.txt_surface = self.font.render(self.txt, True, TXT_COLOR)
        width = max(50, self.txt_surface.get_width() + 10)
        self.box_rect.w = width

        return float(self.txt)


class Button(object):
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
            color = Button.NORMAL

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
