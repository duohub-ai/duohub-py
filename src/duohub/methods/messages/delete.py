from typing import Dict, Any, Optional
import httpx
from ...environment import Environment
from ...exceptions import APIError

def delete_message(
    message_id: str,
    env: Optional[Environment] = None
) -> Dict[str, Any]:
    """Delete a message by ID.
    
    Args:
        message_id: ID of the message to delete
        env: Optional environment instance
    
    Returns:
        dict: Response containing status and success message
        
    Raises:
        ValueError: If message_id is not provided
        APIError: If the API request fails
    """
    if env is None:
        env = Environment()
    
    if not message_id:
        raise ValueError("message_id is required")

    client = httpx.Client(headers=env.headers)
    try:
        response = client.delete(
            env.get_full_url(f"/messages/delete/{message_id}")
        )
        response.raise_for_status()
        return response.json()
    except httpx.HTTPStatusError as e:
        if e.response.status_code == 404:
            raise APIError("Message not found")
        raise APIError(f"API request failed with status code {e.response.status_code}: {e.response.text}")
    except httpx.RequestError as e:
        raise APIError(f"An error occurred while requesting {e.request.url!r}.")