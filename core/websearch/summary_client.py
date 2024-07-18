import logging
import os

from core.llm_clients.llm_client_base import LLM_CLIENT_BASE

# Get logger
logger = logging.getLogger(__name__)

API_KEY = os.getenv("API_KEY")
BASE_URL = os.getenv("BASE_URL")
API_MODEL = os.getenv("API_MODEL")


def summarize_text_llm(llm_client: LLM_CLIENT_BASE, file_name: str) -> str:
    """ Updated function to handle large text by splitting into chunks of manageable token size. """
    with open(file_name, 'r') as file:
        text = file.read()
    if not text:
        return "No text provided to process."

    system_prompt = """You will receive text from various sources.
Your task is to focus solely on the main subject described in the text and ignore any irrelevant information.
Please rewrite the main subject of the text in a clearer and more concise manner,
ensuring that it provides a better understanding of the main topic without including unnecessary details.
Your rewritten text should be well-written and accurately represent the main subject of the original text.
"""
    chunk_size = 1000
    final_summary = ""
    all_words = text.split()
    for start_index in range(0, len(all_words), chunk_size):
        chunk = all_words[start_index:start_index + chunk_size]
        chunk_text = " ".join(chunk)
        text_summary = llm_client.request(system_prompt, chunk_text)
        if not text_summary:
            logger.error("Failed to generate summary for chunk.")
            return None
        final_summary += text_summary
    return final_summary
