#!/usr/bin/env python3
"""
Startup script for the Voice Assistant SaaS API
"""

import uvicorn
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

if __name__ == "__main__":
    # Get configuration from environment
    host = os.getenv("HOST", "127.0.0.1")  # Changed from 0.0.0.0 to 127.0.0.1
    port = int(os.getenv("PORT", "8001"))   # Changed from 8000 to 8001
    reload = os.getenv("RELOAD", "true").lower() == "true"
    
    print(f"🚀 Starting Voice Assistant SaaS API...")
    print(f"📍 Host: {host}")
    print(f"🔌 Port: {port}")
    print(f"🔄 Reload: {reload}")
    print(f"📖 API Docs: http://{host}:{port}/docs")
    print(f"🔍 Health Check: http://{host}:{port}/health")
    
    try:
        # Start the server
        uvicorn.run(
            "saas_api:app",
            host=host,
            port=port,
            reload=reload,
            log_level="info"
        )
    except OSError as e:
        if "10013" in str(e) or "permission" in str(e).lower():
            print(f"❌ Port {port} is in use or blocked. Trying alternative ports...")
            
            # Try alternative ports
            alternative_ports = [8002, 8003, 8004, 8005, 3000, 3001]
            for alt_port in alternative_ports:
                try:
                    print(f"🔄 Trying port {alt_port}...")
                    uvicorn.run(
                        "saas_api:app",
                        host=host,
                        port=alt_port,
                        reload=reload,
                        log_level="info"
                    )
                    break
                except OSError:
                    continue
            else:
                print("❌ All ports are blocked. Please:")
                print("1. Check if another application is using these ports")
                print("2. Run as administrator")
                print("3. Try a different port manually: PORT=9000 python start_server.py")
        else:
            raise e 