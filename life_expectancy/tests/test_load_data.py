"""Tests for the load data module"""
import pandas as pd

from life_expectancy.cleaning import load_data

def test_load_data_from_fixture_file(eu_life_expectancy_input):
    
    path = "life_expectancy/tests/fixtures/eu_life_expectancy_raw.tsv"

    result = load_data(path)

    pd.testing.assert_frame_equal(result, eu_life_expectancy_input)
    