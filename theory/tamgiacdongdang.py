"""Bài giảng lý thuyết: TAM GIÁC ĐỒNG DẠNG
Spec: specs/theory/tam-giac-dong-dang/spec-ly-thuyet.md

Cấu trúc:
    Scene 00 – Intro
    Scene 01 – Định nghĩa  (dual_geometry: △ABC + △A'B'C')
    Scene 02 – Nhận xét    (3 tính chất đồng dạng, tái dùng figure scene 01)
    Scene 03 – Định lí     (geometry: △ABC, MN // BC ⟹ △AMN ∽ △ABC)
"""

import sys
from pathlib import Path

# scenes/theory/ → project root (chứa manim_helpers/)
_PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(_PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(_PROJECT_ROOT))

from manim import *
import numpy as np
from manim_voiceover import VoiceoverScene

from manim_helpers import (
    # color tokens
    COLOR_DEFAULT, COLOR_BACKGROUND, COLOR_GRID,
    COLOR_EQUAL_1, COLOR_EQUAL_2,
    COLOR_ACTIVE,
    # timing tokens
    TIMING_INDICATE_SEGMENT,
    # motion tokens
    MOTION_ENTER, MOTION_EXIT,
    # emphasis tokens
    EMPHASIS_SCALE, EMPHASIS_INDICATE_TIME,
    # layer tokens
    LAYER_BACKGROUND, LAYER_GEOMETRY, LAYER_MARKERS,
    # dot marker
    MARKER_DOT_RADIUS,
    # theory layout
    TheoryColumn, place_figure, place_dual_figures,
    make_gtts_service,
    # geometry engine
    GeometryEngine,
)

# ---------------------------------------------------------------------------
# TeX template chuẩn – bắt buộc cho mọi Tex/MathTex có tiếng Việt
# ---------------------------------------------------------------------------

viet_tex_template = TexTemplate(
    tex_compiler="xelatex",
    output_format=".xdv",
    preamble=r"""
\usepackage{fontspec}
\usepackage{amsmath}
\usepackage{amssymb}
\usepackage{vntex}
\setmainfont{Times New Roman}
""")


# ---------------------------------------------------------------------------
# Module-level helpers
# ---------------------------------------------------------------------------

def _parallel_marks(seg_mob: Line, color: str = COLOR_EQUAL_1) -> VGroup:
    """Tạo dấu // tại giữa đoạn thẳng – 2 tick vuông góc với đoạn."""
    unit = seg_mob.get_unit_vector()
    perp = rotate_vector(unit, PI / 2)
    mid  = seg_mob.get_center()

    def _tick(center: np.ndarray) -> Line:
        return Line(
            center - perp * 0.13,
            center + perp * 0.13,
            color=color,
            stroke_width=2.0,
        ).set_z_index(LAYER_MARKERS)

    return VGroup(_tick(mid - unit * 0.11), _tick(mid + unit * 0.11))


# ---------------------------------------------------------------------------
# Scene class
# ---------------------------------------------------------------------------

class TamGiacDongDang(VoiceoverScene):
    """Video lý thuyết: Tam giác đồng dạng."""

    def construct(self):
        self.set_speech_service(make_gtts_service())
        self.setup_scene_style()
        self.scene00_intro()
        self.scene01_dinhNghia()
        self.scene02_nhanXet()
        self.scene03_dinhLi()

    # ── setup ──────────────────────────────────────────────────────────────

    def setup_scene_style(self):
        Mobject.set_default(color=COLOR_DEFAULT)
        Tex.set_default(color=COLOR_DEFAULT)
        MathTex.set_default(color=COLOR_DEFAULT)
        self.camera.background_color = COLOR_BACKGROUND
        grid = NumberPlane(
            x_range=[-8, 8, 1], y_range=[-5, 5, 1],
            axis_config={"stroke_width": 0},
            background_line_style={
                "stroke_color": COLOR_GRID,
                "stroke_width": 1,
                "stroke_opacity": 0.4,
            })
        grid.set_z_index(LAYER_BACKGROUND - 10)
        self.add(grid)

    # ── shared state ───────────────────────────────────────────────────────
    # self.lesson_title   → tiêu đề bài (thu nhỏ sau scene00, giữ xuyên suốt)
    # self.figure_group   → hình hiện tại (scene01 → giữ sang scene02)

    # =========================================================================
    # Scene 00 — Intro
    # =========================================================================

    def scene00_intro(self):
        self.lesson_title = Tex(
            r"\textbf{TAM GIÁC ĐỒNG DẠNG}",
            tex_template=viet_tex_template, font_size=40)
        self.lesson_title.to_edge(UP, buff=0.4)

        section = Tex(
            r"I. CÁC KIẾN THỨC CẦN NHỚ",
            tex_template=viet_tex_template, font_size=30)
        section.next_to(self.lesson_title, DOWN, buff=0.35)

        with self.voiceover(
            "Chào mừng các bạn đến với bài học Tam giác đồng dạng. "
            "Phần một, các kiến thức cần nhớ."
        ) as ov:
            self.play(Write(self.lesson_title), run_time=ov.duration * 0.55)
            self.play(FadeIn(section), run_time=ov.duration * 0.45)

        self.wait(0.5)
        self.play(FadeOut(section), run_time=MOTION_EXIT)
        self.play(
            self.lesson_title.animate.scale(0.6).to_edge(UP, buff=0.15),
            run_time=MOTION_EXIT)

    # =========================================================================
    # Scene 01 — Định nghĩa
    # =========================================================================

    def scene01_dinhNghia(self):
        # ── Heading ──────────────────────────────────────────────────────────
        block_heading = Tex(
            r"\textbf{1. Định nghĩa}",
            tex_template=viet_tex_template, font_size=32)
        block_heading.to_corner(UL, buff=0.5)
        self.play(Write(block_heading), run_time=MOTION_ENTER)

        # ── TheoryColumn ─────────────────────────────────────────────────────
        col = TheoryColumn(block_heading, has_figure=True)

        # ── Body text ────────────────────────────────────────────────────────
        line1 = Tex(
            r"Tam giác $A'B'C'$ gọi là \textbf{đồng dạng} với tam giác $ABC$ nếu:",
            tex_template=viet_tex_template, font_size=26)
        col.place(line1, gap=0.30)

        # ── Công thức tỉ số cạnh ─────────────────────────────────────────────
        formula_ratio = MathTex(
            r"\frac{A'B'}{AB} = \frac{B'C'}{BC} = \frac{A'C'}{AC}",
            tex_template=viet_tex_template, font_size=30)
        col.place_formula(formula_ratio, gap=0.28)

        # ── Công thức góc bằng nhau ───────────────────────────────────────────
        formula_angles = MathTex(
            r"\widehat{A'} = \widehat{A},\quad"
            r"\widehat{B'} = \widehat{B},\quad"
            r"\widehat{C'} = \widehat{C}",
            tex_template=viet_tex_template, font_size=28)
        col.place_formula(formula_angles, gap=0.28)

        # ── Kí hiệu đồng dạng ────────────────────────────────────────────────
        formula_symbol = MathTex(
            r"\text{Kí hiệu: }\Delta A'B'C' \backsim \Delta ABC",
            tex_template=viet_tex_template, font_size=26)
        col.place_formula(formula_symbol, gap=0.25)

        # ── Tỉ số đồng dạng k ────────────────────────────────────────────────
        formula_k = MathTex(
            r"k = \frac{A'B'}{AB} = \frac{B'C'}{BC} = \frac{A'C'}{AC}",
            tex_template=viet_tex_template, font_size=26)
        col.place_formula(formula_k, gap=0.18)

        line_k = Tex(
            r"là \textbf{tỉ số đồng dạng} của $\Delta A'B'C'$ với $\Delta ABC$.",
            tex_template=viet_tex_template, font_size=24)
        col.place(line_k, gap=0.20)

        # ── Figure: dual_geometry ─────────────────────────────────────────────
        # Tam giác ABC (trái)
        A_pos = np.array([-1.0,  1.5, 0])
        B_pos = np.array([-1.8, -1.0, 0])
        C_pos = np.array([ 0.6, -1.0, 0])

        seg_AB = Line(A_pos, B_pos, color=COLOR_DEFAULT,
                      stroke_width=2.0).set_z_index(LAYER_GEOMETRY)
        seg_BC = Line(B_pos, C_pos, color=COLOR_DEFAULT,
                      stroke_width=2.0).set_z_index(LAYER_GEOMETRY)
        seg_CA = Line(C_pos, A_pos, color=COLOR_DEFAULT,
                      stroke_width=2.0).set_z_index(LAYER_GEOMETRY)

        dot_A1 = Dot(A_pos, color=COLOR_DEFAULT,
                     radius=MARKER_DOT_RADIUS).set_z_index(LAYER_MARKERS)
        dot_B1 = Dot(B_pos, color=COLOR_DEFAULT,
                     radius=MARKER_DOT_RADIUS).set_z_index(LAYER_MARKERS)
        dot_C1 = Dot(C_pos, color=COLOR_DEFAULT,
                     radius=MARKER_DOT_RADIUS).set_z_index(LAYER_MARKERS)

        lbl_A1 = Tex(r"$A$", tex_template=viet_tex_template,
                     font_size=24).next_to(dot_A1, UL, buff=0.08)
        lbl_B1 = Tex(r"$B$", tex_template=viet_tex_template,
                     font_size=24).next_to(dot_B1, DL, buff=0.08)
        lbl_C1 = Tex(r"$C$", tex_template=viet_tex_template,
                     font_size=24).next_to(dot_C1, DR, buff=0.08)

        fig_abc = VGroup(
            seg_AB, seg_BC, seg_CA,
            dot_A1, dot_B1, dot_C1,
            lbl_A1, lbl_B1, lbl_C1)

        # Tam giác A'B'C' (phải, nhỏ hơn ~0.6 lần)
        Ap_pos = np.array([ 0.5,  0.9, 0])
        Bp_pos = np.array([-0.1, -0.5, 0])
        Cp_pos = np.array([ 1.3, -0.5, 0])

        seg_ApBp = Line(Ap_pos, Bp_pos, color=COLOR_EQUAL_2,
                        stroke_width=2.0).set_z_index(LAYER_GEOMETRY)
        seg_BpCp = Line(Bp_pos, Cp_pos, color=COLOR_EQUAL_2,
                        stroke_width=2.0).set_z_index(LAYER_GEOMETRY)
        seg_CpAp = Line(Cp_pos, Ap_pos, color=COLOR_EQUAL_2,
                        stroke_width=2.0).set_z_index(LAYER_GEOMETRY)

        dot_Ap = Dot(Ap_pos, color=COLOR_EQUAL_2,
                     radius=MARKER_DOT_RADIUS).set_z_index(LAYER_MARKERS)
        dot_Bp = Dot(Bp_pos, color=COLOR_EQUAL_2,
                     radius=MARKER_DOT_RADIUS).set_z_index(LAYER_MARKERS)
        dot_Cp = Dot(Cp_pos, color=COLOR_EQUAL_2,
                     radius=MARKER_DOT_RADIUS).set_z_index(LAYER_MARKERS)

        lbl_Ap = Tex(r"$A'$", tex_template=viet_tex_template,
                     font_size=24).next_to(dot_Ap, UR, buff=0.08)
        lbl_Bp = Tex(r"$B'$", tex_template=viet_tex_template,
                     font_size=24).next_to(dot_Bp, DL, buff=0.08)
        lbl_Cp = Tex(r"$C'$", tex_template=viet_tex_template,
                     font_size=24).next_to(dot_Cp, DR, buff=0.08)

        fig_abcp = VGroup(
            seg_ApBp, seg_BpCp, seg_CpAp,
            dot_Ap, dot_Bp, dot_Cp,
            lbl_Ap, lbl_Bp, lbl_Cp)

        # place_dual_figures → scale + đặt vào FigurePanel, trả VGroup
        self.figure_group = place_dual_figures(
            fig_abc, fig_abcp,
            label_left=r"$\Delta ABC$",
            label_right=r"$\Delta A'B'C'$",
            tex_template=viet_tex_template,
        )

        # ── Voiceover + Animations ────────────────────────────────────────────

        with self.voiceover(
            "Định nghĩa. Ta nói tam giác A phẩy B phẩy C phẩy đồng dạng với tam giác A B C "
            "khi thoả mãn đồng thời hai điều kiện."
        ) as ov:
            self.play(FadeIn(line1), run_time=ov.duration * 0.4)
            self.play(
                Create(seg_AB), Create(seg_BC), Create(seg_CA),
                FadeIn(dot_A1, dot_B1, dot_C1, lbl_A1, lbl_B1, lbl_C1),
                run_time=ov.duration * 0.6)

        with self.voiceover(
            "Thứ nhất, tỉ số các cạnh tương ứng bằng nhau: "
            "A phẩy B phẩy trên A B bằng B phẩy C phẩy trên B C bằng A phẩy C phẩy trên A C."
        ) as ov:
            self.play(Write(formula_ratio), run_time=ov.duration * 0.45)
            self.play(
                Create(seg_ApBp), Create(seg_BpCp), Create(seg_CpAp),
                FadeIn(dot_Ap, dot_Bp, dot_Cp, lbl_Ap, lbl_Bp, lbl_Cp),
                run_time=ov.duration * 0.55)

        with self.voiceover(
            "Thứ hai, ba góc tương ứng bằng nhau: "
            "góc A phẩy bằng góc A, góc B phẩy bằng góc B, góc C phẩy bằng góc C."
        ) as ov:
            self.play(Write(formula_angles), run_time=ov.duration)

        with self.voiceover(
            "Ta kí hiệu tam giác A phẩy B phẩy C phẩy đồng dạng với tam giác A B C "
            "bằng dấu ngoặc xoáy ngược. "
            "Giá trị k bằng tỉ số các cạnh tương ứng được gọi là tỉ số đồng dạng."
        ) as ov:
            self.play(Write(formula_symbol), run_time=ov.duration * 0.4)
            self.play(Write(formula_k), run_time=ov.duration * 0.35)
            self.play(FadeIn(line_k), run_time=ov.duration * 0.25)

        # Indicate các thuật ngữ in đậm
        self.play(
            Indicate(line1, scale_factor=EMPHASIS_SCALE, color=COLOR_ACTIVE),
            run_time=EMPHASIS_INDICATE_TIME)
        self.play(
            Indicate(line_k, scale_factor=EMPHASIS_SCALE, color=COLOR_ACTIVE),
            run_time=EMPHASIS_INDICATE_TIME)

        self.wait(0.5)

        # Cleanup — KEEP self.figure_group cho Scene 02
        self.play(
            FadeOut(block_heading),
            FadeOut(col.all),
            run_time=MOTION_EXIT)

    # =========================================================================
    # Scene 02 — Nhận xét
    # =========================================================================

    def scene02_nhanXet(self):
        # ── Heading ──────────────────────────────────────────────────────────
        block_heading = Tex(
            r"\textbf{Nhận xét}",
            tex_template=viet_tex_template, font_size=32)
        block_heading.to_corner(UL, buff=0.5)
        self.play(Write(block_heading), run_time=MOTION_ENTER)

        # ── TheoryColumn (có figure panel bên phải — tái dùng scene01) ────────
        col = TheoryColumn(block_heading, has_figure=True)

        # ── Tính chất 1: đối xứng ─────────────────────────────────────────────
        prop1a = MathTex(
            r"\Delta A'B'C' \backsim \Delta ABC \;\text{(tỉ số }k)",
            tex_template=viet_tex_template, font_size=24)
        col.place_formula(prop1a, gap=0.15)

        prop1b = MathTex(
            r"\Rightarrow \Delta ABC \backsim \Delta A'B'C' \;\text{(tỉ số } \tfrac{1}{k})",
            tex_template=viet_tex_template, font_size=24)
        col.place_formula(prop1b, gap=0.12)

        prop1_text = Tex(
            r"Ta nói hai tam giác $A'B'C'$ và $ABC$ \textbf{đồng dạng với nhau}.",
            tex_template=viet_tex_template, font_size=24)
        col.place(prop1_text, gap=0.28)

        # ── Tính chất 2: phản xạ và từ bằng nhau ─────────────────────────────
        prop2a = MathTex(
            r"\text{Hai tam giác bằng nhau} \Rightarrow \text{đồng dạng, } k = 1",
            tex_template=viet_tex_template, font_size=24)
        col.place_formula(prop2a, gap=0.15)

        prop2b = Tex(
            r"Mọi tam giác đồng dạng với chính nó $(k=1)$.",
            tex_template=viet_tex_template, font_size=24)
        col.place(prop2b, gap=0.28)

        # ── Tính chất 3: bắc cầu ──────────────────────────────────────────────
        prop3a = MathTex(
            r"\Delta A''B''C'' \backsim \Delta A'B'C' \;(k),\;"
            r"\Delta A'B'C' \backsim \Delta ABC \;(m)",
            tex_template=viet_tex_template, font_size=22)
        col.place_formula(prop3a, gap=0.12)

        prop3b = MathTex(
            r"\Rightarrow \Delta A''B''C'' \backsim \Delta ABC \;\text{tỉ số } k \cdot m",
            tex_template=viet_tex_template, font_size=24)
        col.place_formula(prop3b, gap=0.20)

        # ── Voiceover + Animations ────────────────────────────────────────────

        with self.voiceover(
            "Nhận xét. Có ba tính chất quan trọng về quan hệ đồng dạng. "
            "Thứ nhất, nếu tam giác A phẩy B phẩy C phẩy đồng dạng với tam giác A B C theo tỉ số k, "
            "thì ngược lại tam giác A B C đồng dạng với tam giác A phẩy B phẩy C phẩy theo tỉ số một phần k. "
            "Khi đó ta nói hai tam giác đồng dạng với nhau."
        ) as ov:
            self.play(FadeIn(prop1a), run_time=ov.duration * 0.28)
            self.play(FadeIn(prop1b), run_time=ov.duration * 0.40)
            self.play(FadeIn(prop1_text), run_time=ov.duration * 0.32)

        with self.voiceover(
            "Thứ hai, hai tam giác bằng nhau thì đồng dạng với tỉ số đồng dạng bằng một. "
            "Và mọi tam giác đều đồng dạng với chính nó."
        ) as ov:
            self.play(FadeIn(prop2a), run_time=ov.duration * 0.5)
            self.play(FadeIn(prop2b), run_time=ov.duration * 0.5)

        with self.voiceover(
            "Thứ ba, nếu tam giác A hai phẩy B hai phẩy C hai phẩy đồng dạng với "
            "tam giác A phẩy B phẩy C phẩy theo tỉ số k, "
            "và tam giác A phẩy B phẩy C phẩy đồng dạng với tam giác A B C theo tỉ số m, "
            "thì tam giác A hai phẩy B hai phẩy C hai phẩy đồng dạng với "
            "tam giác A B C theo tỉ số k nhân m."
        ) as ov:
            self.play(FadeIn(prop3a), run_time=ov.duration * 0.5)
            self.play(FadeIn(prop3b), run_time=ov.duration * 0.5)

        self.wait(0.5)

        # Cleanup — FadeOut tất cả kể cả figure_group từ scene01
        self.play(
            FadeOut(block_heading),
            FadeOut(col.all),
            FadeOut(self.figure_group),
            run_time=MOTION_EXIT)

    # =========================================================================
    # Scene 03 — Định lí
    # =========================================================================

    def scene03_dinhLi(self):
        # ── Heading ──────────────────────────────────────────────────────────
        block_heading = Tex(
            r"\textbf{2. Định lí}",
            tex_template=viet_tex_template, font_size=32)
        block_heading.to_corner(UL, buff=0.5)
        self.play(Write(block_heading), run_time=MOTION_ENTER)

        # ── TheoryColumn ──────────────────────────────────────────────────────
        col = TheoryColumn(block_heading, has_figure=True)

        # ── Phát biểu định lí ────────────────────────────────────────────────
        line1 = Tex(
            r"Nếu một đường thẳng cắt hai cạnh của một tam giác",
            tex_template=viet_tex_template, font_size=26)
        col.place(line1, gap=0.15)

        line2 = Tex(
            r"là \textbf{song song} với cạnh còn lại,",
            tex_template=viet_tex_template, font_size=26)
        col.place(line2, gap=0.15)

        line3 = Tex(
            r"thì nó tạo thành một tam giác mới \textbf{đồng dạng}",
            tex_template=viet_tex_template, font_size=26)
        col.place(line3, gap=0.15)

        line4 = Tex(
            r"với tam giác đã cho.",
            tex_template=viet_tex_template, font_size=26)
        col.place(line4, gap=0.32)

        # ── Công thức GT / KL ────────────────────────────────────────────────
        formula_gt = MathTex(
            r"\Delta ABC,\; MN \parallel BC \;(M \in AB,\; N \in AC)",
            tex_template=viet_tex_template, font_size=26)
        col.place_formula(formula_gt, gap=0.18)

        formula_kl = MathTex(
            r"\Rightarrow \Delta AMN \backsim \Delta ABC",
            tex_template=viet_tex_template, font_size=28)
        col.place_formula(formula_kl, gap=0.20)

        # ── Figure: geometry – △ABC với MN // BC ─────────────────────────────
        A3_pos = np.array([ 0.0,  2.2, 0])
        B3_pos = np.array([-2.0, -1.0, 0])
        C3_pos = np.array([ 2.0, -1.0, 0])

        # M trên AB, N trên AC, cùng tỉ lệ t = 0.55 tính từ A
        _t = 0.55
        M3_pos = A3_pos + _t * (B3_pos - A3_pos)
        N3_pos = A3_pos + _t * (C3_pos - A3_pos)

        # Các cạnh △ABC
        seg_AB3 = Line(A3_pos, B3_pos, color=COLOR_DEFAULT,
                       stroke_width=2.0).set_z_index(LAYER_GEOMETRY)
        seg_BC3 = Line(B3_pos, C3_pos, color=COLOR_DEFAULT,
                       stroke_width=2.0).set_z_index(LAYER_GEOMETRY)
        seg_CA3 = Line(C3_pos, A3_pos, color=COLOR_DEFAULT,
                       stroke_width=2.0).set_z_index(LAYER_GEOMETRY)

        # Đường MN (song song BC)
        seg_MN3 = Line(M3_pos, N3_pos, color=COLOR_EQUAL_2,
                       stroke_width=2.5).set_z_index(LAYER_GEOMETRY)

        # Dots
        dot_A3 = Dot(A3_pos, color=COLOR_DEFAULT,
                     radius=MARKER_DOT_RADIUS).set_z_index(LAYER_MARKERS)
        dot_B3 = Dot(B3_pos, color=COLOR_DEFAULT,
                     radius=MARKER_DOT_RADIUS).set_z_index(LAYER_MARKERS)
        dot_C3 = Dot(C3_pos, color=COLOR_DEFAULT,
                     radius=MARKER_DOT_RADIUS).set_z_index(LAYER_MARKERS)
        dot_M3 = Dot(M3_pos, color=COLOR_EQUAL_2,
                     radius=MARKER_DOT_RADIUS).set_z_index(LAYER_MARKERS)
        dot_N3 = Dot(N3_pos, color=COLOR_EQUAL_2,
                     radius=MARKER_DOT_RADIUS).set_z_index(LAYER_MARKERS)

        # Labels
        lbl_A3 = Tex(r"$A$", tex_template=viet_tex_template,
                     font_size=24).next_to(dot_A3, UP,    buff=0.10)
        lbl_B3 = Tex(r"$B$", tex_template=viet_tex_template,
                     font_size=24).next_to(dot_B3, DL,    buff=0.10)
        lbl_C3 = Tex(r"$C$", tex_template=viet_tex_template,
                     font_size=24).next_to(dot_C3, DR,    buff=0.10)
        lbl_M3 = Tex(r"$M$", tex_template=viet_tex_template,
                     font_size=24).next_to(dot_M3, LEFT,  buff=0.10)
        lbl_N3 = Tex(r"$N$", tex_template=viet_tex_template,
                     font_size=24).next_to(dot_N3, RIGHT, buff=0.10)

        # Dấu song song (//) trên MN và BC
        tick_MN = _parallel_marks(seg_MN3, color=COLOR_EQUAL_1)
        tick_BC = _parallel_marks(seg_BC3, color=COLOR_EQUAL_1)

        # Tô nhẹ △AMN để phân biệt
        fill_AMN = Polygon(
            A3_pos, M3_pos, N3_pos,
            fill_color=COLOR_EQUAL_2, fill_opacity=0.15,
            stroke_width=0.0).set_z_index(LAYER_GEOMETRY - 1)

        # ── GeometryEngine ────────────────────────────────────────────────────
        # Dùng để highlight_segment "MN" và "BC" (song song) trong voiceover.
        # Không dùng register_triangle_fill vì fills phải được tạo SAU place_figure
        # để tọa độ khớp với vị trí đã scale/move.
        self.geo = GeometryEngine(self)
        self.geo.register_point("A", A3_pos, dot=dot_A3)
        self.geo.register_point("B", B3_pos, dot=dot_B3)
        self.geo.register_point("C", C3_pos, dot=dot_C3)
        self.geo.register_point("M", M3_pos, dot=dot_M3)
        self.geo.register_point("N", N3_pos, dot=dot_N3)

        self.geo.register_segment("AB", seg_AB3)
        self.geo.register_segment("BC", seg_BC3)
        self.geo.register_segment("CA", seg_CA3)
        self.geo.register_segment("MN", seg_MN3)

        # ── Đặt figure vào panel ──────────────────────────────────────────────
        self.figure_group = VGroup(
            seg_AB3, seg_BC3, seg_CA3, seg_MN3,
            fill_AMN,
            dot_A3, dot_B3, dot_C3, dot_M3, dot_N3,
            lbl_A3, lbl_B3, lbl_C3, lbl_M3, lbl_N3,
            tick_MN, tick_BC,
        )
        place_figure(self.figure_group)

        # ── Voiceover + Animations ────────────────────────────────────────────

        with self.voiceover(
            "Định lí. Xét tam giác A B C."
        ) as ov:
            self.play(FadeIn(line1), run_time=ov.duration * 0.3)
            self.play(
                Create(seg_AB3), Create(seg_BC3), Create(seg_CA3),
                FadeIn(dot_A3, dot_B3, dot_C3, lbl_A3, lbl_B3, lbl_C3),
                run_time=ov.duration * 0.7)

        with self.voiceover(
            "Nếu ta vẽ đường thẳng M N cắt cạnh A B tại M và cắt cạnh A C tại N, "
            "sao cho M N song song với B C."
        ) as ov:
            self.play(FadeIn(line2), run_time=ov.duration * 0.15)
            self.play(
                FadeIn(dot_M3, dot_N3, lbl_M3, lbl_N3),
                Create(seg_MN3),
                run_time=ov.duration * 0.5)
            self.play(
                FadeIn(tick_MN, tick_BC),
                run_time=ov.duration * 0.35)

        with self.voiceover(
            "Thì nó tạo thành một tam giác mới đồng dạng với tam giác đã cho. "
            "Cụ thể, tam giác A M N đồng dạng với tam giác A B C."
        ) as ov:
            self.play(FadeIn(line3, line4), run_time=ov.duration * 0.2)
            self.play(Write(formula_gt), run_time=ov.duration * 0.35)
            self.play(FadeIn(fill_AMN), run_time=ov.duration * 0.1)
            self.play(Write(formula_kl), run_time=ov.duration * 0.35)

        # Highlight cạnh MN // BC bằng GeometryEngine, rồi nhấn mạnh kết luận
        with self.voiceover(
            "Trên hình, M N song song với B C, và tam giác A M N đồng dạng với tam giác A B C."
        ) as ov:
            # Highlight song song: MN và BC cùng màu EQUAL_1
            self.geo.highlight_segment("MN", color=COLOR_EQUAL_1,
                                       run_time=TIMING_INDICATE_SEGMENT)
            self.geo.highlight_segment("BC", color=COLOR_EQUAL_1,
                                       run_time=TIMING_INDICATE_SEGMENT)
            # Nhấn mạnh △AMN bằng fill animation
            self.play(
                fill_AMN.animate.set_fill(opacity=0.45),
                run_time=ov.duration * 0.3,
                rate_func=there_and_back)
            self.play(
                Indicate(formula_kl, scale_factor=EMPHASIS_SCALE, color=COLOR_ACTIVE),
                run_time=EMPHASIS_INDICATE_TIME)

        # Indicate thuật ngữ in đậm
        self.play(
            Indicate(line2, scale_factor=EMPHASIS_SCALE, color=COLOR_ACTIVE),
            run_time=EMPHASIS_INDICATE_TIME)
        self.play(
            Indicate(line3, scale_factor=EMPHASIS_SCALE, color=COLOR_ACTIVE),
            run_time=EMPHASIS_INDICATE_TIME)

        self.wait(0.5)

        # Cleanup — FadeOut tất cả
        self.play(
            FadeOut(block_heading),
            FadeOut(col.all),
            FadeOut(self.figure_group),
            run_time=MOTION_EXIT)
