# Project I Power Flow Report Directory

This directory contains the engineering reports for **Project I (Course Code: EE3810E)** at the **School of Electrical and Electronic Engineering (SEEE), Hanoi University of Science and Technology (HUST)**.

---

## 🏆 Current Official Deliverable (Version 2 - 100% English)

The current official submission report follows the standardized HUST graduation/project report layout (Outer Cover, Inner Sub-cover, Assignment Sheet, Declaration, Acknowledgements, Abstract, TOC, Chapters 1–6, and References) and is written **100% in formal academic English**.

- **PDF Document**: [`Project_I_Report_HUST_v2.pdf`](Project_I_Report_HUST_v2.pdf) (50 pages, publication-grade layout)
- **LaTeX Source**: [`Project_I_Report_HUST_v2.tex`](Project_I_Report_HUST_v2.tex)
- **Word Document**: [`Project_I_Report_HUST_v2.docx`](Project_I_Report_HUST_v2.docx)
- **Build / Generator Script**: [`generate_hust_report_v2.py`](generate_hust_report_v2.py)
  - Run `python generate_hust_report_v2.py` to regenerate both PDF and Word documents and automatically clean up all temporary `.aux`, `.log`, `.toc`, etc. files.

---

## 📁 Thư mục & Báo cáo chính thức (Clean & Organized)

```text
report/
├── Project_I_Report_HUST_v2.pdf               # [NỘP NHANH] Báo cáo tiếng Anh chính thức (48 trang)
├── Project_I_Report_HUST_Vietnamese_v2.pdf    # [NỘP NHANH] Báo cáo tiếng Việt chính thức (38 trang)
├── README.md                                  # Hướng dẫn cấu trúc thư mục
│
├── 01_English_Report/                         # TRỌN BỘ TIẾNG ANH (HUST ENGLISH TRACK)
│   ├── Project_I_Report_HUST_v2.pdf           # Bản PDF nộp chính thức
│   ├── Project_I_Report_HUST_v2.docx          # Bản Word nộp / chỉnh sửa
│   ├── Project_I_Report_HUST_v2.tex           # Mã nguồn LaTeX chuẩn Bách Khoa
│   └── generate_hust_report_v2.py             # Script tự động biên dịch & dọn dẹp
│
├── 02_Vietnamese_Report/                      # TRỌN BỘ TIẾNG VIỆT (HƯỚNG ĐẠI TRÀ / TIẾNG VIỆT)
│   ├── Project_I_Report_HUST_Vietnamese_v2.pdf# Bản PDF nộp chính thức
│   ├── Project_I_Report_HUST_Vietnamese_v2.docx# Bản Word nộp / chỉnh sửa
│   ├── Project_I_Report_HUST_Vietnamese_v2.tex # Mã nguồn LaTeX tiếng Việt
│   └── generate_hust_report_vietnamese.py     # Script tự động biên dịch & dọn dẹp
│
├── 03_IEEE_Format/                            # BÀI BÁO TÓM TẮT CHUẨN IEEE (2-COLUMN)
│   ├── Project_I_Report_IEEE.pdf              # Bản PDF tóm tắt 2 cột IEEE Transactions
│   └── Project_I_Report_IEEE.tex              # Mã nguồn LaTeX IEEE
│
└── 04_Templates/                              # MẪU CHUẨN ĐHBK HÀ NỘI
    └── Mẫu ĐATN_2019_version 1_1.docx         # Mẫu Word gốc của Trường ĐHBK Hà Nội
```

---

## 🛠 Cách biên dịch lại báo cáo (Recompiling)

Mỗi thư mục báo cáo đều có sẵn script Python biên dịch 1 click độc lập, tự động chạy `pdflatex` 2 pass và dọn dẹp toàn bộ file rác (`.aux`, `.log`, `.out`, `.toc`, `.lof`, `.lot`):

- **Biên dịch bản tiếng Anh:**
  ```bash
  python report/01_English_Report/generate_hust_report_v2.py
  ```
- **Biên dịch bản tiếng Việt:**
  ```bash
  python report/02_Vietnamese_Report/generate_hust_report_vietnamese.py
  ```

