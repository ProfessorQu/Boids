from pygame import Vector2
from typing import List

from boid import Boid


class SpatialHashGrid(object):
    def __init__(self, cell_size):
        """The init method for the hashgrid

        Args:
            cell_size ([type]): the sizeof the hashgrid cells
        """
        self.cell_size = cell_size
        self.grid = {}

    def _hash(self, point: Vector2) -> tuple:
        """Get the hash of a point

        Args:
            point (Vector2): the point to get the hash

        Returns:
            tuple: the hash or the key at that point
        """
        return point.x // self.cell_size, point.y // self.cell_size

    def insert(self, boid: Boid, point: Vector2):
        """Insert the boid at a point

        Args:
            boid (Boid): the target boid
            point (Vector2): the point at which to insert the target
        """
        point_hash = self._hash(point)

        self.grid.setdefault(point_hash, []).append(boid)
        boid.set_hash(point_hash)

    def delete(self, boid: Boid):
        """Delete a boid from a cell

        Args:
            boid (Boid): the target boid
        """
        boids_in_hash = self.grid.get(boid.hash, [])

        if boid in boids_in_hash:
            boids_in_hash.remove(boid)

            boid.set_hash(tuple)

    def move(self, boid: Boid, point: Vector2):
        """Move a boid from one cell to the other

        Args:
            boid (Boid): the target boid
            point (Vector2): the point to move the boid to
        """
        self.delete(boid)
        self.insert(boid, point)

    def get_close_boids(
        self, boid: Boid,
        perception: int, view_angle: float
    ) -> List[Boid]:
        """Get boids close to a certain boid

        Args:
            boid (Boid): the target boid
            perception (int): how many cells away the boid can see
            view_angle (float): the view angle at which the boid can see WIP

        Returns:
            List[Boid]: the boids that are close to the target
        """
        close_boids = []

        for x in range(1 - perception, perception):
            for y in range(1 - perception, perception):
                close_boids.extend(
                    self.grid.get((boid.hash[0] + x, boid.hash[1] + y), [])
                )

        return close_boids


# ------------ WIP ------------
        # boids_in_view = []
        # for other in close_boids:
        # # (right, bottom)
        # # print(other.pos - boid.pos)
        # # (right, bottom)
        # # print(boid.steer)

        # dir_to_other = Vector2(
        # max(min(other.pos.x - boid.pos.x, 1), -1),
        # max(min(other.pos.y - boid.pos.y, 1), -1)
        # )

        # current_dir = Vector2(
        # max(min(boid.steer.x, 1), -1),
        # max(min(boid.steer.y, 1), -1)
        # )

        # diff_sum = abs(current_dir.x + current_dir.y -
        # dir_to_other.x + dir_to_other.y)

        # if (diff_sum <= view_angle):
        # boids_in_view.append(other)
