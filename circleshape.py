# circleshape.py
#
# Defines the base class that all moving game objects (player, asteroids, shots) inherit from.
#
# WHY A BASE CLASS?
# Every object in this game shares the same fundamental idea: it lives at a position
# on screen, it may be moving (velocity), and it has a size (radius). Rather than
# copy-pasting those properties into every class, we define them once here and let
# subclasses inherit them for free.
#
# WHY CIRCLE-BASED?
# Using circles for collision detection is the simplest and cheapest approach.
# Two circles overlap when the distance between their centers is less than the
# sum of their radii. That's one distance calculation — no rotation math needed.

import pygame


# CircleShape extends pygame's built-in Sprite class.
# pygame.sprite.Sprite gives us group membership for free — when an object is
# added to a sprite Group, pygame can update and draw all of them with one call.
class CircleShape(pygame.sprite.Sprite):
    def __init__(self, x, y, radius):
        # Check if the subclass set a `containers` attribute before calling super().__init__.
        # `containers` is a pygame convention: if you assign a Group (or tuple of Groups)
        # to a class-level `containers` variable, any new instance is automatically added
        # to those groups at creation time — no manual .add() needed.
        if hasattr(self, "containers"):
            super().__init__(self.containers)
        else:
            super().__init__()

        # pygame.Vector2 is a 2D vector helper. It stores (x, y) and provides
        # convenient math like addition, scaling, rotation, and distance — all
        # the things we need for movement and collision.
        self.position = pygame.Vector2(x, y)
        self.velocity = pygame.Vector2(0, 0)  # Starts stationary; subclasses set this
        self.radius = radius

    def draw(self, screen):
        # Subclasses MUST override this. There is no generic way to draw a "circle shape"
        # because players look like triangles and asteroids look like circles.
        pass

    def update(self, dt):
        # Subclasses MUST override this. `dt` is "delta time" — the number of seconds
        # since the last frame. Multiplying movement by dt makes the game speed
        # frame-rate independent: the ship moves at the same real-world speed whether
        # the game runs at 30 FPS or 120 FPS.
        pass

    def collides_with(self, other):
        # Circle-circle collision check.
        # If the straight-line distance between the two center points is less than
        # the sum of their radii, the circles are overlapping.
        combined_radius = self.radius + other.radius
        if self.position.distance_to(other.position) < combined_radius:
            return True
        return False
