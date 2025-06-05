"""Pytest configuration file"""
import pandas as pd
import pytest

from . import FIXTURES_DIR, OUTPUT_DIR

@pytest.fixture(scope="session")
def pt_life_expectancy_expected() -> pd.DataFrame:
    """Fixture to load the expected output of the cleaning script"""
    return pd.read_csv(FIXTURES_DIR / "pt_life_expectancy_expected.csv")

@pytest.fixture(scope="session")
def eu_life_expectancy_input() -> pd.DataFrame:
    """Fixture to load the input sample for testing cleaning."""
    return pd.read_csv(FIXTURES_DIR / "eu_life_expectancy_raw.tsv", sep="\t")

@pytest.fixture(scope="session")
def eu_life_expectancy_expected() -> pd.DataFrame:
    """Fixture to load the expected cleaned output of the sample."""
    return pd.read_csv(FIXTURES_DIR / "eu_life_expectancy_expected.csv")
