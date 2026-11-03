"""
Script tạo lưu đồ thuật toán Newton--Raphson tọa độ cực
Đạt chuẩn xuất bản IEEE Transactions:
- Hình học cân đối hoàn hảo (Symmetric Orthogonal Layout)
- Sửa triệt để lỗi logic toán học của bản nháp
- Font chữ kỹ thuật Segoe UI / Arial sắc nét, hỗ trợ tiếng Việt có dấu đầy đủ
- Xuất file vector SVG và raster PNG độ phân giải cao 400 DPI
"""
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, Polygon
import os

def generate_ieee_flowchart(output_png, output_svg=None):
    # Kích thước khung hình theo tỷ lệ vàng chuẩn bài báo khoa học IEEE
    fig = plt.figure(figsize=(10.5, 15.0), dpi=400)
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_xlim(-2, 105)
    ax.set_ylim(0, 150)
    ax.axis('off')

    # Bảng màu chuẩn xuất bản IEEE Monochrome / Black & White
    # 0. Start / End: Đen trắng kỹ thuật
    c_start_fill = '#F8FAFC'
    c_start_edge = '#000000'
    c_start_txt  = '#000000'

    # 1. Đọc dữ liệu: Trắng viền đen
    c_step1_fill = '#FFFFFF'
    c_step1_edge = '#000000'
    c_step1_txt  = '#000000'

    # 2. Khởi tạo phẳng: Trắng viền đen
    c_step2_fill = '#FFFFFF'
    c_step2_edge = '#000000'
    c_step2_txt  = '#000000'

    # 3. Tính công suất & sai lệch: Trắng viền đen
    c_step3_fill = '#FFFFFF'
    c_step3_edge = '#000000'
    c_step3_txt  = '#000000'

    # Khối điều kiện (Hình thoi): Xám nhạt viền đen
    c_cond_fill  = '#F8FAFC'
    c_cond_edge  = '#000000'
    c_cond_txt   = '#000000'

    # 4. Jacobian & Cập nhật: Trắng viền đen
    c_step4_fill = '#FFFFFF'
    c_step4_edge = '#000000'
    c_step4_txt  = '#000000'

    # 5. Đại lượng thứ cấp: Trắng viền đen
    c_step5_fill = '#FFFFFF'
    c_step5_edge = '#000000'
    c_step5_txt  = '#000000'

    # 6. Báo cáo & Kết quả: Trắng viền đen
    c_step6_fill = '#FFFFFF'
    c_step6_edge = '#000000'
    c_step6_txt  = '#000000'

    arrow_col = '#000000'
    font_main = 'Segoe UI'

    # Hàm vẽ hộp chữ nhật bo góc
    def draw_rounded_box(cx, cy, w, h, fill_col, edge_col, radius=1.2, lw=2.2):
        box = FancyBboxPatch(
            (cx - w/2, cy - h/2), w, h,
            boxstyle=f"round,pad=0.2,rounding_size={radius}",
            facecolor=fill_col, edgecolor=edge_col,
            linewidth=lw, zorder=2
        )
        ax.add_patch(box)

    # Hàm vẽ hình thoi kiểm tra điều kiện
    def draw_diamond(cx, cy, w, h, fill_col, edge_col, lw=2.2):
        poly = Polygon([
            (cx, cy + h/2),
            (cx + w/2, cy),
            (cx, cy - h/2),
            (cx - w/2, cy)
        ], closed=True, facecolor=fill_col, edgecolor=edge_col, linewidth=lw, zorder=2)
        ax.add_patch(poly)

    # Hàm vẽ mũi tên trực tiếp
    def draw_direct_arrow(x1, y1, x2, y2, lw=2.0):
        ax.annotate(
            '', xy=(x2, y2), xytext=(x1, y1),
            arrowprops=dict(
                arrowstyle="-|>", color=arrow_col,
                lw=lw, mutation_scale=16,
                shrinkA=0, shrinkB=0
            ), zorder=3
        )

    # ==================== TỌA ĐỘ VÀ KÍCH THƯỚC ====================
    # Trục chính thẳng đứng tại giữa trang: X = 50.0
    MAIN_X = 50.0
    BOX_W  = 62.0   # Chiều rộng các hộp (từ X = 19.0 đến X = 81.0)
    LEFT_E = MAIN_X - BOX_W / 2   # 19.0
    RIGHT_E = MAIN_X + BOX_W / 2  # 81.0

    # ------------------ 0. BẮT ĐẦU ------------------
    y_start = 143.0
    h_start = 6.2
    draw_rounded_box(MAIN_X, y_start, 26.0, h_start, c_start_fill, c_start_edge, radius=3.1)
    ax.text(MAIN_X, y_start, "BẮT ĐẦU", fontsize=12.5, fontweight='bold', fontfamily=font_main,
            color=c_start_txt, ha='center', va='center', zorder=5)

    # Mũi tên 0 -> 1
    draw_direct_arrow(MAIN_X, y_start - h_start/2, MAIN_X, 134.5)

    # ------------------ 1. KHỐI 1: ĐỌC DỮ LIỆU & Y_BUS ------------------
    y_b1 = 129.0
    h_b1 = 11.0
    draw_rounded_box(MAIN_X, y_b1, BOX_W, h_b1, c_step1_fill, c_step1_edge)
    ax.text(MAIN_X, y_b1 + 2.2, "1. Đọc dữ liệu lưới (Nút, Nhánh)",
            fontsize=12, fontweight='bold', fontfamily=font_main, color=c_step1_txt, ha='center', va='center', zorder=5)
    ax.text(MAIN_X, y_b1 - 2.5, r"Thành lập ma trận dẫn nạp nút $\mathbf{Y}_{\mathrm{bus}} = \mathbf{G} + j\mathbf{B}$ (theo KCL)",
            fontsize=11.5, fontfamily=font_main, color=c_step1_txt, ha='center', va='center', zorder=5)

    # Mũi tên 1 -> 2
    draw_direct_arrow(MAIN_X, y_b1 - h_b1/2, MAIN_X, 118.0)

    # ------------------ 2. KHỐI 2: KHỞI TẠO PHẲNG ------------------
    y_b2 = 112.5
    h_b2 = 11.0
    draw_rounded_box(MAIN_X, y_b2, BOX_W, h_b2, c_step2_fill, c_step2_edge)
    ax.text(MAIN_X, y_b2 + 2.2, r"2. Khởi tạo phẳng (Flat Start): đặt bước lặp $m = 0$",
            fontsize=12, fontweight='bold', fontfamily=font_main, color=c_step2_txt, ha='center', va='center', zorder=5)
    ax.text(MAIN_X, y_b2 - 2.5, r"$U_i^{(0)} = 1.0\text{ p.u.}$ (Nút PQ),   $\delta_i^{(0)} = 0.0\text{ rad}$ (Mọi nút $i \neq 1$)",
            fontsize=11.5, fontfamily=font_main, color=c_step2_txt, ha='center', va='center', zorder=5)

    # Mũi tên 2 -> 3
    draw_direct_arrow(MAIN_X, y_b2 - h_b2/2, MAIN_X, 101.5)

    # ------------------ 3. KHỐI 3: TÍNH CÔNG SUẤT & SAI LỆCH ------------------
    y_b3 = 96.0
    h_b3 = 11.0
    draw_rounded_box(MAIN_X, y_b3, BOX_W, h_b3, c_step3_fill, c_step3_edge)
    ax.text(MAIN_X, y_b3 + 2.2, r"3. Tính công suất nút $P_i^{(m)},\; Q_i^{(m)}$",
            fontsize=12, fontweight='bold', fontfamily=font_main, color=c_step3_txt, ha='center', va='center', zorder=5)
    ax.text(MAIN_X, y_b3 - 2.5, r"Xác định sai lệch: $\Delta P_i^{(m)} = P_i^{\mathrm{spec}} - P_i^{(m)},\; \Delta Q_i^{(m)} = Q_i^{\mathrm{spec}} - Q_i^{(m)}$",
            fontsize=11, fontfamily=font_main, color=c_step3_txt, ha='center', va='center', zorder=5)

    # Mũi tên 3 -> Khối điều kiện
    draw_direct_arrow(MAIN_X, y_b3 - h_b3/2, MAIN_X, 85.0)

    # ------------------ KHỐI ĐIỀU KIỆN (DIAMOND): HỘI TỤ ------------------
    y_cond = 78.5
    w_cond = 46.0
    h_cond = 13.0
    draw_diamond(MAIN_X, y_cond, w_cond, h_cond, c_cond_fill, c_cond_edge)
    ax.text(MAIN_X, y_cond + 2.0, r"$\|\mathbf{f}^{(m)}\|_\infty \leq \epsilon$ ?",
            fontsize=12.5, fontweight='bold', fontfamily=font_main, color=c_cond_txt, ha='center', va='center', zorder=5)
    ax.text(MAIN_X, y_cond - 2.5, r"$(\epsilon = 10^{-10}\text{ p.u.})$",
            fontsize=11, fontfamily=font_main, color=c_cond_txt, ha='center', va='center', zorder=5)

    # ------------------ 4. KHỐI 4: JACOBIAN & CẬP NHẬT (KHI CHƯA HỘI TỤ) ------------------
    y_b4 = 58.5
    h_b4 = 15.0
    draw_rounded_box(MAIN_X, y_b4, BOX_W, h_b4, c_step4_fill, c_step4_edge)
    ax.text(MAIN_X, y_b4 + 4.5, r"4. Tính 4 khối ma trận Jacobian $\mathbf{J}^{(m)} = [\mathbf{H}\; \mathbf{N};\; \mathbf{M}\; \mathbf{L}]$",
            fontsize=12, fontweight='bold', fontfamily=font_main, color=c_step4_txt, ha='center', va='center', zorder=5)
    ax.text(MAIN_X, y_b4 + 1.0, r"Giải hệ phương trình đại số tuyến tính: $\mathbf{J}^{(m)} \Delta\mathbf{x}^{(m)} = \Delta\mathbf{f}^{(m)}$",
            fontsize=11.5, fontweight='bold', fontfamily=font_main, color=c_step4_txt, ha='center', va='center', zorder=5)
    ax.text(MAIN_X, y_b4 - 2.5, r"Cập nhật biến trạng thái: $\mathbf{x}^{(m+1)} = \mathbf{x}^{(m)} + \Delta\mathbf{x}^{(m)}$",
            fontsize=11.5, fontfamily=font_main, color=c_step4_txt, ha='center', va='center', zorder=5)
    ax.text(MAIN_X, y_b4 - 5.5, r"Tăng bước lặp: $m \leftarrow m + 1$",
            fontsize=11, fontfamily=font_main, color=c_step4_txt, ha='center', va='center', zorder=5)

    # Mũi tên từ Đáy Diamond đi thẳng xuống Khối 4: CHƯA (SAI)
    draw_direct_arrow(MAIN_X, y_cond - h_cond/2, MAIN_X, y_b4 + h_b4/2)
    # Nhãn "Chưa (Sai)" nằm thoáng sang phải của mũi tên
    ax.text(MAIN_X + 2.5, (y_cond - h_cond/2 + y_b4 + h_b4/2) / 2, "Chưa (Sai)\nChưa hội tụ",
            color='#000000', fontsize=10.5, fontweight='bold', fontfamily=font_main, ha='left', va='center',
            bbox=dict(boxstyle='round,pad=0.25', facecolor='#ffffff', edgecolor='#000000', lw=1.2, alpha=0.95),
            zorder=6)

    # ĐƯỜNG VÒNG LẶP (LOOP BACK) TỪ KHỐI 4 LÊN KHỐI 3 (BÊN TRÁI):
    # Đi từ mép trái Khối 4 (X = LEFT_E = 19.0) rẽ trái ra X = 7.5, đi lên Y = y_b3 = 96.0, rồi đâm vào mép trái Khối 3
    X_LOOP = 7.5
    ax.plot([LEFT_E, X_LOOP], [y_b4, y_b4], color=arrow_col, lw=2.0, zorder=3)
    ax.plot([X_LOOP, X_LOOP], [y_b4, y_b3], color=arrow_col, lw=2.0, zorder=3)
    ax.annotate(
        '', xy=(LEFT_E, y_b3), xytext=(X_LOOP, y_b3),
        arrowprops=dict(
            arrowstyle="-|>", color=arrow_col,
            lw=2.0, mutation_scale=16,
            shrinkA=0, shrinkB=0
        ), zorder=3
    )
    # Nhãn trên đường vòng lặp
    ax.text(X_LOOP, (y_b4 + y_b3)/2, "Vòng lặp\n" + r"($m \leftarrow m+1$)",
            color='#000000', fontsize=10.5, fontweight='bold', fontfamily=font_main, ha='center', va='center',
            bbox=dict(boxstyle='round,pad=0.25', facecolor='#ffffff', edgecolor='#000000', lw=1.2, alpha=0.95),
            zorder=6)

    # ------------------ 5. KHỐI 5: TÍNH TOÁN THỨ CẤP SAU HỘI TỤ ------------------
    y_b5 = 37.0
    h_b5 = 13.0
    draw_rounded_box(MAIN_X, y_b5, BOX_W, h_b5, c_step5_fill, c_step5_edge)
    ax.text(MAIN_X, y_b5 + 3.2, "5. Tính toán các đại lượng vận hành thứ cấp sau hội tụ:",
            fontsize=12, fontweight='bold', fontfamily=font_main, color=c_step5_txt, ha='center', va='center', zorder=5)
    ax.text(MAIN_X, y_b5 - 0.2, r"Dòng công suất nhánh $\dot{S}_{ij}$, Tổn thất công suất $\Delta\dot{S}_{ij}$",
            fontsize=11.5, fontfamily=font_main, color=c_step5_txt, ha='center', va='center', zorder=5)
    ax.text(MAIN_X, y_b5 - 3.5, r"Công suất phát nút SLACK ($P_{G1}, Q_{G1}$) & Kiểm toán cân bằng công suất",
            fontsize=11, fontfamily=font_main, color=c_step5_txt, ha='center', va='center', zorder=5)

    # ĐƯỜNG RẼ HỘI TỤ (ĐẠT / ĐÚNG) TỪ HÌNH THOI XUỐNG KHỐI 5 (BÊN PHẢI):
    # Đi từ đỉnh phải hình thoi (X = MAIN_X + w_cond/2 = 73.0) ra X = 92.5, đi xuống Y = y_b5 = 37.0, đâm vào mép phải Khối 5
    X_BYPASS = 92.5
    x_diamond_right = MAIN_X + w_cond / 2
    ax.plot([x_diamond_right, X_BYPASS], [y_cond, y_cond], color=arrow_col, lw=2.0, zorder=3)
    ax.plot([X_BYPASS, X_BYPASS], [y_cond, y_b5], color=arrow_col, lw=2.0, zorder=3)
    ax.annotate(
        '', xy=(RIGHT_E, y_b5), xytext=(X_BYPASS, y_b5),
        arrowprops=dict(
            arrowstyle="-|>", color=arrow_col,
            lw=2.0, mutation_scale=16,
            shrinkA=0, shrinkB=0
        ), zorder=3
    )
    # Nhãn trên đường rẽ hội tụ
    ax.text(X_BYPASS, (y_cond + y_b5)/2, "Đúng (Đạt)\nĐã hội tụ",
            color='#000000', fontsize=10.5, fontweight='bold', fontfamily=font_main, ha='center', va='center',
            bbox=dict(boxstyle='round,pad=0.25', facecolor='#ffffff', edgecolor='#000000', lw=1.2, alpha=0.95),
            zorder=6)

    # Mũi tên 5 -> 6
    y_b6 = 20.0
    h_b6 = 10.0
    draw_direct_arrow(MAIN_X, y_b5 - h_b5/2, MAIN_X, y_b6 + h_b6/2)

    # ------------------ 6. KHỐI 6: XUẤT KẾT QUẢ ------------------
    draw_rounded_box(MAIN_X, y_b6, BOX_W, h_b6, c_step6_fill, c_step6_edge)
    ax.text(MAIN_X, y_b6 + 1.8, "6. Xuất bảng dữ liệu kết quả & Báo cáo kỹ thuật",
            fontsize=12, fontweight='bold', fontfamily=font_main, color=c_step6_txt, ha='center', va='center', zorder=5)
    ax.text(MAIN_X, y_b6 - 2.2, "Bảng điện áp nút, trào lưu nhánh và cảnh báo giới hạn vận hành",
            fontsize=11, fontfamily=font_main, color=c_step6_txt, ha='center', va='center', zorder=5)

    # Mũi tên 6 -> Kết thúc
    y_end = 6.5
    h_end = 6.2
    draw_direct_arrow(MAIN_X, y_b6 - h_b6/2, MAIN_X, y_end + h_end/2)

    # ------------------ 7. KẾT THÚC ------------------
    draw_rounded_box(MAIN_X, y_end, 26.0, h_end, c_start_fill, c_start_edge, radius=3.1)
    ax.text(MAIN_X, y_end, "KẾT THÚC", fontsize=12.5, fontweight='bold', fontfamily=font_main,
            color=c_start_txt, ha='center', va='center', zorder=5)

    # Lưu hình ảnh chất lượng cao
    plt.savefig(output_png, dpi=400, bbox_inches='tight', pad_inches=0.1)
    print(f"Saved publication-grade PNG to: {output_png}")
    if output_svg:
        plt.savefig(output_svg, format='svg', bbox_inches='tight', pad_inches=0.1)
        print(f"Saved publication-grade SVG to: {output_svg}")
    plt.close()

if __name__ == '__main__':
    out_dir = r"c:\Users\Lax\Downloads\Project_I_Power_Flow\figures"
    out_png = os.path.join(out_dir, "algorithm_vi.png")
    out_svg = os.path.join(out_dir, "algorithm_vi.svg")
    generate_ieee_flowchart(out_png, out_svg)
