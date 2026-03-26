# Federated Learning for Multi-Agent Decision Systems

A beginner-friendly project simulating 5 independent agents in a GridWorld environment, practicing federated learning with a simple FedAvg aggregator, plus a malicious agent scenario and defense discussion.

## Goals
- Each agent trains locally with its own environment.
- Periodic model aggregation by a central server (FedAvg).
- Malicious agent sends bad updates; server applies basic defense.
- Evaluate reward trend and success rate.

## Requirements
- Python 3.8+
- PyTorch
- NumPy

## Usage
1. Create Python environment:
```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```
2. Run training:
```bash
python fed_learning/main.py
```

## Outputs
- Per-round training reward trends
- Evaluation success rates
- Malicious effect and defense report

## Notes
- This is a simple prototype. For production, use robust secure aggregation (FedShare, Krum, Trimmed mean, etc.).
