from typing import Dict, Any, List, Optional
import httpx
from ...environment import Environment
from ...exceptions import APIError

def add_files_to_memory(
    memory_id: str,
    files: List[str],
    env: Optional[Environment] = None
) -> Dict[str, Any]:
    """Add files to a memory.
    
    Args:
        memory_id: ID of the memory to add the files to
        files: List of file IDs to add
        env: Optional environment instance
        
    Returns:
        dict: Response data from the API
        
    Raises:
        ValueError: If invalid parameters are provided
        APIError: If the API request fails
    """
    if env is None:
        env = Environment()
        
    if not memory_id:
        raise ValueError("memory_id is required")
        
    if not files or not isinstance(files, list):
        raise ValueError("files must be a non-empty list of file IDs")
        
    payload = {
        "memoryID": memory_id,
        "files": files
    }
    
    client = httpx.Client(headers=env.headers)
    try:
        response = client.post(
            env.get_full_url("/memories/add-files"),
            json=payload
        )
        response.raise_for_status()
        return response.json()["data"]
    except httpx.HTTPStatusError as e:
        raise APIError(f"API request failed with status code {e.response.status_code}: {e.response.text}")
    except httpx.RequestError as e:
        raise APIError(f"An error occurred while requesting {e.request.url!r}.")

