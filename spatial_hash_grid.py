from pygame import Vector2
from typing import List, Tuple
import numpy as np

from boid import Boid


class SpatialHashGrid(object):
    FOV_TO_RADIANS = 180 / np.pi / 2

    def __init__(self, cell_size: int,
                 perception: int, field_of_view: float):
        """The init method for the hashgrid

        Args:
            cell_size (int): the size of the hashgrid cells
            perception (int): how many cells away can a boid see
            field_of_view (float): what is the boid's field of view
        """
        # Set the cell size and the grid
        self.cell_size = cell_size
        self.grid = {}

        # Set the perception and calculate the field of view
        self._perception = perception
        self._field_of_view = field_of_view * SpatialHashGrid.FOV_TO_RADIANS

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
        # Get the hash of a point
        point_hash = self._hash(point)

        # Add the boid to the point hash
        self.grid.setdefault(point_hash, []).append(boid)
        boid.set_hash(point_hash)

    def delete(self, boid: Boid):
        """Delete a boid from a cell

        Args:
            boid (Boid): the target boid
        """
        # Get all boids in the same hash
        boids_in_hash = self.grid.get(boid.hash, [])

        # If the boid is in the boid hash, delete it
        if boid in boids_in_hash:
            boids_in_hash.remove(boid)
            boid.set_hash(tuple)

    def move(self, boid: Boid, point: Vector2):
        """Move a boid from one cell to the other

        Args:
            boid (Boid): the target boid
            point (Vector2): the point to move the boid to
        """
        # Remove and insert the boid
        self.delete(boid)
        self.insert(boid, point)

    def get_close_boids(
        self, boid: Boid
    ) -> Tuple[List[Boid], List[Boid]]:
        """Get boids close to a certain boid

        Args:
            boid (Boid): the target boid

        Returns:
            List[Boid]: the boids that are close to the target
        """
        close_boids = []
        boids_of_type = []

        # Loop over all cells in the perception range
        for x in range(1 - self._perception, self._perception):
            for y in range(1 - self._perception, self._perception):
                # Get boids in the current cell
                boids_in_cell = self.grid.get((boid.hash[0] + x,
                                               boid.hash[1] + y), [])

                for other in boids_in_cell:  # Loop over all boids in cell
                    #               c² - a² - b²
                    # C = arccos ( -------------  )
                    #                   -2ab

                    boid_to_other = boid.pos.distance_to(other.pos)  # c
                    boid_to_dir = boid.pos.distance_to(boid.dir)     # a
                    other_to_dir = other.pos.distance_to(boid.dir)   # b

                    if boid_to_other <= 0 or boid_to_dir <= 0:
                        # Add other to close boids
                        close_boids.append(other)

                        # Add other if it is the same type
                        if other.type == boid.type:
                            boids_of_type.append(other)

                        continue

                    c_min_a_min_b = (   # c² - a² - b²
                        other_to_dir ** 2 -
                        boid_to_other ** 2 -
                        boid_to_dir ** 2
                    )
                    neg_2_times_a_times_b = (  # -2ab
                        -2 * boid_to_other * boid_to_dir
                    )
                    angle = np.arccos(  # C
                        c_min_a_min_b /
                        neg_2_times_a_times_b
                    )

                    # Test if other is in boid's field of view
                    if (angle <= self._field_of_view or np.isnan(angle)):
                        # Add other to close boids
                        close_boids.append(other)

                        # Add other if it is the same type
                        if other.type == boid.type:
                            boids_of_type.append(other)

        return close_boids, boids_of_type
