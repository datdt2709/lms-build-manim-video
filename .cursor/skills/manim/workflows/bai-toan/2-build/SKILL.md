---
name: manim-step-2-build-scenes
description: Sinh file Python Manim hoàn chỉnh từ Scene Spec (Step 1). Dùng sau khi đã có Scene Spec để tạo code toàn bộ scene, kết hợp đúng skill dạng toán.
---

# Skill: Manim Step 2 – Sinh Code Từ Scene Spec

## Mục đích

Nhận **Scene Spec** (từ Step 1) → Sinh ra **file Python Manim** hoàn chỉnh với tất cả các scene method. Bước này kết hợp spec + skill dạng toán để tạo code chất lượng cao.

---

## Khi nào dùng skill này?

- Có sẵn một `scene-spec.md` từ Step 1
- Người dùng cung cấp scene breakdown dạng text / Gemini draft
- Người dùng muốn sinh code cho một hoặc nhiều scene cụ thể
- Người dùng muốn convert từ `Scene` (không voiceover) sang `VoiceoverScene`

---

## Quy trình thực hiện

### Bước 1 – Đọc và phân tích spec

1. Đọc `scene-spec.md` (hoặc nội dung spec được cung cấp)
2. Xác định:
   - Loại toán → chọn skill (`manim-hinh-phang` hoặc `manim-dai-so-hinh-khong-gian`)
   - Số scene và thứ tự
   - State chia sẻ giữa các scene (`self.*`)
3. Đọc skill dạng toán tương ứng để lấy pattern cụ thể
4. Áp dụng pattern bookmark-driven ở mục "Pattern: Đọc segments → sinh voiceover block với bookmark" bên dưới

### Bước 2 – Tạo file Python

**Template file hoàn chỉnh**:

```python
from manim import *
import numpy as np
from manim_voiceover import VoiceoverScene

from manim_helpers import (
    make_gtts_service,
    # geometry helpers
    line_intersection, cross2d, angle_between_vectors,
    AngleMarker, GeometryEngine,
    # proof + sync
    ProofLine,
    sync_point, sync_segment, sync_angle,
    sync_triangle, sync_quadrilateral, sync_relation,
    # design tokens
    COLOR_DEFAULT, COLOR_BACKGROUND, COLOR_GRID,
    COLOR_EQUAL_1, COLOR_EQUAL_2, COLOR_EQUAL_3,
    COLOR_ACTIVE, COLOR_SECONDARY, COLOR_FADED,
    COLOR_RESULT_KEY, COLOR_RESULT_FINAL,
    COLOR_CIRCLE, COLOR_RIGHT_ANGLE, COLOR_AUX_LINE, COLOR_TANGENT,
    STATE_DEFAULT, STATE_HIGHLIGHT, apply_state,
    TIMING_POINT, TIMING_SEGMENT, TIMING_ANGLE,
    TIMING_INDICATE_SEGMENT, TIMING_INDICATE_TRIANGLE,
    TIMING_PROOF_WRITE, TIMING_RELATION, TIMING_CONCLUSION, TIMING_FADE,
    LAYER_BACKGROUND, LAYER_GEOMETRY, LAYER_MARKERS,
    LAYER_PROOF_TEXT, LAYER_HIGHLIGHT,
)


# TeX Template chuẩn cho tiếng Việt
viet_tex_template = TexTemplate(
    tex_compiler="xelatex",
    output_format=".xdv",
    preamble=r"""
\usepackage{fontspec}
\usepackage{amsmath}
\usepackage{amssymb}
\usepackage{vntex}
\setmainfont{Times New Roman}
"""
)


class TenBaiToan(VoiceoverScene):
    def construct(self):
        self.set_speech_service(make_gtts_service())
        self.scene01_introVaDeBai()
        self.scene02_chienThuat()
        self.scene03_buoc1()
        # ... thêm các scene theo spec

    def scene01_introVaDeBai(self):
        # 1. Khởi tạo GeometryEngine ngay đầu scene đầu tiên — dùng xuyên suốt video
        self.geo = GeometryEngine(self)
        # 2. Tính tọa độ + tạo Mobject + register vào self.geo (xem manim-hinh-phang)
        # 3. ... rest of scene 01
        pass

    def scene02_chienThuat(self):
        # Mọi scene sau dùng self.geo đã có sẵn từ scene01
        pass
```

> **Bắt buộc**: `line_intersection`, `cross2d`, `angle_between_vectors`, `AngleMarker` import từ `manim_helpers` — KHÔNG copy-paste vào file. `self.geo = GeometryEngine(self)` được khởi tạo ở scene đầu, các scene sau truy cập qua `self.geo.*`.

**Tốc độ voiceover**: dùng `make_gtts_service()` (đã import ở template). Chỉnh `VOICEOVER_GLOBAL_SPEED` trong `manim_helpers/voiceover_config.py` — không hardcode `global_speed` trong file scene trừ khi spec yêu cầu.

### Bước 3 – Implement từng scene method

Với mỗi scene trong spec, implement theo thứ tự:

1. **Dọn dẹp đầu scene** (nếu cần)
2. **Tạo title** → `to_corner(UL)`
3. **Tính toán tọa độ** (numpy, không animate)
4. **Tạo Mobjects**
5. **Voiceover blocks** (mỗi ý = 1 `with self.voiceover(...) as ov:`)
6. **Đóng khung kết quả** + `to_corner(UR)`
7. **Dọn dẹp cuối scene** (FadeOut, lưu self.*)

---

## Quy tắc chọn Animation

### Khi nào dùng gì

Dòng chứng minh nhiều token: dùng `ProofLine` + `pf.write(...)` (token khởi đầu invisible — xem `manim-proof-sync` §2). **Tex / MathTex một khối** (GT/KL, tiêu đề) cần reveal theo voiceover: tách dòng + `Write` tuần tự hoặc `AnimationGroup(..., lag_ratio=...)` — xem `manim-proof-sync` §5b.

```python
# Hiện text/formula mới
self.play(Write(new_text))
self.play(Write(new_mathTex))

# Hiện hình hình học
self.play(Create(circle))
self.play(Create(polygon))
self.play(Create(line))
self.play(Create(dot))

# Biến đổi phương trình (có ký hiệu chung)
self.play(TransformMatchingTex(eq_old, eq_new))

# Copy từ nguồn → tạo kết quả mới (nguồn vẫn còn)
self.play(TransformFromCopy(source_group, result))

# Thay hoàn toàn một Mobject bằng Mobject mới
self.play(ReplacementTransform(old_mob, new_mob))

# Nhấn mạnh, thu hút chú ý
self.play(Indicate(mob, color=YELLOW, scale_factor=1.2))
self.play(Flash(dot))

# Hiện / Ẩn
self.play(FadeIn(mob))
self.play(FadeOut(mob))

# Di chuyển đến vị trí mới
self.play(mob.animate.move_to(target))
self.play(mob.animate.next_to(other_mob, DOWN))
self.play(mob.animate.to_corner(UR, buff=0.5))
self.play(mob.animate.scale(0.8))
```

### Kết hợp animation trong cùng một play()

```python
# Chạy song song (cùng lúc)
self.play(
    Write(title),
    Create(diagram[0]),
    run_time=2.0
)
```

---

## Các pattern scene phổ biến

### Pattern: Đọc segments → sinh voiceover block với bookmark + sync_*

Khi spec dùng format segment mới (xem `../1-spec/SKILL-hinh-hoc.md`), mỗi `segment_N` được dịch thành 1 `with self.voiceover(...)` block. Có 2 trường hợp:

#### Trường hợp 1 – Segment đơn giản (dùng `write: text:` cũ)

Áp dụng khi segment có 1 bookmark + 1 dòng MathTex / Tex đơn lẻ. Format spec cũ vẫn dùng được; pattern này KHÔNG đổi.

#### Trường hợp 2 – Segment chứng minh nhiều thực thể (dùng `proof_tokens` + actions `sync_*`)

Áp dụng cho mọi dòng "△OFB = △OFC (c.g.c) ⇒ BF = FC; ∠OFB = ∠OFC" — tức bất kỳ dòng nào liệt kê ≥ 2 thực thể hình học. Đây là pattern **mới và bắt buộc** từ Step 1 trở đi.

**Spec segment (rút gọn từ ví dụ trong `../1-spec/SKILL-hinh-hoc.md`):**

```
#### segment_K
- voice: >
    "Do đó <bookmark mark='tri_OFB_expr'/> tam giác O F B
     <bookmark mark='tri_equal_expr'/> bằng
     <bookmark mark='tri_OFC_expr'/> tam giác O F C
     <bookmark mark='tri_cgc_expr'/> theo trường hợp cạnh góc cạnh.
     <bookmark mark='seg_BF_expr'/> Suy ra B F
     <bookmark mark='seg_equal_expr'/> bằng
     <bookmark mark='seg_FC_expr'/> F C."
- proof_tokens:
    - id: tri_OFB     latex: \triangle OFB
    - id: eq1         latex: =
    - id: tri_OFC     latex: \triangle OFC
    - id: cgc         latex: \;(\text{c.g.c})
    - id: seg_BF      latex: ;\quad BF
    - id: seg_eq      latex: =
    - id: seg_FC      latex: FC
- actions:
    - at: tri_OFB_expr   → sync_triangle(token=tri_OFB, shape=tri_OFB_fill, color=COLOR_EQUAL_1)
    - at: tri_equal_expr → sync_relation(token=eq1)
    - at: tri_OFC_expr   → sync_triangle(token=tri_OFC, shape=tri_OFC_fill, color=COLOR_EQUAL_2)
    - at: tri_cgc_expr   → sync_relation(token=cgc)
    - at: seg_BF_expr    → sync_segment(token=seg_BF, shape=seg_BF, color=COLOR_EQUAL_1)
    - at: seg_equal_expr → sync_relation(token=seg_eq)
    - at: seg_FC_expr    → sync_segment(token=seg_FC, shape=seg_FC, color=COLOR_EQUAL_1)
```

**Python code tương ứng:**

```python
# 1. proof_tokens → khởi tạo ProofLine ngay trước voiceover block
pf_05 = ProofLine(
    ("tri_OFB", r"\triangle OFB"),
    ("eq1",     "="),
    ("tri_OFC", r"\triangle OFC"),
    ("cgc",     r"\;(\text{c.g.c})"),
    ("seg_BF",  r";\quad BF"),
    ("seg_eq",  "="),
    ("seg_FC",  r"FC"),
    tex_template=viet_tex_template, font_size=26,
).place_below(cursor)
self.add(pf_05)
proof.add(pf_05)

# 2. Voiceover block — mỗi action `at: bookmark` → 1 dòng sync_*
with self.voiceover(text=(
    "Do đó <bookmark mark='tri_OFB_expr'/> tam giác O F B "
    "<bookmark mark='tri_equal_expr'/> bằng "
    "<bookmark mark='tri_OFC_expr'/> tam giác O F C "
    "<bookmark mark='tri_cgc_expr'/> theo trường hợp cạnh góc cạnh. "
    "<bookmark mark='seg_BF_expr'/> Suy ra B F "
    "<bookmark mark='seg_equal_expr'/> bằng "
    "<bookmark mark='seg_FC_expr'/> F C."
)) as ov:
    sync_triangle(self, "tri_OFB_expr", pf_05.write("tri_OFB"),
                  self.geo.triangle_fill("OFB"), color=COLOR_EQUAL_1)
    sync_relation(self, "tri_equal_expr", pf_05.write("eq1"))
    sync_triangle(self, "tri_OFC_expr", pf_05.write("tri_OFC"),
                  self.geo.triangle_fill("OFC"), color=COLOR_EQUAL_2)
    sync_relation(self, "tri_cgc_expr", pf_05.write("cgc"))
    sync_segment(self, "seg_BF_expr", pf_05.write("seg_BF"),
                 self.geo.segment("BF"), color=COLOR_EQUAL_1)
    sync_relation(self, "seg_equal_expr", pf_05.write("seg_eq"))
    sync_segment(self, "seg_FC_expr", pf_05.write("seg_FC"),
                 self.geo.segment("FC"), color=COLOR_EQUAL_1)

cursor = pf_05.get_bottom_left_cursor() + DOWN * 0.05
```

**Quy tắc dịch từng thành phần (mở rộng):**

| Spec                                              | Python                                                    |
|---------------------------------------------------|-----------------------------------------------------------|
| `voice: "... <bookmark mark='...'/> ..."`         | Chuỗi `text=` của `self.voiceover()`                      |
| `proof_tokens: [(id, latex), ...]`                | `pf_NN = ProofLine(...).place_below(cursor)` trước `with` |
| `at: <type>_<name>_expr → sync_<type>(...)`        | `sync_<type>(self, "<bk>", pf_NN.write("X"), shape, ...)` |
| `at: <type>_equal_expr → sync_relation(token=X)`  | `sync_relation(self, "<bk>", pf_NN.write("X"))`            |
| `at: tri_cgc_expr → sync_relation(token=cgc)`     | `sync_relation(self, "tri_cgc_expr", pf_NN.write("cgc"))`  |
| `at: start → AnimA(), AnimB()`                    | `self.play(...)` đầu block, trước mọi sync_*               |
| `at: end → AnimD()`                               | Hiếm dùng — ưu tiên bookmark cụ thể                       |
| `[after Xs] FadeOut(mob)`                         | `self.wait(X)` + `FadeOut` sau `with` (hoặc cleanup_temp)  |
| `post: Circumscribe(mob, ...)`                    | `Circumscribe(..., color=COLOR_RESULT_FINAL)` sau `with`   |
| `write: ~` (không proof token)                    | Không khởi tạo ProofLine trong segment                     |
| `write: text: "...", at: bk_x` (segment cũ)       | MathTex + `Write(...)` trong action `at: bk_x`             |

**Quy tắc thứ tự bắt buộc trong 1 voiceover block:**

```python
with self.voiceover(text="...bookmarks...") as ov:
    # 1. (Optional) Action at: start chạy ngay đầu block
    self.play(...)

    # 2. Lần lượt theo thứ tự bookmark trong voice:
    sync_<type>(self, "<bookmark_1>", pf.write("token_1"), <shape>, color=<COLOR>)
    sync_relation(self, "<bookmark_2>", pf.write("token_2"))
    sync_<type>(self, "<bookmark_3>", pf.write("token_3"), <shape>, color=<COLOR>)
    # ...

    # 3. KHÔNG thêm self.wait(ov.duration) ở cuối — voiceover tự chờ
```

**Lưu ý quan trọng**:

- Mỗi `sync_*()` đã gọi `wait_until_bookmark` nội bộ — KHÔNG còn viết `self.wait_until_bookmark(...)` thủ công.
- `pf.write(token_id)` trả Animation, được truyền vào `sync_*` như tham số `tex_anim` — KHÔNG gọi `self.play(pf.write(...))` rời.
- `sync_angle(...)` chỉ FadeIn sector, KHÔNG tự FadeOut. Cuối block phải gọi `self.geo.cleanup_temp()` hoặc `FadeOut(sector)` thủ công.
- Tất cả `color=` trong sync_* dùng `COLOR_EQUAL_*` token (xem `manim-design-tokens`).

**Xử lý section `### objects` (Loại A):**

```python
# Trước vòng lặp segment, dựng tất cả object Loại A khai báo trong ### objects:
circle_AI = Circle(radius=R_circle, color="#1565C0")
dot_O = Dot(O_pos, color="#E65100", radius=0.07)
label_O = MathTex("O", tex_template=viet_tex_template).next_to(O_pos, RIGHT, buff=0.12)

# Các object này được dùng trong actions của các segment bên dưới.
# Sau khi Create trong segment tương ứng, nếu add_to_persistent=yes:
self.persistent_geom.add(circle_AI, dot_O, label_O)
```

**Xử lý section `### metadata`:**

```python
# cleanup_start → FadeOut ngay đầu scene method
self.play(FadeOut(self.gt_vgroup), FadeOut(self.kl_vgroup))

# cleanup_end → FadeOut ở cuối scene method (sau tất cả segments)
self.play(FadeOut(proof), FadeOut(title_a))

# persist → lưu vào self.* để scene sau truy cập
self.circle_AI = circle_AI
self.dot_O = dot_O
```

**Ví dụ đầy đủ: scene chứng minh "△OFB = △OFC (c.g.c)" — pattern mới với `ProofLine` + `sync_*`:**

```python
def scene04_chungMinhTaiTrungDiem(self):
    # --- metadata: cleanup_start ---
    self.play(FadeOut(self.title_prev))

    # --- objects Loại A ---
    seg_OF = Line(self.O_pos, self.F_pos, color=COLOR_AUX_LINE)
    self.geo.register_segment("OF", seg_OF)
    self.play(Create(seg_OF))
    self.persistent_geom.add(seg_OF)

    # --- title ---
    title = Tex(r"\textbf{Bước 2: $\triangle OFB = \triangle OFC$ (c.g.c)}",
                tex_template=viet_tex_template, font_size=32).to_corner(UL, buff=0.5)
    self.play(Write(title))

    # --- proof accumulator + cursor ---
    proof = VGroup()
    left_x = title.get_left()[0]
    cursor = np.array([left_x, title.get_bottom()[1] - 0.4, 0])

    # --- objects Loại B (Polygon fill cho 2 tam giác — invisible cho đến khi sync) ---
    self.add(self.geo.register_triangle_fill("OFB"))
    self.add(self.geo.register_triangle_fill("OFC"))

    # === segment_K — proof_tokens + sync_* (pattern mới) ===
    pf_05 = ProofLine(
        ("tri_OFB", r"\triangle OFB"),
        ("eq1",     "="),
        ("tri_OFC", r"\triangle OFC"),
        ("cgc",     r"\;(\text{c.g.c})"),
        ("seg_BF",  r";\quad BF"),
        ("seg_eq",  "="),
        ("seg_FC",  r"FC"),
        tex_template=viet_tex_template, font_size=26,
    ).place_below(cursor)
    self.add(pf_05)
    proof.add(pf_05)

    with self.voiceover(text=(
        "Do đó <bookmark mark='tri_OFB_expr'/> tam giác O F B "
        "<bookmark mark='tri_equal_expr'/> bằng "
        "<bookmark mark='tri_OFC_expr'/> tam giác O F C "
        "<bookmark mark='tri_cgc_expr'/> theo trường hợp cạnh góc cạnh. "
        "<bookmark mark='seg_BF_expr'/> Suy ra B F "
        "<bookmark mark='seg_equal_expr'/> bằng "
        "<bookmark mark='seg_FC_expr'/> F C."
    )) as ov:
        sync_triangle(self, "tri_OFB_expr", pf_05.write("tri_OFB"),
                      self.geo.triangle_fill("OFB"), color=COLOR_EQUAL_1)
        sync_relation(self, "tri_equal_expr", pf_05.write("eq1"))
        sync_triangle(self, "tri_OFC_expr", pf_05.write("tri_OFC"),
                      self.geo.triangle_fill("OFC"), color=COLOR_EQUAL_2)
        sync_relation(self, "tri_cgc_expr", pf_05.write("cgc"))
        sync_segment(self, "seg_BF_expr", pf_05.write("seg_BF"),
                     self.geo.segment("BF"), color=COLOR_EQUAL_1)
        sync_relation(self, "seg_equal_expr", pf_05.write("seg_eq"))
        sync_segment(self, "seg_FC_expr", pf_05.write("seg_FC"),
                     self.geo.segment("FC"), color=COLOR_EQUAL_1)

    cursor = pf_05.get_bottom_left_cursor() + DOWN * 0.05

    # === segment kết luận — Pattern B (Circumscribe đpcm) ===
    pf_result = ProofLine(
        ("imp",      r"\Rightarrow"),
        ("midpoint", r"F\ \text{là trung điểm}"),
        ("seg_BC",   r"\ BC"),
        tex_template=viet_tex_template, font_size=26,
    ).place_below(cursor)
    self.add(pf_result)
    proof.add(pf_result)

    with self.voiceover(text="Vậy <bookmark mark='dot_F_expr'/> F là trung điểm của B C.") as ov:
        sync_relation(self, "dot_F_expr", pf_result.write_all(),
                      write_time=TIMING_CONCLUSION)
        self.play(Circumscribe(pf_result, color=COLOR_RESULT_FINAL,
                               fade_out=True, run_time=1.5))

    # --- cleanup any leftover temporary markers ---
    self.geo.cleanup_temp()

    # --- metadata: cleanup_end ---
    self.play(FadeOut(proof), FadeOut(title))

    # --- metadata: persist ---
    self.seg_OF = seg_OF
```

**Ví dụ segment đơn giản (Trường hợp 1 – format cũ vẫn hợp lệ):**

```python
def scene03_setupGoalCauA(self):
    self.play(FadeOut(self.gt_vgroup), FadeOut(self.kl_vgroup))

    title_a = Tex(r"\textbf{Ý a: CM I là trung điểm EF}",
                  tex_template=viet_tex_template, font_size=34).to_corner(UL, buff=0.5)
    self.play(Write(title_a))

    proof = VGroup()
    left_x = title_a.get_left()[0]
    cursor = np.array([left_x, title_a.get_bottom()[1] - 0.4, 0])

    # === segment_1 — write: text dạng cũ vẫn dùng được khi chỉ có 1 thực thể ===
    with self.voiceover(text=(
        "Câu a yêu cầu <bookmark mark='dot_I_expr'/> chứng minh I là trung điểm của E F."
    )) as ov:
        muc_tieu = MathTex(r"IE = IF",
                           tex_template=viet_tex_template, font_size=28)
        muc_tieu.next_to(cursor, DOWN, aligned_edge=LEFT, buff=0.18)
        self.wait_until_bookmark("dot_I_expr")
        self.play(Write(muc_tieu),
                  Indicate(self.geo._dots["I"], color=COLOR_ACTIVE, scale_factor=1.8),
                  run_time=TIMING_CONCLUSION)
        proof.add(muc_tieu)

    # ... các segment tiếp theo dùng pattern proof_tokens + sync_* ...
```

### Pattern: Scene intro đề bài

```python
def scene01_introVaDeBai(self):
    # Intro animation
    with self.voiceover(text="Chào các em!...") as ov:
        title1 = Text("Tiêu đề chính", font="Times New Roman", weight=BOLD, font_size=48)
        self.play(Write(title1), run_time=ov.duration * 0.5)
        self.play(FadeOut(title1), run_time=ov.duration * 0.3)

    # GT/KL VGroup
    self.gt_vgroup = VGroup(
        Tex(r"\textbf{Cho (Giả thiết):}", tex_template=viet_tex_template, font_size=40),
        Tex(r"- Điều kiện 1", tex_template=viet_tex_template, font_size=36),
        Tex(r"- Điều kiện 2", tex_template=viet_tex_template, font_size=36),
    ).arrange(DOWN, aligned_edge=LEFT, buff=0.2).to_corner(UL, buff=0.5)

    self.kl_vgroup = VGroup(
        Tex(r"\textbf{Kết luận:}", tex_template=viet_tex_template, font_size=40),
        Tex(r"a) Kết luận a", tex_template=viet_tex_template, font_size=36),
    ).arrange(DOWN, aligned_edge=LEFT, buff=0.2).next_to(self.gt_vgroup, DOWN, buff=0.5, aligned_edge=LEFT)

    # Tính toán tọa độ hình học
    # ...

    # Tạo Mobjects và diagram
    # ...
    self.diagram = diagram_elements.scale(0.8).shift(RIGHT * 4.0, DOWN * 1.0)

    # Dựng hình từng bước với voiceover
    with self.voiceover(text="Cho nửa đường tròn...") as ov:
        self.play(Write(VGroup(*self.gt_vgroup[0:3])), run_time=ov.duration * 0.1)
        n_steps = 6
        run_t = (ov.duration * 0.85) / n_steps
        self.play(Create(self.diagram[0]), run_time=run_t)
        # ... tiếp tục dựng

    # Hiện KL
    self.play(Write(self.kl_vgroup.get_submobjects()[0]))
    with self.voiceover(text="Yêu cầu...") as ov:
        self.play(Write(self.kl_vgroup.get_submobjects()[1]), run_time=ov.duration * 0.7)
        self.play(Indicate(self.kl_vgroup.get_submobjects()[1], scale_factor=1.2))
```

### Pattern: Scene tổng kết

```python
def sceneN_tongKet(self):
    title = Tex(r"\textbf{Tổng kết}", tex_template=viet_tex_template, font_size=42)
    title.to_corner(UL, buff=0.5)
    self.play(Write(title))

    # Di chuyển các kết quả đã lưu về bên trái
    with self.voiceover(text="Tóm lại...") as ov:
        self.play(self.result1.animate.next_to(title, DOWN, buff=0.3, aligned_edge=LEFT))
        self.play(self.result2.animate.next_to(self.result1, DOWN, buff=0.3, aligned_edge=LEFT))

    # Kết luận cuối
    with self.voiceover(text="Suy ra...") as ov:
        final = Tex(r"$\Rightarrow$ Kết luận cuối", tex_template=viet_tex_template)
        final.next_to(self.result2, DOWN, buff=0.5, aligned_edge=LEFT)
        self.play(Write(final))
        box = SurroundingRectangle(VGroup(self.result1, self.result2, final), color=RED, buff=0.3)
        self.play(Create(box))

    self.wait(2)
```

---

## Xử lý các trường hợp đặc biệt

### Khi góc `RightAngle` hiện sai vị trí

```python
# Thử lần lượt quadrant: (1,1), (-1,1), (1,-1), (-1,-1)
# Xem kết quả sau mỗi lần render thử
right_angle = RightAngle(line1, line2, length=0.3, quadrant=(-1, 1), color=WHITE)
```

### Khi `TransformMatchingTex` lỗi

Kiểm tra các ký hiệu có khớp chính xác không. Nếu không:
```python
# Fallback: FadeOut cái cũ, Write cái mới
self.play(FadeOut(old_eq))
self.play(Write(new_eq))
```

### Khi text bị chồng lên nhau

```python
# FadeOut nhóm cũ trước khi thêm mới
group_to_clear = VGroup(eq1, eq2, eq3)
self.play(
    FadeOut(group_to_clear),
    new_mob.animate.move_to(old_position),
    run_time=0.4
)
```

### Khi muốn giữ lại và di chuyển kết quả

```python
# Không FadeOut kết quả, thay vào đó animate di chuyển
result_group = VGroup(result_mob, result_box)
self.play(
    FadeOut(other_stuff),
    result_group.animate.to_corner(UR, buff=0.5).scale(0.9)
)
```

---

## Danh sách self.* cần lưu (hình phẳng điển hình)

```python
# Scene 01 lưu lại:
self.diagram         # VGroup toàn bộ hình, đã scale + shift
self.gt_vgroup       # VGroup GT text
self.kl_vgroup       # VGroup KL text
self.dot_C           # Dot C (để lấy get_center())
self.dot_D           # Dot D
self.dot_E           # Dot E
self.dot_F           # Dot F
self.dot_I           # Dot I
self.diameter        # Line A-B (dùng cho RightAngle)
self.segment_AC      # Line A-C
self.segment_BC      # Line B-C (hoặc B-F)
self.line_EF_obj     # Line E-F (dùng cho RightAngle)
self.right_angle_C_ACB  # RightAngle tại C
self.line_CE         # Line C-E (dùng cho Angle ở scene sau)
self.line_CF         # Line C-F

# Mỗi scene chứng minh lưu thêm:
self.result1_group   # VGroup(result_mob, box) từ scene 03 → dùng ở scene tổng kết
self.result2_group   # VGroup từ scene 04
```

---

## Checklist trước khi submit code

- [ ] Import đúng: `from manim import *`, `from manim_voiceover import VoiceoverScene`
- [ ] **Bắt buộc**: `from manim_helpers import *` (hoặc named imports đầy đủ token + helper)
- [ ] `viet_tex_template` ở module level; `line_intersection`, `cross2d`, `angle_between_vectors`, `AngleMarker` import từ `manim_helpers` (KHÔNG copy-paste vào file)
- [ ] Class kế thừa `VoiceoverScene`
- [ ] Dòng đầu `construct()`: `self.set_speech_service(make_gtts_service())` — **không** gọi `GTTSService(...)` trực tiếp
- [ ] Tốc độ voiceover: chỉnh `VOICEOVER_GLOBAL_SPEED` trong `manim_helpers/voiceover_config.py` (không hardcode `global_speed` trong file scene)
- [ ] **Scene đầu tiên** khởi tạo `self.geo = GeometryEngine(self)`; mọi điểm/đoạn/tam giác/tứ giác có `self.geo.register_*(...)` ngay sau khi tạo Mobject
- [ ] Mỗi scene method được gọi đúng thứ tự trong `construct()`
- [ ] Mọi `Tex(...)` / `MathTex(...)` tiếng Việt có `tex_template=viet_tex_template`
- [ ] **Mọi `color=` dùng `COLOR_*` token** (xem `manim-design-tokens`); KHÔNG hardcode hex
- [ ] **Mọi `run_time=` của effect dùng `TIMING_*` token**; KHÔNG hardcode số
- [ ] **Mọi `set_z_index(...)` dùng `LAYER_*` token**; KHÔNG hardcode `2`, `5`
- [ ] **Mỗi proof line dùng `ProofLine(...)`** với token semantic; mỗi token được Write qua `pf.write("id")` đồng bộ với 1 bookmark `<type>_<name>_expr`
- [ ] **Mọi action highlight (đoạn / góc / tam giác / tứ giác / điểm) dùng `sync_<type>(...)`**; KHÔNG raw `Indicate(...)` / `FadeIn(Sector(...))` / `seg.animate.set_stroke(...)` thủ công
- [ ] `sync_*` đã gọi `wait_until_bookmark` nội bộ — KHÔNG còn viết thủ công trong code
- [ ] `sync_angle(...)` được clean up ở cuối block (qua `self.geo.cleanup_temp()` hoặc `FadeOut` thủ công)
- [ ] Mọi `Sector` / `AngleMarker` / `Polygon` highlight dùng `self.geo.*` API; KHÔNG khai báo `Sector(arc_center=..., start_angle=..., angle=...)` thủ công
- [ ] Quy tắc màu (rule 5): cùng 1 màu cho tập "bằng nhau" (`COLOR_EQUAL_1`); 2+ màu khác cho phân biệt (`COLOR_EQUAL_1`/`_2`/`_3`)
- [ ] Mọi Mobject tạm được FadeOut ở cuối scene
- [ ] State `self.*` được lưu đúng để scene sau truy cập (đặc biệt `self.geo`, `self.persistent_geom`, `self.diagram`)
- [ ] Kết quả trung gian: `SurroundingRectangle(..., color=COLOR_RESULT_KEY)`
- [ ] Kết quả cuối / đpcm: `SurroundingRectangle(..., color=COLOR_RESULT_FINAL)` HOẶC `Circumscribe(..., color=COLOR_RESULT_FINAL, fade_out=True)`
- [ ] Mỗi `segment_N` trong spec → đúng 1 `with self.voiceover(...)` block, không tách không gộp
- [ ] Chuỗi `text=` trong `self.voiceover()` copy nguyên xi `voice:` từ spec, giữ nguyên `<bookmark mark="..."/>` tags
- [ ] Tên bookmark theo pattern `<type>_<name>_expr` (`tri_OFB_expr`, `seg_BF_expr`, `tri_equal_expr`, ...) — KHÔNG còn dùng `bk_*`
- [ ] Spec có `proof_tokens` → khởi tạo `pf_NN = ProofLine(...)` ngay TRƯỚC `with self.voiceover(...)` block
- [ ] Spec có `at: <bookmark> → sync_<type>(token=X, shape=Y, color=Z)` → 1 dòng `sync_<type>(self, "<bookmark>", pf_NN.write("X"), <shape_var>, color=<Z>)` trong block
- [ ] Spec có `at: <bookmark> → sync_relation(token=X)` → 1 dòng `sync_relation(self, "<bookmark>", pf_NN.write("X"))` trong block
- [ ] Mọi `at: start` action được `self.play(...)` ngay đầu block, **trước** mọi `sync_*`
- [ ] Thứ tự `sync_*` trong code khớp thứ tự bookmark xuất hiện trong chuỗi `voice`
- [ ] `write: text, at: bk_x` (format cũ) → `Write(proof_line)` nằm trong cùng `self.play(...)` tại bookmark `bk_x` (vẫn hợp lệ cho segment đơn)
- [ ] `[after Xs] FadeOut(mob)` → có `self.wait(X)` rồi `self.play(FadeOut(mob))`
- [ ] `post: Circumscribe(...)` → có thêm `self.play(Circumscribe(..., color=COLOR_RESULT_FINAL, fade_out=True))` sau block write tương ứng
- [ ] Object Loại A (`add_to_persistent=yes`) được `self.persistent_geom.add(...)` ngay sau khi `Create`
- [ ] `cleanup_start` từ metadata → `FadeOut(...)` ở đầu scene method
- [ ] `cleanup_end` từ metadata → `FadeOut(...)` ở cuối scene method (sau tất cả segments)
- [ ] `persist` từ metadata → mỗi object được gán `self.tên_object = tên_object` ở cuối scene method
