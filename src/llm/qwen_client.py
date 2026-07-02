import json
import urllib.request
from config.settings import LLM_MODEL_NAME
from utils.logger import get_logger

logger = get_logger(__name__)


def get_llm():
    """No longer needed to load weights into VRAM. Handled by Ollama."""
    pass


def generate_answer(prompt: str, format: str = None) -> str:
    """Send the prompt to the local Ollama API."""
    logger.info(f"Sending prompt to Ollama ({LLM_MODEL_NAME})...")
    
    url = "http://localhost:11434/api/generate"
    
    data = {
        "model": LLM_MODEL_NAME,
        "prompt": prompt,
        "stream": False
    }
    if format == "json":
        data["format"] = "json"
    
    req = urllib.request.Request(
        url, 
        data=json.dumps(data).encode("utf-8"), 
        headers={"Content-Type": "application/json"}
    )
    
    try:
        with urllib.request.urlopen(req) as response:
            result = json.loads(response.read().decode("utf-8"))
            return result.get("response", "Error: No response found.")
    except urllib.error.URLError:
        error_msg = (
            "Error: Could not connect to Ollama. \n"
            "Please make sure you have installed Ollama and run:\n"
            f"    ollama run {LLM_MODEL_NAME}\n"
            "in a separate terminal window."
        )
        logger.error(error_msg)
        return error_msg
    except Exception as e:
        logger.error(f"Ollama generation failed: {e}")
        return f"Error: {e}"
