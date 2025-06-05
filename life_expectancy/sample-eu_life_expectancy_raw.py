import pandas as pd
from life_expectancy.cleaning import clean_data

# Create Input Fixture with Guaranteed Region
raw_df = pd.read_csv("life_expectancy/data/eu_life_expectancy_raw.tsv", sep="\t")
first_col = raw_df.columns[0]

region = "PT"
region_rows = raw_df[raw_df[first_col].str.endswith(f",{region}")]
other_rows = raw_df[~raw_df[first_col].str.endswith(f",{region}")].sample(n=10, random_state=42)

fixture_input = pd.concat([region_rows.head(2), other_rows], ignore_index=True)
fixture_input = fixture_input.sample(frac=1, random_state=42).reset_index(drop=True)
fixture_input.to_csv("life_expectancy/tests/fixtures/eu_life_expectancy_raw.tsv", sep="\t", index=False)

# Create Expected Output Fixture
df_input = pd.read_csv("life_expectancy/tests/fixtures/eu_life_expectancy_raw.tsv", sep="\t")
df_expected = clean_data(df_input, country=region)
df_expected.to_csv("life_expectancy/tests/fixtures/eu_life_expectancy_expected.csv", index=False)
