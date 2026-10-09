---
name: manim-hinh-phang
description: Dựng hình phẳng 2D (tam giác, đường tròn, tiếp tuyến, góc nội tiếp). Dùng khi bài toán hình học phẳng cần tính tọa độ, tạo Mobject và ghép VGroup.
---

# Skill: Manim – Hình Phẳng (Geometry 2D)

## Khi nào dùng skill này?

Dùng khi bài toán liên quan đến **hình học phẳng**: tam giác, đường tròn, tiếp tuyến, góc nội tiếp, trung điểm, cát tuyến, v.v.

Skill này tập trung vào **dựng hình** (tính tọa độ, tạo Mobject, ghép VGroup, scene pattern). Các nội dung sau đã được tách ra skill riêng — đọc thêm khi cần:

| Nội dung                                              | Skill phụ trách                                      |
|-------------------------------------------------------|------------------------------------------------------|
| TeX template tiếng Việt, cấu trúc class chung         | `.cursor/rules/manim-global.mdc`                     |
| `COLOR_*`, `TIMING_*`, `LAYER_*`, naming convention   | `manim/primitives/design-tokens/SKILL.md`            |
| Bookmark granularity, `ProofLine`, `sync_<type>`      | `manim/primitives/proof-sync/SKILL.md`             |
| `AngleMarker`, `GeometryEngine`, quy tắc màu highlight| `manim/primitives/geometry-engine/SKILL.md`          |
| `persistent_geom`, FadeOut rules, `proof_accumulator` | `manim/primitives/scene-lifecycle/SKILL.md`          |
| `ProofColumn`, cursor management, layout màn hình     | `manim/primitives/layout-system/SKILL.md`            |
| Templates dạng bài: tiếp tuyến, tam giác, góc nội tiếp| `manim/patterns/` (circle-tangent, inscribed-angle, …) |

---

## 1. Helper bắt buộc – import từ `manim_helpers`

Helper hình học (`line_intersection`, `cross2d`, `angle_between_vectors`) đã chuyển sang package `manim_helpers/geo_engine.py`. KHÔNG còn copy-paste vào module level mỗi project.

```python
from manim_helpers import (
    line_intersection, cross2d, angle_between_vectors,
    AngleMarker, GeometryEngine, ProofLine, ProofColumn,
    sync_point, sync_segment, sync_angle, sync_triangle, sync_quadrilateral, sync_relation,
    COLOR_DEFAULT, COLOR_CIRCLE, COLOR_ACTIVE, COLOR_SECONDARY, COLOR_AUX_LINE,
    COLOR_RIGHT_ANGLE, COLOR_TANGENT, COLOR_EQUAL_1, COLOR_EQUAL_2, COLOR_EQUAL_3,
    COLOR_RESULT_KEY, COLOR_RESULT_FINAL,
    TIMING_FADE, TIMING_PROOF_WRITE, TIMING_CONCLUSION,
    LAYER_GEOMETRY, LAYER_MARKERS, LAYER_PROOF_TEXT,
)
```

---

## 2. Tính toán tọa độ hình học cơ bản

### Quy tắc bắt buộc — điểm trên đường tròn

Điểm nằm **trên** đường tròn tâm `O` bán kính `R` phải tính bằng góc, ví dụ `P = O + np.array([R*np.cos(theta), R*np.sin(theta), 0])` (hoặc tương đương với `O = ORIGIN`). **Không** hardcode tọa độ thập phân xấp xỉ rồi giả định điểm thuộc đường tròn — sai vài phần trăm đã làm lệch toàn bộ giao điểm / đường cao sau này. Sau khi chọn góc, có thể tự kiểm tra `np.linalg.norm(P - O)` bằng `R`.

### Đường tròn và nửa đường tròn

```python
R = 2.5
O = ORIGIN          # hoặc np.array([0, 0, 0])
A = LEFT * R        # Điểm trái đường kính
B = RIGHT * R       # Điểm phải đường kính

# Điểm C trên nửa đường tròn (góc tính từ trục Ox)
C_angle = 70 * DEGREES
C = np.array([R * np.cos(C_angle), R * np.sin(C_angle), 0])

# Tiếp tuyến tại C (vuông góc với OC)
vec_OC = C - O
tangent_vec = np.array([-vec_OC[1], vec_OC[0], 0])  # Xoay 90°
tangent_start = C - tangent_vec * 10
tangent_end   = C + tangent_vec * 10
```

### Giao điểm điển hình

```python
D = LEFT * 1.0  # Điểm D trên đường kính AB

perp_line = [D + DOWN * 10, D + UP * 10]

E = line_intersection([A, C], perp_line)
F = line_intersection([B, C], perp_line)
I = line_intersection(perp_line, [tangent_start, tangent_end])
```

---

## 3. Các Mobject hình học cơ bản

> Mọi `color=` dùng `COLOR_*` token (xem `manim-design-tokens`). Mọi `set_z_index(...)` dùng `LAYER_*` token. Tên biến tuân naming convention `dot_<X>`, `seg_<XY>`, `ra_<X>`, `circ_<NAME>`.

### Đường tròn / nửa đường tròn

```python
semicircle  = Arc(radius=R, start_angle=0, angle=PI, color=COLOR_CIRCLE)
circ_O      = Circle(radius=R, color=COLOR_CIRCLE).move_to(O)
seg_AB      = Line(A, B, color=COLOR_DEFAULT)   # đường kính
```

### Đoạn thẳng, điểm, nhãn

```python
dot_O   = Dot(O, color=COLOR_ACTIVE,    radius=0.06).set_z_index(LAYER_MARKERS)
dot_C   = Dot(C, color=COLOR_DEFAULT,   radius=0.06).set_z_index(LAYER_MARKERS)
label_O = MathTex("O").next_to(O, DOWN, buff=0.2).set_z_index(LAYER_MARKERS)
label_C = MathTex("C").next_to(C, UR,   buff=0.1).set_z_index(LAYER_MARKERS)

seg_AC  = Line(A, C, color=COLOR_DEFAULT)
seg_BC  = Line(B, C, color=COLOR_DEFAULT)
seg_EF  = Line(E, F, color=COLOR_AUX_LINE)
seg_CI  = Line(C, I, color=COLOR_TANGENT)
```

### Quy tắc z-index bắt buộc

Đoạn thẳng / cung mặc định `z_index = 0`. Nếu tạo Dot/label **sau** khi Create line, chúng sẽ bị line đè lên. Luôn áp dụng:

```python
# LUÔN set z_index = LAYER_MARKERS cho mọi Dot và label
dot_A   = Dot(A, color=COLOR_DEFAULT, radius=0.06).set_z_index(LAYER_MARKERS)
dot_D   = Dot(D, color=COLOR_DEFAULT, radius=0.06).set_z_index(LAYER_MARKERS)
label_A = MathTex("A").next_to(A, UL, buff=0.1).set_z_index(LAYER_MARKERS)

seg_AB  = Line(A, B, color=COLOR_DEFAULT)   # z_index=0 (LAYER_GEOMETRY ngầm) → nằm dưới dot
```

### Thứ tự trong VGroup và tách animation – bắt buộc

**Vấn đề**: Dù đã set `z_index=LAYER_MARKERS`, khi `Create(VGroup(...))` cùng lúc, Manim vẫn có thể render line đè lên dot nếu dot xuất hiện *trước* line trong VGroup. `z_index` chỉ có tác dụng khi cả hai đã add vào scene.

**Giải pháp – áp dụng cả 3**:

**(1) Trong VGroup: luôn đặt Dot/label SAU tất cả Line/Arc:**

```python
# SAI – dot_H xuất hiện trước line_OA → bị đè
bad_group = VGroup(dot_O, dot_H, label_H, seg_OA, seg_AB)   # ❌

# ĐÚNG – toàn bộ line trước, dot/label sau cùng
good_group = VGroup(seg_OA, seg_AB, dot_O, dot_H, label_H)  # ✓
```

**(2) Tách animation: Create lines trước, rồi mới Create dots/labels:**

```python
# SAI
self.play(Create(VGroup(seg_OA, dot_H, label_H)))             # ❌
# ĐÚNG
self.play(Create(seg_OA))
self.play(Create(dot_H), Write(label_H))                       # ✓
```

**(3) `bring_to_front` sau khi add tất cả vào scene (phòng thủ):**

```python
all_dots   = [dot_O, dot_A, dot_B, dot_C, dot_H, dot_M]
all_labels = [label_O, label_A, label_B, label_C, label_H, label_M]
self.bring_to_front(*all_dots, *all_labels)
```

### Junction dots – bắt buộc

Mỗi điểm giao / đầu nối giữa các đoạn **bắt buộc** có `Dot` riêng, dù đã là endpoint của một line.

```python
dot_D = Dot(D, color=COLOR_DEFAULT,    radius=0.06).set_z_index(LAYER_MARKERS)
dot_E = Dot(E, color=COLOR_AUX_LINE,   radius=0.06).set_z_index(LAYER_MARKERS)
dot_F = Dot(F, color=COLOR_AUX_LINE,   radius=0.06).set_z_index(LAYER_MARKERS)
```

### Tam giác (Polygon) – chỉ dựng, không highlight ở đây

```python
tri_ABC = Polygon(A, B, C, color=COLOR_DEFAULT)
```

> Highlight tam giác (Polygon fill, `show_congruence`, `compare_triangles`) → dùng `GeometryEngine`. Xem `manim-geometry-engine`.

### Góc và RightAngle

```python
ra_D = RightAngle(
    seg_AB,            # Line 1
    line_EF_obj,       # Line 2
    length=0.3,
    quadrant=(-1, 1),
    color=COLOR_RIGHT_ANGLE,
)
ra_C = RightAngle(seg_AC, seg_BC, length=0.3, quadrant=(-1, -1), color=COLOR_RIGHT_ANGLE)
```

> Highlight 1 góc / cặp góc bằng nhau / tổng góc → dùng `AngleMarker(...)` từ `manim-geometry-engine`, KHÔNG xài `Sector(...)` thủ công + boilerplate `cross2d`.

### Quy tắc xác định `quadrant` cho RightAngle

`quadrant=(sx, sy)` xác định góc vuông nằm về phía nào so với giao điểm:

1. Tính vector chỉ hướng của **Line 1**: `v1 = end1 - start1`
2. Tính vector chỉ hướng của **Line 2**: `v2 = end2 - start2`
3. `sx = sign(v1.x)` nếu muốn góc nằm cùng hướng x với Line 1, ngược lại `-sign(v1.x)`
4. `sy = sign(v2.y)` nếu muốn góc nằm cùng hướng y với Line 2, ngược lại `-sign(v2.y)`

**Ví dụ**:

```python
# diameter = Line(A, B) → v1.x > 0
# line_EF  = Line(E, F) → v2.y > 0
# Góc vuông ở góc trên-TRÁI giao điểm D: sx = -1, sy = +1
ra_D = RightAngle(seg_AB, line_EF_obj, length=0.3, quadrant=(-1, 1),
                  color=COLOR_RIGHT_ANGLE)

# segment_AC: A(trái) → C(trên phải): v1.x>0, v1.y>0
# segment_BC: B(phải) → C(trên trái): v2.x<0, v2.y>0
# Góc ACB ở góc dưới-trái của C → quadrant=(-1, -1)
ra_C = RightAngle(seg_AC, seg_BC, length=0.3, quadrant=(-1, -1),
                  color=COLOR_RIGHT_ANGLE)
```

Nếu vẫn sai, thử lần lượt `(1,1)`, `(-1,1)`, `(1,-1)`, `(-1,-1)` và render preview.

---

## 4. Nhóm hình – VGroup với index cố định

```python
base_geom = VGroup(semicircle, seg_AB, dot_O, label_O, dot_A, label_A, dot_B, label_B)
# Index:        [0]          [1]     [2]     [3]      [4]     [5]      [6]     [7]

diagram_elements = VGroup(
    base_geom,            # [0]
    dot_C, label_C,       # [1], [2]
    dot_D, label_D,       # [3], [4]
    seg_AC,               # [5]
    seg_BC,               # [6]
    line_EF_obj,          # [7]
    dot_E, label_E,       # [8], [9]
    dot_F, label_F,       # [10], [11]
    tangent_line_obj,     # [12]
    dot_I, label_I,       # [13], [14]
    ra_D,                 # [15]
    ra_C,                 # [16]
)

self.diagram = diagram_elements.scale(0.8).shift(RIGHT * 4.0, DOWN * 1.0)
```

Lưu các Dot quan trọng riêng:

```python
self.dot_C = dot_C
self.dot_D = dot_D
self.dot_E = dot_E
self.dot_F = dot_F
self.dot_I = dot_I
```

---

## 5. Ràng buộc vẽ hình theo từng ý

> **QUY TẮC BẮT BUỘC**: Dữ kiện của **ý nào** thì chỉ dựng hình cho **ý đó**. Không vẽ trước phần tử chưa được đề cập trong dữ kiện của ý hiện tại.

### Phân tách dữ kiện

| Ý  | Dữ kiện sử dụng                    | Phần tử được vẽ                    |
|----|------------------------------------|------------------------------------|
| a) | GT chung + các điểm liên quan ý a  | Chỉ Mobject của ý a                |
| b) | GT chung + các điểm liên quan ý b  | Thêm (FadeIn) Mobject mới của ý b  |
| c) | GT chung + ...                     | Tương tự                           |

### Phân biệt hai loại nét phụ trợ

- **Loại A – Nét hình học mới** (cạnh tam giác mới, đường cao, đường nối hai điểm đã có): `Create()` vĩnh viễn, đặt tên `seg_*`, lưu `self.seg_*`. **KHÔNG có** `FadeOut`. Sau Create, gọi `bring_to_front` cho dot/label bị che. **Bắt buộc** thêm vào `self.persistent_geom`.
- **Quy tắc side completeness:** Mọi tam giác / tứ giác đã `register_triangle` / `register_quadrilateral` mà **cạnh chưa đủ** trên diagram (chưa có `Line` tương ứng trong `geo` / chưa `Create` vĩnh viễn) phải bổ sung **Loại A** trước khi gọi `sync_triangle` / `sync_quadrilateral` hoặc `geo.highlight_triangle` / `geo.show_congruence` / `geo.compare_triangles`: dùng `geo.get_missing_sides("TênTamGiacHoacTuGiac")`; nếu danh sách khác rỗng thì `geo.create_missing_sides(...)` rồi `Create` từng cạnh + `persistent_geom.add` (xem `manim-geometry-engine`).
- **Quy tắc angle completeness:** Góc ∠XYZ (đỉnh tại `Y`) được nhắc trong chứng minh và cần **cả hai nét** `Y–X` và `Y–Z` trên màn hình (hoặc sẽ `sync_segment` / `highlight_segment` lên hai tia) thì hai đoạn đó phải là Loại A đã `Create` — thường đã được bao phủ nếu đã `create_missing_sides` cho tam giác chứa góc; nếu không, vẽ thêm hai `Line` + `register_segment` (mô tả đầy đủ → `manim-geometry-engine` mục **Angle completeness**).
- **Loại B – Highlight tạm** (Polygon fill màu, `Sector` góc, đổi màu tạm): dùng `sync_*()` từ `manim-proof-sync` hoặc `geo.show_*` từ `manim-geometry-engine`. KHÔNG `Indicate(...)` / `FadeIn(Sector(...))` thủ công.

### Cách triển khai

```python
# ---- Tính tọa độ TẤT CẢ điểm (chỉ tính, chưa tạo Mobject) ----
R, O, A, B, C = ...

# Điểm CHỈ dùng ở ý a):
D = ...
E, F = line_intersection(...), line_intersection(...)

# Điểm CHỈ dùng ở ý b):
I = line_intersection(...)

# ---- Tạo Mobject theo từng nhóm ý ----
base_geom = VGroup(semicircle, seg_AB, dot_O, label_O, dot_A, label_A, dot_B, label_B)
group_a   = VGroup(dot_C, label_C, dot_D, label_D, seg_AC, seg_BC, line_EF_obj,
                   dot_E, label_E, dot_F, label_F, ra_D, ra_C)
group_b   = VGroup(tangent_line_obj, dot_I, label_I)
```

```python
def scene01_introVaDeBai(self):
    with self.voiceover(text="Cho nửa đường tròn tâm O bán kính R...") as ov:
        self.play(Create(base_geom), run_time=ov.duration * 0.8)

    with self.voiceover(text="Ý a: Lấy điểm C trên nửa đường tròn, D trên AB...") as ov:
        self.play(Create(group_a), run_time=ov.duration * 0.8)

    with self.voiceover(text="Ý b: Kẻ tiếp tuyến tại C cắt AB tại I...") as ov:
        self.play(FadeIn(group_b), run_time=ov.duration * 0.8)

    # SAU KHI CREATE XONG TOÀN BỘ HÌNH — khởi tạo persistent_geom
    # (Xem manim-scene-lifecycle cho chi tiết persistent_geom management)
    self.persistent_geom = VGroup(
        base_geom,
        *group_a,
        *group_b,
    )
```

### Lỗi cần tránh

```python
# SAI – vẽ điểm I (chỉ dùng ở ý b) ngay trong base_geom:
base_geom = VGroup(semicircle, seg_AB, ..., tangent_line_obj, dot_I, label_I)  # ❌

# ĐÚNG – chỉ vẽ I khi voiceover đề cập ý b:
# scene intro: Create(base_geom) + Create(group_a)
# scene b hoặc cuối scene intro: FadeIn(group_b)              # ✓
```

---

## 6. Pattern Scene 01 – Dựng hình từng bước

> Phần voiceover bookmark + Write proof line chi tiết — xem `manim-proof-sync`. Phần dưới đây tập trung vào **dựng hình + GT/KL**, không lặp lại bookmark rules.

```python
def scene01_introVaDeBai(self):
    # --- A. Intro title ---
    with self.voiceover(text="Chào các em!...") as ov:
        title1 = Text("Tiêu đề bài giảng", font="Times New Roman",
                      weight=BOLD, font_size=48)
        self.play(Write(title1), run_time=ov.duration * 0.4)
        self.play(FadeOut(title1), run_time=ov.duration * 0.2)

    # --- B. GT/KL ---
    self.gt_vgroup = VGroup(
        Tex(r"\textbf{Cho (Giả thiết):}", tex_template=viet_tex_template, font_size=40),
        Tex(r"- Điều kiện 1.", tex_template=viet_tex_template, font_size=36),
        Tex(r"- Điều kiện 2.", tex_template=viet_tex_template, font_size=36),
    ).arrange(DOWN, aligned_edge=LEFT, buff=0.2).to_corner(UL, buff=0.5)

    self.kl_vgroup = VGroup(
        Tex(r"\textbf{Chứng minh (Kết luận):}", tex_template=viet_tex_template, font_size=40),
        Tex(r"a) Kết luận a.", tex_template=viet_tex_template, font_size=36),
    ).arrange(DOWN, aligned_edge=LEFT, buff=0.2).next_to(
        self.gt_vgroup, DOWN, buff=0.5, aligned_edge=LEFT
    )

    # --- C. Tính tọa độ (numpy, không animate) ---
    # ... base_geom, group_a, group_b ...

    # --- D. Tạo Mobject + scale + shift ---
    self.diagram = diagram_elements.scale(0.8).shift(RIGHT * 4.0, DOWN * 1.0)

    # --- E. Init GeometryEngine cho mọi scene sau dùng ---
    self.geo = GeometryEngine(self)
    self.geo.register_point("O", O); self.geo.register_point("A", A)
    self.geo.register_point("B", B); self.geo.register_point("C", C)
    self.geo.register_segment("AC", seg_AC)
    self.geo.register_segment("BC", seg_BC)

    # --- F. Dựng hình theo từng ý ---
    with self.voiceover(text="Cho nửa đường tròn tâm O...") as ov:
        gt_part1 = VGroup(*self.gt_vgroup.get_submobjects()[:3])
        self.play(Write(gt_part1), run_time=ov.duration * 0.1)
        run_t = ov.duration * 0.8 / 5
        self.play(Create(self.diagram[0]), run_time=run_t)
        self.play(Create(self.diagram[1]), Write(self.diagram[2]), run_time=run_t)

    # --- G. Hiện KL ---
    self.play(Write(self.kl_vgroup.get_submobjects()[0]))
    with self.voiceover(text="Yêu cầu a)...") as ov:
        focus_a = self.kl_vgroup.get_submobjects()[1]
        self.play(Write(focus_a), run_time=ov.duration * 0.7)
        self.play(Indicate(focus_a, scale_factor=1.2), run_time=0.8)
```

---

## 7. Pattern Scene chứng minh – Cấu trúc chuẩn

> Phần Write proof + sync_* — xem `manim-proof-sync`. Phần `geo.show_*` — xem `manim-geometry-engine`. Quản lý cursor/cột proof — xem `manim-layout-system` (`ProofColumn`). Lifecycle/FadeOut — xem `manim-scene-lifecycle`.

```python
def scene02_chungMinhBuoc1(self):
    # 1. Dọn dẹp scene trước
    self.play(FadeOut(self.gt_vgroup), FadeOut(self.kl_vgroup))

    # 2. Tiêu đề scene
    title = Tex(r"\textbf{Bước 1: Chứng minh $IE = IC$}",
                tex_template=viet_tex_template, font_size=36).to_corner(UL, buff=0.5)
    self.play(Write(title))

    # 3. Mục tiêu
    goal = MathTex(r"\text{CM: } \widehat{IEC} = \widehat{ICE}",
                   tex_template=viet_tex_template).next_to(title, DOWN, aligned_edge=LEFT)
    with self.voiceover(text="Ta cần chứng minh...") as ov:
        self.play(Write(goal), run_time=ov.duration * 0.7)
        self.play(Indicate(goal, color=COLOR_ACTIVE), run_time=0.8)

    # 4. ProofColumn + ProofLine + sync_* — xem manim-proof-sync + manim-layout-system

    # 5. Kết luận – đóng khung kết quả
    #
    # ── PATTERN A: Kết quả TRUNG GIAN (scene sau dùng làm tiền đề) ──────────
    result_mob = MathTex(r"IE = IC")
    result_mob.next_to(goal, DOWN, buff=1.0, aligned_edge=LEFT)
    self.play(TransformFromCopy(VGroup(self.geo.segment("IE"),
                                       self.geo.segment("IC")), result_mob))
    box = SurroundingRectangle(result_mob, color=COLOR_RESULT_KEY, buff=0.2)
    self.play(Create(box))

    # 6. Dọn dẹp + di chuyển kết quả lên UR — xem manim-scene-lifecycle
    self.play(FadeOut(title), FadeOut(goal))
    self.result_group = VGroup(result_mob, box)
    self.play(self.result_group.animate.to_corner(UR, buff=0.5))
```

> **Color chuẩn cho box**: kết quả trung gian → `COLOR_RESULT_KEY` (xanh lá); kết luận đpcm → `COLOR_RESULT_FINAL` (đỏ).

---

## 8. Brace – gộp nhiều biểu thức

```python
source_eqs = VGroup(eq1, eq2)

right_x = source_eqs.get_right()[0]
brace_spine = Line(
    [right_x + 0.1, source_eqs.get_top()[1] + 0.1, 0],
    [right_x + 0.1, source_eqs.get_bottom()[1] - 0.1, 0],
    stroke_opacity=0.0,
)
brace = Brace(brace_spine, direction=RIGHT, color=COLOR_DEFAULT)
self.play(Create(brace))

result = MathTex(r"...").next_to(brace, RIGHT, buff=0.2)
self.play(Write(result))
```

---

## 9. Nội dung đã tách sang skill khác

Để giữ skill này tập trung vào dựng hình, các nội dung sau **KHÔNG còn ở đây**:

- **TeX/MathTex tiếng Việt + `viet_tex_template`** → xem `.cursor/rules/manim-global.mdc` mục 1.
- **Bảng màu chuẩn nền sáng (`COLOR_*`, `MOTION_*`, `EMPHASIS_*`)** → xem `manim-design-tokens`.
- **Highlight cạnh / góc / tam giác / tứ giác** → xem `manim-proof-sync` (`sync_*`) + `manim-geometry-engine` (`geo.show_*`).
- **Boilerplate `Sector` + `cross2d` + `angle_between_vectors`** → xem `manim-geometry-engine` mục 1 (`AngleMarker`).
- **Quy tắc màu khi "bằng nhau" vs "phân biệt"** → xem `manim-geometry-engine` mục 4.
- **`persistent_geom`, FadeOut rules, `proof_accumulator`** → xem `manim-scene-lifecycle`.
- **Cursor management, `ProofColumn`, layout màn hình** → xem `manim-layout-system`.
- **Templates tọa độ dạng bài cụ thể** → xem `manim/patterns/`.

---

## 10. Checklist trước khi render

- [ ] Import `from manim_helpers import *` (hoặc named imports đầy đủ, bao gồm `ProofColumn`)
- [ ] **Mọi** `Tex(...)` / `MathTex(...)` chứa tiếng Việt có `tex_template=viet_tex_template`
- [ ] **Mọi** màu dùng `COLOR_*` token, KHÔNG hardcode hex
- [ ] **Mọi** `run_time=` của effect dùng `TIMING_*` token, KHÔNG hardcode số
- [ ] **Mọi** `set_z_index(...)` dùng `LAYER_*` token, KHÔNG hardcode `2`, `5`
- [ ] **Điểm trên đường tròn** tính bằng `R*cos/sin(theta)` (hoặc tương đương), **không** hardcode tọa độ xấp xỉ; tự kiểm `norm(P-O)==R` khi cần
- [ ] Tam giác / tứ giác trước `sync_*` / highlight engine: đủ cạnh Loại A (`geo.create_missing_sides` nếu `get_missing_sides` khác rỗng) — xem `manim-geometry-engine`
- [ ] Góc cần hai tia/cạnh hiển thị: đủ hai `Line` + register trước `sync_angle` / highlight (angle completeness — `manim-geometry-engine`)
- [ ] Đặt tên Mobject theo naming convention `dot_*`, `seg_*`, `ang_*`, `tri_*`, `quad_*`, `circ_*`, `ra_*`, `pf_*`
- [ ] `self.geo = GeometryEngine(self)` khởi tạo ở scene đầu; mọi điểm/đoạn đã `register_*`
- [ ] `line_intersection`, `cross2d`, `AngleMarker` import từ `manim_helpers` — KHÔNG copy-paste
- [ ] `self.diagram` lưu và reuse đúng index; mọi Dot quan trọng lưu vào `self.dot_*`
- [ ] Trong VGroup: tất cả `Line`/`Arc` đặt **trước** `Dot`/`label`
- [ ] Animation tách 2 bước: `Create(lines...)` → `Create(dots...) + Write(labels...)`
- [ ] Sau khi dựng xong: `self.bring_to_front(*all_dots, *all_labels)`
- [ ] Mọi giao điểm / đầu nối có `Dot` riêng (junction dots)
- [ ] **Dữ kiện ý nào thì chỉ vẽ hình cho ý đó**
- [ ] Nét **Loại A**: `Create()` vĩnh viễn, `bring_to_front`, `persistent_geom.add(...)` ← xem `manim-scene-lifecycle`
- [ ] Nét **Loại B**: KHÔNG `Indicate(...)` thủ công; dùng `sync_*` / `geo.show_*`
- [ ] `RightAngle` dùng đúng `quadrant` (xác định theo hướng vector — xem mục 3)
- [ ] `run_time` trong cùng 1 voiceover block tổng ≤ `ov.duration`
- [ ] Box trung gian: `COLOR_RESULT_KEY`; box đpcm: `COLOR_RESULT_FINAL`
- [ ] Lifecycle/cleanup/cursor → **đọc thêm** `manim-scene-lifecycle` và `manim-layout-system`
