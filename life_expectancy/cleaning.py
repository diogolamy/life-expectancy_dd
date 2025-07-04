"""Data cleaning life_expectancy"""

import argparse
from life_expectancy.load_data import load_data
from life_expectancy.data_transformations import clean_data
from life_expectancy.save_data import save_data
from life_expectancy.region_enum import Region


def main(args=None):
    """
    Main function for load, clean, and save the life expectancy data,
    based on a specific country code.
    """

    parser = argparse.ArgumentParser(description="Clean EU life expectancy data.")
    parser.add_argument("input_path", help="Path to input data file")
    parser.add_argument("output_path", help="Path to save cleaned data")
    parser.add_argument("--country", default="PT", help="Country code to filter (default: PT)")

    parsed_args = parser.parse_args(args)

    country_enum = Region(parsed_args.country)

    df = load_data(parsed_args.input_path)
    cleaned_df = clean_data(df, country=country_enum)
    save_data(cleaned_df, parsed_args.output_path)
    return cleaned_df


if __name__ == "__main__":  # pragma: no cover
    main()
