from typing import Dict, Any, Optional
import httpx
from ...environment import Environment
from ...exceptions import APIError

def get_session(
    session_id: str,
    env: Optional[Environment] = None
) -> Dict[str, Any]:
    """Retrieve a single session by ID.
    
    Args:
        session_id: ID of the session to retrieve
        env: Optional environment instance
    
    Returns:
        dict: Session data containing:
            - id: Session ID
            - userID: User ID
            - customerUserID: Customer user ID
            - metadata: List of metadata key-value pairs
            - createdAt: Creation timestamp
            - updatedAt: Last update timestamp
            - deletedAt: Deletion timestamp (if applicable)
            - endedAt: Session end timestamp (if applicable)
        
    Raises:
        ValueError: If session_id is not provided
        APIError: If the API request fails
    """
    if env is None:
        env = Environment()
    
    if not session_id:
        raise ValueError("session_id is required")

    client = httpx.Client(headers=env.headers)
    try:
        response = client.get(
            env.get_full_url(f"/sessions/get/{session_id}")
        )
        response.raise_for_status()
        return response.json()["data"]
    except httpx.HTTPStatusError as e:
        if e.response.status_code == 404:
            raise APIError("Session not found")
        raise APIError(f"API request failed with status code {e.response.status_code}: {e.response.text}")
    except httpx.RequestError as e:
        raise APIError(f"An error occurred while requesting {e.request.url!r}.")