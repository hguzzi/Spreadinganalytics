# Spreadinganalytics

### XAI-Guided GNN Framework for Ebola Epidemic Intervention Design

[![License: MIT](https://img.shields.io/badge/code-MIT-blue.svg)](https://opensource.org/licenses/MIT)
[![License: CC BY 4.0](https://img.shields.io/badge/data-CC%20BY%204.0-green.svg)](https://creativecommons.org/licenses/by/4.0/)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![CI](https://github.com/hguzzi/Spreadinganalytics/actions/workflows/ci.yml/badge.svg)](https://github.com/hguzzi/Spreadinganalytics/actions/workflows/ci.yml)

A graph neural network (GNN) framework with explainable AI (XAI) for designing targeted Ebola virus disease (EVD) interventions. The framework uses Integrated Gradients attribution to guide vaccination, edge removal, and isolation strategies on contact networks, evaluated across three feasibility pillars: **performance advantage**, **robustness**, and **actionability**.

> **Companion paper**: Guzzi, P.H. (2026). *Feasibility of explainable AI-guided intervention design for Ebola virus disease outbreaks: a graph neural network framework with sensitivity and adaptive analysis.* [DOI: to be added]

---

## Quickstart

```bash
# Clone
git clone https://github.com/hguzzi/Spreadinganalytics.git
cd Spreadinganalytics

# Install dependencies
pip install -r requirements.txt

# Run a baseline simulation
python -c "
from src.ebola_sim_module import load_network, build_seihrd_params, run_simulation

graph = load_network('BA', N=1000)
params = build_seihrd_params(R0=2.51, f=0.33, avg_degree=5.96)
metrics, history = run_simulation(graph, params, I0=3, n_steps=100, seed=42)
print(f'Total deaths: {metrics[\"total_deaths\"]}')
"
```

---

## Repository Structure

```
Spreadinganalytics/
├── config.py                       # Central path configuration (auto-resolves relative to repo root)
├── src/
│   └── ebola_sim_module.py         # Main module: SEIHRD simulation, GNN, XAI, interventions
├── models/
│   ├── 01_seird_ode/               # ODE compartmental models
│   │   ├── seird_ode_model.py
│   │   ├── seihrd_ode_model.py
│   │   └── parameter_calibration.py
│   └── 02_network_simulation/      # Network-based stochastic simulation engines
│       ├── seird_network_sim.py
│       └── seihrd_network_sim.py
├── data/                           # All simulation data and XAI attributions
│   ├── calibrated_params.json
│   ├── networks/                   # 13 contact network edgelists + metrics
│   ├── simulation_results/         # 21 result CSVs (dose-response, sensitivity, scaling, etc.)
│   ├── supplementary/              # 10 supplementary analysis CSVs + table CSVs
│   └── xai_attributions/           # 5 PKL files (IG/Saliency node & edge scores)
├── notebooks/                      # 4 Jupyter notebooks (full computational trace)
├── requirements.txt
├── CITATION.cff
├── LICENSE
└── .github/workflows/ci.yml        # CI: import verification
```

---

## Key Parameters

All simulations use Bundibugyo-specific parameters calibrated to the 2026 DRC/Uganda outbreak:

| Parameter | Value | Description |
|-----------|-------|-------------|
| R₀ | 2.51 | Basic reproduction number (95% CI: 2.27–2.82) |
| CFR | 0.33 | Case fatality ratio (95% CI: 0.26–0.40) |
| σ | 1/8.5 | Exposed-to-infectious rate (mean incubation 8.5 days) |
| α | 1/3.0 | Hospitalization rate (mean 3 days) |
| avg degree | 5.96 | Mean network degree (calibrated from BA N=500) |

R₀ decomposition: community = 1.537, hospital = 0.574, funeral = 0.399.

---

## Network Architectures

Five contact network topologies at three population scales (N = 500, 1,000, 5,000):

| Network | Type | Key Property |
|---------|------|--------------|
| BA | Barabási-Albert | Scale-free, degree heterogeneity, superspreaders |
| WS | Watts-Strogatz | Small-world, high clustering |
| RG | Random Geometric | Spatial proximity, high clustering |
| SBM | Stochastic Block Model | Community structure |
| Synthpops | Synthetic Populations | Realistic age/layer mixing |

---

## Interventions

Six intervention strategies evaluated across coverage levels (vaccination 10–70%, edge removal 10–90%, isolation 30–90%):

| Strategy | Description |
|----------|-------------|
| IG-guided vaccination | Vaccinate top-ranked nodes by Integrated Gradients attribution |
| IG-guided edge removal | Remove top-ranked edges by IG attribution (structural intervention) |
| IG-guided isolation | Isolate top-ranked infectious nodes by IG attribution |
| Betweenness vaccination | Vaccinate highest-betweenness nodes |
| Random vaccination | Randomly vaccinate a fraction of the population |
| Standard isolation | Isolate a random fraction of infectious nodes |

---

## Usage Examples

### Load and simulate on a network

```python
from src.ebola_sim_module import load_network, build_seihrd_params, run_simulation

graph = load_network("BA", N=1000)
params = build_seihrd_params(R0=2.51, f=0.33, avg_degree=5.96)
metrics, history = run_simulation(graph, params, I0=3, n_steps=100, seed=42)
print(f"Total deaths: {metrics['total_deaths']}, Attack rate: {metrics['attack_rate_pct']:.1f}%")
```

### Load XAI attributions

```python
import pickle

with open("data/xai_attributions/xai_attributions_N1000.pkl", "rb") as f:
    attributions = pickle.load(f)

ig_node_scores = attributions["BA"]["ig_node_scores"]
ig_edge_scores = attributions["BA"]["ig_edge_scores"]
gnn_accuracy = attributions["BA"]["gnn_accuracy"]
```

### Load a network edgelist directly

```python
import networkx as nx

graph = nx.read_edgelist("data/networks/BA_N1000.edgelist", nodetype=int)
print(f"Nodes: {graph.number_of_nodes()}, Edges: {graph.number_of_edges()}")
```

### Run the SEIHRD ODE model

```python
from models.01_seird_ode.seihrd_ode_model import SEIHRDModel

model = SEIHRDModel()
results = model.simulate(N=4392200, I0=10, t_end=200)
```

---

## Data Overview

| Directory | Files | Description |
|-----------|-------|-------------|
| `data/networks/` | 16 | 13 edgelists (5 architectures × 3 scales) + 3 metrics CSVs |
| `data/simulation_results/` | 21 | Phase 1 baselines, intervention comparisons, dose-response, scaling, sensitivity (OAT + LHS), adaptive XAI, GNN metrics |
| `data/supplementary/` | 10 | Supplementary dose-response (N=1000/5000), OAT sensitivity, adaptive XAI, network sensitivity + table CSVs |
| `data/xai_attributions/` | 5 | IG + Saliency node/edge scores per network, attribution drift logs |

Total: ~1,845 epidemic simulations + ~45 GNN trainings across all analyses.

---

## License

- **Source code** (`src/`, `models/`, `notebooks/`, `config.py`): **MIT License**
- **Data** (`data/`): **Creative Commons Attribution 4.0 International (CC-BY 4.0)**

See [LICENSE](LICENSE) for the full text of both licenses.

---

## Citation

If you use this code or data, please cite both the repository and the companion paper:

```bibtex
@software{guzzi2026_spreadinganalytics,
  author    = {Guzzi, PietroHiram},
  title     = {{Spreadinganalytics: XAI-Guided GNN Framework for Ebola Epidemic Intervention Design}},
  year      = {2026},
  url       = {https://github.com/hguzzi/Spreadinganalytics}
}
```

See [CITATION.cff](CITATION.cff) for additional citation formats.

---

## Contact

**PietroHiram Guzzi**
Department of Surgical and Medical Sciences, Magna Graecia University, Catanzaro, Italy
Data Analytics and Computational Epidemiology Research Group
