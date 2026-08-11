import pandas as pd


def load_dataset(csv_path, label=None):
    df = pd.read_csv(csv_path)

    if label is not None:
        df["label"] = label

    return df