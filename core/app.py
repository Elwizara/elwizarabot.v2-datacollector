import logging
import os
import traceback
from dotenv import load_dotenv

from core.llm_clients.llm_client import LLMClient

from core.websearch.serp_api import get_links_topics
from core.websearch.web_scraper import extract_text_from_url
from core.websearch.summary_client import summarize_text_llm

# Get logger
logger = logging.getLogger(__name__)

# Load environment variables from .env file
load_dotenv()


def App(topic: str) -> dict:
    try:
        # Create main directory for the query
        topic_dir = topic.replace(' ', '_').replace('/', '_')
        main_dir = os.path.join(os.getcwd(), f"data/{topic_dir}")
        os.makedirs(main_dir, exist_ok=True)
        links = get_links_topics(main_dir, topic)
        if not links:
            logger.error("No links found")
            return
        # collect data from the links
        file_names = extract_text_from_url(links, main_dir)
        if not file_names:
            logger.error("No data collected")
            return
        # summarize the data by llm-client
        code_client = LLMClient().GetCoderClient()
        for file_name in file_names:
            summary = summarize_text_llm(code_client, file_name)
            with open(file_name.replace(".txt", "_summary.txt"), 'w') as f:
                f.write(summary)
        return "DONE"
    except Exception as e:
        tb = traceback.format_exc()  # This will give you the stack trace.
        logger.error(f"Exception: {e}\n{tb}")
