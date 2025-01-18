from typing import Dict, Any, Optional
import httpx
from ...environment import Environment
from ...exceptions import APIError

def list_users(
    limit: Optional[int] = 10,
    next_token: Optional[str] = None,
    previous_token: Optional[str] = None,
    env: Optional[Environment] = None
) -> Dict[str, Any]:
    """Retrieve a paginated list of users.
    
    Args:
        limit: Maximum number of users to return (default: 10)
        next_token: Token for getting the next page of results
        previous_token: Token for getting the previous page of results
        env: Optional environment instance
    
    Returns:
        dict: Contains:
            - users: List of user objects
            - nextToken: Token for the next page
            - previousToken: Token for the previous page
            - count: Number of users in the current page
        
    Raises:
        ValueError: If invalid parameters are provided
        APIError: If the API request fails
    """
    if env is None:
        env = Environment()
    
    # Validate limit
    if limit is not None and limit < 1:
        raise ValueError("limit must be a positive integer")

    # Build query parameters
    params = {}
    if limit is not None:
        params['limit'] = limit
    if next_token:
        params['nextToken'] = next_token
    if previous_token:
        params['previousToken'] = previous_token

    client = httpx.Client(headers=env.headers)
    try:
        response = client.get(
            env.get_full_url("/users/list"),
            params=params
        )
        response.raise_for_status()
        return response.json()
    except httpx.HTTPStatusError as e:
        raise APIError(f"API request failed with status code {e.response.status_code}: {e.response.text}")
    except httpx.RequestError as e:
        raise APIError(f"An error occurred while requesting {e.request.url!r}.")