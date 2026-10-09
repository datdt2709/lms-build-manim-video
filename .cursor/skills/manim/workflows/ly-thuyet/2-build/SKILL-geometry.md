---
name: manim-build-ly-thuyet
description: Sinh file Python Manim hoàn chỉnh từ spec-ly-thuyet.md (Step 2 cho bài giảng lý thuyết). Dùng sau khi đã có spec lý thuyết để tạo code các scene Định nghĩa / Định lí / Nhận xét. Kết hợp với manim-theory-layout và manim-theory-blocks.
---

> **Scope:** Skill này dành cho `subject: geometry`. Với `subject: algebra` → đọc `SKILL-algebra.md` trong cùng thư mục.

# Skill: Manim Build – Bài Giảng Lý Thuyết (Step 2) — Geometry

## Mục đích

Đọc `spec-ly-thuyet.md` → sinh file Python Manim với đầy đủ class + scene methods.

---

## Khi nào dùng skill này?

- Đã có `spec-ly-thuyet.md` từ `manim-spec-ly-thuyet` **và** `spec.subject == "geometry"`
- Cần sinh code Python cho 1 hoặc nhiều scene lý thuyết hình học
- Khác `manim-step-2-build-scenes` (bài toán): không dùng `ProofLine`, không `GeometryEngine` persistent
- Khác `SKILL-algebra.md`: không dùng `Axes`, `NumberLine`, `FractionBar`

---

## Quy trình 3 bước

### Bước 1 – Đọc spec

Từ `spec-ly-thuyet.md`, xác định:
1. `lesson_title` và `total_scenes`
2. Từng scene: `block_type`, `heading`, `body_lines`, `formulas`, `figure.type`, `animations`, `cleanup`
3. Đánh dấu scene nào **tái dùng figure** từ scene trước (cleanup = "keep figure_group")

### Bước 2 – Subject routing + Tạo file Python

**Routing theo `spec.subject` trước khi code:**

```
if spec.subject == "geometry":
    → đọc thêm skill: theory-figure/geometry
    → áp dụng GeometryEngine post-place pattern (Section 2)
    → nếu dinh_nghia / dinh_li có 2 hình liên quan → dùng 2-related-shapes (Section 1)
    → KHÔNG hardcode tọa độ sau place_figure — dùng dot.get_center()

if spec.subject == "algebra":
    → DỪNG — đọc SKILL-algebra.md thay thế
    → SKILL-algebra.md hướng dẫn dùng theory-figure/algebra (C1)
    → KHÔNG dùng GeometryEngine, KHÔNG dùng AngleMarker

if spec.subject in ["statistics", "trigonometry", "combinatorics"]:
    → Bảng số liệu: dùng Table (Manim built-in)
    → Đồ thị: tham khảo SKILL-algebra.md (dùng Axes từ coordinate-plane)
```

Dùng template dưới đây, điền thông tin từ spec.

### Bước 3 – Implement từng scene method

Với mỗi scene, theo thứ tự:
1. Dọn dẹp từ scene trước (nếu có)
2. Tạo `block_heading` → `to_corner(UL, buff=0.5)` → `Write`
3. Tạo `TheoryColumn` và các body mobs (chưa add vào scene)
4. Dựng hình (nếu có figure) → `place_figure` / `place_dual_figures`
5. Voiceover blocks: `FadeIn` text + figure theo `ov.duration`
6. `Indicate` thuật ngữ / cặp góc (nếu spec yêu cầu)
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
    COLOR_CIRCLE, COLOR_RIGHT_ANGLE, COLOR_AUX_LINE,
    TIMING_INDICATE_SEGMENT, TIMING_FADE,
    LAYER_BACKGROUND, LAYER_GEOMETRY, LAYER_MARKERS,
    # theory layout
    make_gtts_service,
    TheoryColumn,
)
from manim_helpers.theory_helpers import (
    place_figure, place_dual_figures,
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


class TenBaiLyThuyet(VoiceoverScene):
    def construct(self):
        self.set_speech_service(make_gtts_service())
        self.setup_scene_style()
        self.scene00_intro()
        self.scene01_dinhNghia()
        self.scene02_dinhLi()
        self.scene03_nhanXet()
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
    # self.figure_group   → hình hiện tại (có thể tái dùng)
    # self.lesson_title   → tiêu đề bài (có thể thu nhỏ sau scene00)
```

---

## Pattern từng loại scene

### Scene 00 — Intro

```python
def scene00_intro(self):
    self.lesson_title = Tex(
        r"\textbf{BÀI X. TÊN BÀI}",
        tex_template=viet_tex_template, font_size=36)
    self.lesson_title.to_edge(UP, buff=0.4)

    section = Tex(r"I. TÓM TẮT LÝ THUYẾT",
                  tex_template=viet_tex_template, font_size=28)
    section.next_to(self.lesson_title, DOWN, buff=0.3)

    with self.voiceover("Bài học hôm nay: [tên bài].") as ov:
        self.play(Write(self.lesson_title), run_time=ov.duration * 0.6)
        self.play(FadeIn(section), run_time=ov.duration * 0.4)

    self.wait(0.5)
    self.play(FadeOut(section))
    # Giữ self.lesson_title hoặc thu nhỏ:
    # self.play(self.lesson_title.animate.scale(0.7).to_edge(UP, buff=0.2))
```

---

### Scene với figure mới

```python
def scene01_dinhNghia(self):
    # 1. Heading
    block_heading = Tex(r"\textbf{1. Định nghĩa}",
                        tex_template=viet_tex_template, font_size=32)
    block_heading.to_corner(UL, buff=0.5)
    self.play(Write(block_heading), run_time=0.6)

    # 2. TheoryColumn
    col = TheoryColumn(block_heading, has_figure=True)

    # 3. Body mobs — tạo sẵn theo spec.body_lines
    line1 = Tex(r"...", tex_template=viet_tex_template, font_size=26)
    col.place(line1)
    # thêm lines theo spec...

    # 4. Công thức (nếu spec có formulas)
    # formula = MathTex(r"...", font_size=34)
    # col.place_formula(formula)

    # 5. Dựng hình theo spec.figure.build (geometry)
    #    → xem theory-figure/geometry (post-place GeometryEngine pattern)
    circle = Circle(radius=2.2, color=COLOR_CIRCLE)
    # ... dựng thêm theo spec ...
    self.figure_group = VGroup(circle, ...)
    place_figure(self.figure_group)

    # 6. Voiceover + animations theo spec.animations
    with self.voiceover("...narration từ spec...") as ov:
        self.play(FadeIn(line1), Create(circle), run_time=ov.duration)

    # 7. Indicate nếu spec có terms_bold / cặp góc
    # self.play(Indicate(..., color=COLOR_ACTIVE))

    self.wait(0.5)

    # 8. Cleanup theo spec.cleanup
    # "keep figure_group" → không FadeOut self.figure_group
    self.play(FadeOut(block_heading), FadeOut(col.all))
```

---

### Scene tái dùng figure từ scene trước

```python
def scene02_dinhLi(self):
    # Dọn dẹp từ scene trước nếu cần (chỉ khi spec ghi cleanup_start)
    # self.play(FadeOut(...))

    block_heading = Tex(r"\textbf{2. Định lí}",
                        tex_template=viet_tex_template, font_size=32)
    block_heading.to_corner(UL, buff=0.5)
    self.play(Write(block_heading), run_time=0.6)

    col = TheoryColumn(block_heading, has_figure=True)

    # Body + formula theo spec
    statement = Tex(r"...", tex_template=viet_tex_template, font_size=26)
    col.place(statement, gap=0.30)

    formula = MathTex(r"...", font_size=34)
    col.place_formula(formula)

    # Tái dùng self.figure_group — đã ở đúng vị trí từ scene trước
    # Không cần Create lại; chỉ thêm Indicate / annotation mới

    with self.voiceover("...") as ov:
        self.play(FadeIn(statement), run_time=ov.duration * 0.4)
        self.play(Write(formula), run_time=ov.duration * 0.6)

    # Indicate trên figure_group
    with self.voiceover("...") as ov:
        self.play(
            Indicate(angle_mob_1, color=COLOR_EQUAL_1, scale_factor=1.2),
            Indicate(angle_mob_2, color=COLOR_EQUAL_1, scale_factor=1.2),
            run_time=ov.duration)

    self.wait(0.5)
    self.play(FadeOut(block_heading), FadeOut(col.all))
    # Giữ hoặc FadeOut self.figure_group theo spec.cleanup
```

---

### Scene với DualFigurePanel

```python
def scene03_nhanXet(self):
    block_heading = Tex(r"\textbf{3. Nhận xét}",
                        tex_template=viet_tex_template, font_size=32)
    block_heading.to_corner(UL, buff=0.5)
    self.play(Write(block_heading), run_time=0.5)

    col = TheoryColumn(block_heading, has_figure=True)

    bullets = [
        Tex(r"$\bullet$ ...", tex_template=viet_tex_template, font_size=26),
        Tex(r"$\bullet$ ...", tex_template=viet_tex_template, font_size=26),
    ]
    for b in bullets:
        col.place_bullet(b)

    # Dựng 2 hình nhỏ riêng biệt
    fig_left  = VGroup(...)   # hình 1
    fig_right = VGroup(...)   # hình 2
    dual_panel = place_dual_figures(
        fig_left, fig_right,
        label_left="Label trái", label_right="Label phải")

    with self.voiceover("...") as ov:
        self.play(FadeIn(bullets[0]), Create(fig_left), Create(fig_right),
                  run_time=ov.duration)

    with self.voiceover("...") as ov:
        self.play(FadeIn(bullets[1]), run_time=ov.duration)

    self.wait(0.5)
    self.play(FadeOut(block_heading), FadeOut(col.all), FadeOut(dual_panel))
```

---

## Quy tắc chọn Animation (theory)

| Tình huống | Animation |
|------------|-----------|
| Hiện dòng text / bullet | `FadeIn(mob)` — không `AddTextLetterByLetter` (chậm cho text dài) |
| Hiện heading | `Write(block_heading)` |
| Hiện công thức quan trọng | `Write(formula)` |
| Dựng hình hình học | `Create(mob)` |
| Nhấn mạnh thuật ngữ in đậm | `Indicate(mob, scale_factor=1.12, color=COLOR_ACTIVE)` |
| Nhấn mạnh cặp góc / cạnh | `Indicate(mob, scale_factor=1.2, color=COLOR_EQUAL_1)` |
| Ẩn nhóm cuối scene | `FadeOut(VGroup(...))` |
| Thay figure sang scene khác | `FadeOut(old_figure)` → dựng figure mới → `place_figure` |

**Không dùng trong file theory**: `TransformMatchingTex`, `AddTextLetterByLetter`, `sync_point`, `sync_segment`, `sync_angle`, `ProofLine`.

---

## Quyết định figure lifecycle

| Spec `cleanup` | Code cần làm |
|----------------|-------------|
| `FadeOut(figure_group)` | `self.play(FadeOut(self.figure_group))` cuối scene |
| `keep figure_group` | Không FadeOut; scene sau dùng `self.figure_group` trực tiếp |
| `replace figure` | `self.play(FadeOut(self.figure_group))` → dựng hình mới → `place_figure(new_fig)` → `self.figure_group = new_fig` |

---

## Checklist trước khi render

- [ ] `setup_scene_style()` được gọi đầu `construct()`
- [ ] Mọi `Tex`/`MathTex` tiếng Việt có `tex_template=viet_tex_template`
- [ ] Không có `ProofLine`, `ProofColumn`, `proof_accumulator`
- [ ] Mọi scene kết thúc bằng `FadeOut` đúng theo spec `cleanup`
- [ ] `self.figure_group` được gán khi dựng hình mới, tránh stale reference
- [ ] `col.all` bao gồm đủ body mobs (kiểm tra trước `FadeOut(col.all)`)
- [ ] Màu dùng token (`COLOR_*`), timing dùng token (`TIMING_*`), không hardcode
