from pygame import Vector2
import numpy as np

from boids import Flock


def test_create_boid():
    flock = Flock(
        num_boids=0,
        num_types=1,
        world_size=(100, 100),
        cell_size=10,
        max_speed=1,
        perception=1,
        field_of_view=360,
        avoid_dist=0,
        other_avoid_mult=1,
        other_avoid_dist=0,
        alignment_factor=0,
        cohesion_factor=0,
        seperation_factor=0,
        turn_margin=100,
        turn_factor=0,
        loop_bounds=True
    )
    for _ in range(100):
        boid = flock.create_boid(1, 360)

        assert -flock.max_speed <= boid.dir.x <= flock.max_speed
        assert -flock.max_speed <= boid.dir.y <= flock.max_speed

        assert 0 <= boid.pos.x <= 100
        assert 0 <= boid.pos.y <= 100

        assert boid.type == 0


def test_keep_in_bounds_loop():
    flock = Flock(
        num_boids=0,
        num_types=1,
        world_size=(100, 100),
        cell_size=10,
        max_speed=1,
        perception=1,
        field_of_view=360,
        avoid_dist=0,
        other_avoid_mult=1,
        other_avoid_dist=0,
        alignment_factor=0,
        cohesion_factor=0,
        seperation_factor=0,
        turn_margin=100,
        turn_factor=0,
        loop_bounds=True
    )
    boid = flock.create_boid(1, 360)

    boid.pos = Vector2(0, 0)
    boid.dir = Vector2(-1, 0)

    boid.pos += boid.dir
    flock.keep_in_bounds_loop(boid)

    assert boid.pos == Vector2(100, 0)

    boid.pos = Vector2(100, 0)
    boid.dir = Vector2(1, 0)

    boid.pos += boid.dir
    flock.keep_in_bounds_loop(boid)

    assert boid.pos == Vector2(0, 0)

    boid.pos = Vector2(0, 0)
    boid.dir = Vector2(0, -1)

    boid.pos += boid.dir
    flock.keep_in_bounds_loop(boid)

    assert boid.pos == Vector2(0, 100)

    boid.pos = Vector2(0, 100)
    boid.dir = Vector2(0, 1)

    boid.pos += boid.dir
    flock.keep_in_bounds_loop(boid)

    assert boid.pos == Vector2(0, 0)


def test_keep_in_bounds_turn():
    flock = Flock(
        num_boids=0,
        num_types=1,
        world_size=(100, 100),
        cell_size=10,
        max_speed=1,
        perception=1,
        field_of_view=360,
        avoid_dist=0,
        other_avoid_mult=1,
        other_avoid_dist=0,
        alignment_factor=0,
        cohesion_factor=0,
        seperation_factor=0,
        turn_margin=10,
        turn_factor=1,
        loop_bounds=False
    )
    boid = flock.create_boid(1, 360)

    boid.pos = Vector2(9, 50)
    boid.dir = Vector2(-1, 0)

    flock.keep_in_bounds_turn(boid)

    assert boid.dir == Vector2(0, 0)

    boid.pos = Vector2(10, 50)
    boid.dir = Vector2(-1, 0)

    flock.keep_in_bounds_turn(boid)

    assert boid.dir == Vector2(-1, 0)

    boid.pos = Vector2(90, 50)
    boid.dir = Vector2(1, 0)

    flock.keep_in_bounds_turn(boid)

    assert boid.dir == Vector2(1, 0)

    boid.pos = Vector2(91, 50)
    boid.dir = Vector2(1, 0)

    flock.keep_in_bounds_turn(boid)

    assert boid.dir == Vector2(0, 0)

    boid = flock.create_boid(1, 360)

    boid.pos = Vector2(50, 9)
    boid.dir = Vector2(0, -1)

    flock.keep_in_bounds_turn(boid)

    assert boid.dir == Vector2(0, 0)

    boid.pos = Vector2(50, 10)
    boid.dir = Vector2(0, -1)

    flock.keep_in_bounds_turn(boid)

    assert boid.dir == Vector2(0, -1)

    boid.pos = Vector2(50, 90)
    boid.dir = Vector2(0, 1)

    flock.keep_in_bounds_turn(boid)

    assert boid.dir == Vector2(0, 1)

    boid.pos = Vector2(50, 91)
    boid.dir = Vector2(0, 1)

    flock.keep_in_bounds_turn(boid)

    assert boid.dir == Vector2(0, 0)

    boid.pos = Vector2(100, 100)
    boid.dir = Vector2(2, 2)

    flock.keep_in_bounds_turn(boid)

    assert boid.dir == Vector2(1, 1)


def test_limit_speed():
    flock = Flock(
        num_boids=0,
        num_types=1,
        world_size=(100, 100),
        cell_size=10,
        max_speed=5,
        perception=1,
        field_of_view=360,
        avoid_dist=0,
        other_avoid_mult=1,
        other_avoid_dist=0,
        alignment_factor=0,
        cohesion_factor=0,
        seperation_factor=0,
        turn_margin=10,
        turn_factor=1,
        loop_bounds=True
    )

    boid = flock.create_boid(1, 360)

    for _ in range(100):
        boid.dir = Vector2(np.random.uniform(-10, 10),
                           np.random.uniform(-10, 10))
        speed = np.sqrt(boid.dir.x ** 2 + boid.dir.y ** 2)

        if speed > flock.max_speed:
            flock.limit_speed(boid)
            current_speed = np.sqrt(boid.dir.x ** 2 + boid.dir.y ** 2)

            assert current_speed < speed


def test_alignment():
    flock = Flock(
        num_boids=0,
        num_types=1,
        world_size=(100, 100),
        cell_size=10,
        max_speed=5,
        perception=1,
        field_of_view=360,
        avoid_dist=0,
        other_avoid_mult=1,
        other_avoid_dist=0,
        alignment_factor=1,
        cohesion_factor=0,
        seperation_factor=0,
        turn_margin=10,
        turn_factor=1,
        loop_bounds=True
    )

    for _ in range(100):
        boid1 = flock.create_boid(1, 360)
        boid2 = flock.create_boid(1, 360)

        boid1.dir = Vector2(np.random.uniform(-5, 5),
                            np.random.uniform(-5, 5))
        boid2.dir = Vector2(np.random.uniform(-5, 5),
                            np.random.uniform(-5, 5))

        flock.alignment(boid1, [boid2])
        assert boid1.dir == boid2.dir


def test_alignment_multiple_types():
    flock = Flock(
        num_boids=0,
        num_types=1,
        world_size=(100, 100),
        cell_size=10,
        max_speed=5,
        perception=1,
        field_of_view=360,
        avoid_dist=0,
        other_avoid_mult=1,
        other_avoid_dist=0,
        alignment_factor=1,
        cohesion_factor=0,
        seperation_factor=0,
        turn_margin=10,
        turn_factor=1,
        loop_bounds=True
    )

    for _ in range(100):
        boid1 = flock.create_boid(1, 360)
        boid2 = flock.create_boid(1, 360)

        boid1.dir = Vector2(np.random.uniform(-5, 5),
                            np.random.uniform(-5, 5))
        boid2.dir = Vector2(np.random.uniform(-5, 5),
                            np.random.uniform(-5, 5))

        boid1.type = 0
        boid2.type = 1

        prev_dir = boid1.dir

        flock.alignment(boid1, [boid2])
        assert boid1.dir == prev_dir


def test_cohesion():
    flock = Flock(
        num_boids=0,
        num_types=1,
        world_size=(100, 100),
        cell_size=10,
        max_speed=5,
        perception=2,
        field_of_view=360,
        avoid_dist=0,
        other_avoid_mult=1,
        other_avoid_dist=0,
        alignment_factor=0,
        cohesion_factor=1,
        seperation_factor=0,
        turn_margin=10,
        turn_factor=1,
        loop_bounds=True
    )

    for _ in range(100):
        boid1 = flock.create_boid(1, 360)
        boid2 = flock.create_boid(1, 360)

        boid1.pos = Vector2(np.random.uniform(0, 50),
                            np.random.uniform(0, 50))
        boid2.pos = Vector2(np.random.uniform(0, 50),
                            np.random.uniform(0, 50))

        boid1.dir = Vector2(0, 0)
        boid2.dir = Vector2(0, 0)

        dist = boid1.pos.distance_to(boid2.pos)

        flock.cohesion(boid1, [boid2])
        boid1.pos += boid1.dir

        current_dist = boid1.pos.distance_to(boid2.pos)

        assert current_dist < dist


def test_cohesion_multiple_types():
    flock = Flock(
        num_boids=0,
        num_types=2,
        world_size=(100, 100),
        cell_size=10,
        max_speed=5,
        perception=2,
        field_of_view=360,
        avoid_dist=0,
        other_avoid_mult=1,
        other_avoid_dist=0,
        alignment_factor=0,
        cohesion_factor=1,
        seperation_factor=0,
        turn_margin=10,
        turn_factor=1,
        loop_bounds=True
    )

    for _ in range(100):
        boid1 = flock.create_boid(1, 360)
        boid2 = flock.create_boid(1, 360)

        boid1.pos = Vector2(10, np.random.uniform(0, 50))
        boid2.pos = Vector2(-10, np.random.uniform(0, 50))

        boid1.dir = Vector2(1, 0)

        boid1.type = 0
        boid2.type = 1

        dist = boid1.pos.distance_to(boid2.pos)

        flock.cohesion(boid1, [boid1])
        boid1.pos += boid1.dir

        current_dist = boid1.pos.distance_to(boid2.pos)

        assert current_dist > dist


def test_seperation():
    flock = Flock(
        num_boids=0,
        num_types=1,
        world_size=(100, 100),
        cell_size=10,
        max_speed=5,
        perception=2,
        field_of_view=360,
        avoid_dist=50,
        other_avoid_mult=1,
        other_avoid_dist=0,
        alignment_factor=0,
        cohesion_factor=0,
        seperation_factor=1,
        turn_margin=10,
        turn_factor=1,
        loop_bounds=True
    )

    for _ in range(100):
        boid1 = flock.create_boid(1, 360)
        boid2 = flock.create_boid(1, 360)

        boid1.pos = Vector2(np.random.uniform(0, 50),
                            np.random.uniform(0, 50))
        boid2.pos = Vector2(np.random.uniform(0, 50),
                            np.random.uniform(0, 50))

        boid1.dir = Vector2(0, 0)
        boid2.dir = Vector2(0, 0)

        dist = boid1.pos.distance_to(boid2.pos)

        flock.seperation(boid1, [boid2])
        boid1.pos += boid1.dir

        current_dist = boid1.pos.distance_to(boid2.pos)

        if dist <= flock.avoid_dist:
            assert current_dist > dist
        else:
            assert current_dist == dist


def test_seperation_multiple_types():
    flock = Flock(
        num_boids=0,
        num_types=2,
        world_size=(100, 100),
        cell_size=10,
        max_speed=5,
        perception=2,
        field_of_view=360,
        avoid_dist=50,
        other_avoid_mult=1,
        other_avoid_dist=50,
        alignment_factor=0,
        cohesion_factor=0,
        seperation_factor=1,
        turn_margin=10,
        turn_factor=1,
        loop_bounds=True
    )

    for _ in range(100):
        boid1 = flock.create_boid(1, 360)
        boid2 = flock.create_boid(1, 360)

        boid1.pos = Vector2(np.random.uniform(0, 50),
                            np.random.uniform(0, 50))
        boid2.pos = Vector2(np.random.uniform(0, 50),
                            np.random.uniform(0, 50))

        boid1.dir = Vector2(0, 0)
        boid2.dir = Vector2(0, 0)

        boid1.type = 0
        boid2.type = 1

        dist = boid1.pos.distance_to(boid2.pos)

        flock.seperation(boid1, [boid2])
        boid1.pos += boid1.dir

        current_dist = boid1.pos.distance_to(boid2.pos)

        if dist <= flock.avoid_dist:
            assert current_dist > dist
        else:
            assert current_dist == dist
