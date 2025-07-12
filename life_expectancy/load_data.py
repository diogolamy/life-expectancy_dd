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


# Context function
def load_data(path: str, *, delimiter: str = None) -> pd.DataFrame:
    """
    Loads a dataset based on file extension using the strategy pattern.
    """

    loaders = {
        '.csv': CSVLoader(),
        '.tsv': TSVLoader(),
        '.txt': TXTLoader(delimiter=delimiter or ","),
        '.xlsx': ExcelLoader(),
        '.xls': ExcelLoader(),
        '.json': JSONLoader(),
        '.parquet': ParquetLoader(),
        '.zip': ZipLoader(),
    }

    ext = os.path.splitext(path.lower())[1]

    if ext not in loaders:
        raise ValueError(f"Unsupported file format: {path}")

    if delimiter is not None and ext != '.txt':
        raise ValueError(f"`delimiter` argument is only supported for .txt files, not for {ext}")

    loader = loaders[ext]
    return loader.load_data(path)
