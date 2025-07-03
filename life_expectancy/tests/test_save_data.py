"""Tests for the save data module"""

from unittest.mock import patch

from life_expectancy.cleaning import save_data

def test_save_data_calls_to_csv(eu_life_expectancy_expected, tmp_path):
    """
    Test that save_data calls DataFrame.to_csv with the correct arguments
    when saving to a .csv file. Uses mocking to prevent actual file writing.
    """

    with patch("pandas.DataFrame.to_csv") as mock_to_csv:
        save_data(eu_life_expectancy_expected, tmp_path / "output.csv")

        mock_to_csv.assert_called_once_with(str(tmp_path / "output.csv"), index=False)
