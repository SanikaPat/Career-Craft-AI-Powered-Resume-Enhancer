from flask import Flask, render_template, request, redirect, url_for
import os
import re
import pickle
import numpy as np
import pandas as pd
import google.generativeai as genai
from sentence_transformers import SentenceTransformer
from werkzeug.utils import secure_filename
from resume_ocr import process_resume

app = Flask(__name__)
UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

# Google Gemini API configuration
api_key = "AIzaSyCKSwn8VOO1fdPVVPGrzWJQGSNzUx5F9_M"  # Keep it secure!
genai.configure(api_key=api_key)
SkillEnhancerAI = genai.GenerativeModel('gemini-1.5-flash')

# Load datasets
dataset_path = pd.read_csv("/workspaces/codespaces-flask/Datasets/UpdatedResumeDataSet.csv")
dataset_path1 = pd.read_excel("/workspaces/codespaces-flask/Datasets/prompt_dataset.xlsx")

sbert_model = SentenceTransformer("all-MiniLM-L6-v2")

def predict_top_3_jobs(extracted_skills):
    """
    Predict the top 3 job titles based on extracted skills using Sentence-BERT embeddings.
    """
    if not extracted_skills:
        return ["No skills detected"]

    # Load the trained model and job title embeddings
    with open("/workspaces/codespaces-flask/model.pkl", "rb") as model_file:
        model = pickle.load(model_file)
    with open("/workspaces/codespaces-flask/job_titles.pkl", "rb") as titles_file:
        loaded_job_titles = pickle.load(titles_file)
    with open("/workspaces/codespaces-flask/job_titles_embeddings.pkl", "rb") as embeddings_file:
        loaded_job_titles_embeddings = pickle.load(embeddings_file)

    # Convert extracted skills into a single input string
    skillset_text = " ".join(extracted_skills)

    # Generate Sentence-BERT embedding for the extracted skillset
    skillset_embedding = sbert_model.encode([skillset_text])

    # Compute similarity between skillset and job titles
    similarity_scores = np.dot(loaded_job_titles_embeddings, skillset_embedding.T).flatten()
    
    # Get top 3 most similar job titles
    top_3_indices = np.argsort(similarity_scores)[-3:][::-1]
    top_3_job_titles = [loaded_job_titles[i] for i in top_3_indices]

    return top_3_job_titles


def enhance_skillset(extracted_skills, dataset_path):
    """
    Enhance skillset using Gemini AI.
    """
    prompt = f"""
    I have the following technical skill set: {extracted_skills}.
    Enhance these skills based on common job requirements from this dataset: {dataset_path}.
    Take this dataset into consideration as a format {dataset_path1}.

    Please do the following:
    1. Identify missing/relevant skills common in the dataset.
    2. Remove irrelevant/outdated skills.
    3. Reformat the skillset for clarity.
    4. Ensure the skillset focuses on the most relevant skills.
    5. Provide a structured, concise list of enhanced skills.
    """
    response = SkillEnhancerAI.generate_content(prompt).text
    return re.sub(r'\*', '', response).strip()

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/upload", methods=["GET", "POST"])
def upload():
    if request.method == "POST":
        if "resume" not in request.files:
            return redirect(request.url)

        file = request.files["resume"]
        if file.filename == "":
            return redirect(request.url)

        if file:
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config["UPLOAD_FOLDER"], filename)
            file.save(filepath)

            # Extract skills from resume
            extracted_skills = process_resume(filepath)

            # Predict top 3 job titles
            predicted_jobs = predict_top_3_jobs(extracted_skills)

            # Enhance skills using Gemini AI
            enhanced_skills = enhance_skillset(extracted_skills, dataset_path)

            return render_template("results.html", 
                                   extracted_skills=extracted_skills, 
                                   predicted_jobs=predicted_jobs, 
                                   enhanced_skills=enhanced_skills)

    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)
