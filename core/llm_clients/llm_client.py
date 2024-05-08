import logging
import os
from dotenv import load_dotenv

from core.llm_clients.nvidia_client import NvidiaClient
from core.llm_clients.llm_client_base import LLM_CLIENT_BASE

# Get logger
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

API_CLIENT = os.getenv("API_CLIENT")
API_KEY = os.getenv("API_KEY")
BASE_URL = os.getenv("BASE_URL")
API_MODEL = os.getenv("API_MODEL")
MAX_TOKENS = int(os.getenv("MAX_TOKENS"))


class LLMClient:
    def __init__(self):
        self.API_CLIENT = API_CLIENT
        self.API_KEY = API_KEY
        self.BASE_URL = BASE_URL
        self.API_MODEL = API_MODEL
        self.MAX_TOKENS = MAX_TOKENS

    def GetClient(self,
                  API_CLIENT,
                  API_MODEL,
                  API_KEY,
                  MAX_TOKENS) -> LLM_CLIENT_BASE:
        if API_CLIENT == "nvidia":
            return NvidiaClient(API_MODEL, API_KEY, MAX_TOKENS)
        else:
            logger.error("Invalid API client")
            return LLM_CLIENT_BASE()

    def GetCoderClient(self) -> LLM_CLIENT_BASE:
        return self.GetClient(self.API_CLIENT,
                              self.API_MODEL,
                              self.API_KEY,
                              self.MAX_TOKENS)
