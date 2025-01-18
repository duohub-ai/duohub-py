from typing import Dict, Any, Optional
import httpx
from ...environment import Environment
from ...exceptions import APIError

def get_user(
    user_id: str,
    env: Optional[Environment] = None
) -> Dict[str, Any]:
    """Retrieve a single user by ID.
    
    Args:
        user_id: Unique identifier of the user to retrieve
        env: Optional environment instance
    
    Returns:
        dict: User data containing id, firstName, lastName, email, owner,
              createdAt, and updatedAt
        
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
        response = client.get(
            env.get_full_url(f"/users/get/{user_id}")
        )
        response.raise_for_status()
        return response.json()["data"]
    except httpx.HTTPStatusError as e:
        if e.response.status_code == 404:
            raise APIError("User not found")
        raise APIError(f"API request failed with status code {e.response.status_code}: {e.response.text}")
    except httpx.RequestError as e:
        raise APIError(f"An error occurred while requesting {e.request.url!r}.")