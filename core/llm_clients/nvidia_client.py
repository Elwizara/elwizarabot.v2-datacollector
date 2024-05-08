import logging
import traceback
from openai import Client
from core.llm_clients.llm_client_base import LLM_CLIENT_BASE

logger = logging.getLogger(__name__)


class NvidiaClient(LLM_CLIENT_BASE):
    def __init__(self, API_MODEL: str, API_KEY: str, MAX_TOKENS: int):
        self.API_MODEL = API_MODEL
        self.BASE_URL = "https://integrate.api.nvidia.com/v1"
        self.API_KEY = API_KEY
        self.MAX_TOKENS = MAX_TOKENS

    def request(self, system_message: str, message: str):
        try:
            messages = [
                {
                    "role": "user",
                    "content": f"""{system_message}
                    ----------------------------------------
                    user-request: {message}"""
                }
            ]
            logger.info(f"Requesting Nvidia with messages: {messages}")

            client = Client(api_key=self.API_KEY, base_url=self.BASE_URL)
            response = client.chat.completions.create(
                model=self.API_MODEL,
                messages=messages,
                max_tokens=self.MAX_TOKENS
            )
            if not response:
                logger.error("No response from Nvidia")
                return None
            if response.choices.__len__ == 0:
                logger.error("No choices in response from Nvidia")
                return None
            if not response.choices[0].message.content:
                logger.error("Empty response from Nvidia")
                return None
            logger.info(
                f"Response from Nvidia: {response.choices[0].message.content}")
            return response.choices[0].message.content
        except Exception as e:
            tb = traceback.format_exc()  # This will give you the stack trace.
            logger.error(f"Exception: {e}\n{tb}")
            return None
