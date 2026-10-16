"""
Runner script for Modern Power Flow Studio Web Application.
Launches the FastAPI backend and serves the interactive frontend on http://127.0.0.1:8050.
Can run in parallel with the Streamlit app (which runs on port 8501).
"""

import sys
import os
import webbrowser
from pathlib import Path

# Add project root to path
PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

import uvicorn

def main():
    port = 8050
    host = "127.0.0.1"
    url = f"http://{host}:{port}"
    
    print("=" * 72)
    print("  ⚡ POWERFLOW STUDIO — ỨNG DỤNG TÍNH TRÀO LƯU CÔNG SUẤT HIỆN ĐẠI")
    print("  Đại Học Bách Khoa Hà Nội — Trường Điện - Điện tử (HUST - SEEE)")
    print("=" * 72)
    print(f"  • Máy chủ đang khởi động tại: {url}")
    print(f"  • Cổng chạy độc lập: {port} (chạy song song hoàn hảo với Streamlit :8501)")
    print(f"  • Sơ đồ lưới trực quan, ma trận Y-bus, kiểm tra lỗi thời gian thực")
    print("=" * 72)
    print("  Nhấn Ctrl+C để dừng máy chủ bất kỳ lúc nào.\n")

    # Optionally auto-open browser
    try:
        webbrowser.open(url)
    except Exception:
        pass

    uvicorn.run("web_app.backend.server:app", host=host, port=port, reload=True)

if __name__ == "__main__":
    main()
