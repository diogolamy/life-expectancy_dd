import pandas as pd

def save_data(df: pd.DataFrame, filename) -> None:
    """
    Saves a DataFrame in the format inferred from the file extension.
    """

    filename = str(filename)

    if filename.endswith('.csv'):
        df.to_csv(filename, index=False)
    elif filename.endswith('.xlsx'):
        df.to_excel(filename, index=False)
    elif filename.endswith('.json'):
        df.to_json(filename, orient='records', lines=True)
    elif filename.endswith('.parquet'):
        df.to_parquet(filename, index=False)
    else:
        raise ValueError(f"Unsupported file format for: {filename}")