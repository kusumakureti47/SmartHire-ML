import joblib
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
MODEL_PATH = PROJECT_ROOT / "src" / "models"

MODEL_FILE = MODEL_PATH / "resume_classifier.pkl"
VECTORIZER_FILE = MODEL_PATH / "resume_classifier_vectorizer.pkl"


def predict_category(resume_text):

    model = joblib.load(MODEL_FILE)
    vectorizer = joblib.load(VECTORIZER_FILE)

    resume_text = resume_text.lower().strip()

    resume_vector = vectorizer.transform([resume_text])

    prediction = model.predict(resume_vector)

    return prediction[0]


if __name__ == "__main__":

    print("===== SmartHire Resume Category Predictor =====")

    resume = input("\nPaste your resume text here:\n")

    if resume.strip():
        category = predict_category(resume)

        print("\nPredicted Job Category:")
        print(category)
    else:
        print("Please enter valid resume text.")