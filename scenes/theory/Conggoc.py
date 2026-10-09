"""CHUYÊN ĐỀ 2. CỘNG SỐ ĐO CÁC GÓC — video lý thuyết.

Spec: specs/theory/cong_goc/spec-ly-thuyet.md
Subject: geometry   |   Scenes: 7   |   ~8–10 phút
Hình SGK: 14 (tiên đề cộng góc), 15 (góc kề bù), 16 (so sánh góc).
"""

import sys
from pathlib import Path

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
    COLOR_EQUAL_3,
    COLOR_ACTIVE,
    COLOR_WARNING,
    STATE_DEFAULT,
    TIMING_FADE,
    MOTION_ENTER,
    MOTION_EXIT,
    EMPHASIS_SCALE,
    EMPHASIS_COLOR,
    EMPHASIS_INDICATE_TIME,
    LAYER_BACKGROUND,
    LAYER_GEOMETRY,
    LAYER_MARKERS,
    MARKER_DOT_RADIUS,
    AngleMarker,
    TheoryColumn,
    TEXT_LEFT_X,
    make_lesson_title,
    make_gtts_service,
    place_figure,
    FIG_MAX_W,
    FIG_MAX_H,
)

# ---------------------------------------------------------------------------
# TeX template
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

LESSON_TITLE_TEX = r"\textbf{CHUYÊN ĐỀ 2. CỘNG SỐ ĐO CÁC GÓC}"
SECTION_HEADING_TEX = r"\textbf{A. KIẾN THỨC CẦN NHỚ}"

# Hình 14–16 — từ spec
O_LOCAL = ORIGIN
RAY_LEN = 3.0
HALF_PLANE_OPACITY = 0.12
ANGLE_MARK_DIST = 0.85

FIG14_ANGLES = (0, 30, 75)   # Ox, Oy, Oz
FIG15_OY_DEG = 60
FIG16_ANGLES = (0, 45, 80)   # Ox, Oy, Oz

WRAP_WIDTH_CM = 14
BODY_GAP = 0.16
FORMULA_GAP = 0.25
FORMULA_INDENT = 0.8


def tex_wrapped(
    text: str,
    width_cm: float = WRAP_WIDTH_CM,
    font_size: int = 28,
    color=COLOR_DEFAULT,
) -> Tex:
    body = (
        rf"\begin{{minipage}}{{{width_cm}cm}}"
        rf"\raggedright {text}\end{{minipage}}"
    )
    return Tex(body, tex_template=viet_tex_template, font_size=font_size, color=color)


def _pt_ray(angle_deg: float, dist: float = RAY_LEN, origin=O_LOCAL) -> np.ndarray:
    th = angle_deg * DEGREES
    return origin + np.array([dist * np.cos(th), dist * np.sin(th), 0])


def _make_ray(
    angle_deg: float,
    length: float = RAY_LEN,
    origin=O_LOCAL,
    color=COLOR_DEFAULT,
) -> tuple[Arrow, np.ndarray]:
    end = _pt_ray(angle_deg, length, origin)
    ray = Arrow(
        origin,
        end,
        buff=0,
        max_tip_length_to_length_ratio=0.12,
        stroke_width=STATE_DEFAULT["stroke_width"],
        color=color,
    ).set_z_index(LAYER_GEOMETRY)
    return ray, end


def _label_math(name: str, pos: np.ndarray, direction) -> MathTex:
    lbl = MathTex(name, font_size=24)
    lbl.next_to(pos, direction, buff=0.15)
    return lbl.set_z_index(LAYER_MARKERS)


def _ray_label(name: str, angle_deg: float, dist: float = RAY_LEN * 0.88) -> MathTex:
    pos = _pt_ray(angle_deg, dist)
    th = angle_deg * DEGREES
    dx, dy = np.cos(th), np.sin(th)
    if dy > 0.35:
        direction = UR if dx >= 0 else UL
    elif dy < -0.35:
        direction = DR if dx >= 0 else DL
    else:
        direction = RIGHT if dx >= 0 else LEFT
    return _label_math(name, pos, direction)


def _half_plane_at_o(o: np.ndarray) -> Polygon:
    half_w = FIG_MAX_W * 0.55
    half_h = FIG_MAX_H * 0.45
    return Polygon(
        o + np.array([-half_w, 0, 0]),
        o + np.array([half_w, 0, 0]),
        o + np.array([half_w, half_h, 0]),
        o + np.array([-half_w, half_h, 0]),
        fill_color=COLOR_EQUAL_1,
        fill_opacity=HALF_PLANE_OPACITY,
        stroke_width=0,
    ).set_z_index(LAYER_BACKGROUND)


def _angle_between_degs(
    o: np.ndarray,
    deg_from: float,
    deg_to: float,
    *,
    radius: float = 0.45,
    color=COLOR_EQUAL_1,
    mark_dist: float = ANGLE_MARK_DIST,
) -> Sector:
    th1, th2 = deg_from * DEGREES, deg_to * DEGREES
    p1 = o + np.array([mark_dist * np.cos(th1), mark_dist * np.sin(th1), 0])
    p2 = o + np.array([mark_dist * np.cos(th2), mark_dist * np.sin(th2), 0])
    return AngleMarker(p1, o, p2, color=color, radius=radius)


def _angle_label_at(
    o: np.ndarray,
    deg_from: float,
    deg_to: float,
    text: str,
    *,
    radius: float = 0.65,
) -> MathTex:
    mid_deg = (deg_from + deg_to) / 2
    th = mid_deg * DEGREES
    pos = o + np.array([radius * np.cos(th), radius * np.sin(th), 0])
    lbl = MathTex(text, font_size=22)
    lbl.move_to(pos)
    return lbl.set_z_index(LAYER_MARKERS)


def _build_hinh14() -> dict:
    """Hình 14 — tiên đề cộng góc."""
    O = np.array(O_LOCAL, dtype=float)
    ox, oy, oz = FIG14_ANGLES
    ray_Ox, _ = _make_ray(ox)
    ray_Oy, _ = _make_ray(oy)
    ray_Oz, _ = _make_ray(oz)

    dot_O = Dot(O, radius=MARKER_DOT_RADIUS, color=COLOR_ACTIVE).set_z_index(LAYER_MARKERS)
    label_O = _label_math("O", O, DOWN)
    label_x = _ray_label("x", ox)
    label_y = _ray_label("y", oy)
    label_z = _ray_label("z", oz)

    figure_group = VGroup(ray_Ox, ray_Oy, ray_Oz, dot_O, label_O, label_x, label_y, label_z)
    place_figure(figure_group)

    return {
        "group": figure_group,
        "dot_O": dot_O,
        "ray_Ox": ray_Ox,
        "ray_Oy": ray_Oy,
        "ray_Oz": ray_Oz,
        "label_O": label_O,
        "label_x": label_x,
        "label_y": label_y,
        "label_z": label_z,
        "angles": FIG14_ANGLES,
    }


def _build_hinh15() -> dict:
    """Hình 15 — góc kề bù (đường thẳng xz + tia Oy)."""
    O = np.array(O_LOCAL, dtype=float)
    x_pos = O + LEFT * RAY_LEN
    z_pos = O + RIGHT * RAY_LEN
    line_xz = Line(
        x_pos,
        z_pos,
        color=COLOR_DEFAULT,
        stroke_width=STATE_DEFAULT["stroke_width"],
    ).set_z_index(LAYER_GEOMETRY)
    ray_Oy, _ = _make_ray(FIG15_OY_DEG)

    dot_O = Dot(O, radius=MARKER_DOT_RADIUS, color=COLOR_ACTIVE).set_z_index(LAYER_MARKERS)
    label_O = _label_math("O", O, DOWN)
    label_x = _label_math("x", x_pos, LEFT)
    label_z = _label_math("z", z_pos, RIGHT)
    label_y = _ray_label("y", FIG15_OY_DEG)

    figure_group = VGroup(line_xz, dot_O, ray_Oy, label_O, label_x, label_z, label_y)
    place_figure(figure_group)

    return {
        "group": figure_group,
        "dot_O": dot_O,
        "line_xz": line_xz,
        "ray_Oy": ray_Oy,
        "label_x": label_x,
        "label_z": label_z,
        "label_O": label_O,
        "label_y": label_y,
    }


def _build_hinh16() -> dict:
    """Hình 16 — so sánh góc trên nửa mặt phẳng."""
    O = np.array(O_LOCAL, dtype=float)
    ox, oy, oz = FIG16_ANGLES
    ray_Ox, _ = _make_ray(ox)
    ray_Oy, _ = _make_ray(oy)
    ray_Oz, _ = _make_ray(oz)

    dot_O = Dot(O, radius=MARKER_DOT_RADIUS, color=COLOR_ACTIVE).set_z_index(LAYER_MARKERS)
    label_O = _label_math("O", O, DOWN)
    label_x = _ray_label("x", ox)
    label_y = _ray_label("y", oy)
    label_z = _ray_label("z", oz)

    figure_group = VGroup(ray_Ox, ray_Oy, ray_Oz, dot_O, label_O, label_x, label_y, label_z)
    place_figure(figure_group)

    return {
        "group": figure_group,
        "dot_O": dot_O,
        "ray_Ox": ray_Ox,
        "ray_Oy": ray_Oy,
        "ray_Oz": ray_Oz,
        "label_O": label_O,
        "label_x": label_x,
        "label_y": label_y,
        "label_z": label_z,
        "angles": FIG16_ANGLES,
    }


class Conggoc(VoiceoverScene):
    """Video lý thuyết: Cộng số đo các góc."""

    def construct(self):
        self.set_speech_service(make_gtts_service())
        self.setup_scene_style()
        self.scene00_intro()
        self.scene01_soDoGoc()
        self.scene02_cacLoaiGoc()
        self.scene03_tienDeCongGoc()
        self.scene04_quanHeHaiGoc()
        self.scene05_dungGoc()
        self.scene06_soSanhGoc()

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
        if hasattr(self, "section_heading"):
            return self.section_heading
        return self.lesson_title

    def _block_heading(self, text: str, *, color=COLOR_DEFAULT) -> Tex:
        self._ensure_lesson_title()
        self._ensure_section_heading()
        heading = Tex(text, tex_template=viet_tex_template, font_size=32, color=color)
        heading.next_to(self._heading_anchor(), DOWN, buff=0.25)
        heading.align_to([TEXT_LEFT_X, 0, 0], LEFT)
        return heading

    def _o_center(self, dot_O: Dot) -> np.ndarray:
        return dot_O.get_center()

    # ── Scene 00 — Intro ───────────────────────────────────────────────────

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
                "Chuyên đề hai. Cộng số đo các góc. "
                "Phần A. Kiến thức cần nhớ. "
                "Bài học trình bày số đo góc, các loại góc, "
                "tiên đề cộng góc và quan hệ giữa hai góc. "
                "Ta cũng học cách dựng và so sánh góc "
                "trên nửa mặt phẳng."
            )
        ) as ov:
            self.play(FadeIn(self.lesson_title), run_time=ov.duration * 0.45)
            self.play(FadeIn(self.section_heading), run_time=ov.duration * 0.40)
            self.wait(ov.duration * 0.15)

        self.wait(1.5)

    # ── Scene 01 — Số đo góc ─────────────────────────────────────────────

    def scene01_soDoGoc(self):
        block_heading = self._block_heading(r"\textbf{1. Số đo góc}")
        self.play(Write(block_heading), run_time=MOTION_ENTER)

        col = TheoryColumn(block_heading, has_figure=False)

        line1 = tex_wrapped(r"- Mọi góc đều có số đo.")
        line2 = tex_wrapped(
            r"- Góc \textbf{bẹt} có số đo bằng $180^\circ$.",
            font_size=28,
        )
        line3 = tex_wrapped(
            r"- Không có góc nào có số đo lớn hơn $180^\circ$.",
            font_size=28,
        )
        col.place(line1, gap=BODY_GAP)
        col.place(line2, gap=BODY_GAP)
        col.place(line3, gap=BODY_GAP)

        with self.voiceover(
            text=(
                "Định nghĩa. "
                "Mọi góc đều có số đo. "
                "Góc bẹt có số đo bằng 180 độ. "
                "Không có góc nào có số đo lớn hơn 180 độ."
            )
        ) as ov:
            self.play(FadeIn(line1), run_time=ov.duration * 0.30)
            self.play(FadeIn(line2), run_time=ov.duration * 0.35)
            self.play(FadeIn(line3), run_time=ov.duration * 0.35)

        self.play(
            Indicate(line2, scale_factor=EMPHASIS_SCALE, color=EMPHASIS_COLOR),
            run_time=EMPHASIS_INDICATE_TIME,
        )
        self.wait(1.0)
        self.play(FadeOut(block_heading), FadeOut(col.all), run_time=MOTION_EXIT)

    # ── Scene 02 — Các loại góc ──────────────────────────────────────────

    def scene02_cacLoaiGoc(self):
        block_heading = self._block_heading(r"\textbf{2. Các loại góc}")
        self.play(Write(block_heading), run_time=MOTION_ENTER)

        col = TheoryColumn(block_heading, has_figure=False)
        fs = 28
        fg = FORMULA_GAP

        label_vuong = Tex(
            r"- \textbf{Góc vuông:} số đo bằng $90^\circ$",
            tex_template=viet_tex_template,
            font_size=fs,
        )
        formula_vuong = Tex(
            r"$\bullet$ $90^\circ$",
            tex_template=viet_tex_template,
            font_size=fs + 1,
        )
        label_nhon = Tex(
            r"- \textbf{Góc nhọn:} số đo nhỏ hơn góc vuông",
            tex_template=viet_tex_template,
            font_size=fs,
        )
        formula_nhon = Tex(
            r"$\bullet$ $< 90^\circ$",
            tex_template=viet_tex_template,
            font_size=fs + 1,
        )
        label_tu = Tex(
            r"- \textbf{Góc tù:} số đo lớn hơn góc vuông nhưng nhỏ hơn góc bẹt",
            tex_template=viet_tex_template,
            font_size=fs,
        )
        formula_tu = Tex(
            r"$\bullet$ $90^\circ < \ldots < 180^\circ$",
            tex_template=viet_tex_template,
            font_size=fs + 1,
        )

        col.place(label_vuong, gap=BODY_GAP)
        col.place_formula_left(formula_vuong, indent=FORMULA_INDENT, gap=fg)
        col.place(label_nhon, gap=BODY_GAP)
        col.place_formula_left(formula_nhon, indent=FORMULA_INDENT, gap=fg)
        col.place(label_tu, gap=BODY_GAP)
        col.place_formula_left(formula_tu, indent=FORMULA_INDENT, gap=fg)

        with self.voiceover(
            text=(
                "Định nghĩa. "
                "Góc vuông có số đo bằng 90 độ."
            )
        ) as ov:
            self.play(FadeIn(label_vuong), run_time=ov.duration * 0.50)
            self.play(Write(formula_vuong), run_time=ov.duration * 0.50)

        self.play(
            Indicate(VGroup(label_vuong, formula_vuong), scale_factor=EMPHASIS_SCALE, color=EMPHASIS_COLOR),
            run_time=EMPHASIS_INDICATE_TIME,
        )

        with self.voiceover(
            text="Góc nhọn có số đo nhỏ hơn góc vuông."
        ) as ov:
            self.play(FadeIn(label_nhon), run_time=ov.duration * 0.45)
            self.play(Write(formula_nhon), run_time=ov.duration * 0.55)

        self.play(
            Indicate(VGroup(label_nhon, formula_nhon), scale_factor=EMPHASIS_SCALE, color=EMPHASIS_COLOR),
            run_time=EMPHASIS_INDICATE_TIME,
        )

        with self.voiceover(
            text=(
                "Góc tù có số đo lớn hơn góc vuông "
                "nhưng nhỏ hơn góc bẹt."
            )
        ) as ov:
            self.play(FadeIn(label_tu), run_time=ov.duration * 0.45)
            self.play(Write(formula_tu), run_time=ov.duration * 0.55)

        self.play(
            Indicate(VGroup(label_tu, formula_tu), scale_factor=EMPHASIS_SCALE, color=EMPHASIS_COLOR),
            run_time=EMPHASIS_INDICATE_TIME,
        )

        self.wait(1.0)
        self.play(FadeOut(block_heading), FadeOut(col.all), run_time=MOTION_EXIT)

    # ── Scene 03 — Tiên đề cộng góc (Hình 14) ────────────────────────────

    def scene03_tienDeCongGoc(self):
        block_heading = self._block_heading(r"\textbf{3. Tiên đề cộng góc}")
        self.play(Write(block_heading), run_time=MOTION_ENTER)

        col = TheoryColumn(block_heading, has_figure=True)

        line_forward = Tex(
            r"- Nếu tia $Oy$ nằm giữa hai tia $Ox$ và $Oz$ thì tổng số đo hai góc "
            r"$x\widehat{O}y$ và $y\widehat{O}z$ bằng số đo góc $x\widehat{O}z$.",
            tex_template=viet_tex_template,
            font_size=26,
        )
        line_converse = Tex(
            r"- Ngược lại, nếu tổng số đo hai góc $x\widehat{O}y$ và $y\widehat{O}z$ bằng số đo góc "
            r"$x\widehat{O}z$ thì tia $Oy$ nằm giữa hai tia $Ox$ và $Oz$.",
            tex_template=viet_tex_template,
            font_size=26,
        )
        col.place(line_forward, gap=0.22)
        col.place(line_converse, gap=0.22)

        formula_forward = MathTex(
            r"x\widehat{O}y + y\widehat{O}z = x\widehat{O}z",
            tex_template=viet_tex_template,
            font_size=32,
        )
        formula_converse = MathTex(
            r"x\widehat{O}y + y\widehat{O}z = x\widehat{O}z",
            tex_template=viet_tex_template,
            font_size=32,
        )
        col.place_formula(formula_forward)
        col.place_formula(formula_converse)

        self.fig14 = _build_hinh14()
        self.figure_group = self.fig14["group"]
        ox, oy, oz = self.fig14["angles"]
        o = self._o_center(self.fig14["dot_O"])

        ang_xOy = _angle_between_degs(o, ox, oy, radius=0.55, color=COLOR_EQUAL_1)
        ang_yOz = _angle_between_degs(o, oy, oz, radius=0.65, color=COLOR_EQUAL_2)
        ang_xOz = _angle_between_degs(o, ox, oz, radius=0.90, color=COLOR_EQUAL_3)
        self.angle_group_s3 = VGroup(ang_xOy, ang_yOz, ang_xOz)

        with self.voiceover(
            text=(
                "Định lí. "
                "Nếu tia O y nằm giữa hai tia O x và O z "
                "thì tổng góc x O y và góc y O z "
                "bằng góc x O z."
            )
        ) as ov:
            self.play(Create(self.fig14["ray_Ox"]), run_time=ov.duration * 0.25)
            self.play(
                Create(self.fig14["ray_Oy"]),
                Create(self.fig14["ray_Oz"]),
                FadeIn(self.fig14["dot_O"]),
                Write(self.fig14["label_O"]),
                Write(self.fig14["label_x"]),
                Write(self.fig14["label_y"]),
                Write(self.fig14["label_z"]),
                run_time=ov.duration * 0.35,
            )
            self.play(FadeIn(line_forward), run_time=ov.duration * 0.20)
            self.play(Write(formula_forward), run_time=ov.duration * 0.20)

        with self.voiceover(
            text=(
                "Chẳng hạn, trên hình vẽ, "
                "góc x O y cộng góc y O z bằng góc x O z."
            )
        ) as ov:
            self.play(Create(ang_xOy), run_time=ov.duration * 0.25)
            self.play(Create(ang_yOz), run_time=ov.duration * 0.25)
            self.play(
                Indicate(VGroup(ang_xOy, ang_yOz), color=COLOR_EQUAL_1, scale_factor=EMPHASIS_SCALE),
                run_time=ov.duration * 0.20,
            )
            self.play(Create(ang_xOz), run_time=ov.duration * 0.15)
            self.play(
                Indicate(ang_xOz, color=COLOR_EQUAL_3, scale_factor=EMPHASIS_SCALE),
                run_time=ov.duration * 0.15,
            )

        with self.voiceover(
            text=(
                "Ngược lại, nếu tổng hai góc x O y và y O z "
                "bằng góc x O z "
                "thì tia O y nằm giữa hai tia O x và O z."
            )
        ) as ov:
            self.play(FadeIn(line_converse), run_time=ov.duration * 0.35)
            self.play(Write(formula_converse), run_time=ov.duration * 0.35)
            self.play(
                Indicate(self.fig14["ray_Oy"], color=EMPHASIS_COLOR, scale_factor=EMPHASIS_SCALE),
                run_time=ov.duration * 0.30,
            )

        self.wait(1.0)
        self.play(
            FadeOut(block_heading),
            FadeOut(col.all),
            FadeOut(self.angle_group_s3),
            FadeOut(self.figure_group),
            run_time=MOTION_EXIT,
        )

    # ── Scene 04 — Quan hệ giữa hai góc (Hình 15) ────────────────────────

    def scene04_quanHeHaiGoc(self):
        block_heading = self._block_heading(r"\textbf{4. Quan hệ giữa hai góc}")
        self.play(Write(block_heading), run_time=MOTION_ENTER)

        col = TheoryColumn(block_heading, has_figure=True)
        fs = 24

        label_ke = Tex(
            r"- \textbf{Hai góc kề nhau:} chung một cạnh; hai cạnh còn lại nằm ở hai nửa mặt phẳng đối nhau",
            tex_template=viet_tex_template,
            font_size=fs,
        )
        label_phu = Tex(
            r"- \textbf{Hai góc phụ nhau:} tổng số đo bằng $90^\circ$",
            tex_template=viet_tex_template,
            font_size=fs,
        )
        formula_phu = Tex(r"$\bullet$ $90^\circ$", tex_template=viet_tex_template, font_size=fs + 1)
        label_bu = Tex(
            r"- \textbf{Hai góc bù nhau:} tổng số đo bằng $180^\circ$",
            tex_template=viet_tex_template,
            font_size=fs,
        )
        formula_bu = Tex(r"$\bullet$ $180^\circ$", tex_template=viet_tex_template, font_size=fs + 1)
        label_ke_bu = Tex(
            r"- \textbf{Hai góc kề bù:} vừa kề nhau vừa bù nhau",
            tex_template=viet_tex_template,
            font_size=fs,
        )

        col.place(label_ke, gap=0.14)
        col.place(label_phu, gap=0.14)
        col.place_formula_left(formula_phu, indent=FORMULA_INDENT, gap=0.20)
        col.place(label_bu, gap=0.14)
        col.place_formula_left(formula_bu, indent=FORMULA_INDENT, gap=0.20)
        col.place(label_ke_bu, gap=0.14)

        nhan_xet_heading = Tex(
            r"\textbf{(*) Nhận xét}",
            tex_template=viet_tex_template,
            font_size=fs + 2,
            color=COLOR_WARNING,
        )
        nhan_xet_1 = Tex(
            r"\textit{- Nếu hai góc kề có hai cạnh ngoài là hai tia đối nhau thì chúng bù nhau.}",
            tex_template=viet_tex_template,
            font_size=fs,
            color=COLOR_WARNING,
        )
        nhan_xet_2 = Tex(
            r"\textit{- Nếu hai góc kề bù thì tổng bằng $180^\circ$ và hai cạnh ngoài là hai tia đối nhau.}",
            tex_template=viet_tex_template,
            font_size=fs,
            color=COLOR_WARNING,
        )
        col.place(nhan_xet_heading, gap=0.18)
        col.place_bullet(nhan_xet_1, gap=0.14)
        col.place_bullet(nhan_xet_2, gap=0.14)

        self.fig15 = _build_hinh15()
        self.figure_group = self.fig15["group"]
        o = self._o_center(self.fig15["dot_O"])
        ang_xOy = _angle_between_degs(o, 180, FIG15_OY_DEG, radius=0.55, color=COLOR_EQUAL_1)
        ang_yOz = _angle_between_degs(o, FIG15_OY_DEG, 0, radius=0.45, color=COLOR_EQUAL_2)
        self.angle_group_s4 = VGroup(ang_xOy, ang_yOz)

        with self.voiceover(
            text=(
                "Định nghĩa. "
                "Hai góc kề nhau chung một cạnh; "
                "hai cạnh còn lại nằm ở hai nửa mặt phẳng đối nhau. "
                "Như đã thấy ở Hình 14, hai góc kề có thể nằm cùng nửa mặt phẳng."
            )
        ) as ov:
            self.play(FadeIn(label_ke), run_time=ov.duration)

        with self.voiceover(
            text="Hai góc phụ nhau có tổng số đo bằng 90 độ."
        ) as ov:
            self.play(FadeIn(label_phu), run_time=ov.duration * 0.45)
            self.play(Write(formula_phu), run_time=ov.duration * 0.55)

        self.play(
            Indicate(VGroup(label_phu, formula_phu), scale_factor=EMPHASIS_SCALE, color=EMPHASIS_COLOR),
            run_time=EMPHASIS_INDICATE_TIME,
        )

        with self.voiceover(
            text="Hai góc bù nhau có tổng số đo bằng 180 độ."
        ) as ov:
            self.play(FadeIn(label_bu), run_time=ov.duration * 0.45)
            self.play(Write(formula_bu), run_time=ov.duration * 0.55)

        self.play(
            Indicate(VGroup(label_bu, formula_bu), scale_factor=EMPHASIS_SCALE, color=EMPHASIS_COLOR),
            run_time=EMPHASIS_INDICATE_TIME,
        )

        with self.voiceover(
            text=(
                "Hai góc kề bù vừa kề nhau vừa bù nhau. "
                "Trên hình vẽ, hai góc kề bù có tổng bằng 180 độ."
            )
        ) as ov:
            self.play(FadeIn(label_ke_bu), run_time=ov.duration * 0.15)
            self.play(
                Create(self.fig15["line_xz"]),
                Write(self.fig15["label_x"]),
                Write(self.fig15["label_O"]),
                Write(self.fig15["label_z"]),
                run_time=ov.duration * 0.30,
            )
            self.play(
                Create(self.fig15["ray_Oy"]),
                Write(self.fig15["label_y"]),
                FadeIn(self.fig15["dot_O"]),
                run_time=ov.duration * 0.25,
            )
            self.play(Create(ang_xOy), Create(ang_yOz), run_time=ov.duration * 0.20)
            self.play(
                Indicate(VGroup(ang_xOy, ang_yOz), color=COLOR_EQUAL_1, scale_factor=EMPHASIS_SCALE),
                run_time=ov.duration * 0.10,
            )

        with self.voiceover(text="Nhận xét.") as ov:
            self.play(Write(nhan_xet_heading), run_time=ov.duration)

        with self.voiceover(
            text=(
                "Nếu hai góc kề có hai cạnh ngoài là hai tia đối nhau "
                "thì chúng bù nhau."
            )
        ) as ov:
            self.play(FadeIn(nhan_xet_1), run_time=ov.duration)

        with self.voiceover(
            text=(
                "Nếu hai góc kề bù thì tổng bằng 180 độ "
                "và hai cạnh ngoài là hai tia đối nhau."
            )
        ) as ov:
            self.play(FadeIn(nhan_xet_2), run_time=ov.duration)

        self.wait(1.0)
        self.play(
            FadeOut(block_heading),
            FadeOut(col.all),
            FadeOut(self.angle_group_s4),
            FadeOut(self.figure_group),
            run_time=MOTION_EXIT,
        )

    # ── Scene 05 — Dựng góc trên nửa mặt phẳng ───────────────────────────

    def scene05_dungGoc(self):
        block_heading = self._block_heading(r"\textbf{5. Dựng góc trên nửa mặt phẳng}")
        self.play(Write(block_heading), run_time=MOTION_ENTER)

        col = TheoryColumn(block_heading, has_figure=False)

        body = tex_wrapped(
            r"Trên nửa mặt phẳng cho trước có bờ chứa tia $Ox$, tồn tại "
            r"\textbf{duy nhất} một tia $Oy$ sao cho số đo góc $x\widehat{O}y$ bằng $m^\circ$.",
            font_size=28,
        )
        formula_dung = MathTex(
            r"x\widehat{O}y = m^\circ",
            tex_template=viet_tex_template,
            font_size=32,
        )
        col.place(body, gap=BODY_GAP)
        col.place_formula_left(formula_dung, indent=FORMULA_INDENT, gap=FORMULA_GAP)

        with self.voiceover(
            text=(
                "Định lí. "
                "Trên nửa mặt phẳng cho trước có bờ chứa tia O x, "
                "tồn tại duy nhất một tia O y "
                "sao cho góc x O y bằng m độ."
            )
        ) as ov:
            self.play(FadeIn(body), run_time=ov.duration * 0.55)
            self.play(Write(formula_dung), run_time=ov.duration * 0.45)

        self.play(
            Indicate(body, scale_factor=EMPHASIS_SCALE, color=EMPHASIS_COLOR),
            run_time=EMPHASIS_INDICATE_TIME,
        )
        self.wait(1.0)
        self.play(FadeOut(block_heading), FadeOut(col.all), run_time=MOTION_EXIT)

    # ── Scene 06 — So sánh góc (Hình 16) ─────────────────────────────────

    def scene06_soSanhGoc(self):
        block_heading = self._block_heading(r"\textbf{6. So sánh góc trên nửa mặt phẳng}")
        self.play(Write(block_heading), run_time=MOTION_ENTER)

        col = TheoryColumn(block_heading, has_figure=True)

        statement = Tex(
            r"Trên nửa mặt phẳng bờ chứa tia $Ox$, nếu $x\widehat{O}y = m^\circ$, "
            r"$x\widehat{O}z = n^\circ$ và $m < n$ thì tia $Oy$ nằm giữa hai tia $Ox$ và $Oz$.",
            tex_template=viet_tex_template,
            font_size=26,
        )
        formula_angles = MathTex(
            r"x\widehat{O}y = m^\circ,\quad x\widehat{O}z = n^\circ",
            tex_template=viet_tex_template,
            font_size=30,
        )
        formula_compare = MathTex(
            r"m < n",
            tex_template=viet_tex_template,
            font_size=32,
        )
        col.place(statement, gap=0.22)
        col.place_formula(formula_angles)
        col.place_formula(formula_compare)

        self.fig16 = _build_hinh16()
        self.figure_group = self.fig16["group"]
        ox, oy, oz = self.fig16["angles"]
        o = self._o_center(self.fig16["dot_O"])
        half_plane = _half_plane_at_o(o)

        ang_xOy = _angle_between_degs(o, ox, oy, radius=0.55, color=COLOR_EQUAL_1)
        ang_xOz = _angle_between_degs(o, ox, oz, radius=0.90, color=COLOR_EQUAL_3)
        label_m = _angle_label_at(o, ox, oy, r"m^\circ", radius=0.72)
        label_n = _angle_label_at(o, ox, oz, r"n^\circ", radius=1.05)
        self.angle_group_s6 = VGroup(ang_xOy, ang_xOz, label_m, label_n)

        with self.voiceover(
            text=(
                "Định lí. "
                "Trên nửa mặt phẳng bờ chứa tia O x, "
                "nếu góc x O y bằng m độ, "
                "góc x O z bằng n độ, "
                "và m nhỏ hơn n "
                "thì tia O y nằm giữa hai tia O x và O z."
            )
        ) as ov:
            self.play(Create(self.fig16["ray_Ox"]), run_time=ov.duration * 0.15)
            self.play(FadeIn(half_plane), run_time=ov.duration * 0.12)
            self.play(
                Create(self.fig16["ray_Oy"]),
                Create(ang_xOy),
                Write(label_m),
                FadeIn(self.fig16["dot_O"]),
                Write(self.fig16["label_O"]),
                Write(self.fig16["label_x"]),
                Write(self.fig16["label_y"]),
                run_time=ov.duration * 0.25,
            )
            self.play(
                Create(self.fig16["ray_Oz"]),
                Create(ang_xOz),
                Write(label_n),
                Write(self.fig16["label_z"]),
                run_time=ov.duration * 0.20,
            )
            self.play(FadeIn(statement), run_time=ov.duration * 0.13)
            self.play(Write(formula_angles), run_time=ov.duration * 0.08)
            self.play(Write(formula_compare), run_time=ov.duration * 0.07)

        with self.voiceover(
            text=(
                "Trên hình, góc m nhỏ hơn góc n "
                "nên O y nằm giữa O x và O z."
            )
        ) as ov:
            self.play(
                Indicate(VGroup(ang_xOy, ang_xOz), scale_factor=EMPHASIS_SCALE, color=EMPHASIS_COLOR),
                run_time=ov.duration * 0.45,
            )
            self.play(
                Indicate(self.fig16["ray_Oy"], color=EMPHASIS_COLOR, scale_factor=EMPHASIS_SCALE),
                run_time=ov.duration * 0.55,
            )

        self.wait(1.5)
        self.play(
            FadeOut(block_heading),
            FadeOut(col.all),
            FadeOut(half_plane),
            FadeOut(self.angle_group_s6),
            FadeOut(self.figure_group),
            FadeOut(self.section_heading),
            FadeOut(self.lesson_title),
            run_time=MOTION_EXIT,
        )
