"""Data ingestion functions for loading CSV, JSON, and Excel files."""

import json
import logging
from pathlib import Path

import pandas as pd

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def load_csv(filepath):
    """Load a CSV file into a DataFrame.

    Args:
        filepath (str | Path): Path to CSV file.

    Returns:
        pd.DataFrame: Loaded data.

    Raises:
        FileNotFoundError: If the file does not exist.
        pd.errors.EmptyDataError: If the CSV is empty.
        pd.errors.ParserError: If the CSV cannot be parsed.
        Exception: For any other read errors.
    """
    filepath = Path(filepath)

    if not filepath.exists():
        logger.error("CSV file not found: %s", filepath)
        raise FileNotFoundError(f"CSV file not found: {filepath}")

    try:
        logger.info("Loading CSV file: %s", filepath)

        df = pd.read_csv(filepath)

        logger.info(
            "Successfully loaded %d rows from %s",
            len(df),
            filepath,
        )
        return df

    except pd.errors.EmptyDataError:
        logger.error("CSV file is empty: %s", filepath)
        raise

    except pd.errors.ParserError as e:
        logger.error("Error parsing CSV %s: %s", filepath, e)
        raise

    except Exception:
        logger.exception("Unexpected error loading CSV %s", filepath)
        raise


def load_json(filepath):
    """Load a JSON file and flatten it into a DataFrame.

    Args:
        filepath (str | Path): Path to JSON file.

    Returns:
        pd.DataFrame: Flattened JSON data.

    Raises:
        FileNotFoundError: If the file does not exist.
        json.JSONDecodeError: If the JSON is invalid.
        Exception: For any other read errors.
    """
    filepath = Path(filepath)

    if not filepath.exists():
        logger.error("JSON file not found: %s", filepath)
        raise FileNotFoundError(f"JSON file not found: {filepath}")

    try:
        logger.info("Loading JSON file: %s", filepath)

        with open(filepath, "r", encoding="utf-8") as f:
            data = json.load(f)

        df = pd.json_normalize(data)

        logger.info(
            "Successfully loaded %d rows from %s",
            len(df),
            filepath,
        )

        return df

    except json.JSONDecodeError as e:
        logger.error("Invalid JSON in %s: %s", filepath, e)
        raise

    except Exception:
        logger.exception("Unexpected error loading JSON %s", filepath)
        raise


def load_excel(filepath, sheet_name=0, **kwargs):  # pragma: no cover
    """Load an Excel file into a DataFrame or dictionary of DataFrames.

    Args:
        filepath (str | Path): Path to Excel file.
        sheet_name (str | int | list | None): Sheets to read.
        **kwargs: Additional arguments for ``pd.read_excel()``.

    Returns:
        pd.DataFrame | dict[str, pd.DataFrame]: Loaded data.

    Raises:
        FileNotFoundError: If the file does not exist.
        ValueError: If the sheet name is invalid.
        ImportError: If the required Excel engine is not installed.
        Exception: For any other read errors.
    """
    filepath = Path(filepath)

    if not filepath.exists():
        logger.error("Excel file not found: %s", filepath)
        raise FileNotFoundError(f"Excel file not found: {filepath}")

    try:
        logger.info(
            "Loading Excel file: %s (sheet_name=%s)",
            filepath,
            sheet_name,
        )

        df = pd.read_excel(filepath, sheet_name=sheet_name, **kwargs)

        if isinstance(df, dict):
            total_rows = sum(len(sheet) for sheet in df.values())
            logger.info(
                "Successfully loaded %d sheets (%d total rows) from %s",
                len(df),
                total_rows,
                filepath,
            )
        else:
            logger.info(
                "Successfully loaded %d rows from %s",
                len(df),
                filepath,
            )

        return df

    except ValueError as e:
        logger.error("Value error loading Excel %s: %s", filepath, e)
        raise

    except ImportError as e:
        logger.error("Missing Excel engine for %s: %s", filepath, e)
        raise

    except Exception:
        logger.exception("Unexpected error loading Excel %s", filepath)
        raise
