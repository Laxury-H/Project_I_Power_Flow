# BẮT ĐẦU TỪ ĐÂY — Đồ án 1 Power Flow

## 1. Bạn nhận được gì?

- `report/Project_I_Report.docx`: báo cáo tiếng Anh 25 trang, sửa được.
- `report/Project_I_Report.pdf`: bản xuất tương ứng với Word.
- `slides/Project_I_Defense.pptx`: 15 slide tiếng Anh, có lời nói mẫu trong Notes.
- `app.py`: giao diện chạy trên trình duyệt; `main.py`: tái lập sáu kịch bản.
- `src/`: thuật toán Newton–Raphson tự viết; `data/`: dữ liệu CSV.
- `results/`: kết quả thực tính, lịch sử hội tụ, bằng chứng kiểm thử.
- `docs/`: giải thích tiếng Việt, 32 câu hỏi bảo vệ song ngữ, kịch bản nói, kế hoạch 7 ngày và checklist.

**Điểm bắt đầu:** giải nén ZIP hoàn toàn, đọc tài liệu này, chạy ví dụ 3 bus, rồi đọc `docs/MATHEMATICAL_WALKTHROUGH_VI.md`. Không chạy chương trình ngay bên trong cửa sổ xem ZIP.

## 2. Cài và chạy trên Windows

Cần Python 3.12. Mở Terminal trong thư mục có `app.py`. Nếu đã cài Python, kiểm tra bằng `py -3.12 --version`. Nếu lệnh không nhận, cài Python 3.12 hoặc dùng đúng đường dẫn Python đã có trên máy; không cần quyền Administrator cho môi trường ảo trong thư mục cá nhân.

Bạn có thể nhấp đúp `setup_windows.cmd` để tạo môi trường và cài các gói; lần đầu cần Internet. Sau khi thấy thông báo cài thành công, nhấp đúp `run_windows.cmd` để mở ứng dụng. Hai file CMD là tiện ích tùy chọn, chưa được chạy trên Windows trong môi trường kiểm chứng này.

Các lệnh tương đương để tự thực hiện:

```bat
py -3.12 -m venv .venv
.venv\Scripts\python.exe -m pip install -r requirements.txt
.venv\Scripts\python.exe -m streamlit run app.py
```

Không cần activate môi trường; vì vậy không cần thay đổi PowerShell ExecutionPolicy. Giữ cửa sổ Terminal mở khi dùng ứng dụng. Nếu trình duyệt không tự mở, nhập `http://localhost:8501`. Để dừng, quay lại Terminal và bấm Ctrl+C.

## 3. macOS / Linux

```bash
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
.venv/bin/python -m streamlit run app.py
```

Nếu Python thiếu module venv, cài gói venv phù hợp với Python của hệ điều hành. Không cần triển khai lên cloud để bảo vệ đồ án; chạy local là đủ.

## 4. Chạy demo đầu tiên

1. Chọn `3bus`; chưa cần upload file.
2. Giữ Base power = 100 MVA, Demand scale = 100%, tolerance = 1e-10, Maximum Newton updates = 30.
3. Bấm **Run power flow**. Kết quả mong đợi: hội tụ sau 4 cập nhật; tổn thất hiển thị **2.204693 MW**.
4. Đọc hàng bus 3: V khoảng **0.984385 pu**, góc khoảng **−2.418330°**. Góc bus 2 khoảng **+1.024098°**.
5. Tải lần lượt ba CSV: bus results, branch results, convergence. Kết quả giữ nguyên sau khi tải hoặc khi Streamlit chạy lại với đầu vào không đổi.
6. Đổi tải lên 120%: bảng kết quả cũ biến mất để tránh nhầm. Bấm chạy lại, tổn thất khoảng **2.834110 MW**.
7. Chọn `5bus`, đưa tải về 100%, bấm chạy lại: tổn thất khoảng **3.650487 MW**, điện áp nhỏ nhất khoảng **0.968039 pu**. Đây là mạng tự thiết kế cho học tập, không phải IEEE benchmark.

Đồ thị hội tụ dùng log10 của mismatch để thấy rõ mức giảm; CSV vẫn lưu mismatch gốc theo pu. Hàng iteration = 0 là trạng thái khởi tạo, không phải một lần cập nhật Newton.

## 5. Upload dữ liệu của bạn

Upload **cả hai file**: Bus CSV và Line CSV. Khi mới có một file, ứng dụng yêu cầu bổ sung file còn lại; đó là hành vi dự kiến. Có thể thử ngay `data/buses_3bus.csv` và `data/lines_3bus.csv` trước khi sửa dữ liệu.

| Bus CSV | Ý nghĩa |
|---|---|
| bus | ID nút nguyên, không trùng |
| type | Slack, PV hoặc PQ |
| pg_pu, qg_pu | Công suất phát trên cùng cơ sở công suất |
| pd_pu, qd_pu | Phụ tải, nhập số không âm |
| vm_pu | Điện áp đặt Slack/PV; dự đoán ban đầu tại PQ |
| va_deg | Góc tham chiếu Slack; dự đoán góc tại các nút khác |

Line CSV có đúng bốn cột: `from_bus,to_bus,r_pu,x_pu`. Mô hình yêu cầu R ≥ 0, X > 0, một lưới liên thông và đúng một Slack. Không thêm cột tap hoặc line charging vì mô hình chưa hỗ trợ chúng.

Ví dụ tải 60 MW + j25 Mvar trên base 100 MVA: nhập `pd_pu=0.60,qd_pu=0.25`; không nhập phụ tải âm. Net injection được chương trình tính bằng phát trừ tải. `pg_pu/qg_pu` của Slack và `qg_pu` của PV là placeholder hữu hạn; chương trình tính lại các đại lượng chưa biết.

**Base power trong UI là cơ sở đổi kết quả pu sang MW/Mvar.** Nếu chỉ đổi base mà giữ nguyên CSV pu, đó là cùng bài toán pu với quy mô công suất khác. Chương trình không tự đổi cơ sở trở kháng và không tự chuyển dữ liệu của một hệ vật lý từ base cũ sang base mới.

## 6. Kiểm tra upload/download trong trình duyệt của bạn

Các thao tác này chưa được xác minh bằng trình duyệt thật trong môi trường bàn giao. Thực hiện trước ngày demo:

| Thao tác | Kết quả mong đợi |
|---|---|
| Upload riêng Bus CSV | Có cảnh báo yêu cầu cả hai CSV; không hiện kết quả cũ |
| Upload đủ hai CSV 3bus | Đọc đúng 3 bus và 3 nhánh |
| Chạy ở tải 100% | Tổn thất 2.204693 MW |
| Tải bus_results.csv | Có 3 hàng bus; V3 khoảng 0.984385 |
| Tải branch_results.csv | Có 3 hàng nhánh; tổng p_loss_MW khoảng 2.204693 |
| Tải convergence.csv | Có 5 hàng iteration 0–4; mismatch cuối < 1e-10 |
| Đổi tải rồi bấm chạy | Có kết quả của mức tải mới, không giữ bảng cũ |
| Đặt maximum updates = 0 rồi chạy | Báo Maximum iterations reached; không xuất nghiệm thành công |

Khi mở CSV bằng Excel, dùng Data → From Text/CSV và chọn dấu phẩy nếu toàn bộ hàng bị dồn vào một cột. Dấu thập phân trong CSV là dấu chấm.

## 7. Tái lập kiểm thử và kết quả

Trên Windows, ở thư mục dự án:

```bat
.venv\Scripts\python.exe -m pytest -q --junitxml=results/tests.xml
.venv\Scripts\python.exe verify_pypower.py
.venv\Scripts\python.exe main.py
```

Trên macOS/Linux, thay `.venv\Scripts\python.exe` bằng `.venv/bin/python`. Lệnh `main.py` ghi lại bảng và hình trong `results/` và `figures/`; nên giữ một bản ZIP gốc nếu muốn so sánh. Nếu thay dữ liệu, Word và PowerPoint không tự cập nhật: cần sửa bảng, hình và nhận xét tương ứng trước khi xuất lại PDF.

Bằng chứng bàn giao: 34 kiểm thử đạt; 6 kịch bản đã đối chiếu với PYPOWER. PYPOWER chỉ dùng để kiểm chứng; solver chính vẫn dùng NumPy. Không coi số kiểm thử đạt là bảo đảm cho mọi mạng hoặc mọi mức tải.

## 8. Trình tự học và luyện bảo vệ

- Đọc `docs/MATHEMATICAL_WALKTHROUGH_VI.md`: hiểu P, Q, V, góc pha và Ybus.
- Đọc `docs/CODE_EXPLANATION_VI.md` đồng thời mở các module trong `src/`.
- Tự giải thích vòng cập nhật đầu tiên từ `results/first_iteration.json`.
- Dùng `docs/PRESENTATION_SCRIPT_EN_VI.md` để luyện nói theo từng slide.
- Tự trả lời `docs/DEFENSE_QA_EN_VI.md` trước khi xem đáp án.
- Thực hiện lịch trong `docs/7_DAY_STUDY_PLAN.md`.
- Xem `docs/DEMO_AND_SUBMISSION_VI.md` để chạy thử buổi bảo vệ.

## 9. Những việc chỉ bạn và GVHD có thể chốt

Điền tên, MSSV, lớp, GVHD, năm học và ngày nộp; xác nhận đề tài, template, quy trình nộp và thời lượng bảo vệ. Mở PowerPoint trên máy trình chiếu để kiểm tra Notes, font và biểu đồ. Sau khi sửa Word, cập nhật mục lục tĩnh/số trang và xuất lại PDF. Bộ file là nền tảng đã có kết quả kỹ thuật kiểm chứng, chưa phải bằng chứng GVHD đã duyệt hoặc sinh viên đã hiểu toàn bộ.
