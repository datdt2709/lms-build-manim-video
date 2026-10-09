---
name: manim-algebra-fraction-visual
description: Visualize phân số lớp 4–6 — FractionBar (thanh chia phần), FractionPie (hình tròn), animate quy đồng mẫu (2 thanh song song → mẫu chung), animate rút gọn (gạch chân UCLN). KHÔNG bao gồm phân số trên trục số (thuộc number-line).
---

# Skill: Manim – Fraction Visual (B1)

> Dành riêng cho **biểu diễn phân số trực quan** (lớp 4–6).  
> Phân biệt với `number-line` (phân số trên trục số 1D).

---

## Khi nào dùng skill này?

- Minh họa phân số bằng thanh chia phần (`FractionBar`) hoặc hình tròn (`FractionPie`)
- Animation quy đồng mẫu số: 2 thanh → tìm mẫu chung → chia lại
- Animation rút gọn phân số: gạch UCLN → chia tử và mẫu
- Lớp 4–6: phân số, so sánh phân số, cộng trừ phân số

---

## 1. Import bắt buộc

```python
from manim_helpers import (
    COLOR_DEFAULT, COLOR_EQUAL_1, COLOR_EQUAL_2, COLOR_EQUAL_3,
    COLOR_ACTIVE, COLOR_FADED, COLOR_RESULT_KEY, COLOR_RESULT_FINAL,
    MOTION_ENTER, MOTION_EXIT, MOTION_TRANSFORM,
    TIMING_FADE, EMPHASIS_SCALE, EMPHASIS_COLOR, EMPHASIS_INDICATE_TIME,
    LAYER_GEOMETRY, LAYER_MARKERS, LAYER_PROOF_TEXT,
)
```

---

## 2. FractionBar — thanh chia phần

```python
def FractionBar(numerator, denominator, width=4.0, height=0.7,
                fill_color=COLOR_EQUAL_1, bg_color=COLOR_FADED,
                show_label=True, label_font_size=28):
    """
    Vẽ thanh chia phần: denominator ô, numerator ô được tô màu.
    Trả về VGroup(bar_group, label_tex) hoặc chỉ bar_group nếu show_label=False.
    """
    cell_w = width / denominator
    cells = VGroup()
    for i in range(denominator):
        cell = Rectangle(width=cell_w, height=height, stroke_color=COLOR_DEFAULT, stroke_width=1.5)
        cell.set_fill(fill_color if i < numerator else bg_color, opacity=0.6 if i < numerator else 0.2)
        cell.set_z_index(LAYER_GEOMETRY)
        cells.add(cell)
    cells.arrange(RIGHT, buff=0)

    if show_label:
        lbl = MathTex(rf"\dfrac{{{numerator}}}{{{denominator}}}", font_size=label_font_size)
        lbl.next_to(cells, RIGHT, buff=0.35).set_z_index(LAYER_PROOF_TEXT)
        return VGroup(cells, lbl)
    return cells
```

```python
# Vẽ thanh biểu diễn 3/4
bar = FractionBar(3, 4, width=5, height=0.8)
bar.move_to(ORIGIN)
self.play(FadeIn(bar), run_time=MOTION_ENTER)
```

---

## 3. FractionPie — hình tròn phân số

```python
def FractionPie(numerator, denominator, radius=1.2,
                fill_color=COLOR_EQUAL_1, bg_color=COLOR_FADED,
                show_label=True, label_font_size=28):
    """
    Vẽ hình tròn chia denominator phần, tô numerator phần.
    Trả về VGroup(pie_group, label_tex).
    """
    angle_per = TAU / denominator
    slices = VGroup()
    for i in range(denominator):
        start = PI/2 - i * angle_per          # bắt đầu từ 12 giờ, quay theo chiều kim đồng hồ
        sector = Sector(
            radius=radius,
            start_angle=start - angle_per,
            angle=angle_per,
            fill_color=fill_color if i < numerator else bg_color,
            fill_opacity=0.65 if i < numerator else 0.2,
            stroke_color=COLOR_DEFAULT,
            stroke_width=1.5,
        )
        sector.set_z_index(LAYER_GEOMETRY)
        slices.add(sector)

    if show_label:
        lbl = MathTex(rf"\dfrac{{{numerator}}}{{{denominator}}}", font_size=label_font_size)
        lbl.next_to(slices, RIGHT, buff=0.35).set_z_index(LAYER_PROOF_TEXT)
        return VGroup(slices, lbl)
    return slices
```

```python
# Vẽ hình tròn biểu diễn 2/5
pie = FractionPie(2, 5, radius=1.3)
pie.move_to(ORIGIN)
self.play(FadeIn(pie), run_time=MOTION_ENTER)
```

---

## 4. animate_common_denominator — quy đồng mẫu

Animation: 2 thanh song song → tìm LCD → chia thành các ô nhỏ hơn, highlight ô tương đương.

```python
def animate_common_denominator(scene, frac1, frac2):
    """
    frac1, frac2: tuple (numerator, denominator)
    scene: Manim Scene instance
    Trả về (bar1_new, bar2_new) đã được animate.
    """
    from math import lcm
    n1, d1 = frac1
    n2, d2 = frac2
    lcd = lcm(d1, d2)

    # 1. Vẽ 2 thanh ban đầu
    bar1 = FractionBar(n1, d1, width=5.5, height=0.65, fill_color=COLOR_EQUAL_1, show_label=True)
    bar2 = FractionBar(n2, d2, width=5.5, height=0.65, fill_color=COLOR_EQUAL_2, show_label=True)
    bars = VGroup(bar1, bar2).arrange(DOWN, buff=0.55, aligned_edge=LEFT)
    bars.move_to(ORIGIN)
    scene.play(FadeIn(bars), run_time=MOTION_ENTER)
    scene.wait(0.5)

    # 2. Hiển thị LCD
    lcd_label = MathTex(rf"\text{{BCNN}} = {lcd}", tex_template=viet_tex_template, font_size=30)
    lcd_label.to_corner(UR, buff=0.5)
    scene.play(Write(lcd_label), run_time=MOTION_ENTER)

    # 3. Transform sang thanh mới với mẫu LCD
    n1_new = n1 * (lcd // d1)
    n2_new = n2 * (lcd // d2)
    bar1_new = FractionBar(n1_new, lcd, width=5.5, height=0.65, fill_color=COLOR_EQUAL_1, show_label=True)
    bar2_new = FractionBar(n2_new, lcd, width=5.5, height=0.65, fill_color=COLOR_EQUAL_2, show_label=True)
    bars_new = VGroup(bar1_new, bar2_new).arrange(DOWN, buff=0.55, aligned_edge=LEFT)
    bars_new.move_to(ORIGIN)

    scene.play(
        ReplacementTransform(bar1, bar1_new),
        ReplacementTransform(bar2, bar2_new),
        run_time=MOTION_TRANSFORM,
    )
    scene.wait(0.8)
    return bar1_new, bar2_new, lcd_label
```

```python
# Quy đồng 1/3 và 1/4
bar1_new, bar2_new, lcd_lbl = animate_common_denominator(self, (1, 3), (1, 4))
# Kết quả: 4/12 và 3/12
```

---

## 5. animate_simplify — rút gọn phân số

Animation: gạch UCLN trên tử và mẫu → animate chia → kết quả thu gọn.

```python
def animate_simplify(scene, numerator, denominator, pos=ORIGIN):
    """
    Animate rút gọn numerator/denominator bằng UCLN.
    """
    from math import gcd
    g = gcd(numerator, denominator)
    n_red = numerator // g
    d_red = denominator // g

    # 1. Hiện phân số gốc
    frac_orig = MathTex(rf"\dfrac{{{numerator}}}{{{denominator}}}", font_size=60)
    frac_orig.move_to(pos)
    scene.play(FadeIn(frac_orig), run_time=MOTION_ENTER)

    # 2. Label UCLN
    gcd_label = MathTex(rf"\text{{UCLN}} = {g}", tex_template=viet_tex_template, font_size=32,
                        color=COLOR_ACTIVE)
    gcd_label.next_to(frac_orig, RIGHT, buff=0.6)
    scene.play(Write(gcd_label), run_time=MOTION_ENTER)
    scene.wait(0.3)

    # 3. Gạch chân tử và mẫu
    num_part = frac_orig[0][:len(str(numerator))]  # lấy phần tử số
    strike_n = Line(num_part.get_left(), num_part.get_right(), color=COLOR_ACTIVE, stroke_width=3)
    strike_d_mob = frac_orig[0][len(str(numerator))+1:]  # mẫu
    strike_d = Line(strike_d_mob.get_left(), strike_d_mob.get_right(),
                    color=COLOR_ACTIVE, stroke_width=3)
    scene.play(Create(strike_n), Create(strike_d), run_time=TIMING_FADE)
    scene.wait(0.4)

    # 4. Transform sang phân số rút gọn
    frac_red = MathTex(rf"\dfrac{{{n_red}}}{{{d_red}}}", font_size=60)
    frac_red.move_to(pos)
    box = SurroundingRectangle(frac_red, color=COLOR_RESULT_FINAL, buff=0.18)
    scene.play(
        ReplacementTransform(frac_orig, frac_red),
        FadeOut(VGroup(strike_n, strike_d, gcd_label)),
        run_time=MOTION_TRANSFORM,
    )
    scene.play(Create(box), run_time=MOTION_ENTER)
    return frac_red, box
```

```python
# Rút gọn 6/8
frac, box = animate_simplify(self, 6, 8, pos=ORIGIN)
```

---

## 6. So sánh phân số bằng 2 thanh

```python
def compare_fractions(scene, frac1, frac2, pos=ORIGIN):
    """Hiển thị 2 FractionBar song song và ghi ký hiệu so sánh."""
    from fractions import Fraction
    n1, d1 = frac1
    n2, d2 = frac2
    val1 = Fraction(n1, d1)
    val2 = Fraction(n2, d2)
    cmp_sym = r">" if val1 > val2 else (r"<" if val1 < val2 else r"=")

    bar1 = FractionBar(n1, d1, width=4.5, fill_color=COLOR_EQUAL_1)
    bar2 = FractionBar(n2, d2, width=4.5, fill_color=COLOR_EQUAL_2)
    bars = VGroup(bar1, bar2).arrange(DOWN, buff=0.5, aligned_edge=LEFT)
    bars.move_to(pos)
    scene.play(FadeIn(bars), run_time=MOTION_ENTER)

    sym = MathTex(rf"\dfrac{{{n1}}}{{{d1}}} {cmp_sym} \dfrac{{{n2}}}{{{d2}}}", font_size=40)
    sym.next_to(bars, DOWN, buff=0.45)
    box = SurroundingRectangle(sym, color=COLOR_RESULT_KEY, buff=0.15)
    scene.play(Write(sym), Create(box), run_time=MOTION_ENTER)
    return bars, sym, box
```

---

## 7. Pattern hoàn chỉnh: quy đồng mẫu

```python
def scene_quy_dong_mau(self):
    title = Tex(r"\textbf{Quy đồng mẫu số}", tex_template=viet_tex_template, font_size=38)
    title.to_corner(UL, buff=0.45)
    self.play(Write(title), run_time=MOTION_ENTER)

    # Quy đồng 2/3 và 3/4
    bar1_new, bar2_new, lcd_lbl = animate_common_denominator(self, (2, 3), (3, 4))
    # Kết quả: 8/12 và 9/12

    self.wait(1.5)
    self.play(FadeOut(VGroup(title, bar1_new, bar2_new, lcd_lbl)), run_time=MOTION_EXIT)
```

---

## Checklist

- [ ] `from manim_helpers import COLOR_EQUAL_1, COLOR_EQUAL_2, MOTION_ENTER, ...` — không hardcode màu
- [ ] `FractionBar` và `FractionPie` dùng `COLOR_EQUAL_1` / `_2` cho các phân số cần so sánh (màu khác nhau)
- [ ] `animate_simplify` hiển thị UCLN rõ ràng trước khi gạch chân
- [ ] `animate_common_denominator` hiển thị BCNN, không chỉ kết quả cuối
- [ ] Không dùng `NumberLine` hay `Axes` — đó là skill khác
