from typing import Dict, Any, Optional
import httpx
from ...environment import Environment
from ...exceptions import APIError

def list_sessions(
    customer_user_id: Optional[str] = None,
    limit: Optional[int] = 10,
    next_token: Optional[str] = None,
    previous_token: Optional[str] = None,
    env: Optional[Environment] = None
) -> Dict[str, Any]:
    """Retrieve a list of sessions with optional filtering and pagination.
    
    Args:
        customer_user_id: Optional filter for sessions by customer user ID
        limit: Maximum number of sessions to return (default: 10, range: 1-100)
        next_token: Token for getting the next page of results
        previous_token: Token for getting the previous page of results
        env: Optional environment instance
    
    Returns:
        dict: Contains:
            - sessions: List of session objects
            - nextToken: Token for the next page
            - previousToken: Token for the previous page
            - count: Number of sessions in the current page
        
    Raises:
        ValueError: If invalid parameters are provided
        APIError: If the API request fails
    """
    if env is None:
        env = Environment()
    
    # Validate limit
    if limit is not None:
        if not isinstance(limit, int) or limit < 1 or limit > 100:
            raise ValueError("limit must be an integer between 1 and 100")

    # Build query parameters
    params = {}
    if customer_user_id:
        params['customerUserID'] = customer_user_id
    if limit is not None:
        params['limit'] = limit
    if next_token:
        params['nextToken'] = next_token
    if previous_token:
        params['previousToken'] = previous_token

    client = httpx.Client(headers=env.headers)
    try:
        response = client.get(
            env.get_full_url("/sessions/list"),
            params=params
        )
        response.raise_for_status()
        return response.json()["data"]
    except httpx.HTTPStatusError as e:
        raise APIError(f"API request failed with status code {e.response.status_code}: {e.response.text}")
    except httpx.RequestError as e:
        raise APIError(f"An error occurred while requesting {e.request.url!r}.")