from predict_category import predict_category
from job_recommender import recommend_jobs
from skill_gap import analyze_skill_gap


def run_smarthire():

    print("=" * 50)
    print("          WELCOME TO SMARTHIRE AI")
    print("=" * 50)

    # Get resume
    resume_text = input("\nPaste your complete resume text:\n")

    if not resume_text.strip():
        print("Please enter valid resume text.")
        return

    # Feature 1: Category prediction
    print("\n" + "=" * 50)
    print("1. RESUME CATEGORY PREDICTION")
    print("=" * 50)

    category = predict_category(resume_text)
    print("Predicted Job Category:", category)

    # Feature 2: Job recommendations
    print("\n" + "=" * 50)
    print("2. TOP 5 JOB RECOMMENDATIONS")
    print("=" * 50)

    jobs = recommend_jobs(resume_text, top_n=5)

    display_columns = [
        col for col in ["jobtitle", "company", "match_score"]
        if col in jobs.columns
    ]

    print(jobs[display_columns].to_string(index=False))

    # Feature 3: Skill gap analysis
    print("\n" + "=" * 50)
    print("3. SKILL GAP ANALYSIS")
    print("=" * 50)

    job_description = input(
        "\nEnter your target job description and required skills:\n"
    )

    if not job_description.strip():
        print("Please enter a valid job description.")
        return

    result = analyze_skill_gap(resume_text, job_description)

    print("\nCandidate Skills:", result["candidate_skills"])
    print("Required Skills:", result["required_skills"])
    print("Matched Skills:", result["matched_skills"])
    print("Missing Skills:", result["missing_skills"])

    print(
        "\nSkill Match Percentage:",
        str(result["match_percentage"]) + "%"
    )

    print("\n" + "=" * 50)
    print("       SMARTHIRE ANALYSIS COMPLETED!")
    print("=" * 50)


if __name__ == "__main__":
    run_smarthire()