---
name: manim-geometry-engine
description: Highlight đoạn thẳng, góc, tam giác, tứ giác trong scene hình học. Dùng khi cần nhấn mạnh đẳng thức cạnh/góc hoặc hai tam giác bằng nhau/đồng dạng.
---

# Skill: Manim – Geometry Engine (rule 5, 9)

## Khi nào dùng skill này?

Bất kỳ scene hình học nào cần highlight đoạn / góc / tam giác / tứ giác — cụ thể là:

- "AB = CD" → highlight 2 đoạn cùng màu
- "∠A = ∠B" → highlight 2 góc cùng màu
- "△ABC = △DEF (c.g.c)" → highlight 2 tam giác hai màu khác
- Chỉ "Xét tam giác ABC" / "Xét tứ giác ABCD" → highlight 1 đối tượng

Skill này code-hoá **rule 5 (quy tắc màu)** và **rule 9 (registry-based API)** thành 2 thứ:

1. `AngleMarker(A, O, B, color, ...)` — Sector tự tính start_angle / angle / dấu xoay.
2. `GeometryEngine` — registry các thực thể theo tên semantic, có method `highlight_*`, `show_*_equal`, `show_congruence`, `compare_*`, `cleanup_temp`.

> Mục tiêu: scene chứng minh KHÔNG còn boilerplate `v1 = O_pos - K_pos; v2 = A_pos - K_pos; cross2d(...) ...` lặp lại 5 lần / scene; KHÔNG còn lặp `set_fill ... there_and_back` thủ công.

---

## 1. AngleMarker (rule 5 + rule 9)

### Vấn đề cũ

```python
# Boilerplate ~10 dòng / mỗi góc
v1_k = O_pos - K_pos
v2_k = A_pos - K_pos
sec_OKA = Sector(
    arc_center=K_pos, radius=0.32,
    start_angle=np.arctan2(v1_k[1], v1_k[0]),
    angle=angle_between_vectors(v1_k, v2_k) * (
        -1 if (v1_k[0]*v2_k[1] - v1_k[1]*v2_k[0]) < 0 else 1),
    fill_color="#E65100", fill_opacity=0.4,
    stroke_color="#E65100", stroke_width=2,
)
```

### Cách mới

```python
from manim_helpers import AngleMarker, COLOR_EQUAL_1

sec_OKA = AngleMarker(O_pos, K_pos, A_pos, color=COLOR_EQUAL_1)
# Tự tính: start_angle, angle, dấu xoay theo cross2d
# Tự set z_index = LAYER_MARKERS
```

Signature:

```python
AngleMarker(A, O, B, *, color=COLOR_ACTIVE, radius=0.32,
            stroke_width=2.0, fill_opacity=0.4) -> Sector
```

- **A** = điểm đầu của tia đầu, **O** = đỉnh, **B** = điểm đầu của tia thứ hai.
- Trả về `Sector` — thoả mãn `FadeIn` / `FadeOut` / `Indicate` đầy đủ.
- Helper `angle_between_vectors(v1, v2)` và `cross2d(v1, v2)` cũng được export module-level từ `manim_helpers` (không lặp module-level mỗi project).

### Quy tắc màu (rule 5) – cốt lõi

| Tình huống                              | Quy tắc màu                          | API gợi ý                    |
|-----------------------------------------|--------------------------------------|------------------------------|
| 2 góc **bằng nhau** (∠A = ∠B)          | **CÙNG 1 màu** (`COLOR_EQUAL_1`)     | `geo.show_angle_equal(...)`  |
| 2 tam giác **bằng nhau** (△ABC = △DEF) | **HAI màu khác** (EQUAL_1 + EQUAL_2) | `geo.show_congruence(...)`   |
| Tổng/nhiều góc phân biệt               | **N màu khác** từ palette            | `geo.compare_angles(...)`    |
| 1 góc / đoạn / tam giác đơn lẻ         | `COLOR_ACTIVE`                       | `geo.highlight_*`            |

### Ví dụ đúng / sai

```python
# ✓ ĐÚNG – ∠OKA = ∠OAK (bằng nhau) → cùng COLOR_EQUAL_1
sec_OKA = AngleMarker(O, K, A, color=COLOR_EQUAL_1)
sec_OAK = AngleMarker(O, A, K, color=COLOR_EQUAL_1)

# ✗ SAI – tô khác màu cho hai góc đang phải "bằng nhau" → người xem không hiểu
sec_OKA = AngleMarker(O, K, A, color=COLOR_EQUAL_1)
sec_OAK = AngleMarker(O, A, K, color=COLOR_EQUAL_2)   # ❌

# ✓ ĐÚNG – ∠OKA + ∠HKB (tổng / phân biệt) → khác màu
sec_OKA = AngleMarker(O, K, A, color=COLOR_EQUAL_1)
sec_HKB = AngleMarker(H, K, B, color=COLOR_EQUAL_2)   # phân biệt
```

---

## 2. GeometryEngine API (rule 9)

Khởi tạo trong scene đầu (thường là `scene01_introVaDeBai`):

```python
from manim_helpers import GeometryEngine, COLOR_DEFAULT, COLOR_EQUAL_1, COLOR_EQUAL_2

self.geo = GeometryEngine(self)
```

`self.geo` được lưu xuyên scene (vì kế thừa từ `self.*`), mọi scene sau dùng cùng 1 registry.

### Register API

```text
Method                                              Mô tả
──────────────────────────────────────────────────  ─────────────────────────────────────
geo.register_point(name, pos, *, dot, label)        Đăng ký điểm theo tên semantic
geo.register_segment(name, line)                    Đăng ký Line đã tạo
geo.register_triangle(name, vertex_names)           Đăng ký tam giác bằng 3 tên điểm
geo.register_quadrilateral(name, vertex_names)      Tương tự, 4 điểm
geo.register_triangle_fill(name, *, color, ...)     Tạo Polygon fill (mặc định invisible)
geo.register_right_angle(name, ra_mob)              Đăng ký 1 RightAngle đã tạo
```

### Side completeness rule (bắt buộc trước highlight / sync)

`highlight_segment`, `highlight_triangle`, `show_congruence`, `compare_triangles`, và các `sync_triangle` / `sync_quadrilateral` từ `manim-proof-sync` đều giả định **mọi cạnh** của hình đã là `Line` trong `_segments` và đã được `Create` vĩnh viễn trên scene. Nếu một cạnh chỉ là "tưởng tượng" (chưa register / chưa vẽ), hiệu ứng `there_and_back` trên stroke có thể khiến cạnh **chớp rồi biến mất**.

1. Trước `sync_triangle` / `sync_quadrilateral` / `geo.highlight_triangle` / `geo.show_congruence` / `geo.compare_triangles` (và mọi chỗ cần stroke đủ cạnh): gọi `geo.get_missing_sides("TênShape")` — `TênShape` là tên đã truyền vào `register_triangle` / `register_quadrilateral` (ví dụ `"ANH"`, `"BNMC"`).
2. Nếu list trả về **không rỗng**: `geo.create_missing_sides("TênShape", color=COLOR_AUX_LINE)` → với mỗi `(seg_name, line)` trả về, `Create(line)`, `bring_to_front` dot/label liên quan, `persistent_geom.add(line)` (hoặc tương đương).

```text
Method                                              Trả về / tác dụng
──────────────────────────────────────────────────  ─────────────────────────────────────
geo.get_missing_sides(shape_name)                   list[tuple[str,str]] — cặp cạnh chưa
                                                    có trong registry
geo.create_missing_sides(shape_name, *, color)      list[tuple[str,Line]] — tạo Line,
                                                    register_segment, trả về để Create
```

### Angle completeness (hai cạnh tạo góc — bắt buộc khi cần “thấy” hai tia)

`AngleMarker` / `geo.highlight_angle` / `geo.show_angle_equal` / `sync_angle` chỉ vẽ **sector** tại đỉnh; chúng **không** tự thêm nét hai cạnh của góc. Nếu voiceover hoặc bước sau dùng `sync_segment` / `highlight_segment` / so sánh nét trên **hai tia** ∠X (tức các đoạn `XY`, `XZ` đã `register_segment`), hoặc hình học cần người xem **nhìn thấy đủ hai cạnh** tạo góc, thì hai đoạn đó phải đã có trong `_segments` và đã `Create` vĩnh viễn (Loại A) — cùng một nguyên tắc với side completeness.

**Cách làm thực tế:**

- Nếu góc là góc trong tam giác (hoặc tứ giác) đã `register_*`: trước khi nhắc góc + highlight cạnh liên quan, gọi `get_missing_sides` / `create_missing_sides` cho **tam giác / tứ giác chứa hai cạnh ấy** (thường đủ để có cả hai cạnh từ đỉnh).
- Nếu góc tạo bởi hai đoạn **không** cùng một tam giác đã register: dùng `geo.ensure_angle_sides(vertex, pt1, pt2)` thay vì tạo thủ công.

```text
Method                                              Trả về / tác dụng
──────────────────────────────────────────────────  ─────────────────────────────────────
geo.ensure_angle_sides(vertex, pt1, pt2, *, color)  list[tuple[str,Line]] — tạo và
                                                    register_segment cạnh vertex–pt1,
                                                    vertex–pt2 còn thiếu
```

**Khi nào dùng cái nào:**

| Tình huống                                      | API                                      |
|-------------------------------------------------|------------------------------------------|
| Góc trong tam giác / tứ giác đã `register_*`   | `geo.create_missing_sides("TênShape")`   |
| Góc từ 2 điểm bất kỳ (không cùng shape)        | `geo.ensure_angle_sides(vertex, pt1, pt2)` |

Ví dụ:

```python
# Góc ∠BAC tại đỉnh A, hai cạnh AB và AC chưa register
new_sides = self.geo.ensure_angle_sides("A", "B", "C", color=COLOR_AUX_LINE)
for seg_name, seg in new_sides:
    self.play(Create(seg))
    persistent_geom.add(seg)
```

### Lookup

```text
Method                    Trả
────────────────────────  ─────────────
geo.point("A")            np.ndarray
geo.segment("AB")         Line
geo.triangle_fill("OFB")  Polygon
geo.right_angle("B")      RightAngle
```

### Highlight 1 đối tượng đơn lẻ

```text
Method                              Default color   Effect
──────────────────────────────────  ──────────────  ─────────────────────────────────────
geo.highlight_point(name)           COLOR_ACTIVE    Indicate(scale=1.8)
geo.highlight_segment(name)         COLOR_ACTIVE    set_stroke(STATE_HIGHLIGHT width)
                                                    there_and_back
geo.highlight_angle(tri, vtx=1)     COLOR_EQUAL_1   FadeIn(AngleMarker) → temp
geo.highlight_right_angle(name)     COLOR_EQUAL_1   Polygon 4 đỉnh fill + ra.set_stroke;
                                                    KHÔNG set_fill trực tiếp RightAngle
geo.highlight_triangle(name)        COLOR_EQUAL_3   set_fill(opacity=0.35) there_and_back
```

**Độ dày nét:** `highlight_segment` và `show_segment_equal` dùng `STATE_HIGHLIGHT["stroke_width"]` cho xung there-and-back trên đoạn thẳng. `highlight_right_angle` và `show_right_angle_equal` tái dùng cùng `STATE_HIGHLIGHT["stroke_width"]` cho nét RightAngle khi highlight (đồng bộ với design tokens). Cạnh tam giác (stroke kèm fill) trong `highlight_triangle`, `show_congruence` và `compare_triangles` lấy từ `STATE_EQUAL["stroke_width"]`. Chỉnh một lần trong `manim_helpers/visual_tokens.py` là đồng bộ cả engine.

> **Highlight góc vuông:** Khi voiceover nhắc "góc tại B = 90°" và đỉnh đó **đã có** `RightAngle` (`ra_B`) → **KHÔNG** dùng `AngleMarker`/`geo.highlight_angle` (sector cam đè lên ký hiệu L). Dùng `geo.highlight_right_angle("B")`: engine thêm `Polygon` bốn đỉnh **phía sau** ký hiệu L để tô kín ô vuông (path `RightAngle` của Manim chỉ có 3 đỉnh — `set_fill` trực tiếp chỉ tô được nửa tam giác).

### Quy tắc màu được code-hoá – rule 5

```text
Method                              Số ĐT   Quy tắc màu
──────────────────────────────────  ──────  ─────────────────────────────
geo.show_segment_equal(*names)        ≥ 2   CÙNG 1 màu (COLOR_EQUAL_1)
geo.show_angle_equal(*tri_names)      ≥ 2   CÙNG 1 màu
geo.show_right_angle_equal(*names)    ≥ 2   CÙNG 1 màu (nhiều góc vuông =)
geo.show_congruence(tri_a, tri_b)       2   HAI màu khác (EQUAL_1 + EQUAL_2)
geo.compare_triangles(*tri_names)     ≥ 2   Mỗi cái 1 màu khác (palette)
```

### Cleanup

```python
geo.cleanup_temp()   # FadeOut AngleMarker / fill trong _temp_markers; revert RightAngle trong _temp_ra_revert
```

Mọi method `highlight_angle`, `show_angle_equal` đều **track sector vào `_temp_markers`**. `highlight_right_angle` / `show_right_angle_equal` **track snapshot vào `_temp_ra_revert`** để `cleanup_temp` trả fill opacity về 0 và stroke về màu/gốc. Caller chỉ cần gọi `geo.cleanup_temp()` ở cuối block / cuối scene để clear an toàn.

---

## 3. Pattern code đầy đủ – ví dụ "△OFB = △OFC (c.g.c)"

Phối hợp `GeometryEngine` + `ProofLine` + `sync_*` cho 1 segment chứng minh:

```python
from manim_helpers import (
    GeometryEngine, ProofLine,
    sync_triangle, sync_segment, sync_angle, sync_relation,
    COLOR_EQUAL_1, COLOR_EQUAL_2, TIMING_FADE,
)

# === Setup 1 lần ở scene đầu ===
self.geo = GeometryEngine(self)
self.geo.register_point("O", O_pos)
self.geo.register_point("F", F_pos)
self.geo.register_point("B", B_pos)
self.geo.register_point("C", C_pos)
self.geo.register_segment("OF", seg_OF)
self.geo.register_segment("FB", seg_FB)
self.geo.register_segment("FC", seg_FC)
self.geo.register_triangle("OFB", ["O", "F", "B"])
self.geo.register_triangle("OFC", ["O", "F", "C"])
# Tạo invisible fill cho 2 tam giác (sẽ animate set_fill khi highlight)
self.add(self.geo.register_triangle_fill("OFB"),
         self.geo.register_triangle_fill("OFC"))

# === Trong scene chứng minh: pattern A – chi tiết bằng sync_* ===
pf5 = ProofLine(
    ("tri_OFB", r"\triangle OFB"),
    ("eq1",     "="),
    ("tri_OFC", r"\triangle OFC"),
    ("cgc",     r"\;(\text{c.g.c})"),
    ("seg_BF",  r";\quad BF"),
    ("seg_eq",  "="),
    ("seg_FC",  r"FC"),
    tex_template=viet_tex_template, font_size=26,
).place_below(cursor)
self.add(pf5)

with self.voiceover(text=(
    "Do đó <bookmark mark='tri_OFB_expr'/> tam giác O F B "
    "<bookmark mark='tri_equal_expr'/> bằng "
    "<bookmark mark='tri_OFC_expr'/> tam giác O F C "
    "<bookmark mark='tri_cgc_expr'/> theo trường hợp cạnh góc cạnh. "
    "<bookmark mark='seg_BF_expr'/> Suy ra B F "
    "<bookmark mark='seg_equal_expr'/> bằng "
    "<bookmark mark='seg_FC_expr'/> F C."
)) as ov:
    sync_triangle(self, "tri_OFB_expr", pf5.write("tri_OFB"),
                  self.geo.triangle_fill("OFB"), color=COLOR_EQUAL_1)
    sync_relation(self, "tri_equal_expr", pf5.write("eq1"))
    sync_triangle(self, "tri_OFC_expr", pf5.write("tri_OFC"),
                  self.geo.triangle_fill("OFC"), color=COLOR_EQUAL_2)
    sync_relation(self, "tri_cgc_expr", pf5.write("cgc"))
    sync_segment(self, "seg_BF_expr", pf5.write("seg_BF"),
                 self.geo.segment("FB"), color=COLOR_EQUAL_1)
    sync_relation(self, "seg_equal_expr", pf5.write("seg_eq"))
    sync_segment(self, "seg_FC_expr", pf5.write("seg_FC"),
                 self.geo.segment("FC"), color=COLOR_EQUAL_1)

self.geo.cleanup_temp()   # phòng thủ nếu có sector nào tracked
```

### Pattern B – siêu rút gọn bằng `geo.show_*`

Khi scene CHỈ cần "highlight đầy đủ rule 5" mà không cần Write từng token chi tiết, gọi 1 dòng:

```python
with self.voiceover(text="...") as ov:
    self.wait_until_bookmark("tri_proof_expr")
    self.play(pf5.write_all(), run_time=TIMING_PROOF_WRITE)
    self.geo.show_congruence("OFB", "OFC", criterion="c.g.c")
    self.geo.show_segment_equal("FB", "FC")
    self.geo.show_angle_equal("OFB", "OFC", vertex_index=1)

self.geo.cleanup_temp()
```

> Pattern A (chi tiết, sync_* per token) phù hợp với spec "1 thực thể = 1 bookmark"; Pattern B phù hợp khi spec gộp 1 bookmark cho cả dòng. Mặc định **dùng Pattern A** (rule 1 từ `manim-proof-sync`).

---

## 4. Bảng quick-reference

```text
Tình huống                         API gợi ý                         Quy tắc màu
─────────────────────────────────  ────────────────────────────────  ─────────────────
Nhắc 1 điểm                        geo.highlight_point("M")          COLOR_ACTIVE
Nhắc 1 cạnh                        geo.highlight_segment / sync_seg  COLOR_ACTIVE
Nhắc 1 góc                         geo.highlight_angle / sync_angle COLOR_EQUAL_1
Nhắc góc vuông (có RightAngle)     geo.highlight_right_angle("B")  COLOR_EQUAL_1
Hai+ góc vuông bằng nhau           geo.show_right_angle_equal(...)   cùng EQUAL_1
Nhắc 1 tam giác                    geo.highlight_triangle / sync_tri COLOR_EQUAL_3
Cạnh bằng nhau                     geo.show_segment_equal("AB","CD") cùng EQUAL_1
Góc bằng nhau                      geo.show_angle_equal("ABC","DEF") cùng EQUAL_1
Tam giác bằng / đồng dạng          geo.show_congruence(...)          EQUAL_1 + EQUAL_2
So sánh nhiều tam giác / tổng góc  geo.compare_triangles(...)        palette 3 màu
Cleanup marker tạm                 geo.cleanup_temp()                –
```

---

## 5. Code reference

- `manim_helpers/geo_engine.py` — `line_intersection`, `cross2d`, `angle_between_vectors`, `AngleMarker`, `GeometryEngine`

Import:

```python
from manim_helpers import (
    line_intersection, cross2d, angle_between_vectors,
    AngleMarker, GeometryEngine,
)
```

Skill phụ trợ:

- `manim-design-tokens` – `COLOR_*`, `TIMING_*`, `LAYER_*` (engine sử dụng nội bộ)
- `manim-proof-sync` – `ProofLine`, `sync_*` (kết hợp với engine để Write proof + highlight đồng bộ)

---

## 6. Checklist

- [ ] `self.geo = GeometryEngine(self)` được khởi tạo ở scene đầu (thường `scene01`)
- [ ] Mọi điểm / đoạn / tam giác / tứ giác được `register_point` / `register_segment` / `register_triangle` / `register_quadrilateral` ngay sau khi tạo Mobject
- [ ] Trước `sync_*` tam giác/tứ giác hoặc `highlight_triangle` / `show_congruence` / `compare_triangles`: `get_missing_sides` rỗng hoặc đã `create_missing_sides` + `Create` vĩnh viễn
- [ ] Trước khi nhắc / `sync_angle` / `highlight_angle` mà cần **hai cạnh** của góc trên diagram (hoặc sẽ `sync_segment` lên hai tia): hai `Line` tương ứng đã register + `Create` — dùng `create_missing_sides` nếu góc thuộc tam giác/tứ giác đã register, hoặc `ensure_angle_sides(vertex, pt1, pt2)` nếu góc tự do — xem mục **Angle completeness**
- [ ] `sync_right_angle` luôn truyền `geo=self.geo` để `patch` được track vào `_temp_ra_revert`; thiếu `geo` thì `patch` tồn tại vĩnh viễn sau block và `cleanup_temp()` không revert được
- [ ] KHÔNG hardcode `Sector(arc_center=..., start_angle=..., angle=...)` trong scene — luôn dùng `AngleMarker(A, O, B, color=...)` hoặc `geo.highlight_angle(...)`
- [ ] KHÔNG hardcode `Polygon` highlight + `set_fill` thủ công — dùng `geo.highlight_triangle(...)` / `geo.show_congruence(...)`
- [ ] Khi 2+ thực thể **bằng nhau**: dùng `geo.show_*_equal(...)` (CÙNG 1 màu)
- [ ] Khi 2 tam giác **đồng dạng / bằng nhau** (so sánh): dùng `geo.show_congruence(...)` (HAI màu khác)
- [ ] Khi nhắc nhiều thực thể phân biệt: dùng `geo.compare_*` hoặc tạo `AngleMarker` mỗi cái 1 màu từ palette
- [ ] Cuối block (hoặc cuối scene) gọi `geo.cleanup_temp()` để FadeOut mọi sector / fill tạm và revert highlight `RightAngle`
- [ ] Khi đỉnh đã có `RightAngle`, **KHÔNG** tạo `AngleMarker` chồng lên — dùng `geo.highlight_right_angle(...)` (hoặc `sync_right_angle` + register)
- [ ] Mọi marker tạm (sector, fill) có `z_index = LAYER_MARKERS` (Engine tự set)
- [ ] Toàn bộ màu / timing / layer trong API đều dùng default từ `manim-design-tokens`; chỉ override khi spec yêu cầu cụ thể
