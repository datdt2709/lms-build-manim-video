---
name: manim-problem-triangle-congruence
description: Pattern code Manim cho bài toán chứng minh hai tam giác bằng nhau hoặc đồng dạng (c.g.c / g.c.g / c.c.c). Dùng khi cần tọa độ mẫu, highlight tam giác và narration TTS.
---

# Pattern: Tam Giác Bằng Nhau / Đồng Dạng

## Dạng bài điển hình

Bài toán chứng minh hai tam giác bằng nhau (c.g.c / g.c.g / c.c.c) hoặc đồng dạng, rồi suy ra đẳng thức đoạn thẳng / góc.

---

## 1. Tọa độ mẫu — tam giác với đường phân giác / trung tuyến

```python
import numpy as np
from manim import *
from manim_helpers import line_intersection, COLOR_DEFAULT, COLOR_AUX_LINE, COLOR_SECONDARY

# Tam giác ABC cơ bản — điều chỉnh để hình đẹp
A = np.array([-2.5,  0.0, 0])
B = np.array([ 2.5,  0.0, 0])
C = np.array([ 0.5,  3.0, 0])

# Trung điểm
M = (A + B) / 2   # trung điểm AB
N = (B + C) / 2   # trung điểm BC

# Đường cao từ C xuống AB
foot_line = [A + DOWN * 10, A + UP * 10]
AB_line   = [A + LEFT * 10, B + RIGHT * 10]
H = line_intersection([C, C + np.array([0, -10, 0])], AB_line)
# hoặc tính trực tiếp:
AB_vec   = B - A
H_param  = np.dot(C - A, AB_vec) / np.dot(AB_vec, AB_vec)
H        = A + H_param * AB_vec

# Điểm D đối xứng C qua M (AB):
D = 2 * M - C    # hoặc: D = A + B - C (nếu ABDC là hình bình hành)
```

---

## 2. Mobject mẫu — tam giác + điểm + nét phụ

```python
from manim_helpers import COLOR_RIGHT_ANGLE, LAYER_MARKERS
from manim import RightAngle

# Tam giác chính (chỉ dựng; highlight bằng GeometryEngine)
tri_ABC  = Polygon(A, B, C, color=COLOR_DEFAULT)

# Điểm và nhãn (luôn set_z_index(LAYER_MARKERS))
dot_A, label_A = Dot(A, color=COLOR_DEFAULT, radius=0.06).set_z_index(LAYER_MARKERS), \
                 MathTex("A").next_to(A, DL, buff=0.1).set_z_index(LAYER_MARKERS)
dot_B, label_B = Dot(B, color=COLOR_DEFAULT, radius=0.06).set_z_index(LAYER_MARKERS), \
                 MathTex("B").next_to(B, DR, buff=0.1).set_z_index(LAYER_MARKERS)
dot_C, label_C = Dot(C, color=COLOR_DEFAULT, radius=0.06).set_z_index(LAYER_MARKERS), \
                 MathTex("C").next_to(C, UP, buff=0.1).set_z_index(LAYER_MARKERS)

# Nét phụ trợ (Loại A: Create vĩnh viễn + persistent_geom.add)
seg_CH  = Line(C, H, color=COLOR_AUX_LINE)   # đường cao
dot_H   = Dot(H, color=COLOR_AUX_LINE, radius=0.06).set_z_index(LAYER_MARKERS)
label_H = MathTex("H").next_to(H, DOWN, buff=0.15).set_z_index(LAYER_MARKERS)

# Góc vuông tại H
ra_H = RightAngle(
    Line(A, B), Line(C, H),
    length=0.28, quadrant=(1, 1),   # điều chỉnh quadrant theo vị trí H
    color=COLOR_RIGHT_ANGLE,
)
```

---

## 3. Template chứng minh c.g.c

```python
# Chứng minh △OAC = △OBC (c.g.c)
#   OA = OB (bán kính)
#   ∠AOC = ∠BOC (OC là phân giác)
#   OC chung

# ProofLine pattern:
pf_01 = ProofLine(
    ("seg_OA", "OA"), ("eq", "="), ("seg_OB", "OB"),
    tex_template=viet_tex_template, font_size=26,
)
col.place_line(pf_01)
with self.voiceover("OA bằng OB vì cùng là bán kính") as ov:
    sync_segment(self, "seg_OA_mark", pf_01.write("seg_OA"), self.geo.highlight_segment("OA"))
    sync_relation(self, "eq_mark",    pf_01.write("eq"))
    sync_segment(self, "seg_OB_mark", pf_01.write("seg_OB"), self.geo.highlight_segment("OB"))

note_01 = Tex(r"(bán kính)", tex_template=viet_tex_template, font_size=24)
col.place_note(note_01); self.play(Write(note_01))

pf_02 = ProofLine(
    ("ang_AOC", r"\widehat{AOC}"), ("eq", "="), ("ang_BOC", r"\widehat{BOC}"),
    tex_template=viet_tex_template, font_size=26,
)
col.place_line(pf_02)
# ... voiceover ...

note_02 = Tex(r"(OC là phân giác $\widehat{AOB}$)", tex_template=viet_tex_template, font_size=24)
col.place_note(note_02); self.play(Write(note_02))

# Kết luận c.g.c
pf_result = ProofLine(
    ("imp",     r"\Rightarrow"),
    ("tri_OAC", r"\triangle OAC"),
    ("eq",      "="),
    ("tri_OBC", r"\triangle OBC"),
    ("cgc",     r"\;(c.g.c)"),
    tex_template=viet_tex_template, font_size=26,
)
col.place_line(pf_result)
box = SurroundingRectangle(pf_result, color=COLOR_RESULT_KEY, buff=0.15)
self.play(pf_result.write_all(), Create(box))
```

---

## 4. Bảng trường hợp bằng nhau và code pattern

### c.g.c (cạnh–góc–cạnh)

```python
# Cần: 2 cạnh kẹp góc, góc chung hoặc bằng nhau
pf_cgc = ProofLine(
    ("tri_X", r"\triangle ABC"), ("eq", "="), ("tri_Y", r"\triangle DEF"),
    ("rule", r"\;(c.g.c)"),
    tex_template=viet_tex_template, font_size=26,
)
# Dùng geo.show_congruence để highlight visually:
self.geo.show_congruence("cgc", "ABC", "DEF",
                          equal_sides=[("AB","DE"), ("BC","EF")],
                          equal_angle="B")
```

### g.c.g (góc–cạnh–góc)

```python
pf_gcg = ProofLine(
    ("tri_X", r"\triangle ABC"), ("eq", "="), ("tri_Y", r"\triangle DEF"),
    ("rule", r"\;(g.c.g)"),
    tex_template=viet_tex_template, font_size=26,
)
```

### c.c.c (cạnh–cạnh–cạnh)

```python
pf_ccc = ProofLine(
    ("tri_X", r"\triangle ABC"), ("eq", "="), ("tri_Y", r"\triangle DEF"),
    ("rule", r"\;(c.c.c)"),
    tex_template=viet_tex_template, font_size=26,
)
```

---

## 5. Tam giác đồng dạng

```python
# △ABC ∽ △DEF (g.g hoặc c.g.c đồng dạng)
pf_similar = ProofLine(
    ("tri_X", r"\triangle ABC"), ("similar", r"\sim"), ("tri_Y", r"\triangle DEF"),
    tex_template=viet_tex_template, font_size=26,
)
# Suy ra tỉ lệ:
pf_ratio = ProofLine(
    ("frac_AB", r"\dfrac{AB}{DE}"),
    ("eq",      "="),
    ("frac_BC", r"\dfrac{BC}{EF}"),
    ("eq2",     "="),
    ("frac_AC", r"\dfrac{AC}{DF}"),
    tex_template=viet_tex_template, font_size=26,
)
```

---

## 6. GeometryEngine — highlight tam giác

```python
# Highlight một tam giác (Polygon fill tạm)
self.geo.show_triangle("ABC")                          # fill COLOR_EQUAL_1

# So sánh hai tam giác bằng nhau (fill màu khác nhau)
self.geo.compare_triangles("OAC", "OBC")               # fill COLOR_EQUAL_1 và COLOR_EQUAL_2

# Show tick marks trên cạnh bằng nhau
self.geo.show_equal_segments([("AB", "DE"), ("AC", "DF")])

# Show angle arc cho góc bằng nhau
self.geo.show_equal_angles([("BAC", "EDF")])
```

---

## 7. Scene sequence điển hình

```
Scene 01: Dựng tam giác + điểm phụ
  → Create tri_ABC + dots + labels + segs
  → persistent_geom = VGroup(tri_ABC, dots, labels, ...)

Scene 02: CM ý a — VD: △OAC = △OBC
  → Từng ProofLine với sync_segment / sync_angle
  → geo.compare_triangles("OAC", "OBC")
  → result_a = box "△OAC = △OBC"

Scene 03: CM ý b — hệ quả từ bằng nhau
  → Dùng result_a làm tiền đề (self.result_a còn trên màn hình)
  → ProofLine suy ra đẳng thức đoạn / góc
  → result_b = box kết luận b
```

---

## 8. Lỗi thường gặp

| Lỗi                              | Nguyên nhân                          | Cách tránh                              |
|----------------------------------|--------------------------------------|-----------------------------------------|
| Thứ tự đỉnh sai trong (c.g.c)    | `△ABC = △DEF` nhưng AB ↔ EF sai      | Viết đúng thứ tự đỉnh tương ứng         |
| Highlight sai tam giác           | `geo.compare_triangles` sai tên      | Kiểm tra `register_triangle` đã đăng ký |
| Thiếu dấu tick trên cạnh bằng    | Không gọi `show_equal_segments`      | Gọi khi voiceover nhắc cạnh bằng        |
| Góc chứng minh thiếu             | Chỉ chứng minh 2/3 điều kiện          | Kiểm tra đủ 3 điều kiện trước kết luận  |
