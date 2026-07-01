from pathlib import Path
from utils.logger import get_logger
from pypdf import PdfReader
from docx import Document

logger = get_logger(__name__)


def load_txt(file_path: Path) -> list[dict]:
    """Read a .txt file and return its content with metadata."""
    try:
        text = file_path.read_text(encoding="utf-8")
        logger.info(f"Loaded {file_path.name} ({len(text)} characters)")
        return [{"text": text, "metadata": {"source": file_path.name, "page": 1}}]
    except FileNotFoundError:
        logger.error(f"File not found: {file_path}")
        raise
    except UnicodeDecodeError:
        logger.error(f"Could not decode {file_path} as UTF-8")
        raise


def load_pdf(file_path: Path) -> list[dict]:
    """Read a .pdf file and return page-by-page text with metadata."""
    try:
        reader = PdfReader(file_path)
        pages = []
        for i, page in enumerate(reader.pages):
            text = page.extract_text()
            if text:
                pages.append({
                    "text": text,
                    "metadata": {"source": file_path.name, "page": i + 1}
                })
        logger.info(f"Loaded {file_path.name} ({len(pages)} pages)")
        return pages
    except Exception as e:
        logger.error(f"Error loading PDF {file_path}: {e}")
        raise


def load_docx(file_path: Path) -> list[dict]:
    """Read a .docx file and return its content with metadata."""
    try:
        doc = Document(file_path)
        text = "\n".join([paragraph.text for paragraph in doc.paragraphs])
        logger.info(f"Loaded {file_path.name} ({len(text)} characters)")
        return [{"text": text, "metadata": {"source": file_path.name, "page": 1}}]
    except Exception as e:
        logger.error(f"Error loading DOCX {file_path}: {e}")
        raise


def load_document(file_path: Path) -> list[dict]:
    """Auto-detect file type and extract text with metadata."""
    ext = file_path.suffix.lower()
    if ext == ".txt":
        return load_txt(file_path)
    elif ext == ".pdf":
        return load_pdf(file_path)
    elif ext == ".docx":
        return load_docx(file_path)
    else:
        logger.warning(f"Unsupported file type: {ext} for file {file_path}")
        return []
