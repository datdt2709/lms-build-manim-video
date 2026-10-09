"""BÀI 3. TỨ GIÁC NỘI TIẾP — video lý thuyết (spec: specs/theory/tu-giac-noi-tiep/spec-ly-thuyet.md)."""

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
    COLOR_DEFAULT,
    COLOR_BACKGROUND,
    COLOR_GRID,
    COLOR_EQUAL_1,
    COLOR_EQUAL_2,
    COLOR_ACTIVE,
    COLOR_CIRCLE,
    COLOR_AUX_LINE,
    STATE_DEFAULT,
    STATE_HIGHLIGHT,
    TIMING_FADE,
    MOTION_ENTER,
    MOTION_EXIT,
    MOTION_TITLE_OUT,
    EMPHASIS_SCALE,
    EMPHASIS_COLOR,
    LAYER_GEOMETRY,
    LAYER_MARKERS,
    MARKER_DOT_RADIUS,
    AngleMarker,
    TheoryColumn,
    place_figure,
    place_dual_figures,
    make_gtts_service,
)

viet_tex_template = TexTemplate(
    tex_compiler="xelatex",
    output_format=".xdv",
    preamble=r"""
\usepackage{fontspec}
\usepackage{amsmath}
\usepackage{amssymb}
\usepackage{vntex}
\setmainfont{Times New Roman}
""",
)

# ---------------------------------------------------------------------------
# Hằng số hình — từ spec-ly-thuyet.md
# ---------------------------------------------------------------------------

R_CIRC = 2.2
O_POS = ORIGIN
ANGLES_ABCD = (70, 160, 250, 340)  # độ, CCW từ trục Ox


def _pt_on_circle(deg: float) -> np.ndarray:
    th = deg * DEGREES
    return O_POS + np.array([R_CIRC * np.cos(th), R_CIRC * np.sin(th), 0])


def _label_point(name: str, pos: np.ndarray, direction) -> MathTex:
    lbl = MathTex(name, font_size=24)
    lbl.next_to(pos, direction, buff=0.15)
    return lbl.set_z_index(LAYER_MARKERS)


class TuGiacNoiTiep(VoiceoverScene):
    """Bài giảng lý thuyết: Tứ giác nội tiếp."""

    def construct(self):
        self.set_speech_service(make_gtts_service())
        self.setup_scene_style()
        self.scene00_intro()
        self.scene01_dinhNghia()
        self.scene02_dinhLi()
        self.scene03_nhanXet()

    def setup_scene_style(self):
        Mobject.set_default(color=COLOR_DEFAULT)
        Tex.set_default(color=COLOR_DEFAULT)
        MathTex.set_default(color=COLOR_DEFAULT)
        self.camera.background_color = COLOR_BACKGROUND
        grid = NumberPlane(
            x_range=[-8, 8, 1],
            y_range=[-5, 5, 1],
            axis_config={"stroke_width": 0},
            background_line_style={
                "stroke_color": COLOR_GRID,
                "stroke_width": 1,
                "stroke_opacity": 0.4,
            },
        )
        grid.set_z_index(-10)
        self.add(grid)

    # ------------------------------------------------------------------
    # Scene 00 — Intro
    # ------------------------------------------------------------------

    def scene00_intro(self):
        self.lesson_title = Tex(
            r"\textbf{BÀI 3. TỨ GIÁC NỘI TIẾP}",
            tex_template=viet_tex_template,
            font_size=36,
        )
        self.lesson_title.to_edge(UP, buff=0.4)

        section_heading = Tex(
            r"\textbf{I. TÓM TẮT LÝ THUYẾT}",
            tex_template=viet_tex_template,
            font_size=28,
        )
        section_heading.next_to(self.lesson_title, DOWN, buff=0.35)

        with self.voiceover(
            text="Bài ba. Tứ giác nội tiếp. Phần một. Tóm tắt lý thuyết."
        ) as ov:
            self.play(Write(self.lesson_title), run_time=ov.duration * 0.55)
            self.play(FadeIn(section_heading), run_time=ov.duration * 0.45)

        self.wait(1.5)
        self.play(FadeOut(section_heading), run_time=MOTION_TITLE_OUT)

    # ------------------------------------------------------------------
    # Scene 01 — Định nghĩa
    # ------------------------------------------------------------------

    def scene01_dinhNghia(self):
        if not hasattr(self, "lesson_title"):
            self.lesson_title = Tex(
                r"\textbf{BÀI 3. TỨ GIÁC NỘI TIẾP}",
                tex_template=viet_tex_template,
                font_size=36,
            ).to_edge(UP, buff=0.4)
            self.add(self.lesson_title)

        block_heading = Tex(
            r"\textbf{1. Định nghĩa}",
            tex_template=viet_tex_template,
            font_size=32,
        )
        block_heading.to_corner(UL, buff=0.5)
        self.play(Write(block_heading), run_time=MOTION_ENTER)

        col = TheoryColumn(block_heading, has_figure=True)

        line1 = Tex(
            r"Tứ giác có bốn đỉnh nằm trên một đường tròn được gọi là",
            tex_template=viet_tex_template,
            font_size=26,
        )
        line2 = Tex(
            r"\textbf{tứ giác nội tiếp đường tròn}",
            tex_template=viet_tex_template,
            font_size=26,
        )
        line3 = Tex(
            r"(hoặc đơn giản là \textbf{tứ giác nội tiếp})",
            tex_template=viet_tex_template,
            font_size=26,
        )
        line4 = Tex(
            r"và đường tròn được gọi là",
            tex_template=viet_tex_template,
            font_size=26,
        )
        line5 = Tex(
            r"\textbf{đường tròn ngoại tiếp tứ giác}.",
            tex_template=viet_tex_template,
            font_size=26,
        )
        col.place(line1)
        col.place(line2)
        col.place(line3)
        col.place(line4)
        col.place(line5)

        self.A_pos = _pt_on_circle(ANGLES_ABCD[0])
        self.B_pos = _pt_on_circle(ANGLES_ABCD[1])
        self.C_pos = _pt_on_circle(ANGLES_ABCD[2])
        self.D_pos = _pt_on_circle(ANGLES_ABCD[3])

        circ_O = (
            Circle(radius=R_CIRC, color=COLOR_CIRCLE)
            .move_to(O_POS)
            .set_stroke(width=STATE_HIGHLIGHT["stroke_width"])
            .set_z_index(LAYER_GEOMETRY)
        )
        quad_ABCD = Polygon(
            self.A_pos,
            self.B_pos,
            self.C_pos,
            self.D_pos,
            color=COLOR_DEFAULT,
            fill_opacity=0,
        )
        quad_ABCD.set_stroke(
            color=COLOR_DEFAULT, width=STATE_DEFAULT["stroke_width"]
        ).set_z_index(LAYER_GEOMETRY)

        dot_O = Dot(O_POS, radius=MARKER_DOT_RADIUS, color=COLOR_ACTIVE).set_z_index(
            LAYER_MARKERS
        )
        dot_A = Dot(self.A_pos, radius=MARKER_DOT_RADIUS).set_z_index(LAYER_MARKERS)
        dot_B = Dot(self.B_pos, radius=MARKER_DOT_RADIUS).set_z_index(LAYER_MARKERS)
        dot_C = Dot(self.C_pos, radius=MARKER_DOT_RADIUS).set_z_index(LAYER_MARKERS)
        dot_D = Dot(self.D_pos, radius=MARKER_DOT_RADIUS).set_z_index(LAYER_MARKERS)

        label_O = _label_point("O", O_POS, DOWN)
        label_A = _label_point("A", self.A_pos, UL)
        label_B = _label_point("B", self.B_pos, UR)
        label_C = _label_point("C", self.C_pos, DR)
        label_D = _label_point("D", self.D_pos, DL)

        self.figure_group = VGroup(
            circ_O,
            quad_ABCD,
            dot_O,
            dot_A,
            dot_B,
            dot_C,
            dot_D,
            label_O,
            label_A,
            label_B,
            label_C,
            label_D,
        )
        place_figure(self.figure_group)

        with self.voiceover(
            text=(
                "Định nghĩa. Tứ giác có bốn đỉnh nằm trên một đường tròn "
                "được gọi là tứ giác nội tiếp đường tròn, "
                "hoặc đơn giản là tứ giác nội tiếp."
            )
        ) as ov:
            self.play(
                FadeIn(line1),
                Create(circ_O),
                FadeIn(dot_O),
                Write(label_O),
                run_time=ov.duration * 0.45,
            )
            self.play(
                FadeIn(line2),
                FadeIn(line3),
                FadeIn(dot_A),
                FadeIn(dot_B),
                FadeIn(dot_C),
                FadeIn(dot_D),
                run_time=ov.duration * 0.55,
            )

        with self.voiceover(
            text="Đường tròn đó được gọi là đường tròn ngoại tiếp tứ giác."
        ) as ov:
            self.play(
                FadeIn(line4),
                FadeIn(line5),
                Create(quad_ABCD),
                Write(label_A),
                Write(label_B),
                Write(label_C),
                Write(label_D),
                run_time=ov.duration,
            )

        with self.voiceover(
            text=(
                "Chẳng hạn, trên hình vẽ, tứ giác A B C D "
                "có bốn đỉnh A, B, C, D đều nằm trên đường tròn tâm O."
            )
        ) as ov:
            self.play(
                Indicate(
                    VGroup(dot_A, dot_B, dot_C, dot_D),
                    scale_factor=EMPHASIS_SCALE + 0.05,
                    color=EMPHASIS_COLOR,
                ),
                run_time=ov.duration * 0.55,
            )
            self.play(
                Indicate(line2, scale_factor=EMPHASIS_SCALE, color=EMPHASIS_COLOR),
                run_time=ov.duration * 0.2,
            )
            self.play(
                Indicate(line3, scale_factor=EMPHASIS_SCALE, color=EMPHASIS_COLOR),
                run_time=ov.duration * 0.12,
            )
            self.play(
                Indicate(line5, scale_factor=EMPHASIS_SCALE, color=EMPHASIS_COLOR),
                run_time=ov.duration * 0.13,
            )

        self.wait(TIMING_FADE)
        self.play(
            FadeOut(block_heading),
            FadeOut(col.all),
            run_time=MOTION_EXIT,
        )

    # ------------------------------------------------------------------
    # Scene 02 — Định lí (tái dùng figure_group)
    # ------------------------------------------------------------------

    def scene02_dinhLi(self):
        block_heading = Tex(
            r"\textbf{2. Định lí}",
            tex_template=viet_tex_template,
            font_size=32,
        )
        block_heading.to_corner(UL, buff=0.5)
        self.play(Write(block_heading), run_time=MOTION_ENTER)

        col = TheoryColumn(block_heading, has_figure=True)

        statement = Tex(
            r"Trong một tứ giác nội tiếp, tổng số đo hai góc đối nhau bằng $180^\circ$.",
            tex_template=viet_tex_template,
            font_size=26,
        )
        context = Tex(
            r"Trên hình vẽ, tứ giác $ABCD$ nội tiếp $(O)$ nên",
            tex_template=viet_tex_template,
            font_size=26,
        )
        col.place(statement, gap=0.30)
        col.place(context, gap=0.22)

        formula_main = MathTex(
            r"\widehat{A} + \widehat{C} = \widehat{B} + \widehat{D} = 180^\circ",
            tex_template=viet_tex_template,
            font_size=34,
        )
        col.place_formula(formula_main)

        formula_part_1 = MathTex(
            r"\widehat{A} + \widehat{C} = 180^\circ",
            tex_template=viet_tex_template,
            font_size=30,
        )
        formula_part_2 = MathTex(
            r"\widehat{B} + \widehat{D} = 180^\circ",
            tex_template=viet_tex_template,
            font_size=30,
        )
        col.place_formula(formula_part_1, gap=0.25)
        col.place_formula(formula_part_2, gap=0.25)

        ang_A = AngleMarker(
            self.D_pos, self.A_pos, self.B_pos,
            color=COLOR_EQUAL_1, radius=0.35,
        )
        ang_C = AngleMarker(
            self.B_pos, self.C_pos, self.D_pos,
            color=COLOR_EQUAL_1, radius=0.35,
        )
        ang_B = AngleMarker(
            self.A_pos, self.B_pos, self.C_pos,
            color=COLOR_EQUAL_2, radius=0.35,
        )
        ang_D = AngleMarker(
            self.C_pos, self.D_pos, self.A_pos,
            color=COLOR_EQUAL_2, radius=0.35,
        )

        lbl_ang_A = MathTex(r"\widehat{A}", font_size=22).next_to(
            self.A_pos, UL, buff=0.32
        ).set_z_index(LAYER_MARKERS)
        lbl_ang_C = MathTex(r"\widehat{C}", font_size=22).next_to(
            self.C_pos, DR, buff=0.32
        ).set_z_index(LAYER_MARKERS)
        lbl_ang_B = MathTex(r"\widehat{B}", font_size=22).next_to(
            self.B_pos, UR, buff=0.32
        ).set_z_index(LAYER_MARKERS)
        lbl_ang_D = MathTex(r"\widehat{D}", font_size=22).next_to(
            self.D_pos, DL, buff=0.32
        ).set_z_index(LAYER_MARKERS)

        self.angle_group = VGroup(
            ang_A, ang_C, ang_B, ang_D,
            lbl_ang_A, lbl_ang_C, lbl_ang_B, lbl_ang_D,
        )

        with self.voiceover(
            text=(
                "Định lí. Trong một tứ giác nội tiếp, "
                "tổng số đo hai góc đối nhau bằng 180 độ."
            )
        ) as ov:
            self.play(FadeIn(statement), run_time=ov.duration * 0.45)
            self.play(Write(formula_main), run_time=ov.duration * 0.55)

        with self.voiceover(
            text=(
                "Trên hình vẽ, tứ giác A B C D nội tiếp đường tròn tâm O "
                "nên góc A cộng góc C bằng 180 độ."
            )
        ) as ov:
            self.play(FadeIn(context), run_time=ov.duration * 0.2)
            self.play(
                Create(ang_A),
                Create(ang_C),
                Write(lbl_ang_A),
                Write(lbl_ang_C),
                run_time=ov.duration * 0.35,
            )
            self.play(
                Indicate(ang_A, color=COLOR_EQUAL_1, scale_factor=EMPHASIS_SCALE),
                Indicate(ang_C, color=COLOR_EQUAL_1, scale_factor=EMPHASIS_SCALE),
                run_time=ov.duration * 0.25,
            )
            self.play(Write(formula_part_1), run_time=ov.duration * 0.2)

        with self.voiceover(
            text="Tương tự, góc B cộng góc D cũng bằng 180 độ."
        ) as ov:
            self.play(
                Create(ang_B),
                Create(ang_D),
                Write(lbl_ang_B),
                Write(lbl_ang_D),
                run_time=ov.duration * 0.4,
            )
            self.play(
                Indicate(ang_B, color=COLOR_EQUAL_2, scale_factor=EMPHASIS_SCALE),
                Indicate(ang_D, color=COLOR_EQUAL_2, scale_factor=EMPHASIS_SCALE),
                run_time=ov.duration * 0.35,
            )
            self.play(Write(formula_part_2), run_time=ov.duration * 0.25)

        self.wait(1.0)
        self.play(
            FadeOut(block_heading),
            FadeOut(col.all),
            FadeOut(self.angle_group),
            FadeOut(self.figure_group),
            run_time=MOTION_EXIT,
        )

    # ------------------------------------------------------------------
    # Scene 03 — Nhận xét (dual geometry)
    # ------------------------------------------------------------------

    def _build_rect_figure(self):
        hw, hh = 1.4, 0.8
        A = np.array([-hw, hh, 0])
        B = np.array([hw, hh, 0])
        C = np.array([hw, -hh, 0])
        D = np.array([-hw, -hh, 0])
        O = ORIGIN

        rect_ABCD = Rectangle(
            width=2.8, height=1.6, color=COLOR_DEFAULT, fill_opacity=0
        )
        rect_ABCD.set_stroke(
            color=COLOR_DEFAULT, width=STATE_DEFAULT["stroke_width"]
        ).set_z_index(LAYER_GEOMETRY)

        dot_A = Dot(A, radius=MARKER_DOT_RADIUS).set_z_index(LAYER_MARKERS)
        dot_B = Dot(B, radius=MARKER_DOT_RADIUS).set_z_index(LAYER_MARKERS)
        dot_C = Dot(C, radius=MARKER_DOT_RADIUS).set_z_index(LAYER_MARKERS)
        dot_D = Dot(D, radius=MARKER_DOT_RADIUS).set_z_index(LAYER_MARKERS)
        dot_O = Dot(O, radius=MARKER_DOT_RADIUS, color=COLOR_ACTIVE).set_z_index(
            LAYER_MARKERS
        )

        label_A = _label_point("A", A, UL)
        label_B = _label_point("B", B, UR)
        label_C = _label_point("C", C, DR)
        label_D = _label_point("D", D, DL)
        label_O = _label_point("O", O, DOWN)

        seg_AC = DashedLine(A, C, color=COLOR_AUX_LINE, dash_length=0.12).set_z_index(
            LAYER_GEOMETRY
        )
        seg_BD = DashedLine(B, D, color=COLOR_AUX_LINE, dash_length=0.12).set_z_index(
            LAYER_GEOMETRY
        )
        R = np.linalg.norm(A - O)
        circ_O = (
            Circle(radius=R, color=COLOR_CIRCLE)
            .move_to(O)
            .set_stroke(width=STATE_HIGHLIGHT["stroke_width"])
            .set_z_index(LAYER_GEOMETRY)
        )

        labels = VGroup(label_A, label_B, label_C, label_D, label_O)
        fig = VGroup(
            rect_ABCD,
            seg_AC,
            seg_BD,
            circ_O,
            dot_A,
            dot_B,
            dot_C,
            dot_D,
            dot_O,
            labels,
        )
        return {
            "group": fig,
            "outline": rect_ABCD,
            "diagonals": VGroup(seg_AC, seg_BD),
            "circle": circ_O,
            "dot_O": dot_O,
        }

    def _build_square_figure(self):
        hs = 0.9
        E = np.array([-hs, hs, 0])
        F = np.array([hs, hs, 0])
        G = np.array([hs, -hs, 0])
        H = np.array([-hs, -hs, 0])
        O = ORIGIN

        sq_EFGH = Square(side_length=1.8, color=COLOR_DEFAULT, fill_opacity=0)
        sq_EFGH.set_stroke(
            color=COLOR_DEFAULT, width=STATE_DEFAULT["stroke_width"]
        ).set_z_index(LAYER_GEOMETRY)

        dot_E = Dot(E, radius=MARKER_DOT_RADIUS).set_z_index(LAYER_MARKERS)
        dot_F = Dot(F, radius=MARKER_DOT_RADIUS).set_z_index(LAYER_MARKERS)
        dot_G = Dot(G, radius=MARKER_DOT_RADIUS).set_z_index(LAYER_MARKERS)
        dot_H = Dot(H, radius=MARKER_DOT_RADIUS).set_z_index(LAYER_MARKERS)
        dot_O = Dot(O, radius=MARKER_DOT_RADIUS, color=COLOR_ACTIVE).set_z_index(
            LAYER_MARKERS
        )

        label_E = _label_point("E", E, UL)
        label_F = _label_point("F", F, UR)
        label_G = _label_point("G", G, DR)
        label_H = _label_point("H", H, DL)
        label_O = _label_point("O", O, DOWN)

        seg_EG = DashedLine(E, G, color=COLOR_AUX_LINE, dash_length=0.12).set_z_index(
            LAYER_GEOMETRY
        )
        seg_FH = DashedLine(F, H, color=COLOR_AUX_LINE, dash_length=0.12).set_z_index(
            LAYER_GEOMETRY
        )
        R = np.linalg.norm(E - O)
        circ_O = (
            Circle(radius=R, color=COLOR_CIRCLE)
            .move_to(O)
            .set_stroke(width=STATE_HIGHLIGHT["stroke_width"])
            .set_z_index(LAYER_GEOMETRY)
        )

        labels = VGroup(label_E, label_F, label_G, label_H, label_O)
        fig = VGroup(
            sq_EFGH,
            seg_EG,
            seg_FH,
            circ_O,
            dot_E,
            dot_F,
            dot_G,
            dot_H,
            dot_O,
            labels,
        )
        return {
            "group": fig,
            "outline": sq_EFGH,
            "diagonals": VGroup(seg_EG, seg_FH),
            "circle": circ_O,
            "dot_O": dot_O,
        }

    def scene03_nhanXet(self):
        block_heading = Tex(
            r"\textbf{3. Nhận xét}",
            tex_template=viet_tex_template,
            font_size=32,
        )
        block_heading.to_corner(UL, buff=0.5)
        self.play(Write(block_heading), run_time=MOTION_ENTER)

        col = TheoryColumn(block_heading, has_figure=True)

        line1 = Tex(
            r"Hình chữ nhật và hình vuông là các tứ giác nội tiếp.",
            tex_template=viet_tex_template,
            font_size=26,
        )
        line2 = Tex(
            r"Đường tròn ngoại tiếp của chúng có tâm là giao điểm của hai đường chéo",
            tex_template=viet_tex_template,
            font_size=26,
        )
        line3 = Tex(
            r"và bán kính bằng một nửa độ dài đường chéo.",
            tex_template=viet_tex_template,
            font_size=26,
        )
        col.place(line1)
        col.place(line2)
        col.place(line3)

        rect_data = self._build_rect_figure()
        sq_data = self._build_square_figure()

        self.dual_panel = place_dual_figures(
            rect_data["group"],
            sq_data["group"],
            label_left="Hình chữ nhật",
            label_right="Hình vuông",
            tex_template=viet_tex_template,
        )

        with self.voiceover(
            text=(
                "Nhận xét. Hình chữ nhật và hình vuông là các tứ giác nội tiếp."
            )
        ) as ov:
            self.play(FadeIn(line1), run_time=ov.duration * 0.25)
            self.play(
                Create(rect_data["outline"]),
                Create(sq_data["outline"]),
                run_time=ov.duration * 0.75,
            )

        with self.voiceover(
            text=(
                "Đường tròn ngoại tiếp của chúng "
                "có tâm là giao điểm của hai đường chéo."
            )
        ) as ov:
            self.play(FadeIn(line2), run_time=ov.duration * 0.2)
            self.play(
                Create(rect_data["diagonals"]),
                Create(sq_data["diagonals"]),
                run_time=ov.duration * 0.45,
            )
            self.play(
                FadeIn(rect_data["dot_O"]),
                FadeIn(sq_data["dot_O"]),
                Indicate(
                    VGroup(rect_data["dot_O"], sq_data["dot_O"]),
                    scale_factor=EMPHASIS_SCALE,
                    color=EMPHASIS_COLOR,
                ),
                run_time=ov.duration * 0.35,
            )

        with self.voiceover(
            text=(
                "Bán kính bằng một nửa độ dài đường chéo. "
                "Trên hình bên trái, hai đường chéo của hình chữ nhật "
                "cắt nhau tại O, và đường tròn tâm O đi qua bốn đỉnh. "
                "Tương tự với hình vuông bên phải."
            )
        ) as ov:
            self.play(FadeIn(line3), run_time=ov.duration * 0.15)
            self.play(
                Create(rect_data["circle"]),
                Create(sq_data["circle"]),
                run_time=ov.duration * 0.35,
            )
            self.play(
                Indicate(
                    rect_data["diagonals"],
                    color=COLOR_AUX_LINE,
                    scale_factor=EMPHASIS_SCALE,
                ),
                run_time=ov.duration * 0.25,
            )
            self.play(
                Indicate(
                    VGroup(line2, line3),
                    scale_factor=EMPHASIS_SCALE,
                    color=EMPHASIS_COLOR,
                ),
                run_time=ov.duration * 0.25,
            )

        self.wait(1.5)
        self.play(
            FadeOut(block_heading),
            FadeOut(col.all),
            FadeOut(self.dual_panel),
            FadeOut(self.lesson_title),
            run_time=MOTION_EXIT,
        )
