SmartHire – AI-Powered Resume Analysis & Job Recommendation System

SmartHire is a machine learning-based application that helps job seekers identify suitable career opportunities by analyzing their resumes. It predicts job categories, recommends relevant job opportunities, and identifies missing skills to help candidates improve their employability.

Key Features

1. Resume Category Prediction

- Analyzes uploaded resume content.
- Uses supervised machine learning to predict a suitable job category.
- Uses TF-IDF text vectorization.

2. Top 5 Job Recommendations

- Compares resume content with job descriptions.
- Uses TF-IDF and cosine similarity.
- Recommends the five most relevant job opportunities.

3. Skill Gap Analysis

- Extracts candidate skills from the resume.
- Compares candidate skills with job-required skills.
- Identifies matched and missing skills.
- Calculates a skill match percentage.

Technologies Used

Technology| Purpose
Python| Main programming language
Streamlit| Interactive web dashboard
Pandas| Data processing
NumPy| Numerical operations
Scikit-learn| Machine learning
TF-IDF| Text feature extraction
Cosine Similarity| Resume-job matching
PyPDF| PDF resume extraction
python-docx| DOCX resume extraction

Project Structure

SmartHire_New/
│
├── app.py
├── requirements.txt
├── README.md
├── .gitignore
│
├── ui/
│   ├── __init__.py
│   ├── backend.py
│   ├── components.py
│   ├── styles.css
│   └── views.py
│
├── data/
│   ├── raw/
│   └── processed/
│
├── src/
│   ├── data/
│   ├── models/
│   ├── train_model.py
│   ├── predict_category.py
│   ├── job_recommender.py
│   ├── skill_gap.py
│   └── smarthire.py
│
└── venv/

Installation and Execution

Step 1: Clone the repository

git clone YOUR_GITHUB_REPOSITORY_URL
cd SmartHire_New

Step 2: Install dependencies

pip install -r requirements.txt

Step 3: Run the application

streamlit run app.py

The SmartHire dashboard will open in your browser.

Dataset

The project uses resume and job-description datasets for model training, text analysis, and job recommendations.

- Resume dataset: UpdatedResumeDataSet.csv
- Job dataset: naukri_com-job_sample.csv

Please check and follow the original dataset licenses and usage conditions before redistributing them.

Application Screenshots

Add actual application screenshots here:

- Dashboard
- Resume Upload
- Role Prediction
- Job Recommendations
- Skill Gap Analysis

Project Objective

The main objective of SmartHire is to make job searching more intelligent by connecting candidate profiles with relevant job opportunities and helping candidates understand which skills they need to improve.

Future Enhancements

- Advanced resume parsing.
- More accurate skill extraction.
- Personalized learning recommendations.
- Integration with live job portals.
- Improved machine learning models.

Author

Kusuma

Computer Science Student | Aspiring AI/ML Engineer

---

SmartHire – Turning resumes into career opportunities.