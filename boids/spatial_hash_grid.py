from pygame import Vector2
from typing import List, Tuple
import numpy as np

from boids.boid import Boid


class SpatialHashGrid:
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
        self.perception = perception
        self.field_of_view = field_of_view / 2  # Dividing by 2 for angle

    def hash(self, point: Vector2) -> tuple:
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
        point_hash = self.hash(point)

        # Add the boid to the point hash
        self.grid.setdefault(point_hash, []).append(boid)
        boid.hash = point_hash

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
            boid.hash = tuple

    def move(self, boid: Boid, point: Vector2):
        """Move a boid from one cell to the other

        Args:
            boid (Boid): the target boid
            point (Vector2): the point to move the boid to
        """
        # Remove and insert the boid
        self.delete(boid)
        self.insert(boid, point)

    def get_boids(
        self, boid: Boid
    ) -> Tuple[List[Boid], List[Boid]]:
        """Get boids close to a certain boid

        Args:
            boid (Boid): the target boid

        Returns:
            List[Boid]: the boids that are close to the target
        """
        boids = []
        boids_of_type = []

        # Loop over all cells in the perception range
        for x in range(1 - self.perception, self.perception):
            for y in range(1 - self.perception, self.perception):
                # Get boids in the current cell
                boids_in_cell = self.grid.get((boid.hash[0] + x,
                                               boid.hash[1] + y), [])

                for other in boids_in_cell:  # Loop over all boids in cell
                    boid_to_dir = boid.dir - boid.pos
                    boid_to_other = other.pos - boid.pos

                    angle = abs(boid_to_dir.angle_to(boid_to_other))

                    # Test if other is in boid's field of view
                    if (angle <= self.field_of_view or np.isnan(angle)):
                        # Add other to close boids
                        boids.append(other)

                        # Add other if it is the same type
                        if other.type == boid.type:
                            boids_of_type.append(other)

        return boids, boids_of_type
