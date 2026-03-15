# player.py
#
# Defines the Player class — the ship the user flies around the screen.
#
# The ship is drawn as a triangle. Three corner points are recalculated every frame
# based on the ship's current position and rotation angle, so the triangle always
# points in the direction the ship is "facing".

import pygame

import shot
from circleshape import CircleShape
from constants import (
    LINE_WIDTH,
    PLAYER_RADIUS,
    PLAYER_SHOOT_COOLDOWN_SECONDS,
    PLAYER_SHOOT_SPEED,
    PLAYER_SPEED,
    PLAYER_TURN_SPEED,
)
from shot import Shot


class Player(CircleShape):
    def __init__(self, x, y):
        super().__init__(x, y, PLAYER_RADIUS)
        # rotation tracks which direction the nose of the ship is pointing,
        # measured in degrees. 0° = pointing down (pygame's +Y axis points downward).
        self.rotation = 0
        # cooldown_timer counts down between shots. When it drops to 0 or below,
        # the player is allowed to fire again. Starts negative so first shot is instant.
        self.cooldown_timer = 0

    def triangle(self):
        # Calculate the three corner points of the ship triangle.
        #
        # "forward" is a unit vector pointing in the direction the ship faces.
        # We start with (0, 1) — straight down — and rotate it by self.rotation degrees.
        # pygame.Vector2.rotate() rotates counter-clockwise for positive angles.
        forward = pygame.Vector2(0, 1).rotate(self.rotation)

        # "right" is perpendicular to forward, scaled to 2/3 of the ship's radius.
        # This sets the width of the ship's base. Rotating forward by +90° gives the
        # rightward direction relative to the ship.
        right = pygame.Vector2(0, 1).rotate(self.rotation + 90) * self.radius / 1.5

        # Point A: the nose of the ship, one full radius ahead of center
        a = self.position + forward * self.radius

        # Points B and C: the two base corners, one radius behind center,
        # spread left and right by the `right` vector
        b = self.position - forward * self.radius - right
        c = self.position - forward * self.radius + right

        return [a, b, c]

    def draw(self, screen):
        # Draw the ship as a white outlined polygon (no fill — wireframe style).
        # LINE_WIDTH controls how thick the outline strokes are.
        pygame.draw.polygon(screen, "white", self.triangle(), LINE_WIDTH)

    def rotate(self, dt):
        # Increment the rotation angle. PLAYER_TURN_SPEED is in degrees/second,
        # so multiplying by dt gives the correct number of degrees for this frame.
        # Passing a negative dt (from the A key) reverses the direction.
        self.rotation += PLAYER_TURN_SPEED * dt

    def update(self, dt):
        keys = pygame.key.get_pressed()

        # move
        if keys[pygame.K_w]:
            self.move(dt)
        if keys[pygame.K_s]:
            # dt - (2 * dt) = -dt, so this moves backward (reverse thrust)
            self.move(dt - (2 * dt))
        if keys[pygame.K_a]:
            # dt - (2 * dt) = -dt, so this rotates in the negative direction
            self.rotate(dt - (2 * dt))
        if keys[pygame.K_d]:
            self.rotate(dt)

        # shoot
        if keys[pygame.K_SPACE]:
            self.shoot()

        # Tick the cooldown timer down each frame so the player can eventually fire again.
        # It goes negative, which is fine — shoot() just checks if it's > 0.
        self.cooldown_timer -= dt

    def move(self, dt):
        # Build a direction vector pointing the way the ship is currently facing,
        # scale it by PLAYER_SPEED (pixels/second), then multiply by dt to get the
        # distance to travel this frame. Add it to position to move the ship.
        unit_vector = pygame.Vector2(0, 1)
        rotated_vector = unit_vector.rotate(self.rotation)
        rotated_with_speed_vector = rotated_vector * PLAYER_SPEED * dt
        self.position += rotated_with_speed_vector

    def shoot(self):
        # Don't fire if the cooldown hasn't expired yet.
        if self.cooldown_timer > 0:
            return

        # Reset the timer so the player must wait before shooting again.
        self.cooldown_timer = PLAYER_SHOOT_COOLDOWN_SECONDS

        # Spawn a bullet at the ship's current position. Give it a velocity that
        # points in the same direction the ship is facing, scaled by PLAYER_SHOOT_SPEED.
        shot = Shot(self.position.x, self.position.y)
        shot_vector = pygame.Vector2(0, 1)
        rotated_vector = shot_vector.rotate(self.rotation)
        rotated_with_speed_vector = rotated_vector * PLAYER_SHOOT_SPEED
        shot.velocity = rotated_with_speed_vector
