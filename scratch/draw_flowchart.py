"""
Tạo hình ảnh Flowchart thuật toán Newton--Raphson tọa độ cực
Chuẩn xuất bản IEEE Transactions (sắc nét, không răng cưa, toán học chính xác 100%).
"""
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, Polygon, FancyArrowPatch
import matplotlib.lines as mlines
import os

def create_flowchart(output_png, output_svg=None):
    # Thiết lập kích thước đồ thị (tỷ lệ chuẩn A4 / IEEE)
    fig = plt.figure(figsize=(10.5, 14.5), dpi=350)
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 140)
    ax.axis('off')
    
    # Bảng màu IEEE Technical
    c_start_fill = '#E8F5E9'
    c_start_edge = '#1B5E20'
    c_start_txt  = '#0A3D0A'
    
    c_step1_fill = '#E0F2F1'
    c_step1_edge = '#004D40'
    c_step1_txt  = '#00332C'
    
    c_step2_fill = '#E1F5FE'
    c_step2_edge = '#01579B'
    c_step2_txt  = '#002F6C'
    
    c_step3_fill = '#EDE7F6'
    c_step3_edge = '#4A148C'
    c_step3_txt  = '#260057'
    
    c_cond_fill  = '#FFF9C4'
    c_cond_edge  = '#E65100'
    c_cond_txt   = '#BF360C'
    
    c_step4_fill = '#FFEBEE'
    c_step4_edge = '#B71C1C'
    c_step4_txt  = '#7F0000'
    
    c_step5_fill = '#F3E5F5'
    c_step5_edge = '#6A1B9A'
    c_step5_txt  = '#38006B'
    
    c_step6_fill = '#E8EAF6'
    c_step6_edge = '#283593'
    c_step6_txt  = '#1A237E'

    arrow_col = '#1E293B'
    
    def draw_rounded_box(cx, cy, w, h, fill_col, edge_col, radius=0.8):
        box = FancyBboxPatch(
            (cx - w/2, cy - h/2), w, h,
            boxstyle=f"round,pad=0.2,rounding_size={radius}",
            facecolor=fill_col, edgecolor=edge_col,
            linewidth=2.0, zorder=2
        )
        ax.add_patch(box)
        
    def draw_diamond(cx, cy, w, h, fill_col, edge_col):
        poly = Polygon([
            (cx, cy + h/2),
            (cx + w/2, cy),
            (cx, cy - h/2),
            (cx - w/2, cy)
        ], closed=True, facecolor=fill_col, edgecolor=edge_col, linewidth=2.2, zorder=2)
        ax.add_patch(poly)
        
    def draw_arrow(x1, y1, x2, y2, label=None, label_pos=(0.5, 0.5), label_color='#B71C1C'):
        ax.annotate(
            '', xy=(x2, y2), xytext=(x1, y1),
            arrowprops=dict(
                arrowstyle="-|>", color=arrow_col,
                lw=2.0, mutation_scale=16,
                shrinkA=0, shrinkB=0
            ), zorder=3
        )
        if label:
            ax.text(label_pos[0], label_pos[1], label, color=label_color,
                    fontsize=11.5, fontweight='bold', ha='center', va='center',
                    bbox=dict(boxstyle='square,pad=0.2', facecolor='#ffffff', edgecolor='none', alpha=0.9),
                    zorder=4)

    # ==================== TOẠ ĐỘ CÁC KHỐI ====================
    # Trục chính nằm ở X = 42 (để dành lề phải X = 80 cho Khối 4 lặp lại)
    MAIN_X = 42.0
    BOX_W  = 54.0
    
    # 1. BẮT ĐẦU
    y_start = 132.0
    draw_rounded_box(MAIN_X, y_start, 26.0, 7.0, c_start_fill, c_start_edge, radius=3.5)
    ax.text(MAIN_X, y_start, "BẮT ĐẦU", fontsize=13, fontweight='bold',
            color=c_start_txt, ha='center', va='center', zorder=5)
            
    # Mũi tên Start -> Box 1
    draw_arrow(MAIN_X, y_start - 3.5, MAIN_X, 122.5)

    # 2. KHỐI 1: Đọc dữ liệu lưới & Thành lập Y_bus
    y_b1 = 117.0
    h_b1 = 11.0
    draw_rounded_box(MAIN_X, y_b1, BOX_W, h_b1, c_step1_fill, c_step1_edge, radius=1.0)
    ax.text(MAIN_X, y_b1 + 2.2, "1. Đọc dữ liệu lưới (Nút, Nhánh)",
            fontsize=12, fontweight='bold', color=c_step1_txt, ha='center', va='center', zorder=5)
    ax.text(MAIN_X, y_b1 - 2.5, r"Thành lập ma trận dẫn nạp nút $\mathbf{Y}_{\mathrm{bus}}$ (theo KCL)",
            fontsize=11.5, color=c_step1_txt, ha='center', va='center', zorder=5)

    # Mũi tên Box 1 -> Box 2
    draw_arrow(MAIN_X, y_b1 - h_b1/2, MAIN_X, 105.0)

    # 3. KHỐI 2: Khởi tạo phẳng
    y_b2 = 99.5
    h_b2 = 11.0
    draw_rounded_box(MAIN_X, y_b2, BOX_W, h_b2, c_step2_fill, c_step2_edge, radius=1.0)
    ax.text(MAIN_X, y_b2 + 2.2, "2. Khởi tạo phẳng (Flat Start): đặt $m = 0$",
            fontsize=12, fontweight='bold', color=c_step2_txt, ha='center', va='center', zorder=5)
    ax.text(MAIN_X, y_b2 - 2.5, r"$U_i^{(0)} = 1.0\text{ p.u.}$ (Nút PQ),   $\delta_i^{(0)} = 0.0\text{ rad}$",
            fontsize=11.5, color=c_step2_txt, ha='center', va='center', zorder=5)

    # Mũi tên Box 2 -> Box 3
    draw_arrow(MAIN_X, y_b2 - h_b2/2, MAIN_X, 87.5)

    # 4. KHỐI 3: Tính công suất nút & Sai lệch công suất
    y_b3 = 82.0
    h_b3 = 11.0
    draw_rounded_box(MAIN_X, y_b3, BOX_W, h_b3, c_step3_fill, c_step3_edge, radius=1.0)
    ax.text(MAIN_X, y_b3 + 2.2, r"3. Tính công suất nút $P_i^{(m)},\; Q_i^{(m)}$",
            fontsize=12, fontweight='bold', color=c_step3_txt, ha='center', va='center', zorder=5)
    ax.text(MAIN_X, y_b3 - 2.5, r"Xác định sai lệch: $\Delta P_i^{(m)} = P_i^{\mathrm{spec}} - P_i^{(m)},\; \Delta Q_i^{(m)} = Q_i^{\mathrm{spec}} - Q_i^{(m)}$",
            fontsize=11, color=c_step3_txt, ha='center', va='center', zorder=5)

    # Mũi tên Box 3 -> Khối điều kiện
    draw_arrow(MAIN_X, y_b3 - h_b3/2, MAIN_X, 70.0)

    # 5. KHỐI ĐIỀU KIỆN (DIAMOND): Kiểm tra hội tụ
    y_cond = 63.5
    w_cond = 42.0
    h_cond = 13.0
    draw_diamond(MAIN_X, y_cond, w_cond, h_cond, c_cond_fill, c_cond_edge)
    ax.text(MAIN_X, y_cond + 2.0, r"$\|\mathbf{f}^{(m)}\|_\infty \le \epsilon$ ?",
            fontsize=12.5, fontweight='bold', color=c_cond_txt, ha='center', va='center', zorder=5)
    ax.text(MAIN_X, y_cond - 2.5, r"$(\epsilon = 10^{-10}\text{ p.u.})$",
            fontsize=11, color=c_cond_txt, ha='center', va='center', zorder=5)

    # ------------------ NHÁNH 1: ĐÚNG (ĐÃ HỘI TỤ) -> ĐI THẲNG XUỐNG ------------------
    # Mũi tên từ đáy hình thoi đi thẳng xuống Khối 5
    draw_arrow(MAIN_X, y_cond - h_cond/2, MAIN_X, 48.5,
               label=r"Đúng (Hội tụ)", label_pos=(MAIN_X + 6.0, 53.5), label_color='#1B5E20')

    # 6. KHỐI 5: Tính toán thứ cấp sau hội tụ
    y_b5 = 42.5
    h_b5 = 12.0
    draw_rounded_box(MAIN_X, y_b5, BOX_W, h_b5, c_step5_fill, c_step5_edge, radius=1.0)
    ax.text(MAIN_X, y_b5 + 3.0, "5. Tính toán các đại lượng vận hành sau hội tụ:",
            fontsize=12, fontweight='bold', color=c_step5_txt, ha='center', va='center', zorder=5)
    ax.text(MAIN_X, y_b5 - 0.5, r"Dòng công suất nhánh $\dot{S}_{ij}$, Tổn thất công suất $\Delta\dot{S}_{ij}$",
            fontsize=11.5, color=c_step5_txt, ha='center', va='center', zorder=5)
    ax.text(MAIN_X, y_b5 - 3.8, r"Công suất phát nút SLACK ($P_{G1}, Q_{G1}$) & Cân bằng năng lượng",
            fontsize=11, color=c_step5_txt, ha='center', va='center', zorder=5)

    # Mũi tên Box 5 -> Box 6
    draw_arrow(MAIN_X, y_b5 - h_b5/2, MAIN_X, 30.5)

    # 7. KHỐI 6: Xuất kết quả
    y_b6 = 25.5
    h_b6 = 10.0
    draw_rounded_box(MAIN_X, y_b6, BOX_W, h_b6, c_step6_fill, c_step6_edge, radius=1.0)
    ax.text(MAIN_X, y_b6 + 1.8, "6. Xuất bảng dữ liệu kết quả & Báo cáo kỹ thuật",
            fontsize=12, fontweight='bold', color=c_step6_txt, ha='center', va='center', zorder=5)
    ax.text(MAIN_X, y_b6 - 2.2, "Bảng điện áp nút, trào lưu nhánh và cảnh báo vận hành",
            fontsize=11, color=c_step6_txt, ha='center', va='center', zorder=5)

    # Mũi tên Box 6 -> Kết thúc
    draw_arrow(MAIN_X, y_b6 - h_b6/2, MAIN_X, 14.5)

    # 8. KẾT THÚC
    y_end = 11.0
    draw_rounded_box(MAIN_X, y_end, 26.0, 7.0, c_start_fill, c_start_edge, radius=3.5)
    ax.text(MAIN_X, y_end, "KẾT THÚC", fontsize=13, fontweight='bold',
            color=c_start_txt, ha='center', va='center', zorder=5)

    # ------------------ NHÁNH 2: CHƯA (SAI / CHƯA HỘI TỤ) -> RẼ SANG PHẢI ------------------
    # Khối 4 đặt ở nhánh lặp bên phải:
    X_LOOP = 79.0
    W_LOOP = 34.0
    Y_LOOP = 63.5
    H_LOOP = 18.0
    
    # Đoạn rẽ phải từ đỉnh phải của hình thoi sang Khối 4
    x_diamond_right = MAIN_X + w_cond/2  # 42 + 21 = 63
    draw_arrow(x_diamond_right, y_cond, X_LOOP - W_LOOP/2, Y_LOOP,
               label=r"Sai (Chưa)", label_pos=((x_diamond_right + X_LOOP - W_LOOP/2)/2, y_cond + 1.6),
               label_color='#B71C1C')

    # Vẽ Khối 4
    draw_rounded_box(X_LOOP, Y_LOOP, W_LOOP, H_LOOP, c_step4_fill, c_step4_edge, radius=1.0)
    ax.text(X_LOOP, Y_LOOP + 5.5, r"4. Tính ma trận Jacobian $\mathbf{J}^{(m)}$",
            fontsize=11.5, fontweight='bold', color=c_step4_txt, ha='center', va='center', zorder=5)
    ax.text(X_LOOP, Y_LOOP + 2.0, r"(4 khối giải tích $\mathbf{H}, \mathbf{N}, \mathbf{M}, \mathbf{L}$)",
            fontsize=10.5, color=c_step4_txt, ha='center', va='center', zorder=5)
    ax.text(X_LOOP, Y_LOOP - 1.8, r"Giải hệ: $\mathbf{J}^{(m)} \Delta\mathbf{x}^{(m)} = \Delta\mathbf{f}^{(m)}$",
            fontsize=11, fontweight='bold', color=c_step4_txt, ha='center', va='center', zorder=5)
    ax.text(X_LOOP, Y_LOOP - 5.5, r"Cập nhật: $\mathbf{x}^{(m+1)} = \mathbf{x}^{(m)} + \Delta\mathbf{x}^{(m)}$" "\n" r"Tăng bước lặp: $m \leftarrow m + 1$",
            fontsize=10.5, color=c_step4_txt, ha='center', va='center', zorder=5)

    # Đường dây vòng ngược từ Khối 4 lên Khối 3:
    # Đi từ đỉnh trên Khối 4 lên Y = 82, sau đó rẽ trái đâm vào cạnh phải của Khối 3
    y_loop_top = Y_LOOP + H_LOOP/2  # 63.5 + 9.0 = 72.5
    x_box3_right = MAIN_X + BOX_W/2 # 42 + 27 = 69
    
    # Đoạn đứng đi lên từ Khối 4
    ax.plot([X_LOOP, X_LOOP], [y_loop_top, y_b3], color=arrow_col, lw=2.0, zorder=3)
    # Đoạn ngang đâm vào Khối 3 có mũi tên
    ax.annotate(
        '', xy=(x_box3_right, y_b3), xytext=(X_LOOP, y_b3),
        arrowprops=dict(
            arrowstyle="-|>", color=arrow_col,
            lw=2.0, mutation_scale=16,
            shrinkA=0, shrinkB=0
        ), zorder=3
    )
    # Nhãn trên đường vòng
    ax.text(X_LOOP, (y_loop_top + y_b3)/2, "Lặp tiếp\n" + r"($m \leftarrow m+1$)",
            color='#B71C1C', fontsize=10.5, fontweight='bold', ha='center', va='center',
            bbox=dict(boxstyle='round,pad=0.2', facecolor='#ffffff', edgecolor='#B71C1C', alpha=0.95),
            zorder=4)

    # Tiêu đề biểu đồ chuẩn IEEE
    ax.text(50.0, 138.0, "LƯU ĐỒ THUẬT TOÁN NEWTON--RAPHSON TỌA ĐỘ CỰC",
            fontsize=14, fontweight='bold', color='#0F172A', ha='center', va='center')

    # Lưu hình ảnh
    plt.savefig(output_png, dpi=350, bbox_inches='tight', pad_inches=0.1)
    print(f"Saved PNG to: {output_png}")
    if output_svg:
        plt.savefig(output_svg, format='svg', bbox_inches='tight', pad_inches=0.1)
        print(f"Saved SVG to: {output_svg}")
    plt.close()

if __name__ == '__main__':
    out_dir = r"c:\Users\Lax\Downloads\Project_I_Power_Flow\figures"
    out_png = os.path.join(out_dir, "algorithm_vi.png")
    out_svg = os.path.join(out_dir, "algorithm_vi.svg")
    create_flowchart(out_png, out_svg)

