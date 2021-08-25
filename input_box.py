# ----- WIP -----

import pygame


class InputBox(object):
    INACTIVE = pygame.Color(50, 100, 150)
    ACTIVE = pygame.Color(150, 200, 250)
    TXT_COLOR = pygame.Color(100, 100, 100)

    def __init__(
        self,
        rect: pygame.Rect,
        font: pygame.font.Font,
        init_value: str
    ):
        self.rect = pygame.Rect(rect)
        self.color = InputBox.INACTIVE

        self.txt = init_value.encode('utf-8')
        self.font = font
        self.txt_surface = self.font.render(self.txt, True, InputBox.TXT_COLOR)

        self.active = False
        self.backspace_held = False

    def draw(self, screen: pygame.Surface):
        self.color = InputBox.ACTIVE if self.active else InputBox.INACTIVE
        screen.blit(self.txt_surface, (self.rect.x + 5, self.rect.y + 5))
        pygame.draw.rect(screen, self.color, self.rect, 2)

        # pygame.display.flip()

    def update(self, event: pygame.event.Event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.active = bool(self.rect.collidepoint(event.pos))

        if event.type == pygame.KEYDOWN and self.active:
            if event.key == pygame.K_RETURN:
                return self.txt
            elif event.key == pygame.K_BACKSPACE:
                self.txt = self.txt[:-1]
            else:
                self.txt += event.unicode.encode('utf-8')

        self.txt_surface = self.font.render(self.txt, True, InputBox.TXT_COLOR)
        width = max(self.rect.x, self.txt_surface.get_width() + 10)
        self.rect.w = width


def show_error_message(
    screen: pygame.Surface,
    rect: pygame.rect.Rect,
    rect_color: pygame.Color,
    font: pygame.font.Font,
    txt: str,
    txt_color: pygame.Color
):
    rect = pygame.Rect(rect)
    txt = txt.encode('utf-8')

    txt_surface = font.render(txt, True, txt_color)

    screen.blit(txt_surface, (rect.x + 5, rect.y + 5))
    pygame.draw.rect(screen, rect_color, rect, 2)
