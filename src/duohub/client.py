import os
from typing import Dict, Any, List, Optional
import httpx
from .exceptions import APIError, ValidationError, MissingFieldError, InvalidDataTypeError
from .environment import Environment
from .methods.files.upload import get_upload_url, upload_file_content
from .methods.files.create import create_file_record
from .models.enums import MemoryType

class Duohub:
    def __init__(self, api_key=None):
        self.environment = Environment(api_key)
        self.client = httpx.Client(
            headers={
                **self.environment.headers,
                "Connection": "keep-alive",
                "Keep-Alive": "timeout=30, max=1000"
            },
            timeout=httpx.Timeout(30.0, connect=5.0)
        )

    def query(self, query: str, memoryID: str, assisted: bool = False, facts: bool = False, top_k: int = 5) -> Dict[str, Any]:
        url = self.environment.get_full_url("/memory/")
        
        params = {
            "memoryID": memoryID,
            "query": query,
            "assisted": str(assisted).lower(),
            "facts": str(facts).lower(),
            "top_k": top_k
        }
        
        try:
            response = self.client.get(url, params=params)
            response.raise_for_status()
            data = response.json()
            
            # Basic validation of the response
            if not isinstance(data, dict):
                raise InvalidDataTypeError("API response is not a dictionary")
            
            required_fields = ['payload', 'facts', 'sources']
            for field in required_fields:
                if field not in data:
                    raise MissingFieldError(f"Required field '{field}' is missing from the API response")
            
            # Validate data types
            if not isinstance(data['payload'], list):
                raise InvalidDataTypeError("'payload' must be a list")
            if not isinstance(data['facts'], list):
                raise InvalidDataTypeError("'facts' must be a list")
            if not isinstance(data['sources'], list):
                raise InvalidDataTypeError("'sources' must be a list")
            
            # Validate facts structure
            for fact in data['facts']:
                if not isinstance(fact, dict) or 'content' not in fact or not isinstance(fact['content'], str):
                    raise InvalidDataTypeError("Each fact must be a dictionary with a 'content' string")
            
            return data
        except httpx.HTTPStatusError as e:
            raise APIError(f"API request failed with status code {e.response.status_code}: {e.response.text}")
        except httpx.RequestError as e:
            raise APIError(f"An error occurred while requesting {e.request.url!r}.")
        except (ValidationError, MissingFieldError, InvalidDataTypeError) as e:
            raise APIError(f"API response validation failed: {str(e)}")
        except ValueError as e:
            raise APIError(f"Error parsing JSON response: {str(e)}")

    def add_file(self, file_path: str = None, external_uri: str = None, file_type: str = None) -> Dict[str, Any]:
        """Add a file to Duohub.
        
        Args:
            file_path: Path to local file to upload
            external_uri: External URI (requires file_type)
            file_type: Required when using external_uri ('website', 'sitemap', or 'website_bulk')
        """
        if external_uri:
            if not file_type in ['website', 'sitemap', 'website_bulk']:
                raise ValueError("file_type must be 'website', 'sitemap', or 'website_bulk' when using external_uri")
            return create_file_record(
                name=external_uri,
                external_uri=external_uri,
                file_type=file_type
            )

        if not file_path:
            raise ValueError("Must provide either file_path or external_uri")

        # Get file name from path
        name = os.path.basename(file_path)

        # Get upload URL
        upload_data = get_upload_url(name)

        # Upload file with progress
        with open(file_path, 'rb') as f:
            upload_file_content(
                upload_data["uploadUrl"],
                f
             )

        # Create file record
        return create_file_record(
            name=name,
            key=upload_data["key"]
        )

    def create_memory(
        self,
        name: str,
        memory_type: str,
        description: str = None,
        ontology: str = None,
        chunk_size: int = 250,
        chunk_overlap: int = 10,
        webhook_url: str = None,
        acceleration: bool = False
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
            
        Returns:
            dict: Created memory data
        """
        from .methods.memory.create import create_memory as create_memory_request
        return create_memory_request(
            name=name,
            memory_type=memory_type,
            description=description,
            ontology=ontology,
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            webhook_url=webhook_url,
            acceleration=acceleration,
            env=self.environment
        )

    def add_files_to_memory(
        self,
        memory_id: str,
        files: List[str]
    ) -> Dict[str, Any]:
        """Add files to a memory.
        
        Args:
            memory_id: ID of the memory to add the files to
            files: List of file IDs to add
            
        Returns:
            dict: Response data from the API
            
        Note:
            This endpoint can only be used with memories created on or after 17-Dec-2024.
        """
        from .methods.memory.add_files import add_files_to_memory as add_files_request
        return add_files_request(
            memory_id=memory_id,
            files=files,
            env=self.environment
        )

    def delete_file_from_memory(
        self,
        memory_id: str,
        file_id: str
    ) -> Dict[str, Any]:
        """Delete a file from a memory.
        
        Args:
            memory_id: ID of the memory to remove the file from
            file_id: ID of the file to remove
            
        Returns:
            dict: Response data from the API
            
        Note:
            This endpoint can only be used with memories created on or after 17-Dec-2024.
        """
        from .methods.memory.delete_file import delete_file_from_memory as delete_file_request
        return delete_file_request(
            memory_id=memory_id,
            file_id=file_id,
            env=self.environment
        )

    def start_ingestion(
        self,
        memory_id: str
    ) -> Dict[str, Any]:
        """Start ingestion for a memory.
        
        Once you've added files to a memory, call this endpoint to begin ingesting the files.
        
        Args:
            memory_id: ID of the memory to start ingestion for
            
        Returns:
            dict: Response data containing status, message and data
        """
        from .methods.memory.start_ingestion import start_ingestion as start_ingestion_request
        return start_ingestion_request(
            memory_id=memory_id,
            env=self.environment
        )

    # Message Methods
    def get_message(self, message_id: str) -> Dict[str, Any]:
        """Get a message by ID."""
        from .methods.messages.get import get_message
        return get_message(message_id=message_id, env=self.environment)

    def list_messages(
        self,
        session_id: Optional[str] = None,
        customer_user_id: Optional[str] = None,
        role: Optional[str] = None,
        limit: Optional[int] = 10,
        next_token: Optional[str] = None,
        previous_token: Optional[str] = None
    ) -> Dict[str, Any]:
        """List messages with optional filtering."""
        from .methods.messages.list import list_messages
        return list_messages(
            session_id=session_id,
            customer_user_id=customer_user_id,
            role=role,
            limit=limit,
            next_token=next_token,
            previous_token=previous_token,
            env=self.environment
        )

    def delete_message(self, message_id: str) -> Dict[str, Any]:
        """Delete a message by ID."""
        from .methods.messages.delete import delete_message
        return delete_message(message_id=message_id, env=self.environment)

    def create_message(
        self,
        content: str,
        role: str,
        session_id: str,
        customer_user_id: Optional[str] = None,
        message_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """Create a new message."""
        from .methods.messages.create import create_message
        return create_message(
            content=content,
            role=role,
            session_id=session_id,
            customer_user_id=customer_user_id,
            message_id=message_id,
            env=self.environment
        )

    # User Methods
    def get_user(self, user_id: str) -> Dict[str, Any]:
        """Get a user by ID."""
        from .methods.users.get import get_user
        return get_user(user_id=user_id, env=self.environment)

    def list_users(
        self,
        limit: Optional[int] = 10,
        next_token: Optional[str] = None,
        previous_token: Optional[str] = None
    ) -> Dict[str, Any]:
        """List users with pagination."""
        from .methods.users.list import list_users
        return list_users(
            limit=limit,
            next_token=next_token,
            previous_token=previous_token,
            env=self.environment
        )

    def delete_user(self, user_id: str) -> Dict[str, Any]:
        """Delete a user by ID."""
        from .methods.users.delete import delete_user
        return delete_user(user_id=user_id, env=self.environment)

    def create_user(
        self,
        first_name: str,
        last_name: str,
        email: Optional[str] = None,
        user_id: Optional[str] = None,
        phone: Optional[str] = None
    ) -> Dict[str, Any]:
        """Create a new user."""
        from .methods.users.create import create_user
        return create_user(
            first_name=first_name,
            last_name=last_name,
            email=email,
            user_id=user_id,
            phone=phone,
            env=self.environment
        )

    # Session Methods
    def get_session(self, session_id: str) -> Dict[str, Any]:
        """Get a session by ID."""
        from .methods.sessions.get import get_session
        return get_session(session_id=session_id, env=self.environment)

    def list_sessions(
        self,
        customer_user_id: Optional[str] = None,
        limit: Optional[int] = 10,
        next_token: Optional[str] = None,
        previous_token: Optional[str] = None
    ) -> Dict[str, Any]:
        """List sessions with optional filtering."""
        from .methods.sessions.list import list_sessions
        return list_sessions(
            customer_user_id=customer_user_id,
            limit=limit,
            next_token=next_token,
            previous_token=previous_token,
            env=self.environment
        )

    def delete_session(self, session_id: str) -> Dict[str, Any]:
        """Delete a session by ID."""
        from .methods.sessions.delete import delete_session
        return delete_session(session_id=session_id, env=self.environment)

    def create_session(
        self,
        customer_user_id: Optional[str] = None,
        session_id: Optional[str] = None,
        metadata: Optional[List[Dict[str, str]]] = None
    ) -> Dict[str, Any]:
        """Create a new session."""
        from .methods.sessions.create import create_session
        return create_session(
            customer_user_id=customer_user_id,
            session_id=session_id,
            metadata=metadata,
            env=self.environment
        )

    def __del__(self):
        if hasattr(self, 'client'):
            self.client.close()

