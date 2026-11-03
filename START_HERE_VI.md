# BẮT ĐẦU TỪ ĐÂY — Hướng dẫn cài đặt và sử dụng phần mềm PowerFlow (Đồ án 1)

---

## 1. Cấu trúc bộ tài liệu & ứng dụng Đồ án 1

* **Ứng dụng chính (PowerFlow Desktop GUI):** Đặt trong thư mục `Đồ án 1`, khởi động nhanh qua `app.py` hoặc `CHAY_APP.bat`.
* **Báo cáo nộp chính thức:**
  * File PDF: [`report/Bao_Cao_Do_An_1_PowerFlow_29-10-2026.pdf`](report/Bao_Cao_Do_An_1_PowerFlow_29-10-2026.pdf) (Bản chuẩn quy định ĐHBK Hà Nội).
  * File Word: [`report/Bao_Cao_Do_An_1_PowerFlow_29-10-2026.docx`](report/Bao_Cao_Do_An_1_PowerFlow_29-10-2026.docx) (Dùng cho in ấn hoặc chỉnh sửa).
* **Đề bài & Hướng dẫn tự tính tay Casio:**
  * File PDF: [`report/De_Bai_Tinh_Tay_Newton_Raphson_28-10-2026.pdf`](report/De_Bai_Tinh_Tay_Newton_Raphson_28-10-2026.pdf).
* **Mã nguồn giải thuật & giao diện:**
  * `Đồ án 1/gui.py`: Giao diện chính đa luồng (Tkinter).
  * `Đồ án 1/ui_table_editor.py`: Bảng nhập liệu thông minh (phân định rõ Ẩn số vs Thông số cho trước).
  * `Đồ án 1/ui_topology.py`: Sơ đồ 1 sợi Canvas tương tác (mũi tên trào lưu động, phân màu tải đường dây).
  * `Đồ án 1/ui_dashboard.py`: Bảng điều khiển KPI & đồ thị Matplotlib.
  * `Đồ án 1/powerflow.py`: Lõi giải thuật Newton–Raphson tọa độ cực chính xác 100%.
  * `Đồ án 1/tests/`: Bộ 55 bài kiểm thử tự động (Unit Tests) đạt chuẩn 100%.

---

## 2. Cách chạy ứng dụng trên Windows

1. **Khởi chạy tức thì:**
   * Nhấp đúp vào file `CHAY_APP.bat` (hoặc `run_windows.cmd`).
   * Hoặc mở Terminal gõ:
     ```bash
     .venv\Scripts\python.exe app.py
     ```
2. **Thực hiện bài toán trào lưu:**
   * Trong mục **01 Dữ liệu lưới**, chọn ví dụ mẫu: `3 nút · Chuẩn Báo cáo (27/10)`.
   * Bấm nút **Nạp mẫu**.
   * Bấm nút **Tính toán trào lưu**.
   * Phần mềm sẽ tính toán và hiển thị ngay kết quả tại các tab:
     * **Tổng quan:** Xem các thẻ KPI, phân bố điện áp và đường cong hội tụ bậc hai.
     * **Sơ đồ lưới:** Xem mũi tên dòng công suất thực tế trên sơ đồ 1 sợi.
     * **Điện áp nút & Công suất nhánh:** Xem chi tiết các bảng số liệu.
     * **Báo cáo:** Xem báo cáo kỹ thuật tổng hợp dạng văn bản.

---

## 3. Chạy bộ kiểm thử tự động (55 Unit Tests)

Để xác nhận tính toàn vẹn và độ chính xác của toàn bộ chương trình:
```bash
.venv\Scripts\pytest.exe
```
Kết quả đạt: **`55 passed (100% Passed)`**.
