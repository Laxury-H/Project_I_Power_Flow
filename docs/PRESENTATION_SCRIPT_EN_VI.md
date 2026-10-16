# Presentation script

Suggested duration: 10–12 minutes; confirm with the supervisor. Adapt claims to actual student contributions.

## Slide 1 — Steady-state AC power flow

**English script:** Good morning. This project develops a Python program for steady-state AC power flow using the Newton–Raphson method. I will explain the mathematical model, the custom solver and the evidence supporting the numerical results. The scope is a balanced series-line network.

**Điểm cần hiểu:** Nói được mục tiêu; bổ sung tên và GVHD trước khi nộp.

## Slide 2 — Why calculate power flow?

**English script:** Demand and scheduled generation do not directly give every voltage or branch flow. Losses depend on current, while current depends on voltage. Power flow resolves this coupled operating point so we can inspect voltages and line power transfers.

**Điểm cần hiểu:** Điện áp chưa biết khiến tổn thất chưa biết; đây là bài toán phi tuyến.

## Slide 3 — Objectives and scope

**English script:** The objective is to build a transparent solver and validate it with reproducible cases. The implementation includes Slack, PV and PQ buses. It uses constant-power demands and series inductive lines. Equipment limits and transient behavior are outside this project.

**Điểm cần hiểu:** Phân biệt mô hình đã có và future work; không khẳng định vận hành thực tế khả thi.

## Slide 4 — The power-flow equations

**English script:** We define net injection as generation minus demand. Current follows I equals Ybus V. Complex power is voltage times conjugate current. The unknown state contains non-reference angles and PQ voltage magnitudes. The three-bus case therefore has three state variables.

**Điểm cần hiểu:** Phải nhớ liên hợp phức và dấu Pg−Pd; góc nội bộ radian.

## Slide 5 — Bus types and network modeling

**English script:** The reference bus fixes magnitude and angle. A PV bus fixes active injection and magnitude, so its reactive injection is an output. A PQ bus fixes both power injections. Each series admittance contributes positively to two diagonal Ybus entries and negatively to the cross entries.

**Điểm cần hiểu:** PV không có phương trình mismatch Q khi vẫn giữ V; một nhánh đóng góp bốn ô Ybus.

## Slide 6 — Newton–Raphson formulation

**English script:** The mismatch is specified power minus calculated power. The Jacobian differentiates calculated injections. Linearization therefore gives J times the correction equals mismatch. We solve this system directly with NumPy, then update only the unknown variables.

**Điểm cần hiểu:** Giải thích được dấu của J; H,N,M,L và không dùng inverse.

## Slide 7 — Iteration and stopping criteria

**English script:** The algorithm validates the data and builds Ybus once. It calculates mismatch at each state. If the tolerance is reached, it exports the solution. Otherwise, it solves the Jacobian system and repeats. A numerical failure or exhausted update budget produces a diagnostic.

**Điểm cần hiểu:** History k=0 là ban đầu; tối đa 30 cập nhật; failure không có nghĩa vô nghiệm.

## Slide 8 — One shared Python solver

**English script:** The project separates input validation, network construction, power evaluation, derivatives and iteration. Both the command-line script and Streamlit interface call this same core. PYPOWER belongs only to the independent verification script. It is not used to generate the project solution.

**Điểm cần hiểu:** Hiểu từng module và dữ liệu qua các bước; không có solver riêng cho UI.

## Slide 9 — Three-bus test system

**English script:** The supplied case has one Slack bus, one PV generator bus and one PQ load. All quantities use a 100 MVA base. The line model contains only series resistance and reactance. The state vector is delta two, delta three and the third-bus voltage magnitude.

**Điểm cần hiểu:** Dữ liệu do đề bài cung cấp, không gán nhãn IEEE.

## Slide 10 — Three-bus solution

**English script:** The load-bus voltage is about 0.984385 per unit. Bus two has a positive angle and the load bus a negative angle. Total active loss is about 2.204693 megawatts. The Slack generation plus 50 megawatts at bus two equals 60 megawatts demand plus loss. The PV bus absorbs reactive power to hold its specified voltage.

**Điểm cần hiểu:** Q âm không nhất thiết sai; chưa kiểm tra giới hạn máy phát.

## Slide 11 — Convergence and verification

**English script:** The nominal three-bus case converges in four Newton updates. The chart displays the base-ten logarithm of maximum mismatch, so lower values indicate smaller error. Thirty-four tests pass. The six PYPOWER comparisons agree to near floating-point precision for these small cases.

**Điểm cần hiểu:** Đồ thị là log10 residual, không đọc giá trị âm thành mismatch âm.

## Slide 12 — Five-bus load variation

**English script:** The second network is synthetic. Demand scales to eighty, one hundred and one hundred twenty percent while generation schedules and voltage setpoints stay fixed. The minimum voltage falls and active losses rise for these cases. This experiment does not establish a stability limit.

**Điểm cần hiểu:** Nói được synthetic và tải PV tăng khiến Pnet giảm.

## Slide 13 — Limitations and next steps

**English script:** A mathematical power-flow solution does not certify real operating feasibility. This model excludes reactive capability, voltage bounds and thermal ratings. The solver is dense and undamped. My first proposed extension is reactive-limit handling with PV-to-PQ switching, followed by additional branch models.

**Điểm cần hiểu:** Các mở rộng chưa làm; không dùng kết quả để nhận xét ổn định động.

## Slide 14 — Conclusions

**English script:** The project connects circuit equations to a transparent Python implementation. Both networks and all six load scenarios are reproducible. The verification evidence supports the algorithm within its stated assumptions. The remaining academic work is supervisor review, personal information completion and demonstrating understanding of the derivation and code.

**Điểm cần hiểu:** Không nhận bộ nháp kỹ thuật là đã được GVHD duyệt; sinh viên phải tự chạy và hiểu.

## Slide 15 — Thank you

**English script:** Thank you for listening. I welcome questions about the model assumptions, the Jacobian, numerical verification or the code. I can also demonstrate one Newton update and explain the limitations of the current implementation.

**Điểm cần hiểu:** Chuẩn bị demo mạng 3 bus và file first_iteration.json; trả lời trung thực phần đã hiểu.
