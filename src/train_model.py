import pandas as pd
import joblib

from pathlib import Path
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report

PROJECT_ROOT = Path(__file__).resolve().parents[1]

DATA_PATH = PROJECT_ROOT / "data" / "processed" / "cleaned_resumes.csv"
MODEL_PATH = PROJECT_ROOT / "src" / "models"

MODEL_PATH.mkdir(parents=True, exist_ok=True)


def train_resume_classifier():

    print("Loading resume dataset...")

    df = pd.read_csv(DATA_PATH)
    df = df.dropna(subset=["Resume", "Category"])

    X = df["Resume"].astype(str)
    y = df["Category"].astype(str)

    print("Total resumes:", len(df))
    print("Categories:", y.nunique())

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.2,
        random_state=42,
        stratify=y
    )

    print("\nConverting resumes into TF-IDF features...")

    vectorizer = TfidfVectorizer(
        stop_words="english",
        max_features=5000
    )

    X_train_tfidf = vectorizer.fit_transform(X_train)
    X_test_tfidf = vectorizer.transform(X_test)

    print("Training Logistic Regression model...")

    model = LogisticRegression(
        max_iter=1000,
        class_weight="balanced"
    )

    model.fit(X_train_tfidf, y_train)

    predictions = model.predict(X_test_tfidf)

    accuracy = accuracy_score(y_test, predictions)

    print("\nModel training completed!")
    print("Accuracy:", round(accuracy * 100, 2), "%")

    print("\nClassification Report:")
    print(classification_report(y_test, predictions))

    joblib.dump(
        model,
        MODEL_PATH / "resume_classifier.pkl"
    )

    joblib.dump(
        vectorizer,
        MODEL_PATH / "resume_classifier_vectorizer.pkl"
    )

    print("\nModel saved successfully!")


if __name__ == "__main__":
    train_resume_classifier()