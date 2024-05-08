import logging
import os
import json

import http.client

# Get logger
logger = logging.getLogger(__name__)

SERP_API_KEY = os.getenv("SERP_API_KEY")


def get_links_topics(main_dir: str, topic: str) -> list:
    """Perform a search using the Serp API and extract text from each linked page."""
    conn = http.client.HTTPSConnection("google.serper.dev")
    payload = json.dumps({
        "q": topic,
        "num": 10,  # Retrieve a manageable number of results
        "page": 1
    })
    headers = {
        'X-API-KEY': SERP_API_KEY,
        'Content-Type': 'application/json'
    }
    conn.request("POST", "/search", payload, headers)
    res = conn.getresponse()
    if res.status != 200:
        logger.error(f"Failed to fetch search results: {res.reason}")
        return
    data = res.read()

    parsed_data = json.loads(data)

    links = [result['link'] for result in parsed_data.get('organic', [])]
    output_file = os.path.join(main_dir, "links.json")
    with open(output_file, "w") as f:
        json.dump(links, f, ensure_ascii=False)
    return links
