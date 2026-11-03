import os
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, Polygon

# Independent English flowchart generator

def generate_ieee_flowchart_en(output_png, output_svg=None):
    fig = plt.figure(figsize=(10.5, 15.0), dpi=400)
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_xlim(-2, 105)
    ax.set_ylim(0, 150)
    ax.axis('off')

    c_start_fill = '#E8F5E9'
    c_start_edge = '#2E7D32'
    c_start_txt  = '#1B5E20'

    c_step1_fill = '#E0F2F1'
    c_step1_edge = '#00695C'
    c_step1_txt  = '#004D40'

    c_step2_fill = '#E1F5FE'
    c_step2_edge = '#0277BD'
    c_step2_txt  = '#01579B'

    c_step3_fill = '#EDE7F6'
    c_step3_edge = '#5E35B1'
    c_step3_txt  = '#311B92'

    c_cond_fill  = '#FFF9C4'
    c_cond_edge  = '#EF6C00'
    c_cond_txt   = '#B7410E'

    c_step4_fill = '#FFEBEE'
    c_step4_edge = '#C62828'
    c_step4_txt  = '#880E4F'

    c_step5_fill = '#F3E5F5'
    c_step5_edge = '#7B1FA2'
    c_step5_txt  = '#4A148C'

    c_step6_fill = '#E8EAF6'
    c_step6_edge = '#303F9F'
    c_step6_txt  = '#1A237E'

    arrow_col = '#1E293B'
    font_main = 'Segoe UI'

    def draw_rounded_box(cx, cy, w, h, fill_col, edge_col, radius=1.2, lw=2.2):
        box = FancyBboxPatch(
            (cx - w/2, cy - h/2), w, h,
            boxstyle=f"round,pad=0.2,rounding_size={radius}",
            facecolor=fill_col, edgecolor=edge_col,
            linewidth=lw, zorder=2
        )
        ax.add_patch(box)

    def draw_diamond(cx, cy, w, h, fill_col, edge_col, lw=2.2):
        poly = Polygon([
            (cx, cy + h/2),
            (cx + w/2, cy),
            (cx, cy - h/2),
            (cx - w/2, cy)
        ], closed=True, facecolor=fill_col, edgecolor=edge_col, linewidth=lw, zorder=2)
        ax.add_patch(poly)

    def draw_direct_arrow(x1, y1, x2, y2, lw=2.0):
        ax.annotate(
            '', xy=(x2, y2), xytext=(x1, y1),
            arrowprops=dict(
                arrowstyle="-|>", color=arrow_col,
                lw=lw, mutation_scale=16,
                shrinkA=0, shrinkB=0
            ), zorder=3
        )

    MAIN_X = 50.0
    BOX_W  = 62.0
    LEFT_E = MAIN_X - BOX_W / 2
    RIGHT_E = MAIN_X + BOX_W / 2

    # 0. START
    y_start = 143.0
    h_start = 6.2
    draw_rounded_box(MAIN_X, y_start, 26.0, h_start, c_start_fill, c_start_edge, radius=3.1)
    ax.text(MAIN_X, y_start, "START", fontsize=12.5, fontweight='bold', fontfamily=font_main,
            color=c_start_txt, ha='center', va='center', zorder=5)

    draw_direct_arrow(MAIN_X, y_start - h_start/2, MAIN_X, 134.5)

    # 1. READ NETWORK DATA & YBUS
    y_b1 = 129.0
    h_b1 = 11.0
    draw_rounded_box(MAIN_X, y_b1, BOX_W, h_b1, c_step1_fill, c_step1_edge)
    ax.text(MAIN_X, y_b1 + 2.2, "1. Read Grid Data (Busbars, Transmission Lines)",
            fontsize=12, fontweight='bold', fontfamily=font_main, color=c_step1_txt, ha='center', va='center', zorder=5)
    ax.text(MAIN_X, y_b1 - 2.5, r"Formulate Nodal Admittance Matrix $\mathbf{Y}_{\mathrm{bus}} = \mathbf{G} + j\mathbf{B}$ via KCL",
            fontsize=11.5, fontfamily=font_main, color=c_step1_txt, ha='center', va='center', zorder=5)

    draw_direct_arrow(MAIN_X, y_b1 - h_b1/2, MAIN_X, 118.0)

    # 2. FLAT START
    y_b2 = 112.5
    h_b2 = 11.0
    draw_rounded_box(MAIN_X, y_b2, BOX_W, h_b2, c_step2_fill, c_step2_edge)
    ax.text(MAIN_X, y_b2 + 2.2, r"2. Flat Start Initialization: set iteration count $m = 0$",
            fontsize=12, fontweight='bold', fontfamily=font_main, color=c_step2_txt, ha='center', va='center', zorder=5)
    ax.text(MAIN_X, y_b2 - 2.5, r"$U_i^{(0)} = 1.0\text{ p.u.}$ (PQ Buses),   $\delta_i^{(0)} = 0.0\text{ rad}$ (All buses $i \neq 1$)",
            fontsize=11.5, fontfamily=font_main, color=c_step2_txt, ha='center', va='center', zorder=5)

    draw_direct_arrow(MAIN_X, y_b2 - h_b2/2, MAIN_X, 101.5)

    # 3. MISMATCHES
    y_b3 = 96.0
    h_b3 = 11.0
    draw_rounded_box(MAIN_X, y_b3, BOX_W, h_b3, c_step3_fill, c_step3_edge)
    ax.text(MAIN_X, y_b3 + 2.2, r"3. Calculate Nodal Injections $P_i^{(m)},\; Q_i^{(m)}$",
            fontsize=12, fontweight='bold', fontfamily=font_main, color=c_step3_txt, ha='center', va='center', zorder=5)
    ax.text(MAIN_X, y_b3 - 2.5, r"Compute Mismatches: $\Delta P_i^{(m)} = P_i^{\mathrm{spec}} - P_i^{(m)},\; \Delta Q_i^{(m)} = Q_i^{\mathrm{spec}} - Q_i^{(m)}$",
            fontsize=11, fontfamily=font_main, color=c_step3_txt, ha='center', va='center', zorder=5)

    draw_direct_arrow(MAIN_X, y_b3 - h_b3/2, MAIN_X, 85.0)

    # CONVERGENCE CHECK (DIAMOND)
    y_cond = 78.5
    w_cond = 46.0
    h_cond = 13.0
    draw_diamond(MAIN_X, y_cond, w_cond, h_cond, c_cond_fill, c_cond_edge)
    ax.text(MAIN_X, y_cond + 2.0, r"$\|\mathbf{f}^{(m)}\|_\infty \leq \epsilon$ ?",
            fontsize=12.5, fontweight='bold', fontfamily=font_main, color=c_cond_txt, ha='center', va='center', zorder=5)
    ax.text(MAIN_X, y_cond - 2.5, r"$(\epsilon = 10^{-10}\text{ p.u.})$",
            fontsize=11, fontfamily=font_main, color=c_cond_txt, ha='center', va='center', zorder=5)

    # 4. JACOBIAN & UPDATE (NO)
    y_b4 = 58.5
    h_b4 = 15.0
    draw_rounded_box(MAIN_X, y_b4, BOX_W, h_b4, c_step4_fill, c_step4_edge)
    ax.text(MAIN_X, y_b4 + 4.5, r"4. Assemble 4 Analytical Jacobian Submatrices $\mathbf{J}^{(m)} = [\mathbf{H}\; \mathbf{N};\; \mathbf{M}\; \mathbf{L}]$",
            fontsize=11.5, fontweight='bold', fontfamily=font_main, color=c_step4_txt, ha='center', va='center', zorder=5)
    ax.text(MAIN_X, y_b4 + 1.0, r"Solve Linear System: $\mathbf{J}^{(m)} \Delta\mathbf{x}^{(m)} = \Delta\mathbf{f}^{(m)}$",
            fontsize=11.5, fontweight='bold', fontfamily=font_main, color=c_step4_txt, ha='center', va='center', zorder=5)
    ax.text(MAIN_X, y_b4 - 2.5, r"Update State Vector: $\mathbf{x}^{(m+1)} = \mathbf{x}^{(m)} + \Delta\mathbf{x}^{(m)}$",
            fontsize=11.5, fontfamily=font_main, color=c_step4_txt, ha='center', va='center', zorder=5)
    ax.text(MAIN_X, y_b4 - 5.5, r"Increment Iteration Index: $m \leftarrow m + 1$",
            fontsize=11, fontfamily=font_main, color=c_step4_txt, ha='center', va='center', zorder=5)

    draw_direct_arrow(MAIN_X, y_cond - h_cond/2, MAIN_X, y_b4 + h_b4/2)
    ax.text(MAIN_X + 2.5, (y_cond - h_cond/2 + y_b4 + h_b4/2) / 2, "No (False)\nNot Converged",
            color='#C62828', fontsize=10.5, fontweight='bold', fontfamily=font_main, ha='left', va='center',
            bbox=dict(boxstyle='round,pad=0.25', facecolor='#ffffff', edgecolor='#C62828', lw=1.2, alpha=0.95),
            zorder=6)

    # LOOP BACK LEFT
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
    ax.text(X_LOOP, (y_b4 + y_b3)/2, "Iteration Loop\n" + r"($m \leftarrow m+1$)",
            color='#C62828', fontsize=10.5, fontweight='bold', fontfamily=font_main, ha='center', va='center',
            bbox=dict(boxstyle='round,pad=0.25', facecolor='#ffffff', edgecolor='#C62828', lw=1.2, alpha=0.95),
            zorder=6)

    # 5. POST-CONVERGENCE QUANTITIES (YES)
    y_b5 = 37.0
    h_b5 = 13.0
    draw_rounded_box(MAIN_X, y_b5, BOX_W, h_b5, c_step5_fill, c_step5_edge)
    ax.text(MAIN_X, y_b5 + 3.2, "5. Compute Secondary Operational Quantities Post-Convergence:",
            fontsize=12, fontweight='bold', fontfamily=font_main, color=c_step5_txt, ha='center', va='center', zorder=5)
    ax.text(MAIN_X, y_b5 - 0.2, r"Complex Branch Flows $\dot{S}_{ij}$, Transmission Losses $\Delta\dot{S}_{ij}$",
            fontsize=11.5, fontfamily=font_main, color=c_step5_txt, ha='center', va='center', zorder=5)
    ax.text(MAIN_X, y_b5 - 3.5, r"Slack Bus Generation ($P_{G1}, Q_{G1}$) & System Power Balance Audit",
            fontsize=11, fontfamily=font_main, color=c_step5_txt, ha='center', va='center', zorder=5)

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
    ax.text(X_BYPASS, (y_cond + y_b5)/2, "Yes (True)\nConverged!",
            color='#2E7D32', fontsize=10.5, fontweight='bold', fontfamily=font_main, ha='center', va='center',
            bbox=dict(boxstyle='round,pad=0.25', facecolor='#ffffff', edgecolor='#2E7D32', lw=1.2, alpha=0.95),
            zorder=6)

    # 6. EXPORT RESULTS
    y_b6 = 20.0
    h_b6 = 10.0
    draw_direct_arrow(MAIN_X, y_b5 - h_b5/2, MAIN_X, y_b6 + h_b6/2)
    draw_rounded_box(MAIN_X, y_b6, BOX_W, h_b6, c_step6_fill, c_step6_edge)
    ax.text(MAIN_X, y_b6 + 1.8, "6. Export Engineering Tables & Technical Report",
            fontsize=12, fontweight='bold', fontfamily=font_main, color=c_step6_txt, ha='center', va='center', zorder=5)
    ax.text(MAIN_X, y_b6 - 2.2, "Bus voltages, line power flows, loss breakdown & constraint warnings",
            fontsize=11, fontfamily=font_main, color=c_step6_txt, ha='center', va='center', zorder=5)

    # 7. END
    y_end = 6.5
    h_end = 6.2
    draw_direct_arrow(MAIN_X, y_b6 - h_b6/2, MAIN_X, y_end + h_end/2)
    draw_rounded_box(MAIN_X, y_end, 26.0, h_end, c_start_fill, c_start_edge, radius=3.1)
    ax.text(MAIN_X, y_end, "END", fontsize=12.5, fontweight='bold', fontfamily=font_main,
            color=c_start_txt, ha='center', va='center', zorder=5)

    plt.savefig(output_png, dpi=400, bbox_inches='tight', pad_inches=0.1)
    print(f"Saved publication-grade English PNG to: {output_png}")
    if output_svg:
        plt.savefig(output_svg, format='svg', bbox_inches='tight', pad_inches=0.1)
        print(f"Saved publication-grade English SVG to: {output_svg}")
    plt.close()

if __name__ == '__main__':
    out_dir = r"c:\Users\Lax\Downloads\Project_I_Power_Flow\figures"
    generate_ieee_flowchart_en(os.path.join(out_dir, "algorithm_en.png"), os.path.join(out_dir, "algorithm_en.svg"))
    # Also overwrite algorithm.png and algorithm.svg so any legacy English report references get the 400 DPI version
    generate_ieee_flowchart_en(os.path.join(out_dir, "algorithm.png"), os.path.join(out_dir, "algorithm.svg"))
    print("Flowchart generation complete!")
