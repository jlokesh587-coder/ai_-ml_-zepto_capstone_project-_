from analysis import load_and_explore_data
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report
from sklearn.model_selection import train_test_split


def build_and_evaluate_model():
    df = load_and_explore_data()

    X = df[["age", "fare", "pclass", "sibsp", "parch"]]
    y = df["survived"]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    model = RandomForestClassifier(random_state=42)
    model.fit(X_train, y_train)

    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)

    print("Model Accuracy:", accuracy)
    print("\nClassification Report:\n", classification_report(y_test, y_pred))


if __name__ == "__main__":
    build_and_evaluate_model()
