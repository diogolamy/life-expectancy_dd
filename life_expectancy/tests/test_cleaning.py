"""Tests for the cleaning module"""
import pandas as pd

from life_expectancy.cleaning import main
from . import FIXTURES_DIR


def test_main(eu_life_expectancy_expected):
    """Run the 'main' function and compare the output to the expected output"""

    output_path = FIXTURES_DIR / "test_main_output.csv"

    args = [
        str(FIXTURES_DIR / "eu_life_expectancy_raw.tsv"),
        str(output_path),
        "--country", "PT"
    ]

    main(args)

    actual_df = pd.read_csv(output_path)

    pd.testing.assert_frame_equal(actual_df, eu_life_expectancy_expected)
