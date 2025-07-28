"""Load data life_expectancy"""

# pylint: disable=too-few-public-methods

import os
import zipfile
from abc import ABC, abstractmethod

import pandas as pd

# Strategy base class
class DataLoader(ABC):
    """Abstract base class for data loaders."""

    @abstractmethod
    def load_data(self, path: str) -> pd.DataFrame:
        """Load data from a file."""
        raise NotImplementedError

# Strategies
class CSVLoader(DataLoader):
    """Load data from a CSV file."""

    def load_data(self, path: str) -> pd.DataFrame:
        """Load data from a CSV file."""
        return pd.read_csv(path, sep=',')


class TSVLoader(DataLoader):
    """Load data from a TSV file."""

    def load_data(self, path: str) -> pd.DataFrame:
        """Load data from a TSV file."""
        return pd.read_csv(path, sep='\t')


class TXTLoader(DataLoader):
    """Load data from a TXT file."""

    def __init__(self, delimiter: str = ","):
        self.delimiter = delimiter

    def load_data(self, path: str) -> pd.DataFrame:
        return pd.read_csv(path, sep=self.delimiter)


class ExcelLoader(DataLoader):
    """Load data from an Excel file (.xls or .xlsx)."""

    def load_data(self, path: str) -> pd.DataFrame:
        """Load data from an Excel file (.xls or .xlsx)."""
        return pd.read_excel(path)


class JSONLoader(DataLoader):
    """Load data from a JSON file."""

    def load_data(self, path: str) -> pd.DataFrame:
        """Load data from a JSON file."""
        return pd.read_json(path)


class ParquetLoader(DataLoader):
    """Load data from a Parquet file."""

    def load_data(self, path: str) -> pd.DataFrame:
        """Load data from a Parquet file."""
        return pd.read_parquet(path)


class ZipLoader(DataLoader):
    """Loads all supported files from a ZIP archive."""

    def load_data(self, path: str) -> dict[str, pd.DataFrame]:
        loaders = {
            '.csv': CSVLoader(),
            '.tsv': TSVLoader(),
            '.txt': TXTLoader(),
            '.xlsx': ExcelLoader(),
            '.xls': ExcelLoader(),
            '.json': JSONLoader(),
            '.parquet': ParquetLoader(),
        }

        with zipfile.ZipFile(path, 'r') as zip_ref:
            return {
                name: loaders[os.path.splitext(name)[1].lower()].load_data(zip_ref.open(name))
                for name in zip_ref.namelist()
                if os.path.splitext(name)[1].lower() in loaders
            }


def get_loader(ext: str, delimiter: str = None) -> DataLoader:
    """
    Returns the appropriate DataLoader based on the file extension.
    """
    
    ext = ext.lower()
    if ext == '.csv':
        return CSVLoader()
    elif ext == '.tsv':
        return TSVLoader()
    elif ext == '.txt':
        return TXTLoader(delimiter=delimiter or ",")
    elif ext in ['.xls', '.xlsx']:
        return ExcelLoader()
    elif ext == '.json':
        return JSONLoader()
    elif ext == '.parquet':
        return ParquetLoader()
    elif ext == '.zip':
        return ZipLoader()
    else:
        raise ValueError(f"Extensão de ficheiro não suportada: {ext}")


# Context function
def load_data(path: str, *, delimiter: str = None) -> pd.DataFrame:
    """
    Loads a dataset based on file extension using the strategy pattern.
    """
    
    ext = os.path.splitext(path)[1]

    if delimiter is not None and ext != '.txt':
        raise ValueError(f"`delimiter` is only supported for .txt files, not for {ext}")

    loader = get_loader(ext, delimiter)
    return loader.load_data(path)
