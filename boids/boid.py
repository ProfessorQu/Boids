from pygame import Vector2
import pygame


class Boid:
    """The boid object with a position and steerection
    """

    def __init__(self, pos: Vector2, dir_: Vector2,
                 type_: int, color: pygame.color.Color):
        """The initialize method

        Args:
            pos (Vector2): the position of the boid
            steer (Vector2): the direction of the boid
            perception (float): how far the boid can see
        """
        self.pos = pos
        self.dir = dir_

        self.type = type_
        self.color = color

        self.hash = tuple

    def __repr__(self) -> str:
        return (f"Boid(pos={self.pos}, dir={self.dir}, hash={self.hash})")
