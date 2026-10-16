# Giải thích toán học từ đầu

## Mục tiêu
Biết cấu trúc lưới, công suất tải và điều kiện máy phát; tìm điện áp phức tại các bus. Sau đó tính dòng, công suất truyền và tổn thất. Chế độ xác lập vẫn là AC hình sin; phasor không đổi theo thời gian không có nghĩa điện áp tức thời là DC.

## Per unit
Sbase=100 MVA là công suất ba pha. Nếu chọn Vbase là điện áp dây kV thì Zbase=Vbase²/Sbase (ohm), Ibase=Sbase/(√3 Vbase). Ppu=PMW/100 và Qpu=QMvar/100. Không cần gán kV giả cho bộ dữ liệu đã ở pu; muốn đổi sang kV hoặc A phải biết Vbase phù hợp. Mọi đường dây phải quy đổi cùng cơ sở.

## Quy ước dấu và bus
P=Pg−Pd, Q=Qg−Qd. Bus 3 nhận 60 MW và 25 Mvar nên P3=−0.60, Q3=−0.25 pu. Slack biết V và góc; PV biết P và V; PQ biết P và Q. Một Slack của mạng liên thông vừa làm mốc góc vừa cân bằng phần P chưa biết gồm tổn thất. Số biến là (n−1)+nPQ.

## Lập Ybus từng bước
1/(0.02+j0.06)=5−j15; 1/(0.08+j0.24)=1.25−j3.75; 1/(0.06+j0.18)=1.6666667−j5.
Y11=6.25−j18.75, Y22=6.6666667−j20, Y33=2.9166667−j8.75.
Y12=−5+j15, Y13=−1.25+j3.75, Y23=−1.6666667+j5; các phần tử đối xứng bằng nhau. Không có shunt nên tổng hàng bằng 0. Ybus có thể suy biến do không có điểm đất shunt nhưng Jacobian rút gọn vẫn có thể giải được: ta không nghịch đảo Ybus.

## Từ dòng đến công suất
I=YV và S_i=V_i I_i*. Với V_i=v_i exp(jδ_i), Yij=Gij+jBij, lấy phần thực/ảo thu được:
P_i=v_i Σ_j v_j[Gij cos(δ_i−δ_j)+Bij sin(δ_i−δ_j)].
Q_i=v_i Σ_j v_j[Gij sin(δ_i−δ_j)−Bij cos(δ_i−δ_j)].
Liên hợp phức làm đổi dấu phần ảo của I; bỏ liên hợp sẽ làm sai cả dấu và giá trị công suất.

## Tuyến tính hóa
Đặt c(x) là các công suất tính được và s là giá trị chỉ định. c(x+dx) ≈ c(x)+J dx. Muốn c(x+dx)=s, giải J dx=s−c(x). Vì vậy không cần nghịch đảo J. Hàm solve giải hệ trực tiếp.

## Jacobian đầy đủ
Với i≠j và d=δ_i−δ_j:
H_ij=v_i v_j(Gij sin d−Bij cos d)
N_ij=v_i(Gij cos d+Bij sin d)
M_ij=−v_i v_j(Gij cos d+Bij sin d)
L_ij=v_i(Gij sin d−Bij cos d)
Trên đường chéo:
H_ii=−Q_i−Bii v_i²
N_ii=P_i/v_i+Gii v_i
M_ii=P_i−Gii v_i²
L_ii=Q_i/v_i−Bii v_i
H=dP/dδ, N=dP/dv, M=dQ/dδ, L=dQ/dv. Chỉ lấy hàng P không Slack, hàng Q của PQ, cột góc không Slack và cột v của PQ.

## Một vòng lặp thật của mạng 3 bus
x0=[0,0,1] theo thứ tự [δ2 rad,δ3 rad,v3 pu].
Mismatch ban đầu = [0.619, -0.504166667, 0.0375].
Jacobian =
[[21.165     -5.1       -1.7      ]
 [-5.1        9.0375     2.8208333]
 [ 1.7       -3.0125     8.4625   ]]
Giải được dx = [0.0182090762, -0.0411766209, -0.0138847858].
Vậy x1 = [0.0182090762, -0.0411766209, 0.9861152142].
Ở đây δ2 ≈ 1.0433°, δ3 ≈ −2.3592° và v3≈0.986115. Đây mới là bước đầu, KHÔNG phải nghiệm cuối. Lặp đến khi max(abs(mismatch))<10⁻¹⁰ pu. File first_iteration.json giữ số chưa làm tròn.

## Hiểu nghiệm cuối
V3=0.984384736 pu, δ2=1.024098283°, δ3=−2.418329585°. Tổn thất P=2.204692942 MW. Slack phát 12.204692942 MW, cộng bus 2 phát 50 MW bằng tải 60 MW cộng tổn thất.
Bus 2 có Qg=−46.193053410 Mvar: máy phát đang hấp thụ Q để giữ V2=1.02 trong mô hình. Dấu âm này không tự động là lỗi. Nhưng chưa biết giới hạn Q máy phát nên chưa thể khẳng định chế độ vận hành thực tế khả thi. Slack Q=77.807132236 Mvar bù tải và hấp thụ phản kháng của đường dây.

## Tổn thất và xác minh
Sij+Sji=|Iij|²(R+jX)*Sbase. P là nhiệt tổn hao điện trở; phần Q là công suất phản kháng đường dây hấp thụ, không gọi là năng lượng nhiệt mất đi. Kiểm tra cả mismatch, tổng công suất, I²R, Jacobian số và thư viện độc lập. Chỉ nhìn chữ Converged chưa đủ.

## Giới hạn diễn giải
V giảm và tổn thất tăng trong các kịch bản đã chạy. Không suy rộng thành quy luật tuyệt đối cho mọi lưới. Không dùng ba điểm tải để kết luận giới hạn ổn định điện áp; cần continuation và ràng buộc thiết bị. Power flow không chứng minh ổn định động.
