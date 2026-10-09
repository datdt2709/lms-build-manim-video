---
name: manim-proof-sync
description: Đồng bộ voiceover bookmark với ProofLine (MathTex) trong scene chứng minh. Dùng khi scene liệt kê nhiều thực thể hình học liên tiếp, cần bookmark granular và animate theo từng token.
---

# Skill: Manim – Proof Sync (rule 1, 2, 3)

## Khi nào dùng skill này?

Mọi scene **chứng minh** có voiceover + dòng proof (MathTex / Tex). Đặc biệt khi voiceover liệt kê nhiều thực thể hình học liên tiếp (ví dụ "△OFB = △OFC (c.g.c) ⇒ BF = FC; ∠OFB = ∠OFC").

Skill này quy định 3 thứ:

1. **Bookmark granularity** – mỗi thực thể / mỗi từ kết nối có 1 bookmark riêng.
2. **ProofLine** – cách build MathTex theo semantic token, gọi `pf.write("token_id")` thay vì `pf[0]`, `pf[1]`.
3. **sync_<type>** – một hàm helper cho mỗi loại thực thể (segment, angle, triangle, ...) để gói gọn `wait_until_bookmark + AddTextLetterByLetter + visual effect`.

> **Tránh tuyệt đối**: viết tay `self.wait_until_bookmark("...")` rồi `self.play(Write(...), Indicate(...))` rời rạc — pattern này dễ sai bookmark name, dễ trộn timing, dễ quên `FadeOut`. Dùng `sync_*()`.

---

## 1. Bookmark granularity rules (rule 1)

### Quy tắc mới (huỷ rule cũ "≤ 3 bookmark / segment")

Một segment có thể chứa **nhiều bookmark (8–10 hoặc hơn)** khi voiceover liệt kê nhiều thực thể hình học liên tiếp. Mỗi thực thể cần 1 bookmark riêng để effect highlight bám đúng vào lúc TTS đọc đến tên thực thể đó.

### Mỗi thực thể phải có 1 bookmark

```text
Loại thực thể                         Đặt bookmark trước từ nào
────────────────────────────────────  ─────────────────────────────
Đoạn thẳng (segment)                  "BF", "FC", "AB", ...
Góc (angle)                           "góc OFB", "góc OFC"
Tam giác                              "tam giác OFB"
Tứ giác                               "tứ giác ABCD"
Điểm                                  "điểm M", "điểm O"
Đường tròn                            "đường tròn (O)"
Cung                                  "cung BC", "cung lớn"
Bán kính / đường kính                 "bán kính OA", "đường kính AB"
Dây cung / cát tuyến / tiếp tuyến     "dây cung CD", "tiếp tuyến tại A"
Từ kết nối semantic (=, ⇒, c.g.c…)    từng từ
```

Ví dụ voiceover dòng "△OFB = △OFC (c.g.c) ⇒ BF = FC":

```
"Do đó <bookmark mark='tri_OFB_expr'/> tam giác O F B
 <bookmark mark='tri_equal_expr'/> bằng
 <bookmark mark='tri_OFC_expr'/> tam giác O F C
 <bookmark mark='tri_cgc_expr'/> theo trường hợp cạnh góc cạnh.
 <bookmark mark='seg_BF_expr'/> Suy ra B F
 <bookmark mark='seg_equal_expr'/> bằng
 <bookmark mark='seg_FC_expr'/> F C."
```

→ 7 bookmark trong 1 segment, hợp lệ.

### Naming pattern bắt buộc: `<type>_<name>_expr`

Tên bookmark phải **tự mô tả thực thể** để khi đọc spec ta biết ngay action nào sẽ chạy.

```text
Loại                Pattern                  Ví dụ
──────────────────  ───────────────────────  ─────────────────────────────
Tam giác            tri_<XYZ>_expr           tri_OFB_expr, tri_ABC_expr
Tam giác – tiêu chí tri_<criterion>_expr     tri_cgc_expr, tri_ggg_expr
Tam giác – "bằng"   tri_equal_expr           (cố định, từ "=" giữa 2 tam giác)
Đoạn                seg_<XY>_expr            seg_BF_expr, seg_FC_expr
Đoạn – "bằng"       seg_equal_expr           (cố định)
Góc                 angle_<XYZ>_expr         angle_OFB_expr, angle_OFC_expr
Góc – "bằng"        angle_equal_expr         (cố định)
Tứ giác             quad_<WXYZ>_expr         quad_ABCD_expr
Điểm                dot_<X>_expr             dot_M_expr, dot_I_expr
Đường tròn          circ_<NAME>_expr         circ_O_expr
Cung                arc_<XY>_expr            arc_BC_expr
Bán kính            radius_<XY>_expr         radius_OA_expr
Đường kính          diameter_<XY>_expr       diameter_AB_expr
Dây cung            chord_<XY>_expr          chord_CD_expr
Tiếp tuyến          tangent_<XY>_expr        tangent_AB_expr
Cát tuyến           secant_<XY>_expr         secant_AB_expr
Suy ra (⇒)         <context>_implies_expr   tri_implies_seg_expr
```

> Pattern cũ `bk_circle`, `bk_ang` đã **bỏ** — không dùng nữa.

---

## 2. ProofLine semantic token system (rule 2)

### Vấn đề

Cách viết cũ `MathTex(r"\triangle OFB = \triangle OFC \;(\text{c.g.c})", ...)` cho ra mob phẳng, muốn animate riêng "OFB" hoặc "(c.g.c)" phải đếm index `[0]`, `[1]`, ... — đếm sai khi đổi LaTeX là crash.

### Cách mới: `ProofLine`

Khai báo **token bằng tên semantic**. Mỗi token là một sub-expression có id; `pf.write("id")` trả về animation Write 1 token.

```python
from manim_helpers import ProofLine

pf5 = ProofLine(
    ("tri_OFB", r"\triangle OFB"),
    ("eq1",     "="),
    ("tri_OFC", r"\triangle OFC"),
    ("cgc",     r"\;(\text{c.g.c})"),
    ("seg_BF",  r";\quad BF"),
    ("seg_eq",  "="),
    ("seg_FC",  r"FC"),
    tex_template=viet_tex_template,
    font_size=26,
)
pf5.place_below(cursor)        # đặt dưới cursor (np.array hoặc Mobject)
self.add(pf5)                  # add vào scene; mọi token bắt đầu opacity=0 (invisible)
```

**Visibility:** Trong `proof_line.py`, sau khi dựng `MathTex`, mỗi token (sub-expression) được `set_opacity(0)`. `self.add(pf5)` không làm lộ chữ — chỉ khi `pf.write("token_id")` (hoặc `write_all`) mới `set_opacity(1)` rồi `AddTextLetterByLetter` token đó.

API:

```text
Method                                    Mô tả
────────────────────────────────────────  ─────────────────────────────────────────
pf.get(token_id)                          Mobject sub-expression (Indicate riêng)
pf[token_id]                              shortcut = pf.get(token_id)
pf.write(*token_ids, run_time=None)       Animation AddTextLetterByLetter 1+ token
pf.write_all(run_time=None)               Write toàn bộ token theo thứ tự
pf.place_below(anchor, buff, ...)         next_to anchor (Mobject hoặc np.array)
pf.get_bottom_left_cursor()               cursor [left_x, bottom_y, 0] cho dòng sau
pf.token_ids                              list id theo thứ tự khai báo
```

### Quy tắc khai báo token

- Mỗi **thực thể** = 1 token (`tri_OFB`, `seg_BF`, `angle_OFB`).
- Mỗi **từ kết nối** = 1 token (`eq1`, `eq2`, `cgc`, `implies`, `bracket1`).
- Khoảng cách / dấu chấm phẩy đi cùng token kế bên (`r";\quad BF"`) để tránh token "chỉ là khoảng trắng" gây Write rỗng.
- Đặt tên id trong ProofLine phải khớp với phần trong bookmark name (`tri_OFB_expr` ↔ token id `tri_OFB`).

### Ví dụ multi-line proof

```python
pf6 = ProofLine(
    ("implies", r"\Rightarrow"),
    ("tri_OFB", r"\triangle OFB"),
    ("equiv",   r"\equiv"),
    ("tri_OFC", r"\triangle OFC"),
    tex_template=viet_tex_template, font_size=26,
).place_below(pf5.get_bottom_left_cursor(), buff=0.20)
```

---

## 3. Sync helpers theo type (rule 3)

KHÔNG dùng 1 hàm chung `sync_math_and_shape`. Mỗi loại thực thể có **timing riêng** + **effect riêng** vì người xem cần:

- Cạnh: cần thấy nét đậm chớp lên rồi trở lại → `set_stroke ... there_and_back`
- Góc: cần thấy "phần fill bên trong" → `FadeIn(Sector)` rồi tự FadeOut sau block
- Tam giác: cần thấy diện tích tam giác → `set_fill ... there_and_back` trên Polygon
- Điểm: cần thấy "điểm nhảy" → `Indicate(scale_factor=1.8)`
- Quan hệ (`=`, `⇒`, `(c.g.c)`): chỉ Write, không có shape.

### Bảng API

```text
Hàm                          Effect                         Timing              Color
───────────────────────────  ─────────────────────────────  ──────────────────  ─────────────
sync_point(scene,bk,tex,dot) Indicate(dot, scale=1.8)       TIMING_POINT        COLOR_ACTIVE
sync_segment(...)            set_stroke(w=10) then back     TIMING_INDICATE_SEG COLOR_ACTIVE
sync_angle(...)              FadeIn(sector)                 TIMING_ANGLE        (sector color)
sync_right_angle(...,geo)    Polygon fill + ra.set_stroke   TIMING_ANGLE        COLOR_EQUAL_1
sync_triangle(...)           set_fill(op=0.35) then back    TIMING_INDICATE_TRI COLOR_EQUAL_3
sync_quadrilateral(...)      set_fill(op=0.30) then back    TIMING_INDICATE_TRI COLOR_EQUAL_3
sync_relation(...)           chỉ Write                      TIMING_RELATION     –
```

**Side completeness (tam giác / tứ giác):** `sync_triangle` / `sync_quadrilateral` (và `geo.highlight_triangle`, `geo.show_congruence`, `geo.compare_triangles`, …) giả định **mọi cạnh** của hình đã là `Line` đã `Create` vĩnh viễn và nằm trong `geo._segments`. Nếu thiếu, highlight cạnh có thể chỉ flash rồi mất. Trước khi gọi `sync_*` / highlight đó, dùng `geo.get_missing_sides("XYZ")` — nếu khác rỗng thì `geo.create_missing_sides("XYZ")` rồi `Create` + `persistent_geom` (chi tiết API → `manim-geometry-engine`).

**Angle completeness (hai cạnh của góc):** `sync_angle` chỉ `FadeIn` sector; nếu kịch bản cần **cả hai nét** tạo góc (ví dụ sau đó `sync_segment` lên hai cạnh, hoặc góc “nằm” trên hai tia chưa vẽ), phải bổ sung hai `Line` vào diagram trước — thường bằng `create_missing_sides` cho tam giác (hoặc tứ giác) chứa đỉnh góc và hai điểm trên hai tia. Chi tiết → `manim-geometry-engine` mục **Angle completeness**.

### Hợp đồng chung của mỗi `sync_*`

```python
def sync_<type>(scene, bookmark, tex_anim, <shape>, *, write_time=..., ...):
    if bookmark is not None:
        scene.wait_until_bookmark(bookmark)
    scene.play(tex_anim, run_time=write_time)   # AddTextLetterByLetter proof token
    scene.play(<effect>, run_time=<effect_time>)  # visual effect
```

> **Lưu ý sync_angle**: KHÔNG tự FadeOut sector. Caller phải FadeOut sector ở cuối block, hoặc tốt hơn dùng `geo.show_angle_equal(...)` từ `manim-geometry-engine` để engine tự track + cleanup.

> **Lưu ý sync_right_angle**: Luôn truyền `geo=self.geo` khi dùng với `GeometryEngine`. Khi `geo` được truyền, `patch` (Polygon 4 đỉnh tô kín ô vuông) được track vào `geo._temp_ra_revert` và `geo.cleanup_temp()` sẽ tự `FadeOut` patch + revert stroke về trạng thái gốc. **Nếu không truyền `geo`**: `patch` tồn tại vĩnh viễn trên màn hình sau block; caller phải `FadeOut(patch)` và `ra.animate.set_stroke(orig_color, width=orig_width)` tay.
>
> **KHÔNG** dùng `ra.animate.set_fill` trực tiếp trên `RightAngle` — Manim `RightAngle` là polyline 3 điểm, `set_fill` chỉ tô được nửa tam giác. `sync_right_angle` tạo `Polygon` riêng 4 đỉnh để tô kín ô vuông.

> **Đỉnh đã có RightAngle (`ra_<X>`):** dùng `sync_right_angle` hoặc `geo.highlight_right_angle` — **KHÔNG** dùng `sync_angle` với `AngleMarker`/`Sector` đè lên ký hiệu L.

### Khi tex_anim không cần Write

Nếu segment chỉ muốn highlight (không Write thêm token), truyền `tex_anim=None`:

```python
sync_segment(self, "seg_BF_expr", None, self.seg_BF, color=COLOR_EQUAL_1)
```

Hàm sẽ chỉ wait + chạy effect, bỏ qua Write.

### `GeometryEngine.highlight_segment(name)` vs `sync_segment(...)`

Cả hai đều chạy cùng **ý tưởng hiệu ứng**: `seg.animate.set_stroke(..., width=…)` với `rate_func=there_and_back` để nét đậm lên rồi trả về trạng thái cũ.

```text
                        sync_segment(...)              geo.highlight_segment(name)
──────────────────────  ─────────────────────────────  ─────────────────────────────
Bookmark                wait_until_bookmark bên trong  scene tự wait nếu cần TTS
ProofLine               Write token + highlight gom     chỉ hình, không Write
Truy cập cạnh           truyền Line trực tiếp          tra cứu register_segment
Độ dày nét mặc định     stroke_width=10                STATE_HIGHLIGHT (nhẹ hơn)
Màu mặc định            COLOR_ACTIVE                   COLOR_ACTIVE
```

**Khi nào dùng gì**

- Chuỗi chứng minh + bookmark + `ProofLine`: ưu tiên `sync_segment` (đúng rule 3, ít lệch tên bookmark).
- Đã có `GeometryEngine`, chỉ cần nháy cạnh sau một `play` khác (vd. vừa `Create(seg_NE)` xong, hoặc highlight trong đề bài không có token LaTeX): gọi `geo.highlight_segment("NE")` sau khi `wait_until_bookmark` — gọn, không phải giữ ref `self.seg_*` nếu chỉ tra cứu theo tên.

Muốn **cùng độ đậm** giữa hai API: truyền `stroke_width` / `run_time` tường minh vào từng hàm (hoặc chỉnh default trong `sync_helpers.py` / `STATE_HIGHLIGHT` — trade-off toàn project).

---

## 4. Pattern voiceover block hoàn chỉnh

Đây là pattern chuẩn cho 1 segment chứng minh "△OFB = △OFC (c.g.c) ⇒ BF = FC; ∠OFB = ∠OFC". Gọi đầy đủ helper:

```python
from manim_helpers import (
    ProofLine,
    sync_triangle, sync_segment, sync_angle, sync_relation,
    COLOR_EQUAL_1, COLOR_EQUAL_2,
)

# (1) Tạo ProofLine với token semantic
pf5 = ProofLine(
    ("tri_OFB", r"\triangle OFB"),
    ("eq1",     "="),
    ("tri_OFC", r"\triangle OFC"),
    ("cgc",     r"\;(\text{c.g.c})"),
    ("seg_BF",  r";\quad BF"),
    ("seg_eq",  "="),
    ("seg_FC",  r"FC"),
    ("ang_imp", r"\Rightarrow"),
    ("ang_OFB", r"\widehat{OFB}"),
    ("ang_eq",  "="),
    ("ang_OFC", r"\widehat{OFC}"),
    tex_template=viet_tex_template, font_size=26,
).place_below(cursor)
self.add(pf5)
proof.add(pf5)

# (2) Trong voiceover block: mỗi bookmark gọi 1 sync_*
with self.voiceover(
    text=(
        "Do đó <bookmark mark='tri_OFB_expr'/> tam giác O F B "
        "<bookmark mark='tri_equal_expr'/> bằng "
        "<bookmark mark='tri_OFC_expr'/> tam giác O F C "
        "<bookmark mark='tri_cgc_expr'/> theo trường hợp cạnh góc cạnh. "
        "<bookmark mark='seg_BF_expr'/> Suy ra B F "
        "<bookmark mark='seg_equal_expr'/> bằng "
        "<bookmark mark='seg_FC_expr'/> F C, "
        "<bookmark mark='angle_OFB_expr'/> và góc O F B "
        "<bookmark mark='angle_equal_expr'/> bằng "
        "<bookmark mark='angle_OFC_expr'/> góc O F C."
    )
) as ov:
    sync_triangle(self, "tri_OFB_expr", pf5.write("tri_OFB"),
                  self.tri_OFB_fill, color=COLOR_EQUAL_1)
    sync_relation(self, "tri_equal_expr", pf5.write("eq1"))
    sync_triangle(self, "tri_OFC_expr", pf5.write("tri_OFC"),
                  self.tri_OFC_fill, color=COLOR_EQUAL_2)
    sync_relation(self, "tri_cgc_expr", pf5.write("cgc"))

    sync_segment(self, "seg_BF_expr", pf5.write("seg_BF"),
                 self.seg_BF, color=COLOR_EQUAL_1)
    sync_relation(self, "seg_equal_expr", pf5.write("seg_eq"))
    sync_segment(self, "seg_FC_expr", pf5.write("seg_FC"),
                 self.seg_FC, color=COLOR_EQUAL_1)

    sync_angle(self, "angle_OFB_expr", pf5.write("ang_OFB"),
               self.sec_OFB)
    sync_relation(self, "angle_equal_expr", pf5.write("ang_eq"))
    sync_angle(self, "angle_OFC_expr", pf5.write("ang_OFC"),
               self.sec_OFC)

# (3) Cuối block: FadeOut sector tạm (sync_angle không tự cleanup)
self.play(FadeOut(self.sec_OFB), FadeOut(self.sec_OFC), run_time=TIMING_FADE)
```

> **Mẹo**: Nếu dùng `GeometryEngine` từ `manim-geometry-engine`, `geo.show_congruence(...)` + `geo.show_segment_equal(...)` + `geo.show_angle_equal(...)` đã gói cả **highlight + cleanup** trong 1 lời gọi — pattern trên sẽ rút gọn hơn. Xem ví dụ ở `manim-geometry-engine`.

---

## 5. Code reference

- `manim_helpers/proof_line.py` — class `ProofLine`
- `manim_helpers/sync_helpers.py` — `sync_point`, `sync_segment`, `sync_angle`, `sync_right_angle`, `sync_triangle`, `sync_quadrilateral`, `sync_relation`

Import:

```python
from manim_helpers import (
    ProofLine,
    sync_point, sync_segment, sync_angle, sync_right_angle,
    sync_triangle, sync_quadrilateral, sync_relation,
)
```

Skill phụ trợ:

- `manim-design-tokens` – cung cấp `COLOR_*`, `TIMING_*`, `LAYER_*`
- `manim-geometry-engine` – wrap `sync_*` thành API cao hơn (`geo.show_congruence`, `geo.show_segment_equal`)

---

## 5b. Tex / MathTex khối (không qua ProofLine) — reveal theo voiceover

GT/KL, tiêu đề, hoặc một dòng `Tex` / `MathTex` **một khối** không có token `pf.write(...)`. Để tránh hiện cả khối một lúc khi cần khớp giọng đọc:

- Tách thành nhiều `Tex` / `MathTex` và `Write` lần lượt trong cùng block voiceover, **hoặc**
- `AnimationGroup(*[AddTextLetterByLetter(line) for line in tex_lines], lag_ratio=0.3..0.5)` với `run_time=TIMING_PROOF_WRITE` (hoặc tỷ lệ `ov.duration`) để các dòng lệch nhịp nhẹ.

Pattern này bổ sung cho ProofLine (token từng phần); không thay thế bookmark + `sync_*` ở dòng chứng minh chi tiết.

---

## 6. Checklist

- [ ] Mọi bookmark dùng pattern `<type>_<name>_expr` (`tri_OFB_expr`, `seg_BF_expr`, `angle_OFB_expr`, `seg_equal_expr`, `tri_cgc_expr`, ...)
- [ ] **Mỗi thực thể** trong voiceover (đoạn / góc / tam giác / tứ giác / điểm / circle / arc / radius / chord / tangent / secant) có 1 bookmark riêng — không gộp 2 thực thể vào 1 bookmark
- [ ] **Mỗi từ kết nối semantic** (`=`, `⇒`, `(c.g.c)`, `(g.c.g)`, `(c.c.c)`) có 1 bookmark riêng
- [ ] KHÔNG giới hạn 3 bookmark / segment — segment có thể có 8-10+ bookmark khi cần
- [ ] Mọi proof line dùng `ProofLine(...)` với token semantic; KHÔNG dùng `MathTex(...)` rời rạc cho dòng có nhiều thực thể
- [ ] Mỗi token `pf.write(id)` được gọi đồng bộ với đúng 1 bookmark `<type>_<name>_expr`
- [ ] Mọi action highlight dùng `sync_<type>(...)`, KHÔNG raw `Indicate(...)` / `FadeIn(Sector(...))` trong code scene
- [ ] `sync_angle(...)` luôn có `FadeOut(sector)` ở cuối block (hoặc dùng `geo.show_*_equal` từ `manim-geometry-engine` để engine tự cleanup)
- [ ] Mọi `run_time=` trong sync_* để mặc định (lấy từ `TIMING_*` token), chỉ override khi có lý do rõ ràng
- [ ] Token ProofLine và bookmark có cùng base name (`tri_OFB` ↔ `tri_OFB_expr`) — dễ trace
- [ ] Tam giác / tứ giác trước `sync_triangle` / `sync_quadrilateral`: đủ cạnh trên diagram (`geo.get_missing_sides` / `create_missing_sides` — xem `manim-geometry-engine`)
- [ ] Góc cần **hai cạnh/tia** hiển thị hoặc sẽ highlight segment trên hai tia: đủ hai `Line` trong `geo` + `Create` trước `sync_angle` — dùng `geo.create_missing_sides` cho góc thuộc tam giác/tứ giác đã register, hoặc `geo.ensure_angle_sides(vertex, pt1, pt2)` cho góc tự do (xem **Angle completeness** trong `manim-geometry-engine`)
- [ ] `sync_right_angle` luôn truyền `geo=self.geo`; thiếu thì `patch` Polygon tồn tại vĩnh viễn và `cleanup_temp()` không dọn được
