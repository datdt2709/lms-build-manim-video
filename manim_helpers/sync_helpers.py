"""sync_<type> helpers – đồng bộ bookmark + AddTextLetterByLetter proof token + visual effect.

Mỗi voiceover block đặt nhiều bookmark (1 bookmark / thực thể). Trong code,
sau `self.voiceover(text=...)` ta KHÔNG viết tay `wait_until_bookmark` +
`AddTextLetterByLetter` + `Indicate / FadeIn`, mà gọi 1 trong các sync_* phù hợp với loại
thực thể:

    sync_point        – cho điểm
    sync_segment      – cho đoạn thẳng
    sync_angle        – cho góc (Sector / AngleMarker)
    sync_right_angle  – cho góc vuông (RightAngle đã có sẵn, tô fill + stroke)
    sync_triangle     – cho tam giác (Polygon fill tạm)
    sync_quadrilateral– cho tứ giác
    sync_relation     – cho từ kết nối ('=', '⇒', '(c.g.c)', ...) – không có shape

Mỗi hàm:
    1. scene.wait_until_bookmark(bookmark)
    2. scene.play(tex_anim, run_time=write_time)  -- AddTextLetterByLetter proof token
    3. scene.play(<effect>, run_time=indicate/fade_time)  -- visual highlight

Effect chuẩn:
    sync_segment   : seg.animate.set_stroke(color, width=10)  rate=there_and_back
    sync_triangle  : tri.animate.set_fill(color, opacity)     rate=there_and_back
    sync_angle     : FadeIn(sector); KHÔNG tự FadeOut – cần geo.cleanup_temp() hoặc
                     FadeOut tay sau khi hết block (xem manim-geometry-engine).
    sync_point     : Indicate(dot, scale_factor=1.8, color=color)
    sync_relation  : chỉ Write, không có shape effect.
"""

from __future__ import annotations

from typing import Optional

from manim import (
    FadeIn,
    Indicate,
    there_and_back,
)

from .geo_engine import right_angle_square_fill_polygon
from .visual_tokens import (
    COLOR_ACTIVE,
    COLOR_EQUAL_1,
    COLOR_EQUAL_3,
    STATE_HIGHLIGHT,
    TIMING_ANGLE,
    TIMING_INDICATE_SEGMENT,
    TIMING_INDICATE_TRIANGLE,
    TIMING_POINT,
    TIMING_RELATION,
)


# ---------------------------------------------------------------------------
# Helper nội bộ
# ---------------------------------------------------------------------------

def _wait_and_write(scene, bookmark: Optional[str], tex_anim, write_time: float):
    """Wait until bookmark (nếu có) rồi play AddTextLetterByLetter tex_anim."""
    if bookmark is not None:
        scene.wait_until_bookmark(bookmark)
    if tex_anim is not None:
        scene.play(tex_anim, run_time=write_time)


# ---------------------------------------------------------------------------
# sync_point
# ---------------------------------------------------------------------------

def sync_point(
    scene,
    bookmark: Optional[str],
    tex_anim,
    dot,
    *,
    write_time: float = TIMING_RELATION,
    indicate_time: float = TIMING_POINT,
    color: str = COLOR_ACTIVE,
    scale_factor: float = 1.8,
):
    """Đồng bộ AddTextLetterByLetter proof token + Indicate dot điểm."""
    _wait_and_write(scene, bookmark, tex_anim, write_time)
    scene.play(
        Indicate(dot, color=color, scale_factor=scale_factor),
        run_time=indicate_time,
    )


# ---------------------------------------------------------------------------
# sync_segment
# ---------------------------------------------------------------------------

def sync_segment(
    scene,
    bookmark: Optional[str],
    tex_anim,
    seg,
    *,
    write_time: float = TIMING_RELATION,
    indicate_time: float = TIMING_INDICATE_SEGMENT,
    color: str = COLOR_ACTIVE,
    stroke_width: float = 10.0,
):
    """Đồng bộ AddTextLetterByLetter proof token + highlight cạnh (set_stroke there_and_back).

    Effect không phá vỡ stroke gốc của seg vì rate_func=there_and_back trả lại
    state ban đầu sau animation.
    """
    _wait_and_write(scene, bookmark, tex_anim, write_time)
    scene.play(
        seg.animate.set_stroke(color=color, width=stroke_width),
        run_time=indicate_time,
        rate_func=there_and_back,
    )


# ---------------------------------------------------------------------------
# sync_angle
# ---------------------------------------------------------------------------

def sync_angle(
    scene,
    bookmark: Optional[str],
    tex_anim,
    sector,
    *,
    write_time: float = TIMING_RELATION,
    fade_time: float = TIMING_ANGLE,
):
    """Đồng bộ AddTextLetterByLetter proof token + FadeIn sector góc.

    LƯU Ý: KHÔNG tự FadeOut. Caller phải FadeOut sau khi hết voiceover block,
    hoặc dùng GeometryEngine.cleanup_temp() để clear toàn bộ marker tạm.
    """
    _wait_and_write(scene, bookmark, tex_anim, write_time)
    scene.play(FadeIn(sector), run_time=fade_time)


# ---------------------------------------------------------------------------
# sync_right_angle
# ---------------------------------------------------------------------------

def sync_right_angle(
    scene,
    bookmark: Optional[str],
    tex_anim,
    ra,
    *,
    geo=None,
    color: str = COLOR_EQUAL_1,
    fill_opacity: float = 0.55,
    stroke_width: float = STATE_HIGHLIGHT["stroke_width"],
    write_time: float = TIMING_RELATION,
    fade_time: float = TIMING_ANGLE,
):
    """Đồng bộ AddTextLetterByLetter proof token + highlight RightAngle (Polygon đủ ô + stroke).

    Truyền `geo=self.geo` để `patch` được track vào `geo._temp_ra_revert` và
    `geo.cleanup_temp()` có thể FadeOut patch + revert stroke tự động. Nếu
    không truyền `geo`, caller phải FadeOut patch + revert stroke tay.
    """
    _wait_and_write(scene, bookmark, tex_anim, write_time)
    patch = right_angle_square_fill_polygon(ra, color=color, fill_opacity=0.0)
    scene.add(patch)
    if geo is not None:
        geo._temp_ra_revert.append(
            (ra, ra.get_stroke_color(), ra.get_stroke_width(), patch)
        )
    scene.play(
        ra.animate.set_stroke(color=color, width=stroke_width),
        patch.animate.set_fill(opacity=fill_opacity),
        run_time=fade_time,
    )


# ---------------------------------------------------------------------------
# sync_triangle
# ---------------------------------------------------------------------------

def sync_triangle(
    scene,
    bookmark: Optional[str],
    tex_anim,
    tri_fill,
    *,
    write_time: float = TIMING_RELATION,
    indicate_time: float = TIMING_INDICATE_TRIANGLE,
    color: str = COLOR_EQUAL_3,
    fill_opacity: float = 0.35,
):
    """Đồng bộ AddTextLetterByLetter proof token + highlight tam giác (set_fill there_and_back)."""
    _wait_and_write(scene, bookmark, tex_anim, write_time)
    scene.play(
        tri_fill.animate.set_fill(color=color, opacity=fill_opacity)
        .set_stroke(color=color, width=2.5),
        run_time=indicate_time,
        rate_func=there_and_back,
    )


# ---------------------------------------------------------------------------
# sync_quadrilateral
# ---------------------------------------------------------------------------

def sync_quadrilateral(
    scene,
    bookmark: Optional[str],
    tex_anim,
    quad_fill,
    *,
    write_time: float = TIMING_RELATION,
    indicate_time: float = TIMING_INDICATE_TRIANGLE,
    color: str = COLOR_EQUAL_3,
    fill_opacity: float = 0.30,
):
    """Đồng bộ AddTextLetterByLetter proof token + highlight tứ giác."""
    _wait_and_write(scene, bookmark, tex_anim, write_time)
    scene.play(
        quad_fill.animate.set_fill(color=color, opacity=fill_opacity)
        .set_stroke(color=color, width=2.5),
        run_time=indicate_time,
        rate_func=there_and_back,
    )


# ---------------------------------------------------------------------------
# sync_relation – cho '=', '⇒', '(c.g.c)', ... — chỉ Write, không có shape
# ---------------------------------------------------------------------------

def sync_relation(
    scene,
    bookmark: Optional[str],
    tex_anim,
    *,
    write_time: float = TIMING_RELATION,
):
    """Đồng bộ AddTextLetterByLetter 1 token quan hệ ('=', '⇒', '(c.g.c)') – không có shape."""
    _wait_and_write(scene, bookmark, tex_anim, write_time)


__all__ = [
    "sync_point",
    "sync_segment",
    "sync_angle",
    "sync_right_angle",
    "sync_triangle",
    "sync_quadrilateral",
    "sync_relation",
]


# Re-export thường dùng để giúp pop-up IDE
_REEXPORT_COLORS = (COLOR_ACTIVE, COLOR_EQUAL_1, COLOR_EQUAL_3)  # noqa: F841
