# Required imports
from langgraph.graph import StateGraph, END
from typing import TypedDict, Annotated, Sequence
import operator
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from oauth2client.client import GoogleCredentials
import os

# Define the state structure
class VideoUploadState(TypedDict):
    video_path: str
    title: str
    description: str
    category: str
    keywords: list
    privacy_status: str
    upload_status: str
    error_message: str

# Authentication function
def authenticate_youtube():
    """Authenticate with YouTube API"""
    # Assuming you have credentials.json file from Google Cloud Console
    credentials = GoogleCredentials.get_application_default()
    return build('youtube', 'v3', credentials=credentials)

# Node functions
def validate_input(state: VideoUploadState) -> VideoUploadState:
    """Validate video file and metadata"""
    try:
        if not os.path.exists(state["video_path"]):
            raise FileNotFoundError("Video file not found")
        
        if not state["title"] or len(state["title"]) > 100:
            raise ValueError("Title is required and must be under 100 characters")
            
        if not state["description"] or len(state["description"]) > 5000:
            raise ValueError("Description is required and must be under 5000 characters")
            
        return {"upload_status": "validated"}
    except Exception as e:
        return {"upload_status": "failed", "error_message": str(e)}

def prepare_upload(state: VideoUploadState) -> VideoUploadState:
    """Prepare video upload request"""
    if state["upload_status"] != "validated":
        return state
    
    try:
        youtube = authenticate_youtube()
        
        body = {
            "snippet": {
                "title": state["title"],
                "description": state["description"],
                "tags": state["keywords"],
                "categoryId": state["category"]
            },
            "status": {
                "privacyStatus": state["privacy_status"]
            }
        }
        
        return {"youtube_client": youtube, "request_body": body}
    except Exception as e:
        return {"upload_status": "failed", "error_message": str(e)}

def upload_video(state: VideoUploadState) -> VideoUploadState:
    """Execute video upload"""
    if state["upload_status"] != "validated":
        return state
        
    try:
        youtube = state["youtube_client"]
        request_body = state["request_body"]
        
        media = MediaFileUpload(state["video_path"])
        request = youtube.videos().insert(
            part="snippet,status",
            body=request_body,
            media_body=media
        )
        
        response = request.execute()
        return {"upload_status": "completed", "video_id": response["id"]}
    except Exception as e:
        return {"upload_status": "failed", "error_message": str(e)}

# Build the workflow graph
def build_upload_workflow():
    workflow = StateGraph(VideoUploadState)
    
    # Add nodes
    workflow.add_node("validate", validate_input)
    workflow.add_node("prepare", prepare_upload)
    workflow.add_node("upload", upload_video)
    
    # Define edges
    workflow.set_entry_point("validate")
    workflow.add_edge("validate", "prepare")
    workflow.add_edge("prepare", "upload")
    workflow.add_edge("upload", END)
    
    return workflow.compile()

# Main execution function
def upload_youtube_video(
    video_path: str,
    title: str,
    description: str,
    category: str = "22",  # Default to "People & Blogs"
    keywords: list = [],
    privacy_status: str = "private"
):
    """Execute the video upload workflow"""
    # Initialize state
    initial_state = VideoUploadState(
        video_path=video_path,
        title=title,
        description=description,
        category=category,
        keywords=keywords,
        privacy_status=privacy_status,
        upload_status="pending",
        error_message=""
    )
    
    # Create and run workflow
    app = build_upload_workflow()
    result = app.invoke(initial_state)
    
    return result

# Example usage
if __name__ == "__main__":
    # Example parameters
    video_params = {
        "video_path": "path/to/your/video.mp4",
        "title": "My Awesome Video",
        "description": "This is a test video upload",
        "category": "22",
        "keywords": ["test", "video", "automation"],
        "privacy_status": "private"
    }
    
    # Execute upload
    result = upload_youtube_video(**video_params)
    
    if result["upload_status"] == "completed":
        print(f"Video uploaded successfully! Video ID: {result['video_id']}")
    else:
        print(f"Upload failed: {result['error_message']}")