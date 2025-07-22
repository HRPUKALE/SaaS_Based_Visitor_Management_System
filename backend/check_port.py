#!/usr/bin/env python3
"""
Port checker utility for Voice Assistant SaaS Backend
Helps find available ports for the server
"""

import socket
import sys

def check_port(host, port):
    """Check if a port is available"""
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(1)
            result = s.connect_ex((host, port))
            return result != 0  # True if port is available
    except Exception:
        return False

def find_available_port(host, start_port=8001, max_attempts=20):
    """Find an available port starting from start_port"""
    for port in range(start_port, start_port + max_attempts):
        if check_port(host, port):
            return port
    return None

def main():
    host = "127.0.0.1"
    
    print("🔍 Checking available ports...")
    print("=" * 40)
    
    # Check common ports
    common_ports = [8000, 8001, 8002, 8003, 8004, 8005, 3000, 3001, 8080, 9000]
    
    available_ports = []
    used_ports = []
    
    for port in common_ports:
        if check_port(host, port):
            available_ports.append(port)
            print(f"✅ Port {port}: Available")
        else:
            used_ports.append(port)
            print(f"❌ Port {port}: In use")
    
    print("\n" + "=" * 40)
    
    if available_ports:
        recommended_port = available_ports[0]
        print(f"🎯 Recommended port: {recommended_port}")
        print(f"\n🚀 To start the server on port {recommended_port}:")
        print(f"   python start_server.py")
        print(f"\n   Or set environment variable:")
        print(f"   set PORT={recommended_port} && python start_server.py")
    else:
        print("❌ No common ports are available!")
        print("🔧 Trying to find any available port...")
        
        available_port = find_available_port(host, 8001, 50)
        if available_port:
            print(f"✅ Found available port: {available_port}")
            print(f"\n🚀 To start the server on port {available_port}:")
            print(f"   set PORT={available_port} && python start_server.py")
        else:
            print("❌ Could not find any available ports!")
            print("\n💡 Solutions:")
            print("1. Close other applications using these ports")
            print("2. Run as administrator")
            print("3. Restart your computer")
            print("4. Use a different host (e.g., 0.0.0.0)")

if __name__ == "__main__":
    main() 