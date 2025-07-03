"""Load data life_espectancy"""

import os
import pandas as pd

def load_data(path: str, *, delimiter: str = None) -> pd.DataFrame:
    """
    Loads a dataset based on file extension.
    """

    loaders = {
        '.csv': lambda p: pd.read_csv(p, sep=','),
        '.tsv': lambda p: pd.read_csv(p, sep='\t'),
        '.txt': lambda p: pd.read_csv(p, sep=delimiter),
        '.xlsx': pd.read_excel,
        '.xls': pd.read_excel,
        '.json': pd.read_json,
        '.parquet': pd.read_parquet,
    }

    ext = os.path.splitext(path.lower())[1]

    if ext not in loaders:
        raise ValueError(f"Unsupported file format: {path}")

    if delimiter is not None and ext != '.txt':
        raise ValueError(f"`delimiter` argument is only supported for .txt files, not for {ext}")

    return loaders[ext](path)
