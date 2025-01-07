"""Enum models for the duohub Pythonpackage."""

from enum import Enum

class Status(str, Enum):
    """Enum representing the status of a job in the app.
    
    Attributes:
        pending: Job is pending
        processing: Job is processing
        success: Job is completed
        failed: Job is failed
    """
    pending = "pending"
    processing = "processing"
    success = "success"
    failed = "failed"


class FileType(str, Enum):
    """Enum representing the specific type of a file in the app.
    
    Attributes:
        youtube: YouTube video
        website: Website content
        sitemap: Sitemap file
        document: Document file
        text: Text file
        image: Image file
        audio: Audio file
        video: Video file
        audio_recording: Audio recording
        audio_upload: Uploaded audio file
        video_upload: Uploaded video file
        other: Other file types
    """
    youtube = "youtube"
    website = "website"
    sitemap = "sitemap"
    website_bulk = "website_bulk"
    document = "document"
    image = "image"
    audio = "audio"
    video = "video"

class MemoryType(str, Enum):
    """Enum representing types of memory storage.
    
    Attributes:
        graph: Graph-based memory
        vector: Vector-based memory
    """
    graph = "graph"
    vector = "vector"