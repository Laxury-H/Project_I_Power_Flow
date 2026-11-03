# Thư mục Báo cáo & Tài liệu Đồ án 1 (HUST SEEE)

Thư mục này chứa toàn bộ tài liệu báo cáo, đề bài tính tay và mã nguồn biên dịch cho **Đồ án 1 (Mã học phần: EE3810E)** - **Bộ môn Hệ thống điện, Trường Điện - Điện tử, Đại học Bách khoa Hà Nội**.

---

## 🏆 Tài liệu nộp chính thức (Bản chuẩn 100% Newton--Raphson & Hộp trắng)

### 1. Báo cáo tiếng Việt (Official Vietnamese Report)
- **File PDF**: [`Bao_Cao_Do_An_1_PowerFlow_29-10-2026.pdf`](Bao_Cao_Do_An_1_PowerFlow_29-10-2026.pdf) (hoặc [`Bao_Cao_Do_An_1_PowerFlow.pdf`](Bao_Cao_Do_An_1_PowerFlow.pdf) / [`27-10-2026 Báo cáo.pdf`](27-10-2026%20Báo%20cáo.pdf))
  - *Dung lượng: 2.91 MB, 34 trang, chuẩn quy định ĐHBK Hà Nội*.
  - *Tập trung 100% vào phương pháp Newton--Raphson tọa độ cực, mô hình đường dây $\pi$ có $B_0$, 8 công thức đạo hàm riêng giải tích ma trận Jacobian, tính tay Bước 1 trên Casio fx-580/fx-880, đối chiếu 1:1 với app PowerFlow ($< 10^{-16}\text{ p.u.}$), hội tụ bậc hai 4 bước lặp, kiểm toán cân bằng năng lượng, và 2 kịch bản vận hành thực tế*.
- **File Word (.docx)**: [`Bao_Cao_Do_An_1_PowerFlow_29-10-2026.docx`](Bao_Cao_Do_An_1_PowerFlow_29-10-2026.docx) *(2.92 MB, bảng biểu định dạng chuẩn in ấn và nộp lưu chiểu)*.
- **Mã nguồn LaTeX**: [`02_Vietnamese_Report/Bao_Cao_Do_An_1_PowerFlow.tex`](02_Vietnamese_Report/Bao_Cao_Do_An_1_PowerFlow.tex)
- **Script tự động biên dịch**: [`02_Vietnamese_Report/generate_report_do_an_1.py`](02_Vietnamese_Report/generate_report_do_an_1.py)

### 2. Báo cáo tiếng Anh (Official English Report - HUST Elite Track)
- **File PDF**: [`Project_I_Report_HUST_EN_29-10-2026.pdf`](Project_I_Report_HUST_EN_29-10-2026.pdf) (hoặc [`Project_I_Report_HUST_EN.pdf`](Project_I_Report_HUST_EN.pdf))
  - *Dung lượng: 2.89 MB, 36 trang, biên dịch chuẩn xác 0 Overfull warnings, 0 lỗi cú pháp*.
  - *Nội dung chuẩn hóa 1:1 theo bản tiếng Việt: White-Box methodology, Casio hand calculation, 1:1 cross-validation, asymptotic quadratic convergence proof, 6-tab Desktop GUI architecture, Smart Table editor, 54 automated unit tests (100% Passed)*.
- **File Word (.docx)**: [`Project_I_Report_HUST_EN_29-10-2026.docx`](Project_I_Report_HUST_EN_29-10-2026.docx) (hoặc [`Project_I_Report_HUST_EN.docx`](Project_I_Report_HUST_EN.docx)) *(2.99 MB, bảng số liệu và hình ảnh tiếng Anh độ phân giải 350-400 DPI)*.
- **Mã nguồn LaTeX**: [`01_English_Report/Project_I_Report_HUST_EN.tex`](01_English_Report/Project_I_Report_HUST_EN.tex)
- **Script tự động biên dịch**: [`01_English_Report/generate_report_en.py`](01_English_Report/generate_report_en.py)

### 3. Đề bài & Hướng dẫn tự tính tay Casio (White-Box Self-Study)
- **File PDF**: [`De_Bai_Tinh_Tay_Newton_Raphson_28-10-2026.pdf`](De_Bai_Tinh_Tay_Newton_Raphson_28-10-2026.pdf) *(554 KB, 4 trang, hướng dẫn từng bước bấm máy Casio fx-580/fx-880 và bảng checkpoints đối chiếu bảo vệ đồ án)*.
- **Mã nguồn LaTeX**: [`De_Bai_Tinh_Tay_Newton_Raphson.tex`](De_Bai_Tinh_Tay_Newton_Raphson.tex)
- **Script biên dịch**: [`compile_exercise_pdf.py`](compile_exercise_pdf.py)

---

## 📁 Cấu trúc thư mục (Clean & Organized Layout)

```text
report/
├── Bao_Cao_Do_An_1_PowerFlow_29-10-2026.pdf    # [NỘP CHÍNH THỨC - VI] Báo cáo tiếng Việt (2.91 MB)
├── Bao_Cao_Do_An_1_PowerFlow_29-10-2026.docx   # [NỘP CHÍNH THỨC - VI] File Word tiếng Việt (2.92 MB)
├── Project_I_Report_HUST_EN_29-10-2026.pdf    # [NỘP CHÍNH THỨC - EN] Báo cáo tiếng Anh (2.89 MB)
├── Project_I_Report_HUST_EN_29-10-2026.docx   # [NỘP CHÍNH THỨC - EN] File Word tiếng Anh (2.99 MB)
├── 27-10-2026 Báo cáo.pdf                      # [ĐỒNG BỘ] Đồng bộ hoàn toàn với bản tiếng Việt chính thức
├── 27-10-2026 Báo cáo.docx                     # [ĐỒNG BỘ] Đồng bộ hoàn toàn với bản Word tiếng Việt
├── De_Bai_Tinh_Tay_Newton_Raphson_28-10-2026.pdf# [VẤN ĐÁP] Đề bài và hướng dẫn tính tay Casio
├── README.md                                  # Tài liệu thuyết minh danh mục
│
├── 01_English_Report/                         # Báo cáo tiếng Anh chính thức
│   ├── Project_I_Report_HUST_EN.tex          # Mã nguồn LaTeX tiếng Anh chuẩn
│   ├── Project_I_Report_HUST_EN.pdf          # PDF tiếng Anh
│   ├── Project_I_Report_HUST_EN.docx         # Word tiếng Anh
│   └── generate_report_en.py                 # Script tự động biên dịch bản tiếng Anh
│
├── 02_Vietnamese_Report/                      # Báo cáo tiếng Việt chính thức
│   ├── Bao_Cao_Do_An_1_PowerFlow.tex         # Mã nguồn LaTeX tiếng Việt chuẩn
│   ├── Bao_Cao_Do_An_1_PowerFlow.pdf         # PDF tiếng Việt
│   ├── Bao_Cao_Do_An_1_PowerFlow.docx        # Word tiếng Việt
│   └── generate_report_do_an_1.py            # Script tự động biên dịch bản tiếng Việt
│
├── 03_IEEE_Format/                            # Bài báo khoa học tóm tắt 2 cột định dạng IEEE
│   ├── Project_I_Report_IEEE.pdf
│   └── Project_I_Report_IEEE.tex
│
└── 04_Templates/                              # Mẫu văn bản ĐHBK Hà Nội
    └── Mẫu ĐATN_2019_version 1_1.docx
```

---

## 🛠 Hướng dẫn biên dịch lại (How to Recompile)

```bash
# 1. Biên dịch lại toàn bộ hình ảnh chất lượng cao (Việt & Anh, 350-400 DPI):
python build_all_figures_perfect.py

# 2. Biên dịch Báo cáo tiếng Việt (PDF & Word):
python report/02_Vietnamese_Report/generate_report_do_an_1.py

# 3. Biên dịch Báo cáo tiếng Anh (PDF & Word, 0 Overfull warnings):
python report/01_English_Report/generate_report_en.py

# 4. Biên dịch Đề bài tính tay Casio:
python report/compile_exercise_pdf.py
```
