from typing import Optional
import httpx
from ...environment import Environment

def create_file_record(
    name: str,
    key: Optional[str] = None,
    external_uri: Optional[str] = None,
    file_type: Optional[str] = None
) -> dict:
    """Create a file record after upload
    
    Args:
        name: Name of the file
        key: Storage key for uploaded files
        external_uri: External URI for website/sitemap files
        file_type: Type of file (required for external URIs)
        
    Returns:
        dict: Created file record data
    """
    env = Environment()
    client = httpx.Client(headers=env.headers)
    
    payload = {
        "name": name,
        "key": key,
        "externalURI": external_uri,
        "fileType": file_type
    }
    # Remove None values
    payload = {k: v for k, v in payload.items() if v is not None}
    
    response = client.post(
        env.get_full_url("/files/create"),
        json=payload
    )
    response.raise_for_status()
    return response.json()["data"]