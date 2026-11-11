import re


SKILLS = [
    "python", "java", "c++", "sql", "machine learning",
    "deep learning", "artificial intelligence",
    "data analysis", "data science", "pandas", "numpy",
    "scikit-learn", "tensorflow", "pytorch",
    "nlp", "computer vision", "excel", "power bi",
    "tableau", "html", "css", "javascript",
    "react", "node.js", "flask", "django",
    "streamlit", "git", "aws", "azure",
    "communication", "problem solving"
]


def find_skills(text):
    text = text.lower()
    found = []

    for skill in SKILLS:
        pattern = r"(?<!\w)" + re.escape(skill) + r"(?!\w)"

        if re.search(pattern, text):
            found.append(skill)

    return sorted(set(found))


def analyze_skill_gap(resume_text, job_description):

    candidate_skills = set(find_skills(resume_text))
    required_skills = set(find_skills(job_description))

    matched_skills = candidate_skills.intersection(
        required_skills
    )

    missing_skills = required_skills - candidate_skills

    if required_skills:
        match_percentage = (
            len(matched_skills) / len(required_skills)
        ) * 100
    else:
        match_percentage = 0

    return {
        "candidate_skills": sorted(candidate_skills),
        "required_skills": sorted(required_skills),
        "matched_skills": sorted(matched_skills),
        "missing_skills": sorted(missing_skills),
        "match_percentage": round(match_percentage, 2)
    }


if __name__ == "__main__":

    print("===== SmartHire Skill Gap Analysis =====")

    resume = input("\nEnter your resume text:\n")
    job = input("\nEnter the target job description:\n")

    if resume.strip() and job.strip():

        result = analyze_skill_gap(resume, job)

        print("\nCandidate Skills:", result["candidate_skills"])
        print("Required Skills:", result["required_skills"])
        print("Matched Skills:", result["matched_skills"])
        print("Missing Skills:", result["missing_skills"])

        print(
            "\nSkill Match Percentage:",
            str(result["match_percentage"]) + "%"
        )

    else:
        print("Please enter both resume and job description.")