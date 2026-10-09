"""HỆ THỨC VI-ÉT — video lý thuyết (spec: specs/theory/vi-et/spec-ly-thuyet.md)."""

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
    MOTION_ENTER,
    MOTION_EXIT,
    MOTION_TITLE_OUT,
    EMPHASIS_SCALE,
    EMPHASIS_COLOR,
    TheoryColumn,
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

TEXT_ONLY_FONT = 28
WRAP_WIDTH_CM = 16
BODY_GAP = 0.16
FORMULA_GAP = 0.25


def tex_wrapped(text: str, width_cm: float = WRAP_WIDTH_CM, font_size: int = TEXT_ONLY_FONT) -> Tex:
    body = (
        rf"\begin{{minipage}}{{{width_cm}cm}}"
        rf"\raggedright {text}\end{{minipage}}"
    )
    return Tex(body, tex_template=viet_tex_template, font_size=font_size)


class HeThucViet(VoiceoverScene):
    """Bài giảng lý thuyết: Hệ thức Vi-ét."""

    def construct(self):
        self.set_speech_service(make_gtts_service())
        self.setup_scene_style()
        self.scene00_intro()
        self.scene01_heThucViet()
        self.scene02_ungDungViet()

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
            r"\textbf{HỆ THỨC VI-ÉT}",
            tex_template=viet_tex_template,
            font_size=36,
        )
        self.lesson_title.to_edge(UP, buff=0.4)

        section_heading = Tex(
            r"\textbf{1. CÁC KIẾN THỨC CẦN NHỚ}",
            tex_template=viet_tex_template,
            font_size=28,
        )
        section_heading.next_to(self.lesson_title, DOWN, buff=0.35)

        with self.voiceover(
            text="Hệ thức Vi-ét. Phần một. Các kiến thức cần nhớ."
        ) as ov:
            self.play(Write(self.lesson_title), run_time=ov.duration * 0.55)
            self.play(FadeIn(section_heading), run_time=ov.duration * 0.45)

        self.wait(1.5)
        self.play(FadeOut(section_heading), run_time=MOTION_TITLE_OUT)

    # ------------------------------------------------------------------
    # Scene 01 — Hệ thức Vi-ét
    # ------------------------------------------------------------------

    def scene01_heThucViet(self):
        if not hasattr(self, "lesson_title"):
            self.lesson_title = Tex(
                r"\textbf{HỆ THỨC VI-ÉT}",
                tex_template=viet_tex_template,
                font_size=36,
            ).to_edge(UP, buff=0.4)
            self.add(self.lesson_title)

        block_heading = Tex(
            r"\textbf{Hệ thức Vi-ét}",
            tex_template=viet_tex_template,
            font_size=32,
        )
        block_heading.to_corner(UL, buff=0.5)
        self.play(Write(block_heading), run_time=MOTION_ENTER)

        col = TheoryColumn(block_heading, has_figure=False)

        line1 = tex_wrapped(
            r"Cho phương trình bậc hai $ax^2 + bx + c = 0$ với $a \neq 0$."
        )
        line2 = tex_wrapped(
            r"Nếu $x_1, x_2$ là hai nghiệm của phương trình thì:"
        )
        col.place(line1, gap=BODY_GAP)
        col.place(line2, gap=BODY_GAP)

        formula_viet = MathTex(
            r"\begin{cases} x_1 + x_2 = \dfrac{-b}{a} \\[6pt]"
            r"x_1 \cdot x_2 = \dfrac{c}{a} \end{cases}",
            tex_template=viet_tex_template,
            font_size=32,
        )
        col.place_formula_left(formula_viet, indent=0.8, gap=FORMULA_GAP)

        example_intro = tex_wrapped(
            r"Ví dụ: Phương trình $2x^2 - 5x + 2 = 0$ có $\Delta = 9 > 0$ "
            r"nên phương trình có hai nghiệm $x_1, x_2$."
        )
        col.place(example_intro, gap=BODY_GAP)

        example_label = tex_wrapped(r"Theo hệ thức Vi-ét ta có:")
        col.place(example_label, gap=0.15)

        formula_example = MathTex(
            r"\begin{cases} x_1 + x_2 = \dfrac{5}{2} \\[6pt]"
            r"x_1 \cdot x_2 = \dfrac{2}{2} = 1 \end{cases}",
            tex_template=viet_tex_template,
            font_size=32,
        )
        col.place_formula_left(formula_example, indent=0.8, gap=FORMULA_GAP)

        with self.voiceover(
            text=(
                "Hệ thức Vi-ét. "
                "Cho phương trình bậc hai a x bình cộng b x cộng c bằng không, "
                "với a khác không."
            )
        ) as ov:
            self.play(FadeIn(line1), run_time=ov.duration)

        with self.voiceover(
            text=(
                "Nếu x một và x hai là hai nghiệm của phương trình thì "
                "tổng hai nghiệm bằng trừ b chia a, "
                "và tích hai nghiệm bằng c chia a."
            )
        ) as ov:
            self.play(FadeIn(line2), run_time=ov.duration * 0.35)
            self.play(Write(formula_viet), run_time=ov.duration * 0.40)
            self.play(
                Indicate(formula_viet, scale_factor=EMPHASIS_SCALE, color=EMPHASIS_COLOR),
                run_time=ov.duration * 0.25,
            )

        with self.voiceover(
            text=(
                "Ví dụ, phương trình hai x bình trừ năm x cộng hai bằng không "
                "có delta bằng chín, lớn hơn không, "
                "nên phương trình có hai nghiệm x một và x hai."
            )
        ) as ov:
            self.play(FadeIn(example_intro), run_time=ov.duration)

        with self.voiceover(
            text=(
                "Theo hệ thức Vi-ét, tổng hai nghiệm bằng năm phần hai, "
                "tích hai nghiệm bằng hai phần hai, tức bằng một."
            )
        ) as ov:
            self.play(
                FadeIn(example_label),
                Write(formula_example),
                run_time=ov.duration * 0.65,
            )
            self.play(
                Indicate(formula_example, scale_factor=EMPHASIS_SCALE, color=EMPHASIS_COLOR),
                run_time=ov.duration * 0.35,
            )

        self.wait(1.0)
        self.play(
            FadeOut(block_heading),
            FadeOut(col.all),
            run_time=MOTION_EXIT,
        )

    # ------------------------------------------------------------------
    # Scene 02 — Ứng dụng của hệ thức Vi-ét
    # ------------------------------------------------------------------

    def scene02_ungDungViet(self):
        block_heading = Tex(
            r"\textbf{Ứng dụng của hệ thức Vi-ét}",
            tex_template=viet_tex_template,
            font_size=32,
        )
        block_heading.to_corner(UL, buff=0.5)
        self.play(Write(block_heading), run_time=MOTION_ENTER)

        col = TheoryColumn(block_heading, has_figure=False)

        line_a = tex_wrapped(
            r"\textbf{a)} Xét phương trình bậc hai: $ax^2 + bx + c = 0$ với $a \neq 0$."
        )
        line_b1 = tex_wrapped(
            r"Nếu phương trình có $a + b + c = 0$ thì phương trình có một nghiệm là "
            r"$x_1 = 1$, nghiệm kia là $x_2 = \dfrac{c}{a}$."
        )
        line_b2 = tex_wrapped(
            r"Nếu phương trình có $a - b + c = 0$ thì phương trình có một nghiệm là "
            r"$x_1 = -1$, nghiệm kia là $x_2 = -\dfrac{c}{a}$."
        )
        line_c = tex_wrapped(
            r"\textbf{b)} Tìm hai số biết tổng và tích của chúng:"
        )
        line_c2 = tex_wrapped(
            r"Nếu hai số có tổng bằng $S$ và tích bằng $P$ thì hai số đó là hai nghiệm "
            r"của phương trình"
        )
        col.place(line_a, gap=BODY_GAP)
        col.place(line_b1, gap=BODY_GAP)
        col.place(line_b2, gap=BODY_GAP)
        col.place(line_c, gap=BODY_GAP)
        col.place(line_c2, gap=BODY_GAP)

        formula_find = MathTex(
            r"X^2 - SX + P = 0 \quad (\text{ĐK: } S^2 \geq 4P)",
            tex_template=viet_tex_template,
            font_size=30,
        )
        col.place_formula_left(formula_find, indent=0.8, gap=FORMULA_GAP)

        with self.voiceover(
            text=(
                "Ứng dụng của hệ thức Vi-ét. "
                "Xét phương trình bậc hai a x bình cộng b x cộng c bằng không."
            )
        ) as ov:
            self.play(FadeIn(line_a), run_time=ov.duration)

        with self.voiceover(
            text=(
                "Nếu a cộng b cộng c bằng không "
                "thì phương trình có một nghiệm là x bằng một, "
                "nghiệm kia là c chia a. "
                "Chẳng hạn, x bình trừ ba x cộng hai bằng không "
                "có một cộng trừ ba cộng hai bằng không, "
                "nên x bằng một là nghiệm."
            )
        ) as ov:
            self.play(FadeIn(line_b1), run_time=ov.duration)

        with self.voiceover(
            text=(
                "Nếu a trừ b cộng c bằng không "
                "thì phương trình có một nghiệm là x bằng trừ một, "
                "nghiệm kia là trừ c chia a. "
                "Ví dụ, x bình cộng ba x cộng hai bằng không "
                "có một trừ ba cộng hai bằng không, "
                "nên x bằng trừ một là nghiệm."
            )
        ) as ov:
            self.play(FadeIn(line_b2), run_time=ov.duration)

        with self.voiceover(
            text=(
                "Một ứng dụng quan trọng khác: "
                "tìm hai số biết tổng và tích của chúng. "
                "Nếu hai số có tổng bằng S và tích bằng P "
                "thì hai số đó chính là hai nghiệm "
                "của phương trình X bình trừ S X cộng P bằng không, "
                "với điều kiện S bình lớn hơn hoặc bằng bốn P."
            )
        ) as ov:
            self.play(FadeIn(line_c), FadeIn(line_c2), run_time=ov.duration * 0.35)
            self.play(Write(formula_find), run_time=ov.duration * 0.35)
            self.play(
                Indicate(formula_find, scale_factor=EMPHASIS_SCALE, color=EMPHASIS_COLOR),
                run_time=ov.duration * 0.30,
            )

        self.wait(1.5)
        self.play(
            FadeOut(block_heading),
            FadeOut(col.all),
            FadeOut(self.lesson_title),
            run_time=MOTION_EXIT,
        )
