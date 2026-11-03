"""
Script vẽ 2 phương án lưu đồ chuẩn xuất bản IEEE:
Phương án 1 (Vertical Bypass): Xếp 8 khối dọc từ trên xuống dưới, vòng lặp bên trái, nhánh hội tụ bên phải.
Phương án 2 (Side-Loop): Trục chính đi thẳng từ Đầu -> 1 -> 2 -> 3 -> Thoi -> 5 -> 6 -> Cuối.
                         Khối 4 nằm trên nhánh lặp khép kín bên phải (3 -> Thoi -> 4 -> 3).
"""
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, Polygon
import os

font_main = 'Segoe UI'
arrow_col = '#1E293B'

def draw_rounded_box(ax, cx, cy, w, h, fill_col, edge_col, radius=1.2, lw=2.2):
    box = FancyBboxPatch(
        (cx - w/2, cy - h/2), w, h,
        boxstyle=f"round,pad=0.2,rounding_size={radius}",
        facecolor=fill_col, edgecolor=edge_col,
        linewidth=lw, zorder=2
    )
    ax.add_patch(box)

def draw_diamond(ax, cx, cy, w, h, fill_col, edge_col, lw=2.2):
    poly = Polygon([
        (cx, cy + h/2),
        (cx + w/2, cy),
        (cx, cy - h/2),
        (cx - w/2, cy)
    ], closed=True, facecolor=fill_col, edgecolor=edge_col, linewidth=lw, zorder=2)
    ax.add_patch(poly)

def draw_arrow(ax, x1, y1, x2, y2, lw=2.0):
    ax.annotate(
        '', xy=(x2, y2), xytext=(x1, y1),
        arrowprops=dict(
            arrowstyle="-|>", color=arrow_col,
            lw=lw, mutation_scale=16,
            shrinkA=0, shrinkB=0
        ), zorder=3
    )

# ==================== PHƯƠNG ÁN 2: SIDE-LOOP CHUẨN IEEE ====================
def make_side_loop(out_png, out_svg=None):
    fig = plt.figure(figsize=(11.5, 14.5), dpi=400)
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_xlim(0, 115)
    ax.set_ylim(0, 145)
    ax.axis('off')

    # Bảng màu IEEE
    c_start_fill, c_start_edge, c_start_txt = '#E8F5E9', '#2E7D32', '#1B5E20'
    c_step1_fill, c_step1_edge, c_step1_txt = '#E0F2F1', '#00695C', '#004D40'
    c_step2_fill, c_step2_edge, c_step2_txt = '#E1F5FE', '#0277BD', '#01579B'
    c_step3_fill, c_step3_edge, c_step3_txt = '#EDE7F6', '#5E35B1', '#311B92'
    c_cond_fill,  c_cond_edge,  c_cond_txt  = '#FFF9C4', '#EF6C00', '#B7410E'
    c_step4_fill, c_step4_edge, c_step4_txt = '#FFEBEE', '#C62828', '#880E4F'
    c_step5_fill, c_step5_edge, c_step5_txt = '#F3E5F5', '#7B1FA2', '#4A148C'
    c_step6_fill, c_step6_edge, c_step6_txt = '#E8EAF6', '#303F9F', '#1A237E'

    # Trục chính nằm ở X = 43.0
    MAIN_X = 43.0
    BOX_W  = 58.0
    LEFT_E = MAIN_X - BOX_W/2  # 14.0
    RIGHT_E = MAIN_X + BOX_W/2 # 72.0

    # 0. BẮT ĐẦU
    y_start = 138.0
    draw_rounded_box(ax, MAIN_X, y_start, 26.0, 6.2, c_start_fill, c_start_edge, radius=3.1)
    ax.text(MAIN_X, y_start, "BẮT ĐẦU", fontsize=12.5, fontweight='bold', fontfamily=font_main,
            color=c_start_txt, ha='center', va='center', zorder=5)
    draw_arrow(ax, MAIN_X, y_start - 3.1, MAIN_X, 130.0)

    # 1. ĐỌC DỮ LIỆU
    y_b1 = 124.5
    h_b1 = 11.0
    draw_rounded_box(ax, MAIN_X, y_b1, BOX_W, h_b1, c_step1_fill, c_step1_edge)
    ax.text(MAIN_X, y_b1 + 2.2, "1. Đọc dữ liệu lưới (Nút, Nhánh)",
            fontsize=12, fontweight='bold', fontfamily=font_main, color=c_step1_txt, ha='center', va='center', zorder=5)
    ax.text(MAIN_X, y_b1 - 2.5, r"Thành lập ma trận dẫn nạp nút $\mathbf{Y}_{\mathrm{bus}} = \mathbf{G} + j\mathbf{B}$ (theo KCL)",
            fontsize=11.5, fontfamily=font_main, color=c_step1_txt, ha='center', va='center', zorder=5)
    draw_arrow(ax, MAIN_X, y_b1 - h_b1/2, MAIN_X, 113.5)

    # 2. KHỞI TẠO PHẲNG
    y_b2 = 108.0
    h_b2 = 11.0
    draw_rounded_box(ax, MAIN_X, y_b2, BOX_W, h_b2, c_step2_fill, c_step2_edge)
    ax.text(MAIN_X, y_b2 + 2.2, r"2. Khởi tạo phẳng (Flat Start): đặt bước lặp $m = 0$",
            fontsize=12, fontweight='bold', fontfamily=font_main, color=c_step2_txt, ha='center', va='center', zorder=5)
    ax.text(MAIN_X, y_b2 - 2.5, r"$U_i^{(0)} = 1.0\text{ p.u.}$ (Nút PQ),   $\delta_i^{(0)} = 0.0\text{ rad}$ (Mọi nút $i \neq 1$)",
            fontsize=11.5, fontfamily=font_main, color=c_step2_txt, ha='center', va='center', zorder=5)
    draw_arrow(ax, MAIN_X, y_b2 - h_b2/2, MAIN_X, 97.0)

    # 3. TÍNH CÔNG SUẤT VÀ SAI LỆCH
    y_b3 = 91.5
    h_b3 = 11.0
    draw_rounded_box(ax, MAIN_X, y_b3, BOX_W, h_b3, c_step3_fill, c_step3_edge)
    ax.text(MAIN_X, y_b3 + 2.2, r"3. Tính công suất nút $P_i^{(m)},\; Q_i^{(m)}$",
            fontsize=12, fontweight='bold', fontfamily=font_main, color=c_step3_txt, ha='center', va='center', zorder=5)
    ax.text(MAIN_X, y_b3 - 2.5, r"Xác định sai lệch: $\Delta P_i^{(m)} = P_i^{\mathrm{spec}} - P_i^{(m)},\; \Delta Q_i^{(m)} = Q_i^{\mathrm{spec}} - Q_i^{(m)}$",
            fontsize=11, fontfamily=font_main, color=c_step3_txt, ha='center', va='center', zorder=5)
    draw_arrow(ax, MAIN_X, y_b3 - h_b3/2, MAIN_X, 80.5)

    # ĐIỀU KIỆN HỘI TỤ (DIAMOND)
    y_cond = 74.0
    w_cond = 40.0
    h_cond = 13.0
    draw_diamond(ax, MAIN_X, y_cond, w_cond, h_cond, c_cond_fill, c_cond_edge)
    ax.text(MAIN_X, y_cond + 2.0, r"$\|\mathbf{f}^{(m)}\|_\infty \leq \epsilon$ ?",
            fontsize=12.5, fontweight='bold', fontfamily=font_main, color=c_cond_txt, ha='center', va='center', zorder=5)
    ax.text(MAIN_X, y_cond - 2.5, r"$(\epsilon = 10^{-10}\text{ p.u.})$",
            fontsize=11, fontfamily=font_main, color=c_cond_txt, ha='center', va='center', zorder=5)

    # ---------- NHÁNH HỘI TỤ (ĐÚNG): ĐI THẲNG XUỐNG KHỐI 5 ----------
    y_b5 = 48.0
    h_b5 = 13.0
    draw_arrow(ax, MAIN_X, y_cond - h_cond/2, MAIN_X, y_b5 + h_b5/2)
    # Nhãn Đúng
    ax.text(MAIN_X + 6.8, (y_cond - h_cond/2 + y_b5 + h_b5/2)/2, "Đúng\n(Hội tụ)",
            color='#2E7D32', fontsize=10.5, fontweight='bold', fontfamily=font_main, ha='center', va='center',
            bbox=dict(boxstyle='round,pad=0.25', facecolor='#ffffff', edgecolor='#2E7D32', lw=1.2, alpha=0.95),
            zorder=6)

    # 5. KHỐI 5: TÍNH TOÁN THỨ CẤP
    draw_rounded_box(ax, MAIN_X, y_b5, BOX_W, h_b5, c_step5_fill, c_step5_edge)
    ax.text(MAIN_X, y_b5 + 3.2, "5. Tính toán các đại lượng vận hành thứ cấp sau hội tụ:",
            fontsize=12, fontweight='bold', fontfamily=font_main, color=c_step5_txt, ha='center', va='center', zorder=5)
    ax.text(MAIN_X, y_b5 - 0.2, r"Dòng công suất nhánh $\dot{S}_{ij}$, Tổn thất công suất $\Delta\dot{S}_{ij}$",
            fontsize=11.5, fontfamily=font_main, color=c_step5_txt, ha='center', va='center', zorder=5)
    ax.text(MAIN_X, y_b5 - 3.5, r"Công suất phát nút SLACK ($P_{G1}, Q_{G1}$) & Cân bằng công suất",
            fontsize=11, fontfamily=font_main, color=c_step5_txt, ha='center', va='center', zorder=5)

    # Mũi tên 5 -> 6
    y_b6 = 29.5
    h_b6 = 10.0
    draw_arrow(ax, MAIN_X, y_b5 - h_b5/2, MAIN_X, y_b6 + h_b6/2)

    # 6. KHỐI 6: XUẤT KẾT QUẢ
    draw_rounded_box(ax, MAIN_X, y_b6, BOX_W, h_b6, c_step6_fill, c_step6_edge)
    ax.text(MAIN_X, y_b6 + 1.8, "6. Xuất bảng dữ liệu kết quả & Báo cáo kỹ thuật",
            fontsize=12, fontweight='bold', fontfamily=font_main, color=c_step6_txt, ha='center', va='center', zorder=5)
    ax.text(MAIN_X, y_b6 - 2.2, "Bảng điện áp nút, trào lưu nhánh và cảnh báo vận hành",
            fontsize=11, fontfamily=font_main, color=c_step6_txt, ha='center', va='center', zorder=5)

    # Mũi tên 6 -> Kết thúc
    y_end = 14.5
    h_end = 6.2
    draw_arrow(ax, MAIN_X, y_b6 - h_b6/2, MAIN_X, y_end + h_end/2)

    # 7. KẾT THÚC
    draw_rounded_box(ax, MAIN_X, y_end, 26.0, h_end, c_start_fill, c_start_edge, radius=3.1)
    ax.text(MAIN_X, y_end, "KẾT THÚC", fontsize=12.5, fontweight='bold', fontfamily=font_main,
            color=c_start_txt, ha='center', va='center', zorder=5)

    # ---------- NHÁNH LẶP (SAI / CHƯA HỘI TỤ): RẼ PHẢI VÀO KHỐI 4 ----------
    X_STEP4 = 92.5
    W_STEP4 = 39.0
    H_STEP4 = 17.0
    Y_STEP4 = 74.0
    x_diamond_right = MAIN_X + w_cond/2 # 43 + 20 = 63.0

    # Mũi tên từ đỉnh phải Diamond sang mép trái Khối 4
    x_step4_left = X_STEP4 - W_STEP4/2 # 92.5 - 19.5 = 73.0
    draw_arrow(ax, x_diamond_right, y_cond, x_step4_left, Y_STEP4)
    # Nhãn Chưa (Sai)
    ax.text((x_diamond_right + x_step4_left)/2, y_cond + 2.5, "Chưa (Sai)\nChưa hội tụ",
            color='#C62828', fontsize=10, fontweight='bold', fontfamily=font_main, ha='center', va='center',
            bbox=dict(boxstyle='round,pad=0.2', facecolor='#ffffff', edgecolor='#C62828', lw=1.2, alpha=0.95),
            zorder=6)

    # Vẽ Khối 4
    draw_rounded_box(ax, X_STEP4, Y_STEP4, W_STEP4, H_STEP4, c_step4_fill, c_step4_edge)
    ax.text(X_STEP4, Y_STEP4 + 5.2, r"4. Tính ma trận Jacobian $\mathbf{J}^{(m)}$",
            fontsize=11.5, fontweight='bold', fontfamily=font_main, color=c_step4_txt, ha='center', va='center', zorder=5)
    ax.text(X_STEP4, Y_STEP4 + 2.0, r"(4 khối giải tích $\mathbf{H}, \mathbf{N}, \mathbf{M}, \mathbf{L}$)",
            fontsize=10.5, fontfamily=font_main, color=c_step4_txt, ha='center', va='center', zorder=5)
    ax.text(X_STEP4, Y_STEP4 - 1.8, r"Giải hệ: $\mathbf{J}^{(m)} \Delta\mathbf{x}^{(m)} = \Delta\mathbf{f}^{(m)}$",
            fontsize=11, fontweight='bold', fontfamily=font_main, color=c_step4_txt, ha='center', va='center', zorder=5)
    ax.text(X_STEP4, Y_STEP4 - 5.5, r"Cập nhật: $\mathbf{x}^{(m+1)} = \mathbf{x}^{(m)} + \Delta\mathbf{x}^{(m)}$" "\n" r"Tăng bước lặp: $m \leftarrow m + 1$",
            fontsize=10.5, fontfamily=font_main, color=c_step4_txt, ha='center', va='center', zorder=5)

    # ĐƯỜNG VÒNG TỪ ĐỈNH KHỐI 4 LÊN KHỐI 3:
    y_step4_top = Y_STEP4 + H_STEP4/2 # 74 + 8.5 = 82.5
    ax.plot([X_STEP4, X_STEP4], [y_step4_top, y_b3], color=arrow_col, lw=2.0, zorder=3)
    ax.annotate(
        '', xy=(RIGHT_E, y_b3), xytext=(X_STEP4, y_b3),
        arrowprops=dict(
            arrowstyle="-|>", color=arrow_col,
            lw=2.0, mutation_scale=16,
            shrinkA=0, shrinkB=0
        ), zorder=3
    )
    # Nhãn vòng lặp
    ax.text(X_STEP4, (y_step4_top + y_b3)/2, "Vòng lặp\n" + r"($m \leftarrow m+1$)",
            color='#C62828', fontsize=10, fontweight='bold', fontfamily=font_main, ha='center', va='center',
            bbox=dict(boxstyle='round,pad=0.25', facecolor='#ffffff', edgecolor='#C62828', lw=1.2, alpha=0.95),
            zorder=6)

    # Lưu hình ảnh
    plt.savefig(out_png, dpi=400, bbox_inches='tight', pad_inches=0.1)
    if out_svg:
        plt.savefig(out_svg, format='svg', bbox_inches='tight', pad_inches=0.1)
    plt.close()
    print(f"Saved side-loop to {out_png}")

if __name__ == '__main__':
    make_side_loop("scratch/flowchart_side_loop.png")

