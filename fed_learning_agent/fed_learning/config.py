# config.py — single source of truth for all hyperparameters

# ── Grid World ─────────────────────────────────────────────────────────
GRID_SIZE         = 8          # 8x8 grid → 64 states
GOAL_STATE        = (7, 7)     # (row, col) of the terminal state
MAX_STEPS         = 100        # episode length limit
REWARD_GOAL       = 10.0       # reward on reaching goal
REWARD_STEP       = -0.1       # per-step living penalty

# ── Q-Learning ─────────────────────────────────────────────────────────
NUM_ACTIONS       = 4          # 0=up  1=down  2=left  3=right
ALPHA             = 0.1        # learning rate
GAMMA             = 0.99       # discount factor
EPSILON_START     = 1.0        # initial exploration rate
EPSILON_MIN       = 0.05       # floor for epsilon
EPSILON_DECAY     = 0.95       # multiplicative decay per round

# ── Federation ─────────────────────────────────────────────────────────
NUM_AGENTS        = 5          # total agents (indices 0–4)
MALICIOUS_IDS     = [4]        # which agent indices are malicious
NUM_ROUNDS        = 20         # number of federated rounds
LOCAL_EPISODES    = 10         # episodes each agent trains per round

# ── Anomaly Detection ──────────────────────────────────────────────────
ANOMALY_THRESHOLD = -0.5       # cosine similarity below this → flag

# ── Reproducibility ────────────────────────────────────────────────────
SEED              = 42
