from typing import Tuple
import pygame


class InputBox(object):
    INACTIVE = pygame.Color(50, 100, 150)
    ACTIVE = pygame.Color(150, 200, 250)

    BG_COLOR = pygame.Color(0, 0, 0)

    TXT_COLOR = pygame.Color(100, 100, 100)

    def __init__(
        self,
        name: str,
        position: Tuple[int, int],
        font_size: int,
        init_value: str,
    ):
        self.txt = init_value.encode('utf-8')
        self.font = pygame.font.Font(None, 32)

        self.name_surface = self.font.render(name, True, InputBox.TXT_COLOR)
        self.txt_surface = self.font.render(self.txt, True, InputBox.TXT_COLOR)

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
        color = InputBox.ACTIVE if self.active else InputBox.INACTIVE

        pygame.draw.rect(screen, InputBox.BG_COLOR, self.rect)
        pygame.draw.rect(screen, InputBox.BG_COLOR, self.box_rect)

        pygame.draw.rect(screen, color, self.box_rect, 1)

        screen.blit(self.name_surface, self.rect)
        screen.blit(self.txt_surface,
                    (self.box_rect.x + 5, self.box_rect.y + 2))

    def update(self, event: pygame.event.Event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.active = bool(self.box_rect.collidepoint(event.pos))

        if event.type == pygame.KEYDOWN and self.active:
            if event.key == pygame.K_RETURN:
                return self.txt
            elif event.key == pygame.K_BACKSPACE:
                self.txt = self.txt[:-1]

                if len(self.txt) == 0:
                    self.txt = b"0"
            else:
                if len(self.txt) == 1 and self.txt[0] == 48:
                    self.txt = b""

                letter = event.unicode
                if letter.isnumeric():
                    self.txt += letter.encode('utf-8')
                elif letter == "." and b"." not in self.txt:
                    self.txt += letter.encode('utf-8')

        self.txt_surface = self.font.render(self.txt, True, InputBox.TXT_COLOR)
        width = max(50, self.txt_surface.get_width() + 10)
        self.box_rect.w = width
