from typing import List
from pygame import Vector2
import numpy as np


class Boid(object):
    """The boid object with a position and steerection
    """

    def __init__(self, pos: Vector2, steer: Vector2,
                 perception: float, avoidance: float):
        """The initialize method

        Args:
            pos (Vector2): the position of the boid
            steer (Vector2): the direction of the boid
            perception (float): how far the boid can see
        """
        self.pos = pos
        self.steer = steer

        self.perception = perception
        self.avoidance = avoidance

    def update_pos(self):
        """Update position according to steerection
        """
        self.pos += self.steer

    def get_closest_boids(self, flock: list):
        """Find all boids in a certain range

        Args:
            flock (list): the flock of boids
            perception (float): the range to search for boids

        Returns:
            list: the boids within range
        """
        closest_boids = []

        for boid in flock:
            if boid != self:
                c = (self.pos - boid.pos) ** 2

                dist = np.sqrt(c.x + c.y)

                if dist <= self.perception:
                    closest_boids.append(boid)

        return closest_boids

    def __repr__(self):
        return (f"Boid(pos={self.pos}, dir={self.steer})")

    def __str__(self):
        return (f"Boid(pos={self.pos}, dir={self.steer})")


def create_flock(num_boids: int,  canvas_size: tuple,
                 perception: float, avoidance: float):
    """Create a flock, a list of boids.

    Args:
        num_boids (int): the amount of boids
        canvas_size (tuple): the size of the canvas

    Returns:
        list: the flock or list of boids
    """
    width = canvas_size[0]
    height = canvas_size[1]

    flock = []

    for _ in range(num_boids):
        pos = Vector2(
            np.random.uniform(0, width),
            np.random.uniform(0, height)
        )

        steer = Vector2(
            np.random.uniform(-width / 100, width / 100),
            np.random.uniform(-height / 100, height / 100)
        )

        flock.append(Boid(pos, steer, perception, avoidance))

    return flock


def turn(boid: Boid, bounds: dict, turn_factor: float):
    """Turn boids at edge

    Args:
        boid (Boid): the boid that is turning
        bounds (dict): the bounds
        turn_factor (float): the turn factor
    """
    if boid.pos.x < bounds["min_x"]:
        boid.steer.x += turn_factor
    elif boid.pos.x > bounds["max_x"]:
        boid.steer.x -= turn_factor

    if boid.pos.y < bounds["min_y"]:
        boid.steer.y += turn_factor
    elif boid.pos.y > bounds["max_y"]:
        boid.steer.y -= turn_factor


def loop(boid: Boid, bounds: dict, turn_factor: float):
    """Loop boids at the edge

    Args:
        boid (Boid): the boid that is looping
        bounds (dict): the bounds
        turn_factor (float): this does not do anything
    """
    if boid.pos.x < bounds["min_x"]:
        boid.pos.x = bounds["max_x"]
    elif boid.pos.x > bounds["max_x"]:
        boid.pos.x = bounds["min_x"]

    if boid.pos.y < bounds["min_y"]:
        boid.pos.y = bounds["max_y"]
    elif boid.pos.y > bounds["max_y"]:
        boid.pos.y = bounds["min_y"]


def get_steer(boid_pos: Vector2, compare_pos: Vector2):
    return Vector2(boid_pos.x - compare_pos.x, boid_pos.y - compare_pos.y)


def alignment(boid: Boid, closest_boids: List[Boid]):
    avg_steer = Vector2(0, 0)

    for c_boid in closest_boids:
        avg_steer += c_boid.steer

    avg_steer /= len(closest_boids)

    return get_steer(boid.steer, avg_steer)


def cohesion(boid: Boid, closest_boids: List[Boid]):
    center = Vector2(0, 0)

    for c_boid in closest_boids:
        center += c_boid.pos

    center /= len(closest_boids)

    return get_steer(boid.pos, center)


def seperation(boid: Boid, closest_boids: List[Boid]):
    avoid = Vector2(0, 0)

    pos = boid.pos

    for other in closest_boids:
        o_pos = other.pos

        if abs(pos.x - o_pos.x) < boid.avoidance:
            avoid.x = pos.x - o_pos.x

        if abs(pos.y - o_pos.y) < boid.avoidance:
            avoid.y = pos.y - o_pos.y

    return avoid


align_impact = 2
cohese_impact = 1
seperate_impact = 00.1


def update(flock: List[Boid], bounds: dict,
           turn_factor: float, speed_limit: float,
           should_loop: bool = False):
    keep_in_bounds = turn

    if should_loop:
        keep_in_bounds = loop

    for boid in flock:
        boid.update_pos()

        keep_in_bounds(boid, bounds, turn_factor)

        closest_boids = boid.get_closest_boids(flock)

        if closest_boids:
            align = alignment(boid, closest_boids) * align_impact
            cohese = cohesion(boid, closest_boids) * cohese_impact
            seperate = seperation(boid, closest_boids) * seperate_impact

            # print(f"{align=}")
            # print(f"{cohese=}")
            # print(f"{seperate=}")

            boid.steer += align + cohese + seperate

        boid.steer.x = min(max(boid.steer.x, -speed_limit), speed_limit)
        boid.steer.y = min(max(boid.steer.y, -speed_limit), speed_limit)
