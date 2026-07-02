from typing import List, Optional
from pydantic import BaseModel, Field

class Skill(BaseModel):
    category: str = Field(description="The category of the skill, e.g., 'Programming Languages', 'Frameworks', 'Tools'")
    skills: List[str] = Field(description="List of skills in this category")

class Project(BaseModel):
    name: str = Field(description="Name of the project")
    description: str = Field(description="Brief description of what the project is about and what was achieved")
    technologies: List[str] = Field(description="List of technologies used in the project")

class Education(BaseModel):
    degree: str = Field(description="Degree obtained or being pursued")
    institution: str = Field(description="Name of the educational institution")
    year: Optional[str] = Field(None, description="Year of graduation or attendance period")

class ResumeData(BaseModel):
    name: str = Field(description="Full name of the candidate")
    contact_info: str = Field(description="Email, phone number, or links (like LinkedIn/GitHub)")
    summary: str = Field(description="A professional summary or objective for the candidate")
    strengths: List[str] = Field(description="Key strengths and standout qualities based on the resume")
    weaknesses: List[str] = Field(description="Potential weaknesses or areas for improvement")
    ats_compatibility: str = Field(description="A brief evaluation of how well the resume is formatted for ATS (Applicant Tracking Systems) and its overall quality")
    overall_rating: int = Field(description="A rating from 1 to 10 evaluating the overall quality and competitiveness of the resume")
    rating_explanation: str = Field(description="Why this rating was given, detailing the main factors")
    skills: List[Skill] = Field(default_factory=list, description="Categorized list of skills")
    projects: List[Project] = Field(default_factory=list, description="List of notable projects")
    education: List[Education] = Field(default_factory=list, description="Educational background")
