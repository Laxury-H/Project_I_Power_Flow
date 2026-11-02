"""
PowerFlow — Ứng dụng chính của Đồ án 1 (HUST SEEE)
Khởi chạy giao diện chính Desktop Tkinter từ thư mục 'Đồ án 1'.

Cách dùng:
    python app.py
    hoặc
    CHAY_APP.bat / run_windows.cmd
    (Dùng python app.py --web để chạy phiên bản Web cũ)
"""
import sys
import subprocess
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent
DO_AN_1_DIR = ROOT_DIR / "Đồ án 1"

def run_main_app():
    gui_script = DO_AN_1_DIR / "gui.py"
    if not gui_script.exists():
        print(f"Lỗi: Không tìm thấy {gui_script}")
        sys.exit(1)
        
    print("=" * 72)
    print("⚡ POWERFLOW — ỨNG DỤNG CHÍNH ĐỒ ÁN 1 (HUST SEEE)")
    print("   Đang khởi động giao diện Desktop từ thư mục 'Đồ án 1'...")
    print("=" * 72)
    
    # Chạy giao diện chính với working directory là 'Đồ án 1'
    cmd = [sys.executable, str(gui_script)]
    try:
        subprocess.run(cmd, cwd=str(DO_AN_1_DIR), check=True)
    except KeyboardInterrupt:
        print("\nĐã đóng ứng dụng.")
    except Exception as e:
        print(f"Lỗi khi chạy ứng dụng: {e}")
        sys.exit(1)

def run_web_app():
    import webbrowser
    import uvicorn
    port = 8050
    host = "127.0.0.1"
    url = f"http://{host}:{port}/"
    print("=" * 72)
    print("⚡ Khởi động phiên bản Web Studio...")
    print(f"🌐 Mở tại: {url}")
    print("=" * 72)
    try:
        webbrowser.open(url)
    except Exception:
        pass
    uvicorn.run("web_app.backend.server:app", host=host, port=port, reload=False)

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--web":
        run_web_app()
    else:
        run_main_app()
