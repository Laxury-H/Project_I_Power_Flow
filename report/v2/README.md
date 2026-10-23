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

## 📁 Directory Structure & Archives

```text
report/
├── Project_I_Report_HUST_v2.pdf      # [PRIMARY DELIVERABLE] 100% English HUST Report
├── Project_I_Report_HUST_v2.docx     # Formatted Microsoft Word version
├── Project_I_Report_HUST_v2.tex      # LaTeX source code
├── generate_hust_report_v2.py        # Automated generator & clean build script
├── README.md                         # This guide
│
├── v2/                               # Standalone mirror of V2 English release
│   ├── Project_I_Report_HUST_v2.pdf
│   ├── Project_I_Report_HUST_v2.docx
│   ├── Project_I_Report_HUST_v2.tex
│   └── generate_hust_report_v2.py
│
├── v1/                               # Preliminary Version 1 reports
│   ├── Project_I_Report.pdf
│   ├── Project_I_Report.docx
│   ├── Project_I_Report_HUST.tex
│   ├── generate_latex.py
│   └── generate_word.py
│
├── v2_bilingual_draft/               # Archive of early bilingual / draft versions
│   ├── Project_I_Report_HUST_v2_bilingual.pdf
│   ├── Project_I_Report_HUST_v2_bilingual.tex
│   └── generate_hust_report_v2_bilingual.py
│
├── vietnamese/                       # Dedicated Vietnamese-language reports
│   ├── Project_I_Report_HUST_Vietnamese.pdf
│   ├── Project_I_Report_HUST_Vietnamese.docx
│   └── generate_hust_report.py
│
├── ieee_format/                      # IEEE Conference Paper 2-column format
│   ├── Project_I_Report_IEEE.pdf
│   └── Project_I_Report_IEEE.tex
│
└── templates/                        # University official templates
    └── Mẫu ĐATN_2019_version 1_1.docx
```

---

## 🛠 Recompiling the LaTeX Report

To recompile the report from LaTeX, simply execute:
```bash
python generate_hust_report_v2.py
```
This script runs `pdflatex` twice to resolve all internal page references, Table of Contents, List of Figures, and List of Tables, and automatically cleans up auxiliary log and cache files (`.aux`, `.log`, `.out`, `.toc`, `.lof`, `.lot`).
