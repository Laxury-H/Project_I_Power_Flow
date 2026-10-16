# Hiểu code theo luồng dữ liệu

## 1 Input và kiểm tra
`data_models.read_csv()` đọc hai bảng rồi gọi `validation.validate()`. Bus là vị trí đấu nối; bus ID chỉ là nhãn, không phải chỉ số mảng. Vì vậy `ybus.py` tạo từ điển ID → chỉ số. Dữ liệu pg/pd tách riêng giúp tăng tải mà không vô tình tăng công suất phát. Ví dụ bus 2 mạng 5 bus: pg=0.9, pd=0.1 nên P chỉ định=0.8 pu.

`vm_pu` của Slack/PV là giá trị phải giữ; của PQ là dự đoán ban đầu. `va_deg` của Slack là góc tham chiếu; của các nút còn lại là dự đoán. Ô pg/qg chưa biết dùng số 0 hữu hạn làm placeholder, không có nghĩa nghiệm bằng 0.

## 2 Ybus
`build_ybus()` cộng y=1/(R+jX) vào hai ô đường chéo và trừ y khỏi hai ô ngoài đường chéo. Đường dây song song được cộng nhiều lần. Mô hình không có shunt nên tổng mỗi hàng gần 0. Kiểm tra này không áp dụng nguyên xi khi thêm line charging.

## 3 Công suất và mismatch
`power()` tạo V=vm*exp(1j*va), tính I=Y@V rồi S=V*conj(I). Dấu @ là nhân ma trận; dấu * là nhân từng phần tử. `indices()` xác định ns gồm mọi nút không Slack và pq gồm PQ. `mismatch()` ghép ΔP[ns] với ΔQ[pq], đúng thứ tự biến trạng thái.

## 4 Jacobian
`jacobian()` tính đạo hàm của công suất TÍNH ĐƯỢC. Bốn khối H,N,M,L được tính cho mọi bus rồi rút trích bằng `np.ix_`. Không được đổi dấu Jacobian tùy tiện: mismatch đang là specified − calculated nên giải J dx = mismatch.

## 5 Giải và cập nhật
`solve()` dùng `np.linalg.solve(J,f)`. Phần đầu dx chỉnh góc ns, phần sau chỉnh biên độ pq. Không chỉnh biên độ PV hay Slack. Góc dùng radian trong cả đạo hàm và cập nhật. Sau cập nhật phải tính lại mismatch rồi mới kết luận hội tụ.

## 6 Kết thúc và xử lý lỗi
History luôn chứa trạng thái ban đầu ở k=0. Với max_iterations=0, chương trình chỉ kiểm tra trạng thái đầu. Nếu chưa hội tụ thì trả cờ False. Jacobian suy biến được bắt bằng LinAlgError. Bước tạo điện áp không dương hoặc số không hữu hạn bị từ chối. Không có line search; vì thế một bước bị từ chối không chứng minh mạng vô nghiệm.

## 7 Công suất nhánh
`output_tables()` chỉ nhận nghiệm hội tụ. Với mỗi nhánh, Iij=(Vi−Vj)/Zij, Sij=Vi*conj(Iij)*base. Sji tính tại đầu còn lại, không được đặt bằng −Sij vì đường dây có tổn thất. Tổng hai đầu cho công suất hấp thụ của nhánh. Cột i2r_MW cho phép kiểm tra độc lập công thức tổn thất tác dụng.

## 8 Kiểm thử
`test_jacobian_finite_difference` nhiễu từng biến ±10⁻⁶ để so đạo hàm số và giải tích tại một trạng thái không phẳng. Test singular dùng monkeypatch tạo Jacobian 0: đây là kiểm tra cách xử lý lỗi, không phải một mạng vật lý suy biến đã xác định. `verify_pypower.py` xây dữ liệu tương đương và đối chiếu sáu kịch bản bằng thư viện độc lập.

## 9 CLI và UI
`main.py` chạy sáu kịch bản và lưu CSV/JSON/plots. `app.py` gọi cùng solver; không có phiên bản thuật toán riêng trong UI. AppTest kiểm tra luồng chọn mạng và chạy, chưa thay thế kiểm tra upload/download bằng trình duyệt thật.

## Bài tập tự kiểm tra
Đổi tải bus 3 từ 0.6 lên 0.72 và Q từ 0.25 lên 0.30. Chạy lại rồi giải thích tại sao Slack P và tổn thất thay đổi. Tìm chính xác dòng giữ V2=1.02: đó là cơ chế chỉ cập nhật vm[pq], không phải gán lại sau từng vòng.

## 10. Giữ kết quả UI đúng với dữ liệu
`st.session_state` lưu nghiệm và fingerprint của CSV đã scale cùng các thiết lập. Một rerun với đầu vào không đổi vẫn hiển thị kết quả. Khi đổi input, fingerprint khác nên xóa nghiệm cũ, yêu cầu bấm Run lại. Lỗi input cũng xóa nghiệm cũ. Cơ chế này không sửa thuật toán Newton, chỉ tránh mất hoặc dùng nhầm kết quả trong giao diện. AppTest đã kiểm tra retention, invalidation, tải 120% và trường hợp max updates = 0.
