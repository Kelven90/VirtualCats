# Global animation config for each species
# Format: species -> state -> (row, start_col, end_col, loop, frame_interval)

ANIMATION_CONFIGS = {
    "cat": {
        "sitting":      (0, 0, 6, False, 350),
        "standing":     (1, 0, 3, False, 200),
        "laying":       (2, 0, 1, False, 200),
        "sleeping":     (3, 0, 4, True, 700),
        "waking":       (4, 0, 10, False, 250),
        "running":      ((5, 0, 6), (6, 0, 12), True, 150),  # spans 2 rows
        "box_headup":   (7, 0, 12, True, 300),
        "box_cozy":     (8, 0, 10, True, 350),
        "box_head_downup": (9, 0, 12, True, 300),
        "praying_closed": (10, 0, 4, True, 400),
        "dancing":      (11, 0, 4, True, 250),
        "resting_lazy": (12, 0, 9, True, 400),
        "praying_open": (13, 0, 2, True, 400),
        "deep_sleep":   (14, 0, 4, True, 800),
        "collapse_open":(15, 0, 6, False, 300),
        "collapse_closed":(16, 0, 5, False, 300)
    },

    # Future expansion example for bunnies/dogs
    "bunny": {
        # "idle": (row, start, end, loop, interval)
    },

    "dog": {
        # "idle": (row, start, end, loop, interval)
    }
}
