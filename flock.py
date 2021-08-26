from typing import List
from pygame import Vector2
import numpy as np
import pygame

from spatial_hash_grid import SpatialHashGrid
from boid import Boid


class Flock(object):
    def __init__(self, num_boids: int, num_types: int,
                 world_size: tuple, cell_size: int,
                 max_speed: int,
                 perception: int, field_of_view: float,
                 avoid_dist: int, other_avoid_mult: float,
                 other_avoid_dist: int,
                 alignment_factor: float, cohesion_factor: float,
                 seperation_factor: float,
                 turn_margin: int, turn_factor: float,
                 loop_bounds: bool = True):
        """The init method

        Args:
            num_boids (int): the number of boids
            num_types (int): the number of types of boids
            world_size (tuple): the size of the world
            cell_size (int): the size of the hash grid cells
            max_speed (int): the maximum speed
            perception (int): how many cells away can a boid see
            field_of_view (float): how wide is a boid's vision
            avoid_dist (int): distance to keep between boids
            other_avoid_mult (float): multiplier of avoiding other types
            other_avoid_dist (int): distance to keep between other types
            alignment_factor (float): the factor of alignment
            cohesion_factor (float): the factor of cohesion
            seperation_factor (float): the factor of seperation
            turn_margin (int): margin when the boids need to turn
            turn_factor (float): how much to turn when in the turn margin
            loop_bounds (bool, optional): use loop or turn. Defaults to True.
        """
        self._boids = []

        self._world_size = Vector2(world_size[0], world_size[1])
        self._spatial_hash_grid = SpatialHashGrid(
            cell_size,
            perception, field_of_view
        )
        self._max_speed = max_speed

        # Seperation variables
        self._avoid_dist = avoid_dist
        self._other_avoid_dist = other_avoid_dist
        self._other_avoid_mult = other_avoid_mult

        # Factors of all the rules
        self._alignment_factor = alignment_factor
        self._cohesion_factor = cohesion_factor
        self._seperation_factor = seperation_factor

        if loop_bounds:
            self._keep_in_bounds = self._keep_in_bounds_loop
        else:
            self._keep_in_bounds = self._keep_in_bounds_turn
            self._turn_margin = turn_margin
            self._turn_factor = turn_factor

        self.reset_boids(num_boids, num_types)

    def reset_boids(self, num_boids: int, num_types: int,
                    size: int, size_deviation: int):
        # Remove all previous boids
        for boid in self._boids:
            self._spatial_hash_grid.delete(boid)

        self._boids = []
        color_scale = 360 / num_types

        # Create the boids
        for _ in range(num_boids):
            boid = self.create_boid(num_types, color_scale,
                                    size, size_deviation)

            self._spatial_hash_grid.insert(boid, boid.pos)
            self._boids.append(boid)

    def create_boid(self, num_types: int, color_scale: int,
                    size: int, size_dev: int):
        # Set a random position
        pos = Vector2(
            np.random.uniform(0, self._world_size.x),
            np.random.uniform(0, self._world_size.y)
        )

        # Set a random direction
        dir_ = Vector2(
            np.random.uniform(-self._max_speed, self._max_speed),
            np.random.uniform(-self._max_speed, self._max_speed)
        )

        # Set a random type
        type_ = np.random.randint(0, num_types)

        # Set a random color
        color = pygame.Color(0, 0, 0)
        color.hsla = (type_ * color_scale, 100, 50, 100)

        size_ = size + np.random.randint(-size_dev, size_dev)

        # Return the boid
        return Boid(pos, dir_, type_, color, size_)

    def update_boids(self):
        """Update the boids
        """
        # Update all the boids
        for boid in self._boids:
            # Get all close boids
            all_boids = self._spatial_hash_grid.get_boids(boid)
            boids, boids_of_type = all_boids

            # Seperate from ALL boids
            if boids:
                self._seperation(boid, boids)
            # Only align and cohese with boids of boid's own type
            if boids_of_type:
                self._alignment(boid, boids_of_type)
                self._cohesion(boid, boids_of_type)

            # Keep the boid within bounds
            self._keep_in_bounds(boid)
            # Limit the boid's speed
            self._limit_speed(boid)

            # Update the boid's position
            boid.pos += boid.dir
            self._spatial_hash_grid.move(boid, boid.pos)

    def _keep_in_bounds_loop(self, boid: Boid):
        """Keep a boid in bounds by looping

        Args:
            boid (Boid): the target boid
        """
        if boid.pos.x > self._world_size.x:
            boid.pos.x = 0
        elif boid.pos.x < 0:
            boid.pos.x = self._world_size.x

        if boid.pos.y > self._world_size.y:
            boid.pos.y = 0
        elif boid.pos.y < 0:
            boid.pos.y = self._world_size.y

    def _keep_in_bounds_turn(self, boid: Boid):
        """Keeps a boid in bounds by turning

        Args:
            boid (Boid): the target boid
        """
        if (boid.pos.x < self._turn_margin):
            boid.dir.x += self._turn_factor
        if (boid.pos.x > self._world_size.x - self._turn_margin):
            boid.dir.x -= self._turn_factor

        if (boid.pos.y < self._turn_margin):
            boid.dir.y += self._turn_factor
        if (boid.pos.y > self._world_size.y - self._turn_margin):
            boid.dir.y -= self._turn_factor

    def _limit_speed(self, boid: Boid):
        """Limit the speed of a boid

        Args:
            boid (Boid): the target boid
        """
        # Calculate speed
        speed = np.sqrt(boid.dir.x ** 2 + boid.dir.y ** 2)

        # Lower speed if it exceeds the max speed
        if speed > self._max_speed:
            boid.dir = (boid.dir / speed) * self._max_speed

    def _alignment(self, boid: Boid, boids_of_type: List[Boid]):
        """Align with closeby boids of the same type

        Args:
            boid (Boid): the target boid
            boids_of_type (List[Boid]): the closeby boids of the same type
        """
        # Get the average direction of all close boids
        avg_dir = Vector2(0, 0)

        for other in boids_of_type:
            avg_dir += other.dir

        avg_dir /= len(boids_of_type)

        # Update the boid's direction
        boid.dir += (avg_dir - boid.dir) * self._alignment_factor

    def _cohesion(self, boid: Boid, boids_of_type: List[Boid]):
        """Go to the center of mass of closeby boids of the same type

        Args:
            boid (Boid): the target boid
            boids_of_type (List[Boid]): the closeby boids of the same type
        """
        # Get the center of mass of all close boids
        center_of_mass = Vector2(0, 0)

        for other in boids_of_type:
            center_of_mass += other.pos

        center_of_mass /= len(boids_of_type)

        # Update the boid's direction
        boid.dir += (center_of_mass - boid.pos) * self._cohesion_factor

    def _seperation(self, boid: Boid, close_boids: List[Boid]):
        """Move away from closeby boids to not bundle up

        Args:
            boid (Boid): the target boid
            close_boids (List[Boid]): all the closeby boids
        """
        # Get the avoidance to all close boids
        avoid = Vector2(0, 0)

        for other in close_boids:
            dist = boid.pos.distance_to(other.pos)

            other_type = abs(boid.type - other.type)
            if other_type:
                other_avoid = min(other_type, 1) * \
                    self._other_avoid_mult + 1

                if dist <= self._other_avoid_dist:
                    avoid += (boid.pos - other.pos) * other_avoid
            elif dist <= self._avoid_dist:
                avoid += (boid.pos - other.pos)

        # Update the boids direction
        boid.dir += avoid * self._seperation_factor

    @property
    def alignment(self) -> float:
        return self._alignment_factor

    @alignment.setter
    def alignment(self, a):
        self._alignment_factor = a

    @property
    def cohesion(self) -> float:
        return self._cohesion_factor

    @cohesion.setter
    def cohesion(self, c):
        self._cohesion_factor = c / 500

    @property
    def seperation(self) -> float:
        return self._seperation_factor

    @seperation.setter
    def seperation(self, s):
        self._seperation_factor = s

    @property
    def max_speed(self) -> float:
        return self._max_speed

    @max_speed.setter
    def max_speed(self, ms):
        self._max_speed = ms

    @property
    def avoid_dist(self) -> float:
        return self._avoid_dist

    @avoid_dist.setter
    def avoid_dist(self, ad):
        self._avoid_dist = ad

    @property
    def other_avoid_dist(self) -> float:
        return self._other_avoid_dist

    @other_avoid_dist.setter
    def other_avoid_dist(self, oad):
        self._other_avoid_dist = oad

    @property
    def other_avoid_mult(self) -> float:
        return self._other_avoid_mult

    @other_avoid_mult.setter
    def other_avoid_mult(self, oam):
        self._other_avoid_mult = oam

    @property
    def perception(self) -> float:
        return self._spatial_hash_grid.perception

    @perception.setter
    def perception(self, p):
        self._spatial_hash_grid.perception = p

    @property
    def field_of_view(self) -> float:
        return self._spatial_hash_grid.field_of_view

    @field_of_view.setter
    def field_of_view(self, fov):
        self._spatial_hash_grid.field_of_view = fov

    @property
    def boids(self) -> List[Boid]:
        """Get the boids

        Returns:
            List[Boid]: the list of boids
        """
        return self._boids
