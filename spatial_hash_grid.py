from pygame import Vector2
from typing import List
import numpy as np

from boid import Boid


class SpatialHashGrid(object):
    def __init__(self, cell_size: int,
                 perception: int, field_of_view: float):
        """The init method for the hashgrid

        Args:
            cell_size (int): the size of the hashgrid cells
            perception (int): how many cells away can a boid see
            field_of_view (float): what is the boid's field of view
        """
        self.cell_size = cell_size
        self.grid = {}

        self._perception = perception
        self._field_of_view = field_of_view
        self._radians_to_degrees = 180 / np.pi

    def distance(self, point1: Vector2, point2: Vector2) -> float:
        """Calculate distance between two points

        Args:
            point1 (Vector2): the first point
            point2 (Vector2): the second point

        Returns:
            float: the distance from point1 to point2
        """
        diff = point1 - point2
        a = diff.x ** 2
        b = diff.y ** 2

        return np.sqrt(a + b)

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
        self, boid: Boid
    ) -> List[Boid]:
        """Get boids close to a certain boid

        Args:
            boid (Boid): the target boid

        Returns:
            List[Boid]: the boids that are close to the target
        """
        close_boids = []

        for x in range(1 - self._perception, self._perception):
            for y in range(1 - self._perception, self._perception):
                close_boids.extend(
                    self.grid.get((boid.hash[0] + x, boid.hash[1] + y), [])
                )

        boids_in_view = []
        for other in close_boids:
            #           c**2 - a**2 - b**2
            # cos C =   ------------------
            #                 -2ab

            boid_to_other = self.distance(boid.pos, other.pos)
            boid_to_steer = self.distance(boid.pos, boid.steer)
            other_to_steer = self.distance(other.pos, boid.steer)

            c_min_a_min_b = (
                other_to_steer ** 2 -
                boid_to_other ** 2 -
                boid_to_steer ** 2
            )
            neg_2_times_a_times_b = -2 * boid_to_other * boid_to_steer
            angle = np.arccos(
                c_min_a_min_b /
                neg_2_times_a_times_b
            ) * self._radians_to_degrees

            if (angle <= self._field_of_view or np.isnan(angle)):
                boids_in_view.append(other)

        return boids_in_view
