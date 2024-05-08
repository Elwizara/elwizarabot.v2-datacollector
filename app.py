import http.client
import json
import os
from bs4 import BeautifulSoup
import requests
from dotenv import load_dotenv
from openai import Client
from urllib.parse import urlparse

# Load environment variables from .env file
load_dotenv()

def tokenize(text):
    """ Helper function to tokenize the text into words using simple space-based splitting. """
    return text.split()

def safe_dir_name(url):
    """ Generate a safe directory name from a URL """
    parts = urlparse(url)
    return parts.netloc.replace('.', '_') + parts.path.replace('/', '_')


# Function to extract date from a given URL
def extract_text_from_url(url, output_dir):
    """Send a GET request to the URL and parse the HTML content to extract all visible text.
    Write the extracted text to a txt file in the specified directory."""
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raises an HTTPError for bad responses
        soup = BeautifulSoup(response.text, 'html.parser')
        text = soup.get_text(separator='\n', strip=True)  # Separate text by newlines

        # Define file path
        file_name = os.path.join(output_dir, 'extracted_text.txt')
        # Write text to file
        with open(file_name, 'w', encoding='utf-8') as file:
            file.write(text)
        print(f"Text successfully written to {file_name}")

        return text
    except requests.RequestException as e:
        print("HTTP Request failed:", e)
        return None


def send_data_to_GPT(text):
    """ Updated function to handle large text by splitting into chunks of manageable token size. """
    API_KEY = os.getenv("API_KEY")
    BASE_URL = os.getenv("BASE_URL")
    API_MODEL = os.getenv("API_MODEL")
    
    if not text:
        return "No text provided to process."

    system_prompt = """
        You will receive text from various sources.
        Your task is to focus solely on the main subject described in the text and ignore any irrelevant information.
        Please rewrite the main subject of the text in a clearer and more concise manner,
        ensuring that it provides a better understanding of the main topic without including unnecessary details.
        Your rewritten text should be well-written and accurately represent the main subject of the original text.
        """

    client = Client(api_key=API_KEY, base_url=BASE_URL)
    
    paragraphs = text.split('\n')
    chunk = ""
    output = ""
    for paragraph in paragraphs:
        if len(tokenize(chunk + paragraph)) < 1000:
            chunk += paragraph + '\n'
        else:
            messages = [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": chunk}
            ]
            response = client.chat.completions.create(
                model=API_MODEL,
                messages=messages,
                max_tokens=1000
            )
            # print(response.choices[0].message)
            output += response.choices[0].message.content + "\n"
            chunk = paragraph + '\n'  # Start new chunk
    
    # Process the last chunk if it exists
    if chunk:
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": chunk}
        ]
        response = client.chat.completions.create(
            model=API_MODEL,
            messages=messages,
            max_tokens=1000
        )
        output += response.choices[0].message.content + "\n"
        # print(response.choices[0].message)
    return output.strip()

def search_and_extract_text(query):
    """Perform a search using the Serp API and extract text from each linked page."""
    # Create main directory for the query
    main_dir = os.path.join(os.getcwd(), query.replace(' ', '_'))
    os.makedirs(main_dir, exist_ok=True)

    conn = http.client.HTTPSConnection("google.serper.dev")
    payload = json.dumps({
        "q": query,
        "num": 10,  # Retrieve a manageable number of results
        "page": 1
    })
    headers = {
        'X-API-KEY': os.getenv("SERP_API_KEY"),
        'Content-Type': 'application/json'
    }
    conn.request("POST", "/search", payload, headers)
    res = conn.getresponse()
    data = res.read()
    if res.status != 200:
        print(f"Failed to fetch search results: {res.reason}")
        return
    
    parsed_data = json.loads(data)

    links = [result['link'] for result in parsed_data.get('organic', [])]

    for link in links:
        link_dir = os.path.join(main_dir, safe_dir_name(link))
        os.makedirs(link_dir, exist_ok=True)
    
        text = extract_text_from_url(link, link_dir)
        if text:
            clear_text = send_data_to_GPT(text)
            if clear_text:
                # Define the filename using the first line of clear_text or a default name
                file_name = os.path.join(link_dir, 'processed_text.txt')
                with open(file_name, 'w', encoding='utf-8') as file:
                    file.write(clear_text)
                print(f"Processed text successfully written to {file_name}")
            else:
                print("No clear text was generated.")
        else:
            print("Failed to extract text from:", link)

    
# Example usage
search_and_extract_text("نادي الزمالك")
# send_data_to_GPT("hello")
