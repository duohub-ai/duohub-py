from typing import Dict, Any, Optional, Literal
import httpx
from ...environment import Environment
from ...exceptions import APIError

MessageRole = Literal['norole', 'system', 'assistant', 'user', 'function', 'tool']

def create_message(
    content: str,
    role: MessageRole,
    session_id: str,
    customer_user_id: Optional[str] = None,
    message_id: Optional[str] = None,
    env: Optional[Environment] = None
) -> Dict[str, Any]:
    """Create a new message.
    
    Args:
        content: Content of the message
        role: Role of the message sender
              ('norole', 'system', 'assistant', 'user', 'function', 'tool')
        session_id: ID of the session this message belongs to
        customer_user_id: Optional ID of the customer user
        message_id: Optional unique identifier for the message
        env: Optional environment instance
    
    Returns:
        dict: Created message data containing:
            - id: Message ID
            - sessionID: Session ID
            - role: Message role
            - content: Message content
            - userID: User ID
            - customerUserID: Customer user ID
            - createdAt: Creation timestamp
            - updatedAt: Last update timestamp
        
    Raises:
        ValueError: If required fields are missing or invalid
        APIError: If the API request fails
    """
    if env is None:
        env = Environment()
    
    # Validate required fields
    if not content:
        raise ValueError("content is required")
    if not session_id:
        raise ValueError("session_id is required")
    if not role:
        raise ValueError("role is required")
    
    # Validate role
    valid_roles = ['norole', 'system', 'assistant', 'user', 'function', 'tool']
    if role not in valid_roles:
        raise ValueError(f"role must be one of: {', '.join(valid_roles)}")

    payload = {
        "content": content,
        "role": role,
        "sessionID": session_id,
        "customerUserID": customer_user_id,
        "id": message_id
    }
    
    # Remove None values
    payload = {k: v for k, v in payload.items() if v is not None}
    
    client = httpx.Client(headers=env.headers)
    try:
        response = client.post(
            env.get_full_url("/messages/create"),
            json=payload
        )
        response.raise_for_status()
        return response.json()["data"]
    except httpx.HTTPStatusError as e:
        raise APIError(f"API request failed with status code {e.response.status_code}: {e.response.text}")
    except httpx.RequestError as e:
        raise APIError(f"An error occurred while requesting {e.request.url!r}.")