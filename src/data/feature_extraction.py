import pandas as pd
from pathlib import Path
from sklearn.feature_extraction.text import TfidfVectorizer
import joblib

PROJECT_ROOT = Path(__file__).resolve().parents[2]

PROCESSED_PATH = PROJECT_ROOT / "data" / "processed"
MODEL_PATH = PROJECT_ROOT / "src" / "models"

MODEL_PATH.mkdir(parents=True, exist_ok=True)


def extract_resume_features():
    df = pd.read_csv(PROCESSED_PATH / "cleaned_resumes.csv")

    vectorizer = TfidfVectorizer(
        stop_words="english",
        max_features=5000
    )

    features = vectorizer.fit_transform(df["Resume"].fillna(""))

    joblib.dump(
        vectorizer,
        MODEL_PATH / "resume_vectorizer.pkl"
    )

    print("Resume features extracted successfully!")
    print("Resume feature shape:", features.shape)

    return features, df["Category"]


def extract_job_features():
    df = pd.read_csv(PROCESSED_PATH / "cleaned_jobs.csv")

    text_columns = [
        "jobtitle",
        "jobdescription",
        "skills"
    ]

    available_columns = [
        col for col in text_columns if col in df.columns
    ]

    df["combined_text"] = (
        df[available_columns]
        .fillna("")
        .astype(str)
        .agg(" ".join, axis=1)
    )

    vectorizer = TfidfVectorizer(
        stop_words="english",
        max_features=5000
    )

    features = vectorizer.fit_transform(df["combined_text"])

    joblib.dump(
        vectorizer,
        MODEL_PATH / "job_vectorizer.pkl"
    )

    print("Job features extracted successfully!")
    print("Job feature shape:", features.shape)

    return features, df


if __name__ == "__main__":
    extract_resume_features()
    extract_job_features()

    print("\nFeature extraction completed successfully!")