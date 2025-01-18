from typing import Dict, Any, Optional, List
import httpx
from ...environment import Environment
from ...exceptions import APIError

def create_session(
    customer_user_id: Optional[str] = None,
    session_id: Optional[str] = None,
    metadata: Optional[List[Dict[str, str]]] = None,
    env: Optional[Environment] = None
) -> Dict[str, Any]:
    """Create a new session.
    
    Args:
        customer_user_id: Optional ID of the customer user
        session_id: Optional unique identifier for the session
        metadata: Optional list of metadata key-value pairs
                 Example: [{"key": "source", "value": "web"}]
        env: Optional environment instance
    
    Returns:
        dict: Created session data containing:
            - id: Session ID
            - userID: User ID
            - customerUserID: Customer user ID
            - metadata: List of metadata
            - createdAt: Creation timestamp
            - updatedAt: Last update timestamp
            - deletedAt: Deletion timestamp (if applicable)
            - endedAt: Session end timestamp (if applicable)
        
    Raises:
        APIError: If the API request fails
    """
    if env is None:
        env = Environment()
    
    # Build payload
    payload = {}
    if customer_user_id:
        payload["customerUserID"] = customer_user_id
    if session_id:
        payload["id"] = session_id
    if metadata:
        payload["metadata"] = metadata

    client = httpx.Client(headers=env.headers)
    try:
        response = client.post(
            env.get_full_url("/sessions/create"),
            json=payload
        )
        response.raise_for_status()
        return response.json()["data"]
    except httpx.HTTPStatusError as e:
        raise APIError(f"API request failed with status code {e.response.status_code}: {e.response.text}")
    except httpx.RequestError as e:
        raise APIError(f"An error occurred while requesting {e.request.url!r}.")