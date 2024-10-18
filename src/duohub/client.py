import httpx
from .exceptions import APIError, ValidationError, MissingFieldError, InvalidDataTypeError
from .environment import Environment

class Duohub:
    def __init__(self, api_key=None):
        self.environment = Environment(api_key)
        self.client = httpx.Client(
            headers={
                **self.environment.headers,
                "Connection": "keep-alive",
                "Keep-Alive": "timeout=30, max=1000"
            },
            timeout=httpx.Timeout(30.0, connect=5.0)
        )

    def query(self, query: str, memoryID: str, assisted: bool = False):
        url = self.environment.get_full_url("/memory/")
        
        params = {
            "memoryID": memoryID,
            "query": query,
            "assisted": str(assisted).lower()
        }
        
        try:
            response = self.client.get(url, params=params)
            response.raise_for_status()
            data = response.json()
            
            # Basic validation of the response
            if not isinstance(data, dict):
                raise InvalidDataTypeError("API response is not a dictionary")
            
            required_fields = ['result', 'status']  # Add any other required fields
            for field in required_fields:
                if field not in data:
                    raise MissingFieldError(f"Required field '{field}' is missing from the API response")
            
            return data
        except httpx.HTTPStatusError as e:
            raise APIError(f"API request failed with status code {e.response.status_code}: {e.response.text}")
        except httpx.RequestError as e:
            raise APIError(f"An error occurred while requesting {e.request.url!r}.")
        except (ValidationError, MissingFieldError, InvalidDataTypeError) as e:
            raise APIError(f"API response validation failed: {str(e)}")
        
        return response.json()

    def __del__(self):
        if hasattr(self, 'client'):
            self.client.close()
