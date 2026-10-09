---
name: manim-algebra-step-solver
description: Layout cursor dọc không drift cho bài đại số — TransformMatchingTex, arrow ⟹, đóng khung kết quả trung gian/cuối. Dùng cho mọi bài giải phương trình, bất phương trình, hệ phương trình. KHÔNG bao gồm figure, number line, hay geometry.
---

# Skill: Manim – Algebra Step Solver (A1)

> Dành riêng cho **algebraic steps** (text/formula dọc).  
> Phân biệt với `proof-sync` (dành cho geometry proof + bookmark + ProofLine + hình).

---

## Khi nào dùng skill này?

- Giải phương trình, bất phương trình, hệ phương trình theo từng bước
- Biến đổi đẳng thức / bất đẳng thức
- Bất kỳ chuỗi algebraic steps cần trình bày dọc, căn trái, không drift

---

## 1. Import bắt buộc

```python
from manim_helpers import (
    COLOR_DEFAULT, COLOR_ACTIVE, COLOR_RESULT_KEY, COLOR_RESULT_FINAL,
    COLOR_FADED,
    MOTION_ENTER, MOTION_EXIT, MOTION_TRANSFORM,
    EMPHASIS_SCALE, EMPHASIS_COLOR, EMPHASIS_INDICATE_TIME,
    LAYER_PROOF_TEXT,
)
```

---

## 2. Layout cursor dọc (không drift)

Nguyên tắc: **một `left_x` cố định** cho mọi bước; dùng `.next_to(prev, DOWN, aligned_edge=LEFT)` thay vì hardcode `shift`.

```python
# ── Tiêu đề scene ──
title = Tex(r"\textbf{Giải phương trình:}", tex_template=viet_tex_template, font_size=40)
title.to_corner(UL, buff=0.5)
self.play(Write(title), run_time=MOTION_ENTER)

# ── Phương trình gốc ──
eq0 = MathTex(r"2x + 3 = 7").scale(1.1)
eq0.next_to(title, DOWN, buff=0.55, aligned_edge=LEFT)
self.play(FadeIn(eq0), run_time=MOTION_ENTER)

# ── Bước 1 ──
arr1 = MathTex(r"\Rightarrow").next_to(eq0, DOWN, aligned_edge=LEFT, buff=0.35)
eq1  = MathTex(r"2x = 7 - 3 = 4").next_to(arr1, RIGHT, buff=0.25)
self.play(Write(arr1), run_time=MOTION_ENTER)
self.play(FadeIn(eq1), run_time=MOTION_ENTER)

# ── Bước 2 ──
arr2 = MathTex(r"\Rightarrow").next_to(eq1, DOWN, aligned_edge=LEFT, buff=0.35)
eq2  = MathTex(r"x = 2").next_to(arr2, RIGHT, buff=0.25)
self.play(Write(arr2), run_time=MOTION_ENTER)
self.play(FadeIn(eq2), run_time=MOTION_ENTER)
```

**Quy tắc căn chỉnh:**
- Mỗi `MathTex` bước mới dùng `.next_to(prev_eq, DOWN, aligned_edge=LEFT, buff=0.35)`
- `arr` (⟹) dùng `.next_to(prev_eq, DOWN, aligned_edge=LEFT)` rồi bước mới `.next_to(arr, RIGHT)`
- **Không dùng** `.shift(DOWN * n)` vì sẽ drift khi các bước có chiều cao khác nhau

---

## 3. TransformMatchingTex — hai vế có ký hiệu chung

Dùng khi hai biểu thức **chia sẻ ký tự/cụm chung** (Manim tự match và animate phần giống nhau):

```python
eq_a = MathTex(r"2x", r"+", r"3", r"=", r"7")
eq_b = MathTex(r"2x",         r"=", r"4")

# Animation: "2x" và "=" tự trượt đến đúng vị trí; "3", "7" → biến mất; "4" → xuất hiện
self.play(TransformMatchingTex(eq_a, eq_b), run_time=MOTION_TRANSFORM)
```

**Khi nào KHÔNG dùng `TransformMatchingTex`:**
- Hai biểu thức quá khác nhau (không có ký tự chung) → dùng `ReplacementTransform`
- Muốn bước mới xuất hiện độc lập bên dưới (không thay thế dòng cũ) → dùng `FadeIn` bình thường

---

## 4. ReplacementTransform — cấu trúc khác hoàn toàn

```python
eq_old = MathTex(r"(x-2)(x-3) = 0")
eq_new = MathTex(r"x = 2 \quad \text{hoặc} \quad x = 3", tex_template=viet_tex_template)
eq_new.next_to(eq_old, DOWN, aligned_edge=LEFT, buff=0.35)

self.play(ReplacementTransform(eq_old.copy(), eq_new), run_time=MOTION_TRANSFORM)
# Giữ eq_old lại (không xóa) hoặc FadeOut sau khi eq_new đã xuất hiện
```

---

## 5. VGroup arrange — nhiều bước biết trước

Khi toàn bộ các bước đã biết trước (không cần transform từng bước), dùng `VGroup.arrange`:

```python
proof_steps = VGroup(
    MathTex(r"x^2 - 5x + 6 = 0"),
    MathTex(r"(x-2)(x-3) = 0"),
    MathTex(r"x = 2 \quad \text{hoặc} \quad x = 3", tex_template=viet_tex_template),
).arrange(DOWN, aligned_edge=LEFT, buff=0.35)
proof_steps.next_to(title, DOWN, buff=0.55, aligned_edge=LEFT)

for step in proof_steps:
    self.play(FadeIn(step), run_time=MOTION_ENTER)
    self.wait(0.25)
```

---

## 6. Arrow chain ⟹ với Brace gộp

```python
# Arrow + biểu thức kết quả đặt bên phải
arrow = MathTex(r"\Rightarrow")
arrow.next_to(prev_eq, DOWN, aligned_edge=LEFT, buff=0.35)
new_eq = MathTex(r"\text{kết quả}", tex_template=viet_tex_template)
new_eq.next_to(arrow, RIGHT, buff=0.3)

self.play(Write(arrow), run_time=MOTION_ENTER)
self.play(FadeIn(new_eq), run_time=MOTION_ENTER)

# Brace gộp nhiều dòng
group_to_brace = VGroup(eq1, eq2, eq3)
brace = Brace(group_to_brace, direction=RIGHT, color=COLOR_DEFAULT)
brace_label = MathTex(r"\Rightarrow \text{kết luận}", tex_template=viet_tex_template)
brace_label.next_to(brace, RIGHT, buff=0.2)
self.play(Create(brace), Write(brace_label), run_time=MOTION_ENTER)
```

---

## 7. Đóng khung kết quả

```python
# Kết quả TRUNG GIAN — viền COLOR_RESULT_KEY (xanh lá)
box_mid = SurroundingRectangle(result_mid_mob, color=COLOR_RESULT_KEY, buff=0.18)
self.play(Create(box_mid), run_time=MOTION_ENTER)

# Kết quả CUỐI — viền COLOR_RESULT_FINAL (đỏ) + move to corner
result_final = VGroup(arr_final, eq_final)
box_final = SurroundingRectangle(result_final, color=COLOR_RESULT_FINAL, buff=0.22)
self.play(Create(box_final), run_time=MOTION_ENTER)
self.play(
    VGroup(result_final, box_final).animate.to_corner(UR, buff=0.45),
    run_time=MOTION_ENTER,
)
```

---

## 8. Highlight token trong MathTex

```python
# Highlight một phần (token index)
eq = MathTex(r"x^2", r"-", r"5x", r"+", r"6", r"=", r"0")
# Index:    0      1     2      3     4     5     6

self.play(
    Indicate(eq[2], color=EMPHASIS_COLOR, scale_factor=EMPHASIS_SCALE),
    run_time=EMPHASIS_INDICATE_TIME,
)  # Nhấn mạnh "-5x"

# Đổi màu một phần
self.play(eq[0].animate.set_color(COLOR_ACTIVE))  # x² → màu active
```

---

## 9. Pattern scene hoàn chỉnh

```python
def scene_giai_pt(self):
    # 1. Tiêu đề
    title = Tex(r"\textbf{Giải phương trình:}", tex_template=viet_tex_template, font_size=38)
    title.to_corner(UL, buff=0.5)
    self.play(Write(title), run_time=MOTION_ENTER)

    # 2. Phương trình gốc
    eq0 = MathTex(r"x^2 - 5x + 6 = 0").scale(1.1).set_z_index(LAYER_PROOF_TEXT)
    eq0.next_to(title, DOWN, buff=0.55, aligned_edge=LEFT)
    self.play(FadeIn(eq0), run_time=MOTION_ENTER)

    # 3. Các bước biến đổi
    arr1 = MathTex(r"\Rightarrow").next_to(eq0, DOWN, aligned_edge=LEFT, buff=0.35)
    eq1  = MathTex(r"(x-2)(x-3) = 0").next_to(arr1, RIGHT, buff=0.25).set_z_index(LAYER_PROOF_TEXT)
    self.play(Write(arr1), FadeIn(eq1), run_time=MOTION_ENTER)

    arr2 = MathTex(r"\Rightarrow").next_to(eq1, DOWN, aligned_edge=LEFT, buff=0.35)
    eq2  = MathTex(
        r"x = 2 \quad \text{hoặc} \quad x = 3", tex_template=viet_tex_template
    ).next_to(arr2, RIGHT, buff=0.25).set_z_index(LAYER_PROOF_TEXT)
    self.play(Write(arr2), FadeIn(eq2), run_time=MOTION_ENTER)

    # 4. Đóng khung kết quả cuối
    box = SurroundingRectangle(eq2, color=COLOR_RESULT_FINAL, buff=0.2)
    self.play(Create(box), run_time=MOTION_ENTER)
    self.wait(1.0)

    # 5. Cleanup
    self.play(FadeOut(VGroup(title, eq0, arr1, eq1, arr2, eq2, box)), run_time=MOTION_EXIT)
```

---

## Checklist

- [ ] `from manim_helpers import COLOR_RESULT_KEY, COLOR_RESULT_FINAL, MOTION_*` — không hardcode màu/timing
- [ ] Mọi bước dùng `.next_to(prev, DOWN, aligned_edge=LEFT)` — không `.shift(DOWN*n)`
- [ ] `TransformMatchingTex` chỉ khi hai vế có ký tự chung
- [ ] Kết quả trung gian đóng khung `COLOR_RESULT_KEY`; kết quả cuối `COLOR_RESULT_FINAL`
- [ ] `arr = MathTex(r"\Rightarrow")` căn trái; `eq` `.next_to(arr, RIGHT)`
- [ ] Không import hay gọi `GeometryEngine`, `NumberLine`, `Axes` — đó là skill khác
