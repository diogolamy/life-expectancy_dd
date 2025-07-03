"""Tests for the data transformations module"""
import pandas as pd

from life_expectancy.data_transformations import (
    split_columns, unpivot, clean_numeric_column,
    convert_column_dtype, filter_rows
)

def test_split_columns(eu_life_expectancy_input):
    """Test that split_columns correctly splits a compound column into separate columns"""
    result = split_columns(eu_life_expectancy_input, "unit,sex,age,geo\\time", ",",
                           ["unit", "sex", "age", "geo"])

    for col in ["unit", "sex", "age", "geo"]:
        assert col in result.columns

def test_unpivot(eu_life_expectancy_input):
    """Test that unpivot reshapes wide data into long format correctly"""

    result = unpivot(eu_life_expectancy_input, ["unit", "sex", "age", "geo"],
                     identifier_col_name="year", value_col_name="value")

    assert list(result.columns) == ["unit", "sex", "age", "geo", "year", "value"]

def test_clean_numeric_column():
    """Test that clean_numeric_column removes non-numeric symbols and extracts numbers"""
    df = pd.DataFrame({'value': ['', '19.3 e', '71.6']})
    result = clean_numeric_column(df, 'value')
    assert result['value'].tolist() == ['19.3', '71.6']

def test_convert_column_dtype(eu_life_expectancy_intermediate):
    """Test that convert_column_dtype correctly changes the data type of a column"""
    result = convert_column_dtype(eu_life_expectancy_intermediate, "year", int)
    assert result["year"].dtype == int

def test_filter_rows(eu_life_expectancy_intermediate):
    """Test that filter_rows correctly filters rows based on a column value"""
    result = filter_rows(eu_life_expectancy_intermediate, "region", "PT")
    assert (result["region"] == "PT").all()
