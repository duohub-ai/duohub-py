from typing import Dict, Any, Optional
import httpx
from ...environment import Environment
from ...exceptions import APIError

def delete_user(
    user_id: str,
    env: Optional[Environment] = None
) -> Dict[str, Any]:
    """Delete a user by ID.
    
    Args:
        user_id: Unique identifier of the user to delete
        env: Optional environment instance
    
    Returns:
        dict: Response containing status and success message
        
    Raises:
        ValueError: If user_id is not provided
        APIError: If the API request fails
    """
    if env is None:
        env = Environment()
    
    if not user_id:
        raise ValueError("user_id is required")

    client = httpx.Client(headers=env.headers)
    try:
        response = client.delete(
            env.get_full_url(f"/users/delete/{user_id}")
        )
        response.raise_for_status()
        return response.json()
    except httpx.HTTPStatusError as e:
        if e.response.status_code == 404:
            raise APIError("User not found")
        raise APIError(f"API request failed with status code {e.response.status_code}: {e.response.text}")
    except httpx.RequestError as e:
        raise APIError(f"An error occurred while requesting {e.request.url!r}.")
