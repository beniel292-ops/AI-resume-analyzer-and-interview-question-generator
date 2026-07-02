import json
import re
from typing import Optional
from src.llm.qwen_client import generate_answer
from src.resume.schema import ResumeData
from utils.logger import get_logger

logger = get_logger(__name__)

def extract_resume(text: str) -> Optional[ResumeData]:
    """
    Extract structured data from a resume text.
    Retries up to 3 times if the JSON is malformed.
    """
    prompt = f"""
You are an expert resume analyzer. Extract and analyze the following information from the provided resume text:
- name: Full name of the candidate
- contact_info: Email, phone number, or links (like LinkedIn/GitHub)
- summary: A professional summary or objective for the candidate
- strengths: Key strengths and standout qualities based on the resume
- weaknesses: Potential weaknesses or areas for improvement (e.g., missing skills, employment gaps, vague descriptions)
- ats_compatibility: A brief evaluation of how well the resume is formatted for ATS (Applicant Tracking Systems) and its overall quality
- overall_rating: An integer rating from 1 to 10 evaluating the overall quality and competitiveness of the resume
- rating_explanation: Why this rating was given, detailing the main factors
- skills: Categorized list of skills (e.g., 'Programming Languages', 'Frameworks', 'Tools')
- projects: List of notable projects with name, description, and technologies used
- education: Educational background with degree, institution, and year

Resume Text:
\"\"\"
{text}
\"\"\"

Respond ONLY with a valid JSON object matching this schema:
{{
  "name": "string",
  "contact_info": "string",
  "summary": "string",
  "strengths": ["string"],
  "weaknesses": ["string"],
  "ats_compatibility": "string",
  "overall_rating": 0,
  "rating_explanation": "string",
  "skills": [
    {{"category": "string", "skills": ["string"]}}
  ],
  "projects": [
    {{"name": "string", "description": "string", "technologies": ["string"]}}
  ],
  "education": [
    {{"degree": "string", "institution": "string", "year": "string"}}
  ]
}}
Do not include markdown blocks, explanations, or any other text.
"""
    
    max_retries = 3
    for attempt in range(max_retries):
        try:
            logger.info(f"Attempt {attempt + 1}: Generating resume extraction...")
            response = generate_answer(prompt, format="json")
            
            # Clean up response if the model adds markdown code blocks
            if response.startswith("```json"):
                response = response[7:]
            if response.endswith("```"):
                response = response[:-3]
            response = response.strip()
            
            data = json.loads(response)
            
            # Validate with Pydantic
            resume_data = ResumeData(**data)
            return resume_data
            
        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse JSON on attempt {attempt + 1}: {e}")
            logger.error(f"Raw response: {response}")
        except Exception as e:
            logger.error(f"Validation or generation error on attempt {attempt + 1}: {e}")
            
    raise ValueError("Failed to extract valid resume data after 3 attempts. The model returned malformed output.")
