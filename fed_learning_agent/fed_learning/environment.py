# environment.py — GridWorld environment

import numpy as np
from config import (
    GRID_SIZE, GOAL_STATE, MAX_STEPS, REWARD_GOAL, REWARD_STEP
)

# Delta lookup for each action: 0=up, 1=down, 2=left, 3=right
_ACTION_DELTAS = [(-1, 0), (1, 0), (0, -1), (0, 1)]

# Precompute goal state index
_GOAL_INDEX = GOAL_STATE[0] * GRID_SIZE + GOAL_STATE[1]


class GridWorld:
    """
    8x8 grid. Agent navigates from a random start to the goal at GOAL_STATE.
    State is encoded as a single integer: row * GRID_SIZE + col  (0–63).
    """

    def __init__(self):
        self._current_state: int = 0
        self._step_count: int = 0

    # ------------------------------------------------------------------
    def reset(self) -> int:
        """Place agent at a random cell (never the goal). Return state."""
        self._step_count = 0
        # Draw random state until it is not the goal
        while True:
            row = np.random.randint(0, GRID_SIZE)
            col = np.random.randint(0, GRID_SIZE)
            state = row * GRID_SIZE + col
            if state != _GOAL_INDEX:
                break
        self._current_state = state
        return state

    # ------------------------------------------------------------------
    def step(self, action: int):
        """
        Apply action, enforce wall boundaries (clip), compute reward.

        Returns
        -------
        next_state : int
        reward     : float
        done       : bool
        """
        row, col = divmod(self._current_state, GRID_SIZE)
        dr, dc = _ACTION_DELTAS[action]

        # Clip to grid bounds (wall = stay in place)
        new_row = int(np.clip(row + dr, 0, GRID_SIZE - 1))
        new_col = int(np.clip(col + dc, 0, GRID_SIZE - 1))

        next_state = new_row * GRID_SIZE + new_col
        self._current_state = next_state
        self._step_count += 1

        if next_state == _GOAL_INDEX:
            return next_state, REWARD_GOAL, True

        done = self._step_count >= MAX_STEPS
        return next_state, REWARD_STEP, done
