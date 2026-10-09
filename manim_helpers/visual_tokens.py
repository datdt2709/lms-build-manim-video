"""Design tokens dùng chung cho mọi video Manim hình học.

Mọi scene PHẢI dùng các hằng số từ module này thay vì hardcode hex / số / z-index:

    from manim_helpers import (
        COLOR_DEFAULT, COLOR_EQUAL_1, COLOR_ACTIVE, ...,
        STATE_DEFAULT, STATE_HIGHLIGHT, ...,
        TIMING_SEGMENT, TIMING_PROOF_WRITE, ...,
        LAYER_GEOMETRY, LAYER_MARKERS, ...,
        MOTION_ENTER, MOTION_EXIT, MOTION_EMPHASIZE, ...,
        EMPHASIS_SCALE, EMPHASIS_COLOR, ...,
        apply_state,
    )

Quy ước đặt tên Mobject (rule 8) — bắt buộc dùng cho mọi scene hình học:

    point         -> dot_<X>
    segment       -> seg_<XY>
    angle (arc)   -> ang_<XYZ>
    triangle      -> tri_<XYZ>
    quadrilateral -> quad_<WXYZ>
    circle        -> circ_<NAME>
    sector / fill -> sec_<XYZ>
    right angle   -> ra_<X>
    proof line    -> pf_<NN>
"""

from __future__ import annotations

from typing import Dict


# ---------------------------------------------------------------------------
# Color tokens (rule 4) – bảng màu chuẩn cho nền sáng "#F5F1E8"
# ---------------------------------------------------------------------------

# Text & stroke mặc định
COLOR_DEFAULT = "#2C2C2C"
COLOR_BACKGROUND = "#F5F1E8"
COLOR_GRID = "#D6D0C4"

# Cặp màu "bằng nhau" (equal pairs / equal triples)
COLOR_EQUAL_1 = "#E65100"   # cam đậm – cặp đầu
COLOR_EQUAL_2 = "#2D6A2D"   # xanh lá đậm – cặp thứ hai
COLOR_EQUAL_3 = "#1565C0"   # xanh dương đậm – cặp thứ ba

# Trạng thái nhấn mạnh / vai trò
COLOR_ACTIVE = "#E65100"        # alias COLOR_EQUAL_1 – đối tượng đang được "active"
COLOR_SECONDARY = "#546E7A"     # đoạn phụ trợ (bán kính, đoạn nối)
COLOR_FADED = "#9E9E9E"         # đối tượng bị làm mờ

# Cảnh báo / kết quả
COLOR_WARNING = "#BF360C"       # cam cháy – cảnh báo / nhấn mạnh đặc biệt
COLOR_RESULT_KEY = "#2D6A2D"    # xanh lá – kết quả trung gian quan trọng (box GREEN)
COLOR_RESULT_FINAL = "#C62828"  # đỏ – kết luận cuối cùng / đpcm (box RED)

# Đối tượng hình học chuyên dụng
COLOR_CIRCLE = "#1565C0"
COLOR_RIGHT_ANGLE = "#37474F"
COLOR_AUX_LINE = "#546E7A"
COLOR_TANGENT = "#2E7D32"


# ---------------------------------------------------------------------------
# Visual states – dict gói {color, stroke_width, opacity} áp dụng qua apply_state
# ---------------------------------------------------------------------------

STATE_DEFAULT: Dict = {
    "color": COLOR_DEFAULT,
    "stroke_width": 1.6,
    "opacity": 0.9,
}

STATE_HIGHLIGHT: Dict = {
    "color": COLOR_ACTIVE,
    "stroke_width": 3.0,
    "opacity": 1.0,
}

STATE_EQUAL: Dict = {
    "color": COLOR_EQUAL_1,
    "stroke_width": 2.0,
    "opacity": 1.0,
}

STATE_SECONDARY: Dict = {
    "color": COLOR_SECONDARY,
    "stroke_width": 0.8,
    "opacity": 0.7,
}

STATE_FADED: Dict = {
    "color": COLOR_FADED,
    "stroke_width": 0.6,
    "opacity": 0.3,
}

STATE_ACTIVE: Dict = {
    "color": COLOR_ACTIVE,
    "stroke_width": 2.5,
    "opacity": 1.0,
}

# Điểm đánh dấu (Dot) — cân với STATE_DEFAULT stroke ~1.6; tinh chỉnh tập trung tại đây
MARKER_DOT_RADIUS = 0.05
MARKER_DOT_RADIUS_AUX = 0.043  # điểm phụ (~tỉ lệ 0.06/0.07 so với MARKER_DOT_RADIUS)


def apply_state(mob, state: Dict):
    """Apply a visual state (dict) lên một Mobject.

    Hỗ trợ key: color, stroke_width, opacity. Các key thiếu sẽ được bỏ qua.
    Trả về `mob` để chain.
    """
    color = state.get("color")
    stroke_width = state.get("stroke_width")
    opacity = state.get("opacity")

    if color is not None and hasattr(mob, "set_color"):
        mob.set_color(color)
    if stroke_width is not None and hasattr(mob, "set_stroke"):
        try:
            mob.set_stroke(width=stroke_width)
        except TypeError:
            mob.set_stroke(stroke_width)
    if opacity is not None:
        if hasattr(mob, "set_opacity"):
            mob.set_opacity(opacity)
        elif hasattr(mob, "set_fill"):
            mob.set_fill(opacity=opacity)
    return mob


# ---------------------------------------------------------------------------
# Timing tokens (rule 6) – đơn vị: giây
# ---------------------------------------------------------------------------

# Thời gian các effect "Indicate / nhấn mạnh"
TIMING_POINT = 0.2              # Flash / Indicate dot
TIMING_SEGMENT = 0.4            # Indicate đoạn thẳng
TIMING_ANGLE = 0.5              # FadeIn/FadeOut sector góc
TIMING_INDICATE_SEGMENT = 0.6   # set_stroke there_and_back trên cạnh
TIMING_INDICATE_TRIANGLE = 0.7  # set_fill there_and_back trên Polygon

# Thời gian AddTextLetterByLetter proof
TIMING_PROOF_WRITE = 1.0        # AddTextLetterByLetter toàn bộ ProofLine (gõ từng ký tự, cần lâu hơn Write)
TIMING_RELATION = 0.25          # Write 1 token nhỏ trong ProofLine ('=', '⇒', '(c.g.c)')
TIMING_CONCLUSION = 0.8         # Write kết luận cuối ý

# Thời gian Fade chung
TIMING_FADE = 0.3               # FadeIn / FadeOut chuẩn


# ---------------------------------------------------------------------------
# Motion tokens (MOTION_*) – run_time chuẩn cho animation chuyển động
# ---------------------------------------------------------------------------
# Dùng cho các animation di chuyển / xuất hiện / biến mất của Mobject,
# phân biệt với TIMING_* vốn dành cho highlight effect.

MOTION_ENTER = 0.6          # FadeIn / Create cho phần tử mới vào scene
MOTION_EXIT = 0.4           # FadeOut / Uncreate cho phần tử rời scene
MOTION_TRANSFORM = 0.7      # ReplacementTransform / TransformMatchingTex
MOTION_SHIFT = 0.5          # .animate.shift(...) / .animate.move_to(...)
MOTION_SCALE = 0.4          # .animate.scale(...)
MOTION_TO_CORNER = 0.6      # result_group.animate.to_corner(UR, ...)
MOTION_TITLE_IN = 0.9       # AddTextLetterByLetter(title) — tiêu đề scene xuất hiện (gõ từng ký tự, tiêu đề thường dài)
MOTION_TITLE_OUT = 0.35     # FadeOut(title) — tiêu đề biến mất


# ---------------------------------------------------------------------------
# Emphasis tokens (EMPHASIS_*) – cấu hình cho Indicate / Circumscribe
# ---------------------------------------------------------------------------
# Dùng thay vì hardcode scale_factor=1.2, color=COLOR_ACTIVE, v.v.
# trong mọi lệnh Indicate / Circumscribe / Flash.

EMPHASIS_SCALE = 1.15           # scale_factor cho Indicate(...) — vừa đủ nhấn mạnh
EMPHASIS_SCALE_STRONG = 1.3     # scale_factor mạnh hơn (kết luận quan trọng)
EMPHASIS_COLOR = "#E65100"      # alias COLOR_ACTIVE — màu Indicate mặc định
EMPHASIS_FLASH_RADIUS = 0.25    # Flash(..., flash_radius=...) cho Dot
EMPHASIS_CIRCUMSCRIBE_TIME = 1.2  # run_time cho Circumscribe (thường fade_out=True)
EMPHASIS_INDICATE_TIME = 0.7    # run_time cho Indicate(...) — nhấn mạnh trung bình


# ---------------------------------------------------------------------------
# Layer / z-index tokens (rule 7)
# ---------------------------------------------------------------------------
# Layout:  background < geometry < markers < proof text < highlight tạm thời

LAYER_BACKGROUND = 0     # NumberPlane, ô lưới
LAYER_GEOMETRY = 10      # Arc, Circle, Line, Polygon (mặc định)
LAYER_MARKERS = 20       # Dot, label, RightAngle, AngleMarker
LAYER_PROOF_TEXT = 30    # MathTex, Tex của proof, title
LAYER_HIGHLIGHT = 40     # highlight tạm thời (Sector fill, Indicate copy)


# ---------------------------------------------------------------------------
# Naming convention helpers (rule 8) – kiểm tra tên biến tuân quy ước
# ---------------------------------------------------------------------------

NAMING_PATTERNS = {
    "point": r"^dot_[A-Z][A-Za-z0-9_]*$",
    "label": r"^label_[A-Z][A-Za-z0-9_]*$",
    "segment": r"^seg_[A-Z]{2,}[A-Za-z0-9_]*$",
    "angle": r"^ang_[A-Z]{3,}[A-Za-z0-9_]*$",
    "triangle": r"^tri_[A-Z]{3,}[A-Za-z0-9_]*$",
    "quadrilateral": r"^quad_[A-Z]{4,}[A-Za-z0-9_]*$",
    "circle": r"^circ_[A-Za-z0-9_]+$",
    "sector": r"^sec_[A-Z]{3,}[A-Za-z0-9_]*$",
    "right_angle": r"^ra_[A-Z][A-Za-z0-9_]*$",
    "proof_line": r"^pf_\d{1,2}$",
}


def check_name(kind: str, name: str) -> bool:
    """Trả True nếu `name` tuân quy ước đặt tên cho `kind`.

    `kind` thuộc một trong các key của NAMING_PATTERNS.
    Hàm này CHỈ phục vụ self-check trong test, không bắt buộc dùng runtime.
    """
    import re

    pattern = NAMING_PATTERNS.get(kind)
    if pattern is None:
        raise ValueError(f"Unknown naming kind: {kind!r}")
    return bool(re.match(pattern, name))


__all__ = [
    # Colors
    "COLOR_DEFAULT", "COLOR_BACKGROUND", "COLOR_GRID",
    "COLOR_EQUAL_1", "COLOR_EQUAL_2", "COLOR_EQUAL_3",
    "COLOR_ACTIVE", "COLOR_SECONDARY", "COLOR_FADED",
    "COLOR_WARNING", "COLOR_RESULT_KEY", "COLOR_RESULT_FINAL",
    "COLOR_CIRCLE", "COLOR_RIGHT_ANGLE", "COLOR_AUX_LINE", "COLOR_TANGENT",
    # States
    "STATE_DEFAULT", "STATE_HIGHLIGHT", "STATE_EQUAL",
    "STATE_SECONDARY", "STATE_FADED", "STATE_ACTIVE",
    "MARKER_DOT_RADIUS", "MARKER_DOT_RADIUS_AUX",
    "apply_state",
    # Timing (highlight effects)
    "TIMING_POINT", "TIMING_SEGMENT", "TIMING_ANGLE",
    "TIMING_INDICATE_SEGMENT", "TIMING_INDICATE_TRIANGLE",
    "TIMING_PROOF_WRITE", "TIMING_RELATION", "TIMING_CONCLUSION",
    "TIMING_FADE",
    # Motion tokens (animation movement)
    "MOTION_ENTER", "MOTION_EXIT", "MOTION_TRANSFORM",
    "MOTION_SHIFT", "MOTION_SCALE", "MOTION_TO_CORNER",
    "MOTION_TITLE_IN", "MOTION_TITLE_OUT",
    # Emphasis tokens (Indicate / Circumscribe config)
    "EMPHASIS_SCALE", "EMPHASIS_SCALE_STRONG", "EMPHASIS_COLOR",
    "EMPHASIS_FLASH_RADIUS", "EMPHASIS_CIRCUMSCRIBE_TIME", "EMPHASIS_INDICATE_TIME",
    # Layers
    "LAYER_BACKGROUND", "LAYER_GEOMETRY", "LAYER_MARKERS",
    "LAYER_PROOF_TEXT", "LAYER_HIGHLIGHT",
    # Naming
    "NAMING_PATTERNS", "check_name",
]
