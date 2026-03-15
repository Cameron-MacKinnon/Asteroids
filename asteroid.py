# asteroid.py
#
# Defines the Asteroid class — the rocks floating around the screen.
#
# Asteroids come in three sizes (controlled by ASTEROID_KINDS in constants.py).
# When shot, a large asteroid splits into two smaller ones. Medium ones split into
# two small ones. Small ones just disappear.

import random

import pygame

from circleshape import CircleShape
from constants import ASTEROID_MIN_RADIUS, LINE_WIDTH
from logger import log_event


class Asteroid(CircleShape):
    def __init__(self, x, y, radius):
        super().__init__(x, y, radius)

    def draw(self, screen):
        # Draw the asteroid as a white circle outline. The radius varies by size tier,
        # so bigger asteroids look bigger on screen.
        pygame.draw.circle(screen, "white", self.position, self.radius, LINE_WIDTH)

    def update(self, dt):
        # Asteroids move in a straight line forever — no friction, no steering.
        # velocity is set at spawn time in AsteroidField.spawn() and never changes.
        self.position += self.velocity * dt

    def split(self):
        # Remove this asteroid from all sprite groups (kills it from the game world).
        self.kill()

        # If this is the smallest possible asteroid, don't spawn children.
        if self.radius <= ASTEROID_MIN_RADIUS:
            return

        log_event("asteroid_split")

        # Pick a random angle between 20–50 degrees to fan the two child asteroids apart.
        # Without this spread, both children would travel in the same direction and
        # immediately collide with the player again.
        angle = random.uniform(20, 50)

        # Rotate the current velocity by +angle for one child and -angle for the other.
        # This fans them outward in a V shape from the impact point.
        new_vector_pos = self.velocity.rotate(angle)
        new_vector_neg = self.velocity.rotate(angle - (angle * 2))  # same as -angle

        # Each child is one size tier smaller than its parent.
        new_radius = self.radius - ASTEROID_MIN_RADIUS

        # Spawn both children at the same position as the destroyed parent.
        new1 = Asteroid(self.position.x, self.position.y, new_radius)
        new2 = Asteroid(self.position.x, self.position.y, new_radius)

        # Speed up the children slightly (×1.2) to make the split feel energetic.
        new1.velocity = new_vector_pos * 1.2
        new2.velocity = new_vector_neg * 1.2
