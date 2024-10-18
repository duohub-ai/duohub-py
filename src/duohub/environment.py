import os
from .exceptions import AuthenticationError

class Environment:
    DEFAULT_BASE_URL = "https://api.duohub.ai"

    def __init__(self, api_key=None):
        self.api_key = api_key or os.getenv('DUOHUB_API_KEY')
        if not self.api_key:
            raise AuthenticationError("No API key provided. Set DUOHUB_API_KEY environment variable or pass api_key to the constructor.")
        
        self.base_url = self.DEFAULT_BASE_URL

    @property
    def headers(self):
        return {
            "accept": "application/json",
            "X-API-Key": self.api_key
        }

    def get_full_url(self, endpoint):
        return f"{self.base_url.rstrip('/')}/{endpoint.lstrip('/')}"