# Career Craft: AI- Powered Resume Enhancer

CareerCraft is an AI-powered tool that transforms job search and resume enhancement by converting PDF resumes into editable formats using technologies like OCR, machine learning, and NLP. It uses Deep Learning algorithms to match skill sets and keywords, boosting resume visibility within applicant tracking systems. CareerCraft also uses Large Language Models (LLMs) to generate personalized, data-driven resume enhancement recommendations, ensuring that resumes highlight domain-level skills and comply with industry best practices, enhancing candidate visibility, ranking, and employability.

# Features

1. User Interaction 
    - Input: User uploads a resume in PDF format.
    - Output: Receives extracted skillset, top 3 job titles, and an enhanced resume recommendation.

2. PDF to Text
    - Function: Converts scanned PDF resumes into machine-readable text.
    - Tools Used:
        - Tesseract OCR
        - Image Processing

3. Skillset Extraction
    - Function: Extracts relevant skills from resume text.
    - Techniques:
        - Natural Language Processing (NLP)
        - Named Entity Recognition (NER)
        - Keyword Extraction Algorithms
        
4. Job Title Recommendation
    Function: Suggests appropriate job titles based on extracted skills.
    Model Used: Siamese Semantic Similarity Model for matching skills to job titles.

5. Resume Enhancement
    Function: Enhances the resume content based on the extracted skillset by using LLMs.

# Contributers

Sanika Rozario (9572)
Sania Almeida (9582)
Sanika Patankar (9563)


# To run
```
flask --debug run
```
