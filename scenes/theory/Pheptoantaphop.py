"""CHUYÊN ĐỀ 2. PHÉP TOÁN TRONG TẬP HỢP CÁC SỐ TỰ NHIÊN — video lý thuyết.

Spec: specs/theory/phep_toan_tap_hop/spec-ly-thuyet.md
Subject: algebra   |   Scenes: 6   |   ~7–9 phút
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
    COLOR_WARNING,
    MOTION_ENTER,
    MOTION_EXIT,
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

LESSON_TITLE_TEX = (
    r"\textbf{CHUYÊN ĐỀ 2. PHÉP TOÁN TRONG TẬP HỢP CÁC SỐ TỰ NHIÊN}"
)
SECTION_HEADING_TEX = r"\textbf{I. KIẾN THỨC CẦN NHỚ}"

# ---------------------------------------------------------------------------
# Layout constants — theo spec-ly-thuyet.md
# ---------------------------------------------------------------------------

WRAP_WIDTH_CM  = 14
BODY_GAP       = 0.16
FORMULA_GAP    = 0.25
FORMULA_INDENT = 0.8


def tex_wrapped(
    text: str,
    width_cm: float = WRAP_WIDTH_CM,
    font_size: int = 28,
    color=COLOR_DEFAULT,
) -> Tex:
    """Wrap text trong minipage raggedright để tránh LaTeX tự ngắt dòng."""
    body = (
        rf"\begin{{minipage}}{{{width_cm}cm}}"
        rf"\raggedright {text}\end{{minipage}}"
    )
    return Tex(body, tex_template=viet_tex_template, font_size=font_size, color=color)


# ---------------------------------------------------------------------------
# Scene class
# ---------------------------------------------------------------------------

class PhepToanTapHop(VoiceoverScene):
    """Bài giảng lý thuyết: Phép toán trong tập hợp các số tự nhiên."""

    def construct(self):
        self.set_speech_service(make_gtts_service())
        self.setup_scene_style()
        self.scene00_intro()
        self.scene01_tinhChatCongNhan()
        self.scene02_dieuKienTru()
        self.scene03_chiaHet()
        self.scene04_chiaCoDu()
        self.scene05_nhanXet()

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

    def _ensure_lesson_title(self):
        if not hasattr(self, "lesson_title"):
            self.lesson_title = make_lesson_title(LESSON_TITLE_TEX, viet_tex_template)
            self.add(self.lesson_title)

    def _ensure_section_heading(self):
        if not hasattr(self, "section_heading"):
            self._ensure_lesson_title()
            self.section_heading = Tex(
                SECTION_HEADING_TEX,
                tex_template=viet_tex_template,
                font_size=28,
            )
            self.section_heading.next_to(self.lesson_title, DOWN, buff=0.35)
            self.section_heading.align_to([TEXT_LEFT_X, 0, 0], LEFT)
            self.add(self.section_heading)

    def _heading_anchor(self):
        """Neo block_heading: dưới section_heading nếu có, else lesson_title."""
        if hasattr(self, "section_heading"):
            return self.section_heading
        return self.lesson_title

    def _block_heading(self, text: str, *, color=COLOR_DEFAULT) -> Tex:
        self._ensure_lesson_title()
        self._ensure_section_heading()
        heading = Tex(
            text,
            tex_template=viet_tex_template,
            font_size=32,
            color=color,
        )
        heading.next_to(self._heading_anchor(), DOWN, buff=0.25)
        heading.align_to([TEXT_LEFT_X, 0, 0], LEFT)
        return heading

    # ── Scene 00 — Intro ──────────────────────────────────────────────────────

    def scene00_intro(self):
        self.lesson_title = make_lesson_title(LESSON_TITLE_TEX, viet_tex_template)
        self.section_heading = Tex(
            SECTION_HEADING_TEX,
            tex_template=viet_tex_template,
            font_size=28,
        )
        self.section_heading.next_to(self.lesson_title, DOWN, buff=0.35)
        self.section_heading.align_to([TEXT_LEFT_X, 0, 0], LEFT)

        with self.voiceover(
            text=(
                "Phép toán trong tập hợp các số tự nhiên. "
                "Phần một. Kiến thức cần nhớ."
            )
        ) as ov:
            self.play(FadeIn(self.lesson_title), run_time=ov.duration * 0.45)
            self.play(FadeIn(self.section_heading), run_time=ov.duration * 0.40)
            self.wait(ov.duration * 0.15)

        self.wait(1.5)

    # ── Scene 01 — Tính chất cộng và nhân ─────────────────────────────────────

    def scene01_tinhChatCongNhan(self):
        block_heading = self._block_heading(
            r"\textbf{1. Các tính chất cơ bản của phép cộng và phép nhân}"
        )
        self.play(Write(block_heading), run_time=MOTION_ENTER)

        col = TheoryColumn(block_heading, has_figure=False)
        fs = 27
        fg = 0.22

        label_giao_hoan = Tex(
            r"- \textbf{Tính chất giao hoán:}",
            tex_template=viet_tex_template,
            font_size=fs,
        )
        formula_gh_cong = Tex(r"$\bullet$ $a + b = b + a$",
                              tex_template=viet_tex_template, font_size=fs + 1)
        formula_gh_nhan = Tex(r"$\bullet$ $a \cdot b = b \cdot a$",
                              tex_template=viet_tex_template, font_size=fs + 1)

        label_ket_hop = Tex(
            r"- \textbf{Tính chất kết hợp:}",
            tex_template=viet_tex_template,
            font_size=fs,
        )
        formula_kh_cong = Tex(r"$\bullet$ $(a + b) + c = a + (b + c)$",
                              tex_template=viet_tex_template, font_size=fs + 1)
        formula_kh_nhan = Tex(r"$\bullet$ $(a \cdot b) \cdot c = a \cdot (b \cdot c)$",
                              tex_template=viet_tex_template, font_size=fs + 1)

        label_cong_0 = Tex(
            r"- \textbf{Cộng với không:}",
            tex_template=viet_tex_template,
            font_size=fs,
        )
        formula_cong_0 = Tex(r"$\bullet$ $a + 0 = 0 + a = a$",
                             tex_template=viet_tex_template, font_size=fs + 1)

        label_nhan_1 = Tex(
            r"- \textbf{Nhân với một:}",
            tex_template=viet_tex_template,
            font_size=fs,
        )
        formula_nhan_1 = Tex(r"$\bullet$ $a \cdot 1 = 1 \cdot a = a$",
                             tex_template=viet_tex_template, font_size=fs + 1)

        label_phan_phoi = Tex(
            r"- \textbf{Tính chất phân phối:}",
            tex_template=viet_tex_template,
            font_size=fs,
        )
        formula_phan_phoi = Tex(
            r"$\bullet$ $a \cdot (b + c) = a \cdot b + a \cdot c$",
            tex_template=viet_tex_template,
            font_size=fs + 1,
        )

        col.place(label_giao_hoan, gap=BODY_GAP)
        col.place_formula_left(formula_gh_cong, indent=FORMULA_INDENT, gap=fg)
        col.place_formula_left(formula_gh_nhan, indent=FORMULA_INDENT, gap=BODY_GAP)

        col.place(label_ket_hop, gap=BODY_GAP)
        col.place_formula_left(formula_kh_cong, indent=FORMULA_INDENT, gap=fg)
        col.place_formula_left(formula_kh_nhan, indent=FORMULA_INDENT, gap=BODY_GAP)

        col.place(label_cong_0, gap=BODY_GAP)
        col.place_formula_left(formula_cong_0, indent=FORMULA_INDENT, gap=BODY_GAP)

        col.place(label_nhan_1, gap=BODY_GAP)
        col.place_formula_left(formula_nhan_1, indent=FORMULA_INDENT, gap=BODY_GAP)

        col.place(label_phan_phoi, gap=BODY_GAP)
        col.place_formula_left(formula_phan_phoi, indent=FORMULA_INDENT, gap=BODY_GAP)

        # terms_bold_mobs = VGroup(label_giao_hoan, label_ket_hop, label_phan_phoi)

        with self.voiceover(
            text=(
                "Tính chất. "
                "Tính chất giao hoán: a cộng b bằng b cộng a; "
                "a nhân b bằng b nhân a."
            )
        ) as ov:
            self.play(FadeIn(label_giao_hoan), run_time=ov.duration * 0.25)
            self.play(
                Write(formula_gh_cong),
                Write(formula_gh_nhan),
                run_time=ov.duration * 0.55,
            )
            self.play(
                Indicate(
                    VGroup(label_giao_hoan, formula_gh_cong, formula_gh_nhan),
                    scale_factor=EMPHASIS_SCALE,
                    color=EMPHASIS_COLOR,
                ),
                run_time=ov.duration * 0.20,
            )

        with self.voiceover(
            text=(
                "Tính chất kết hợp: a cộng b, cộng c bằng a cộng b cộng c; "
                "a nhân b, nhân c bằng a nhân b nhân c."
            )
        ) as ov:
            self.play(FadeIn(label_ket_hop), run_time=ov.duration * 0.20)
            self.play(
                Write(formula_kh_cong),
                Write(formula_kh_nhan),
                run_time=ov.duration * 0.55,
            )
            self.play(
                Indicate(
                    VGroup(label_ket_hop, formula_kh_cong, formula_kh_nhan),
                    scale_factor=EMPHASIS_SCALE,
                    color=EMPHASIS_COLOR,
                ),
                run_time=ov.duration * 0.25,
            )

        with self.voiceover(
            text=(
                "Cộng với không: a cộng không bằng không cộng a bằng a. "
                "Nhân với một: a nhân một bằng một nhân a bằng a."
            )
        ) as ov:
            self.play(FadeIn(label_cong_0), run_time=ov.duration * 0.15)
            self.play(Write(formula_cong_0), run_time=ov.duration * 0.35)
            self.play(FadeIn(label_nhan_1), run_time=ov.duration * 0.15)
            self.play(Write(formula_nhan_1), run_time=ov.duration * 0.35)

        with self.voiceover(
            text=(
                "Tính chất phân phối: a nhân tổng b cộng c "
                "bằng a nhân b cộng a nhân c."
            )
        ) as ov:
            self.play(FadeIn(label_phan_phoi), run_time=ov.duration * 0.25)
            self.play(Write(formula_phan_phoi), run_time=ov.duration * 0.55)
            self.play(
                Indicate(
                    VGroup(label_phan_phoi, formula_phan_phoi),
                    scale_factor=EMPHASIS_SCALE,
                    color=EMPHASIS_COLOR,
                ),
                run_time=ov.duration * 0.20,
            )

        # self.play(
        #     Indicate(terms_bold_mobs, scale_factor=EMPHASIS_SCALE, color=EMPHASIS_COLOR),
        #     run_time=EMPHASIS_INDICATE_TIME,
        # )

        self.wait(1.0)
        self.play(
            FadeOut(block_heading),
            FadeOut(col.all),
            run_time=MOTION_EXIT,
        )

    # ── Scene 02 — Điều kiện phép trừ ─────────────────────────────────────────

    def scene02_dieuKienTru(self):
        block_heading = self._block_heading(
            r"\textbf{2. Điều kiện để thực hiện phép trừ $a - b$ là $a \geq b$}"
        )
        self.play(Write(block_heading), run_time=MOTION_ENTER)

        col = TheoryColumn(block_heading, has_figure=False)

        line1 = tex_wrapped(
            r"- Điều kiện để thực hiện phép trừ $a - b$ là $a \geq b$."
        )
        formula_dieu_kien = Tex(r"$\bullet$ $a \geq b$",
                                tex_template=viet_tex_template, font_size=32)

        line2 = tex_wrapped(
            r"- Tính chất phân phối của phép nhân đối với phép trừ:"
        )
        formula_phan_phoi_tru = Tex(
            r"$\bullet$ $a \cdot (b - c) = a \cdot b - a \cdot c$",
            tex_template=viet_tex_template,
            font_size=30,
        )

        col.place(line1, gap=BODY_GAP)
        col.place_formula_left(formula_dieu_kien, indent=FORMULA_INDENT, gap=FORMULA_GAP)
        col.place(line2, gap=BODY_GAP)
        col.place_formula_left(formula_phan_phoi_tru, indent=FORMULA_INDENT, gap=FORMULA_GAP)

        with self.voiceover(
            text=(
                "Định nghĩa. "
                "Để thực hiện phép trừ a trừ b trong tập số tự nhiên, "
                "a phải lớn hơn hoặc bằng b."
            )
        ) as ov:
            self.play(FadeIn(line1), run_time=ov.duration * 0.35)
            self.play(Write(formula_dieu_kien), run_time=ov.duration * 0.45)
            self.play(
                Indicate(formula_dieu_kien, scale_factor=EMPHASIS_SCALE, color=EMPHASIS_COLOR),
                run_time=ov.duration * 0.20,
            )

        with self.voiceover(
            text=(
                "Phép nhân còn phân phối đối với phép trừ: "
                "a nhân hiệu b trừ c bằng a nhân b trừ a nhân c."
            )
        ) as ov:
            self.play(FadeIn(line2), run_time=ov.duration * 0.30)
            self.play(Write(formula_phan_phoi_tru), run_time=ov.duration * 0.70)

        self.wait(1.0)
        self.play(
            FadeOut(block_heading),
            FadeOut(col.all),
            run_time=MOTION_EXIT,
        )

    # ── Scene 03 — Chia hết ───────────────────────────────────────────────────

    def scene03_chiaHet(self):
        block_heading = self._block_heading(
            r"\textbf{3. Điều kiện để số $a$ chia hết cho số $b \neq 0$}"
        )
        self.play(Write(block_heading), run_time=MOTION_ENTER)

        col = TheoryColumn(block_heading, has_figure=False)

        line1 = tex_wrapped(
            r"- Số $a$ \textbf{chia hết} cho số $b \neq 0$ khi tồn tại số $q$ sao cho:"
        )
        formula_chia_het = Tex(r"$\bullet$ $a = b \cdot q$",
                               tex_template=viet_tex_template, font_size=34)

        col.place(line1, gap=BODY_GAP)
        col.place_formula_left(formula_chia_het, indent=FORMULA_INDENT, gap=FORMULA_GAP)

        with self.voiceover(
            text=(
                "Định nghĩa. "
                "Số a chia hết cho số b khác không "
                "khi tồn tại số q sao cho a bằng b nhân q."
            )
        ) as ov:
            self.play(FadeIn(line1), run_time=ov.duration * 0.45)
            self.play(Write(formula_chia_het), run_time=ov.duration * 0.55)

        self.play(
            Indicate(line1, scale_factor=EMPHASIS_SCALE, color=EMPHASIS_COLOR),
            run_time=EMPHASIS_INDICATE_TIME,
        )

        self.wait(1.0)
        self.play(
            FadeOut(block_heading),
            FadeOut(col.all),
            run_time=MOTION_EXIT,
        )

    # ── Scene 04 — Phép chia có dư ──────────────────────────────────────────

    def scene04_chiaCoDu(self):
        block_heading = self._block_heading(r"\textbf{4. Phép chia có dư}")
        self.play(Write(block_heading), run_time=MOTION_ENTER)

        col = TheoryColumn(block_heading, has_figure=False)

        line1 = tex_wrapped(r"- Chia số $a$ cho số $b \neq 0$ ta được:")
        formula_chia_du = Tex(r"$\bullet$ $a = b \cdot q + r$",
                              tex_template=viet_tex_template, font_size=34)
        formula_dieu_kien_r = Tex(r"$\bullet$ $0 \leq r < b$",
                                  tex_template=viet_tex_template, font_size=32)

        col.place(line1, gap=BODY_GAP)
        col.place_formula_left(formula_chia_du, indent=FORMULA_INDENT, gap=0.28)
        col.place_formula_left(formula_dieu_kien_r, indent=FORMULA_INDENT, gap=FORMULA_GAP)

        with self.voiceover(
            text=(
                "Định lí. "
                "Khi chia số a cho số b khác không, "
                "ta được a bằng b nhân q cộng r, "
                "với r lớn hơn hoặc bằng không và nhỏ hơn b."
            )
        ) as ov:
            self.play(FadeIn(line1), run_time=ov.duration * 0.20)
            self.play(Write(formula_chia_du), run_time=ov.duration * 0.40)
            self.play(Write(formula_dieu_kien_r), run_time=ov.duration * 0.25)
            self.play(
                Indicate(formula_dieu_kien_r, scale_factor=EMPHASIS_SCALE, color=EMPHASIS_COLOR),
                run_time=ov.duration * 0.15,
            )

        self.wait(1.0)
        self.play(
            FadeOut(block_heading),
            FadeOut(col.all),
            run_time=MOTION_EXIT,
        )

    # ── Scene 05 — Nhận xét ───────────────────────────────────────────────────

    def scene05_nhanXet(self):
        block_heading = self._block_heading(
            r"\textbf{(*) Nhận xét}",
            color=COLOR_WARNING,
        )
        self.play(Write(block_heading), run_time=MOTION_ENTER)

        col = TheoryColumn(block_heading, has_figure=False)
        bullet_fs = 26
        bullet_gap = 0.18

        bullet1 = Tex(
            r"\textit{- $r \in \{0;\,1;\,2;\,\ldots;\,b-1\}$, "
            r"nên khi chia một số cho $b$ thì số dư có $b$ khả năng.}",
            tex_template=viet_tex_template,
            font_size=bullet_fs,
            color=COLOR_WARNING,
        )
        bullet2 = Tex(
            r"\textit{- $(a - r) \vdots b$.}",
            tex_template=viet_tex_template,
            font_size=bullet_fs,
            color=COLOR_WARNING,
        )
        bullet3 = Tex(
            r"\textit{- Nếu $a \vdots c$ và $b \vdots c$ "
            r"thì $(a \pm b) : c = a : c \pm b : c$.}",
            tex_template=viet_tex_template,
            font_size=bullet_fs,
            color=COLOR_WARNING,
        )
        bullet4 = Tex(
            r"\textit{- Nếu $a \vdots b$ và $b \vdots c$ "
            r"thì $a \vdots c$ (tính chất bắc cầu).}",
            tex_template=viet_tex_template,
            font_size=bullet_fs,
            color=COLOR_WARNING,
        )

        col.place_bullet(bullet1, gap=bullet_gap)
        col.place_bullet(bullet2, gap=bullet_gap)
        col.place_bullet(bullet3, gap=bullet_gap)
        col.place_bullet(bullet4, gap=bullet_gap)

        with self.voiceover(
            text=(
                "Nhận xét. "
                "Số dư r thuộc tập từ không đến b trừ một, "
                "nên khi chia một số cho b thì số dư có b khả năng."
            )
        ) as ov:
            self.play(FadeIn(bullet1), run_time=ov.duration * 0.70)
            self.play(
                Indicate(bullet1, scale_factor=EMPHASIS_SCALE, color=COLOR_WARNING),
                run_time=ov.duration * 0.30,
            )

        with self.voiceover(text="Hiệu a trừ r chia hết cho b.") as ov:
            self.play(FadeIn(bullet2), run_time=ov.duration * 0.65)
            self.play(
                Indicate(bullet2, scale_factor=EMPHASIS_SCALE, color=COLOR_WARNING),
                run_time=ov.duration * 0.35,
            )

        with self.voiceover(
            text=(
                "Nếu a chia hết cho c và b chia hết cho c "
                "thì a cộng b hoặc a trừ b cũng chia hết cho c."
            )
        ) as ov:
            self.play(FadeIn(bullet3), run_time=ov.duration * 0.65)
            self.play(
                Indicate(bullet3, scale_factor=EMPHASIS_SCALE, color=COLOR_WARNING),
                run_time=ov.duration * 0.35,
            )

        with self.voiceover(
            text=(
                "Nếu a chia hết cho b và b chia hết cho c "
                "thì a chia hết cho c — đây là tính chất bắc cầu."
            )
        ) as ov:
            self.play(FadeIn(bullet4), run_time=ov.duration * 0.65)
            self.play(
                Indicate(bullet4, scale_factor=EMPHASIS_SCALE, color=COLOR_WARNING),
                run_time=ov.duration * 0.35,
            )

        self.wait(1.5)
        self.play(
            FadeOut(block_heading),
            FadeOut(col.all),
            FadeOut(self.section_heading),
            FadeOut(self.lesson_title),
            run_time=MOTION_EXIT,
        )
