"""
Central path configuration for the Spreadinganalytics package.

All data directories are resolved relative to the repository root,
so the code works out-of-the-box after cloning — no hardcoded paths.
"""

from pathlib import Path

# Repository root (parent of this file)
BASE_DIR = Path(__file__).parent.resolve()

# Data directories
DATA_DIR = BASE_DIR / "data"
NETWORKS_DIR = DATA_DIR / "networks"
RESULTS_DIR = DATA_DIR / "simulation_results"
ATTRIBUTIONS_DIR = DATA_DIR / "xai_attributions"
SUPPLEMENTARY_DIR = DATA_DIR / "supplementary"

# Model directories
MODELS_DIR = BASE_DIR / "models"
