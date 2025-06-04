import pandas as pd
from life_expectancy.cleaning import clean_data, save_data

# Load raw data with composite first column
raw_path = "life_expectancy/data/eu_life_expectancy_raw.tsv"
df = pd.read_csv(raw_path, sep="\t")

composite_col = df.columns[0]

# Ensure that PT is on the sample
target_region = 'PT'
region_rows = df[df[composite_col].str.endswith(",{}".format(target_region))]

other_rows = df[~df[composite_col].str.endswith(",{}".format(target_region))]
sampled_rows = other_rows.sample(n=10, random_state=42)

# Combine with the region rows (at least 1 row guaranteed)
input_fixture_df = pd.concat([region_rows.head(2), sampled_rows], ignore_index=True)

# Shuffle the combined rows
input_fixture_df = input_fixture_df.sample(frac=1, random_state=42).reset_index(drop=True)

# Save fixture to TSV (same format as input, untouched structure)
input_fixture_path = "life_expectancy/tests/fixtures/eu_life_expectancy_raw.tsv"
input_fixture_df.to_csv(input_fixture_path, sep="\t", index=False)



# Path to the input fixture
input_fixture_path = "life_expectancy/tests/fixtures/eu_life_expectancy_raw.tsv"

# Load the fixture
df_input = pd.read_csv(input_fixture_path, sep="\t")

# Clean it using your existing function
df_expected = clean_data(df_input, country="PT")  # or another region you ensured

# Save expected output
expected_fixture_path = "life_expectancy/tests/fixtures/eu_life_expectancy_expected.csv"
df_expected.to_csv(expected_fixture_path, index=False)



