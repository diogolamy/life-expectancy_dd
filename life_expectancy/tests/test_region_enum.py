"""Tests for the region enum module"""

from life_expectancy.load_data import load_data
from life_expectancy.data_transformations import clean_data
from life_expectancy.region_enum import Region

def test_enum_values():
    """
    Test that the Region enum values match the regions in the cleaned dataset.
    """

    df = load_data("life_expectancy/data/eu_life_expectancy_raw.tsv")
    df = clean_data(df, country = None)
    expected_regions = sorted(df["region"].unique())

    actual_regions = sorted(r.value for r in Region)
    assert expected_regions == actual_regions

def test_countries_excludes_aggregates():
    """
    Test that Region.countries() excludes aggregate regions.
    """

    excluded = {"DE_TOT", "EA18", "EA19", "EEA30_2007", "EEA31",
                "EFTA", "EU27_2007", "EU27_2020", "EU28"}
    countries = Region.countries()
    assert not any(code in countries for code in excluded)

    expected_included = [r.value for r in Region if r.name not in excluded]
    assert set(countries) == set(expected_included)
