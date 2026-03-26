# agent.py — Q-learning agent (honest and malicious variants)

import numpy as np
from config import (
    GRID_SIZE, NUM_ACTIONS, ALPHA, GAMMA,
    EPSILON_START, EPSILON_MIN, EPSILON_DECAY,
    LOCAL_EPISODES, MALICIOUS_IDS
)
from environment import GridWorld


class Agent:
    """
    A Q-learning agent that trains on a local GridWorld.

    Honest agents send their true Q-table to the federation server.
    Malicious agents send the negated Q-table (sign-flip attack),
    which pushes the global model toward bad policies.
    """

    def __init__(self, agent_id: int, is_malicious: bool = False):
        self.agent_id     = agent_id
        self.is_malicious = is_malicious
        self.epsilon      = EPSILON_START
        self.q_table      = np.zeros((GRID_SIZE * GRID_SIZE, NUM_ACTIONS))
        self._env         = GridWorld()

    # ------------------------------------------------------------------
    def select_action(self, state: int) -> int:
        """Epsilon-greedy action selection."""
        if np.random.random() < self.epsilon:
            return np.random.randint(NUM_ACTIONS)
        return int(np.argmax(self.q_table[state]))

    # ------------------------------------------------------------------
    def train_episode(self) -> float:
        """
        Run one full episode using Q-learning updates.
        Returns total undiscounted reward for the episode.
        """
        state = self._env.reset()
        total_reward = 0.0

        while True:
            action = self.select_action(state)
            next_state, reward, done = self._env.step(action)

            # Q-learning TD update
            # Mask out future value when episode terminates at goal
            best_next = float(np.max(self.q_table[next_state]))
            td_target = reward + GAMMA * best_next * (1 - int(done))
            td_error  = td_target - self.q_table[state, action]
            self.q_table[state, action] += ALPHA * td_error

            total_reward += reward
            state = next_state

            if done:
                break

        return total_reward

    # ------------------------------------------------------------------
    def train_local(self, num_episodes: int = LOCAL_EPISODES) -> float:
        """Train for num_episodes and return mean reward."""
        rewards = [self.train_episode() for _ in range(num_episodes)]
        return float(np.mean(rewards))

    # ------------------------------------------------------------------
    def get_weights(self) -> np.ndarray:
        """
        Return this agent's Q-table for upload to the server.

        Honest  → true Q-table copy
        Malicious → sign-flipped Q-table copy (attack)
        """
        if self.is_malicious:
            return -self.q_table.copy()
        return self.q_table.copy()

    # ------------------------------------------------------------------
    def set_weights(self, global_weights: np.ndarray) -> None:
        """Overwrite local Q-table with global weights from server."""
        self.q_table = global_weights.copy()

    # ------------------------------------------------------------------
    def decay_epsilon(self) -> None:
        """Reduce exploration rate after each federated round."""
        self.epsilon = max(EPSILON_MIN, self.epsilon * EPSILON_DECAY)
