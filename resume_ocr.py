import os
import cv2
import numpy as np
import pytesseract
import re
import pandas as pd
from pdf2image import convert_from_path

# Load skills dataset
SKILLS_DATASET_PATH = "/workspaces/codespaces-flask/skills_dataset.xlsx"

def load_skills():
    """Load skills from the dataset and return a list of normalized skills."""
    if os.path.exists(SKILLS_DATASET_PATH):
        skill_data = pd.read_excel(SKILLS_DATASET_PATH)
        return skill_data['Skills'].str.lower().unique().tolist()
    return []

skills_list = load_skills()

# Deskew function
def deskew(image):
    """Deskew an image using OpenCV."""
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    gray = cv2.bitwise_not(gray)
    coords = np.column_stack(np.where(gray > 0))
    angle = cv2.minAreaRect(coords)[-1]

    if angle < -45:
        angle = -(90 + angle)
    else:
        angle = -angle

    (h, w) = image.shape[:2]
    center = (w // 2, h // 2)
    M = cv2.getRotationMatrix2D(center, angle, 1.0)
    rotated = cv2.warpAffine(image, M, (w, h), flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE)

    return rotated

# Extract text from an image
def extract_text_from_image(image):
    """Extract text from an image using Tesseract OCR."""
    return pytesseract.image_to_string(image)

# Process PDF and extract text
def extract_text_from_pdf(pdf_filename):
    """Convert a PDF to images, preprocess them, and extract text."""
    if not os.path.exists(pdf_filename):
        return None

    pages = convert_from_path(pdf_filename)
    extracted_text = []

    for page in pages:
        preprocessed_image = deskew(np.array(page))
        text = extract_text_from_image(preprocessed_image)
        extracted_text.append(text)

    return "\n".join(extracted_text)

# Extract skills from text
def extract_skills_from_text(text, skills_list):
    """Extract relevant skills from text based on a predefined skills dataset."""
    skill_headers = ['SKILLS', 'TECHNICAL SKILLS', 'SKILL SET', 'EXPERTISE']
    skills_section = None

    for header in skill_headers:
        if header.lower() in text.lower():
            skills_section = text.lower().split(header.lower(), 1)[1]
            break

    extracted_skills = []
    if skills_section:
        lines = skills_section.splitlines()
        for line in lines:
            if re.search(r'^[A-Z][A-Z\s]*$', line.strip()):
                break
            line = re.sub(r'[^\w\s]', '', line).strip().lower()

            for skill in skills_list:
                skill_pattern = re.escape(skill)
                if re.search(r'\b' + skill_pattern + r'\b', line, re.IGNORECASE):
                    extracted_skills.append(skill)

    return list(set(extracted_skills))

# Main function to process resume and extract skills
def process_resume(pdf_filename):
    """Extract text from the resume and identify relevant skills."""
    resume_text = extract_text_from_pdf(pdf_filename)
    skills_found = extract_skills_from_text(resume_text, skills_list)
    return skills_found
