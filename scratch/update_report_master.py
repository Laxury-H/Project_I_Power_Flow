"""
Tạo phiên bản nâng cấp toàn diện cho generate_report_do_an_1.py:
- Tích hợp 100% ứng dụng mới PowerFlow trong 'Đồ án 1'
- Thêm phân tích chi tiết 8 phân hệ giao diện Tkinter
- Thêm cơ chế nhập liệu thông minh phân định ẩn số và hằng số
- Thêm Kịch bản 3: Sự cố N-1 (contingency.py) kèm hình ảnh & bảng số liệu
- Thêm Kịch bản 4: So chuẩn 4 bộ giải NR vs FDPF vs GS vs DC (solvers.py)
- Thêm bộ 55 Unit Tests đạt 100% Passed
- Đồng bộ hóa sang cả Word (.docx) và PDF
"""
import os

target_file = r"c:\Users\Lax\Downloads\Project_I_Power_Flow\report\02_Vietnamese_Report\generate_report_do_an_1.py"

# Đọc file hiện tại
with open(target_file, "r", encoding="utf-8") as f:
    content = f.read()

print("Current file length:", len(content))

