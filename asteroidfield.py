# asteroidfield.py
#
# Defines AsteroidField — a manager object responsible for spawning new asteroids
# at regular intervals from the edges of the screen.
#
# It doesn't draw anything itself; its only job is to watch a timer and, when it
# fires, pick a random screen edge, random size, random speed, and create a new
# Asteroid aimed roughly toward the center of the play area.

import random

import pygame

from asteroid import Asteroid
from constants import *


class AsteroidField(pygame.sprite.Sprite):
    # `edges` is a class-level list defining the four screen borders.
    # Each entry is a pair:
    #   [0] - a direction vector pointing INWARD from that edge (so asteroids travel toward center)
    #   [1] - a lambda that generates a random spawn POSITION along that edge
    #         The lambda takes a value in [0, 1] and maps it to a pixel coordinate.
    #
    # The slight overshoot (±ASTEROID_MAX_RADIUS) places the spawn point just off-screen
    # so the asteroid "flies in" from beyond the visible edge rather than popping into view.
    edges = [
        [
            pygame.Vector2(1, 0),  # Left edge → push rightward
            lambda y: pygame.Vector2(-ASTEROID_MAX_RADIUS, y * SCREEN_HEIGHT),
        ],
        [
            pygame.Vector2(-1, 0),  # Right edge → push leftward
            lambda y: pygame.Vector2(
                SCREEN_WIDTH + ASTEROID_MAX_RADIUS, y * SCREEN_HEIGHT
            ),
        ],
        [
            pygame.Vector2(0, 1),  # Top edge → push downward
            lambda x: pygame.Vector2(x * SCREEN_WIDTH, -ASTEROID_MAX_RADIUS),
        ],
        [
            pygame.Vector2(0, -1),  # Bottom edge → push upward
            lambda x: pygame.Vector2(
                x * SCREEN_WIDTH, SCREEN_HEIGHT + ASTEROID_MAX_RADIUS
            ),
        ],
    ]

    def __init__(self):
        # Register with the sprite group defined in main.py via the `containers` mechanism.
        pygame.sprite.Sprite.__init__(self, self.containers)
        # spawn_timer accumulates elapsed time (in seconds) and resets each time
        # an asteroid is spawned.
        self.spawn_timer = 0.0

    def spawn(self, radius, position, velocity):
        # Create a new Asteroid. Because Asteroid.containers is set in main.py,
        # it automatically joins the correct sprite groups without any extra .add() call.
        asteroid = Asteroid(position.x, position.y, radius)
        asteroid.velocity = velocity

    def update(self, dt):
        # Accumulate time since the last spawn.
        self.spawn_timer += dt

        # Once the timer exceeds the spawn interval, spawn one asteroid and reset.
        if self.spawn_timer > ASTEROID_SPAWN_RATE_SECONDS:
            self.spawn_timer = 0

            # Pick one of the four edges at random.
            edge = random.choice(self.edges)

            # Choose a random travel speed and build the base velocity vector.
            # The edge's direction vector is a unit vector, so multiplying by `speed`
            # gives us pixels-per-second in that direction.
            speed = random.randint(40, 100)
            velocity = edge[0] * speed

            # Add a small random angle offset (±30°) so asteroids don't all travel
            # perfectly perpendicular to the edge — they fan in at slight angles.
            velocity = velocity.rotate(random.randint(-30, 30))

            # Pick a random spawn point along the chosen edge.
            # random.uniform(0, 1) gives a fractional position from one end to the other.
            position = edge[1](random.uniform(0, 1))

            # Pick a random size tier (1, 2, or 3) and multiply by the minimum radius
            # to get the actual radius for this asteroid.
            kind = random.randint(1, ASTEROID_KINDS)
            self.spawn(ASTEROID_MIN_RADIUS * kind, position, velocity)
