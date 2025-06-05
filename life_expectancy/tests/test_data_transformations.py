"""Tests for the data transformations module"""
import pandas as pd

import pytest
from life_expectancy.data_transformations import (
    split_columns, unpivot, clean_numeric_column,
    convert_column_dtype, filter_rows
)

def test_split_columns():
    df = pd.DataFrame({"compound": ["A,B,C", "D,E,F"]})
    result = split_columns(df.copy(), "compound", ",", ["col1", "col2", "col3"])
    assert list(result.columns) == ["col1", "col2", "col3"]
    assert result.shape == (2, 3)

def test_unpivot():
    df = pd.DataFrame({"id": [1], "2020": [10], "2021": [20]})
    result = unpivot(df, exclude_columns=["id"], identifier_col_name="year", value_col_name="value")
    assert set(result.columns) == {"id", "year", "value"}
    assert len(result) == 2

def test_clean_numeric_column():
    df = pd.DataFrame({"value": ["€1,000", "N/A", " 200 "]})
    cleaned = clean_numeric_column(df, "value")
    assert cleaned["value"].tolist() == ["1000", "200"]

def test_convert_column_dtype():
    df = pd.DataFrame({"val": ["1", "2"]})
    result = convert_column_dtype(df, "val", int)
    assert result["val"].dtype == int

def test_filter_rows():
    df = pd.DataFrame({"country": ["PT", "DE"], "val": [10, 20]})
    result = filter_rows(df, "country", "PT")
    assert result.shape[0] == 1
    assert result.iloc[0]["val"] == 10
    