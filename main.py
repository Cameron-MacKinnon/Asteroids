# main.py
#
# Entry point for the game. This file is responsible for:
#   1. Initializing pygame and creating the window
#   2. Setting up all game objects and sprite groups
#   3. Running the game loop — the heartbeat that drives everything
#   4. Handling collision detection between objects
#   5. Handling the quit event and game-over state
#
# The game loop pattern used here is the standard pygame structure:
#   - Process input/events
#   - Update game state
#   - Render everything
#   - Wait for the next frame

import sys
from turtle import up

import pygame

from asteroid import Asteroid
from asteroidfield import AsteroidField
from constants import SCREEN_HEIGHT, SCREEN_WIDTH
from logger import log_event, log_state
from player import Player
from shot import Shot


def main():
    # welcome
    print(f"Starting Asteroids with Pygame version {pygame.version.ver}")
    print(f"Screen width: {SCREEN_WIDTH}")
    print(f"Screen height: {SCREEN_HEIGHT}")

    # Initialize pygame's internal systems (display, events, clock, etc.)
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

    # --- Sprite Groups ---
    # Sprite groups are pygame's way of managing collections of objects.
    #
    # `updatable`: every object whose state changes each frame (moves, fires timers, etc.)
    # `drawable`:  every object that needs to be rendered to the screen
    # `asteroids`: only asteroids — used to iterate specifically for collision checks
    # `shots`:     only bullets — used to iterate specifically for collision checks
    #
    # An object can belong to multiple groups at once (e.g. Asteroid is in
    # updatable, drawable, AND asteroids).
    updatable = pygame.sprite.Group()
    drawable = pygame.sprite.Group()
    asteroids = pygame.sprite.Group()
    shots = pygame.sprite.Group()

    # --- Wire up containers ---
    # Setting `containers` on a class before instantiating it causes every new
    # instance of that class to auto-register with those groups at creation time.
    # This means we never manually call group.add() — objects join the right groups
    # just by being created (e.g. when AsteroidField spawns a new asteroid in split()).
    Player.containers = (updatable, drawable)
    Asteroid.containers = (asteroids, updatable, drawable)
    AsteroidField.containers = (
        updatable  # The field manager has no visual, so no drawable
    )
    Shot.containers = (shots, drawable, updatable)

    # Create the asteroid field manager. It has no visual but its update() fires
    # the spawn timer each frame, creating new Asteroid objects on a schedule.
    asteroid_field = AsteroidField()

    # Create the player ship in the center of the screen.
    player = Player(x=SCREEN_WIDTH / 2, y=SCREEN_HEIGHT / 2)

    # --- Clock ---
    # pygame.time.Clock caps the frame rate and measures delta time.
    clock = pygame.time.Clock()
    dt = 0  # Delta time in seconds; 0 on the very first frame

    # --- Game Loop ---
    # This loop runs once per frame until the game ends.
    while True:
        # Call the boot.dev logger once per second for assessment purposes.
        log_state()

        # Process OS/window events. Without draining this queue, the window
        # becomes unresponsive (the OS thinks the app has frozen).
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return

        # Clear the screen to black before drawing the new frame.
        # Without this, each frame paints on top of the last — leaving ghost trails.
        screen.fill("black")

        # Update all game objects: player input, asteroid movement, spawn timers, etc.
        updatable.update(dt)

        # --- Collision: asteroid vs player ---
        # If any asteroid overlaps the player's hitbox circle, it's game over.
        for a in asteroids:
            if a.collides_with(player):
                log_event("player_hit")
                print("Game over!")
                sys.exit()

        # --- Collision: asteroid vs shots ---
        # Check every bullet against every asteroid.
        # If they overlap, destroy the bullet and split the asteroid.
        for a in asteroids:
            for projectile in shots:
                if a.collides_with(projectile):
                    log_event("asteroid_shot")
                    a.split()
                    projectile.kill()

        # Draw all drawable objects onto the screen surface.
        for unit in drawable:
            unit.draw(screen)

        # Flip the display buffer — makes everything drawn above actually visible.
        # pygame uses double-buffering: draw to a hidden back buffer, then flip to show it.
        # This prevents flickering that would happen if we drew directly to the visible screen.
        pygame.display.flip()

        # Cap the frame rate at 60 FPS and capture delta time.
        # clock.tick(60) blocks until it's time for the next frame, then returns
        # the milliseconds since last call. Dividing by 1000 converts to seconds.
        dt = clock.tick(60) / 1000


if __name__ == "__main__":
    main()
