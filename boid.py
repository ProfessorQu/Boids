from pygame import Vector2


class Boid(object):
    """The boid object with a position and steerection
    """

    def __init__(self, pos: Vector2, steer: Vector2):
        """The initialize method

        Args:
            pos (Vector2): the position of the boid
            steer (Vector2): the direction of the boid
            perception (float): how far the boid can see
        """
        self.pos = pos
        self.steer = steer

        self._hash = tuple

    @property
    def hash(self) -> tuple:
        """Get the hash

        Returns:
            tuple: what cell is the boid in
        """
        return self._hash

    def set_hash(self, new_hash):
        """Set the boids hash

        Args:
            new_hash ([type]): the hash for the boid
        """
        self._hash = new_hash

    def __repr__(self) -> str:
        return (f"Boid(pos={self.pos}, dir={self.steer}, hash={self._hash})")
