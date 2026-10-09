---
name: manim-algebra-identity-figure
description: Visualize hằng đẳng thức lớp 8 bằng hình ô diện tích — (a+b)², (a-b)², (a+b)(a-b) — với cell labels MathTex tự động căn giữa ô, animation ghép/tách. KHÔNG dùng Axes, GeometryEngine hay step-solver.
---

# Skill: Manim – Identity Figure (B2)

> Dành riêng cho **hằng đẳng thức đại số** (lớp 8) biểu diễn bằng hình ô diện tích.  
> Phân biệt với `hinh-phang` (hình học phẳng tổng quát có `GeometryEngine`).

---

## Khi nào dùng skill này?

- `(a+b)² = a² + 2ab + b²` — hình vuông lớn chia 4 ô
- `(a-b)² = a² - 2ab + b²` — hình vuông cắt góc
- `(a+b)(a-b) = a² - b²` — hình chữ nhật biến đổi thành hiệu hai bình phương
- Lớp 8: chứng minh trực quan hằng đẳng thức bằng hình ô

---

## 1. Import bắt buộc

```python
from manim_helpers import (
    COLOR_DEFAULT, COLOR_EQUAL_1, COLOR_EQUAL_2, COLOR_EQUAL_3,
    COLOR_ACTIVE, COLOR_SECONDARY, COLOR_RESULT_KEY, COLOR_RESULT_FINAL,
    MOTION_ENTER, MOTION_EXIT, MOTION_TRANSFORM,
    TIMING_FADE, EMPHASIS_SCALE, EMPHASIS_COLOR, EMPHASIS_INDICATE_TIME,
    LAYER_GEOMETRY, LAYER_MARKERS, LAYER_PROOF_TEXT,
)
```

---

## 2. Hằng đẳng thức (a+b)²

Hình vuông cạnh (a+b) chia thành 4 ô: a², ab, ab, b².

```python
def identity_sq_plus(a_val=2, b_val=1, cell_scale=1.2, label_font_size=32):
    """
    Xây dựng hình ô cho (a+b)² với giá trị a_val, b_val cho kích thước ô.
    Trả về VGroup chứa toàn bộ hình + labels.
    a_size, b_size: kích thước vật lý tỉ lệ với a_val, b_val
    """
    a_size = a_val * cell_scale
    b_size = b_val * cell_scale
    total = a_size + b_size

    # 4 ô hình chữ nhật
    cell_a2  = Rectangle(width=a_size, height=a_size,
                         fill_color=COLOR_EQUAL_1, fill_opacity=0.5, stroke_color=COLOR_DEFAULT)
    cell_ab1 = Rectangle(width=b_size, height=a_size,
                         fill_color=COLOR_EQUAL_2, fill_opacity=0.5, stroke_color=COLOR_DEFAULT)
    cell_ab2 = Rectangle(width=a_size, height=b_size,
                         fill_color=COLOR_EQUAL_2, fill_opacity=0.5, stroke_color=COLOR_DEFAULT)
    cell_b2  = Rectangle(width=b_size, height=b_size,
                         fill_color=COLOR_EQUAL_3, fill_opacity=0.5, stroke_color=COLOR_DEFAULT)

    # Sắp xếp theo lưới 2×2
    row_top    = VGroup(cell_a2, cell_ab1).arrange(RIGHT, buff=0)
    row_bottom = VGroup(cell_ab2, cell_b2).arrange(RIGHT, buff=0)
    grid = VGroup(row_top, row_bottom).arrange(DOWN, buff=0)
    grid.set_z_index(LAYER_GEOMETRY)

    # Labels căn giữa từng ô
    def mid_label(cell, tex):
        lbl = MathTex(tex, font_size=label_font_size)
        lbl.move_to(cell.get_center()).set_z_index(LAYER_PROOF_TEXT)
        return lbl

    lbl_a2  = mid_label(cell_a2,  r"a^2")
    lbl_ab1 = mid_label(cell_ab1, r"ab")
    lbl_ab2 = mid_label(cell_ab2, r"ab")
    lbl_b2  = mid_label(cell_b2,  r"b^2")

    # Dimension labels (a, b trên cạnh trên và cạnh trái)
    lbl_a_top  = MathTex("a", font_size=label_font_size, color=COLOR_EQUAL_1)
    lbl_a_top.next_to(cell_a2, UP, buff=0.18)
    lbl_b_top  = MathTex("b", font_size=label_font_size, color=COLOR_EQUAL_3)
    lbl_b_top.next_to(cell_ab1, UP, buff=0.18)
    lbl_a_left = MathTex("a", font_size=label_font_size, color=COLOR_EQUAL_1)
    lbl_a_left.next_to(cell_a2, LEFT, buff=0.18)
    lbl_b_left = MathTex("b", font_size=label_font_size, color=COLOR_EQUAL_3)
    lbl_b_left.next_to(cell_ab2, LEFT, buff=0.18)

    return VGroup(
        grid,
        lbl_a2, lbl_ab1, lbl_ab2, lbl_b2,
        lbl_a_top, lbl_b_top, lbl_a_left, lbl_b_left,
    )
```

### Animation (a+b)²

```python
def scene_sq_plus(self):
    title = Tex(r"$(a+b)^2 = a^2 + 2ab + b^2$", font_size=40)
    title.to_corner(UL, buff=0.45)
    self.play(Write(title), run_time=MOTION_ENTER)

    fig = identity_sq_plus(a_val=2, b_val=1)
    fig.move_to(ORIGIN + RIGHT * 0.5)

    # 1. Hiện khung ngoài trước
    outer = Square(
        side_length=fig[0].width,  # xấp xỉ
        stroke_color=COLOR_DEFAULT, stroke_width=2.5, fill_opacity=0,
    ).move_to(fig[0].get_center())
    self.play(Create(outer), run_time=MOTION_ENTER)

    # 2. Hiện từng ô + labels
    grid_group = fig[0]
    labels_group = VGroup(*fig[1:])
    self.play(FadeIn(grid_group), run_time=MOTION_ENTER)
    self.play(FadeIn(labels_group), run_time=MOTION_ENTER)

    # 3. Indicate từng ô
    cell_a2 = grid_group[0][0]
    cell_ab_pair = VGroup(grid_group[0][1], grid_group[1][0])  # 2 ô ab
    cell_b2 = grid_group[1][1]

    self.play(Indicate(cell_a2,      color=COLOR_EQUAL_1, scale_factor=EMPHASIS_SCALE),
              run_time=EMPHASIS_INDICATE_TIME)
    self.play(Indicate(cell_ab_pair, color=COLOR_EQUAL_2, scale_factor=EMPHASIS_SCALE),
              run_time=EMPHASIS_INDICATE_TIME)
    self.play(Indicate(cell_b2,      color=COLOR_EQUAL_3, scale_factor=EMPHASIS_SCALE),
              run_time=EMPHASIS_INDICATE_TIME)

    # 4. Công thức kết quả
    formula = MathTex(r"(a+b)^2 = a^2 + 2ab + b^2", font_size=36)
    formula.next_to(fig, DOWN, buff=0.55)
    box = SurroundingRectangle(formula, color=COLOR_RESULT_FINAL, buff=0.18)
    self.play(Write(formula), Create(box), run_time=MOTION_ENTER)
    self.wait(1.2)
    self.play(FadeOut(VGroup(title, outer, fig, formula, box)), run_time=MOTION_EXIT)
```

---

## 3. Hằng đẳng thức (a-b)²

Hình vuông cạnh a, cắt bỏ góc cạnh b, minh họa `(a-b)² = a² - 2ab + b²`.

```python
def identity_sq_minus(a_val=3, b_val=1, cell_scale=1.0, label_font_size=30):
    """
    Hình vuông cạnh a chia thành:
      - (a-b)²  ← ô chính (góc dưới-phải)
      - b(a-b)  ← 2 ô cạnh (trên-phải và dưới-trái)
      - b²      ← góc trên-trái (bị cắt ra)
    """
    a  = a_val * cell_scale
    b  = b_val * cell_scale
    ab = a - b

    cell_sq   = Rectangle(width=ab, height=ab,
                          fill_color=COLOR_EQUAL_1, fill_opacity=0.55, stroke_color=COLOR_DEFAULT)
    cell_top  = Rectangle(width=ab, height=b,
                          fill_color=COLOR_EQUAL_2, fill_opacity=0.45, stroke_color=COLOR_DEFAULT)
    cell_left = Rectangle(width=b,  height=ab,
                          fill_color=COLOR_EQUAL_2, fill_opacity=0.45, stroke_color=COLOR_DEFAULT)
    cell_b2   = Rectangle(width=b,  height=b,
                          fill_color=COLOR_EQUAL_3, fill_opacity=0.45, stroke_color=COLOR_DEFAULT,
                          stroke_style="dashed")  # góc cắt bỏ

    # Lắp ghép: b2 | top / left | sq (lưới 2×2 nhưng thứ tự trực quan)
    row_top    = VGroup(cell_b2,  cell_top).arrange(RIGHT, buff=0)
    row_bottom = VGroup(cell_left, cell_sq ).arrange(RIGHT, buff=0)
    grid = VGroup(row_top, row_bottom).arrange(DOWN, buff=0)
    grid.set_z_index(LAYER_GEOMETRY)

    def mid_label(cell, tex):
        lbl = MathTex(tex, font_size=label_font_size)
        lbl.move_to(cell.get_center()).set_z_index(LAYER_PROOF_TEXT)
        return lbl

    lbl_sq   = mid_label(cell_sq,   r"(a-b)^2")
    lbl_top  = mid_label(cell_top,  r"b(a-b)")
    lbl_left = mid_label(cell_left, r"b(a-b)")
    lbl_b2   = mid_label(cell_b2,   r"b^2")

    return VGroup(grid, lbl_sq, lbl_top, lbl_left, lbl_b2)
```

### Animation (a-b)²

```python
def scene_sq_minus(self):
    title = Tex(r"$(a-b)^2 = a^2 - 2ab + b^2$", font_size=40)
    title.to_corner(UL, buff=0.45)
    self.play(Write(title), run_time=MOTION_ENTER)

    fig = identity_sq_minus(a_val=3, b_val=1)
    fig.move_to(ORIGIN + RIGHT * 0.3)
    self.play(FadeIn(fig[0]), run_time=MOTION_ENTER)

    # Indicate từng vùng
    self.play(Indicate(fig[0][1][1], color=COLOR_EQUAL_1, scale_factor=EMPHASIS_SCALE),
              run_time=EMPHASIS_INDICATE_TIME)   # ô (a-b)²
    ab_pair = VGroup(fig[0][0][1], fig[0][1][0])
    self.play(Indicate(ab_pair, color=COLOR_EQUAL_2, scale_factor=EMPHASIS_SCALE),
              run_time=EMPHASIS_INDICATE_TIME)   # 2 ô b(a-b)

    self.play(FadeIn(VGroup(*fig[1:])), run_time=MOTION_ENTER)

    formula = MathTex(r"(a-b)^2 = a^2 - 2ab + b^2", font_size=36)
    formula.next_to(fig, DOWN, buff=0.5)
    box = SurroundingRectangle(formula, color=COLOR_RESULT_FINAL, buff=0.18)
    self.play(Write(formula), Create(box), run_time=MOTION_ENTER)
    self.wait(1.2)
    self.play(FadeOut(VGroup(title, fig, formula, box)), run_time=MOTION_EXIT)
```

---

## 4. Hằng đẳng thức (a+b)(a-b)

Hình chữ nhật `a × (a+b)` biến đổi thành `a² - b²`.

```python
def identity_diff_sq(a_val=3, b_val=1, cell_scale=1.0, label_font_size=30):
    """
    Hình chữ nhật (a+b) × (a-b):
      - Ô trái: a × a = a²
      - Ô phải: a × b = ab (sẽ bị cắt)
    Biến đổi: a² - b² = (a+b)(a-b).
    """
    a  = a_val * cell_scale
    b  = b_val * cell_scale

    cell_a2 = Rectangle(width=a, height=a,
                        fill_color=COLOR_EQUAL_1, fill_opacity=0.55, stroke_color=COLOR_DEFAULT)
    cell_ab = Rectangle(width=b, height=a,
                        fill_color=COLOR_EQUAL_2, fill_opacity=0.45, stroke_color=COLOR_DEFAULT)

    row = VGroup(cell_a2, cell_ab).arrange(RIGHT, buff=0)
    row.set_z_index(LAYER_GEOMETRY)

    def mid_label(cell, tex):
        lbl = MathTex(tex, font_size=label_font_size)
        lbl.move_to(cell.get_center()).set_z_index(LAYER_PROOF_TEXT)
        return lbl

    lbl_a2 = mid_label(cell_a2, r"a^2")
    lbl_ab = mid_label(cell_ab, r"ab")

    # Kích thước labels ngoài
    lbl_top_a  = MathTex("a", font_size=label_font_size, color=COLOR_EQUAL_1).next_to(cell_a2, UP, buff=0.18)
    lbl_top_b  = MathTex("b", font_size=label_font_size, color=COLOR_EQUAL_2).next_to(cell_ab, UP, buff=0.18)
    lbl_left_a = MathTex("a", font_size=label_font_size, color=COLOR_EQUAL_1).next_to(cell_a2, LEFT, buff=0.18)

    return VGroup(row, lbl_a2, lbl_ab, lbl_top_a, lbl_top_b, lbl_left_a)
```

### Animation (a+b)(a-b)

```python
def scene_diff_sq(self):
    title = Tex(r"$(a+b)(a-b) = a^2 - b^2$", font_size=40)
    title.to_corner(UL, buff=0.45)
    self.play(Write(title), run_time=MOTION_ENTER)

    fig = identity_diff_sq(a_val=3, b_val=1)
    fig.move_to(ORIGIN + RIGHT * 0.3)
    self.play(FadeIn(fig), run_time=MOTION_ENTER)
    self.wait(0.5)

    # Indicate ô ab (sẽ bị xóa)
    cell_ab = fig[0][1]
    self.play(cell_ab.animate.set_fill(COLOR_ACTIVE, opacity=0.7), run_time=TIMING_FADE)
    self.wait(0.3)

    # FadeOut ô ab → còn lại a²
    lbl_minus = MathTex(r"- b^2", font_size=36, color=COLOR_EQUAL_2)
    lbl_minus.next_to(fig[0][0], RIGHT, buff=1.2)
    self.play(FadeOut(VGroup(cell_ab, fig[2])),  # cell_ab + lbl_ab
              Write(lbl_minus), run_time=MOTION_TRANSFORM)

    formula = MathTex(r"a^2 - b^2 = (a+b)(a-b)", font_size=36)
    formula.next_to(fig, DOWN, buff=0.55)
    box = SurroundingRectangle(formula, color=COLOR_RESULT_FINAL, buff=0.18)
    self.play(Write(formula), Create(box), run_time=MOTION_ENTER)
    self.wait(1.2)
    self.play(FadeOut(VGroup(title, fig, lbl_minus, formula, box)), run_time=MOTION_EXIT)
```

---

## 5. Checklist

- [ ] `from manim_helpers import COLOR_EQUAL_1, COLOR_EQUAL_2, MOTION_ENTER, ...` — không hardcode màu
- [ ] Cell labels dùng `lbl.move_to(cell.get_center())` — không hardcode tọa độ
- [ ] Kích thước ô tỉ lệ với `a_val`, `b_val` — không cố định
- [ ] `Indicate` từng ô với đúng màu (`COLOR_EQUAL_1` cho a², `COLOR_EQUAL_2` cho ab, ...)
- [ ] Công thức kết quả đóng khung `COLOR_RESULT_FINAL`
- [ ] Không dùng `Axes`, `NumberLine`, `GeometryEngine` — đó là skill khác
