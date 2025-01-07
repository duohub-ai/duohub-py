from typing import Dict, Any, Optional
import httpx
from ...environment import Environment
from ...exceptions import APIError

def delete_file_from_memory(
    memory_id: str,
    file_id: str,
    env: Optional[Environment] = None
) -> Dict[str, Any]:
    """Delete a file from a memory.
    
    Args:
        memory_id: ID of the memory to remove the file from
        file_id: ID of the file to remove
        env: Optional environment instance
        
    Returns:
        dict: Response data from the API
        
    Raises:
        ValueError: If invalid parameters are provided
        APIError: If the API request fails
        
    Note:
        This endpoint can only be used with memories created on or after 17-Dec-2024.
    """
    if env is None:
        env = Environment()
        
    if not memory_id:
        raise ValueError("memory_id is required")
        
    if not file_id:
        raise ValueError("file_id is required")
        
    payload = {
        "memoryID": memory_id,
        "fileID": file_id
    }
    
    client = httpx.Client(headers=env.headers)
    try:
        response = client.delete(
            env.get_full_url("/memories/delete-file"),
            params=payload
        )
        response.raise_for_status()
        return response.json()
    except httpx.HTTPStatusError as e:
        raise APIError(f"API request failed with status code {e.response.status_code}: {e.response.text}")
    except httpx.RequestError as e:
        raise APIError(f"An error occurred while requesting {e.request.url!r}.")



