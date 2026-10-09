---
name: manim-theory-figure-algebra
description: Orchestrate hình đại số cho scene bài giảng lý thuyết — chọn đúng primitive theo figure_type (function→coordinate-plane, number_line→number-line, fraction→fraction-visual, identity→identity-figure), áp dụng post-place pattern. Dùng sau khi đã có spec-ly-thuyet.md và spec.subject == "algebra". KHÔNG tự render hình.
---

# Skill: Manim – Theory Figure (Algebra) — C1

> Dành riêng cho `subject: algebra`. Kết hợp với `manim-theory-blocks` và `manim-theory-layout`.  
> Đọc skill này khi spec có `figure.type` là `function`, `number_line`, `fraction`, hoặc `identity`.

---

## Khi nào dùng skill này?

- Spec lý thuyết có `subject: algebra` và block có `figure` khác `none`
- Cần chọn đúng primitive (A1–B2) theo `figure_type` của block
- Cần áp dụng **post-`place_figure` pattern** cho algebra figure (giống geometry nhưng không có `GeometryEngine`)

---

## 1. Bảng routing `figure_type` → primitive

| `figure_type` | Primitive skill | Helper chính |
|---|---|---|
| `function` | `algebra/coordinate-plane` (A3) | `plot_linear`, `plot_quadratic`, `mark_roots`, `mark_point` |
| `number_line` | `algebra/number-line` (A2) | `mark_integer_range`, `shade_region`, `place_point` |
| `fraction` | `algebra/fraction-visual` (B1) | `FractionBar`, `FractionPie`, `animate_common_denominator`, `animate_simplify` |
| `identity` | `algebra/identity-figure` (B2) | `identity_sq_plus`, `identity_sq_minus`, `identity_diff_sq` |
| `geometry` | `theory-figure/geometry` | Xem skill đó |
| `dual_geometry` | `theory-figure/geometry` Section 4 | Xem skill đó |
| `none` | — | Text full width |

---

## 2. Post-`place_figure` pattern cho algebra

Algebra figure **không dùng `GeometryEngine`** nhưng vẫn cần `place_figure` để scale và định vị đúng panel.

```python
# ── Bước 1: Dựng figure với tọa độ cục bộ (chưa care vị trí màn hình) ──
if figure_type == "function":
    axes = Axes(x_range=[-3,5,1], y_range=[-2,8,1], x_length=6.5, y_length=4.5, ...)
    graph = plot_linear(axes, a=2, b=-1, color=COLOR_EQUAL_1, label_tex=r"y=2x-1")
    figure_group = VGroup(axes, graph)

elif figure_type == "number_line":
    nl = NumberLine(x_range=[-3,7,1], length=7, include_numbers=True, ...)
    region = shade_region(nl, x_start=2, x_end=None)
    pt = place_point(nl, 2, closed=False)
    figure_group = VGroup(nl, region, pt)

elif figure_type == "fraction":
    bar = FractionBar(3, 4, width=4.5, height=0.75)
    figure_group = VGroup(bar)

elif figure_type == "identity":
    fig = identity_sq_plus(a_val=2, b_val=1)
    figure_group = fig

# ── Bước 2: place_figure (scale + move_to đúng panel) ──
place_figure(figure_group)
self.figure_group = figure_group

# ── Bước 3: Animate figure (SAU place_figure) ──
# Với function: create axes → create graph
# Với number_line: create nl → fadein region + pt
# Với fraction/identity: fadein toàn bộ hoặc build từng phần
```

**Lý do quan trọng:** `place_figure()` gọi `scale_to_fit_width` và `move_to` → mọi tọa độ hardcode trước `place_figure` sẽ bị sai. Với algebra, không cần `register_point` như geometry, nhưng **vẫn phải animate SAU `place_figure`**.

---

## 3. Pattern đầy đủ: figure_type = `function`

```python
def build_figure_function(self, spec):
    """
    spec: dict với keys: x_range, y_range, curves (list dicts: type, params, label, color)
    """
    from manim_helpers import COLOR_EQUAL_1, COLOR_EQUAL_2, MOTION_ENTER, LAYER_GEOMETRY

    axes = Axes(
        x_range=spec.get("x_range", [-3, 5, 1]),
        y_range=spec.get("y_range", [-2, 8, 1]),
        x_length=spec.get("x_length", 6.5),
        y_length=spec.get("y_length", 4.5),
        axis_config={
            "color": COLOR_DEFAULT,
            "include_tip": True,
            "include_numbers": True,
            "font_size": 22,
        },
    )
    x_lbl = axes.get_x_axis_label("x")
    y_lbl = axes.get_y_axis_label("y")

    figure_group = VGroup(axes, x_lbl, y_lbl)

    # Dựng các đường đồ thị từ spec
    graphs = []
    for curve in spec.get("curves", []):
        if curve["type"] == "linear":
            a, b = curve["params"]
            g = plot_linear(axes, a, b, color=curve.get("color", COLOR_EQUAL_1),
                           label_tex=curve.get("label"))
        elif curve["type"] == "quadratic":
            a, b, c = curve["params"]
            g = plot_quadratic(axes, a, b, c, color=curve.get("color", COLOR_EQUAL_2),
                              label_tex=curve.get("label"))
        graphs.append(g)
        figure_group.add(g)

    place_figure(figure_group)
    self.figure_group = figure_group

    # Animate
    self.play(Create(axes), Write(x_lbl), Write(y_lbl), run_time=MOTION_ENTER)
    for g in graphs:
        self.play(Create(g), run_time=MOTION_ENTER)

    # Roots nếu có
    if "roots" in spec:
        roots_group = mark_roots(axes, spec["roots"])
        self.play(FadeIn(roots_group), run_time=MOTION_ENTER)
        figure_group.add(roots_group)
```

---

## 4. Pattern đầy đủ: figure_type = `number_line`

```python
def build_figure_number_line(self, spec):
    """
    spec: dict với keys: x_range, inequality (dict: type, value, closed)
    """
    nl = NumberLine(
        x_range=spec.get("x_range", [-5, 8, 1]),
        length=spec.get("length", 8),
        include_numbers=True,
        include_tip=True,
        color=COLOR_DEFAULT,
        font_size=24,
    )

    figure_group = VGroup(nl)

    if "inequality" in spec:
        ineq = spec["inequality"]
        region = shade_region(nl,
                              x_start=ineq.get("x_start"),
                              x_end=ineq.get("x_end"),
                              color=COLOR_EQUAL_1)
        pt = place_point(nl, ineq["boundary"], closed=ineq.get("closed", True))
        figure_group.add(region, pt)

    place_figure(figure_group)
    self.figure_group = figure_group

    # Animate
    self.play(Create(nl), run_time=MOTION_ENTER)
    if "inequality" in spec:
        self.play(FadeIn(figure_group[1]), run_time=MOTION_ENTER)  # region
        self.play(FadeIn(figure_group[2]), run_time=MOTION_ENTER)  # point
```

---

## 5. Sync Indicate với Voice (algebra)

Pattern đồng bộ Indicate algebra figure với voiceover (tương tự geometry nhưng không dùng `AngleMarker`):

```python
# Khi voice đọc "đồ thị hàm y=2x-1 cắt trục hoành tại x=0.5":
with self.voiceover("đồ thị cắt trục hoành tại x bằng 0.5...") as ov:
    roots_grp = mark_roots(axes, [0.5])
    self.play(FadeIn(roots_grp), run_time=ov.duration * 0.6)
    self.play(Indicate(roots_grp, scale_factor=EMPHASIS_SCALE, color=EMPHASIS_COLOR),
              run_time=ov.duration * 0.4)

# Khi voice đọc "tập nghiệm x > 2":
with self.voiceover("tập nghiệm là x lớn hơn 2...") as ov:
    self.play(FadeIn(region), run_time=ov.duration * 0.5)
    self.play(FadeIn(pt_open), run_time=ov.duration * 0.3)
    self.play(Indicate(region, color=EMPHASIS_COLOR, scale_factor=1.05),
              run_time=ov.duration * 0.2)
```

---

## 6. Cleanup pattern

```python
# Cuối scene: FadeOut figure_group + mọi thứ thêm vào
self.play(
    FadeOut(self.figure_group),
    FadeOut(block_heading),
    FadeOut(body_group),
    run_time=MOTION_EXIT,
)
```

---

## 7. Checklist

- [ ] Đọc `figure_type` từ spec → route đúng primitive (bảng mục 1)
- [ ] Dựng figure **trước** `place_figure` (tọa độ cục bộ)
- [ ] `place_figure(figure_group)` **trước** khi animate
- [ ] `self.figure_group = figure_group` để dễ cleanup sau
- [ ] Animate figure **sau** `place_figure` — không animate trước
- [ ] `shade_region` / `mark_roots` thêm vào `figure_group` để cleanup cùng
- [ ] Không dùng `GeometryEngine`, `register_point`, `AngleMarker` — đó là `theory-figure/geometry`
