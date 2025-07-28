"""Tests for the load data module"""
import pandas as pd

from life_expectancy.cleaning import load_data

def test_load_data_from_fixture_file(eu_life_expectancy_input):
    """Test that load_data correctly reads the TSV file into a DataFrame matching the fixture."""
    path = "life_expectancy/tests/fixtures/eu_life_expectancy_raw.tsv"

    result = load_data(path)

    pd.testing.assert_frame_equal(result, eu_life_expectancy_input)

def test_load_data_from_eurostat_zip_runs():
    """
    Test that load_data successfully loads supported files from a Eurostat ZIP archive.
    """
    path = "life_expectancy/data/eurostat_life_expect.zip"

    result = load_data(path)

    assert isinstance(result, dict)
    assert result, "No files were loaded from the ZIP archive"

    for name, df in result.items():
        assert isinstance(df, pd.DataFrame), f"{name} did not load as a DataFrame"
        assert not df.empty, f"{name} loaded as an empty DataFrame"
