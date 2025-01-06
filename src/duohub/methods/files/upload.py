from typing import BinaryIO
import requests
from os.path import splitext
from ...environment import Environment

def get_file_type(fileName: str) -> str:
    """Determine content type based on file extension"""
    extension_map = {
        # Images
        '.jpg': 'image/jpeg',
        '.jpeg': 'image/jpeg',
        '.png': 'image/png',
        '.pdf': 'application/pdf',
        '.svg': 'image/svg+xml',
        '.gif': 'image/gif',
        '.webp': 'image/webp',
        
        # Documents
        '.doc': 'application/msword',
        '.docx': 'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
        '.xls': 'application/vnd.ms-excel',
        '.xlsx': 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
        '.ppt': 'application/vnd.ms-powerpoint',
        '.pptx': 'application/vnd.openxmlformats-officedocument.presentationml.presentation',
        '.txt': 'text/plain',
        '.csv': 'text/csv',
        '.rtf': 'application/rtf',
        '.odt': 'application/vnd.oasis.opendocument.text',
        
        # Videos
        '.mp4': 'video/mp4',
        '.mov': 'video/quicktime',
        '.avi': 'video/x-msvideo',
        '.wmv': 'video/x-ms-wmv',
        '.flv': 'video/x-flv',
        '.webm': 'video/webm',
        '.mkv': 'video/x-matroska',
        
        # Audio
        '.mp3': 'audio/mpeg',
        '.wav': 'audio/wav',
        '.ogg': 'audio/ogg',
        '.m4a': 'audio/mp4',
        '.aac': 'audio/aac',
        '.wma': 'audio/x-ms-wma',
        '.flac': 'audio/flac'
    }
    _, ext = splitext(fileName.lower())
    return extension_map.get(ext, 'application/octet-stream')

def get_upload_url(filename: str) -> dict:
    """Get a pre-signed URL for file upload
    
    Args:
        filename: Name of the file to upload
        
    Returns:
        dict: Contains uploadUrl and key
    """
    env = Environment()
    
    # Get the content type for the file
    
    response = requests.post(
        env.get_full_url("/files/upload"),
        headers=env.headers,
        json={
            "fileName": filename        }
    )
    response.raise_for_status()
    return response.json()["data"]

def upload_file_content(upload_url: str, file: BinaryIO) -> None:
    """Upload file content to the pre-signed URL
    
    Args:
        upload_url: Pre-signed URL for upload
        file: File object to upload
    """
    content = file.read()
    
    # Extract filename from the URL
    filename = upload_url.split('/')[-1].split('?')[0]
    
    # Get correct content type for the file
    content_type = get_file_type(filename)
    
    headers = {
        "Content-Type": content_type
    }
    
    response = requests.put(
        upload_url,
        headers=headers,
        data=content,
        allow_redirects=False
    )
    
    if response.status_code != 200:
        print(f"Upload failed: {response.status_code}")
        print(f"Response headers: {dict(response.headers)}")
        print(f"Response body: {response.text}")
    
    response.raise_for_status()