# AERIS

AERIS is organized as one project with two independent notebooks:

1. `01_fd001_eda_feature_engineering.ipynb` prepares and exports the data.
2. `02_random_forest_training_evaluation.ipynb` loads those exports, trains the model, and evaluates it.

The notebooks do not import or execute one another. Their contract is the content of `data/processed/`:

- `train_original.csv`
- `test_original.csv`
- `test_rul.csv`
- `dataset_metadata.json`

Shared saving, loading, and validation logic lives in `src/aeris/data_io.py` so it is not duplicated across notebooks.

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
