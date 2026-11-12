"""The data contract between the preparation and modeling notebooks."""

from __future__ import annotations

import json
from pathlib import Path

import pandas as pd


TRAIN_FILE = "train_original.csv"
TEST_FILE = "test_original.csv"
TEST_RUL_FILE = "test_rul.csv"
METADATA_FILE = "dataset_metadata.json"


def save_processed_data(
    output_dir: str | Path,
    train_df: pd.DataFrame,
    test_df: pd.DataFrame,
    test_rul_df: pd.DataFrame,
    feature_columns: list[str],
) -> None:
    """Save Notebook 1 outputs using the format expected by Notebook 2."""
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    train_df.to_csv(output_dir / TRAIN_FILE, index=False)
    test_df.to_csv(output_dir / TEST_FILE, index=False)
    test_rul_df.to_csv(output_dir / TEST_RUL_FILE, index=False)

    metadata = {
        "target_column": "RUL",
        "id_column": "engine_id",
        "feature_columns": feature_columns,
    }
    (output_dir / METADATA_FILE).write_text(
        json.dumps(metadata, indent=2),
        encoding="utf-8",
    )


def load_processed_data(
    data_dir: str | Path,
) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame, list[str]]:
    """Load and minimally validate the prepared data for Notebook 2."""
    data_dir = Path(data_dir)
    required_files = [TRAIN_FILE, TEST_FILE, TEST_RUL_FILE, METADATA_FILE]
    missing_files = [name for name in required_files if not (data_dir / name).is_file()]

    if missing_files:
        raise FileNotFoundError(
            f"Run Notebook 1 first. Missing files in {data_dir}: {missing_files}"
        )

    train_df = pd.read_csv(data_dir / TRAIN_FILE)
    test_df = pd.read_csv(data_dir / TEST_FILE)
    test_rul_df = pd.read_csv(data_dir / TEST_RUL_FILE)
    metadata = json.loads((data_dir / METADATA_FILE).read_text(encoding="utf-8"))
    feature_columns = metadata["feature_columns"]

    required_train_columns = {"engine_id", "cycle", "RUL", *feature_columns}
    required_test_columns = {"engine_id", "cycle", *feature_columns}

    missing_train_columns = required_train_columns - set(train_df.columns)
    missing_test_columns = required_test_columns - set(test_df.columns)

    if missing_train_columns:
        raise ValueError(f"Training data is missing: {sorted(missing_train_columns)}")
    if missing_test_columns:
        raise ValueError(f"Testing data is missing: {sorted(missing_test_columns)}")
    if "true_rul" not in test_rul_df.columns:
        raise ValueError("test_rul.csv must contain a 'true_rul' column.")

    return train_df, test_df, test_rul_df, feature_columns
