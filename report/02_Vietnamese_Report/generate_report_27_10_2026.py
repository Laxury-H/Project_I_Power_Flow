"""
Script tạo báo cáo Đồ án 1 (HUST SEEE) - Đồng bộ hóa với ứng dụng PowerFlow mới.
Khởi chạy bộ sinh báo cáo hoàn chỉnh từ generate_report_do_an_1.py:
- Tích hợp 100% ứng dụng mới PowerFlow trong thư mục 'Đồ án 1'.
- Trực quan hóa 8 phân hệ giao diện Tkinter, cơ chế bảng nhập liệu thông minh [Ẩn số].
- Phân tích 4 kịch bản vận hành thực tế (Tăng tải, Bù tụ tĩnh, Sự cố N-1, So chuẩn 4 bộ giải).
- Bộ 55 bài kiểm thử tự động (Unit Tests) đạt chuẩn 100% Passed.
- Xuất song song file PDF và Word (.docx) sang cả 'Bao_Cao_Do_An_1_PowerFlow' và '27-10-2026 Báo cáo'.
"""
import os
import sys

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, CURRENT_DIR)

from generate_report_do_an_1 import main

if __name__ == '__main__':
    main()
