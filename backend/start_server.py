#!/usr/bin/env python
"""
Alternative server startup script
"""
import uvicorn
import sys
import os

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from main import app

if __name__ == "__main__":
    print("=" * 50)
    print("Starting Plagiarism Detection API Server")
    print("=" * 50)
    print("Server URL: http://127.0.0.1:8000")
    print("Health Check: http://127.0.0.1:8000/health")
    print("API Docs: http://127.0.0.1:8000/docs")
    print("=" * 50)
    print("Press CTRL+C to stop the server")
    print("=" * 50)
    
    try:
        uvicorn.run(
            "main:app",
            host="127.0.0.1",
            port=8000,
            reload=False,
            log_level="info"
        )
    except KeyboardInterrupt:
        print("\nServer stopped by user")
    except Exception as e:
        print(f"\nError: {e}")
        sys.exit(1)

