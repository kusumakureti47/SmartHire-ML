import pandas as pd
from pathlib import Path

# Project root folder
PROJECT_ROOT = Path(__file__).resolve().parents[2]

# Dataset paths
RESUME_DATA_PATH = PROJECT_ROOT / "data" / "raw" / "UpdatedResumeDataSet.csv"
JOB_DATA_PATH = PROJECT_ROOT / "data" / "raw" / "naukri_com-job_sample.csv"


def load_resume_data():
    """Load resume dataset."""
    if not RESUME_DATA_PATH.exists():
        raise FileNotFoundError(f"Resume dataset not found: {RESUME_DATA_PATH}")

    return pd.read_csv(RESUME_DATA_PATH)


def load_job_data():
    """Load job listings dataset."""
    if not JOB_DATA_PATH.exists():
        raise FileNotFoundError(f"Job dataset not found: {JOB_DATA_PATH}")

    return pd.read_csv(JOB_DATA_PATH)


if __name__ == "__main__":
    resumes = load_resume_data()
    jobs = load_job_data()

    print("Resume dataset loaded successfully!")
    print("Resume shape:", resumes.shape)

    print("\nJob dataset loaded successfully!")
    print("Job shape:", jobs.shape)

    print("\nResume columns:", resumes.columns.tolist())
    print("Job columns:", jobs.columns.tolist())