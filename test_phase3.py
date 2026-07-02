from src.resume.schema import ResumeData
from src.questions.generator import generate_questions
import json

def test_question_generator():
    resume_json = """
    {
      "name": "John Doe",
      "contact_info": "Email: john.doe@example.com | Phone: 555-1234\\nLinkedIn: linkedin.com/in/johndoe",
      "skills": [
        {
          "category": "Programming Languages",
          "skills": ["Python", "JavaScript", "SQL"]
        },
        {
          "category": "Frameworks",
          "skills": ["React", "Django", "FastAPI"]
        },
        {
          "category": "Tools",
          "skills": ["Git", "Docker", "AWS"]
        }
      ],
      "projects": [
        {
          "name": "Personal AI Assistant",
          "description": "- Built a local RAG assistant using Ollama, ChromaDB, and Streamlit.\\n- Used Python and Transformers for embeddings.",
          "technologies": ["Python", "Transformers"]
        },
        {
          "name": "E-commerce Platform",
          "description": "- Developed a scalable e-commerce backend.\\n- Technologies: Django, PostgreSQL, Redis.",
          "technologies": ["Django", "PostgreSQL", "Redis"]
        }
      ],
      "education": [
        {
          "degree": "B.S. in Computer Science",
          "institution": "University of Technology",
          "year": "2020"
        }
      ]
    }
    """
    resume_data = ResumeData(**json.loads(resume_json))
    
    print("Generating interview questions (this may take a few seconds)...")
    try:
        questions = generate_questions(resume_data)
        print("\n--- Generated Questions ---")
        print(questions.model_dump_json(indent=2))
        print("---------------------------\n")
        print("Phase 3 test successful!")
    except Exception as e:
        print(f"Generation failed: {e}")

if __name__ == "__main__":
    test_question_generator()
