---
name: manim-build-ly-thuyet-algebra
description: Sinh file Python Manim hoàn chỉnh từ spec-ly-thuyet.md cho bài giảng lý thuyết đại số (Step 2). Dùng khi spec.subject == "algebra". Kết hợp theory-figure/algebra (C1) + algebra primitives A2/A3/B1/B2. KHÔNG dùng GeometryEngine, AngleMarker, ProofLine.
---

> **Scope:** Skill này dành cho `subject: algebra`. Với `subject: geometry` → đọc `SKILL-geometry.md`.

# Skill: Manim Build – Bài Giảng Lý Thuyết (Step 2) — Algebra

## Khi nào dùng skill này?

- Đã có `spec-ly-thuyet.md` từ `manim-spec-ly-thuyet` **và** `spec.subject == "algebra"`
- Block có `figure.type` thuộc: `function`, `number_line`, `fraction`, `identity`, hoặc `none`
- Phân biệt với `SKILL-geometry.md`: không dùng `GeometryEngine`, không dùng `AngleMarker`, không dùng `register_point`

---

## Quy trình 3 bước

### Bước 1 – Đọc spec

Từ `spec-ly-thuyet.md`, xác định:
1. `lesson_title` và `total_scenes`
2. Từng scene: `block_type`, `heading`, `body_lines`, `formulas`, `figure.type`, `animations`, `cleanup`
3. Đánh dấu scene nào tái dùng figure từ scene trước (`cleanup = "keep figure_group"`)

### Bước 2 – Routing figure_type → primitive

**Bắt buộc đọc skill `theory-figure/algebra` (C1) trước khi code figure.**

| `figure.type` | Primitive skill | Helper chính |
|---|---|---|
| `function` | `algebra/coordinate-plane` (A3) | `Axes`, `plot_linear`, `plot_quadratic`, `mark_roots` |
| `number_line` | `algebra/number-line` (A2) | `NumberLine`, `shade_region`, `place_point` |
| `fraction` | `algebra/fraction-visual` (B1) | `FractionBar`, `FractionPie`, `animate_common_denominator` |
| `identity` | `algebra/identity-figure` (B2) | `identity_sq_plus`, `identity_sq_minus`, `identity_diff_sq` |
| `none` | — | Text full width, không cần figure panel |

### Bước 3 – Implement từng scene method

Với mỗi scene, theo thứ tự:
1. Dọn dẹp từ scene trước (nếu có)
2. Tạo `block_heading` → `to_corner(UL, buff=0.5)` → `Write`
3. Tạo `TheoryColumn` và các body mobs
4. **Dựng figure** theo `figure.type` (xem mục 3 bên dưới) → `place_figure(figure_group)`
5. Voiceover blocks: `FadeIn` text + figure theo `ov.duration`
6. `Indicate` thuật ngữ (nếu spec có `terms_bold`)
7. `FadeOut` theo `cleanup` trong spec

---

## Template file Python

```python
from manim import *
import numpy as np
from manim_voiceover import VoiceoverScene

from manim_helpers import (
    # design tokens
    COLOR_DEFAULT, COLOR_BACKGROUND, COLOR_GRID,
    COLOR_EQUAL_1, COLOR_EQUAL_2, COLOR_EQUAL_3,
    COLOR_ACTIVE, COLOR_SECONDARY, COLOR_FADED,
    COLOR_RESULT_KEY, COLOR_RESULT_FINAL,
    MOTION_ENTER, MOTION_EXIT, MOTION_TRANSFORM,
    TIMING_FADE, TIMING_POINT,
    LAYER_BACKGROUND, LAYER_GEOMETRY, LAYER_MARKERS, LAYER_PROOF_TEXT,
    # theory layout
    make_gtts_service,
    TheoryColumn,
)
from manim_helpers.theory_helpers import (
    place_figure,
    FIG_CENTER_X, FIG_CENTER_Y, FIG_MAX_W, FIG_MAX_H,
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
""")


class TenBaiLyThuyetDaiSo(VoiceoverScene):
    def construct(self):
        self.set_speech_service(make_gtts_service())
        self.setup_scene_style()
        self.scene00_intro()
        self.scene01_dinhNghia()
        self.scene02_dinhLi()
        # thêm scene theo spec

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
        grid.set_z_index(-10)
        self.add(grid)

    # ── State chia sẻ giữa scenes ──────────────────────────────────
    # self.figure_group   → figure hiện tại (Axes, NumberLine, FractionBar...)
    # self.lesson_title   → tiêu đề bài
```

---

## Pattern dựng figure algebra

**Quy tắc post-`place_figure`:** Dựng figure với tọa độ cục bộ → gọi `place_figure(figure_group)` → animate SAU place_figure. KHÔNG gọi `GeometryEngine`, `register_point`, `AngleMarker`.

### figure_type = `function`

```python
# Dùng algebra/coordinate-plane (A3)
axes = Axes(
    x_range=[-3, 5, 1], y_range=[-2, 8, 1],
    x_length=6.5, y_length=4.5,
    axis_config={
        "color": COLOR_DEFAULT, "include_tip": True,
        "include_numbers": True, "font_size": 22,
    },
)
x_lbl = axes.get_x_axis_label("x")
y_lbl = axes.get_y_axis_label("y")

# Plot đường thẳng y = 2x - 1
graph = axes.plot(lambda x: 2*x - 1, color=COLOR_EQUAL_1)
graph_lbl = MathTex(r"y=2x-1", color=COLOR_EQUAL_1, font_size=26)
graph_lbl.next_to(graph.get_end(), RIGHT, buff=0.15)

self.figure_group = VGroup(axes, x_lbl, y_lbl, graph, graph_lbl)
place_figure(self.figure_group)   # ← place TRƯỚC animate

# Animate SAU place_figure
self.play(Create(axes), Write(x_lbl), Write(y_lbl), run_time=MOTION_ENTER)
self.play(Create(graph), FadeIn(graph_lbl), run_time=MOTION_ENTER)
```

### figure_type = `number_line`

```python
# Dùng algebra/number-line (A2)
nl = NumberLine(
    x_range=[-3, 8, 1], length=7,
    include_numbers=True, include_tip=True,
    color=COLOR_DEFAULT, font_size=24,
)

# Tập nghiệm x > 2
region = shade_region(nl, x_start=2, x_end=None, color=COLOR_EQUAL_1)
pt_open = place_point(nl, 2, closed=False, color=COLOR_EQUAL_1)

self.figure_group = VGroup(nl, region, pt_open)
place_figure(self.figure_group)

# Animate SAU place_figure
self.play(Create(nl), run_time=MOTION_ENTER)
self.play(FadeIn(region), FadeIn(pt_open), run_time=MOTION_ENTER)
```

### figure_type = `fraction`

```python
# Dùng algebra/fraction-visual (B1)
bar = FractionBar(3, 4, width=4.5, height=0.75,
                  fill_color=COLOR_EQUAL_1, show_label=True)
self.figure_group = VGroup(bar)
place_figure(self.figure_group)

# Animate
self.play(FadeIn(self.figure_group), run_time=MOTION_ENTER)
```

### figure_type = `identity`

```python
# Dùng algebra/identity-figure (B2)
fig = identity_sq_plus(a_val=2, b_val=1)
self.figure_group = fig
place_figure(self.figure_group)

# Animate từng phần
self.play(FadeIn(self.figure_group[0]), run_time=MOTION_ENTER)  # grid
self.play(FadeIn(VGroup(*self.figure_group[1:])), run_time=MOTION_ENTER)  # labels
```

---

## Ví dụ scene hoàn chỉnh: figure_type = `function`

```python
def scene01_dinhNghia(self):
    # 1. Heading
    block_heading = Tex(r"\textbf{1. Định nghĩa}",
                        tex_template=viet_tex_template, font_size=32)
    block_heading.to_corner(UL, buff=0.5)
    self.play(Write(block_heading), run_time=0.6)

    # 2. TheoryColumn
    col = TheoryColumn(block_heading, has_figure=True)

    # 3. Body lines theo spec
    line1 = Tex(r"Hàm số bậc nhất có dạng $y = ax + b$, $a \neq 0$.",
                tex_template=viet_tex_template, font_size=26)
    col.place(line1)
    line2 = Tex(r"Đồ thị là một đường thẳng không qua gốc tọa độ.",
                tex_template=viet_tex_template, font_size=26)
    col.place(line2)

    # 4. Dựng figure (function) — dùng Axes
    axes = Axes(
        x_range=[-2, 4, 1], y_range=[-3, 6, 1],
        x_length=5.5, y_length=4,
        axis_config={"color": COLOR_DEFAULT, "include_numbers": True,
                     "font_size": 20, "include_tip": True},
    )
    x_lbl = axes.get_x_axis_label("x")
    y_lbl = axes.get_y_axis_label("y")
    graph = axes.plot(lambda x: 2*x - 1, color=COLOR_EQUAL_1)
    graph_lbl = MathTex(r"y=2x-1", color=COLOR_EQUAL_1, font_size=26)
    graph_lbl.next_to(graph.get_end(), RIGHT, buff=0.12)

    self.figure_group = VGroup(axes, x_lbl, y_lbl, graph, graph_lbl)
    place_figure(self.figure_group)   # place_figure TRƯỚC animate

    # 5. Voiceover block 1: giới thiệu định nghĩa + dựng trục
    with self.voiceover(
        "Hàm số bậc nhất có dạng y bằng a x cộng b, với a khác 0."
    ) as ov:
        self.play(FadeIn(line1), run_time=ov.duration * 0.5)
        self.play(Create(axes), Write(x_lbl), Write(y_lbl),
                  run_time=ov.duration * 0.5)

    # 6. Voiceover block 2: vẽ đồ thị + giải thích
    with self.voiceover(
        "Đồ thị của hàm số là một đường thẳng. "
        "Chẳng hạn, đây là đồ thị y bằng 2 x trừ 1."
    ) as ov:
        self.play(FadeIn(line2), run_time=ov.duration * 0.4)
        self.play(Create(graph), FadeIn(graph_lbl), run_time=ov.duration * 0.6)

    self.wait(0.5)

    # 7. Cleanup theo spec
    self.play(FadeOut(block_heading), FadeOut(col.all))
    # "keep figure_group" nếu scene sau tái dùng, hoặc:
    # self.play(FadeOut(self.figure_group))
```

---

## Ví dụ scene hoàn chỉnh: figure_type = `number_line`

```python
def scene02_dinhLi(self):
    block_heading = Tex(r"\textbf{2. Định lí}",
                        tex_template=viet_tex_template, font_size=32)
    block_heading.to_corner(UL, buff=0.5)
    self.play(Write(block_heading), run_time=0.6)

    col = TheoryColumn(block_heading, has_figure=True)

    statement = Tex(
        r"Bất phương trình $ax + b > 0$ ($a > 0$) có nghiệm $x > -\dfrac{b}{a}$.",
        tex_template=viet_tex_template, font_size=26)
    col.place(statement)

    formula = MathTex(r"S = \left\{x \mid x > -\dfrac{b}{a}\right\}", font_size=34)
    col.place_formula(formula)

    # Dựng figure (number_line)
    nl = NumberLine(
        x_range=[-4, 6, 1], length=6.5,
        include_numbers=True, include_tip=True,
        color=COLOR_DEFAULT, font_size=22,
    )
    region = shade_region(nl, x_start=2, x_end=None, color=COLOR_EQUAL_1)
    pt_open = place_point(nl, 2, closed=False, color=COLOR_EQUAL_1)
    pt_lbl  = MathTex(r"-\tfrac{b}{a}", font_size=24, color=COLOR_EQUAL_1)
    pt_lbl.next_to(nl.n2p(2), DOWN, buff=0.35)

    self.figure_group = VGroup(nl, region, pt_open, pt_lbl)
    place_figure(self.figure_group)   # place TRƯỚC animate

    with self.voiceover(
        "Bất phương trình a x cộng b lớn hơn 0 với a dương "
        "có tập nghiệm là x lớn hơn âm b trên a."
    ) as ov:
        self.play(FadeIn(statement), run_time=ov.duration * 0.4)
        self.play(Write(formula), Create(nl), run_time=ov.duration * 0.4)
        self.play(FadeIn(region), FadeIn(pt_open), FadeIn(pt_lbl),
                  run_time=ov.duration * 0.2)

    self.wait(0.5)
    self.play(FadeOut(block_heading), FadeOut(col.all),
              FadeOut(self.figure_group))
```

---

## Quy tắc chọn Animation (theory algebra)

| Tình huống | Animation |
|---|---|
| Hiện dòng text / bullet | `FadeIn(mob)` |
| Hiện heading | `Write(block_heading)` |
| Hiện công thức quan trọng | `Write(formula)` |
| Dựng `Axes` / `NumberLine` | `Create(axes)` / `Create(nl)` |
| Vẽ đồ thị | `Create(graph)` |
| Tô vùng / điểm trên trục | `FadeIn(region)`, `FadeIn(pt)` |
| Nhấn mạnh thuật ngữ | `Indicate(mob, scale_factor=1.12, color=COLOR_ACTIVE)` |
| Ẩn nhóm cuối scene | `FadeOut(VGroup(...))` |

---

## Quyết định figure lifecycle

| Spec `cleanup` | Code cần làm |
|---|---|
| `FadeOut(figure_group)` | `self.play(FadeOut(self.figure_group))` cuối scene |
| `keep figure_group` | Không FadeOut; scene sau dùng `self.figure_group` trực tiếp |
| `replace figure` | `self.play(FadeOut(self.figure_group))` → dựng figure mới → `place_figure(new_fig)` → `self.figure_group = new_fig` |

---

## Checklist trước khi render

- [ ] `setup_scene_style()` được gọi đầu `construct()`
- [ ] Mọi `Tex`/`MathTex` tiếng Việt có `tex_template=viet_tex_template`
- [ ] `place_figure(figure_group)` được gọi **TRƯỚC** mọi `self.play(Create/FadeIn)` cho figure
- [ ] KHÔNG gọi `GeometryEngine()`, `register_point()`, `AngleMarker()`, `TickMark()`
- [ ] KHÔNG có `ProofLine`, `ProofColumn`, `proof_accumulator`, `sync_point`, `sync_segment`
- [ ] KHÔNG dùng `place_dual_figures` (dành cho geometry) — dùng `VGroup(...).arrange(RIGHT)` nếu cần 2 figure algebra
- [ ] `self.figure_group` được gán đủ mọi Mobject thuộc figure để FadeOut đúng
- [ ] `col.all` bao gồm đủ body mobs
- [ ] Màu dùng token (`COLOR_*`), timing dùng token (`MOTION_*`/`TIMING_*`), không hardcode
