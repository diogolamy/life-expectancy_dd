"""Tests for the save data module"""

import pandas as pd
from unittest.mock import patch

from life_expectancy.cleaning import save_data

def test_save_data_calls_to_csv(tmp_path):

    df = pd.DataFrame({"col": [1, 2, 3]})
    
    output_path = tmp_path / "test_output.csv"

    with patch("pandas.DataFrame.to_csv") as mock_to_csv:
        save_data(df, str(output_path)) 

        mock_to_csv.assert_called_once_with(str(output_path), index=False)
