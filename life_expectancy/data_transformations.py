"""Data transformation life_espectancy"""

import pandas as pd
from life_expectancy.region_enum import Region

def split_columns(df: pd.DataFrame,
                  column: str,
                  delimiter: str = ',',
                  new_column_names: list[str] = None) -> pd.DataFrame:
    """
    Splits a column into multiple columns using a delimiter.
    """

    splits = df[column].str.split(delimiter, expand=True)
    num_cols = splits.shape[1]

    if new_column_names:
        if len(new_column_names) != num_cols:
            raise ValueError(f"{len(new_column_names)} names, but {num_cols} columns.")
        new_cols = new_column_names
    else:
        new_cols = [f'col_{i+1}' for i in range(num_cols)]

    df[new_cols] = splits
    df.drop(columns=[column], inplace=True)

    return df


def unpivot(df: pd.DataFrame, exclude_columns: list,
            identifier_col_name="identifier", value_col_name="value") -> pd.DataFrame:
    """
    Reshape the data by gathering multiple columns into key-value pairs, 
    keeping certain columns fixed.
    """

    value_columns = [col for col in df.columns if col not in exclude_columns]

    unpivoted_df = pd.melt(df,
                           id_vars=exclude_columns,
                           value_vars=value_columns,
                           var_name=identifier_col_name,
                           value_name=value_col_name)

    return unpivoted_df


def clean_numeric_column(df: pd.DataFrame, column: str) -> pd.DataFrame:
    """
    Remove common non-numeric symbols and extract numeric data, 
    dropping invalid entries.
    """

    df[column] = df[column].astype(str).str.strip()

    symbols_to_remove = ['$', ',', '%', '€', ':', 'kg', 'approx.', 'N/A', 'missing']
    for sym in symbols_to_remove:
        df[column] = df[column].str.replace(sym, '', regex=False)

    df[column] = df[column].str.extract(r'(-?\d+\.?\d*)', expand=False)
    df = df.dropna(subset=[column])

    return df


def convert_column_dtype(df, column_name, target_dtype):
    """
    Converts a DataFrame column to a specified data type.
    """

    df[column_name] = df[column_name].astype(target_dtype)
    return df


def filter_rows(df: pd.DataFrame, column: str, value) -> pd.DataFrame:
    """
    Filters rows where the column matches the specified value.
    """

    return df[df[column] == value]

def clean_data(df: pd.DataFrame, country: Region = Region.PT) -> pd.DataFrame:
    """
    Clean dataframe based on life expectancy data format by splitting columns, 
    reshaping, converting types, and filtering by country.
    """

    id_columns = ['unit', 'sex', 'age', 'region']

    df = split_columns(df, column='unit,sex,age,geo\\time',
                       delimiter=',', new_column_names=id_columns)

    df = unpivot(df, exclude_columns=id_columns,
                 identifier_col_name='year', value_col_name='value')

    df = clean_numeric_column(df, 'year')
    df = convert_column_dtype(df, 'year', int)

    df = clean_numeric_column(df, 'value')
    df = convert_column_dtype(df, 'value', float)

    if country:
        df = filter_rows(df, 'region', country.value)

    return df
