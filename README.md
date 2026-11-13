# AERIS

AERIS is organized as one project with two independent notebooks:

1. `01_fd001_eda_feature_engineering.ipynb` prepares and exports the data.
2. `02_random_forest_training_evaluation.ipynb` loads those exports, trains the model, and evaluates it.

Notebook 1 downloads the public C-MAPSS archive from the [NASA Prognostics Center of Excellence dataset repository](https://www.nasa.gov/intelligent-systems-division/discovery-and-systems-health/pcoe/pcoe-data-set-repository/) and extracts only the FD001 files.

The notebooks do not import or execute one another. Their contract is the content of `data/processed/`:

- `train_original.csv`
- `test_original.csv`
- `train_engineered.csv`
- `test_engineered.csv`
- `test_rul.csv`
- `dataset_metadata.json`

Shared loading and validation logic lives in `src/aeris/data_io.py` so Notebook 2 does not repeat Notebook 1's preparation checks.

When running in Colab, both notebooks mount Google Drive and use `MyDrive/AERIS/data`. Run Notebook 1 once to create the processed files; Notebook 2 can then read them from a separate Colab runtime. Outside Colab, data remains under the project-local `data/` directory.

## Install

From the project root, install the shared package and dependencies:

```bash
pip install -e .
```

## Project structure

```text
AERIS/
|-- notebooks/
|   |-- 01_fd001_eda_feature_engineering.ipynb
|   `-- 02_random_forest_training_evaluation.ipynb
|-- src/aeris/
|   `-- data_io.py
|-- data/
|   |-- raw/
|   `-- processed/
|-- models/
|-- reports/
`-- requirements.txt
```

## Execution order

Run Notebook 1 once to generate the processed artifacts. Then run Notebook 2. Notebook 2 should never depend on variables left in Notebook 1's memory.

By default, the notebooks use `data/` in the project root and `MyDrive/AERIS/data` on Google Colab. To use another location, set `AERIS_DATA_DIR` before running the data setup cell:

```python
import os
os.environ["AERIS_DATA_DIR"] = "/path/to/aeris-data"
```

Notebook 2 writes the reusable model to `models/` and its CV, holdout, NASA test, and feature-importance tables to `reports/`.
