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

    # init pygame
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

    # init groups/objects
    updatable = pygame.sprite.Group()
    drawable = pygame.sprite.Group()
    asteroids = pygame.sprite.Group()
    shots = pygame.sprite.Group()
    Player.containers = (updatable, drawable)
    Asteroid.containers = (asteroids, updatable, drawable)
    AsteroidField.containers = updatable
    Shot.containers = (shots, drawable, updatable)
    asteroid_field = AsteroidField()
    player = Player(x=SCREEN_WIDTH / 2, y=SCREEN_HEIGHT / 2)

    # start clock and init time delta for FPS
    clock = pygame.time.Clock()
    dt = 0

    # start game loop
    while True:
        # call logger for bootdotdev cli tool assessment
        log_state()

        # listen for window closure
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return

        # colour screen black
        screen.fill("black")

        # update object states
        updatable.update(dt)

        # check for asteroid collisions
        for a in asteroids:
            if a.collides_with(player):
                log_event("player_hit")
                print("Game over!")
                sys.exit()

        # check for asteroid hits!
        for a in asteroids:
            for projectile in shots:
                if a.collides_with(projectile):
                    log_event("asteroid_shot")
                    a.split()
                    projectile.kill()

        # render results
        for unit in drawable:
            unit.draw(screen)

        # make changes visible
        pygame.display.flip()

        # cap framerate at 60fps
        dt = clock.tick(60) / 1000


if __name__ == "__main__":
    main()
