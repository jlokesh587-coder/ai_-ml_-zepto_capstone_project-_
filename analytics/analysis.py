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

def perform_eda(df):
    plt.figure(figsize=(10, 6))
    sns.histplot(df["age"], kde=True)
    plt.title("Distribution of Age")
    plt.savefig("age_distribution.png")

    plt.figure(figsize=(10, 6))
    sns.boxplot(x="class", y="fare", data=df)
    plt.title("Fare by Passenger Class")
    plt.savefig("fare_boxplot.png")

    plt.figure(figsize=(10, 6))
    sns.barplot(x="sex", y="survived", data=df)
    plt.title("Survival Rate by Sex")
    plt.savefig("survival_rate_sex.png")

    plt.figure(figsize=(12, 8))
    sns.heatmap(
        df.select_dtypes(include="number").corr(), annot=True, cmap="coolwarm"
    )
    plt.title("Correlation Heatmap")
    plt.savefig("correlation_heatmap.png")


if __name__ == "__main__":
    df = load_and_explore_data()
    perform_eda(df)



