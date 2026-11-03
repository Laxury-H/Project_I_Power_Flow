"""
PowerFlow — Ứng dụng Desktop chính thức của Đồ án 1 (HUST SEEE)
Khởi chạy giao diện chính Desktop Tkinter từ thư mục 'Đồ án 1'.

Cách dùng:
    python app.py
    hoặc nhấp đúp:
    CHAY_APP.bat / run_windows.cmd
"""
import sys
import subprocess
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent
DO_AN_1_DIR = ROOT_DIR / "Đồ án 1"

def main():
    gui_script = DO_AN_1_DIR / "gui.py"
    if not gui_script.exists():
        print(f"Lỗi: Không tìm thấy tệp {gui_script}")
        sys.exit(1)
        
    print("=" * 72)
    print("⚡ POWERFLOW — ỨNG DỤNG DESKTOP CHÍNH THỨC ĐỒ ÁN 1 (HUST SEEE)")
    print("   Khởi chạy giao diện đồ họa Python/Tkinter từ 'Đồ án 1'...")
    print("=" * 72)
    
    cmd = [sys.executable, str(gui_script)]
    try:
        subprocess.run(cmd, cwd=str(DO_AN_1_DIR), check=True)
    except KeyboardInterrupt:
        print("\nĐã đóng ứng dụng.")
    except Exception as e:
        print(f"Lỗi khi chạy ứng dụng: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
