from pygame import Vector2
import numpy as np

from boids import SpatialHashGrid, Flock, Boid


def test_hash():
    spatial_hash_grid = SpatialHashGrid(
        cell_size=100,
        perception=2,
        field_of_view=360
    )

    point_hash = spatial_hash_grid.hash(Vector2(99, 99))
    assert point_hash == (0, 0)

    point_hash = spatial_hash_grid.hash(Vector2(100, 100))
    assert point_hash == (1, 1)

    point_hash = spatial_hash_grid.hash(Vector2(199, 199))
    assert point_hash == (1, 1)

    point_hash = spatial_hash_grid.hash(Vector2(200, 200))
    assert point_hash == (2, 2)


def test_insert():
    spatial_hash_grid = SpatialHashGrid(
        cell_size=100,
        perception=2,
        field_of_view=360
    )

    for _ in range(100):
        boid = Boid(Vector2(
            np.random.uniform(0, 1000),
            np.random.uniform(0, 1000)
        ),
            Vector2(0, 0),
            0, (0, 0, 0))

        spatial_hash_grid.insert(boid, Vector2(0, 0))
        assert boid in spatial_hash_grid.grid[boid.hash]


def test_delete():
    spatial_hash_grid = SpatialHashGrid(
        cell_size=100,
        perception=2,
        field_of_view=360
    )

    for _ in range(100):
        boid = Boid(Vector2(
            np.random.uniform(0, 1000),
            np.random.uniform(0, 1000)
        ),
            Vector2(0, 0),
            0, (0, 0, 0))

        spatial_hash_grid.insert(boid, Vector2(0, 0))
        prev_boid_hash = boid.hash
        spatial_hash_grid.delete(boid)

        assert boid not in spatial_hash_grid.grid[prev_boid_hash]


def test_move():
    spatial_hash_grid = SpatialHashGrid(
        cell_size=100,
        perception=2,
        field_of_view=360
    )

    for _ in range(100):
        boid = Boid(
            Vector2(np.random.uniform(0, 1000),
                    np.random.uniform(0, 1000)),
            Vector2(np.random.randint(-1, 1) * 100,
                    np.random.randint(-1, 1) * 100),
            0, (0, 0, 0)
        )

        spatial_hash_grid.insert(boid, boid.pos)
        prev_boid_hash = boid.hash
        spatial_hash_grid.move(boid, boid.pos + boid.dir)

        if boid.dir.x == 0 and boid.dir.y == 0:
            assert boid.hash == prev_boid_hash
        else:
            assert boid.hash != prev_boid_hash


def create_boid(flock: Flock, x: int, y: int, type_: int):
    boid = flock.create_boid(2, 180)
    boid.pos = Vector2(x, y)
    boid.dir = Vector2(1, 1)
    boid.type = type_
    flock.spatial_hash_grid.insert(boid, boid.pos)

    return boid


def test_get_boids():
    flock = Flock(
        num_boids=0,
        num_types=1,
        world_size=(1000, 1000),
        cell_size=10,
        max_speed=1,
        perception=2,
        field_of_view=270,
        avoid_dist=0,
        other_avoid_mult=1,
        other_avoid_dist=0,
        alignment_factor=0,
        cohesion_factor=0,
        seperation_factor=0,
        turn_margin=0,
        turn_factor=0,
        loop_bounds=True
    )

    boid1 = create_boid(flock, 0, 0, 0)
    boid2 = create_boid(flock, 1, 1, 0)
    flock.boids = [boid1, boid2]

    boids, boids_of_type = flock.spatial_hash_grid.get_boids(boid1)
    assert boid2 in boids and boid2 in boids_of_type

    boids, boids_of_type = flock.spatial_hash_grid.get_boids(boid2)
    assert boid1 not in boids and boid2 not in boids_of_type

    flock.spatial_hash_grid.delete(boid1)
    flock.spatial_hash_grid.delete(boid2)


def test_get_boids_multiple_types():
    flock = Flock(
        num_boids=0,
        num_types=2,
        world_size=(1000, 1000),
        cell_size=10,
        max_speed=1,
        perception=2,
        field_of_view=270,
        avoid_dist=0,
        other_avoid_mult=1,
        other_avoid_dist=0,
        alignment_factor=0,
        cohesion_factor=0,
        seperation_factor=0,
        turn_margin=0,
        turn_factor=0,
        loop_bounds=True
    )

    boid1 = create_boid(flock, 0, 0, 0)
    boid2 = create_boid(flock, 1, 1, 1)
    flock.boids = [boid1, boid2]

    boids, boids_of_type = flock.spatial_hash_grid.get_boids(boid1)
    assert boid2 in boids and boid2 not in boids_of_type

    boids, boids_of_type = flock.spatial_hash_grid.get_boids(boid2)
    assert boid1 not in boids and boid1 not in boids_of_type

    flock.spatial_hash_grid.delete(boid1)
    flock.spatial_hash_grid.delete(boid2)
