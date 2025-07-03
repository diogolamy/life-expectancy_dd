"""Tests for the cleaning module"""
import pandas as pd

from life_expectancy.cleaning import main
from . import FIXTURES_DIR


def test_main(eu_life_expectancy_expected):
    """Run the 'main' function and compare the output to the expected output"""

    args = [
        str(FIXTURES_DIR / "eu_life_expectancy_raw.tsv"),
        str(FIXTURES_DIR / "eu_life_expectancy_expected.csv"),
        "--country", "PT"
    ]

    result = main(args)

    pd.testing.assert_frame_equal(
    result.reset_index(drop=True),
    eu_life_expectancy_expected.reset_index(drop=True)
)
