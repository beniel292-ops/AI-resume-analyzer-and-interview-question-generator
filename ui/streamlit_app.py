import os
import sys
import tempfile
import hashlib
from pathlib import Path
import streamlit as st

# Add the project root to sys.path so we can import src modules
project_root = Path(__file__).resolve().parent.parent
sys.path.append(str(project_root))

from src.ingestion.loaders import load_pdf
from src.ingestion.chunker import chunk_document
from src.embeddings.embedder import embed_texts
from src.vectorstore.chroma_client import get_collection, add_chunks
from src.resume.analyzer import extract_resume
from src.questions.generator import generate_questions
from src.rag.pipeline import ask_rag_assistant

st.set_page_config(page_title="AI Resume Analyzer", layout="wide")

# Initialize Chat Sessions
if "chats" not in st.session_state or not isinstance(st.session_state["chats"].get("Chat 1"), dict):
    st.session_state["chats"] = {
        "Chat 1": {
            "messages": [],
            "resume_data": None,
            "questions": None,
            "last_hash": None
        }
    }
if "active_chat_id" not in st.session_state:
    st.session_state["active_chat_id"] = "Chat 1"

with st.sidebar:
    st.header("Chat Sessions")
    if st.button("➕ New Chat"):
        new_id = f"Chat {len(st.session_state['chats']) + 1}"
        st.session_state["chats"][new_id] = {
            "messages": [],
            "resume_data": None,
            "questions": None,
            "last_hash": None
        }
        st.session_state["active_chat_id"] = new_id
    
    st.markdown("---")
    for chat_id in list(st.session_state["chats"].keys()):
        # Highlight active chat
        btn_type = "primary" if chat_id == st.session_state["active_chat_id"] else "secondary"
        if st.button(f"💬 {chat_id}", key=f"btn_{chat_id}", use_container_width=True, type=btn_type):
            st.session_state["active_chat_id"] = chat_id
            st.rerun()

    st.markdown("---")
    if st.button("🗑️ Clear All Chats"):
        st.session_state["chats"] = {
            "Chat 1": {
                "messages": [],
                "resume_data": None,
                "questions": None,
                "last_hash": None
            }
        }
        st.session_state["active_chat_id"] = "Chat 1"
        st.rerun()

st.title("AI Resume Analyzer & Interview Generator")

active_chat_id = st.session_state["active_chat_id"]
active_chat = st.session_state["chats"][active_chat_id]

uploaded_file = st.file_uploader(f"Upload a Resume PDF for {active_chat_id}", type="pdf", key=f"uploader_{active_chat_id}")

if uploaded_file is not None:
    bytes_data = uploaded_file.getvalue()
    file_hash = hashlib.sha256(bytes_data).hexdigest()
    
    # Check if already ingested
    collection = get_collection()
    existing = collection.get(where={"file_hash": file_hash}, limit=1)
    
    # Save to temp file for processing
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
        tmp.write(bytes_data)
        tmp_path = Path(tmp.name)
        
    pages_data = []
    try:
        pages_data = load_pdf(tmp_path)
    except Exception as e:
        st.error(f"Failed to load PDF: {e}")
        os.remove(tmp_path)
        st.stop()
        
    # Ingestion step
    if existing and existing.get("ids"):
        st.info("PDF already ingested in ChromaDB (duplicate check passed).")
    else:
        with st.spinner("Ingesting PDF into ChromaDB..."):
            # Add file_hash to metadata
            for page in pages_data:
                page["metadata"]["file_hash"] = file_hash
                page["metadata"]["source"] = uploaded_file.name
                
            chunks_data = chunk_document(pages_data)
            if chunks_data:
                texts = [c["text"] for c in chunks_data]
                embeddings = embed_texts(texts)
                add_chunks(chunks_data, embeddings)
                st.success("Successfully chunked and stored in ChromaDB!")
            else:
                st.warning("No text could be extracted for chunking.")
                
    # Combine text for analysis
    full_text = "\n".join([page["text"] for page in pages_data])
    
    # Step 1: Resume Analysis
    if active_chat["resume_data"] is None or active_chat["last_hash"] != file_hash:
        with st.spinner("Analyzing Resume (this may take a minute with local models)..."):
            try:
                resume_data = extract_resume(full_text)
                active_chat["resume_data"] = resume_data
                active_chat["last_hash"] = file_hash
                # Clear previous questions if new resume
                active_chat["questions"] = None
            except Exception as e:
                st.error(f"Failed to extract resume data: {e}")
                
    # Cleanup temp file
    if os.path.exists(tmp_path):
        os.remove(tmp_path)

# Display Resume Data
if active_chat["resume_data"] is not None:
    resume_data = active_chat["resume_data"]
    st.subheader("Deep Resume Analysis")
    
    # Display Rating
    st.metric(label="Overall Competitiveness Rating", value=f"{resume_data.overall_rating}/10")
    st.caption(f"*Why? {resume_data.rating_explanation}*")
    st.markdown("---")
    
    st.markdown("### Professional Summary")
    st.info(resume_data.summary)
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("### Strengths")
        for strength in resume_data.strengths:
            st.markdown(f"- ✅ {strength}")
    with col2:
        st.markdown("### Areas for Improvement")
        for weakness in resume_data.weaknesses:
            st.markdown(f"- ⚠️ {weakness}")
            
    st.markdown("### ATS Compatibility Evaluation")
    st.warning(resume_data.ats_compatibility)
    
    st.markdown("---")
    
    col_left, col_right = st.columns(2)
    with col_left:
        st.markdown(f"**Name:** {resume_data.name}")
        st.markdown(f"**Contact Info:**\n{resume_data.contact_info}")
        
        st.markdown("### Skills")
        for skill_cat in resume_data.skills:
            st.markdown(f"- **{skill_cat.category}:** {', '.join(skill_cat.skills)}")
            
    with col_right:
        st.markdown("### Education")
        for edu in resume_data.education:
            st.markdown(f"- **{edu.degree}** at {edu.institution} ({edu.year or 'N/A'})")
            
        st.markdown("### Projects")
        for proj in resume_data.projects:
            st.markdown(f"- **{proj.name}**: {proj.description}")
            if proj.technologies:
                st.markdown(f"  *Tech: {', '.join(proj.technologies)}*")
                
    # Step 2: Question Generation Button
    st.markdown("---")
    if st.button("Generate Interview Questions", key=f"gen_q_{active_chat_id}"):
        with st.spinner("Generating targeted questions..."):
            try:
                questions = generate_questions(resume_data)
                active_chat["questions"] = questions
            except Exception as e:
                st.error(f"Failed to generate questions: {e}")
                
    # Display Questions
    if active_chat["questions"] is not None:
        st.subheader("Generated Interview Questions")
        for idx, q in enumerate(active_chat["questions"].questions):
            st.markdown(f"**Q{idx+1} ({q.category}):** {q.question}")
            st.caption(f"*Rationale: {q.rationale}*")
            with st.expander("Suggested Answer"):
                st.write(q.suggested_answer)

# --- Step 3: Interactive RAG Chat ---
st.markdown("---")
st.subheader(f"Ask the AI about this resume ({active_chat_id})")

active_messages = active_chat["messages"]

# Display chat messages from history
for message in active_messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# React to user input
if prompt := st.chat_input("Ask a question about the candidate..."):
    # Display user message
    st.chat_message("user").markdown(prompt)
    active_messages.append({"role": "user", "content": prompt})
    
    # Build a simple chat history string for context
    history_str = ""
    for msg in active_messages[-5:-1]:  # keep last few turns
        role = "You" if msg["role"] == "user" else "Assistant"
        history_str += f"{role}: {msg['content']}\n"
        
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                system_context = ""
                if active_chat["resume_data"] is not None:
                    system_context = f"Candidate Resume Analysis Data:\n{active_chat['resume_data'].model_dump_json(indent=2)}"
                    
                response = ask_rag_assistant(prompt, chat_history=history_str, system_context=system_context)
                st.markdown(response)
                active_messages.append({"role": "assistant", "content": response})
            except Exception as e:
                st.error(f"Error querying model: {e}")
