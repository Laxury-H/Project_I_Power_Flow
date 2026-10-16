"""
PowerFlow Studio v2.0 — Modern Newton-Raphson Power Flow Application
Entry point to launch the PowerFlow Studio web application.

Usage:
    python app.py
    hoặc
    run_windows.cmd
"""
import sys
import webbrowser
from pathlib import Path
import uvicorn

def main():
    port = 8050
    host = "127.0.0.1"
    url = f"http://{host}:{port}/"
    
    print("=" * 72)
    print("⚡ POWERFLOW STUDIO v2.0 — HỆ THỐNG TRÀO LƯU CÔNG SUẤT & ĐIỀU ĐỘ HIỆN ĐẠI")
    print(f"🌐 Đang mở giao diện tại: {url}")
    print("   Nhấn Ctrl+C để dừng máy chủ.")
    print("=" * 72)
    
    try:
        webbrowser.open(url)
    except Exception:
        pass
        
    uvicorn.run("web_app.backend.server:app", host=host, port=port, reload=False)

if __name__ == "__main__":
    main()
