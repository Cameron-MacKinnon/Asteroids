# shot.py
#
# Defines the Shot class — the bullets fired by the player.
#
# A shot is the simplest game object: it spawns at the ship's position, travels in
# a straight line in whatever direction the ship was facing, and never changes speed
# or direction on its own. Collision detection is handled in main.py.

import pygame

from circleshape import CircleShape
from constants import LINE_WIDTH, SHOT_RADIUS


class Shot(CircleShape):
    def __init__(self, x, y):
        super().__init__(x, y, SHOT_RADIUS)
        # rotation is stored but not used for movement (shots travel in a straight line).
        # It could be used in future for visual effects or angled projectiles.
        self.rotation = 0

    def draw(self, screen):
        # Draw the bullet as a small white circle outline.
        # Using the same LINE_WIDTH as other objects keeps the visual style consistent.
        pygame.draw.circle(screen, "white", self.position, self.radius, LINE_WIDTH)

    def update(self, dt):
        # Move the shot in a straight line each frame.
        # velocity was set at creation time in Player.shoot() and never changes,
        # so this just advances the position by velocity * dt (distance = speed × time).
        self.position += self.velocity * dt
