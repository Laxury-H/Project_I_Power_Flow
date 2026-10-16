# Kế hoạch học và luyện bảo vệ 7 ngày
Thời lượng đề xuất 2–3 giờ/ngày, điều chỉnh theo nền tảng. Bắt đầu ngày nào thì tính đó là ngày 1.

| Ngày | Việc học và làm | Bằng chứng tự kiểm tra |
|---|---|---|
| 1 | Hỏi GVHD xác nhận đề tài/template; học phasor, P/Q, pu và ba loại bus | Tự viết đại lượng biết/chưa biết và đổi 60 MW sang 0.6 pu |
| 2 | Tính ba dẫn nạp, tự lập Ybus trên giấy; đọc ybus.py | Giải thích dấu âm ngoài đường chéo, tổng hàng 0 |
| 3 | Học S=VI*, P/Q và mismatch; chạy ví dụ 3 bus | Tự tính mismatch ban đầu và xác định 3 biến |
| 4 | Học tuyến tính hóa và Jacobian; xem một vòng lặp thật | Giải thích J dx=ΔS và tại sao dùng radian |
| 5 | Chạy pytest và PYPOWER; xem công suất nhánh, kịch bản tải | Chứng minh Pg=Pd+loss, giải thích Q âm của PV |
| 6 | Đọc báo cáo, sửa thông tin cá nhân; luyện 15 slide trong 10–12 phút | Tự nói không đọc màn hình; trả lời câu 1–20 |
| 7 | Luyện câu khó 21–32; thử demo offline; rà checklist và định dạng GVHD | Chạy lại trên máy nộp, giải thích lỗi không hội tụ, hoàn thiện file nộp |

Mỗi buổi: 20 phút ôn, 60 phút hiểu và tính, 30 phút chạy code, 20 phút nói lại bằng tiếng Anh. Nếu chưa hiểu Jacobian thì giảm thời gian chỉnh màu slide, dành thêm thời gian cho ngày 3–4. Không cần học OPF, dynamics hay short circuit cho phạm vi này.
