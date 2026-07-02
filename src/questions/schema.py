from typing import List
from pydantic import BaseModel, Field

class InterviewQuestion(BaseModel):
    question: str = Field(description="The interview question text")
    category: str = Field(description="Category of the question, e.g., 'Technical', 'Behavioral', 'Project-specific', 'General'")
    rationale: str = Field(description="Why this question is being asked based on the resume")
    suggested_answer: str = Field(description="A brief suggested or ideal answer from the candidate")

class QuestionSet(BaseModel):
    questions: List[InterviewQuestion] = Field(description="List of generated interview questions")
