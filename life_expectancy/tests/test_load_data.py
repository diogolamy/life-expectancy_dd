"""Tests for the load data module"""
import pandas as pd

from life_expectancy.cleaning import load_data

def test_load_data_from_fixture_file(eu_life_expectancy_input):
    """Test that load_data correctly reads the TSV file into a DataFrame matching the fixture."""
    path = "life_expectancy/tests/fixtures/eu_life_expectancy_raw.tsv"

    result = load_data(path, '\t')

# Debug output
    print("Result columns:", result.columns.tolist())
    print("Fixture columns:", eu_life_expectancy_input.columns.tolist())
    print("Result shape:", result.shape)
    print("Fixture shape:", eu_life_expectancy_input.shape)

    pd.testing.assert_frame_equal(result, eu_life_expectancy_input)
