# main.py — Federated Learning simulation entry point

import numpy as np
from config import (
    SEED, NUM_AGENTS, MALICIOUS_IDS, NUM_ROUNDS, LOCAL_EPISODES,
    GRID_SIZE, NUM_ACTIONS
)
from agent import Agent
from server import FederatedServer
from environment import GridWorld

WIDTH = 52  # terminal output width


# ── Helpers ────────────────────────────────────────────────────────────

def sep(char: str = "=") -> None:
    print(char * WIDTH)


def print_header() -> None:
    sep()
    print(" FEDERATED LEARNING - MULTI-AGENT DECISION SYSTEM")
    print(f" {NUM_AGENTS} agents  |  {GRID_SIZE}x{GRID_SIZE} GridWorld  |  "
          f"{NUM_ROUNDS} rounds  |  Q-Learning")
    sep()
    print()


def print_round_header(round_num: int) -> None:
    print()
    sep()
    print(f" ROUND {round_num}/{NUM_ROUNDS}")
    sep()


def evaluate_weights(
    weights: np.ndarray,
    num_episodes: int = 300,
    eval_eps: float = 0.02,
) -> float:
    """
    Near-greedy rollout using a fixed Q-table.
    eval_eps = 0.02 adds minimal exploration to prevent cycles
    when Q-values are near-zero. Returns mean episode reward.
    """
    env = GridWorld()
    total = 0.0
    for _ in range(num_episodes):
        state = env.reset()
        ep_reward = 0.0
        while True:
            if np.random.random() < eval_eps:
                action = np.random.randint(NUM_ACTIONS)
            else:
                action = int(np.argmax(weights[state]))
            state, reward, done = env.step(action)
            ep_reward += reward
            if done:
                break
        total += ep_reward
    return total / num_episodes


# ── Verbose training (FedAvg + malicious) ──────────────────────────────

def run_verbose_training(seed: int) -> dict:
    """
    Full verbose training with FedAvg and malicious agent.
    Prints all round details and anomaly detections.
    Returns metrics dict.
    """
    np.random.seed(seed)
    agents = [
        Agent(agent_id=i, is_malicious=(i in MALICIOUS_IDS))
        for i in range(NUM_AGENTS)
    ]
    server = FederatedServer()

    metrics = {
        "round_honest_rewards": [],
        "anomaly_rounds": [],
        "final_weights": None,
    }

    for round_num in range(1, NUM_ROUNDS + 1):
        print_round_header(round_num)

        global_w = server.get_global_weights()
        for agent in agents:
            agent.set_weights(global_w)

        round_rewards = []
        for agent in agents:
            avg_r = agent.train_local(LOCAL_EPISODES)
            round_rewards.append(avg_r)

            label     = "MALICIOUS" if agent.is_malicious else "honest   "
            indicator = "  [SIGN-FLIP ACTIVE]" if agent.is_malicious else ""
            print(f"  [Agent {agent.agent_id}] {label} | "
                  f"avg_reward: {avg_r:7.2f} | "
                  f"eps={agent.epsilon:.2f}"
                  f"{indicator}")

        weights_list = [agent.get_weights() for agent in agents]

        anomalies = server.detect_anomalies(weights_list)
        if anomalies:
            for a in anomalies:
                print(f"  *** ANOMALY DETECTED: Agent {a['agent_id']} "
                      f"(cosine_sim={a['cosine_sim']:.4f}) ***")
            metrics["anomaly_rounds"].append(round_num)
        else:
            print("  [OK] No anomalies detected this round.")

        new_global = server.aggregate_fedavg(weights_list)
        server.update_global(new_global)
        print("  FedAvg applied -> global model updated")

        for agent in agents:
            agent.decay_epsilon()

        honest_rewards = [
            round_rewards[i] for i in range(NUM_AGENTS)
            if i not in MALICIOUS_IDS
        ]
        mean_honest = float(np.mean(honest_rewards))
        metrics["round_honest_rewards"].append(mean_honest)
        print(f"  Mean honest reward this round: {mean_honest:.2f}")

    metrics["final_weights"] = server.get_global_weights()
    return metrics


# ── Quiet experiment runner ─────────────────────────────────────────────

def run_quiet_experiment(
    seed: int,
    use_median: bool = False,
    include_malicious: bool = True,
) -> tuple:
    """
    Run a full training experiment silently.
    Returns (round_honest_rewards, final_server_weights).
    """
    np.random.seed(seed)

    agents = [
        Agent(
            agent_id=i,
            is_malicious=(i in MALICIOUS_IDS and include_malicious),
        )
        for i in range(NUM_AGENTS)
    ]
    server = FederatedServer()
    round_rewards = []

    for _ in range(NUM_ROUNDS):
        global_w = server.get_global_weights()
        for agent in agents:
            agent.set_weights(global_w)

        honest_r = []
        weights_list = []
        for agent in agents:
            avg_r = agent.train_local(LOCAL_EPISODES)
            if not agent.is_malicious:
                honest_r.append(avg_r)
            weights_list.append(agent.get_weights())

        if use_median:
            new_global = server.aggregate_median(weights_list)
        else:
            new_global = server.aggregate_fedavg(weights_list)
        server.update_global(new_global)

        for agent in agents:
            agent.decay_epsilon()

        round_rewards.append(float(np.mean(honest_r)))

    return round_rewards, server.get_global_weights()


# ── Final comparison ───────────────────────────────────────────────────

def run_comparison(verbose_metrics: dict) -> None:
    print()
    sep()
    print(" FINAL COMPARISON: 3 Independent Experiments")
    sep()
    print()
    print("  Running three full training runs (silent)...")
    print("    [1] FedAvg    + malicious agent (sign-flip attack)")
    print("    [2] Median    + malicious agent (Byzantine-robust)")
    print("    [3] FedAvg    + honest agents only (oracle baseline)")
    print()

    # Use offset seeds so each experiment has different randomness
    _, fedavg_w = run_quiet_experiment(SEED + 10, use_median=False, include_malicious=True)
    _, median_w = run_quiet_experiment(SEED + 10, use_median=True,  include_malicious=True)
    _, honest_w = run_quiet_experiment(SEED + 10, use_median=False, include_malicious=False)

    # Evaluate final deployed policy from each experiment
    np.random.seed(SEED + 99)
    fedavg_score  = evaluate_weights(fedavg_w)
    np.random.seed(SEED + 99)
    median_score  = evaluate_weights(median_w)
    np.random.seed(SEED + 99)
    honest_score  = evaluate_weights(honest_w)

    # Results table
    col1 = 30
    col2 = 22
    row_sep = "-" * (col1 + col2 + 3)

    print(f"  {'Experiment':<{col1}} {'Avg Reward (300 eps)':>{col2}}")
    print(f"  {row_sep}")
    print(f"  {'[1] FedAvg  (vulnerable)':<{col1}} {fedavg_score:>{col2}.2f}")
    print(f"  {'[2] Median  (defended)':<{col1}} {median_score:>{col2}.2f}")
    print(f"  {'[3] Honest-only baseline':<{col1}} {honest_score:>{col2}.2f}")
    print()

    # Interpret results
    if median_score > fedavg_score:
        gap = median_score - fedavg_score
        print(f"  Median aggregation outperforms FedAvg by {gap:.2f} reward.")
        print("  Byzantine-robust defense reduces attack impact.")
    else:
        print("  Note: With only 1 malicious agent out of 5 (20%), FedAvg")
        print("  is partially resilient. The effect is clearest in early rounds.")

    # Anomaly detection summary from verbose run
    total_flagged = len(verbose_metrics["anomaly_rounds"])
    print()
    print("  Anomaly Detection Summary (Experiment 1):")
    print(f"  - Rounds with detected anomaly: {total_flagged}/{NUM_ROUNDS}")
    if verbose_metrics["anomaly_rounds"]:
        print(f"  - Agent(s) {MALICIOUS_IDS} flagged in rounds: "
              f"{verbose_metrics['anomaly_rounds']}")

    print()
    sep()
    print(" Training complete.")
    sep()


# ── Entry point ────────────────────────────────────────────────────────

def main() -> None:
    print_header()
    verbose_metrics = run_verbose_training(SEED)
    run_comparison(verbose_metrics)


if __name__ == "__main__":
    main()
