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

def test_clean_numeric_column(eu_life_expectancy_input):
    """Test that clean_numeric_column removes non-numeric symbols and extracts numbers"""
    result = clean_numeric_column(eu_life_expectancy_input, "year")
    assert result["value"].tolist() == ["1000", "200"]

def test_convert_column_dtype():
    """Test that convert_column_dtype correctly changes the data type of a column"""
    df = pd.DataFrame({"val": ["1", "2"]})
    result = convert_column_dtype(df, "val", int)
    assert result["val"].dtype == int

def test_filter_rows():
    """Test that filter_rows correctly filters rows based on a column value"""
    df = pd.DataFrame({"country": ["PT", "DE"], "val": [10, 20]})
    result = filter_rows(df, "country", "PT")
    assert result.shape[0] == 1
    assert result.iloc[0]["val"] == 10
