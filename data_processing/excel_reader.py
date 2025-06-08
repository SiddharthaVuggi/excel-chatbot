import pandas as pd
import re
from typing import Tuple

def _normalize(col: str) -> str:
    col = col.strip().lower()
    return re.sub(r"[^a-z0-9]+", "_", col)

def load_and_process_excel(file_buf) -> Tuple[pd.DataFrame, list]:
    """Read Excel, normalise columns, return df and schema list."""
    df = pd.read_excel(file_buf, engine="openpyxl")
    df.columns = [_normalize(c) for c in df.columns]
    return df, df.columns.tolist()