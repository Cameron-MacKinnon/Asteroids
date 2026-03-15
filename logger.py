# logger.py
#
# Diagnostic logging utilities used by the boot.dev CLI tool to assess game state.
#
# Two log files are produced (in the project root):
#   game_state.jsonl  — a snapshot of all game objects, taken once per second
#   game_events.jsonl — a record of discrete events (e.g. "asteroid_split", "player_hit")
#
# Both use JSON Lines format (.jsonl): one JSON object per line, making the file
# easy to stream, append to, and parse without loading the whole file into memory.
#
# Logging stops automatically after _MAX_SECONDS seconds so the files don't grow forever.

import inspect
import json
import math
from datetime import datetime

__all__ = ["log_state", "log_event"]

_FPS = 60          # Assumed frame rate, used to convert frame count to seconds
_MAX_SECONDS = 16  # Stop logging after this many real-world seconds
_SPRITE_SAMPLE_LIMIT = 10  # Cap how many sprites we log per group (avoids huge files)

# Module-level state — these persist across calls within the same run.
_frame_count = 0
_state_log_initialized = False   # True after the first state log write (switches mode to append)
_event_log_initialized = False   # Same, for the event log
_start_time = datetime.now()     # Recorded at import time; used to calculate elapsed seconds


def log_state():
    global _frame_count, _state_log_initialized

    # Stop logging after _MAX_SECONDS to avoid unbounded file growth.
    if _frame_count > _FPS * _MAX_SECONDS:
        return

    # Increment the frame counter every call. log_state() is called once per frame,
    # so _frame_count is a rough proxy for "how many frames have elapsed".
    _frame_count += 1

    # Only write a snapshot once per second (every _FPS frames), not every frame.
    # _frame_count % _FPS == 0 is true exactly once every 60 frames.
    if _frame_count % _FPS != 0:
        return

    now = datetime.now()

    # --- Inspect the caller's local variables ---
    # inspect.currentframe() returns this function's stack frame.
    # frame.f_back is the caller's frame (i.e. main()'s local variables).
    # This lets us introspect the game state without requiring the caller to
    # explicitly pass anything — the logger "reaches up" into the call stack.
    frame = inspect.currentframe()
    if frame is None:
        return

    frame_back = frame.f_back
    if frame_back is None:
        return

    # Copy the caller's local variables into a dict we can safely iterate.
    local_vars = frame_back.f_locals.copy()

    screen_size = []
    game_state = {}

    for key, value in local_vars.items():
        # Detect the pygame Surface (the screen object) by checking for get_size().
        if "pygame" in str(type(value)) and hasattr(value, "get_size"):
            screen_size = value.get_size()

        # Detect sprite Groups by class name. Log the first _SPRITE_SAMPLE_LIMIT sprites.
        if hasattr(value, "__class__") and "Group" in value.__class__.__name__:
            sprites_data = []

            for i, sprite in enumerate(value):
                if i >= _SPRITE_SAMPLE_LIMIT:
                    break

                # Collect whichever properties the sprite exposes.
                sprite_info = {"type": sprite.__class__.__name__}

                if hasattr(sprite, "position"):
                    sprite_info["pos"] = [
                        round(sprite.position.x, 2),
                        round(sprite.position.y, 2),
                    ]

                if hasattr(sprite, "velocity"):
                    sprite_info["vel"] = [
                        round(sprite.velocity.x, 2),
                        round(sprite.velocity.y, 2),
                    ]

                if hasattr(sprite, "radius"):
                    sprite_info["rad"] = sprite.radius

                if hasattr(sprite, "rotation"):
                    sprite_info["rot"] = round(sprite.rotation, 2)

                sprites_data.append(sprite_info)

            game_state[key] = {"count": len(value), "sprites": sprites_data}

        # Fallback: if we haven't found any groups yet, log any lone sprite objects
        # (like the Player instance) directly.
        if len(game_state) == 0 and hasattr(value, "position"):
            sprite_info = {"type": value.__class__.__name__}

            sprite_info["pos"] = [
                round(value.position.x, 2),
                round(value.position.y, 2),
            ]

            if hasattr(value, "velocity"):
                sprite_info["vel"] = [
                    round(value.velocity.x, 2),
                    round(value.velocity.y, 2),
                ]

            if hasattr(value, "radius"):
                sprite_info["rad"] = value.radius

            if hasattr(value, "rotation"):
                sprite_info["rot"] = round(value.rotation, 2)

            game_state[key] = sprite_info

    # Build the final log entry. The ** operator unpacks game_state as top-level keys.
    entry = {
        "timestamp": now.strftime("%H:%M:%S.%f")[:-3],  # HH:MM:SS.mmm
        "elapsed_s": math.floor((now - _start_time).total_seconds()),
        "frame": _frame_count,
        "screen_size": screen_size,
        **game_state,
    }

    # On the first write, open in "w" (overwrite) to start a fresh log for this run.
    # On subsequent writes, open in "a" (append) to keep growing the same file.
    mode = "w" if not _state_log_initialized else "a"
    with open("game_state.jsonl", mode) as f:
        f.write(json.dumps(entry) + "\n")

    _state_log_initialized = True


def log_event(event_type, **details):
    # Log a discrete game event immediately (not on a timer like log_state).
    # Callers pass an event_type string and any extra key-value details they want recorded.
    # Example: log_event("asteroid_shot", asteroid_radius=40)
    global _event_log_initialized

    now = datetime.now()

    event = {
        "timestamp": now.strftime("%H:%M:%S.%f")[:-3],
        "elapsed_s": math.floor((now - _start_time).total_seconds()),
        "frame": _frame_count,
        "type": event_type,
        **details,  # Any extra kwargs (e.g. position, radius) get merged in here
    }

    mode = "w" if not _event_log_initialized else "a"
    with open("game_events.jsonl", mode) as f:
        f.write(json.dumps(event) + "\n")

    _event_log_initialized = True
