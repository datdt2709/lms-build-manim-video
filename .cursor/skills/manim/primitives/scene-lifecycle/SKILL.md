---
name: manim-scene-lifecycle
description: Quản lý vòng đời Mobject trong scene: FadeOut khi kết thúc, persistent_geom, proof_accumulator. Dùng khi cần quyết định nhóm Mobject nào tồn tại qua các bước chứng minh.
---

# Skill: Manim – Scene Lifecycle & Cleanup

## Khi nào dùng skill này?

Dùng khi cần quyết định:
- Mobject nào phải `FadeOut` khi scene kết thúc?
- Mobject nào thuộc `self.persistent_geom`?
- Cách quản lý `proof_accumulator` trong scene nhiều bước?
- Dòng kết luận / `result_tex` nằm trong nhóm nào?

> Skill này tách ra từ `SKILL-hinh-phang` (mục 8, 11, 12). Xem skill đó cho geometry construction.

---

## 1. Phân loại Mobject theo vòng đời

| Category       | Ví dụ                                      | Khởi tạo                         | Cleanup cuối scene                          |
|----------------|--------------------------------------------|----------------------------------|---------------------------------------------|
| **persistent** | hình vẽ, `seg_*`, `dot_*`, `ra_*`, `circ_*`| Scene 01 → `self.persistent_geom`| **KHÔNG FadeOut bao giờ**                   |
| **temp_text**  | `title`, `goal`, `muc_tieu`                | Đầu mỗi scene                    | `FadeOut` cuối scene                        |
| **proof**      | `pf_01..pf_NN`, `note_*`, dòng CM          | Tích lũy `proof = VGroup()`      | `FadeOut(proof)` — kể cả `result_tex` cuối  |
| **ui**         | `gt_vgroup`, `kl_vgroup` (GT/KL intro)     | Scene 01                         | `FadeOut` ở đầu scene 02                    |
| **result**     | `result_group = VGroup(pf_result, box)`    | Cuối mỗi scene CM                | `to_corner(UR)`; `FadeOut` khi dùng xong    |

---

## 2. Khởi tạo và duy trì `self.persistent_geom`

### Khởi tạo cuối Scene 01

```python
# Cuối scene01_introVaDeBai — SAU KHI đã Create/FadeIn toàn bộ hình vẽ:
self.persistent_geom = VGroup(
    self.semicircle, self.seg_AB,
    self.dot_O, self.label_O,
    self.dot_A, self.label_A, self.dot_B, self.label_B,
    self.dot_C, self.label_C,
    self.dot_D, self.label_D,
    self.seg_AC, self.seg_BC,
    self.line_EF_obj,
    self.dot_E, self.label_E, self.dot_F, self.label_F,
    self.ra_D, self.ra_C,
    # tangent line nếu đã FadeIn:
    self.tangent_line_obj, self.dot_I, self.label_I,
)
# KHÔNG add: gt_vgroup, kl_vgroup, title, result — chúng là text/ui, sẽ FadeOut
```

### Cập nhật mỗi khi Create nét Loại A mới (scene sau)

```python
# Ngay sau Create hoặc FadeIn nét Loại A mới:
self.seg_MN = Line(M, N, color=COLOR_AUX_LINE)
self.play(Create(self.seg_MN))
self.persistent_geom.add(self.seg_MN)   # ← bắt buộc
self.bring_to_front(*all_dots, *all_labels)
```

### Quy tắc bất di bất dịch

- **KHÔNG bao giờ** `FadeOut` bất kỳ phần tử nào trong `self.persistent_geom`.
- Nếu cần làm mờ tạm thời để highlight: dùng `apply_state(mob, STATE_FADED)` rồi phục hồi `STATE_DEFAULT`.
- Sau `FadeOut(proof)` — hình vẽ vẫn còn nguyên vì nằm trong `persistent_geom`.

---

## 3. Quy tắc FadeOut cuối scene

```python
# Pattern chuẩn cuối mỗi scene chứng minh:
self.play(
    FadeOut(title),         # temp_text
    FadeOut(goal),          # temp_text
    FadeOut(proof),         # proof VGroup — gồm mọi pf_* và note_*
    # KHÔNG FadeOut self.persistent_geom
    # result_group đã to_corner(UR) → giữ nguyên
)
```

### Bảng quyết định nhanh

| Mobject                                        | FadeOut khi kết thúc scene?                    |
|------------------------------------------------|--------------------------------------------------|
| `title`, `goal`, `muc_tieu`                    | ✓ Có                                           |
| `eq_*`, `note_*`, dòng chứng minh              | ✓ Có (trong `proof`)                             |
| `pf_01`, `pf_02`, ..., `pf_NN`                 | ✓ Có (trong `proof`)                             |
| `result_tex` / dòng đpcm (`ProofLine` kết luận) | ✓ Có — trong `proof` hoặc `cleanup_end`          |
| Bất kỳ phần tử trong `persistent_geom`         | ✗ Không                                          |
| `result_group` (box kết quả trung gian)        | Giữ và `to_corner(UR)`                         |

---

## 4. Lỗi orphan `result_tex` — cần tránh

**Lỗi phổ biến nhất**: `Write(result_tex)` nhưng `result_tex` nằm **ngoài** `proof`, nên khi `FadeOut(proof)` nó vẫn còn và **chồng lên** proof scene sau.

```python
# ❌ SAI — result_tex là orphan
proof = VGroup()
proof.add(pf_01, pf_02, note1)
# ...
result_tex = MathTex(r"\Rightarrow IE = IC").next_to(cursor, DOWN, ...)
self.play(Write(result_tex))       # result_tex không được add vào proof!
self.play(FadeOut(proof))          # result_tex vẫn còn trên màn hình → orphan

# ✓ ĐÚNG — thêm result vào proof trước khi FadeOut, HOẶC dùng ProofLine + box
result_tex = MathTex(r"\Rightarrow IE = IC").next_to(cursor, DOWN, ...)
self.play(Write(result_tex))
proof.add(result_tex)              # ← bắt buộc nếu result_tex không phải result_group
self.play(FadeOut(proof))
```

**Ngoại lệ hợp lệ**: Nếu kết luận cần giữ lại sang scene sau → dùng `result_group` pattern:

```python
pf_result = ProofLine(...)
box = SurroundingRectangle(pf_result, color=COLOR_RESULT_KEY, buff=0.15)
self.result_group = VGroup(pf_result, box)
self.play(self.result_group.animate.to_corner(UR, buff=0.5))
# result_group KHÔNG nằm trong proof → KHÔNG bị FadeOut cùng proof
# Scene sau: self.play(FadeOut(self.result_group)) khi không còn cần
```

---

## 5. Pattern `proof_accumulator` — nhiều bước trong 1 scene

### Nguyên tắc

**1 ý chứng minh = 1 scene method**. Nếu ý đó có nhiều bước lập luận nhưng tất cả hướng đến cùng 1 kết luận → toàn bộ nằm trong **1 scene method duy nhất**.

| Tình huống                                              | Quyết định                    |
|---------------------------------------------------------|-------------------------------|
| Bước 1 và 2 phục vụ cùng 1 kết luận                     | → 1 scene, `proof` tích lũy   |
| Bước 2 dùng ngay kết quả bước 1 (không KQ trung gian)   | → 1 scene, `proof` tích lũy   |
| Bước 1 và 2 ra **hai KQ trung gian độc lập** (2 box)    | → 2 scene methods riêng       |

### Giới hạn

Tổng số dòng `proof` ≤ **12 dòng** ở `font_size=26`. Nếu vượt → tách thành 2 scene.

### Code pattern chuẩn

```python
def scene07_chungMinhCauC(self):
    # 1. FadeOut ui/result từ scene trước nếu cần
    if hasattr(self, "result_b"):
        self.play(FadeOut(self.result_b))

    # 2. Tiêu đề + mục tiêu
    title = Tex(r"\textbf{CM ý c) – ...}",
                tex_template=viet_tex_template, font_size=32).to_corner(UL, buff=0.5)
    self.play(Write(title))

    goal = Tex(r"CM: ...", tex_template=viet_tex_template, font_size=28)
    goal.next_to(title, DOWN, aligned_edge=LEFT, buff=0.3)
    self.play(Write(goal))

    # 3. Khởi tạo proof accumulator
    proof = VGroup()
    left_x = title.get_left()[0]
    cursor = np.array([left_x, goal.get_bottom()[1] - 0.4, 0])

    # --- Bước 1 ---
    pf_01 = ProofLine(...).place_below(cursor)
    self.add(pf_01)
    with self.voiceover(text="...") as ov:
        sync_angle(self, ...)
        sync_relation(self, ...)
        sync_angle(self, ...)
    proof.add(pf_01)
    cursor = pf_01.get_bottom_left_cursor() + DOWN * 0.05

    note1 = Tex(r"(lý do...)", ..., font_size=24).next_to(
        cursor, DOWN, aligned_edge=LEFT, buff=0.18)
    self.play(Write(note1))
    proof.add(note1)
    cursor = np.array([left_x, note1.get_bottom()[1] - 0.25, 0])

    # --- Bước 2 (KHÔNG FadeOut proof giữa chừng) ---
    pf_02 = ProofLine(...).place_below(cursor)
    self.add(pf_02)
    with self.voiceover(text="...") as ov:
        ...
    proof.add(pf_02)
    cursor = pf_02.get_bottom_left_cursor() + DOWN * 0.05

    # --- Kết luận ---
    pf_result = ProofLine(
        ("imp", r"\Rightarrow"), ...,
        tex_template=viet_tex_template, font_size=26,
    ).place_below(cursor)
    self.add(pf_result)
    box_c = SurroundingRectangle(pf_result, color=COLOR_RESULT_FINAL, buff=0.15)
    with self.voiceover(text="Vậy ...") as ov:
        self.play(pf_result.write_all(), Create(box_c), run_time=ov.duration * 0.8)

    self.result_c = VGroup(pf_result, box_c)
    self.play(self.result_c.animate.to_corner(UR, buff=0.5))

    # 4. FadeOut proof + title + goal (proof KHÔNG bao gồm result_c)
    self.play(FadeOut(proof), FadeOut(title), FadeOut(goal))
```

### Lỗi cần tránh

```python
# ❌ SAI – FadeOut proof giữa 2 bước → mất liên tục chứng minh
def scene07_buoc1(self):
    ...
    self.play(FadeOut(proof))    # xóa bằng chứng trước khi dùng xong

def scene08_buoc2(self):         # tách scene cho cùng 1 ý
    ...

# ✓ ĐÚNG – 1 scene, proof tích lũy liên tục, FadeOut một lần ở cuối
def scene07_chungMinhCauC(self):
    proof = VGroup()
    # Bước 1: proof.add(pf_01, note1)
    # Bước 2: proof.add(pf_02)         ← KHÔNG FadeOut ở giữa
    # Kết luận: result_c = VGroup(pf_result, box) → to_corner(UR)
    self.play(FadeOut(proof), FadeOut(title))   # FadeOut một lần ở cuối
```

---

## 6. Quy tắc cập nhật `cursor`

> `cursor` phải là `np.array([left_x, y, 0])` với `left_x` cố định — **KHÔNG** dùng `mob.get_bottom()` trực tiếp vì trả về center-x của dòng, gây thụt lề drift dần mỗi dòng.

```python
# Khởi tạo cursor từ anchor cố định:
left_x = title.get_left()[0]
cursor = np.array([left_x, title.get_bottom()[1] - 0.4, 0])

# Sau mỗi ProofLine:
cursor = np.array([left_x, pf_N.get_bottom()[1] - 0.05, 0])

# Sau mỗi note Tex:
cursor = np.array([left_x, note.get_bottom()[1] - 0.25, 0])
```

> **Hoặc dùng `ProofColumn`** từ `manim_helpers` — quản lý `cursor` tự động (xem `manim-layout-system`).

---

## 7. Scene kết (tổng kết toàn bài)

Nếu có scene tổng kết tất cả kết quả:
- FadeOut tất cả `result_group` còn tồn tại ở UR.
- Tạo lại `Tex` / `MathTex` mới để tổng hợp (không reuse mob đã FadeOut).
- Có thể `FadeOut(self.persistent_geom)` nếu muốn màn hình trống hoàn toàn cho kết luận.

```python
def scene_final_ketLuan(self):
    # FadeOut các result còn trên màn hình
    cleanup = VGroup()
    for attr in ["result_a", "result_b", "result_c"]:
        if hasattr(self, attr):
            cleanup.add(getattr(self, attr))
    if len(cleanup):
        self.play(FadeOut(cleanup))

    # Tổng kết bằng Tex mới
    final = VGroup(
        Tex(r"\textbf{Kết luận:}", tex_template=viet_tex_template, font_size=36),
        Tex(r"a) ...", tex_template=viet_tex_template, font_size=32),
        Tex(r"b) ...", tex_template=viet_tex_template, font_size=32),
        Tex(r"c) ...", tex_template=viet_tex_template, font_size=32),
    ).arrange(DOWN, aligned_edge=LEFT, buff=0.25).to_corner(UL, buff=0.5)
    self.play(Write(final))
    self.wait(3)
```

---

## 8. Checklist lifecycle

- [ ] `self.persistent_geom` được khởi tạo cuối Scene 01, **sau** khi Create/FadeIn toàn bộ hình vẽ
- [ ] Mỗi lần `Create` nét Loại A mới: `self.persistent_geom.add(mob)` ngay lập tức
- [ ] KHÔNG bao giờ `FadeOut` phần tử trong `persistent_geom`
- [ ] Cuối mỗi scene: `FadeOut` đúng nhóm — `title`, `goal`, `proof` (temp_text + proof)
- [ ] `result_tex` / dòng đpcm nằm trong `proof` hoặc được tách vào `result_group` rõ ràng — không để orphan
- [ ] `proof_accumulator`: 1 ý = 1 scene method; không `FadeOut(proof)` giữa chừng
- [ ] Tổng dòng proof ≤ 12 dòng (font 26); nếu vượt → tách scene
- [ ] `cursor` luôn là `np.array([left_x, y, 0])` với `left_x` cố định — KHÔNG dùng `mob.get_bottom()` trực tiếp
- [ ] Kết quả trung gian: `result_group = VGroup(mob, box)`, `to_corner(UR)`, box `COLOR_RESULT_KEY`
- [ ] Kết luận đpcm: box `COLOR_RESULT_FINAL`; `Circumscribe(..., fade_out=True)` nếu không cần persistent
- [ ] Scene tổng kết: tạo `Tex` mới, không reuse mob đã FadeOut trước đó
