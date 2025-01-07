from typing import Dict, Any, Optional
import httpx
from ...environment import Environment
from ...exceptions import APIError

def start_ingestion(
    memory_id: str,
    env: Optional[Environment] = None
) -> Dict[str, Any]:
    """Start ingestion for a memory.
    
    Args:
        memory_id: ID of the memory to start ingestion for
        env: Optional environment instance
        
    Returns:
        dict: Response data containing status, message and data
        
    Raises:
        ValueError: If memory_id is not provided
        APIError: If the API request fails
    """
    if env is None:
        env = Environment()
        
    if not memory_id:
        raise ValueError("memory_id is required")
        
    payload = {
        "memoryID": memory_id
    }
    
    client = httpx.Client(headers=env.headers)
    try:
        response = client.post(
            env.get_full_url("/memories/start-ingestion"),
            json=payload
        )
        response.raise_for_status()
        return response.json()
    except httpx.HTTPStatusError as e:
        raise APIError(f"API request failed with status code {e.response.status_code}: {e.response.text}")
    except httpx.RequestError as e:
        raise APIError(f"An error occurred while requesting {e.request.url!r}.")
