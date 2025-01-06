from typing import BinaryIO
import httpx
from tqdm import tqdm
from ...environment import Environment

def get_upload_url(filename: str) -> dict:
    """Get a pre-signed URL for file upload
    
    Args:
        filename: Name of the file to upload
        
    Returns:
        dict: Contains uploadUrl and key
    """
    env = Environment()
    client = httpx.Client(headers=env.headers)
    
    response = client.post(
        env.get_full_url("/files/upload"),
        json={"fileName": filename}
    )
    response.raise_for_status()
    return response.json()["data"]

def upload_file_content(upload_url: str, file: BinaryIO) -> None:
    """Upload file content to the pre-signed URL
    
    Args:
        upload_url: Pre-signed URL for upload
        file: File object to upload
    """
    # Get file size for progress bar
    file.seek(0, 2)  # Seek to end of file
    file_size = file.tell()
    file.seek(0)  # Reset to beginning
    
    client = httpx.Client()
    
    with tqdm(total=file_size, unit='B', unit_scale=True, desc="Uploading") as pbar:
        # Create a wrapper for the file that updates the progress bar
        class ProgressFileWrapper:
            def __init__(self, file, pbar):
                self.file = file
                self.pbar = pbar
            
            def read(self, size):
                data = self.file.read(size)
                self.pbar.update(len(data))
                return data
        
        wrapped_file = ProgressFileWrapper(file, pbar)
        
        response = client.put(
            upload_url,
            content=wrapped_file,
            headers={"Content-Type": "application/octet-stream"}
        )
        response.raise_for_status()