import re
from typing import BinaryIO, Dict, List, Tuple

import pandas as pd


def _normalize(column: str) -> str:
    """
    Normalize column names:
    - Trim whitespace
    - Convert to lowercase
    - Replace non-alphanumeric characters with underscores
    """
    column = column.strip().lower()
    return re.sub(r"[^a-z0-9]+", "_", column).strip("_")


def load_and_process_excel(
    file_buf: BinaryIO,
) -> Tuple[pd.DataFrame, List[Dict[str, str]]]:
    """
    Read an Excel file, normalize column names, validate data,
    and return the processed DataFrame along with schema metadata.

    Returns:
        Tuple containing:
        - Processed DataFrame
        - List of schema dictionaries
    """

    try:
        df = pd.read_excel(file_buf, engine="openpyxl")
    except Exception as e:
        raise ValueError(f"Unable to read Excel file: {e}")

    if df.empty:
        raise ValueError("The uploaded Excel file is empty.")

    # Normalize column names
    normalized_columns = [_normalize(col) for col in df.columns]

    # Handle duplicate column names
    seen = {}
    unique_columns = []

    for col in normalized_columns:
        if col in seen:
            seen[col] += 1
            unique_columns.append(f"{col}_{seen[col]}")
        else:
            seen[col] = 0
            unique_columns.append(col)

    df.columns = unique_columns

    # Remove completely empty rows
    df.dropna(how="all", inplace=True)

    # Build schema
    schema = [
        {
            "column": col,
            "dtype": str(df[col].dtype),
            "missing_values": int(df[col].isna().sum()),
            "unique_values": int(df[col].nunique()),
        }
        for col in df.columns
    ]

    return df, schema
