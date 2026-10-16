# PowerFlow Studio — Ứng dụng Web Tính Trào Lưu Công Suất Xác Lập

Ứng dụng web chạy cục bộ hiện đại, hiệu năng cao, được thiết kế để tính toán trào lưu công suất xác lập trong hệ thống điện bằng phương pháp Newton–Raphson, có thể chạy song song độc lập với ứng dụng Streamlit hiện có (`app.py`) để đối chiếu và so sánh kết quả.

---

## Các tính năng nổi bật

1. **Sơ đồ một sợi trực quan & tương tác (Single-Line Diagram):**
   - Vẽ tự động sơ đồ lưới điện bằng SVG sắc nét.
   - Phân biệt trực quan các loại nút: **Slack (Hồng/Đỏ)**, **PV (Hổ phách/Vàng)**, **PQ (Xanh lơ)**.
   - Hỗ trợ **kéo thả (Drag & Drop)** vị trí các thanh cái trên sơ đồ theo ý muốn.
   - Hiển thị mũi tên động và công suất truyền tải $P_{ij}$ khi đã giải xong trào lưu.
   - **Tooltip tương tác:** Rê chuột vào thanh cái hoặc đường dây để xem chi tiết thông số điện áp, góc pha, dòng điện và tổn thất.

2. **Bảng dữ liệu Nút và Đường dây song song (Side-by-side Tables):**
   - Bảng nút (Buses) và Bảng đường dây (Lines) hiển thị song song, trực quan và dễ theo dõi.
   - Cho phép **nhập liệu trực tiếp bằng tay**, thêm hàng, xóa hàng.
   - Hỗ trợ **Import CSV** và **Export CSV** nhanh chóng.
   - Cho phép đặt cơ sở công suất $S_{base}$ (mặc định 100 MVA) và công tắc chuyển đổi hiển thị giữa hệ đơn vị tương đối (**pu**) và giá trị thực (**MW / Mvar**).

3. **Kiểm tra dữ liệu thời gian thực (Real-time Live Validation):**
   - Tự động kiểm tra lỗi tức thì khi người dùng chỉnh sửa bất kỳ ô dữ liệu nào.
   - Báo lỗi chi tiết bằng tiếng Việt:
     - Thiếu nút Slack hoặc nhiều hơn 1 nút Slack.
     - Dữ liệu thiếu, sai định dạng số hoặc giá trị không hợp lệ.
     - Điện áp $V_m \le 0$, phụ tải $P_d < 0$ hoặc $Q_d < 0$.
     - Đường dây có điện trở âm $R < 0$ hoặc điện kháng không dương $X \le 0$.
     - Đường dây tự lặp $(a = b)$ hoặc nối đến nút không tồn tại.
     - Lưới điện bị chia cắt / mất liên thông (cô lập nút).

4. **Ma trận dẫn nạp nút $Y_{bus}$ tự động (Admittance Matrix Inspector):**
   - Tự động lập ma trận $Y_{bus}$ từ bảng đường dây.
   - Trình bày dạng ma trận số học trực quan, nổi bật phần tử đường chéo chính.
   - Hỗ trợ chuyển đổi qua lại giữa dạng đại số ($G + jB$) và dạng cực ($|Y| \angle \theta^\circ$).
   - Thống kê kích thước, số phần tử khác không và độ thưa (Sparsity).

5. **Giải thuật Newton–Raphson & Nhật ký hội tụ (Convergence Telemetry):**
   - Nhật ký chi tiết từng vòng lặp: Sai số tác dụng $\Delta P_{\max}$, sai số phản kháng $\Delta Q_{\max}$, sai số cực đại $\|\Delta S\|_\infty$.
   - Vẽ tự động biểu đồ đường cong hội tụ sai số theo hàm $\log_{10}(\text{mismatch})$ trên HTML5 Canvas.
   - Báo cáo rõ ràng lý do dừng: Đã hội tụ trong dung sai $\epsilon$, vượt quá số vòng lặp tối đa, hoặc ma trận Jacobi suy biến.

6. **Bảng kết quả toàn diện & Kiểm tra giới hạn $Q$ (Q-limit Check):**
   - Bảng kết quả thanh cái: Biên độ áp $|V|$, góc pha $\delta$, công suất nút $P_{net}, Q_{net}$, công suất phát thu hồi tại nút Slack/PV, công suất phụ tải.
   - **Cột kiểm tra giới hạn $Q$:** Cảnh báo nếu công suất phản kháng phát tại nút PV vượt quá dải $[Q_{\min}, Q_{\max}]$.
   - Bảng dòng công suất nhánh: $P_{from}, Q_{from}, P_{to}, Q_{to}$, tổn thất kỹ thuật $\Delta P_{loss}, \Delta Q_{loss}$, kiểm chứng công thức $I^2 R$.
   - Thẻ thống kê tổng hợp: Tổng phát, tổng tải, tổng tổn thất, sai số cân bằng công suất.
   - Một nút bấm **"Xuất toàn bộ kết quả ra CSV"**.

7. **Tích hợp sẵn 2 kịch bản chuẩn:**
   - **Lưới mẫu 3 nút (Task Benchmark):** Nút 1 Slack ($1.0\text{ pu}$), Nút 2 PV ($1.02\text{ pu}, 40\text{ MW}$), Nút 3 PQ ($60\text{ MW}, 25\text{ Mvar}$).
   - **Lưới mẫu 5 nút (Synthetic Case):** Hệ thống 5 nút có tải tại chỗ tại nút máy phát PV.

---

## Cấu trúc thư mục

```
web_app/
├── backend/
│   ├── __init__.py
│   ├── server.py             # Máy chủ FastAPI REST API
│   └── solver_service.py     # Cầu nối giải trào lưu, kiểm tra lỗi và sinh Y-bus
├── frontend/
│   ├── index.html            # Giao diện Single Page Application
│   ├── style.css             # Thiết kế Glassmorphism & Cyber Dispatch hiện đại
│   └── app.js                # Xử lý tương tác SVG, bảng động và gọi API
├── run_app.py                # Script khởi động máy chủ trên cổng 8050
├── run_web_app.cmd           # Shortcut khởi động nhanh trên Windows
└── README.md
```

---

## Hướng dẫn cài đặt và khởi chạy

Ứng dụng chạy trên cổng **8050**, hoàn toàn độc lập nên có thể chạy **song song cùng lúc** với ứng dụng Streamlit hiện có (`http://localhost:8501`) để đối chiếu kết quả.

### Cách 1: Chạy bằng dòng lệnh (Terminal / PowerShell)
```powershell
.venv\Scripts\python.exe web_app/run_app.py
```

### Cách 2: Chạy bằng file thực thi nhanh Windows
Nhấp đúp chuột vào file:
```cmd
web_app\run_web_app.cmd
```

Mở trình duyệt web và truy cập địa chỉ:
👉 **[http://127.0.0.1:8050](http://127.0.0.1:8050)**
