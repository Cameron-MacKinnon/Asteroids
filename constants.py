# constants.py
#
# This file is the single source of truth for all "magic numbers" in the game.
# Instead of scattering raw numbers (like 1280 or 300) throughout the codebase,
# we name them here. That way, if you want to tweak the game feel — e.g. make the
# player turn faster or asteroids spawn more often — there's one obvious place to look.

# --- Screen ---
SCREEN_WIDTH = 1280   # Width of the game window in pixels
SCREEN_HEIGHT = 720   # Height of the game window in pixels

# --- Drawing ---
# pygame.draw functions accept a "width" argument for the thickness of outlines.
# 0 means "fill the shape solid". A small value like 2 gives a thin wireframe look,
# which is the classic Asteroids aesthetic.
LINE_WIDTH = 2

# --- Player ---
PLAYER_RADIUS = 20       # The player ship fits inside a circle of this radius (pixels)
PLAYER_TURN_SPEED = 300  # Degrees per second the ship rotates when A/D is held
PLAYER_SPEED = 200       # Pixels per second the ship moves forward when W is held
PLAYER_SHOOT_SPEED = 500 # Pixels per second a bullet travels after being fired
PLAYER_SHOOT_COOLDOWN_SECONDS = 0.3  # Seconds the player must wait between shots

# --- Shots ---
SHOT_RADIUS = 5  # Radius of the bullet circle in pixels

# --- Asteroids ---
ASTEROID_MIN_RADIUS = 20   # Smallest an asteroid can be; below this it doesn't split further
ASTEROID_KINDS = 3         # How many size tiers exist (1×min, 2×min, 3×min radius)
ASTEROID_SPAWN_RATE_SECONDS = 0.8  # A new asteroid spawns from a screen edge every this many seconds
ASTEROID_MAX_RADIUS = ASTEROID_MIN_RADIUS * ASTEROID_KINDS  # Largest possible asteroid radius
