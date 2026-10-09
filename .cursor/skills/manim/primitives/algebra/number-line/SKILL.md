---
name: manim-algebra-number-line
description: Dựng NumberLine cho bài lớp 6+ — ticks, labels số nguyên/phân số/thập phân, shade vùng bất phương trình, điểm mở ○ / đóng ●, animate điểm chuyển động. KHÔNG bao gồm Axes 2D, parabol hay geometry.
---

# Skill: Manim – Number Line (A2)

> Dành riêng cho **trục số 1D** (lớp 6+).  
> Phân biệt với `coordinate-plane` (Axes 2D cho hàm số lớp 7+).

---

## Khi nào dùng skill này?

- Biểu diễn tập nghiệm bất phương trình trên trục số (`x > 2`, `-1 ≤ x < 3`)
- Biểu diễn điểm phân số / số thập phân trên trục
- Animate điểm chuyển động (kiểm nghiệm nghiệm)
- Lớp 6: số nguyên, ước bội; Lớp 7: phân số, số hữu tỉ

---

## 1. Import bắt buộc

```python
from manim_helpers import (
    COLOR_DEFAULT, COLOR_ACTIVE, COLOR_EQUAL_1, COLOR_SECONDARY,
    COLOR_RESULT_KEY, COLOR_RESULT_FINAL, COLOR_FADED,
    MOTION_ENTER, MOTION_EXIT, TIMING_POINT, TIMING_SEGMENT,
    EMPHASIS_SCALE, EMPHASIS_COLOR, EMPHASIS_INDICATE_TIME,
    LAYER_GEOMETRY, LAYER_MARKERS,
)
```

---

## 2. Tạo NumberLine cơ bản

```python
# Số nguyên: x từ -5 đến 5
nl = NumberLine(
    x_range=[-5, 5, 1],        # [min, max, step]
    length=9,                   # chiều dài vật lý (đơn vị Manim)
    include_numbers=True,
    include_tip=True,
    tip_width=0.2,
    tip_height=0.2,
    color=COLOR_DEFAULT,
    label_direction=DOWN,
    font_size=28,
)
nl.move_to(ORIGIN)
self.play(Create(nl), run_time=MOTION_ENTER)
```

```python
# Phân số: x từ 0 đến 3, bước 0.5
nl = NumberLine(
    x_range=[0, 3, 0.5],
    length=8,
    include_numbers=True,
    numbers_to_include=[0, 0.5, 1, 1.5, 2, 2.5, 3],
    decimal_number_config={"num_decimal_places": 1},
    include_tip=True,
    color=COLOR_DEFAULT,
)
```

---

## 3. Helper: `mark_integer_range`

Đánh dấu một đoạn giá trị trên trục số bằng Brace hoặc label:

```python
def mark_integer_range(nl, a, b, label_tex, color=COLOR_ACTIVE):
    """Vẽ segment highlight từ nl.n2p(a) đến nl.n2p(b)."""
    seg = Line(nl.n2p(a), nl.n2p(b), color=color, stroke_width=6)
    seg.set_z_index(LAYER_GEOMETRY)
    lbl = MathTex(label_tex, color=color, font_size=28)
    lbl.next_to(seg, UP, buff=0.18)
    return VGroup(seg, lbl)
```

Cách dùng:
```python
rng = mark_integer_range(nl, 2, 5, r"x \in [2,5]")
self.play(Create(rng), run_time=MOTION_ENTER)
```

---

## 4. Helper: `shade_region`

Tô vùng bất phương trình bằng `Line` dày hoặc `Rectangle` mỏng:

```python
def shade_region(nl, x_start, x_end, color=COLOR_EQUAL_1, opacity=0.35):
    """
    Tô màu vùng [x_start, x_end] trên trục số.
    Dùng x_start=None hoặc x_end=None cho vùng vô cực.
    """
    if x_start is None:
        p_start = nl.get_left() + LEFT * 0.5
    else:
        p_start = nl.n2p(x_start)
    if x_end is None:
        p_end = nl.get_right() + RIGHT * 0.5
    else:
        p_end = nl.n2p(x_end)

    region = Rectangle(
        width=abs(p_end[0] - p_start[0]),
        height=0.25,
        fill_color=color,
        fill_opacity=opacity,
        stroke_width=0,
    )
    region.move_to((p_start + p_end) / 2)
    region.set_z_index(LAYER_GEOMETRY - 1)
    return region
```

```python
# x > 2: tô từ 2 đến +∞
region = shade_region(nl, x_start=2, x_end=None, color=COLOR_EQUAL_1)
self.play(FadeIn(region), run_time=MOTION_ENTER)

# -1 ≤ x < 3: tô từ -1 đến 3
region2 = shade_region(nl, x_start=-1, x_end=3, color=COLOR_EQUAL_1)
self.play(FadeIn(region2), run_time=MOTION_ENTER)
```

---

## 5. Helper: `place_point` — điểm mở ○ / đóng ●

```python
def place_point(nl, x_val, closed=True, color=COLOR_ACTIVE):
    """
    closed=True  → Dot đặc ● (đầu mút thuộc tập nghiệm)
    closed=False → Circle rỗng ○ (đầu mút không thuộc)
    """
    pos = nl.n2p(x_val)
    if closed:
        pt = Dot(pos, color=color, radius=0.10)
    else:
        pt = Circle(radius=0.10, color=color, stroke_width=2.5)
        pt.move_to(pos)
        pt.set_fill(opacity=0)   # rỗng giữa
    pt.set_z_index(LAYER_MARKERS)
    return pt
```

```python
# x > 2: điểm mở tại 2
pt_open  = place_point(nl, 2, closed=False, color=COLOR_EQUAL_1)
# -1 ≤ x: điểm đóng tại -1
pt_close = place_point(nl, -1, closed=True, color=COLOR_EQUAL_1)

self.play(FadeIn(pt_open), run_time=TIMING_POINT)
self.play(FadeIn(pt_close), run_time=TIMING_POINT)
```

---

## 6. Animate điểm chuyển động

```python
# Di chuyển dot từ vị trí này sang vị trí khác
dot_x = Dot(nl.n2p(0), color=COLOR_ACTIVE, radius=0.12).set_z_index(LAYER_MARKERS)
self.play(FadeIn(dot_x), run_time=TIMING_POINT)

# Chạy từ 0 → 4
self.play(dot_x.animate.move_to(nl.n2p(4)), run_time=1.2)

# Dùng ValueTracker để animate mượt + cập nhật label
tracker = ValueTracker(0)
dot_tracked = always_redraw(
    lambda: Dot(nl.n2p(tracker.get_value()), color=COLOR_ACTIVE, radius=0.12)
              .set_z_index(LAYER_MARKERS)
)
lbl_x = always_redraw(
    lambda: MathTex(rf"x = {tracker.get_value():.1f}", font_size=26)
              .next_to(dot_tracked, UP, buff=0.18)
)
self.add(dot_tracked, lbl_x)
self.play(tracker.animate.set_value(3), run_time=1.5)
self.remove(dot_tracked, lbl_x)
```

---

## 7. Pattern hoàn chỉnh: biểu diễn nghiệm bất phương trình

```python
def scene_bat_phuong_trinh(self):
    # 1. Tiêu đề + phương trình
    title = Tex(r"\textbf{Nghiệm:} $2x - 1 > 3$", tex_template=viet_tex_template, font_size=36)
    title.to_corner(UL, buff=0.45)
    self.play(Write(title), run_time=MOTION_ENTER)

    # 2. Dựng trục số
    nl = NumberLine(
        x_range=[-3, 7, 1], length=9,
        include_numbers=True, include_tip=True,
        color=COLOR_DEFAULT, font_size=26,
    )
    nl.move_to(DOWN * 0.5)
    self.play(Create(nl), run_time=MOTION_ENTER)

    # 3. Bước giải (step-solver pattern — gọi A1 nếu cần)
    sol = MathTex(r"x > 2").next_to(title, DOWN, aligned_edge=LEFT, buff=0.4)
    self.play(FadeIn(sol), run_time=MOTION_ENTER)

    # 4. Điểm mở tại 2
    pt = place_point(nl, 2, closed=False)
    self.play(FadeIn(pt), run_time=TIMING_POINT)

    # 5. Tô vùng x > 2
    region = shade_region(nl, x_start=2, x_end=None)
    self.play(FadeIn(region), run_time=MOTION_ENTER)

    # 6. Label tập nghiệm
    set_label = MathTex(r"S = \{x \mid x > 2\}").next_to(sol, DOWN, aligned_edge=LEFT, buff=0.3)
    box = SurroundingRectangle(set_label, color=COLOR_RESULT_FINAL, buff=0.18)
    self.play(FadeIn(set_label), Create(box), run_time=MOTION_ENTER)
    self.wait(1.2)

    # 7. Cleanup
    self.play(FadeOut(VGroup(title, sol, nl, pt, region, set_label, box)), run_time=MOTION_EXIT)
```

---

## Checklist

- [ ] `from manim_helpers import COLOR_EQUAL_1, MOTION_ENTER, LAYER_MARKERS, ...` — không hardcode
- [ ] `nl.n2p(x)` để chuyển giá trị → tọa độ Manim (không hardcode pixel)
- [ ] Điểm đầu mút: `closed=True` (●) hoặc `closed=False` (○) đúng theo dấu ≤ / <
- [ ] `shade_region` tô nhẹ (`opacity=0.35`) để không che số trên trục
- [ ] Không dùng `Axes`, `plot_*`, `GeometryEngine` — đó là skill khác
