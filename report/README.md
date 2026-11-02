# Thư mục Báo cáo & Tài liệu Đồ án 1 (HUST SEEE)

Thư mục này chứa toàn bộ tài liệu báo cáo và hướng dẫn tính tay cho **Đồ án 1 (Mã học phần: EE3810E)** - **Bộ môn Hệ thống điện, Trường Điện - Điện tử, Đại học Bách khoa Hà Nội**.

---

## 🏆 Tài liệu nộp chính thức hiện tại (Đồ án 1 - Hộp trắng & App PowerFlow)

1. **Báo cáo Đồ án 1 chính thức (Bản chuẩn quy định ĐHBK Hà Nội)**:
   - **File PDF**: [`Bao_Cao_Do_An_1_PowerFlow_29-10-2026.pdf`](Bao_Cao_Do_An_1_PowerFlow_29-10-2026.pdf) *(33+ trang, sơ đồ chuẩn IEEE nét cao, đầy đủ ma trận giải tích và kết quả đối chiếu)*.
   - **File Word (.docx)**: [`Bao_Cao_Do_An_1_PowerFlow_29-10-2026.docx`](Bao_Cao_Do_An_1_PowerFlow_29-10-2026.docx) *(Bản Word định dạng chuẩn để in ấn hoặc chỉnh sửa)*.
   - **Mã nguồn LaTeX**: [`02_Vietnamese_Report/Bao_Cao_Do_An_1_PowerFlow.tex`](02_Vietnamese_Report/Bao_Cao_Do_An_1_PowerFlow.tex)
   - **Script biên dịch tự động**: [`02_Vietnamese_Report/generate_report_do_an_1.py`](02_Vietnamese_Report/generate_report_do_an_1.py)

2. **Tài liệu Đề bài & Hướng dẫn tự tính tay Casio (White-Box Self-Study)**:
   - **File PDF**: [`De_Bai_Tinh_Tay_Newton_Raphson_28-10-2026.pdf`](De_Bai_Tinh_Tay_Newton_Raphson_28-10-2026.pdf) *(4 trang, hướng dẫn từng bước bấm máy Casio fx-580/fx-880 và bảng checkpoints đối chiếu)*.
   - **Mã nguồn LaTeX**: [`De_Bai_Tinh_Tay_Newton_Raphson.tex`](De_Bai_Tinh_Tay_Newton_Raphson.tex)
   - **Script biên dịch**: [`compile_exercise_pdf.py`](compile_exercise_pdf.py)

---

## 📁 Cấu trúc thư mục (Clean & Organized)

```text
report/
├── Bao_Cao_Do_An_1_PowerFlow_29-10-2026.pdf    # [NỘP CHÍNH THỨC] Báo cáo Đồ án 1 (33 trang)
├── Bao_Cao_Do_An_1_PowerFlow_29-10-2026.docx   # [NỘP CHÍNH THỨC] File Word nộp / in ấn
├── De_Bai_Tinh_Tay_Newton_Raphson_28-10-2026.pdf# [HỌC TẬP / VẤN ĐÁP] Đề bài & hướng dẫn tính tay
├── README.md                                  # Hướng dẫn danh mục tài liệu
│
├── 01_English_Report/                         # Bản báo cáo tiếng Anh (HUST English Track)
│   ├── Project_I_Report_HUST_v2.pdf
│   └── generate_hust_report_v2.py
│
├── 02_Vietnamese_Report/                      # Bộ mã nguồn LaTeX & Generator tiếng Việt
│   ├── Bao_Cao_Do_An_1_PowerFlow.tex
│   ├── generate_report_do_an_1.py
│   └── 27-10-2026 Báo cáo.tex
│
├── 03_IEEE_Format/                            # Bài báo tóm tắt 2 cột định dạng IEEE
│   ├── Project_I_Report_IEEE.pdf
│   └── Project_I_Report_IEEE.tex
│
└── 04_Templates/                              # Mẫu chuẩn Bộ môn & ĐHBK Hà Nội
    └── Mẫu ĐATN_2019_version 1_1.docx
```

---

## 🛠 Cách biên dịch lại (Recompiling)

- Để biên dịch lại Báo cáo Đồ án 1 mới:
  ```bash
  python report/02_Vietnamese_Report/generate_report_do_an_1.py
  ```
- Để biên dịch lại Đề bài tính tay:
  ```bash
  python report/compile_exercise_pdf.py
  ```
