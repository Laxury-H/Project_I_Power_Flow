"""
Cập nhật generate_report_do_an_1.py với nội dung hoàn chỉnh phản ánh 100% ứng dụng mới PowerFlow (Đồ án 1).
"""
import os

report_script = r"c:\Users\Lax\Downloads\Project_I_Power_Flow\report\02_Vietnamese_Report\generate_report_do_an_1.py"

with open(report_script, "r", encoding="utf-8") as f:
    text = f.read()

# 1. CẬP NHẬT CHƯƠNG 3 TRONG LATEX
old_ch3 = r"""\section{Thiết Kế Đột Phá: Phân Định Rõ Ràng Ẩn Số Và Thông Số Đã Biết}
Một cải tiến vượt bậc của phần mềm PowerFlow nằm ở cơ chế xử lý nhập liệu thông minh trong \texttt{ui\_table\_editor.py}:
\begin{enumerate}
    \item \textbf{Trên bảng hiển thị (Treeview):}
    \begin{itemize}
        \item Nút SLACK: Hai cột phát $P_g, Q_g$ không hiển thị số 0 mà hiển thị nhãn nổi bật \textbf{\texttt{[Ẩn số]}}.
        \item Nút PV: Cột $Q_g$ hiển thị \textbf{\texttt{[Ẩn số]}}, cột góc điện áp hiển thị \textbf{\texttt{[Ẩn: 0°]}}.
        \item Nút PQ: Cột điện áp hiển thị \textbf{\texttt{[Ẩn: 1.0]}}, góc hiển thị \textbf{\texttt{[Ẩn: 0°]}}, hai cột phát $P_g, Q_g$ hiển thị dấu gạch ngang \textbf{\texttt{—}} (không có máy phát).
    \end{itemize}
    \item \textbf{Trong hộp thoại sửa thông số nút (\texttt{BusDialog}):}
    Khi người dùng thay đổi loại nút trong hộp chọn:
    \begin{itemize}
        \item Nếu chọn \texttt{SLACK}: Các ô $P_g, Q_g$ lập tức bị vô hiệu hóa (disabled), hiển thị hướng dẫn: \textit{"U đặt, $\delta=0^\circ$ là hằng số cho trước; $P_g, Q_g$ là ẩn số máy phát tự bù"}.
        \item Nếu chọn \texttt{PV}: Ô góc $\delta$ và ô $Q_g$ bị khóa lại, hướng dẫn: \textit{"$U$ đặt và $P_g$ là thông số cho trước; $Q_g$ và góc $\delta$ là ẩn số cần tìm"}.
        \item Nếu chọn \texttt{PQ}: Ô điện áp $U$, góc $\delta$ và các ô phát bị khóa lại, chỉ mở ô tải $P_d, Q_d$, hướng dẫn: \textit{"Tải $P_d, Q_d$ là thông số cho trước; Điện áp $U$ và góc $\delta$ là ẩn số cần tìm"}.
    \end{itemize}
\end{enumerate}

Thiết kế này bảo đảm tính chặt chẽ tuyệt đối về mặt kỹ thuật, giúp người học nắm vững bản chất bài toán và tự tin giải trình trước hội đồng chấm đồ án."""

new_ch3 = r"""\section{Thiết Kế Đột Phá: Phân Định Rõ Ràng Ẩn Số Và Thông Số Đã Biết}
Một cải tiến vượt bậc và giàu giá trị sư phạm của phần mềm PowerFlow nằm ở cơ chế xử lý nhập liệu thông minh trong \texttt{ui\_table\_editor.py} (Hình~\ref{fig:smart_table}):

\begin{figure}[H]
\centering
\includegraphics[width=0.95\textwidth]{powerflow_smart_table.png}
\caption{Cơ chế phân định rạch ròi bản chất toán học giữa Thông số đã biết và Ẩn số cần tìm trong phần mềm PowerFlow.}
\label{fig:smart_table}
\end{figure}

\begin{enumerate}
    \item \textbf{Trên bảng hiển thị trực quan (Treeview):}
    \begin{itemize}
        \item Nút SLACK: Hai cột phát $P_g, Q_g$ không hiển thị số 0 mà hiển thị nhãn nổi bật \textbf{\texttt{[Ẩn số]}}. Điện áp $U_1 = 1.05\text{ p.u.}$ và góc pha $\delta_1 = 0^\circ$ là thông số cho trước.
        \item Nút PV: Cột $Q_g$ hiển thị \textbf{\texttt{[Ẩn số]}}, cột góc điện áp hiển thị \textbf{\texttt{[Ẩn: 0°]}}, chỉ cho phép hiển thị giá trị đặt $U_i$ và công suất phát ấn định $P_{Gi}$.
        \item Nút PQ: Cột điện áp hiển thị \textbf{\texttt{[Ẩn: 1.0]}}, góc hiển thị \textbf{\texttt{[Ẩn: 0°]}}, hai cột phát $P_g, Q_g$ hiển thị dấu gạch ngang \textbf{\texttt{—}} (vô hiệu hóa do không có máy phát), chỉ hiển thị thông số tải tiêu thụ $P_{Li}, Q_{Li}$.
    \end{itemize}
    \item \textbf{Trong hộp thoại sửa thông số nút (\texttt{BusDialog}):}
    Khi người dùng thay đổi loại nút trong hộp chọn (\texttt{Combobox}):
    \begin{itemize}
        \item Nếu chọn \texttt{SLACK}: Các ô $P_g, Q_g$ lập tức bị vô hiệu hóa (\texttt{disabled}), hiển thị hướng dẫn: \textit{"$U$ đặt, $\delta=0^\circ$ là hằng số cho trước; $P_g, Q_g$ là ẩn số máy phát tự bù"}.
        \item Nếu chọn \texttt{PV}: Ô góc $\delta$ và ô $Q_g$ bị khóa lại, hướng dẫn: \textit{"$U$ đặt và $P_g$ là thông số cho trước; $Q_g$ và góc $\delta$ là ẩn số cần tìm"}.
        \item Nếu chọn \texttt{PQ}: Ô điện áp $U$, góc $\delta$ và các ô phát bị khóa lại, chỉ mở ô tải $P_d, Q_d$, hướng dẫn: \textit{"Tải $P_d, Q_d$ là thông số cho trước; Điện áp $U$ và góc $\delta$ là ẩn số cần tìm"}.
    \end{itemize}
    \item \textbf{Hỗ trợ dán dữ liệu từ Clipboard Excel:}
    Cho phép người dùng sao chép bảng dữ liệu nút hoặc nhánh từ phần mềm Microsoft Excel rồi nhấn phím tắt \texttt{Ctrl+V} để dán trực tiếp vào bảng. Thuật toán tự động chuẩn hóa dấu phẩy thập phân, lọc bỏ khoảng trắng và ánh xạ chính xác vào các trường dữ liệu.
\end{enumerate}

\section{Các Phân Hệ Giao Diện Người Dùng Chuyên Sâu (8 Phân Hệ)}
Phần mềm PowerFlow được trang bị 8 phân hệ chuyên biệt tại khung làm việc bên phải cửa sổ chính:
\begin{enumerate}
    \item \textbf{Tab 1 -- Tổng quan (Executive Dashboard):} Hiển thị các thẻ chỉ số KPI tổng hợp ($\sum P_G, \sum Q_G, \sum P_D, \sum Q_D, \Delta P_{\text{loss}}, \Delta Q_{\text{loss}}$, hệ số công suất $\cos\varphi$), kết hợp hai đồ thị trực quan: biểu đồ phân bố điện áp thanh cái (có dải giới hạn vận hành $[0.95, 1.05\text{ p.u.}]$) và đồ thị quỹ đạo hội tụ sai lệch theo thang đo logarit.
    \item \textbf{Tab 2 -- Sơ đồ lưới điện (Interactive Topology Canvas):} Sơ đồ một sợi trực quan vẽ bằng Canvas, tự động định vị thanh cái, máy phát, phụ tải và hiển thị mũi tên động chỉ hướng dòng công suất thực tế ($P \to$). Hệ thống phân cấp màu sắc cảnh báo mức tải nhiệt đường dây: Xanh lục ($< 80\%$), Vàng cam ($80\% - 100\%$), Đỏ ($> 100\%$).
    \item \textbf{Tab 3 -- Điện áp nút (Bus Voltages):} Bảng tra cứu số liệu điện áp $U_i\text{ (kV, p.u.)}$, góc pha $\delta_i\text{ (độ, rad)}$, công suất phát và phụ tải tại từng thanh cái.
    \item \textbf{Tab 4 -- Công suất nhánh (Branch Flows):} Bảng số liệu chi tiết dòng công suất đầu $P_{ij}, Q_{ij}$, dòng công suất cuối $P_{ji}, Q_{ji}$, tổn thất công suất $\Delta P_{ij}, \Delta Q_{ij}$, dòng điện tải $I_{ij}\text{ (A)}$ và tỷ lệ mang tải phần trăm.
    \item \textbf{Tab 5 -- Phân tích sự cố $N-1$ (Contingency Analysis):} Quét tự động và mô phỏng sự cố sa thải từng đường dây, đánh giá mức độ sụt áp và nguy cơ quá tải dây chuyền.
    \item \textbf{Tab 6 -- So sánh kịch bản (Scenario Comparison):} So sánh đối chiếu trực quan đáp ứng của hệ thống điện giữa các mức phụ tải ($80\%, 100\%, 120\%$) và kịch bản bù công suất phản kháng.
    \item \textbf{Tab 7 -- So chuẩn bộ giải (Solvers Benchmark):} Bảng so sánh tốc độ và độ chính xác giữa 4 phương pháp giải trào lưu: Newton–Raphson, Fast Decoupled (FDPF), Gauss–Seidel (GS) và DC Flow.
    \item \textbf{Tab 8 -- Báo cáo chi tiết (Technical Report):} Xuất văn bản báo cáo kỹ thuật tổng hợp toàn diện các chỉ số trào lưu, có nút "Sao chép toàn bộ" để tích hợp vào thuyết minh.
\end{enumerate}

\section{Hệ Thống Kiểm Thử Tự Động Toàn Diện (55 Unit Tests)}
Để bảo đảm tính ổn định và sự toàn vẹn toán học tuyệt đối, mã nguồn phần mềm trong thư mục \texttt{Đồ án 1} được bảo vệ bởi bộ 55 bài kiểm thử tự động (\texttt{pytest}) chia thành 6 mô-đun:
\begin{itemize}
    \item \texttt{test\_powerflow.py} (17 tests): Kiểm tra thuật toán Newton–Raphson, định luật KCL tại mọi thanh cái, bảo toàn cân bằng công suất toàn lưới, kiểm tra tính đối xứng của ma trận dẫn nạp $\mathbf{Y}_{\text{bus}}$ và đạo hàm giải tích ma trận Jacobian.
    \item \texttt{test\_gui.py} (16 tests): Kiểm tra khởi tạo cửa sổ ứng dụng, chuyển đổi qua lại giữa 8 tabs giao diện, nạp 6 bộ dữ liệu mẫu, và hoạt động của luồng tính toán nền.
    \item \texttt{test\_ui\_upgrades.py} (10 tests): Kiểm tra tính năng dán từ clipboard Excel, hộp thoại \texttt{BusDialog}/\texttt{BranchDialog}, và cơ chế tự động khóa các ô ẩn số cho SLACK, PV, PQ.
    \item \texttt{test\_solvers.py} (5 tests): Kiểm tra tính đúng đắn và tốc độ hội tụ của các thuật toán FDPF, Gauss–Seidel và DC Power Flow.
    \item \texttt{test\_data\_io.py} (5 tests): Kiểm tra xuất nhập dữ liệu tệp JSON, tệp Excel (\texttt{.xlsx}) và tệp CSV chuẩn UTF-8-SIG tự động nhận diện ngôn ngữ.
    \item \texttt{test\_contingency.py} (2 tests): Kiểm tra thuật toán phân tích quét sự cố $N-1$ và tính toán chỉ số rủi ro PI.
\end{itemize}
Toàn bộ 55 bài kiểm thử đều vượt qua với kết quả tuyệt đối: \textbf{55 passed in 10.5s (100\% Passed)}."""

if old_ch3 in text:
    text = text.replace(old_ch3, new_ch3)
    print("Updated Chapter 3 successfully!")

# 2. CẬP NHẬT CHƯƠNG 4 TRONG LATEX
old_ch4_end = r"""\noindent \textbf{Nhận xét vật lý:} Việc bù công suất phản kháng tại chỗ tại thanh cái phụ tải đã giúp điện áp nút 3 được nâng từ $0.9444\text{ p.u.}$ lên $0.9786\text{ p.u.}$, nằm hoàn toàn trong vùng vận hành tối ưu $[0.95, 1.05\text{ p.u.}]$. Đồng thời, do giảm bớt dòng phản kháng truyền tải từ các nguồn phát ở nút 1 và nút 2 về nút 3, tổn thất công suất tác dụng toàn hệ thống giảm mạnh $16.54\%$ ($1.0672\text{ MW}$).

% ==================== CHƯƠNG 5: KẾT LUẬN ====================
\chapter{Kết Luận Và Bài Học Kinh Nghiệm}"""

new_ch4_end = r"""\noindent \textbf{Nhận xét vật lý:} Việc bù công suất phản kháng tại chỗ tại thanh cái phụ tải đã giúp điện áp nút 3 được nâng từ $0.9444\text{ p.u.}$ lên $0.9786\text{ p.u.}$, nằm hoàn toàn trong vùng vận hành tối ưu $[0.95, 1.05\text{ p.u.}]$. Đồng thời, do giảm bớt dòng phản kháng truyền tải từ các nguồn phát ở nút 1 và nút 2 về nút 3, tổn thất công suất tác dụng toàn hệ thống giảm mạnh $16.54\%$ ($1.0672\text{ MW}$).

\subsection{Kịch Bản 3: Đánh Giá An Ninh Hệ Thống Và Sự Cố Đơn Lẻ $N-1$ Bằng Phần Mềm}
Trong vận hành hệ thống điện thực tế, tiêu chuẩn an ninh $N-1$ đòi hỏi lưới điện phải tiếp tục vận hành an toàn, không có phần tử nào bị quá tải nhiệt và điện áp mọi thanh cái phải nằm trong giới hạn cho phép ($U \ge 0.95\text{ p.u.}$) khi xảy ra sự cố ngừng đột ngột một phần tử bất kỳ.

Sử dụng phân hệ \textbf{Sự cố $N-1$} của phần mềm PowerFlow (\texttt{contingency.py}), ta tiến hành mô phỏng tự động sự cố sa thải lần lượt từng đường dây trên lưới 3 nút chuẩn. Kết quả được minh họa trên Hình~\ref{fig:contingency_chart} và tổng hợp trong Bảng~\ref{tab:contingency_results}:

\begin{figure}[H]
\centering
\includegraphics[width=0.92\textwidth]{powerflow_contingency_n1.png}
\caption{Đánh giá an ninh hệ thống điện lưới 3 nút dưới các kịch bản sự cố đơn lẻ $N-1$.}
\label{fig:contingency_chart}
\end{figure}

\begin{table}[H]
\centering
\caption{Kết quả phân tích sự cố đơn lẻ $N-1$ bằng phần mềm PowerFlow trên lưới 3 nút.}
\label{tab:contingency_results}
\resizebox{\textwidth}{!}{\begin{tabular}{ccccccccl}
\toprule
\textbf{Nhánh sự cố} & \textbf{Từ -- Đến} & \textbf{Hội tụ} & \textbf{Số bước} & $U_{\min}\text{ (p.u.)}$ & \textbf{Nút $U_{\min}$} & \textbf{Tải max (\%)} & \textbf{Mức độ rủi ro} & \textbf{Cảnh báo vận hành} \\
\midrule
L23 & $2 - 3$ & Có & 6 & $\mathbf{0.6472}$ & Nút 3 & $\mathbf{208.4\%}$ & \textbf{Nguy cấp (CRITICAL)} & Nhánh L13 quá tải 208\%; Nút 3 sụt áp sâu \\
L13 & $1 - 3$ & Có & 7 & $\mathbf{0.7660}$ & Nút 3 & $\mathbf{168.7\%}$ & \textbf{Nguy cấp (CRITICAL)} & Nhánh L23 quá tải 169\%; L12 quá tải 101\% \\
L12 & $1 - 2$ & Có & 3 & $0.9430$ & Nút 3 & $80.8\%$ & \textbf{Cảnh báo (WARNING)} & Nhánh L13 mang tải cao; Nút 3 sụt áp nhẹ \\
\bottomrule
\end{tabular}}
\end{table}

\noindent \textbf{Nhận xét vật lý và giải trình kỹ thuật:}
\begin{itemize}
    \item \textbf{Khi đứt nhánh L23 ($2-3$):} Toàn bộ phụ tải $120\text{ MW} + j50\text{ Mvar}$ tại nút 3 bị dồn hoàn toàn lên đường dây duy nhất còn lại là L13 ($1-3$). Do trở kháng nhánh L13 lớn ($z_{13} = 0.08 + j0.24\text{ p.u.}$), dòng công suất lớn chạy qua gây tổn thất và sụt áp khủng khiếp: điện áp nút 3 sụt giảm xuống mức nghiêm trọng $0.6472\text{ p.u.}$, đồng thời đường dây L13 bị quá tải nhiệt lên tới $208.4\%$. Đây là sự cố nghiêm trọng nhất (Worst Contingency).
    \item \textbf{Khi đứt nhánh L13 ($1-3$):} Phụ tải nút 3 phải nhận điện từ nguồn máy phát nút 2 qua nhánh L23, đồng thời nút 2 phải nhận công suất truyền tải từ nút 1 qua nhánh L12. Kết quả là cả hai nhánh L12 và L23 đều bị quá tải ($101.0\%$ và $168.7\%$), điện áp nút 3 sụt xuống $0.7660\text{ p.u.}$.
    \item \textbf{Ý nghĩa điều độ:} Kết quả mô phỏng $N-1$ cảnh báo người kỹ sư vận hành rằng lưới 3 nút ở chế độ tải định mức không đạt tiêu chuẩn an toàn $N-1$. Khi xảy ra sự cố trên các nhánh cấp điện về nút 3, hệ thống rơ-le sa thải phụ tải theo tần số/điện áp (UFLS/UVLS) hoặc các bộ tụ bù tĩnh tốc độ cao bắt buộc phải kích hoạt ngay lập tức để tránh hiện tượng sụp đổ điện áp dây chuyền (Voltage Collapse).
\end{itemize}

\subsection{Kịch Bản 4: Đối Sánh Hiệu Năng Giữa 4 Thuật Toán Trào Lưu Công Suất}
Một tính năng nghiên cứu chuyên sâu độc đáo của phần mềm PowerFlow nằm ở phân hệ \textbf{So chuẩn bộ giải} (\texttt{solvers.py}). Phân hệ này cho phép giải đồng thời một lưới điện bằng 4 phương pháp số học kinh điển: Newton–Raphson (NR), Phân tách nhanh (Fast Decoupled - FDPF phiên bản XB), Gauss–Seidel (GS) và Trào lưu một chiều (DC Power Flow).

Hình~\ref{fig:solvers_chart} và Bảng~\ref{tab:solvers_benchmark} tổng hợp kết quả đối sánh toàn diện trên hệ thống điện 3 nút chuẩn:

\begin{figure}[H]
\centering
\includegraphics[width=0.92\textwidth]{powerflow_solvers_benchmark.png}
\caption{Đối sánh số bước lặp và thời gian giải số học giữa 4 thuật toán trào lưu công suất.}
\label{fig:solvers_chart}
\end{figure}

\begin{table}[H]
\centering
\caption{Bảng đối sánh hiệu năng và đặc tính hội tụ giữa 4 thuật toán trào lưu công suất.}
\label{tab:solvers_benchmark}
\resizebox{\textwidth}{!}{\begin{tabular}{lcccccc}
\toprule
\textbf{Thuật toán} & \textbf{Mã hiệu} & \textbf{Số bước lặp} & \textbf{Thời gian CPU} & $\Delta P_{\text{loss}}\text{ (MW)}$ & \textbf{Đặc tính hội tụ} & \textbf{Phạm vi ứng dụng tối ưu} \\
\midrule
\textbf{Newton–Raphson} & NR & \textbf{3 -- 4} & $0.78\text{ ms}$ & $\mathbf{6.452}$ & \textbf{Bậc hai (Quadratic)} & Tiêu chuẩn vàng công nghiệp, độ chính xác cao nhất \\
\textbf{Fast Decoupled} & FDPF & $7$ & $\mathbf{0.27\text{ ms}}$ & $\mathbf{6.452}$ & Hình học (Geometric) & Quét sự cố $N-1$, EMS thời gian thực, lưới $X/R$ cao \\
\textbf{Gauss–Seidel} & GS & $11$ & $0.33\text{ ms}$ & $\mathbf{6.452}$ & Tuyến tính (Linear, chậm) & Minh họa học tập, lưới hình tia đơn giản \\
\textbf{DC Power Flow} & DC & $\mathbf{1}$ & $\mathbf{0.07\text{ ms}}$ & $0.000$ & Tuyến tính (Không lặp) & Thị trường điện, quy hoạch dài hạn, lọc nhanh sự cố \\
\bottomrule
\end{tabular}}
\end{table}

\noindent \textbf{Đánh giá so sánh khoa học:}
\begin{enumerate}
    \item \textbf{Độ chính xác và kết quả hội tụ:} Cả 3 phương pháp xoay chiều chính xác (NR, FDPF, GS) đều hội tụ về cùng một điểm nghiệm vật lý duy nhất với tổn thất chuẩn xác $6.452\text{ MW}$ và điện áp nút 3 $U_3 = 0.9444\text{ p.u.}$. Điều này chứng minh tính đúng đắn và sự đồng quy của bộ thư viện thuật toán trong phần mềm.
    \item \textbf{Tốc độ hội tụ và số bước lặp:} Thuật toán Newton–Raphson thể hiện ưu thế vượt trội với số bước lặp ít nhất (3 bước) nhờ đặc tính hội tụ bậc hai (sai số giảm bình phương sau mỗi bước). Ngược lại, Gauss–Seidel đòi hỏi tới 11 bước lặp do chỉ hội tụ tuyến tính.
    \item \textbf{Thời gian tính toán:} Phương pháp Phân tách nhanh FDPF tận dụng việc tính toán và nghịch đảo ma trận dẫn nạp hằng số $B', B''$ chỉ duy nhất một lần tại bước đầu, giúp thời gian giải giảm xuống chỉ còn $0.27\text{ ms}$ (nhanh hơn gần 3 lần so với việc phải lập lại và nghịch đảo ma trận Jacobian đầy đủ ở mỗi bước của NR). Phương pháp DC Flow giải hệ phương trình đại số tuyến tính chỉ trong $0.07\text{ ms}$, phù hợp tuyệt vời cho các bài toán phân tích hàng triệu kịch bản thị trường điện.
\end{enumerate}

% ==================== CHƯƠNG 5: KẾT LUẬN ====================
\chapter{Kết Luận Và Bài Học Kinh Nghiệm}"""

if old_ch4_end in text:
    text = text.replace(old_ch4_end, new_ch4_end)
    print("Updated Chapter 4 successfully!")

# 3. CẬP NHẬT WORD DOCUMENT GENERATOR (METADATA)
old_word_sections = r"""        ("Chương 3: Thiết kế & Kiến trúc phần mềm PowerFlow (Đồ án 1)", [
            ("3.1 Tổng quan ứng dụng", "Phần mềm Desktop GUI hiện đại viết bằng Python và Tkinter, hỗ trợ đa luồng chống treo giao diện."),
            ("3.2 Thiết kế bảng nhập liệu thông minh", "Tự động phân định rõ thông số cho trước và ẩn số cần tìm, khóa các ô ẩn số cho SLACK/PV/PQ tránh nhầm lẫn số 0."),
            ("3.3 Sơ đồ 1 sợi & Bảng điều khiển KPI", "Trực quan hóa cấu trúc lưới, hướng dòng công suất nhánh và cảnh báo mức tải bằng màu sắc sinh động."),
            ("3.4 Bộ kiểm thử tự động", "Bao gồm 55 unit tests đạt chuẩn 100% Passed bảo đảm tính toàn vẹn của mã nguồn.")
        ]),
        ("Chương 4: Tính toán thủ công từng bước & Đối chiếu chuẩn xác", [
            ("4.1 Hệ thống mẫu 3 nút chuẩn", "S_base = 100 MVA, Nút 1 Slack 1.05 pu, Nút 2 PV 1.04 pu (50 MW), Nút 3 PQ 120 MW + j50 Mvar."),
            ("4.2 Chi tiết tính tay Bước lặp 1", "Thế số chi tiết: Delta P_2 = 0.4827 pu, Delta P_3 = -1.0708 pu, Delta Q_3 = -0.0675 pu, ma trận Jacobian 3x3 và giải ra bước nhảy hiệu chỉnh."),
            ("4.3 Đối chiếu 1:1 với phần mềm PowerFlow", "Khớp chuẩn xác tuyệt đối, độ lệch < 10^-16 pu, hội tụ bậc hai hoàn hảo sau 4 bước lặp."),
            ("4.4 Khảo sát 2 kịch bản vận hành", "Tăng tải 80%-120% (tổn thất tăng bậc hai); Bù tụ ngang 30 Mvar tại nút 3 nâng điện áp từ 0.9444 lên 0.9786 pu và giảm 16.5% tổn thất.")
        ]),"""

new_word_sections = r"""        ("Chương 3: Thiết kế & Kiến trúc phần mềm PowerFlow (Đồ án 1)", [
            ("3.1 Kiến trúc phân tầng 3 lớp", "Phần mềm Desktop GUI hiện đại viết bằng Python/Tkinter đa luồng, lõi giải thuật Newton--Raphson tọa độ cực chính tắc."),
            ("3.2 Thiết kế bảng nhập liệu thông minh", "Tự động phân định rõ thông số cho trước và ẩn số cần tìm, khóa các ô ẩn số cho SLACK/PV/PQ tránh nhầm lẫn số 0; hỗ trợ dán từ Excel."),
            ("3.3 Hệ thống 8 phân hệ chuyên biệt", "Gồm Dashboard KPI, Sơ đồ lưới Canvas tương tác, Bảng điện áp nút, Công suất nhánh, Sự cố N-1, So sánh kịch bản, So chuẩn bộ giải và Báo cáo."),
            ("3.4 Bộ kiểm thử tự động toàn diện", "Bao gồm 55 unit tests đạt chuẩn 100% Passed trên 6 mô-đun kiểm thử bảo đảm tính toàn vẹn của mã nguồn.")
        ]),
        ("Chương 4: Tính toán thủ công từng bước & Đối chiếu chuẩn xác", [
            ("4.1 Hệ thống mẫu 3 nút chuẩn", "S_base = 100 MVA, Nút 1 Slack 1.05 pu, Nút 2 PV 1.04 pu (50 MW), Nút 3 PQ 120 MW + j50 Mvar."),
            ("4.2 Chi tiết tính tay Bước lặp 1", "Thế số chi tiết: Delta P_2 = 0.4827 pu, Delta P_3 = -1.0708 pu, Delta Q_3 = -0.0675 pu, ma trận Jacobian 3x3 và giải ra bước nhảy hiệu chỉnh."),
            ("4.3 Đối chiếu 1:1 với phần mềm PowerFlow", "Khớp chuẩn xác tuyệt đối, độ lệch < 10^-16 pu, hội tụ bậc hai hoàn hảo sau 4 bước lặp."),
            ("4.4 Khảo sát 4 kịch bản vận hành mở rộng", "Tăng tải 80%-120%; Bù tụ tĩnh 30 Mvar; Đánh giá sự cố N-1 đường dây (L12, L13, L23); So chuẩn hiệu năng giữa 4 thuật toán NR, FDPF, GS, DC.")
        ]),"""

if old_word_sections in text:
    text = text.replace(old_word_sections, new_word_sections)
    print("Updated Word chapters metadata successfully!")

# 4. CHÈN HÌNH ẢNH VÀO TỪNG MỤC CỦA TÀI LIỆU WORD
old_img_insert = r"""            if s_title.startswith("4.1"):
                net_img = os.path.join(FIGURES_DIR, "3bus_network_vi.png")
                if os.path.exists(net_img):
                    p_img = doc.add_paragraph()
                    p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
                    p_img.paragraph_format.space_before = Pt(10)
                    p_img.paragraph_format.space_after = Pt(5)
                    doc.add_picture(net_img, width=Inches(5.0))
                    p_cap = doc.add_paragraph()
                    p_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
                    p_cap.paragraph_format.space_after = Pt(15)
                    rc = p_cap.add_run("Hình 4.1: Sơ đồ nguyên lý hệ thống điện mẫu 3 nút (chuẩn IEEE)")
                    rc.font.italic = True
                    rc.font.size = Pt(10)"""

new_img_insert = r"""            # Chèn hình ảnh minh họa tương ứng vào tài liệu Word
            img_map = {
                "2.6": ("algorithm_vi.png", "Hình 2.2: Lưu đồ thuật toán Newton--Raphson tọa độ cực (chuẩn IEEE)", 4.2),
                "3.1": ("powerflow_app_architecture.png", "Hình 3.1: Kiến trúc phân tầng 3 lớp của phần mềm PowerFlow", 5.2),
                "3.2": ("powerflow_smart_table.png", "Hình 3.2: Cơ chế phân định Ẩn số và Thông số cho trước trong bảng nhập liệu", 5.4),
                "4.1": ("3bus_network_vi.png", "Hình 4.1: Sơ đồ một sợi hệ thống điện truyền tải mẫu 3 nút chuẩn", 4.8),
                "4.4": ("powerflow_contingency_n1.png", "Hình 4.2: Đánh giá sự cố đơn lẻ N-1 trên lưới 3 nút", 5.2),
            }
            prefix = s_title[:3]
            if prefix in img_map:
                fname, caption, w_in = img_map[prefix]
                fpath = os.path.join(FIGURES_DIR, fname)
                if os.path.exists(fpath):
                    p_img = doc.add_paragraph()
                    p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
                    p_img.paragraph_format.space_before = Pt(10)
                    p_img.paragraph_format.space_after = Pt(5)
                    doc.add_picture(fpath, width=Inches(w_in))
                    p_cap = doc.add_paragraph()
                    p_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
                    p_cap.paragraph_format.space_after = Pt(15)
                    rc = p_cap.add_run(caption)
                    rc.font.italic = True
                    rc.font.size = Pt(10)"""

if old_img_insert in text:
    text = text.replace(old_img_insert, new_img_insert)
    print("Updated Word image insertion successfully!")

# 5. ĐỒNG BỘ SAO CHÉP
old_main_clean = r"""        clean_auxiliary_files(CURRENT_DIR)
        print("Done! Cleaned auxiliary files.")"""

new_main_clean = r"""        # Đồng bộ hóa với file '27-10-2026 Báo cáo' để bảo đảm người dùng mở file nào cũng là bản mới
        import shutil
        old_named_pdf = os.path.join(REPORT_ROOT, "27-10-2026 Báo cáo.pdf")
        old_local_pdf = os.path.join(CURRENT_DIR, "27-10-2026 Báo cáo.pdf")
        shutil.copy2(PDF_FILE, old_named_pdf)
        shutil.copy2(PDF_FILE, old_local_pdf)
        if os.path.exists(DOCX_FILE):
            shutil.copy2(DOCX_FILE, os.path.join(REPORT_ROOT, "27-10-2026 Báo cáo.docx"))
            shutil.copy2(DOCX_FILE, os.path.join(CURRENT_DIR, "27-10-2026 Báo cáo.docx"))
        print("Synchronized all 27-10-2026 report files to new PowerFlow app standard!")
        clean_auxiliary_files(CURRENT_DIR)
        print("Done! Cleaned auxiliary files.")"""

if old_main_clean in text:
    text = text.replace(old_main_clean, new_main_clean)
    print("Updated main synchronization successfully!")

with open(report_script, "w", encoding="utf-8") as f:
    f.write(text)

print("Saved updated generate_report_do_an_1.py successfully!")
