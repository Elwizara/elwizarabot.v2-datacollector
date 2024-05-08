import logging
import os
import traceback

from bs4 import BeautifulSoup
import requests
from urllib.parse import urlparse

# Get logger
logger = logging.getLogger(__name__)


def tokenize(text):
    """ Helper function to tokenize the text into words using simple space-based splitting. """
    return text.split()


def safe_file_name(url):
    """ Generate a safe directory name from a URL """
    parts = urlparse(url)
    return parts.netloc.replace('.', '_') + parts.path.replace('/', '_')


def extract_text_from_url(links: list, main_dir: str) -> list:
    result = []
    for link in links:
        """Send a GET request to the URL and parse the HTML content to extract all visible text.
        Write the extracted text to a txt file in the specified directory."""
        try:
            response = requests.get(link)
            if response.status_code != 200:
                logger.error(
                    f"Failed to extract text from {link}: {response.status_code}")
                continue
            soup = BeautifulSoup(response.text, 'html.parser')
            # Separate text by newlines
            text = soup.get_text(separator='\n', strip=True)

            # Define file path
            topic_dir = f"{main_dir}/data"
            os.makedirs(topic_dir, exist_ok=True)
            file_name = f"{main_dir}/data/{safe_file_name(link)}.txt"
            # Write text to file
            with open(file_name, 'w', encoding='utf-8') as file:
                file.write(text)
            logger.info(f"Text successfully written to {file_name}")
            result.append(file_name)
        except requests.RequestException as e:
            tb = traceback.format_exc()  # This will give you the stack trace.
            logger.error(f"Failed to extract text from {link}: {e}\n{tb}")
            continue
    return result
