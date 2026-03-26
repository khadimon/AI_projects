# server.py — Federated aggregation server

import numpy as np
from typing import List
from config import GRID_SIZE, NUM_ACTIONS, ANOMALY_THRESHOLD


class FederatedServer:
    """
    Central federation server.

    Receives Q-table updates from all agents, detects anomalies using
    cosine similarity, and aggregates using FedAvg (mean) or Median.
    Median aggregation is robust to sign-flip attacks.
    """

    def __init__(self):
        self.global_weights: np.ndarray = np.zeros(
            (GRID_SIZE * GRID_SIZE, NUM_ACTIONS)
        )
        self._last_anomalies: list = []

    # ------------------------------------------------------------------
    def get_global_weights(self) -> np.ndarray:
        """Return a copy of the current global Q-table."""
        return self.global_weights.copy()

    # ------------------------------------------------------------------
    def aggregate_fedavg(self, weights_list: List[np.ndarray]) -> np.ndarray:
        """
        Element-wise mean across all submitted Q-tables (FedAvg).
        Vulnerable to a sign-flip attack.
        """
        stacked = np.stack(weights_list, axis=0)   # (N, 64, 4)
        return np.mean(stacked, axis=0)             # (64, 4)

    # ------------------------------------------------------------------
    def aggregate_median(self, weights_list: List[np.ndarray]) -> np.ndarray:
        """
        Element-wise median across all submitted Q-tables.
        Robust to a single outlier (sign-flip) when N_honest > N_malicious.
        Used only for the final comparison; does NOT update server state.
        """
        stacked = np.stack(weights_list, axis=0)   # (N, 64, 4)
        return np.median(stacked, axis=0)           # (64, 4)

    # ------------------------------------------------------------------
    def detect_anomalies(self, weights_list: List[np.ndarray]) -> List[dict]:
        """
        Compare each agent's update to the population mean using cosine
        similarity. Flag any agent whose similarity falls below
        ANOMALY_THRESHOLD (a sign-flipped vector scores near -1.0).

        Returns
        -------
        list of dicts: [{"agent_id": int, "cosine_sim": float}, ...]
        Empty list if no anomalies detected.
        """
        stacked    = np.stack(weights_list, axis=0)  # (N, 64, 4)
        mean_flat  = np.mean(stacked, axis=0).flatten()
        norm_mean  = np.linalg.norm(mean_flat)

        anomalies = []
        for i, w in enumerate(weights_list):
            w_flat = w.flatten()
            norm_w = np.linalg.norm(w_flat)

            # Guard against zero vectors (early training, all-zero tables)
            if norm_w < 1e-10 or norm_mean < 1e-10:
                continue

            cosine_sim = float(np.dot(w_flat, mean_flat) / (norm_w * norm_mean))

            if cosine_sim < ANOMALY_THRESHOLD:
                anomalies.append({"agent_id": i, "cosine_sim": cosine_sim})

        self._last_anomalies = anomalies
        return anomalies

    # ------------------------------------------------------------------
    def update_global(self, new_weights: np.ndarray) -> None:
        """Store aggregated weights as the new global model."""
        self.global_weights = new_weights.copy()
