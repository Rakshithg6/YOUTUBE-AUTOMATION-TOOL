# YOUTUBE-AUTOMATION-TOOL
This is a Python-based automation tool for uploading videos to YouTube using the YouTube Data API and LangGraph for workflow management. It provides a structured approach to validate, prepare, and upload videos with error handling and status tracking.

## Features
- Automated video upload workflow
- Input validation for video files and metadata
- Configurable video settings (title, description, privacy status, etc.)
- Error handling and status tracking
- Built with LangGraph for state management
- Extensible architecture

## Prerequisites
- Python 3.8+
- Google Cloud Project with YouTube Data API enabled
- OAuth 2.0 credentials from Google Cloud Console
- Video files in supported formats (MP4, AVI, etc.)

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/youtube-upload-automation.git
cd youtube-upload-automation
```
```
youtube-upload-automation/
├── youtube_uploader.py    # Main script with upload logic
├── requirements.txt       # Project dependencies
├── README.md             # This file
└── credentials.json      # Google Cloud credentials (not tracked)
```


