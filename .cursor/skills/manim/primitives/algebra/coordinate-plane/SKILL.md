---
name: manim-algebra-coordinate-plane
description: Dựng Axes 2D cho hàm số lớp 7+ — plot_linear (y=ax+b), plot_quadratic (y=ax²+bx+c), mark_roots, label tọa độ tự động, đánh dấu giao điểm. KHÔNG bao gồm trục số 1D, GeometryEngine hay hình phẳng.
---

# Skill: Manim – Coordinate Plane (A3)

> Dành riêng cho **Axes 2D + hàm số** (lớp 7+).  
> Phân biệt với `number-line` (trục số 1D) và `geometry-engine` (hình học phẳng).

---

## Khi nào dùng skill này?

- Vẽ đồ thị hàm số `y = ax + b`, `y = ax²+bx+c`, `y = ax`
- Đánh dấu nghiệm (giao điểm đồ thị với trục hoàng), giao điểm 2 đồ thị
- Biểu diễn bảng biến thiên (tùy chọn)
- Lớp 7: hàm số bậc nhất; Lớp 9: hàm số bậc hai (parabol)

---

## 1. Import bắt buộc

```python
from manim_helpers import (
    COLOR_DEFAULT, COLOR_ACTIVE, COLOR_EQUAL_1, COLOR_EQUAL_2,
    COLOR_SECONDARY, COLOR_RESULT_KEY, COLOR_RESULT_FINAL,
    MOTION_ENTER, MOTION_EXIT, MOTION_TRANSFORM,
    TIMING_POINT, TIMING_SEGMENT,
    EMPHASIS_SCALE, EMPHASIS_COLOR, EMPHASIS_INDICATE_TIME,
    LAYER_GEOMETRY, LAYER_MARKERS, LAYER_PROOF_TEXT,
)
```

---

## 2. Tạo Axes với label tùy chỉnh, auto-scale

```python
axes = Axes(
    x_range=[-3, 5, 1],       # [min, max, step]
    y_range=[-2, 8, 1],
    x_length=7,                # chiều dài vật lý
    y_length=5,
    axis_config={
        "color": COLOR_DEFAULT,
        "include_tip": True,
        "tip_width": 0.18,
        "tip_height": 0.18,
        "include_numbers": True,
        "font_size": 22,
    },
)
axes.move_to(ORIGIN + DOWN * 0.3)

x_label = axes.get_x_axis_label("x", edge=RIGHT, direction=RIGHT, buff=0.15)
y_label = axes.get_y_axis_label("y", edge=UP, direction=UP, buff=0.1)

self.play(Create(axes), Write(x_label), Write(y_label), run_time=MOTION_ENTER)
```

**Auto-scale theo range:** Chọn `x_length` và `y_length` sao cho tỉ lệ `x_length/(x_max-x_min) ≈ y_length/(y_max-y_min)` để đồ thị không méo.

---

## 3. Helper: `plot_linear` — đường thẳng y=ax+b

```python
def plot_linear(axes, a, b, color=COLOR_EQUAL_1, label_tex=None):
    """Vẽ đường thẳng y = ax + b trên axes."""
    x_min, x_max = axes.x_range[0], axes.x_range[1]
    graph = axes.plot(lambda x: a * x + b, x_range=[x_min, x_max], color=color)
    graph.set_z_index(LAYER_GEOMETRY)
    if label_tex:
        lbl = MathTex(label_tex, color=color, font_size=26)
        lbl.next_to(graph.get_end(), RIGHT, buff=0.15)
        lbl.set_z_index(LAYER_MARKERS)
        return VGroup(graph, lbl)
    return graph
```

```python
line1 = plot_linear(axes, a=2, b=-1, color=COLOR_EQUAL_1, label_tex=r"y=2x-1")
self.play(Create(line1), run_time=MOTION_ENTER)
```

---

## 4. Helper: `plot_quadratic` — parabol y=ax²+bx+c

```python
def plot_quadratic(axes, a, b, c, color=COLOR_EQUAL_2, label_tex=None):
    """Vẽ parabol y = ax² + bx + c trên axes."""
    x_min, x_max = axes.x_range[0], axes.x_range[1]
    graph = axes.plot(lambda x: a*x**2 + b*x + c, x_range=[x_min, x_max], color=color)
    graph.set_z_index(LAYER_GEOMETRY)
    if label_tex:
        # Đặt label tại đỉnh parabol (nếu a > 0: min; a < 0: max)
        x_vertex = -b / (2 * a)
        y_vertex = a * x_vertex**2 + b * x_vertex + c
        pos = axes.c2p(x_vertex, y_vertex)
        direction = UP if a > 0 else DOWN
        lbl = MathTex(label_tex, color=color, font_size=26)
        lbl.next_to(pos, direction, buff=0.2)
        lbl.set_z_index(LAYER_MARKERS)
        return VGroup(graph, lbl)
    return graph
```

```python
parabola = plot_quadratic(axes, a=1, b=-2, c=-3, label_tex=r"y=x^2-2x-3")
self.play(Create(parabola), run_time=MOTION_ENTER)
```

---

## 5. Helper: `mark_roots` — nghiệm (giao Ox)

```python
def mark_roots(axes, roots, color=COLOR_ACTIVE):
    """
    Đánh dấu nghiệm (x0, 0) trên trục hoành.
    roots: list[float]
    """
    group = VGroup()
    for x0 in roots:
        pos = axes.c2p(x0, 0)
        dot = Dot(pos, color=color, radius=0.09).set_z_index(LAYER_MARKERS)
        lbl = MathTex(str(int(x0)) if float(x0).is_integer() else f"{x0}", font_size=24, color=color)
        lbl.next_to(dot, DOWN, buff=0.18).set_z_index(LAYER_MARKERS)
        group.add(VGroup(dot, lbl))
    return group
```

```python
roots = mark_roots(axes, roots=[-1, 3])
self.play(FadeIn(roots), run_time=MOTION_ENTER)
```

---

## 6. Helper: `mark_point` — đánh dấu điểm bất kỳ

```python
def mark_point(axes, x, y, label_tex=None, color=COLOR_ACTIVE, direction=UR):
    """Đánh dấu điểm (x, y) trên mặt phẳng tọa độ."""
    pos = axes.c2p(x, y)
    dot = Dot(pos, color=color, radius=0.09).set_z_index(LAYER_MARKERS)
    group = VGroup(dot)
    if label_tex:
        lbl = MathTex(label_tex, font_size=24, color=color)
        lbl.next_to(dot, direction, buff=0.15).set_z_index(LAYER_MARKERS)
        group.add(lbl)
    return group
```

---

## 7. Đánh dấu giao điểm 2 đồ thị

```python
# Tìm giao điểm bằng numpy hoặc tính tay
from scipy.optimize import brentq  # hoặc tính nghiệm giải tích

def find_intersection(f, g, x_min, x_max):
    """Tìm x sao cho f(x) = g(x) trong [x_min, x_max]."""
    return brentq(lambda x: f(x) - g(x), x_min, x_max)

f = lambda x: 2*x - 1
g = lambda x: x**2 - 3

x_inter = find_intersection(f, g, 1, 3)  # ≈ 2.303
y_inter = f(x_inter)

pt_inter = mark_point(axes, x_inter, y_inter, label_tex=r"A", direction=UL)
self.play(FadeIn(pt_inter), run_time=TIMING_POINT)
```

---

## 8. Dashed lines từ điểm đến trục

```python
def dashed_to_axes(axes, x, y, color=COLOR_SECONDARY):
    """Vẽ đường nét đứt từ điểm (x,y) xuống trục x và sang trục y."""
    pos = axes.c2p(x, y)
    x_axis_pos = axes.c2p(x, 0)
    y_axis_pos = axes.c2p(0, y)

    h_dash = DashedLine(pos, x_axis_pos, color=color, stroke_width=1.5, dash_length=0.12)
    v_dash = DashedLine(pos, y_axis_pos, color=color, stroke_width=1.5, dash_length=0.12)
    return VGroup(h_dash, v_dash)
```

```python
dashes = dashed_to_axes(axes, x=2, y=3)
self.play(Create(dashes), run_time=TIMING_SEGMENT)
```

---

## 9. Pattern hoàn chỉnh: đồ thị hàm bậc nhất

```python
def scene_ham_so_bac_nhat(self):
    # 1. Tiêu đề
    title = Tex(r"\textbf{Đồ thị hàm số} $y = 2x - 1$", tex_template=viet_tex_template, font_size=36)
    title.to_corner(UL, buff=0.45)
    self.play(Write(title), run_time=MOTION_ENTER)

    # 2. Axes
    axes = Axes(
        x_range=[-2, 4, 1], y_range=[-4, 6, 1],
        x_length=6.5, y_length=5,
        axis_config={"include_numbers": True, "color": COLOR_DEFAULT, "font_size": 22, "include_tip": True},
    ).move_to(ORIGIN + RIGHT * 0.5)
    x_lbl = axes.get_x_axis_label("x")
    y_lbl = axes.get_y_axis_label("y")
    self.play(Create(axes), Write(x_lbl), Write(y_lbl), run_time=MOTION_ENTER)

    # 3. Plot đường thẳng
    line = plot_linear(axes, a=2, b=-1, label_tex=r"y=2x-1")
    self.play(Create(line), run_time=MOTION_ENTER)

    # 4. Nghiệm (giao Ox: x=0.5)
    roots = mark_roots(axes, roots=[0.5])
    self.play(FadeIn(roots), run_time=MOTION_ENTER)

    # 5. Điểm đặc biệt (0, -1)
    y_intercept = mark_point(axes, 0, -1, label_tex=r"(0,-1)", direction=LEFT)
    self.play(FadeIn(y_intercept), run_time=TIMING_POINT)

    self.wait(1.5)

    # 6. Cleanup
    self.play(FadeOut(VGroup(title, axes, x_lbl, y_lbl, line, roots, y_intercept)),
              run_time=MOTION_EXIT)
```

---

## Checklist

- [ ] `from manim_helpers import COLOR_EQUAL_1, MOTION_ENTER, LAYER_MARKERS, ...` — không hardcode
- [ ] `axes.c2p(x, y)` để chuyển tọa độ toán → tọa độ Manim (không hardcode pixel)
- [ ] `x_length` / `y_length` cân đối với range để đồ thị không méo
- [ ] `mark_roots` dùng `axes.c2p(x0, 0)` — không dùng `nl.n2p`
- [ ] `plot_*` trả về `VGroup(graph, label)` để dễ FadeOut
- [ ] Không dùng `NumberLine`, `GeometryEngine` — đó là skill khác
