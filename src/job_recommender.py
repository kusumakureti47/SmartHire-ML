import pandas as pd

from pathlib import Path
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

PROJECT_ROOT = Path(__file__).resolve().parents[1]

DATA_PATH = PROJECT_ROOT / "data" / "processed" / "cleaned_jobs.csv"


def recommend_jobs(resume_text, top_n=5):

    jobs = pd.read_csv(DATA_PATH)

    # Find available job information columns
    column_map = {col.lower(): col for col in jobs.columns}

    text_candidates = [
        "jobtitle",
        "jobdescription",
        "skills"
    ]

    available_columns = [
        column_map[col]
        for col in text_candidates
        if col in column_map
    ]

    if not available_columns:
        raise ValueError("No suitable job text columns found.")

    # Combine job title, description and skills
    jobs["combined_text"] = (
        jobs[available_columns]
        .fillna("")
        .astype(str)
        .agg(" ".join, axis=1)
    )

    # Remove empty job records
    jobs = jobs[jobs["combined_text"].str.strip() != ""]

    # Convert resume and jobs into TF-IDF features
    documents = jobs["combined_text"].tolist() + [resume_text]

    vectorizer = TfidfVectorizer(
        stop_words="english",
        max_features=5000
    )

    tfidf_matrix = vectorizer.fit_transform(documents)

    job_vectors = tfidf_matrix[:-1]
    resume_vector = tfidf_matrix[-1]

    # Calculate similarity scores
    scores = cosine_similarity(
        resume_vector,
        job_vectors
    ).flatten()

    # Select top matching jobs
    jobs["match_score"] = scores

    recommendations = jobs.nlargest(
        min(top_n, len(jobs)),
        "match_score"
    )

    return recommendations


if __name__ == "__main__":

    print("===== SmartHire Job Recommender =====")

    resume = input("\nEnter your resume text:\n")

    if resume.strip():

        results = recommend_jobs(resume)

        print("\n===== TOP 5 MATCHING JOBS =====")

        display_columns = [
            col for col in [
                "jobtitle",
                "company",
                "match_score"
            ]
            if col in results.columns
        ]

        print(results[display_columns].to_string(index=False))

    else:
        print("Please enter valid resume text.")