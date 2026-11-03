# Đồ án 1: Tính toán trào lưu công suất xác lập bằng phương pháp Newton–Raphson
**Bộ môn Hệ thống điện — Trường Điện - Điện tử — Đại học Bách khoa Hà Nội (HUST SEEE)**

---

## ⚡ 1. Khởi động ứng dụng chính (PowerFlow Desktop GUI)

Ứng dụng chính thức của đồ án được phát triển chuyên sâu cho phương pháp Newton--Raphson tọa độ cực, đặt tại thư mục `Đồ án 1`. Khởi chạy trên Windows:

```bash
# Cách 1: Chạy trực tiếp qua launcher chính
python app.py

# Cách 2: Nhấp đúp vào file batch
CHAY_APP.bat   (hoặc run_windows.cmd)
```

Toàn bộ ứng dụng chạy hoàn toàn độc lập dưới dạng **Desktop GUI (Python / Tkinter)**, không phụ thuộc vào trình duyệt web hay dịch vụ đám mây, khởi động tức thì và hoạt động mượt mà trên Windows/macOS.

---

## 🚀 2. Các tính năng nổi bật của phần mềm PowerFlow

1. **Trình nhập liệu thông minh (Smart Table Input Editor):**
   - Phân định rạch ròi bản chất toán học giữa Thông số đã biết và Ẩn số trạng thái:
     - Nút **SLACK**: Các ô phát $P_g, Q_g$ hiển thị rõ `[Ẩn số]` (tuyệt đối không hiển thị số 0 gây hiểu lầm), điện áp $U=1.05\text{ p.u.}$ và góc $\delta=0^\circ$ cho trước.
     - Nút **PV**: Công suất phản kháng $Q_g$ hiển thị `[Ẩn số]`, góc pha $\delta$ hiển thị `[Ẩn: 0°]`, chỉ cho phép nhập $U$ đặt và $P_g$ phát.
     - Nút **PQ**: Điện áp $U$ và góc pha $\delta$ hiển thị `[Ẩn]`, hai ô phát bị khóa `—`, chỉ cho phép nhập tải tiêu thụ $P_d, Q_d$.
   - Tự động nhận diện dữ liệu dán trực tiếp từ bảng tính Excel (`Ctrl+V`).
2. **Sơ đồ một sợi trực quan (Interactive Single-Line Diagram):**
   - Vẽ động trên Canvas: Thanh cái, nguồn phát, phụ tải và đường dây truyền tải.
   - Hiển thị mũi tên chỉ hướng dòng công suất thực tế ($P \to$).
   - Tự động phân cấp màu sắc theo phần trăm mang tải đường dây: **Xanh lục** ($< 80\%$), **Vàng cam** ($80\% - 100\%$), **Đỏ** ($> 100\%$).
   - Hỗ trợ công cụ thu phóng (Zoom), kéo thả (Pan), và xuất ảnh sơ đồ chất lượng cao.
3. **Bảng điều khiển KPI & Đồ thị (Executive Dashboard):**
   - Thẻ chỉ số tổng quát: Tổng phát $\sum P_G, \sum Q_G$, tổng tải $\sum P_D, \sum Q_D$, tổng tổn thất $\Delta P, \Delta Q$, hệ số công suất $\cos\varphi$.
   - Đồ thị phân bố điện áp nút kèm dải an toàn quy chuẩn $[0.95, 1.05\text{ p.u.}]$.
   - Đồ thị quỹ đạo hội tụ bậc hai qua từng bước lặp theo thang đo logarit.
4. **Hệ thống 6 phân hệ tập trung thuần Newton--Raphson:**
   - **Tab 1 -- Tổng quan (Executive Dashboard):** Thẻ KPI và 2 biểu đồ trực quan.
   - **Tab 2 -- Sơ đồ lưới điện (Interactive Topology Canvas):** Sơ đồ 1 sợi động với mũi tên công suất.
   - **Tab 3 -- Điện áp nút (Bus Voltages):** Bảng điện áp xác lập $U_i, \delta_i$ (độ, rad, kV).
   - **Tab 4 -- Công suất nhánh (Branch Flows):** Bảng dòng công suất $P_{ij}, Q_{ij}$, tổn thất $\Delta P, \Delta Q$, dòng điện tải $I_{ij}\text{ (A)}$.
   - **Tab 5 -- So sánh kịch bản (Scenario Comparison):** Khảo sát biến thiên phụ tải ($80\% - 120\%$) và tụ bù tĩnh $Q_C = 30\text{ Mvar}$.
   - **Tab 6 -- Báo cáo chi tiết (Technical Report):** Văn bản tổng hợp đầy đủ số liệu kèm nút sao chép toàn bộ.

---

## 🧪 3. Kiểm thử tự động (Unit Tests)

Dự án sở hữu bộ **54 bài kiểm thử tự động (Unit Tests)** bảo vệ toàn vẹn giải thuật số học và giao diện:
```bash
pytest
```
*Kết quả:* **`54 passed in 8.59s (100% Passed)`** khẳng định tính toàn vẹn toán học và độ ổn định phần mềm tuyệt đối.

---

## 📚 4. Báo cáo kỹ thuật nộp Đồ án (Tiếng Việt & Tiếng Anh)

Tài liệu báo cáo chính thức được biên soạn bằng LaTeX và Word theo chuẩn quy định của ĐHBK Hà Nội đặt tại thư mục `report/`:
- **Bản tiếng Việt chính thức**:
  - File PDF: [`report/Bao_Cao_Do_An_1_PowerFlow_29-10-2026.pdf`](report/Bao_Cao_Do_An_1_PowerFlow_29-10-2026.pdf) *(34 trang, 2.91 MB)*.
  - File Word: [`report/Bao_Cao_Do_An_1_PowerFlow_29-10-2026.docx`](report/Bao_Cao_Do_An_1_PowerFlow_29-10-2026.docx) *(2.92 MB)*.
- **Bản tiếng Anh chính thức (Elite Track)**:
  - File PDF: [`report/Project_I_Report_HUST_EN_29-10-2026.pdf`](report/Project_I_Report_HUST_EN_29-10-2026.pdf) *(36 trang, 2.89 MB, 0 Overfull warnings)*.
  - File Word: [`report/Project_I_Report_HUST_EN_29-10-2026.docx`](report/Project_I_Report_HUST_EN_29-10-2026.docx) *(2.99 MB)*.
- **Đề bài & Hướng dẫn tự tính tay Casio**:
  - File PDF: [`report/De_Bai_Tinh_Tay_Newton_Raphson_28-10-2026.pdf`](report/De_Bai_Tinh_Tay_Newton_Raphson_28-10-2026.pdf) *(4 trang, 554 KB)*.
- **Lưu đồ giải thuật chuẩn IEEE 400 DPI**:
  - Tiếng Việt: [`figures/algorithm_vi.png`](figures/algorithm_vi.png) & [`figures/algorithm_vi.svg`](figures/algorithm_vi.svg)
  - Tiếng Anh: [`figures/algorithm_en.png`](figures/algorithm_en.png) & [`figures/algorithm_en.svg`](figures/algorithm_en.svg)
