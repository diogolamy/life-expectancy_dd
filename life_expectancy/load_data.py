"""Load data life_espectancy"""

import pandas as pd

def load_data(path: str, *, delimiter: str = '\t') -> pd.DataFrame:
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

    path = path.lower()
    for file_extension, loader_function in loaders.items():
        if path.endswith(file_extension):
            return loader_function(path)

    raise ValueError(f"Unsupported file format: {path}")
