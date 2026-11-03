"""
Script tạo các hình ảnh minh họa chuyên sâu cho ứng dụng PowerFlow (Đồ án 1)
để tích hợp vào Chương 3 và Chương 4 của Báo cáo kỹ thuật.
"""
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, Arrow
import numpy as np
import os

font_main = 'Segoe UI'

def generate_solvers_benchmark_chart(out_path):
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 4.2), dpi=350)
    
    solvers = ['Newton–Raphson\n(NR)', 'Fast Decoupled\n(FDPF XB)', 'Gauss–Seidel\n(GS)', 'DC Power Flow\n(DCPF)']
    iters = [3, 7, 11, 1]
    times = [0.78, 0.27, 0.33, 0.07]
    colors = ['#0284c7', '#0d9488', '#f59e0b', '#64748b']
    
    # Đồ thị 1: Số bước lặp hội tụ
    bars1 = ax1.bar(solvers, iters, color=colors, width=0.55, edgecolor='#1e293b', linewidth=1.2)
    ax1.set_title('Số bước lặp hội tụ (Lưới 3 nút chuẩn)', fontsize=11, fontweight='bold', fontfamily=font_main, pad=10)
    ax1.set_ylabel('Số bước lặp (Iterations)', fontsize=10, fontfamily=font_main)
    ax1.set_ylim(0, 13)
    ax1.grid(axis='y', linestyle='--', alpha=0.3)
    for bar, val in zip(bars1, iters):
        yval = bar.get_height()
        ax1.text(bar.get_x() + bar.get_width()/2.0, yval + 0.3, f'{val}', ha='center', va='bottom',
                 fontsize=10, fontweight='bold', fontfamily=font_main)
    ax1.tick_params(axis='x', labelsize=9)
    
    # Đồ thị 2: Thời gian tính toán CPU (ms)
    bars2 = ax2.bar(solvers, times, color=colors, width=0.55, edgecolor='#1e293b', linewidth=1.2)
    ax2.set_title('Thời gian tính toán trên CPU (ms)', fontsize=11, fontweight='bold', fontfamily=font_main, pad=10)
    ax2.set_ylabel('Thời gian (ms)', fontsize=10, fontfamily=font_main)
    ax2.set_ylim(0, 1.0)
    ax2.grid(axis='y', linestyle='--', alpha=0.3)
    for bar, val in zip(bars2, times):
        yval = bar.get_height()
        ax2.text(bar.get_x() + bar.get_width()/2.0, yval + 0.02, f'{val:.2f} ms', ha='center', va='bottom',
                 fontsize=9.5, fontweight='bold', fontfamily=font_main)
    ax2.tick_params(axis='x', labelsize=9)
    
    plt.tight_layout()
    plt.savefig(out_path, dpi=350, bbox_inches='tight')
    plt.close()
    print(f"Saved solvers benchmark chart to {out_path}")

def generate_contingency_chart(out_path):
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 4.2), dpi=350)
    
    scenarios = ['Sa thải L12\n(Nút 1-2)', 'Sa thải L13\n(Nút 1-3)', 'Sa thải L23\n(Nút 2-3)']
    min_voltages = [0.9430, 0.7660, 0.6472]
    max_loadings = [80.8, 168.7, 208.4]
    
    # Đồ thị 1: Điện áp nút thấp nhất sau sự cố
    colors_v = ['#eab308', '#ef4444', '#b91c1c']
    bars1 = ax1.bar(scenarios, min_voltages, color=colors_v, width=0.5, edgecolor='#1e293b', linewidth=1.2)
    ax1.axhline(0.95, color='#16a34a', linestyle='--', linewidth=1.5, label='Giới hạn dưới quy chuẩn (0.95 p.u.)')
    ax1.set_title('Điện áp nút thấp nhất sau sự cố N-1', fontsize=11, fontweight='bold', fontfamily=font_main, pad=10)
    ax1.set_ylabel(r'Điện áp $U_{\mathrm{min}}$ (p.u.)', fontsize=10, fontfamily=font_main)
    ax1.set_ylim(0.5, 1.05)
    ax1.grid(axis='y', linestyle='--', alpha=0.3)
    ax1.legend(loc='lower left', fontsize=8.5)
    for bar, val in zip(bars1, min_voltages):
        yval = bar.get_height()
        ax1.text(bar.get_x() + bar.get_width()/2.0, yval + 0.015, f'{val:.4f}', ha='center', va='bottom',
                 fontsize=9.5, fontweight='bold', fontfamily=font_main)
    ax1.tick_params(axis='x', labelsize=9)
    
    # Đồ thị 2: Mức mang tải cực đại của các nhánh còn lại (%)
    colors_l = ['#3b82f6', '#f97316', '#dc2626']
    bars2 = ax2.bar(scenarios, max_loadings, color=colors_l, width=0.5, edgecolor='#1e293b', linewidth=1.2)
    ax2.axhline(100.0, color='#dc2626', linestyle='--', linewidth=1.5, label='Định mức nhiệt 100%')
    ax2.set_title('Mức mang tải cực đại đường dây (%)', fontsize=11, fontweight='bold', fontfamily=font_main, pad=10)
    ax2.set_ylabel('Mức tải (%)', fontsize=10, fontfamily=font_main)
    ax2.set_ylim(0, 240)
    ax2.grid(axis='y', linestyle='--', alpha=0.3)
    ax2.legend(loc='upper left', fontsize=8.5)
    for bar, val in zip(bars2, max_loadings):
        yval = bar.get_height()
        ax2.text(bar.get_x() + bar.get_width()/2.0, yval + 3.0, f'{val:.1f}%', ha='center', va='bottom',
                 fontsize=9.5, fontweight='bold', fontfamily=font_main)
    ax2.tick_params(axis='x', labelsize=9)
    
    plt.tight_layout()
    plt.savefig(out_path, dpi=350, bbox_inches='tight')
    plt.close()
    print(f"Saved contingency chart to {out_path}")

def generate_smart_table_diagram(out_path):
    fig, ax = plt.subplots(figsize=(10.5, 4.8), dpi=350)
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 50)
    ax.axis('off')
    
    # Tiêu đề
    ax.text(50, 47, "CƠ CHẾ PHÂN ĐỊNH RẠCH RÒI ẨN SỐ VÀ THÔNG SỐ ĐÃ BIẾT TRONG BẢNG NHẬP LIỆU",
            fontsize=11.5, fontweight='bold', fontfamily=font_main, ha='center', va='center', color='#0f172a')
    
    def draw_card(cx, cy, w, h, fill_col, border_col):
        box = FancyBboxPatch((cx - w/2, cy - h/2), w, h,
                             boxstyle="round,pad=0.2,rounding_size=1.0",
                             facecolor=fill_col, edgecolor=border_col, linewidth=1.8, zorder=2)
        ax.add_patch(box)
        
    # Card 1: Nút SLACK
    draw_card(18, 25, 30, 36, '#f0fdf4', '#16a34a')
    ax.text(18, 40, "NÚT SLACK (CÂN BẰNG)", fontsize=10.5, fontweight='bold', fontfamily=font_main,
            ha='center', va='center', color='#166534', zorder=3)
    ax.text(18, 35, "Thanh cái chuẩn hệ thống", fontsize=8.5, fontfamily=font_main, ha='center', va='center', color='#4b5563', zorder=3)
    ax.plot([5, 31], [32, 32], color='#bbf7d0', lw=1.2, zorder=3)
    
    ax.text(6, 27, "Thông số CHO TRƯỚC:", fontsize=8.5, fontweight='bold', fontfamily=font_main, ha='left', color='#15803d', zorder=3)
    ax.text(8, 23, r"• $U_1 = 1.05\text{ p.u.}$ (Hằng số)", fontsize=8.5, fontfamily=font_main, ha='left', color='#1e293b', zorder=3)
    ax.text(8, 19, r"• $\delta_1 = 0^\circ$ (Gốc pha)", fontsize=8.5, fontfamily=font_main, ha='left', color='#1e293b', zorder=3)
    
    ax.text(6, 14, "ẨN SỐ CẦN TÌM:", fontsize=8.5, fontweight='bold', fontfamily=font_main, ha='left', color='#b91c1c', zorder=3)
    ax.text(8, 10, r"• $P_{G1}$ hiển thị: ", fontsize=8.5, fontfamily=font_main, ha='left', color='#1e293b', zorder=3)
    ax.text(21, 10, "[Ẩn số]", fontsize=8.5, fontweight='bold', fontfamily=font_main, ha='left', color='#b91c1c', zorder=3)
    ax.text(8, 6, r"• $Q_{G1}$ hiển thị: ", fontsize=8.5, fontfamily=font_main, ha='left', color='#1e293b', zorder=3)
    ax.text(21, 6, "[Ẩn số]", fontsize=8.5, fontweight='bold', fontfamily=font_main, ha='left', color='#b91c1c', zorder=3)

    # Card 2: Nút PV
    draw_card(50, 25, 30, 36, '#eff6ff', '#2563eb')
    ax.text(50, 40, "NÚT PV (MÁY PHÁT)", fontsize=10.5, fontweight='bold', fontfamily=font_main,
            ha='center', va='center', color='#1e40af', zorder=3)
    ax.text(50, 35, "Điều khiển điện áp thanh cái", fontsize=8.5, fontfamily=font_main, ha='center', va='center', color='#4b5563', zorder=3)
    ax.plot([37, 63], [32, 32], color='#bfdbfe', lw=1.2, zorder=3)
    
    ax.text(38, 27, "Thông số CHO TRƯỚC:", fontsize=8.5, fontweight='bold', fontfamily=font_main, ha='left', color='#1d4ed8', zorder=3)
    ax.text(40, 23, r"• $U_2 = 1.04\text{ p.u.}$ (Điện áp đặt)", fontsize=8.5, fontfamily=font_main, ha='left', color='#1e293b', zorder=3)
    ax.text(40, 19, r"• $P_{G2} = 50.0\text{ MW}$ (Công suất phát)", fontsize=8.5, fontfamily=font_main, ha='left', color='#1e293b', zorder=3)
    
    ax.text(38, 14, "ẨN SỐ CẦN TÌM:", fontsize=8.5, fontweight='bold', fontfamily=font_main, ha='left', color='#b91c1c', zorder=3)
    ax.text(40, 10, r"• $\delta_2$ hiển thị: ", fontsize=8.5, fontfamily=font_main, ha='left', color='#1e293b', zorder=3)
    ax.text(53, 10, "[Ẩn: 0°]", fontsize=8.5, fontweight='bold', fontfamily=font_main, ha='left', color='#b91c1c', zorder=3)
    ax.text(40, 6, r"• $Q_{G2}$ hiển thị: ", fontsize=8.5, fontfamily=font_main, ha='left', color='#1e293b', zorder=3)
    ax.text(53, 6, "[Ẩn số]", fontsize=8.5, fontweight='bold', fontfamily=font_main, ha='left', color='#b91c1c', zorder=3)

    # Card 3: Nút PQ
    draw_card(82, 25, 30, 36, '#faf5ff', '#9333ea')
    ax.text(82, 40, "NÚT PQ (PHỤ TẢI)", fontsize=10.5, fontweight='bold', fontfamily=font_main,
            ha='center', va='center', color='#6b21a8', zorder=3)
    ax.text(82, 35, "Tiêu thụ công suất phụ tải", fontsize=8.5, fontfamily=font_main, ha='center', va='center', color='#4b5563', zorder=3)
    ax.plot([69, 95], [32, 32], color='#e9d5ff', lw=1.2, zorder=3)
    
    ax.text(70, 27, "Thông số CHO TRƯỚC:", fontsize=8.5, fontweight='bold', fontfamily=font_main, ha='left', color='#7e22ce', zorder=3)
    ax.text(72, 23, r"• $P_{L3} = 120.0\text{ MW}$ (Tải P)", fontsize=8.5, fontfamily=font_main, ha='left', color='#1e293b', zorder=3)
    ax.text(72, 19, r"• $Q_{L3} = 50.0\text{ Mvar}$ (Tải Q)", fontsize=8.5, fontfamily=font_main, ha='left', color='#1e293b', zorder=3)
    
    ax.text(70, 14, "ẨN SỐ CẦN TÌM:", fontsize=8.5, fontweight='bold', fontfamily=font_main, ha='left', color='#b91c1c', zorder=3)
    ax.text(72, 10, r"• $U_3$ hiển thị: ", fontsize=8.5, fontfamily=font_main, ha='left', color='#1e293b', zorder=3)
    ax.text(85, 10, "[Ẩn: 1.0]", fontsize=8.5, fontweight='bold', fontfamily=font_main, ha='left', color='#b91c1c', zorder=3)
    ax.text(72, 6, r"• $\delta_3$ hiển thị: ", fontsize=8.5, fontfamily=font_main, ha='left', color='#1e293b', zorder=3)
    ax.text(85, 6, "[Ẩn: 0°]", fontsize=8.5, fontweight='bold', fontfamily=font_main, ha='left', color='#b91c1c', zorder=3)

    plt.tight_layout()
    plt.savefig(out_path, dpi=350, bbox_inches='tight')
    plt.close()
    print(f"Saved smart table diagram to {out_path}")

if __name__ == '__main__':
    fig_dir = r"c:\Users\Lax\Downloads\Project_I_Power_Flow\figures"
    generate_solvers_benchmark_chart(os.path.join(fig_dir, "powerflow_solvers_benchmark.png"))
    generate_contingency_chart(os.path.join(fig_dir, "powerflow_contingency_n1.png"))
    generate_smart_table_diagram(os.path.join(fig_dir, "powerflow_smart_table.png"))
