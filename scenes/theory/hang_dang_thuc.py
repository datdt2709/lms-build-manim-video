"""HẰNG ĐẲNG THỨC ĐÁNG NHỚ — video lý thuyết.

Spec: specs/theory/hang_dang_thuc/spec-ly-thuyet.md
Subject: algebra   |   Scenes: 6   |   ~6–8 phút
figure.type: none cho toàn bộ — ảnh SGK không có hình vẽ.
"""

import sys
from pathlib import Path

_PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(_PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(_PROJECT_ROOT))

from manim import *
from manim_voiceover import VoiceoverScene

from manim_helpers import (
    COLOR_DEFAULT,
    COLOR_BACKGROUND,
    COLOR_GRID,
    COLOR_EQUAL_1,
    COLOR_EQUAL_2,
    COLOR_RESULT_KEY,
    MOTION_ENTER,
    MOTION_EXIT,
    MOTION_TITLE_OUT,
    EMPHASIS_SCALE,
    EMPHASIS_COLOR,
    EMPHASIS_INDICATE_TIME,
    TheoryColumn,
    TEXT_LEFT_X,
    make_lesson_title,
    make_gtts_service,
)

# ---------------------------------------------------------------------------
# TeX template chuẩn — bắt buộc cho mọi Tex/MathTex có tiếng Việt
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
""",
)

# ---------------------------------------------------------------------------
# Layout constants — theo spec-ly-thuyet.md
# ---------------------------------------------------------------------------

TEXT_ONLY_FONT = 28
WRAP_WIDTH_CM  = 14
BODY_GAP       = 0.16
FORMULA_GAP    = 0.28
FORMULA_INDENT = 0.8


def tex_wrapped(
    text: str,
    width_cm: float = WRAP_WIDTH_CM,
    font_size: int = TEXT_ONLY_FONT,
) -> Tex:
    """Wrap text trong minipage raggedright để tránh LaTeX tự ngắt dòng."""
    body = (
        rf"\begin{{minipage}}{{{width_cm}cm}}"
        rf"\raggedright {text}\end{{minipage}}"
    )
    return Tex(body, tex_template=viet_tex_template, font_size=font_size)


# ---------------------------------------------------------------------------
# Scene class
# ---------------------------------------------------------------------------

class HangDangThuc(VoiceoverScene):
    """Bài giảng lý thuyết: Hằng đẳng thức đáng nhớ."""

    def construct(self):
        self.set_speech_service(make_gtts_service())
        self.setup_scene_style()
        self.scene00_intro()
        self.scene01_dinhNghia()
        # self.scene02_binhPhuongTong()
        # self.scene03_binhPhuongHieu()
        # self.scene04_viDu21()
        # self.scene05_hieuHaiBinhPhuong()

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

    # ── Scene 00 — Intro ──────────────────────────────────────────────────────

    def scene00_intro(self):
        self.lesson_title = make_lesson_title(
            r"\textbf{HẰNG ĐẲNG THỨC ĐÁNG NHỚ}", viet_tex_template
        )
        with self.voiceover(text="Hằng đẳng thức đáng nhớ.") as ov:
            self.play(FadeIn(self.lesson_title), run_time=ov.duration)
        self.wait(1.0)

    # ── Scene 01 — Định nghĩa hằng đẳng thức ─────────────────────────────────

    def scene01_dinhNghia(self):
        if not hasattr(self, "lesson_title"):
            self.lesson_title = make_lesson_title(
                r"\textbf{HẰNG ĐẲNG THỨC ĐÁNG NHỚ}", viet_tex_template
            )
            self.add(self.lesson_title)

        block_heading = Tex(
            r"\textbf{1. Hằng đẳng thức}",
            tex_template=viet_tex_template,
            font_size=32,
        )
        block_heading.next_to(self.lesson_title, DOWN, buff=0.35)
        block_heading.align_to([TEXT_LEFT_X, 0, 0], LEFT)
        self.play(Write(block_heading), run_time=MOTION_ENTER)

        col = TheoryColumn(block_heading, has_figure=False)

        line1 = tex_wrapped(
            r"Nếu hai biểu thức $P$ và $Q$ nhận giá trị như nhau"
            r" với mọi giá trị của biến, thì $P = Q$ được gọi là"
            r" một \textbf{đồng nhất thức} hay một \textbf{hằng đẳng thức}."
        )
        col.place(line1, gap=BODY_GAP)

        line_ex_intro = tex_wrapped(r"Ví dụ: Đẳng thức")
        col.place(line_ex_intro, gap=0.12)

        formula_ex = MathTex(r"3(x + y) = 3x + 3y", font_size=32)
        col.place_formula_left(formula_ex, indent=FORMULA_INDENT, gap=0.15)

        line_ex_end = tex_wrapped(r"là một hằng đẳng thức.")
        col.place(line_ex_end, gap=BODY_GAP)

        with self.voiceover(
            text=(
                "Định nghĩa. "
                "Nếu hai biểu thức P và Q nhận giá trị như nhau "
                "với mọi giá trị của biến, "
                "thì P bằng Q được gọi là một đồng nhất thức "
                "hay một hằng đẳng thức."
            )
        ) as ov:
            self.play(FadeIn(line1), run_time=ov.duration * 0.80)
            self.play(
                Indicate(line1, scale_factor=EMPHASIS_SCALE, color=EMPHASIS_COLOR),
                run_time=ov.duration * 0.20,
            )

        with self.voiceover(
            text=(
                "Ví dụ, ba nhân tổng x cộng y bằng ba x cộng ba y "
                "là một hằng đẳng thức."
            )
        ) as ov:
            self.play(FadeIn(line_ex_intro), run_time=ov.duration * 0.20)
            self.play(Write(formula_ex), run_time=ov.duration * 0.50)
            self.play(FadeIn(line_ex_end), run_time=ov.duration * 0.30)

        self.wait(1.0)
        self.play(
            FadeOut(block_heading),
            FadeOut(col.all),
            run_time=MOTION_EXIT,
        )

    # ── Scene 02 — 2.1 Bình phương của một tổng ──────────────────────────────

    def scene02_binhPhuongTong(self):
        block_heading = Tex(
            r"\textbf{2.1. Bình phương của một tổng}",
            tex_template=viet_tex_template,
            font_size=32,
        )
        block_heading.next_to(self.lesson_title, DOWN, buff=0.35)
        block_heading.align_to([TEXT_LEFT_X, 0, 0], LEFT)
        self.play(Write(block_heading), run_time=MOTION_ENTER)

        col = TheoryColumn(block_heading, has_figure=False)

        line1 = tex_wrapped(r"Với hai biểu thức $A$, $B$ tùy ý, ta có:")
        col.place(line1, gap=FORMULA_GAP)

        formula_main = MathTex(
            r"(A + B)^2 = A^2 + 2AB + B^2",
            font_size=38,
        )
        col.place_formula_left(formula_main, indent=FORMULA_INDENT, gap=FORMULA_GAP)

        with self.voiceover(
            text=(
                "Tính chất. Bình phương của một tổng. "
                "Với hai biểu thức A và B bất kỳ, "
                "bình phương của tổng A cộng B "
                "bằng A bình phương cộng hai lần A nhân B, cộng B bình phương."
            )
        ) as ov:
            self.play(FadeIn(line1), run_time=ov.duration * 0.25)
            self.play(Write(formula_main), run_time=ov.duration * 0.55)
            self.play(
                Indicate(
                    formula_main,
                    scale_factor=EMPHASIS_SCALE,
                    color=EMPHASIS_COLOR,
                ),
                run_time=ov.duration * 0.20,
            )

        with self.voiceover(
            text="Đây là một trong những hằng đẳng thức đáng nhớ quan trọng nhất."
        ) as ov:
            box = SurroundingRectangle(formula_main, color=COLOR_RESULT_KEY, buff=0.18)
            self.play(Create(box), run_time=ov.duration)

        self.wait(1.0)
        self.play(
            FadeOut(block_heading),
            FadeOut(col.all),
            FadeOut(box),
            run_time=MOTION_EXIT,
        )

    # ── Scene 03 — 2.1 Bình phương của một hiệu ──────────────────────────────

    def scene03_binhPhuongHieu(self):
        block_heading = Tex(
            r"\textbf{2.1. Bình phương của một hiệu}",
            tex_template=viet_tex_template,
            font_size=32,
        )
        block_heading.next_to(self.lesson_title, DOWN, buff=0.35)
        block_heading.align_to([TEXT_LEFT_X, 0, 0], LEFT)
        self.play(Write(block_heading), run_time=MOTION_ENTER)

        col = TheoryColumn(block_heading, has_figure=False)

        line1 = tex_wrapped(r"Với hai biểu thức $A$, $B$ tùy ý, ta có:")
        col.place(line1, gap=FORMULA_GAP)

        formula_main = MathTex(
            r"(A - B)^2 = A^2 - 2AB + B^2",
            font_size=38,
        )
        col.place_formula_left(formula_main, indent=FORMULA_INDENT, gap=FORMULA_GAP)

        with self.voiceover(
            text=(
                "Bình phương của một hiệu. "
                "Với hai biểu thức A và B bất kỳ, "
                "bình phương của hiệu A trừ B "
                "bằng A bình phương trừ hai lần A nhân B, cộng B bình phương."
            )
        ) as ov:
            self.play(FadeIn(line1), run_time=ov.duration * 0.25)
            self.play(Write(formula_main), run_time=ov.duration * 0.55)
            self.play(
                Indicate(
                    formula_main,
                    scale_factor=EMPHASIS_SCALE,
                    color=EMPHASIS_COLOR,
                ),
                run_time=ov.duration * 0.20,
            )

        with self.voiceover(
            text=(
                "Lưu ý dấu âm ở hạng tử giữa "
                "là điểm khác biệt so với bình phương của tổng."
            )
        ) as ov:
            self.play(
                Indicate(
                    formula_main,
                    scale_factor=EMPHASIS_SCALE,
                    color=COLOR_EQUAL_1,
                ),
                run_time=ov.duration,
            )

        self.wait(1.0)
        self.play(
            FadeOut(block_heading),
            FadeOut(col.all),
            run_time=MOTION_EXIT,
        )

    # ── Scene 04 — Ví dụ bình phương tổng và hiệu ────────────────────────────

    def scene04_viDu21(self):
        block_heading = Tex(
            r"\textbf{Ví dụ}",
            tex_template=viet_tex_template,
            font_size=32,
        )
        block_heading.next_to(self.lesson_title, DOWN, buff=0.35)
        block_heading.align_to([TEXT_LEFT_X, 0, 0], LEFT)
        self.play(Write(block_heading), run_time=MOTION_ENTER)

        col = TheoryColumn(block_heading, has_figure=False)

        ex1 = MathTex(
            r"\bullet \ (x + 2)^2 = x^2 + 2 \cdot x \cdot 2 + 2^2 = x^2 + 4x + 4",
            font_size=27,
        )
        col.place_formula_left(ex1, indent=0.4, gap=0.24)

        ex2 = MathTex(
            r"\bullet \ (x - 2)^2 = x^2 - 2 \cdot x \cdot 2 + 2^2 = x^2 - 4x + 4",
            font_size=27,
        )
        col.place_formula_left(ex2, indent=0.4, gap=0.24)

        with self.voiceover(
            text=(
                "Ví dụ. Áp dụng hằng đẳng thức bình phương của một tổng: "
                "x cộng hai, tất cả bình phương, "
                "bằng x bình phương cộng bốn x cộng bốn."
            )
        ) as ov:
            self.play(Write(ex1), run_time=ov.duration * 0.75)
            self.play(
                Indicate(ex1, scale_factor=EMPHASIS_SCALE, color=COLOR_EQUAL_1),
                run_time=ov.duration * 0.25,
            )

        with self.voiceover(
            text=(
                "Áp dụng hằng đẳng thức bình phương của một hiệu: "
                "x trừ hai, tất cả bình phương, "
                "bằng x bình phương trừ bốn x cộng bốn."
            )
        ) as ov:
            self.play(Write(ex2), run_time=ov.duration * 0.75)
            self.play(
                Indicate(ex2, scale_factor=EMPHASIS_SCALE, color=COLOR_EQUAL_2),
                run_time=ov.duration * 0.25,
            )

        self.wait(1.0)
        self.play(
            FadeOut(block_heading),
            FadeOut(col.all),
            run_time=MOTION_EXIT,
        )

    # ── Scene 05 — 2.2 Hiệu hai bình phương ──────────────────────────────────

    def scene05_hieuHaiBinhPhuong(self):
        block_heading = Tex(
            r"\textbf{2.2. Hiệu hai bình phương}",
            tex_template=viet_tex_template,
            font_size=32,
        )
        block_heading.next_to(self.lesson_title, DOWN, buff=0.35)
        block_heading.align_to([TEXT_LEFT_X, 0, 0], LEFT)
        self.play(Write(block_heading), run_time=MOTION_ENTER)

        col = TheoryColumn(block_heading, has_figure=False)

        line1 = tex_wrapped(r"Với hai biểu thức $A$, $B$ tùy ý, ta có:")
        col.place(line1, gap=FORMULA_GAP)

        formula_main = MathTex(
            r"A^2 - B^2 = (A - B)(A + B)",
            font_size=38,
        )
        col.place_formula_left(formula_main, indent=FORMULA_INDENT, gap=FORMULA_GAP)

        with self.voiceover(
            text=(
                "Tính chất. Hiệu hai bình phương. "
                "Với hai biểu thức A và B bất kỳ, "
                "A bình phương trừ B bình phương "
                "bằng tích của A trừ B và A cộng B."
            )
        ) as ov:
            self.play(FadeIn(line1), run_time=ov.duration * 0.25)
            self.play(Write(formula_main), run_time=ov.duration * 0.55)
            self.play(
                Indicate(
                    formula_main,
                    scale_factor=EMPHASIS_SCALE,
                    color=EMPHASIS_COLOR,
                ),
                run_time=ov.duration * 0.20,
            )

        with self.voiceover(
            text="Đây là hằng đẳng thức giúp phân tích nhân tử rất hiệu quả."
        ) as ov:
            box = SurroundingRectangle(formula_main, color=COLOR_RESULT_KEY, buff=0.18)
            self.play(Create(box), run_time=ov.duration * 0.60)
            self.play(
                Indicate(
                    formula_main,
                    scale_factor=EMPHASIS_SCALE,
                    color=COLOR_EQUAL_1,
                ),
                run_time=ov.duration * 0.40,
            )

        self.wait(1.5)
        self.play(
            FadeOut(block_heading),
            FadeOut(col.all),
            FadeOut(box),
            FadeOut(self.lesson_title),
            run_time=MOTION_EXIT,
        )
