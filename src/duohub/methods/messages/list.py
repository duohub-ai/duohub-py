from typing import Dict, Any, Optional, Literal
import httpx
from ...environment import Environment
from ...exceptions import APIError

MessageRole = Literal['norole', 'system', 'assistant', 'user', 'function', 'tool']

def list_messages(
    session_id: Optional[str] = None,
    customer_user_id: Optional[str] = None,
    role: Optional[MessageRole] = None,
    limit: Optional[int] = 10,
    next_token: Optional[str] = None,
    previous_token: Optional[str] = None,
    env: Optional[Environment] = None
) -> Dict[str, Any]:
    """Retrieve a list of messages with optional filtering.
    
    Args:
        session_id: Optional filter for messages by session ID
        customer_user_id: Optional filter for messages by customer user ID
        role: Optional filter for messages by role
              ('norole', 'system', 'assistant', 'user', 'function', 'tool')
        limit: Maximum number of messages to return (default: 10)
        next_token: Token for getting the next page of results
        previous_token: Token for getting the previous page of results
        env: Optional environment instance
    
    Returns:
        dict: Contains:
            - messages: List of message objects
            - nextToken: Token for the next page
            - previousToken: Token for the previous page
            - count: Number of messages in the current page
        
    Raises:
        ValueError: If invalid parameters are provided
        APIError: If the API request fails
    """
    if env is None:
        env = Environment()
    
    # Validate role if provided
    if role is not None:
        valid_roles = ['norole', 'system', 'assistant', 'user', 'function', 'tool']
        if role not in valid_roles:
            raise ValueError(f"role must be one of: {', '.join(valid_roles)}")

    # Build query parameters
    params = {}
    if session_id:
        params['sessionID'] = session_id
    if customer_user_id:
        params['customerUserID'] = customer_user_id
    if role:
        params['role'] = role
    if limit is not None:
        params['limit'] = limit
    if next_token:
        params['nextToken'] = next_token
    if previous_token:
        params['previousToken'] = previous_token

    client = httpx.Client(headers=env.headers)
    try:
        response = client.get(
            env.get_full_url("/messages/list"),
            params=params
        )
        response.raise_for_status()
        return response.json()
    except httpx.HTTPStatusError as e:
        raise APIError(f"API request failed with status code {e.response.status_code}: {e.response.text}")
    except httpx.RequestError as e:
        raise APIError(f"An error occurred while requesting {e.request.url!r}.")