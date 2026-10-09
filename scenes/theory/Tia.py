"""CÁC DẤU HIỆU NHẬN BIẾT MỘT TIA NẰM GIỮA HAI TIA KHÁC — video lý thuyết.

Spec: specs/theory/tia/spec-ly-thuyet.md
Subject: geometry   |   Scenes: 8   |   ~8–10 phút
Hình SGK: 33–37 (tái dùng Hình 33 scenes 01→03).
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
    GeometryEngine,
    line_intersection,
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

LESSON_TITLE_TEX = (
    r"\textbf{CÁC DẤU HIỆU NHẬN BIẾT MỘT TIA NẰM GIỮA HAI TIA KHÁC}"
)
SECTION_HEADING_TEX = r"\textbf{A. KIẾN THỨC CẦN NHỚ}"

# Hình 33–37 — từ spec
O_LOCAL = ORIGIN
RAY_LEN = 3.0
DIST_AB = 2.5
DOT_M_RADIUS = 0.07
HALF_PLANE_OPACITY = 0.12
ANGLE_MARK_DIST = 0.85

FIG33_ANGLES = (0, 40, 95)  # Ox, Oy, Oz
FIG34_ANGLES = (0, 25, 55, 100)  # Ox, Oy, Oz, Ot
FIG35_ANGLES = (0, 20, 45, 70, 90)  # Ox, Om, Ot, On, Oy
FIG36_ANGLES = (0, 40, 320)  # OA, OB, OC
FIG37_ANGLES = (0, 135, 225)  # OA, OB, OC (OA' = 180 vẽ sau)


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
    """Nửa mặt phẳng phía trên Ox, căn theo O sau place_figure."""
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


def _build_hinh33() -> dict:
    """Hình 33 — dấu hiệu 1."""
    O = np.array(O_LOCAL, dtype=float)
    ray_Ox, _ = _make_ray(FIG33_ANGLES[0])
    ray_Oz, tip_z = _make_ray(FIG33_ANGLES[2])
    ray_Oy, tip_y = _make_ray(FIG33_ANGLES[1])
    A = _pt_ray(FIG33_ANGLES[0], DIST_AB)
    B = _pt_ray(FIG33_ANGLES[2], DIST_AB)
    seg_AB = Line(A, B, color=COLOR_DEFAULT, stroke_width=STATE_DEFAULT["stroke_width"])
    seg_AB.set_z_index(LAYER_GEOMETRY)
    M = line_intersection([A, B], [O, tip_y])

    dot_O = Dot(O, radius=MARKER_DOT_RADIUS, color=COLOR_ACTIVE).set_z_index(LAYER_MARKERS)
    dot_A = Dot(A, radius=MARKER_DOT_RADIUS).set_z_index(LAYER_MARKERS)
    dot_B = Dot(B, radius=MARKER_DOT_RADIUS).set_z_index(LAYER_MARKERS)
    dot_M = Dot(M, radius=DOT_M_RADIUS, color=COLOR_ACTIVE).set_z_index(LAYER_MARKERS)

    label_O = _label_math("O", O, DOWN)
    label_A = _label_math("A", A, UR)
    label_B = _label_math("B", B, UL)
    label_M = _label_math("M", M, RIGHT)
    label_x = _ray_label("x", FIG33_ANGLES[0])
    label_y = _ray_label("y", FIG33_ANGLES[1])
    label_z = _ray_label("z", FIG33_ANGLES[2])

    figure_group = VGroup(
        ray_Ox,
        ray_Oz,
        ray_Oy,
        seg_AB,
        dot_O,
        dot_A,
        dot_B,
        dot_M,
        label_O,
        label_A,
        label_B,
        label_M,
        label_x,
        label_y,
        label_z,
    )
    place_figure(figure_group)

    return {
        "group": figure_group,
        "dot_O": dot_O,
        "dot_A": dot_A,
        "dot_B": dot_B,
        "dot_M": dot_M,
        "ray_Ox": ray_Ox,
        "ray_Oy": ray_Oy,
        "ray_Oz": ray_Oz,
        "seg_AB": seg_AB,
        "label_O": label_O,
        "label_A": label_A,
        "label_B": label_B,
        "label_M": label_M,
        "label_x": label_x,
        "label_y": label_y,
        "label_z": label_z,
        "angles": FIG33_ANGLES,
    }


def _build_multi_ray(
    ray_names: list[tuple[str, float]],
    *,
    half_plane: bool = False,
    angle_pairs: list[tuple[float, float, float, str]] | None = None,
) -> dict:
    """Dựng hình nhiều tia quanh O. angle_pairs: (deg1, deg2, radius, color_token_name)."""
    O = np.array(O_LOCAL, dtype=float)
    rays = {}
    labels = []
    mobs = []

    for name, deg in ray_names:
        ray, _ = _make_ray(deg)
        rays[name] = ray
        mobs.append(ray)
        labels.append(_ray_label(name, deg))

    dot_O = Dot(O, radius=MARKER_DOT_RADIUS, color=COLOR_ACTIVE).set_z_index(LAYER_MARKERS)
    label_O = _label_math("O", O, DOWN)
    mobs.extend([dot_O, label_O, *labels])

    angle_mobs = VGroup()
    if angle_pairs:
        color_map = {
            "1": COLOR_EQUAL_1,
            "2": COLOR_EQUAL_2,
            "3": COLOR_EQUAL_3,
        }
        for d1, d2, rad, ckey in angle_pairs:
            ang = _angle_between_degs(O, d1, d2, radius=rad, color=color_map[ckey])
            angle_mobs.add(ang)
        mobs.extend(angle_mobs)

    figure_group = VGroup(*mobs)
    place_figure(figure_group)

    return {
        "group": figure_group,
        "dot_O": dot_O,
        "label_O": label_O,
        "labels": labels,
        "rays": rays,
        "angle_mobs": angle_mobs,
        "ray_names": ray_names,
        "half_plane": half_plane,
    }


class Tia(VoiceoverScene):
    """Video lý thuyết: Các dấu hiệu nhận biết một tia nằm giữa hai tia khác."""

    def construct(self):
        self.set_speech_service(make_gtts_service())
        self.setup_scene_style()
        self.scene00_intro()
        self.scene01_dauHieu1()
        self.scene02_dauHieu2()
        self.scene03_dauHieu3()
        self.scene04_dauHieu4()
        self.scene05_dauHieu5()
        self.scene06_dauHieu6a()
        self.scene07_dauHieu6b()

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

    def _block_heading(self, text: str) -> Tex:
        self._ensure_lesson_title()
        self._ensure_section_heading()
        heading = Tex(text, tex_template=viet_tex_template, font_size=32)
        heading.next_to(self._heading_anchor(), DOWN, buff=0.25)
        heading.align_to([TEXT_LEFT_X, 0, 0], LEFT)
        return heading

    def _register_fig33_geo(self, fig: dict):
        self.geo = GeometryEngine(self)
        self.geo.register_point("O", fig["dot_O"].get_center(), dot=fig["dot_O"])
        self.geo.register_point("A", fig["dot_A"].get_center(), dot=fig["dot_A"])
        self.geo.register_point("B", fig["dot_B"].get_center(), dot=fig["dot_B"])
        self.geo.register_point("M", fig["dot_M"].get_center(), dot=fig["dot_M"])

    def _o_center(self) -> np.ndarray:
        return self.geo.point("O")

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
                "Các dấu hiệu nhận biết một tia nằm giữa hai tia khác. "
                "Phần A. Kiến thức cần nhớ. "
                "Khi tia O y nằm giữa O x và O z, "
                "tổng góc x O y cộng góc y O z bằng góc x O z. "
                "Bài học giúp rèn luyện lập luận chính xác "
                "khi xét vị trí tương đối của các tia."
            )
        ) as ov:
            self.play(FadeIn(self.lesson_title), run_time=ov.duration * 0.45)
            self.play(FadeIn(self.section_heading), run_time=ov.duration * 0.40)
            self.wait(ov.duration * 0.15)

        self.wait(1.5)

    # ── Scene 01 — Dấu hiệu 1 (Hình 33) ──────────────────────────────────

    def scene01_dauHieu1(self):
        block_heading = self._block_heading(r"\textbf{Dấu hiệu 1}")
        self.play(Write(block_heading), run_time=MOTION_ENTER)

        col = TheoryColumn(block_heading, has_figure=True)

        line1 = Tex(
            r"Cho tia $Oy$ cắt đoạn thẳng $AB$ tại điểm $M$ nằm giữa hai điểm $A$ và $B$",
            tex_template=viet_tex_template,
            font_size=26,
        )
        line2 = Tex(
            r"($A, B$ khác $O$; $A$ thuộc tia $Ox$; $B$ thuộc tia $Oz$).",
            tex_template=viet_tex_template,
            font_size=26,
        )
        line3 = Tex(
            r"Khi đó tia $Oy$ nằm giữa hai tia $Ox$ và $Oz$.",
            tex_template=viet_tex_template,
            font_size=26,
        )
        col.place(line1)
        col.place(line2)
        col.place(line3)

        self.fig33 = _build_hinh33()
        self.figure_group = self.fig33["group"]
        self._register_fig33_geo(self.fig33)

        with self.voiceover(
            text=(
                "Dấu hiệu một. "
                "Cho tia O y cắt đoạn thẳng A B tại điểm M nằm giữa hai điểm A và B. "
                "A và B khác O; A thuộc tia O x; B thuộc tia O z."
            )
        ) as ov:
            self.play(
                Create(self.fig33["ray_Ox"]),
                Create(self.fig33["ray_Oz"]),
                FadeIn(self.fig33["dot_O"]),
                Write(self.fig33["label_O"]),
                Write(self.fig33["label_x"]),
                Write(self.fig33["label_z"]),
                run_time=ov.duration * 0.35,
            )
            self.play(
                FadeIn(line1),
                FadeIn(line2),
                Create(self.fig33["dot_A"]),
                Create(self.fig33["dot_B"]),
                Write(self.fig33["label_A"]),
                Write(self.fig33["label_B"]),
                Create(self.fig33["seg_AB"]),
                run_time=ov.duration * 0.65,
            )

        with self.voiceover(
            text=(
                "Khi đó tia O y nằm giữa hai tia O x và O z. "
                "Chẳng hạn, trên hình vẽ, "
                "tia O y cắt đoạn A B tại M nằm giữa A và B."
            )
        ) as ov:
            self.play(FadeIn(line3), run_time=ov.duration * 0.15)
            self.play(
                Create(self.fig33["ray_Oy"]),
                FadeIn(self.fig33["dot_M"]),
                Write(self.fig33["label_y"]),
                Write(self.fig33["label_M"]),
                run_time=ov.duration * 0.35,
            )
            self.play(
                Indicate(
                    VGroup(self.fig33["dot_M"], self.fig33["dot_A"], self.fig33["dot_B"]),
                    color=EMPHASIS_COLOR,
                    scale_factor=EMPHASIS_SCALE,
                ),
                run_time=ov.duration * 0.25,
            )
            self.play(
                Indicate(self.fig33["ray_Oy"], color=EMPHASIS_COLOR, scale_factor=EMPHASIS_SCALE),
                run_time=ov.duration * 0.25,
            )

        self.wait(1.0)
        self.play(FadeOut(block_heading), FadeOut(col.all), run_time=MOTION_EXIT)

    # ── Scene 02 — Dấu hiệu 2 (reuse Hình 33) ────────────────────────────

    def scene02_dauHieu2(self):
        block_heading = self._block_heading(r"\textbf{Dấu hiệu 2}")
        self.play(Write(block_heading), run_time=MOTION_ENTER)

        col = TheoryColumn(block_heading, has_figure=True)

        statement = Tex(
            r"Nếu tổng số đo hai góc $x\widehat{O}y$ và $y\widehat{O}z$ bằng số đo góc "
            r"$x\widehat{O}z$ thì tia $Oy$ nằm giữa hai tia $Ox$ và $Oz$.",
            tex_template=viet_tex_template,
            font_size=26,
        )
        col.place(statement, gap=0.30)

        formula_sum = MathTex(
            r"x\widehat{O}y + y\widehat{O}z = x\widehat{O}z",
            tex_template=viet_tex_template,
            font_size=34,
        )
        col.place_formula(formula_sum)

        ox, oy, oz = self.fig33["angles"]
        o = self._o_center()
        ang_xOy = _angle_between_degs(o, ox, oy, radius=0.55, color=COLOR_EQUAL_1)
        ang_yOz = _angle_between_degs(o, oy, oz, radius=0.65, color=COLOR_EQUAL_2)
        ang_xOz = _angle_between_degs(o, ox, oz, radius=0.90, color=COLOR_EQUAL_3)
        self.angle_group_s2 = VGroup(ang_xOy, ang_yOz, ang_xOz)

        with self.voiceover(
            text=(
                "Dấu hiệu hai. "
                "Nếu tổng số đo hai góc x O y và y O z "
                "bằng số đo góc x O z "
                "thì tia Oy nằm giữa hai tia O x và O z."
            )
        ) as ov:
            self.play(FadeIn(statement), run_time=ov.duration * 0.40)
            self.play(Write(formula_sum), run_time=ov.duration * 0.60)

        with self.voiceover(
            text=(
                "Trên hình, góc x O y cộng góc y O z bằng góc x O z."
            )
        ) as ov:
            self.play(Create(ang_xOy), run_time=ov.duration * 0.25)
            self.play(Create(ang_yOz), run_time=ov.duration * 0.25)
            self.play(Create(ang_xOz), run_time=ov.duration * 0.20)
            self.play(
                Indicate(VGroup(ang_xOy, ang_yOz), color=COLOR_EQUAL_1, scale_factor=EMPHASIS_SCALE),
                run_time=ov.duration * 0.15,
            )
            self.play(
                Indicate(ang_xOz, color=COLOR_EQUAL_3, scale_factor=EMPHASIS_SCALE),
                run_time=ov.duration * 0.15,
            )

        self.wait(1.0)
        self.play(
            FadeOut(block_heading),
            FadeOut(col.all),
            FadeOut(formula_sum),
            FadeOut(self.angle_group_s2),
            run_time=MOTION_EXIT,
        )

    # ── Scene 03 — Dấu hiệu 3 (reuse Hình 33) ────────────────────────────

    def scene03_dauHieu3(self):
        block_heading = self._block_heading(r"\textbf{Dấu hiệu 3}")
        self.play(Write(block_heading), run_time=MOTION_ENTER)

        col = TheoryColumn(block_heading, has_figure=True)

        statement = Tex(
            r"Trên cùng một nửa mặt phẳng bờ chứa tia $Ox$, nếu $x\widehat{O}y < x\widehat{O}z$ "
            r"thì tia $Oy$ nằm giữa hai tia $Ox$ và $Oz$.",
            tex_template=viet_tex_template,
            font_size=26,
        )
        col.place(statement, gap=0.30)

        formula_compare = MathTex(
            r"x\widehat{O}y < x\widehat{O}z",
            tex_template=viet_tex_template,
            font_size=34,
        )
        col.place_formula(formula_compare)

        o = self._o_center()
        half_plane = _half_plane_at_o(o)

        ox, oy, oz = self.fig33["angles"]
        ang_xOy = _angle_between_degs(o, ox, oy, radius=0.55, color=COLOR_EQUAL_1)
        ang_xOz = _angle_between_degs(o, ox, oz, radius=0.90, color=COLOR_EQUAL_3)
        self.angle_group_s3 = VGroup(ang_xOy, ang_xOz)

        with self.voiceover(
            text=(
                "Dấu hiệu ba. "
                "Trên cùng một nửa mặt phẳng bờ chứa tia O x, "
                "nếu góc x O y nhỏ hơn góc x O z "
                "thì tia O y nằm giữa hai tia O x và O z."
            )
        ) as ov:
            self.play(FadeIn(half_plane), run_time=ov.duration * 0.20)
            self.play(FadeIn(statement), run_time=ov.duration * 0.35)
            self.play(Create(ang_xOy), Create(ang_xOz), run_time=ov.duration * 0.25)
            self.play(
                Indicate(VGroup(ang_xOy, ang_xOz), scale_factor=EMPHASIS_SCALE, color=EMPHASIS_COLOR),
                run_time=ov.duration * 0.20,
            )

        with self.voiceover(
            text=(
                "Trên hình, góc x O y nhỏ hơn góc x O z "
                "nên O y nằm giữa O x và O z."
            )
        ) as ov:
            self.play(Write(formula_compare), run_time=ov.duration * 0.35)
            self.play(
                Indicate(self.fig33["ray_Oy"], color=EMPHASIS_COLOR, scale_factor=EMPHASIS_SCALE),
                run_time=ov.duration * 0.65,
            )

        self.wait(1.0)
        self.play(
            FadeOut(block_heading),
            FadeOut(col.all),
            FadeOut(formula_compare),
            FadeOut(half_plane),
            FadeOut(self.angle_group_s3),
            FadeOut(self.figure_group),
            run_time=MOTION_EXIT,
        )

    # ── Scene 04 — Dấu hiệu 4 (Hình 34) ──────────────────────────────────

    def scene04_dauHieu4(self):
        block_heading = self._block_heading(r"\textbf{Dấu hiệu 4}")
        self.play(Write(block_heading), run_time=MOTION_ENTER)

        col = TheoryColumn(block_heading, has_figure=True)

        line1 = Tex(
            r"Sau đây ta thừa nhận ba dấu hiệu mới để nhận biết một tia nằm giữa hai tia khác.",
            tex_template=viet_tex_template,
            font_size=26,
        )
        line2 = Tex(
            r"Cho bốn tia $Ox$, $Oy$, $Oz$, $Ot$ cùng nằm trên một nửa mặt phẳng bờ chứa tia $Ox$.",
            tex_template=viet_tex_template,
            font_size=26,
        )
        line3 = Tex(
            r"Nếu $x\widehat{O}y < x\widehat{O}z < x\widehat{O}t$ thì tia $Oz$ nằm giữa hai tia $Oy$ và $Ot$.",
            tex_template=viet_tex_template,
            font_size=26,
        )
        col.place(line1)
        col.place(line2)
        col.place(line3)

        formula_chain = MathTex(
            r"x\widehat{O}y < x\widehat{O}z < x\widehat{O}t",
            tex_template=viet_tex_template,
            font_size=34,
        )
        col.place_formula(formula_chain)

        self.fig34 = _build_multi_ray(
            [("x", 0), ("y", 25), ("z", 55), ("t", 100)],
            half_plane=True,
        )
        self.figure_group = self.fig34["group"]
        rays = self.fig34["rays"]
        half_plane = _half_plane_at_o(self.fig34["dot_O"].get_center())
        ray_labels = VGroup(*self.fig34["labels"])

        with self.voiceover(
            text=(
                "Dấu hiệu bốn. "
                "Sau đây ta thừa nhận ba dấu hiệu mới. "
                "Cho bốn tia O x, O y, O z, O t "
                "cùng nằm trên một nửa mặt phẳng bờ chứa tia O x."
            )
        ) as ov:
            self.play(FadeIn(line1), run_time=ov.duration * 0.20)
            self.play(
                Create(rays["x"]),
                FadeIn(half_plane),
                FadeIn(self.fig34["dot_O"]),
                Write(self.fig34["label_O"]),
                Write(ray_labels),
                run_time=ov.duration * 0.25,
            )
            self.play(Create(rays["y"]), run_time=ov.duration * 0.18)
            self.play(Create(rays["z"]), run_time=ov.duration * 0.18)
            self.play(Create(rays["t"]), run_time=ov.duration * 0.19)

        with self.voiceover(
            text=(
                "Nếu góc x O y nhỏ hơn góc x O z, "
                "và góc x O z nhỏ hơn góc x O t, "
                "thì tia O z nằm giữa hai tia O y và O t. "
                "Trên hình, các góc tăng dần theo thứ tự y, z, t."
            )
        ) as ov:
            self.play(FadeIn(line2), FadeIn(line3), run_time=ov.duration * 0.20)
            self.play(Write(formula_chain), run_time=ov.duration * 0.25)
            self.play(
                Indicate(VGroup(rays["y"], rays["z"], rays["t"]), scale_factor=EMPHASIS_SCALE),
                run_time=ov.duration * 0.25,
            )
            self.play(
                Indicate(rays["z"], color=EMPHASIS_COLOR, scale_factor=EMPHASIS_SCALE),
                run_time=ov.duration * 0.30,
            )

        self.wait(1.0)
        self.play(
            FadeOut(block_heading),
            FadeOut(col.all),
            FadeOut(formula_chain),
            FadeOut(half_plane),
            FadeOut(self.figure_group),
            run_time=MOTION_EXIT,
        )

    # ── Scene 05 — Dấu hiệu 5 (Hình 35) ──────────────────────────────────

    def scene05_dauHieu5(self):
        block_heading = self._block_heading(r"\textbf{Dấu hiệu 5}")
        self.play(Write(block_heading), run_time=MOTION_ENTER)

        col = TheoryColumn(block_heading, has_figure=True)

        line1 = Tex(
            r"Cho năm tia $Ox$, $Om$, $Ot$, $On$, $Oy$ cùng nằm trên một nửa mặt phẳng bờ chứa tia $Ox$.",
            tex_template=viet_tex_template,
            font_size=26,
        )
        line2 = Tex(
            r"Nếu tia $Ot$ nằm giữa hai tia $Ox$ và $Oy$;",
            tex_template=viet_tex_template,
            font_size=26,
        )
        line3 = Tex(
            r"tia $Om$ nằm giữa hai tia $Ot$ và $Ox$;",
            tex_template=viet_tex_template,
            font_size=26,
        )
        line4 = Tex(
            r"tia $On$ nằm giữa hai tia $Ot$ và $Oy$ thì tia $Ot$ nằm giữa hai tia $Om$ và $On$.",
            tex_template=viet_tex_template,
            font_size=26,
        )
        col.place(line1)
        col.place(line2)
        col.place(line3)
        col.place(line4)

        self.fig35 = _build_multi_ray(
            [("x", 0), ("m", 20), ("t", 45), ("n", 70), ("y", 90)],
        )
        self.figure_group = self.fig35["group"]
        rays = self.fig35["rays"]
        ray_labels = VGroup(*self.fig35["labels"])

        with self.voiceover(
            text=(
                "Dấu hiệu năm. "
                "Cho năm tia O x, O m, O t, O n, O y "
                "cùng nằm trên một nửa mặt phẳng bờ chứa tia O x. "
                "Ot nằm giữa O x và O y; "
                "Om nằm giữa O t và O x; "
                "On nằm giữa O t và O y."
            )
        ) as ov:
            self.play(
                Create(rays["x"]),
                FadeIn(self.fig35["dot_O"]),
                Write(self.fig35["label_O"]),
                Write(ray_labels),
                run_time=ov.duration * 0.10,
            )
            self.play(Create(rays["m"]), run_time=ov.duration * 0.12)
            self.play(Create(rays["t"]), run_time=ov.duration * 0.12)
            self.play(Create(rays["n"]), run_time=ov.duration * 0.12)
            self.play(Create(rays["y"]), run_time=ov.duration * 0.12)
            self.play(
                FadeIn(line1),
                FadeIn(line2),
                FadeIn(line3),
                FadeIn(line4),
                run_time=ov.duration * 0.42,
            )

        with self.voiceover(
            text=(
                "Khi đó tia O t nằm giữa hai tia O m và O n. "
                "Trên hình, O t nằm giữa O m và O n."
            )
        ) as ov:
            self.play(
                Indicate(VGroup(rays["t"], rays["x"], rays["y"]), scale_factor=EMPHASIS_SCALE),
                run_time=ov.duration * 0.20,
            )
            self.play(
                Indicate(VGroup(rays["m"], rays["t"], rays["x"]), scale_factor=EMPHASIS_SCALE),
                run_time=ov.duration * 0.20,
            )
            self.play(
                Indicate(VGroup(rays["n"], rays["t"], rays["y"]), scale_factor=EMPHASIS_SCALE),
                run_time=ov.duration * 0.20,
            )
            self.play(
                Indicate(
                    VGroup(rays["t"], rays["m"], rays["n"]),
                    color=EMPHASIS_COLOR,
                    scale_factor=EMPHASIS_SCALE,
                ),
                run_time=ov.duration * 0.40,
            )

        self.wait(1.0)
        self.play(
            FadeOut(block_heading),
            FadeOut(col.all),
            FadeOut(self.figure_group),
            run_time=MOTION_EXIT,
        )

    # ── Scene 06 — Dấu hiệu 6a (Hình 36) ─────────────────────────────────

    def scene06_dauHieu6a(self):
        block_heading = self._block_heading(r"\textbf{Dấu hiệu 6 — a)}")
        self.play(Write(block_heading), run_time=MOTION_ENTER)

        col = TheoryColumn(block_heading, has_figure=True)

        line1 = Tex(
            r"Cho hai góc kề $A\widehat{O}B$ và $A\widehat{O}C$.",
            tex_template=viet_tex_template,
            font_size=26,
        )
        line2 = Tex(
            r"Nếu $A\widehat{O}B + A\widehat{O}C \leq 180^\circ$ thì tia $OA$ nằm giữa hai tia $OB$ và $OC$.",
            tex_template=viet_tex_template,
            font_size=26,
        )
        col.place(line1)
        col.place(line2)

        formula_leq = MathTex(
            r"A\widehat{O}B + A\widehat{O}C \leq 180^\circ",
            tex_template=viet_tex_template,
            font_size=34,
        )
        col.place_formula(formula_leq)

        self.fig36 = _build_multi_ray(
            [("A", 0), ("B", 40), ("C", 320)],
            angle_pairs=[(0, 40, 0.5, "1"), (0, 320, 0.55, "2")],
        )
        self.figure_group = self.fig36["group"]
        rays = self.fig36["rays"]
        ang_mobs = self.fig36["angle_mobs"]
        ray_labels = VGroup(*self.fig36["labels"])

        with self.voiceover(
            text=(
                "Dấu hiệu sáu, phần a. "
                "Cho hai góc kề A O B và A O C. "
                "Nếu tổng hai góc không quá 180 độ "
                "thì tia O A nằm giữa hai tia O B và O C."
            )
        ) as ov:
            self.play(
                Create(rays["A"]),
                FadeIn(self.fig36["dot_O"]),
                Write(self.fig36["label_O"]),
                Write(ray_labels),
                run_time=ov.duration * 0.15,
            )
            self.play(
                Create(rays["B"]),
                Create(rays["C"]),
                run_time=ov.duration * 0.25,
            )
            self.play(FadeIn(line1), FadeIn(line2), run_time=ov.duration * 0.25)
            self.play(Create(ang_mobs[0]), Create(ang_mobs[1]), run_time=ov.duration * 0.20)
            self.play(Write(formula_leq), run_time=ov.duration * 0.15)

        with self.voiceover(
            text=(
                "Trên hình, hai góc kề có tổng không quá 180 độ, "
                "nên O A nằm giữa O B và O C."
            )
        ) as ov:
            self.play(
                Indicate(ang_mobs, scale_factor=EMPHASIS_SCALE, color=EMPHASIS_COLOR),
                run_time=ov.duration * 0.45,
            )
            self.play(
                Indicate(rays["A"], color=EMPHASIS_COLOR, scale_factor=EMPHASIS_SCALE),
                run_time=ov.duration * 0.55,
            )

        self.wait(1.0)
        self.play(
            FadeOut(block_heading),
            FadeOut(col.all),
            FadeOut(formula_leq),
            FadeOut(self.figure_group),
            run_time=MOTION_EXIT,
        )

    # ── Scene 07 — Dấu hiệu 6b (Hình 37) ─────────────────────────────────

    def scene07_dauHieu6b(self):
        block_heading = self._block_heading(r"\textbf{Dấu hiệu 6 — b)}")
        self.play(Write(block_heading), run_time=MOTION_ENTER)

        col = TheoryColumn(block_heading, has_figure=True)

        line1 = Tex(
            r"Nếu $A\widehat{O}B + A\widehat{O}C > 180^\circ$ thì tia $OA$ không nằm giữa hai tia $OB$ và $OC$.",
            tex_template=viet_tex_template,
            font_size=26,
        )
        line2 = Tex(
            r"Tia đối $OA'$ của tia $OA$ nằm giữa hai tia $OB$ và $OC$.",
            tex_template=viet_tex_template,
            font_size=26,
        )
        col.place(line1)
        col.place(line2)

        formula_gt = MathTex(
            r"A\widehat{O}B + A\widehat{O}C > 180^\circ",
            tex_template=viet_tex_template,
            font_size=34,
        )
        col.place_formula(formula_gt)

        self.fig37 = _build_multi_ray(
            [("A", 0), ("B", 135), ("C", 225)],
            angle_pairs=[(0, 135, 0.55, "1"), (0, 225, 0.6, "2")],
        )
        self.figure_group = self.fig37["group"]
        rays = self.fig37["rays"]
        ang_mobs = self.fig37["angle_mobs"]
        ray_labels = VGroup(*self.fig37["labels"])

        with self.voiceover(
            text=(
                "Dấu hiệu sáu, phần b. "
                "Nếu tổng hai góc A O B và A O C "
                "lớn hơn 180 độ "
                "thì tia O A không nằm giữa hai tia O B và O C."
            )
        ) as ov:
            self.play(
                Create(rays["A"]),
                Create(rays["B"]),
                Create(rays["C"]),
                FadeIn(self.fig37["dot_O"]),
                Write(self.fig37["label_O"]),
                Write(ray_labels),
                run_time=ov.duration * 0.30,
            )
            self.play(Create(ang_mobs[0]), Create(ang_mobs[1]), run_time=ov.duration * 0.25)
            self.play(FadeIn(line1), Write(formula_gt), run_time=ov.duration * 0.45)

        self.play(
            Indicate(rays["A"], color=COLOR_DEFAULT, scale_factor=EMPHASIS_SCALE),
            run_time=EMPHASIS_INDICATE_TIME,
        )

        o = self.fig37["dot_O"].get_center()
        ray_OAp, tip_ap = _make_ray(180, origin=o)
        label_Ap = _label_math("A'", tip_ap, LEFT)

        with self.voiceover(
            text=(
                "Tia đối O A phẩy của tia O A "
                "nằm giữa hai tia O B và O C. "
                "Trên hình, tổng hai góc lớn hơn 180 độ; "
                "tia đối O A phẩy nằm giữa O B và O C."
            )
        ) as ov:
            self.play(FadeIn(line2), run_time=ov.duration * 0.15)
            self.play(Create(ray_OAp), Write(label_Ap), run_time=ov.duration * 0.35)
            self.play(
                Indicate(VGroup(ray_OAp, label_Ap), color=EMPHASIS_COLOR, scale_factor=EMPHASIS_SCALE),
                run_time=ov.duration * 0.50,
            )

        self.wait(1.5)
        self.play(
            FadeOut(block_heading),
            FadeOut(col.all),
            FadeOut(formula_gt),
            FadeOut(self.figure_group),
            FadeOut(ray_OAp),
            FadeOut(label_Ap),
            FadeOut(self.section_heading),
            FadeOut(self.lesson_title),
            run_time=MOTION_EXIT,
        )
