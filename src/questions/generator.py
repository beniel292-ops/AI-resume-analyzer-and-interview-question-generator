import json
from typing import Optional
from src.llm.qwen_client import generate_answer
from src.questions.schema import QuestionSet
from src.resume.schema import ResumeData
from utils.logger import get_logger

logger = get_logger(__name__)

def generate_questions(resume_data: ResumeData) -> Optional[QuestionSet]:
    """
    Generate personalized interview questions based on extracted resume data.
    Retries up to 3 times if the JSON is malformed.
    """
    import time
    
    prompt = f"""
You are an expert technical interviewer. Based on the following resume data, generate 4 to 6 personalized interview questions for the candidate.
Ensure a mix of categories: Technical, Behavioral, Project-specific, and General.
Make these questions different from any previous generations if possible. (Generation ID: {time.time()})

Resume Data:
{resume_data.model_dump_json(indent=2)}

Respond ONLY with a valid JSON object matching this schema:
{{
  "questions": [
    {{
      "question": "string",
      "category": "string",
      "rationale": "string",
      "suggested_answer": "string"
    }}
  ]
}}
Do not include markdown blocks, explanations, or any other text.
"""
    
    max_retries = 3
    for attempt in range(max_retries):
        try:
            logger.info(f"Attempt {attempt + 1}: Generating interview questions...")
            response = generate_answer(prompt, format="json")
            
            # Clean up response if the model adds markdown code blocks
            if response.startswith("```json"):
                response = response[7:]
            if response.endswith("```"):
                response = response[:-3]
            response = response.strip()
            
            data = json.loads(response)
            
            # Validate with Pydantic
            question_set = QuestionSet(**data)
            return question_set
            
        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse JSON on attempt {attempt + 1}: {e}")
            logger.error(f"Raw response: {response}")
        except Exception as e:
            logger.error(f"Validation or generation error on attempt {attempt + 1}: {e}")
            
    raise ValueError("Failed to generate valid interview questions after 3 attempts. The model returned malformed output.")
