from typing import List
from pygame import Vector2
import numpy as np

from spatial_hash_grid import SpatialHashGrid
from boid import Boid


class Boids(object):
    def __init__(self, num_boids: int, world_size: int, max_speed: int,
                 perception: int, view_angle: float,
                 avoid_distance: int, cell_size: int,
                 alignment_factor: float, cohesion_factor: int,
                 seperation_factor: int):
        """The init method

        Args:
            num_boids (int): the amount of boids to create
            world_size (int): the size of world
            max_speed (int): the speed limit for the boids
            perception (int): how many cells the boids can see
            view_angle (float): their view angle
            avoid_distance (int): the distance at which they avoid other boids
            cell_size (int): the sizes of the hashgrid cells
            alignment_factor (float): how much does alignment weigh
            cohesion_factor (int): how much does cohesion weigh
            seperation_factor (int): how much does seperation weigh
        """

        self._width, self._height = world_size[0], world_size[1]
        self._spatial_hash_grid = SpatialHashGrid(cell_size)
        self._boids = []

        self._max_speed = max_speed
        self._perception = perception
        self._view_angle = view_angle
        self._avoid_distance = avoid_distance

        self.alignment_factor = alignment_factor
        self.cohesion_factor = cohesion_factor
        self.seperation_factor = seperation_factor

        for _ in range(num_boids):
            pos = Vector2(
                np.random.uniform(0, self._width),
                np.random.uniform(0, self._height)
            )

            steer = Vector2(
                np.random.uniform(-self._max_speed, self._max_speed),
                np.random.uniform(-self._max_speed, self._max_speed)
            )

            boid = Boid(pos, steer)

            self._spatial_hash_grid.insert(boid, pos)
            self._boids.append(boid)

    def update_boids(self):
        """Update the boids
        """
        for boid in self._boids:
            close_boids = self._spatial_hash_grid.get_close_boids(
                boid, self._perception, self._view_angle
            )

            if close_boids:
                self._alignment(boid, close_boids)
                self._cohesion(boid, close_boids)
                self._seperation(boid, close_boids)

            self._keep_in_bounds(boid)
            self._limit_speed(boid)

            boid.pos += boid.steer

            self._spatial_hash_grid.move(boid, boid.pos)

    def _keep_in_bounds(self, boid: Boid):
        """Keep a boid in bounds

        Args:
            boid (Boid): the target boid
        """
        if boid.pos.x > self._width:
            boid.pos.x = 0
        elif boid.pos.x < 0:
            boid.pos.x = self._width

        if boid.pos.y > self._height:
            boid.pos.y = 0
        elif boid.pos.y < 0:
            boid.pos.y = self._height

    def _limit_speed(self, boid: Boid):
        """Limit the speed of a boid

        Args:
            boid (Boid): the target boid
        """
        speed = np.sqrt(boid.steer.x ** 2 + boid.steer.y ** 2)

        if speed > self._max_speed:
            boid.steer = (boid.steer / speed) * self._max_speed

    def _alignment(self, boid: Boid, close_boids: List[Boid]):
        """Align with closeby boids

        Args:
            boid (Boid): the target boids
            close_boids (List[Boid]): the closeby boids
        """
        avg_steer = Vector2(0, 0)

        for other in close_boids:
            avg_steer += other.steer

        avg_steer /= len(close_boids)

        boid.steer += (avg_steer - boid.steer) * self.alignment_factor

    def _cohesion(self, boid: Boid, close_boids: List[Boid]):
        """Go to the center of mass of closeby boids

        Args:
            boid (Boid): the target boid
            close_boids (List[Boid]): the closeby boids
        """
        center = Vector2(0, 0)

        for other in close_boids:
            center += other.pos

        center /= len(close_boids)

        boid.steer += (center - boid.pos) * self.cohesion_factor

    def _seperation(self, boid: Boid, close_boids: List[Boid]):
        """Move away from closeby boids to not bundle up

        Args:
            boid (Boid): the target boid
            close_boids (List[Boid]): the closeby boids
        """
        move = Vector2(0, 0)

        for other in close_boids:
            dist = np.sqrt(
                (boid.pos.x - other.pos.x) ** 2 +
                (boid.pos.y - other.pos.y) ** 2
            )

            if dist < self._avoid_distance:
                move += boid.pos - other.pos

        boid.steer += move * self.seperation_factor

    @property
    def boids(self) -> List[Boid]:
        return self._boids
