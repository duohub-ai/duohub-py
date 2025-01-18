from typing import Dict, Any, Optional
import httpx
from ...environment import Environment
from ...exceptions import APIError

def create_memory(
    name: str,
    memory_type: str,
    description: str = None,
    ontology: str = None,
    chunk_size: int = 250,
    chunk_overlap: int = 10,
    webhook_url: str = None,
    acceleration: bool = False,
    fact_extraction: bool = False,
    env: Optional[Environment] = None
) -> Dict[str, Any]:
    """Create a new memory (graph or vector).
    
    Args:
        name: Name of the memory
        memory_type: Type of memory storage ('graph' or 'vector')
        description: Description of the memory
        ontology: Ontology type for the memory (required for graph memory type)
                 Options: culture, essays, support_requests
        chunk_size: Size of text chunks in characters (only for vector memory type)
        chunk_overlap: Overlap size between chunks in percentages (1-50, vector only)
        webhook_url: Optional webhook URL for notifications
        acceleration: Whether to enable acceleration
        env: Optional environment instance
        fact_extraction: Whether to enable fact extraction
    Returns:
        dict: Created memory data
        
    Raises:
        ValueError: If invalid parameters are provided
        APIError: If the API request fails
    """
    if env is None:
        env = Environment()
    
    # Validate memory_type
    memory_type = memory_type.lower()
    if memory_type not in ['graph', 'vector']:
        raise ValueError("memory_type must be either 'graph' or 'vector'")
    
    # Validate ontology for graph memory
    if memory_type == 'graph' and not ontology:
        raise ValueError("ontology is required for graph memory type")
    
    # Validate chunk_overlap range
    if chunk_overlap is not None and not (1 < chunk_overlap < 50):
        raise ValueError("chunk_overlap must be between 1 and 50")
    # Add multiple files to a memory

    payload = {
        "name": name,
        "memoryType": memory_type,
        "description": description,
        "ontology": ontology,
        "chunkSize": chunk_size,
        "chunkOverlap": chunk_overlap,
        "webhookUrl": webhook_url,
        "acceleration": acceleration,
        "factExtraction": fact_extraction
    }
    
    # Remove None values
    payload = {k: v for k, v in payload.items() if v is not None}
    
    client = httpx.Client(headers=env.headers)
    try:
        response = client.post(
            env.get_full_url("/memories/create"),
            json=payload
        )
        response.raise_for_status()
        return response.json()["data"]
    except httpx.HTTPStatusError as e:
        raise APIError(f"API request failed with status code {e.response.status_code}: {e.response.text}")
    except httpx.RequestError as e:
        raise APIError(f"An error occurred while requesting {e.request.url!r}.")
