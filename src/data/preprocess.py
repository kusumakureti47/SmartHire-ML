import pandas as pd
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]

RAW_PATH = PROJECT_ROOT / "data" / "raw"
PROCESSED_PATH = PROJECT_ROOT / "data" / "processed"

PROCESSED_PATH.mkdir(parents=True, exist_ok=True)


def clean_text(text):
    if pd.isna(text):
        return ""

    text = str(text)
    text = text.lower()
    text = " ".join(text.split())

    return text


def preprocess_resumes():
    file_path = RAW_PATH / "UpdatedResumeDataSet.csv"

    df = pd.read_csv(file_path)

    df = df.dropna(subset=["Category", "Resume"])
    df["Category"] = df["Category"].astype(str).str.strip()
    df["Resume"] = df["Resume"].apply(clean_text)

    df = df.drop_duplicates()
    df = df[df["Resume"] != ""]

    output_path = PROCESSED_PATH / "cleaned_resumes.csv"
    df.to_csv(output_path, index=False)

    print("Resume preprocessing completed!")
    print("Resume records:", len(df))

    return df


def preprocess_jobs():
    file_path = RAW_PATH / "naukri_com-job_sample.csv"

    df = pd.read_csv(file_path)

    text_columns = [
        "jobtitle",
        "jobdescription",
        "skills",
        "industry",
        "education",
        "experience"
    ]

    for column in text_columns:
        if column in df.columns:
            df[column] = df[column].apply(clean_text)

    df = df.drop_duplicates()
    df = df[df["jobtitle"] != ""]

    output_path = PROCESSED_PATH / "cleaned_jobs.csv"
    df.to_csv(output_path, index=False)

    print("Job preprocessing completed!")
    print("Job records:", len(df))

    return df


if __name__ == "__main__":
    resumes = preprocess_resumes()
    jobs = preprocess_jobs()

    print("\nBoth datasets cleaned successfully!")