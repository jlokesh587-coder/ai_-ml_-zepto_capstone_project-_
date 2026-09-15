import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns


def load_and_explore_data():
    df = sns.load_dataset("titanic")
    print("Dataset shape:", df.shape)
    print("\nMissing values:\n", df.isnull().sum())

    df["age"].fillna(df["age"].median(), inplace=True)
    df.drop(columns=["deck"], inplace=True)

    print("\nMissing values after handling:\n", df.isnull().sum())
    return df


if __name__ == "__main__":
    df = load_and_explore_data()
