from typing import Dict, Any, Optional
import httpx
from ...environment import Environment
from ...exceptions import APIError

def create_user(
    first_name: str,
    last_name: str,
    email: Optional[str] = None,
    user_id: Optional[str] = None,
    phone: Optional[str] = None,
    env: Optional[Environment] = None
) -> Dict[str, Any]:
    """Create a new user.
    
    Args:
        first_name: User's first name
        last_name: User's last name
        email: Optional user's email address
        user_id: Optional unique identifier for the user
        phone: Optional user's phone number
        env: Optional environment instance
    
    Returns:
        dict: Created user data containing:
            - id: User ID
            - firstName: First name
            - lastName: Last name
            - email: Email address
            - owner: Owner ID
            - userID: User ID
            - createdAt: Creation timestamp
            - updatedAt: Last update timestamp
        
    Raises:
        ValueError: If required fields are missing
        APIError: If the API request fails
    """
    if env is None:
        env = Environment()
    
    # Validate required fields
    if not first_name:
        raise ValueError("first_name is required")
    if not last_name:
        raise ValueError("last_name is required")

    # Build payload
    payload = {
        "firstName": first_name,
        "lastName": last_name,
        "email": email,
        "id": user_id,
        "phone": phone
    }
    
    # Remove None values
    payload = {k: v for k, v in payload.items() if v is not None}

    client = httpx.Client(headers=env.headers)
    try:
        response = client.post(
            env.get_full_url("/users/create"),
            json=payload
        )
        response.raise_for_status()
        return response.json()["data"]
    except httpx.HTTPStatusError as e:
        raise APIError(f"API request failed with status code {e.response.status_code}: {e.response.text}")
    except httpx.RequestError as e:
        raise APIError(f"An error occurred while requesting {e.request.url!r}.")
