'''Create Sample Data for Test Fixtures'''

import pandas as pd
from life_expectancy.data_transformations import split_columns, unpivot, clean_data

# Create Input Fixture with Guaranteed Region
raw_df = pd.read_csv("life_expectancy/data/eu_life_expectancy_raw.tsv", sep="\t")
first_col = raw_df.columns[0]

REGION = "PT"
region_rows = raw_df[raw_df[first_col].str.endswith(f",{REGION}")]
other_rows = raw_df[~raw_df[first_col].str.endswith(f",{REGION}")].sample(n=10, random_state=42)

fixture_input = pd.concat([region_rows.head(2), other_rows], ignore_index=True)
fixture_input.to_csv("life_expectancy/tests/fixtures/eu_life_expectancy_raw.tsv",
                     sep="\t", index=False)

print("Original shape:", raw_df.shape)
print("Fixture shape:", fixture_input.shape)

# Create Intermediate Fixture

id_columns = ['unit', 'sex', 'age', 'region']

df_intermediate = split_columns(fixture_input.copy(), column='unit,sex,age,geo\\time',
                                delimiter=',', new_column_names=id_columns)

df_intermediate = unpivot(df_intermediate, exclude_columns=id_columns,
                          identifier_col_name='year', value_col_name='value')

df_intermediate.to_csv("life_expectancy/tests/fixtures/eu_life_expectancy_intermediate_raw.tsv",
                       sep="\t", index=False)

# Create Expected Output Fixture
df_input = pd.read_csv("life_expectancy/tests/fixtures/eu_life_expectancy_raw.tsv", sep="\t")
df_expected = clean_data(df_input, country=REGION)
df_expected.to_csv("life_expectancy/tests/fixtures/eu_life_expectancy_expected.csv", index=False)
