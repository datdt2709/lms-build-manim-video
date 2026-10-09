---
name: manim-problem-circle-tangent
description: Pattern code Manim cho bài toán tiếp tuyến đường tròn, nửa đường tròn, hai tiếp tuyến từ điểm ngoài. Dùng khi có góc nội tiếp 90° hoặc power of a point.
---

# Pattern: Tiếp Tuyến Đường Tròn / Nửa Đường Tròn

## Dạng bài điển hình

Bài toán liên quan đến: nửa đường tròn, tiếp tuyến tại điểm trên đường tròn, góc nội tiếp bằng 90°, hai tiếp tuyến từ điểm ngoài, power of a point.

---

## 1. Tọa độ mẫu – Nửa đường tròn + tiếp tuyến tại C

```python
import numpy as np
from manim import *
from manim_helpers import line_intersection, COLOR_CIRCLE, COLOR_DEFAULT, COLOR_AUX_LINE, COLOR_TANGENT

R = 2.5
O = np.array([0.0, 0.0, 0.0])
A = np.array([-R, 0.0, 0.0])   # trái đường kính
B = np.array([ R, 0.0, 0.0])   # phải đường kính

# Điểm C trên nửa đường tròn (góc tự chọn, tránh ~0° và ~180°)
C_angle = 70 * DEGREES          # điều chỉnh để hình đẹp
C = np.array([R * np.cos(C_angle), R * np.sin(C_angle), 0])

# Điểm D trên đường kính AB (nằm giữa A và B)
D_ratio = 0.35                  # D chia AB: D = A + ratio * (B - A)
D = A + D_ratio * (B - A)

# Đường vuông góc với AB tại D → giao đường tròn ở E (nội tiếp)
perp_line = [D + DOWN * 10, D + UP * 10]
CD_line   = [C + (C - D) * 10, D + (D - C) * 10]   # đường thẳng CD kéo dài
# Giao AC với đường vuông góc tại D:
E = line_intersection([A, C], perp_line)  # giao điểm E = AC ∩ perp_D
F = line_intersection([B, C], perp_line)  # giao điểm F = BC ∩ perp_D

# Tiếp tuyến tại C (vuông góc với OC)
vec_OC = C - O
tan_vec = np.array([-vec_OC[1], vec_OC[0], 0])   # xoay 90° ngược chiều kim
tan_start = C - tan_vec * 3
tan_end   = C + tan_vec * 3

# Điểm I = tiếp tuyến tại C cắt AB (hoặc đường thẳng AB)
AB_line = [A + LEFT * 5, B + RIGHT * 5]
I = line_intersection([tan_start, tan_end], AB_line)
```

---

## 2. Mobject mẫu

```python
# Hình cơ bản
semicircle       = Arc(radius=R, start_angle=0, angle=PI, color=COLOR_CIRCLE)
seg_AB           = Line(A, B, color=COLOR_DEFAULT)

dot_O, label_O   = Dot(O, color=COLOR_DEFAULT, radius=0.06), MathTex("O").next_to(O, DOWN, buff=0.2)
dot_A, label_A   = Dot(A, color=COLOR_DEFAULT, radius=0.06), MathTex("A").next_to(A, UL, buff=0.1)
dot_B, label_B   = Dot(B, color=COLOR_DEFAULT, radius=0.06), MathTex("B").next_to(B, UR, buff=0.1)
dot_C, label_C   = Dot(C, color=COLOR_DEFAULT, radius=0.06), MathTex("C").next_to(C, UR, buff=0.1)
dot_D, label_D   = Dot(D, color=COLOR_DEFAULT, radius=0.06), MathTex("D").next_to(D, DOWN, buff=0.2)

# Nét phụ
seg_AC           = Line(A, C, color=COLOR_DEFAULT)
seg_BC           = Line(B, C, color=COLOR_DEFAULT)
line_EF_obj      = Line(E + UP * 0.2, F + DOWN * 0.2, color=COLOR_AUX_LINE)  # DH ⊥ AB kéo dài
tangent_line_obj = Line(tan_start, tan_end, color=COLOR_TANGENT)

dot_E, label_E   = Dot(E, color=COLOR_AUX_LINE, radius=0.06), MathTex("E").next_to(E, LEFT, buff=0.1)
dot_F, label_F   = Dot(F, color=COLOR_AUX_LINE, radius=0.06), MathTex("F").next_to(F, RIGHT, buff=0.1)
dot_I, label_I   = Dot(I, color=COLOR_TANGENT, radius=0.06), MathTex("I").next_to(I, DOWN, buff=0.2)

# Góc vuông tại D (CD ⊥ AB)
from manim import RightAngle
from manim_helpers import COLOR_RIGHT_ANGLE
ra_D = RightAngle(seg_AB, line_EF_obj, length=0.28, quadrant=(-1, 1), color=COLOR_RIGHT_ANGLE)

# Góc vuông tại C (ACB nội tiếp nửa đường tròn = 90°)
ra_C = RightAngle(seg_AC, seg_BC, length=0.28, quadrant=(-1, -1), color=COLOR_RIGHT_ANGLE)
```

---

## 3. VGroup và diagram layout

```python
base_geom = VGroup(
    semicircle, seg_AB,
    dot_O, label_O, dot_A, label_A, dot_B, label_B,
)
group_a = VGroup(
    dot_C, label_C, dot_D, label_D,
    seg_AC, seg_BC, line_EF_obj,
    dot_E, label_E, dot_F, label_F,
    ra_D, ra_C,
)
group_b = VGroup(tangent_line_obj, dot_I, label_I)

diagram_elements = VGroup(base_geom, *group_a, *group_b)
self.diagram = diagram_elements.scale(0.8).shift(RIGHT * 4.0 + DOWN * 1.0)
```

---

## 4. Các định lý thường dùng

| Định lý                    | Phát biểu ngắn                                      | Khi nào dùng                    |
|----------------------------|-----------------------------------------------------|---------------------------------|
| Góc nội tiếp nửa đường tròn | `∠ACB = 90°` (C trên nửa đường tròn, AB đường kính) | Chứng minh góc vuông tại C      |
| Tiếp tuyến ⊥ bán kính      | `OC ⊥ tiếp tuyến tại C`                             | Tìm hướng tiếp tuyến            |
| Góc tiếp tuyến–dây cung    | Góc tiếp tuyến–dây = góc nội tiếp cùng cung          | Liên hệ tiếp tuyến / góc nội tiếp |
| Power of a point           | `ID² = IA · IB` (I ngoài đường tròn)                 | Chứng minh tích đoạn thẳng      |
| Hai tiếp tuyến từ 1 điểm   | `IA = IB` (I ngoài, 2 tiếp tuyến)                    | Đẳng cự từ điểm ngoài           |

---

## 5. Scene sequence điển hình

```
Scene 01: Intro + dựng hình
  → Create base_geom → Create group_a → FadeIn group_b
  → Hiện GT/KL
  → persistent_geom = VGroup(base_geom, *group_a, *group_b)

Scene 02: CM ý a — VD: IE = IC
  → Dùng RightAngle ra_D, ra_C để highlight góc vuông
  → Dùng geo.show_congruence("triangle", "ECI", "DCI") hoặc sync_triangle
  → result_a = VGroup(pf_result, box_a)

Scene 03: CM ý b — VD: IE² + IF² = EF²
  → Áp dụng Pytago: IE² + IF² = EF² từ tam giác EIF vuông tại I
  → geo.highlight_angle("EIF") để highlight góc vuông tại I
  → result_b = VGroup(pf_result, box_b)
```

---

## 6. Lỗi thường gặp và cách tránh

| Lỗi                              | Nguyên nhân                         | Cách tránh                                      |
|----------------------------------|-------------------------------------|-------------------------------------------------|
| `ra_C` sai góc phần tư           | `quadrant` sai hướng vector AC, BC  | Quy tắc mục 3 `SKILL-hinh-phang`                |
| `line_intersection` trả `None`   | Hai đường thẳng song song           | `if I is not None` trước khi tạo Dot            |
| Tiếp tuyến quá ngắn              | `tan_start/tan_end` scale nhỏ       | Nhân `tan_vec` hệ số 3–4, `scale` cùng diagram  |
| C gần A hoặc B                   | `C_angle` < 15° hoặc > 165°         | Chọn `C_angle` trong 30°–150°                   |
