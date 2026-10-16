# Kịch bản demo và chuẩn bị nộp

## Demo ứng dụng trong khoảng 3 phút

**0:00–0:30 — Bài toán.** Mở app đã khởi động trước. Nói: “This program computes the steady-state bus voltages and branch power flows using a Newton–Raphson solver implemented in NumPy.” Chỉ Slack/PV/PQ trong bảng dữ liệu, nêu base 100 MVA.

**0:30–1:15 — Chạy 3 bus.** Bấm Run ở tải 100%. Chỉ V3 = 0.984385 pu, δ3 ≈ −2.418330°, tổn thất ≈ 2.204693 MW. Nói: “The slack generator balances demand and network losses. The PV voltage magnitude remains fixed.” Không nhầm Q âm của PV là lỗi; nguồn có thể hấp thụ Q trong mô hình này.

**1:15–1:45 — Hội tụ và kiểm chứng.** Chỉ đồ thị log10 mismatch, giải thích 4 cập nhật từ trạng thái k=0. Nói: “Convergence is checked by the maximum power mismatch. I also check the analytical Jacobian, network balance and branch losses.” Chỉ vào kết quả pytest/PYPOWER đã chạy sẵn nếu cần, không cần chạy toàn bộ trong lúc trình bày.

**1:45–2:15 — Thay tải.** Tăng tải lên 120%, chạy lại; tổn thất ≈ 2.834110 MW. Giải thích phụ tải P và Q cùng tăng, lịch phát PV cố định, Slack bù phần thiếu và tổn thất.

**2:15–2:45 — Khả năng dùng lại.** Chọn 5 bus, tải 100%; chạy lại. Nói rõ synthetic educational system. Tải một file CSV nếu đã kiểm tra thành công trên máy demo.

**2:45–3:00 — Giới hạn.** “The current model excludes line charging, transformer taps and generator reactive limits. These results do not establish dynamic stability or equipment feasibility.”

## Dự phòng khi demo có sự cố

- App chưa mở: dùng lệnh trong START_HERE, chờ thông báo địa chỉ local.
- Cổng 8501 đang bận: dừng phiên cũ, hoặc thêm `--server.port 8502` vào lệnh Streamlit.
- Kết quả cũ biến mất khi đổi input: đó là chủ đích; bấm Run lại.
- Mạng tự nhập báo lỗi: quay lại CSV mẫu, kiểm tra đủ cột và đúng dấu tải.
- Không hội tụ: đọc thông báo; đừng tăng max iterations rồi khẳng định mạng vật lý chắc chắn có nghiệm.
- Không chạy được tại buổi bảo vệ: dùng PDF, slide và CSV đã có; nói rõ đây là kết quả chạy trước. Không giả vờ đó là live execution.

## Tự đánh giá trước khi nộp

1. Giải thích được vì sao có đúng 3 biến trạng thái ở mạng 3 bus.
2. Tự tính được y12 và một hàng Ybus.
3. Chỉ đúng đoạn cập nhật góc của non-Slack và điện áp PQ.
4. Giải thích được Jacobian là đạo hàm công suất tính, còn mismatch là specified trừ calculated.
5. Tính được tổng P phát trừ tổng P tải bằng tổn thất.
6. Phân biệt convergence, accuracy và physical feasibility.
7. Nói đúng phần mình đã thực sự đọc, sửa, kiểm thử và hiểu; ghi nhận công cụ hỗ trợ theo quy định học phần.

Nếu chưa làm được một mục, dành buổi học tiếp theo cho mục đó trước khi học thêm tính năng mới.

## Danh sách bàn giao cho GVHD

Kiểm tra hình thức nộp với GVHD. Bộ tài liệu hiện có sẵn Word, PDF, PPTX, source, CSV, log kiểm thử và hướng dẫn. Không tự coi tất cả đều là hồ sơ bắt buộc của học phần. Trong Word tìm các placeholder như `[STUDENT NAME]`, `[STUDENT ID]`, `[CLASS]`, `[SUPERVISOR NAME]`, `[ACADEMIC YEAR]`, `[DATE]` và điền thông tin đúng. Kiểm tra cả bìa slide và ghi chú; xuất PDF lại nếu sửa Word. Giữ một bản dự phòng offline trên máy trình chiếu.
