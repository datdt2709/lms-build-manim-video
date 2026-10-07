"""Geometry engine – AngleMarker và GeometryEngine registry.

Module này gom toàn bộ boilerplate hình học hay lặp:

    - line_intersection(line1_points, line2_points)
    - cross2d(v1, v2), angle_between_vectors(v1, v2)
    - AngleMarker(A, O, B, color, ...) -> Sector tự tính start_angle / angle / dấu
    - GeometryEngine: registry-based wrapper trên Scene để register dot / seg /
      ang / tri / quad theo tên semantic, sau đó gọi `geo.highlight_segment(...)`,
      `geo.show_segment_equal(...)`, `geo.show_congruence(...)` v.v.

Quy ước màu (rule 5) được code-hóa:
    - show_*_equal(...)        -> 1 màu duy nhất cho mọi đối tượng (chỉ ra "bằng nhau")
    - show_congruence(...)     -> 2 màu khác nhau (so sánh hai tam giác)
    - compare_*(...)           -> 2+ màu khác nhau (phân biệt nhiều thực thể)
"""

from __future__ import annotations

from typing import Dict, Iterable, List, Optional, Sequence

import numpy as np
from manim import (
    Dot,
    FadeIn,
    FadeOut,
    Indicate,
    Line,
    MathTex,
    Polygon,
    RightAngle,
    Sector,
    VGroup,
    there_and_back,
)

from .visual_tokens import (
    COLOR_ACTIVE,
    COLOR_AUX_LINE,
    COLOR_EQUAL_1,
    COLOR_EQUAL_2,
    COLOR_EQUAL_3,
    COLOR_DEFAULT,
    STATE_HIGHLIGHT,
    STATE_EQUAL,
    LAYER_GEOMETRY,
    LAYER_MARKERS,
    TIMING_ANGLE,
    TIMING_FADE,
    TIMING_INDICATE_SEGMENT,
    TIMING_INDICATE_TRIANGLE,
    TIMING_POINT,
)


# ---------------------------------------------------------------------------
# Module-level helpers (rule 9)
# ---------------------------------------------------------------------------

def line_intersection(line1_points, line2_points):
    """Tính tọa độ giao điểm của hai đường thẳng đi qua 2 điểm.

    Trả về np.ndarray [x, y, 0] hoặc None nếu hai đường song song.
    """
    p1, p2 = line1_points
    p3, p4 = line2_points
    dx1, dy1 = p2[0] - p1[0], p2[1] - p1[1]
    dx2, dy2 = p4[0] - p3[0], p4[1] - p3[1]
    D = dx1 * dy2 - dy1 * dx2
    if D == 0:
        return None
    t = ((p3[0] - p1[0]) * dy2 - (p3[1] - p1[1]) * dx2) / D
    return np.array([p1[0] + t * dx1, p1[1] + t * dy1, 0])


def cross2d(v1, v2) -> float:
    """Cross product 2D (v1.x * v2.y - v1.y * v2.x)."""
    return v1[0] * v2[1] - v1[1] * v2[0]


def angle_between_vectors(v1, v2) -> float:
    """Góc không dấu giữa 2 vector 2D, radian, trong [0, pi]."""
    n1 = np.linalg.norm(v1[:2])
    n2 = np.linalg.norm(v2[:2])
    if n1 == 0 or n2 == 0:
        return 0.0
    cos = float(np.dot(v1[:2], v2[:2]) / (n1 * n2))
    cos = max(-1.0, min(1.0, cos))
    return float(np.arccos(cos))


def _compute_right_angle_square_vertices(ra: RightAngle) -> np.ndarray:
    """Bốn đỉnh hình vuông tại góc vuông (đỉnh + 3 góc của ký hiệu L).

    Manim `RightAngle` chỉ vẽ polyline 3 điểm; `set_fill` đóng path nên chỉ tô
    được một tam giác. Polygon đủ 4 đỉnh mới tô kín cả ô vuông.
    """
    line1, line2 = ra.get_lines()[0], ra.get_lines()[1]
    inter = line_intersection(
        [line1.get_start(), line1.get_end()],
        [line2.get_start(), line2.get_end()],
    )
    if inter is None:
        raise ValueError("RightAngle: hai cạnh không cắt nhau, không tính được ô vuông.")
    quadrant = ra.quadrant
    radius = getattr(ra, "radius", None)
    if radius is None:
        if quadrant[0] == 1:
            dist_1 = float(np.linalg.norm(line1.get_end() - inter))
        else:
            dist_1 = float(np.linalg.norm(line1.get_start() - inter))
        if quadrant[1] == 1:
            dist_2 = float(np.linalg.norm(line2.get_end() - inter))
        else:
            dist_2 = float(np.linalg.norm(line2.get_start() - inter))
        if min(dist_1, dist_2) < 0.6:
            radius = (2.0 / 3.0) * min(dist_1, dist_2)
        else:
            radius = 0.4
    u1 = quadrant[0] * radius * line1.get_unit_vector()
    u2 = quadrant[1] * radius * line2.get_unit_vector()
    anchor_angle_1 = inter + u1
    anchor_angle_2 = inter + u2
    anchor_middle = inter + u1 + u2
    return np.array([inter, anchor_angle_1, anchor_middle, anchor_angle_2])


def right_angle_square_fill_polygon(
    ra: RightAngle,
    *,
    color: str = COLOR_EQUAL_1,
    fill_opacity: float = 0.0,
) -> Polygon:
    """Polygon đủ bốn đỉnh phía sau ký hiệu L; không stroke; z nhẹ hơn `ra`."""
    verts = _compute_right_angle_square_vertices(ra)
    poly = Polygon(
        *verts,
        fill_color=color,
        fill_opacity=fill_opacity,
        stroke_width=0,
    )
    z = ra.get_z_index()
    poly.set_z_index(z - 1)
    return poly


# ---------------------------------------------------------------------------
# AngleMarker – Sector với start_angle / angle / dấu xoay tự tính
# ---------------------------------------------------------------------------

def AngleMarker(
    A,
    O,
    B,
    *,
    color: str = COLOR_ACTIVE,
    radius: float = 0.32,
    stroke_width: float = 2.0,
    fill_opacity: float = 0.4,
) -> Sector:
    """Tạo Sector biểu thị góc AOB tại đỉnh O.

    Tự tính:
        - start_angle = arctan2(OA.y, OA.x)
        - angle = arccos(OA.OB / |OA||OB|), có dấu theo cross2d(OA, OB)

    Loại bỏ hoàn toàn boilerplate `v1 = .. v2 = .. cross2d ..` mỗi project.
    """
    O = np.asarray(O, dtype=float)
    A = np.asarray(A, dtype=float)
    B = np.asarray(B, dtype=float)
    v1 = A - O
    v2 = B - O
    start = float(np.arctan2(v1[1], v1[0]))
    ang = angle_between_vectors(v1, v2)
    if cross2d(v1, v2) < 0:
        ang = -ang
    sector = Sector(
        arc_center=O,
        radius=radius,
        start_angle=start,
        angle=ang,
        fill_color=color,
        fill_opacity=fill_opacity,
        stroke_color=color,
        stroke_width=stroke_width,
    )
    sector.set_z_index(LAYER_MARKERS)
    return sector


# ---------------------------------------------------------------------------
# GeometryEngine
# ---------------------------------------------------------------------------

# Bảng màu mặc định khi cần "n thực thể khác nhau"
_PALETTE_DISTINCT = (COLOR_EQUAL_1, COLOR_EQUAL_2, COLOR_EQUAL_3)


class GeometryEngine:
    """Registry các thực thể hình học theo tên semantic + helper highlight.

    Cách dùng:
        geo = GeometryEngine(self)
        geo.register_point("A", A_pos, color=COLOR_DEFAULT, label_dir=UL)
        geo.register_point("B", B_pos)
        geo.register_segment("AB", "A", "B", color=COLOR_DEFAULT)
        geo.register_triangle("OFB", ["O", "F", "B"])

        geo.highlight_segment("AB")
        geo.highlight_angle("OFB", color=COLOR_EQUAL_1)
        geo.show_segment_equal("BF", "FC")           # cùng màu
        geo.show_angle_equal("OFB", "OFC")           # cùng màu
        geo.show_congruence("OFB", "OFC", criterion="c.g.c")  # 2 màu khác nhau
        geo.cleanup_temp()                           # xoá mọi marker tạm
    """

    def __init__(self, scene):
        self.scene = scene
        self._points: Dict[str, np.ndarray] = {}
        self._dots: Dict[str, Dot] = {}
        self._labels: Dict[str, MathTex] = {}
        self._segments: Dict[str, Line] = {}
        self._triangle_pts: Dict[str, List[str]] = {}
        self._quad_pts: Dict[str, List[str]] = {}
        self._triangle_fills: Dict[str, Polygon] = {}
        self._temp_markers: List = []
        self._right_angles: Dict[str, RightAngle] = {}
        self._temp_ra_revert: List = []

    # ------------------------------------------------------------------
    # Register API
    # ------------------------------------------------------------------

    def register_point(
        self,
        name: str,
        pos,
        *,
        dot: Optional[Dot] = None,
        label: Optional[MathTex] = None,
    ) -> Dot:
        """Đăng ký 1 điểm theo tên semantic; trả về Dot.

        Nếu `dot=None` thì engine không tạo Dot; caller chịu trách nhiệm
        Create dot riêng (vì màu/style riêng theo từng project). Engine chỉ
        nhớ vị trí + reference Dot đã có.
        """
        self._points[name] = np.asarray(pos, dtype=float)
        if dot is not None:
            self._dots[name] = dot
        if label is not None:
            self._labels[name] = label
        return dot

    def register_segment(self, name: str, line: Line) -> Line:
        """Đăng ký 1 segment đã được tạo sẵn."""
        self._segments[name] = line
        return line

    def register_triangle(self, name: str, vertex_names: Sequence[str]) -> None:
        """Đăng ký tam giác theo 3 tên điểm đã register."""
        if len(vertex_names) != 3:
            raise ValueError("Triangle cần 3 điểm.")
        for v in vertex_names:
            if v not in self._points:
                raise KeyError(f"Điểm {v!r} chưa register.")
        self._triangle_pts[name] = list(vertex_names)

    def register_quadrilateral(self, name: str, vertex_names: Sequence[str]) -> None:
        if len(vertex_names) != 4:
            raise ValueError("Quadrilateral cần 4 điểm.")
        for v in vertex_names:
            if v not in self._points:
                raise KeyError(f"Điểm {v!r} chưa register.")
        self._quad_pts[name] = list(vertex_names)

    def register_triangle_fill(
        self,
        name: str,
        *,
        color: str = COLOR_EQUAL_3,
        fill_opacity: float = 0.0,
    ) -> Polygon:
        """Tạo Polygon fill cho tam giác đã register; lưu vào registry và scene.

        Mặc định fill_opacity=0 → invisible cho đến khi sync_triangle()
        gọi animate.set_fill().
        """
        verts = self._triangle_pts[name]
        pts = [self._points[v] for v in verts]
        poly = Polygon(
            *pts,
            fill_color=color,
            fill_opacity=fill_opacity,
            stroke_color=color,
            stroke_width=0,
        )
        poly.set_z_index(LAYER_GEOMETRY)
        self._triangle_fills[name] = poly
        return poly

    def register_right_angle(self, name: str, ra: RightAngle) -> RightAngle:
        """Đăng ký 1 RightAngle đã tạo theo tên semantic."""
        self._right_angles[name] = ra
        return ra

    def get_missing_sides(self, shape_name: str) -> List[tuple[str, str]]:
        """Các cạnh (v1, v2) của tam giác / tứ giác đã register mà chưa có trong `_segments`.

        Kiểm tra cả hai chiều (AB và BA). Dùng trước `sync_triangle` / `sync_quadrilateral`
        hoặc `highlight_*` để tránh cạnh chỉ flash rồi biến mất vì chưa `Create` vĩnh viễn.
        """
        if shape_name in self._triangle_pts:
            verts = self._triangle_pts[shape_name]
        elif shape_name in self._quad_pts:
            verts = self._quad_pts[shape_name]
        else:
            return []
        n = len(verts)
        missing: List[tuple[str, str]] = []
        for i in range(n):
            v1, v2 = verts[i], verts[(i + 1) % n]
            if v1 + v2 not in self._segments and v2 + v1 not in self._segments:
                missing.append((v1, v2))
        return missing

    def create_missing_sides(
        self,
        shape_name: str,
        *,
        color: str = COLOR_AUX_LINE,
    ) -> List[tuple[str, Line]]:
        """Tạo `Line` cho từng cạnh thiếu, `register_segment` theo tên `v1+v2`, trả về list.

        Caller gọi `Create` / `FadeIn` và `persistent_geom.add(...)` nếu cần giữ trên diagram.
        """
        result: List[tuple[str, Line]] = []
        for v1, v2 in self.get_missing_sides(shape_name):
            p1, p2 = self._points[v1], self._points[v2]
            seg = Line(p1, p2, color=color).set_z_index(LAYER_GEOMETRY)
            seg_name = v1 + v2
            self._segments[seg_name] = seg
            result.append((seg_name, seg))
        return result

    def ensure_angle_sides(
        self,
        vertex: str,
        pt1: str,
        pt2: str,
        *,
        color: str = COLOR_AUX_LINE,
    ) -> List[tuple[str, Line]]:
        """Tạo và register các cạnh vertex–pt1, vertex–pt2 còn thiếu cho góc tự do.

        Dùng khi góc tạo bởi hai điểm không thuộc cùng một tam giác đã register
        (không thể dùng `create_missing_sides`). Kiểm tra cả hai chiều tên cạnh.

        Trả về list (seg_name, Line) cho các cạnh thực sự mới tạo.
        Caller gọi `Create` / `FadeIn` và `persistent_geom.add(...)` để giữ trên diagram.
        """
        result: List[tuple[str, Line]] = []
        for a, b in [(vertex, pt1), (vertex, pt2)]:
            if a + b not in self._segments and b + a not in self._segments:
                seg = Line(self._points[a], self._points[b], color=color)
                seg.set_z_index(LAYER_GEOMETRY)
                self._segments[a + b] = seg
                result.append((a + b, seg))
        return result

    # ------------------------------------------------------------------
    # Lookup
    # ------------------------------------------------------------------

    def point(self, name: str) -> np.ndarray:
        return self._points[name]

    def segment(self, name: str) -> Line:
        return self._segments[name]

    def triangle_fill(self, name: str) -> Polygon:
        return self._triangle_fills[name]

    def right_angle(self, name: str) -> RightAngle:
        return self._right_angles[name]

    # ------------------------------------------------------------------
    # Highlight API
    # ------------------------------------------------------------------

    def highlight_point(
        self,
        name: str,
        *,
        color: str = COLOR_ACTIVE,
        scale_factor: float = 1.8,
        run_time: float = TIMING_POINT,
    ):
        dot = self._dots[name]
        self.scene.play(
            Indicate(dot, color=color, scale_factor=scale_factor),
            run_time=run_time,
        )

    def highlight_segment(
        self,
        name: str,
        *,
        color: str = COLOR_ACTIVE,
        stroke_width: float = STATE_HIGHLIGHT["stroke_width"],
        run_time: float = TIMING_INDICATE_SEGMENT,
    ):
        seg = self._segments[name]
        self.scene.play(
            seg.animate.set_stroke(color=color, width=stroke_width),
            run_time=run_time,
            rate_func=there_and_back,
        )

    def highlight_angle(
        self,
        triangle_name: str,
        *,
        vertex_index: int = 1,
        color: str = COLOR_EQUAL_1,
        radius: float = 0.32,
        run_time: float = TIMING_ANGLE,
    ):
        """Highlight góc tại đỉnh `vertex_index` của tam giác (mặc định đỉnh giữa).

        Ví dụ tri_OFB → vertex_index=1 → góc tại F (∠OFB).
        Sector được FadeIn rồi track vào temp_markers.
        """
        verts = self._triangle_pts[triangle_name]
        if not (0 <= vertex_index < 3):
            raise ValueError("vertex_index phải 0/1/2")
        v_left = verts[(vertex_index - 1) % 3]
        v_apex = verts[vertex_index]
        v_right = verts[(vertex_index + 1) % 3]
        sec = AngleMarker(
            self._points[v_left],
            self._points[v_apex],
            self._points[v_right],
            color=color,
            radius=radius,
        )
        self.scene.play(FadeIn(sec), run_time=run_time)
        self._temp_markers.append(sec)
        return sec

    def highlight_right_angle(
        self,
        name: str,
        *,
        color: str = COLOR_EQUAL_1,
        fill_opacity: float = 0.55,
        stroke_width: float = STATE_HIGHLIGHT["stroke_width"],
        run_time: float = TIMING_ANGLE,
    ):
        """Stroke trên RightAngle + Polygon 4 đỉnh (tô kín ô vuông); cleanup_temp revert."""
        ra = self._right_angles[name]
        patch = right_angle_square_fill_polygon(ra, color=color, fill_opacity=0.0)
        self.scene.add(patch)
        self._temp_ra_revert.append(
            (ra, ra.get_stroke_color(), ra.get_stroke_width(), patch)
        )
        self.scene.play(
            ra.animate.set_stroke(color=color, width=stroke_width),
            patch.animate.set_fill(opacity=fill_opacity),
            run_time=run_time,
        )

    def highlight_triangle(
        self,
        name: str,
        *,
        color: str = COLOR_EQUAL_3,
        fill_opacity: float = 0.35,
        run_time: float = TIMING_INDICATE_TRIANGLE,
    ):
        """Highlight tam giác bằng Polygon fill there_and_back.

        Tự tạo poly nếu chưa register fill.
        """
        if name not in self._triangle_fills:
            self.register_triangle_fill(name, color=color, fill_opacity=0.0)
            self.scene.add(self._triangle_fills[name])
        poly = self._triangle_fills[name]
        self.scene.play(
            poly.animate.set_fill(color=color, opacity=fill_opacity).set_stroke(
                color=color, width=STATE_EQUAL["stroke_width"]
            ),
            run_time=run_time,
            rate_func=there_and_back,
        )

    # ------------------------------------------------------------------
    # show_*_equal / show_congruence – mã hoá rule màu (rule 5)
    # ------------------------------------------------------------------

    def show_segment_equal(
        self,
        *seg_names: str,
        color: str = COLOR_EQUAL_1,
        run_time: float = TIMING_INDICATE_SEGMENT,
    ):
        """Highlight nhiều đoạn bằng nhau – CÙNG 1 màu (rule 5)."""
        if len(seg_names) < 2:
            raise ValueError("show_segment_equal cần ≥ 2 đoạn.")
        anims = []
        for n in seg_names:
            seg = self._segments[n]
            anims.append(seg.animate.set_stroke(color=color, width=STATE_HIGHLIGHT["stroke_width"]))
        self.scene.play(*anims, run_time=run_time, rate_func=there_and_back)

    def show_angle_equal(
        self,
        *triangle_names: str,
        vertex_index: int = 1,
        color: str = COLOR_EQUAL_1,
        radius: float = 0.32,
        run_time: float = TIMING_ANGLE,
    ):
        """Highlight nhiều góc bằng nhau – CÙNG 1 màu (rule 5).

        Mỗi triangle_name dùng `vertex_index` để xác định đỉnh của góc.
        """
        if len(triangle_names) < 2:
            raise ValueError("show_angle_equal cần ≥ 2 góc.")
        sectors = []
        for tn in triangle_names:
            verts = self._triangle_pts[tn]
            if not (0 <= vertex_index < 3):
                raise ValueError("vertex_index phải 0/1/2")
            v_left = verts[(vertex_index - 1) % 3]
            v_apex = verts[vertex_index]
            v_right = verts[(vertex_index + 1) % 3]
            sec = AngleMarker(
                self._points[v_left],
                self._points[v_apex],
                self._points[v_right],
                color=color,
                radius=radius,
            )
            sectors.append(sec)
        self.scene.play(*[FadeIn(s) for s in sectors], run_time=run_time)
        self._temp_markers.extend(sectors)
        return sectors

    def show_right_angle_equal(
        self,
        *names: str,
        color: str = COLOR_EQUAL_1,
        fill_opacity: float = 0.55,
        stroke_width: float = STATE_HIGHLIGHT["stroke_width"],
        run_time: float = TIMING_ANGLE,
    ):
        """Highlight ≥ 2 RightAngle bằng nhau – CÙNG 1 màu (rule 5)."""
        if len(names) < 2:
            raise ValueError("show_right_angle_equal cần ≥ 2 góc vuông.")
        anims = []
        for n in names:
            ra = self._right_angles[n]
            patch = right_angle_square_fill_polygon(ra, color=color, fill_opacity=0.0)
            self.scene.add(patch)
            self._temp_ra_revert.append(
                (ra, ra.get_stroke_color(), ra.get_stroke_width(), patch)
            )
            anims.append(ra.animate.set_stroke(color=color, width=stroke_width))
            anims.append(patch.animate.set_fill(opacity=fill_opacity))
        self.scene.play(*anims, run_time=run_time)

    def show_congruence(
        self,
        tri_a: str,
        tri_b: str,
        *,
        criterion: str = "c.g.c",
        color_a: str = COLOR_EQUAL_1,
        color_b: str = COLOR_EQUAL_2,
        run_time: float = TIMING_INDICATE_TRIANGLE,
    ):
        """Highlight 2 tam giác đồng dạng / bằng nhau – HAI màu khác nhau (rule 5).

        Lần lượt set_fill cho hai tam giác (rate_func=there_and_back) để học sinh
        thấy rõ hai tam giác riêng biệt, không bị nhầm là "cùng 1 thực thể".

        `criterion` chỉ là metadata (hiển thị trong proof) – engine không tự render.
        """
        for n, c in ((tri_a, color_a), (tri_b, color_b)):
            if n not in self._triangle_fills:
                self.register_triangle_fill(n, color=c, fill_opacity=0.0)
                self.scene.add(self._triangle_fills[n])

        self.scene.play(
            self._triangle_fills[tri_a]
            .animate.set_fill(color=color_a, opacity=0.32)
            .set_stroke(color=color_a, width=STATE_EQUAL["stroke_width"]),
            run_time=run_time,
            rate_func=there_and_back,
        )
        self.scene.play(
            self._triangle_fills[tri_b]
            .animate.set_fill(color=color_b, opacity=0.32)
            .set_stroke(color=color_b, width=STATE_EQUAL["stroke_width"]),
            run_time=run_time,
            rate_func=there_and_back,
        )

    def compare_triangles(
        self,
        *tri_names: str,
        palette: Sequence[str] = _PALETTE_DISTINCT,
        run_time: float = TIMING_INDICATE_TRIANGLE,
    ):
        """Highlight nhiều tam giác phân biệt – mỗi tam giác 1 màu (rule 5)."""
        if len(tri_names) < 2:
            raise ValueError("compare_triangles cần ≥ 2 tam giác.")
        for i, tn in enumerate(tri_names):
            color = palette[i % len(palette)]
            if tn not in self._triangle_fills:
                self.register_triangle_fill(tn, color=color, fill_opacity=0.0)
                self.scene.add(self._triangle_fills[tn])
            self.scene.play(
                self._triangle_fills[tn]
                .animate.set_fill(color=color, opacity=0.32)
                .set_stroke(color=color, width=STATE_EQUAL["stroke_width"]),
                run_time=run_time,
                rate_func=there_and_back,
            )

    # ------------------------------------------------------------------
    # Cleanup
    # ------------------------------------------------------------------

    def cleanup_temp(self, *, run_time: float = TIMING_FADE):
        """FadeOut marker tạm; revert RightAngle đã highlight về stroke/fill gốc."""
        if not self._temp_markers and not self._temp_ra_revert:
            return
        anims = [FadeOut(m) for m in self._temp_markers]
        for entry in self._temp_ra_revert:
            if len(entry) == 4:
                ra, orig_color, orig_stroke, patch = entry
            else:
                ra, orig_color, orig_stroke = entry
                patch = None
            anims.append(
                ra.animate.set_stroke(color=orig_color, width=orig_stroke)
            )
            if patch is not None:
                anims.append(FadeOut(patch))
        self.scene.play(*anims, run_time=run_time)
        self._temp_markers.clear()
        self._temp_ra_revert.clear()


__all__ = [
    "line_intersection",
    "cross2d",
    "angle_between_vectors",
    "AngleMarker",
    "right_angle_square_fill_polygon",
    "GeometryEngine",
]
