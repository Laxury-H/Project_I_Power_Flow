# Defense questions and answers

32 questions. Short English answers are rehearsal aids; Vietnamese explanations provide the reasoning. Adapt first-person claims to actual work performed.

## 1. Why is power flow analysis important?

Level: Basic

**English answer:** It calculates steady-state voltages, branch flows and losses for specified generation and demand.

**Giải thích:** Power flow cho biết trạng thái xác lập của lưới. Biết tải chưa đủ biết điện áp vì điện áp và dòng liên quan qua trở kháng, còn tổn thất phụ thuộc dòng.

## 2. What does steady state mean here?

Level: Basic

**English answer:** Balanced sinusoidal operation is represented by phasors that do not change with time.

**Giải thích:** Đại lượng tức thời vẫn hình sin. Chỉ biên độ và góc phasor không đổi; không phải hệ DC và không xét quá trình quá độ.

## 3. What is the difference between Slack, PV and PQ buses?

Level: Basic

**English answer:** Slack specifies voltage magnitude and angle; PV specifies active injection and magnitude; PQ specifies active and reactive injections.

**Giải thích:** Mỗi nút có bốn đại lượng P,Q,V,δ. Slack tìm P,Q; PV tìm Q,δ; PQ tìm V,δ. Nhớ đại lượng biết trước để chọn đúng phương trình.

## 4. Why is one Slack bus necessary?

Level: Basic

**English answer:** It sets the angle reference and balances the unknown active-power loss in this connected network.

**Giải thích:** Không thể chỉ định toàn bộ P phát và tải khi chưa biết tổn thất. Một Slack gánh phần chênh lệch. Mạng nhiều đảo cần xử lý từng đảo; chương trình hiện chỉ nhận một đảo.

## 5. What is the per-unit system?

Level: Basic

**English answer:** It expresses a physical quantity as a ratio to a consistent base value.

**Giải thích:** Trên Sbase=100 MVA, 60 MW là 0.6 pu. Zbase=Vbase²/Sbase với Vbase điện áp dây. Phải đồng nhất cơ sở trước khi tính.

## 6. What sign convention do you use?

Level: Basic

**English answer:** Net injection equals generation minus demand.

**Giải thích:** Tải 60 MW,25 Mvar có Pnet=−0.6,Qnet=−0.25 pu. CSV ghi pd,qd dương; code tự lấy pg−pd và qg−qd.

## 7. How is Ybus constructed?

Level: Basic

**English answer:** Each line admittance is added to two diagonal entries and subtracted from two off-diagonal entries.

**Giải thích:** Từ Ii=Σyij(Vi−Vj), hệ số Vi dương và hệ số Vj âm. Dùng y=1/(R+jX), không dùng trực tiếp Z.

## 8. What is complex power?

Level: Basic

**English answer:** Complex power is S=VI*, with active power as its real part and reactive power as its imaginary part.

**Giải thích:** Liên hợp dòng điện là bắt buộc. Trong code S=V*np.conj(Y@V); dấu nhân * là từng phần tử, @ là nhân ma trận.

## 9. Which quantities are input and output?

Level: Basic

**English answer:** Inputs describe topology, impedance, demand and controlled generation; outputs include voltages, injections and branch losses.

**Giải thích:** Input không chứa đáp án V3. V3=1 là dự đoán đầu cho PQ. Phải phân biệt setpoint Slack/PV và giá trị khởi tạo PQ.

## 10. What is the main three-bus result?

Level: Basic

**English answer:** The load voltage is 0.984384736 pu and active loss is 2.204692942 MW on a 100 MVA base.

**Giải thích:** Góc δ2≈1.024098°, δ3≈−2.418330°. Số này được tính bởi main.py; không hardcode trong solver.

## 11. Why use Newton–Raphson?

Level: Intermediate

**English answer:** It solves the coupled nonlinear equations with an explicit Jacobian and converges rapidly near a regular solution.

**Giải thích:** Chọn NR vì dễ liên hệ đạo hàm, đại số tuyến tính và code. Không nói luôn hội tụ; NR phụ thuộc điểm đầu và điều kiện bài toán.

## 12. What is the Jacobian matrix?

Level: Intermediate

**English answer:** It contains derivatives of calculated active and reactive injections with respect to unknown angles and magnitudes.

**Giải thích:** H=dP/dδ,N=dP/dV,M=dQ/dδ,L=dQ/dV. Jacobian mô tả công suất thay đổi xấp xỉ bao nhiêu khi điện áp thay đổi nhỏ.

## 13. Which variables are updated?

Level: Intermediate

**English answer:** All non-Slack angles and only PQ voltage magnitudes are updated.

**Giải thích:** Mạng 3 bus có x=[δ2,δ3,V3]. V1,δ1,V2 không được chỉnh. Code dùng va[ns] và vm[pq].

## 14. Why is reactive power not specified at a PV bus?

Level: Intermediate

**English answer:** Reactive injection adjusts to maintain the specified voltage magnitude.

**Giải thích:** Nếu vừa khóa P,V,Q tại PV mà không thêm biến thì dễ thừa phương trình. Khi có Q limit, thường phải khóa Q ở giới hạn và chuyển PV thành PQ; hiện chưa triển khai.

## 15. How many state variables are there?

Level: Intermediate

**English answer:** There are nPV+2nPQ variables for one connected Slack bus.

**Giải thích:** Tương đương n−1+nPQ. Mạng 3 bus:1+2=3; mạng 5 bus:1+2×3=7.

## 16. Why does your update use J dx equals mismatch?

Level: Intermediate

**English answer:** The mismatch is specified minus calculated power, while J differentiates calculated power.

**Giải thích:** Tuyến tính hóa c(x+dx)≈c(x)+Jdx=s, suy ra Jdx=s−c. Nếu định nghĩa mismatch ngược lại phải đổi dấu vế phải.

## 17. Why do you use radians internally?

Level: Intermediate

**English answer:** The trigonometric derivative formulas assume radians.

**Giải thích:** Nhập và xuất góc độ cho dễ đọc. Dùng np.deg2rad trước khi tính và np.rad2deg khi xuất. Không cộng correction radian vào góc độ.

## 18. Why solve the linear system instead of forming an inverse?

Level: Intermediate

**English answer:** A direct linear solve avoids explicitly constructing the inverse and is the appropriate numerical operation.

**Giải thích:** np.linalg.solve(J,f) trả correction. Không cần np.linalg.inv(J)@f, vừa dư việc vừa kém thuận lợi về số học.

## 19. What does convergence mean?

Level: Intermediate

**English answer:** The largest selected active or reactive mismatch is below the stated tolerance.

**Giải thích:** Tolerance 10⁻¹⁰ pu. Kiểm tra sau khi cập nhật; iteration 0 là trạng thái ban đầu. Hội tụ không đồng nghĩa lưới đáp ứng giới hạn thiết bị.

## 20. How do you know the solution is correct?

Level: Intermediate

**English answer:** I check residuals, analytical derivatives, network balance, I²R losses and agreement with PYPOWER.

**Giải thích:** Có 34 test pytest, thêm 6 so sánh PYPOWER. Đây là xác minh triển khai trong cùng mô hình, chưa là đối chiếu đo đạc lưới thật.

## 21. Why do transmission lines have active losses?

Level: Advanced

**English answer:** Series resistance dissipates power equal to I squared R.

**Giải thích:** Tính cả Sij và Sji; tổng P hai đầu là tổn thất. Tổng Q là hấp thụ phản kháng do X, không coi Q là nhiệt tiêu tán.

## 22. Why does voltage decrease when load increases?

Level: Advanced

**English answer:** For these cases, higher current through series impedance increases voltage drops at PQ buses.

**Giải thích:** Kết luận giới hạn ở các case đã chạy. Với bù Q, điều khiển tap hoặc nguồn phân tán, xu hướng có thể khác. PV/Slack giữ nguyên V theo giả thiết.

## 23. What happens if the Jacobian is singular?

Level: Advanced

**English answer:** The linear solve fails and the program returns a diagnostic instead of declaring convergence.

**Giải thích:** Code bắt LinAlgError. Test dùng Jacobian 0 được tiêm để kiểm tra handler, không phải một lưới thực suy biến. Có thể xem lại topology, reference, initialization và conditioning.

## 24. Does non-convergence prove that no solution exists?

Level: Advanced

**English answer:** No. It may reflect a poor starting point, numerical conditioning or an unsuitable iteration method.

**Giải thích:** Solver không damping, không continuation. Một bước tạo V âm sẽ bị dừng. Không được lấy thất bại NR làm bằng chứng sụp đổ điện áp.

## 25. Why is the PV reactive generation negative?

Level: Advanced

**English answer:** The voltage-controlled bus absorbs reactive power to maintain its specified magnitude in this model.

**Giải thích:** Mạng 3 bus Qg2≈−46.193 Mvar. Dấu âm hợp lệ về toán nhưng phải có giới hạn khả năng máy phát mới kết luận khả thi vật lý.

## 26. Is your five-bus case a standard benchmark?

Level: Advanced

**English answer:** No. It is a documented synthetic educational test system.

**Giải thích:** Không gọi IEEE 5 bus. Dữ liệu được công bố đầy đủ CSV, có local load tại PV để kiểm tra net injection.

## 27. How do you scale demand?

Level: Advanced

**English answer:** I scale both active and reactive demand while holding scheduled generation and controlled voltages fixed.

**Giải thích:** Cả pd và qd nhân 0.8,1,1.2 nên giữ power factor. Bus PV có tải tại chỗ thì Pnet đổi dù Pg giữ nguyên.

## 28. Can these cases establish a voltage stability limit?

Level: Advanced

**English answer:** No. Three steady-state load scenarios do not locate a stability boundary.

**Giải thích:** Cần continuation power flow, ràng buộc thiết bị và phân tích phù hợp. Cũng không suy ra ổn định động từ nghiệm xác lập.

## 29. Why can Ybus be singular while the power-flow solution exists?

Level: Advanced

**English answer:** A series-only Ybus has zero row sums, but the solver uses a reduced nonlinear system with a voltage reference.

**Giải thích:** Ta không giải V=inv(Ybus)I. Jacobian rút gọn có thể khả nghịch tại nghiệm mặc dù Ybus nguyên thủy suy biến.

## 30. What are the limitations of the program?

Level: Advanced

**English answer:** It excludes charging, taps, reactive limits and operating ratings, and uses dense undamped Newton steps.

**Giải thích:** Chỉ một mạng liên thông cân bằng, R≥0,X>0, tải PQ không đổi. Không hỗ trợ unbalanced, OPF, faults hay transient stability.

## 31. What exactly did you implement yourself?

Level: Advanced

**English answer:** The package exposes custom Ybus, power equations, an analytical Jacobian, Newton updates and branch calculations; I must describe my actual contribution accurately.

**Giải thích:** Đây là bộ code/báo cáo có AI hỗ trợ. Khi bảo vệ, chỉ nhận phần mình thực sự đã hiểu, sửa và kiểm chứng; giải thích PYPOWER chỉ dùng đối chiếu. Điền nhật ký đóng góp thật, không học câu nhận toàn bộ code là tự viết.

## 32. What would you improve first?

Level: Advanced

**English answer:** I would add and verify reactive-limit enforcement with PV-to-PQ switching.

**Giải thích:** Ưu tiên khả thi vận hành trước giao diện đẹp. Sau đó mới charging/tap, sparse matrices và damping. Các chức năng này đang là future work, không phải đã có.
