---
name: manim-problem-inscribed-angle
description: Pattern code Manim cho bài toán góc nội tiếp, góc tâm, tứ giác nội tiếp và cung. Dùng khi cần đặt nhiều điểm trên đường tròn và chứng minh quan hệ góc.
---

# Pattern: Góc Nội Tiếp / Góc Tâm / Cung

## Dạng bài điển hình

Bài toán liên quan đến: góc nội tiếp và góc tâm cùng chắn cung, hai góc nội tiếp bằng nhau (cùng chắn cung), góc nội tiếp chắn nửa đường tròn = 90°, tứ giác nội tiếp.

---

## 1. Tọa độ mẫu — nhiều điểm trên đường tròn

```python
import numpy as np
from manim import *
from manim_helpers import COLOR_CIRCLE, COLOR_DEFAULT, COLOR_AUX_LINE

R = 2.5
O = np.array([0.0, 0.0, 0.0])

# Các điểm trên đường tròn — chọn góc để hình đẹp, không trùng nhau
A_angle = 200 * DEGREES   # góc tính từ Ox dương
B_angle = 340 * DEGREES
M_angle =  80 * DEGREES
N_angle = 130 * DEGREES

A = np.array([R * np.cos(A_angle), R * np.sin(A_angle), 0])
B = np.array([R * np.cos(B_angle), R * np.sin(B_angle), 0])
M = np.array([R * np.cos(M_angle), R * np.sin(M_angle), 0])
N = np.array([R * np.cos(N_angle), R * np.sin(N_angle), 0])

# Điểm H = giao điểm hai dây MN và AB (nếu cần)
from manim_helpers import line_intersection
H = line_intersection([M, N], [A, B])

# Đường kính MK (K đối diện M)
K_angle = M_angle + PI
K = np.array([R * np.cos(K_angle), R * np.sin(K_angle), 0])
```

---

## 2. Mobject mẫu

```python
from manim_helpers import LAYER_MARKERS, COLOR_RIGHT_ANGLE

# Đường tròn đầy đủ
circ_O = Circle(radius=R, color=COLOR_CIRCLE).move_to(O)
dot_O  = Dot(O, color=COLOR_DEFAULT, radius=0.06).set_z_index(LAYER_MARKERS)
label_O = MathTex("O").next_to(O, DOWN, buff=0.2).set_z_index(LAYER_MARKERS)

# Các điểm trên đường tròn
def make_point(P, name, direction=UP, color=COLOR_DEFAULT):
    d = Dot(P, color=color, radius=0.06).set_z_index(LAYER_MARKERS)
    l = MathTex(name).next_to(P, direction, buff=0.12).set_z_index(LAYER_MARKERS)
    return d, l

dot_A, label_A = make_point(A, "A", DL)
dot_B, label_B = make_point(B, "B", DR)
dot_M, label_M = make_point(M, "M", UP)
dot_N, label_N = make_point(N, "N", UL)

# Dây cung và nét phụ
seg_MN = Line(M, N, color=COLOR_DEFAULT)
seg_AB = Line(A, B, color=COLOR_DEFAULT)
seg_MA = Line(M, A, color=COLOR_DEFAULT)
seg_MB = Line(M, B, color=COLOR_DEFAULT)

# Bán kính phụ trợ (Loại A nếu cần):
seg_OA = Line(O, A, color=COLOR_AUX_LINE)
seg_OB = Line(O, B, color=COLOR_AUX_LINE)
```

---

## 3. Cung và góc — visualize

```python
from manim_helpers import AngleMarker

# Góc nội tiếp ∠AMB (M trên đường tròn, chắn cung AB không chứa M)
ang_AMB = AngleMarker(M, A, B, radius=0.4, color=COLOR_ACTIVE)

# Góc tâm ∠AOB (tâm O, cùng chắn cung AB)
ang_AOB = AngleMarker(O, A, B, radius=0.5, color=COLOR_SECONDARY)
# Tính: góc tâm = 2 × góc nội tiếp

# Hiển thị cung AB (phần cung không chứa M)
arc_AB = Arc(
    radius=R,
    start_angle=A_angle,
    angle=(B_angle - A_angle) % TAU,   # đi từ A đến B theo chiều dương
    color=COLOR_ACTIVE,
    stroke_width=5,
).move_to(O)
```

---

## 4. Các định lý và pattern chứng minh

### Định lý 1: Hai góc nội tiếp cùng chắn cung → bằng nhau

```
∠AMB = ∠ANB  (M, N đều nằm trên cung lớn AB, cùng phía với cung nhỏ AB)
```

```python
# ProofLine:
pf = ProofLine(
    ("ang_AMB", r"\widehat{AMB}"), ("eq", "="), ("ang_ANB", r"\widehat{ANB}"),
    tex_template=viet_tex_template, font_size=26,
)
col.place_line(pf)
with self.voiceover("Góc A M B bằng góc A N B") as ov:
    sync_angle(self, "m1", pf.write("ang_AMB"), self.geo.highlight_angle("AMB"))
    sync_relation(self, "m2", pf.write("eq"))
    sync_angle(self, "m3", pf.write("ang_ANB"), self.geo.highlight_angle("ANB"))
note = Tex(r"(góc nội tiếp cùng chắn cung $\wideparen{AB}$)",
           tex_template=viet_tex_template, font_size=24)
col.place_note(note); self.play(Write(note))
```

### Định lý 2: Góc tâm = 2 × Góc nội tiếp (cùng chắn cung)

```python
pf = ProofLine(
    ("ang_AOB", r"\widehat{AOB}"), ("eq", "="),
    ("two", "2"), ("ang_AMB", r"\widehat{AMB}"),
    tex_template=viet_tex_template, font_size=26,
)
```

### Định lý 3: Góc nội tiếp chắn nửa đường tròn = 90°

```python
pf = ProofLine(
    ("ang_AMB", r"\widehat{AMB}"), ("eq", "="), ("ninety", r"90^\circ"),
    tex_template=viet_tex_template, font_size=26,
)
note = Tex(r"(góc nội tiếp chắn nửa đường tròn, $AB$ là đường kính)",
           tex_template=viet_tex_template, font_size=24)
```

### Định lý 4: Tứ giác nội tiếp — tổng 2 góc đối = 180°

```python
# △ABMN nội tiếp đường tròn
pf = ProofLine(
    ("ang_A", r"\widehat{A}"), ("plus", "+"), ("ang_M", r"\widehat{M}"),
    ("eq", "="), ("deg180", r"180^\circ"),
    tex_template=viet_tex_template, font_size=26,
)
note = Tex(r"(tứ giác $ABMN$ nội tiếp đường tròn)",
           tex_template=viet_tex_template, font_size=24)
```

---

## 5. Highlight cung — visualize cùng voiceover

```python
# Khi voiceover nhắc "cùng chắn cung AB":
arc_highlight = Arc(
    radius=R,
    start_angle=min(A_angle, B_angle),
    angle=abs(B_angle - A_angle),
    color=COLOR_ACTIVE, stroke_width=6,
).move_to(O).set_z_index(LAYER_HIGHLIGHT)

with self.voiceover("<bookmark mark='arc'/> cùng chắn cung AB") as ov:
    self.wait_until_bookmark("arc")
    self.play(FadeIn(arc_highlight), run_time=TIMING_ANGLE)
    self.play(FadeOut(arc_highlight), run_time=TIMING_ANGLE)
```

---

## 6. Tọa độ góc label — hướng lấy nhãn theo vị trí điểm trên đường tròn

```python
def label_direction_for_circle(angle_rad, R=2.5, label_buff=0.15):
    """Trả về hướng (direction) phù hợp để đặt label cho điểm trên đường tròn."""
    x = np.cos(angle_rad)
    y = np.sin(angle_rad)
    # Đẩy nhãn ra ngoài đường tròn
    return np.array([x, y, 0])

# Dùng:
label_M = MathTex("M").next_to(M, label_direction_for_circle(M_angle), buff=0.15)
```

---

## 7. Scene sequence điển hình

```
Scene 01: Dựng đường tròn + các điểm
  → Create circ_O + dot_O, label_O
  → Create dots và labels từng điểm theo voiceover
  → persistent_geom = VGroup(circ_O, dot_O, label_O, dot_A, label_A, ...)

Scene 02: CM ý a — VD: ∠AMB = ∠ANB
  → sync_angle cho từng góc
  → Highlight cung AB bằng arc_highlight FadeIn → FadeOut
  → result_a = box "∠AMB = ∠ANB"

Scene 03: CM ý b — VD: tứ giác AMNB nội tiếp
  → Dùng kết quả scene 02
  → Chứng minh tổng góc đối = 180°
  → result_b = box kết luận
```

---

## 8. Lỗi thường gặp

| Lỗi                                    | Nguyên nhân                    | Cách tránh                                    |
|----------------------------------------|--------------------------------|-----------------------------------------------|
| Arc `start_angle` / `angle` sai chiều  | Góc ngược chiều kim đồng hồ    | Vẽ thử preview chất lượng thấp                |
| Hai điểm trùng / ngược trên đường tròn | `A_angle ≈ B_angle ± π`        | Chọn góc cách nhau ≥ 30°                      |
| Label điểm bị đè bởi đường tròn         | Thiếu `set_z_index` cho label  | `label.set_z_index(LAYER_MARKERS)`            |
| Góc nội tiếp sai hướng                 | `AngleMarker` sai thứ tự điểm  | `AngleMarker(vertex, p1, p2)` — vertex = đỉnh |
