import os
from fpdf import FPDF
from src.ingestion.loaders import load_pdf
from src.resume.analyzer import extract_resume

def generate_sample_pdf(filepath: str):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    resume_text = """
John Doe
Email: john.doe@example.com | Phone: 555-1234
LinkedIn: linkedin.com/in/johndoe

Skills:
Programming Languages: Python, JavaScript, SQL
Frameworks: React, Django, FastAPI
Tools: Git, Docker, AWS

Experience & Projects:
Personal AI Assistant
- Built a local RAG assistant using Ollama, ChromaDB, and Streamlit.
- Used Python and Transformers for embeddings.

E-commerce Platform
- Developed a scalable e-commerce backend.
- Technologies: Django, PostgreSQL, Redis.

Education:
B.S. in Computer Science
University of Technology
2020
"""
    for line in resume_text.split("\n"):
        pdf.cell(200, 10, txt=line, ln=1, align="L")
    pdf.output(filepath)

if __name__ == "__main__":
    from pathlib import Path
    pdf_path = Path("sample_resume.pdf")
    print("Generating sample PDF...")
    generate_sample_pdf(str(pdf_path))
    
    print("Loading PDF...")
    pages = load_pdf(pdf_path)
    text = "\n".join([page["text"] for page in pages])
    
    print("Extracting resume data (this may take a few seconds)...")
    try:
        resume_data = extract_resume(text)
        print("\n--- Extracted Resume Data ---")
        print(resume_data.model_dump_json(indent=2))
        print("-----------------------------\n")
        print("Phase 2 test successful!")
    except Exception as e:
        print(f"Extraction failed: {e}")
