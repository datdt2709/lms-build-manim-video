---
name: manim-layout-system
description: Quản lý layout màn hình và cột chứng minh ProofColumn tránh cursor drift. Dùng khi proof có nhiều dòng MathTex liên tiếp cần căn chỉnh vị trí chuẩn.
---

# Skill: Manim – Layout System & ProofColumn

## Khi nào dùng skill này?

Dùng khi cần:
- Quản lý cột chứng minh nhiều dòng (tránh cursor drift / thụt lề drift)
- Tổ chức layout màn hình chuẩn cho proof video
- Tránh lỗi `mob.get_bottom()` trả về center-x gây `left_x` sai

> Skill này bổ sung cho `manim-hinh-phang` (geometry) và `manim-scene-lifecycle` (cleanup). Phần voiceover bookmark → xem `manim-proof-sync`.

---

## 1. Lỗi cursor drift — vấn đề gốc rễ

### Triệu chứng

```python
# Mỗi dòng thụt lề dần sang phải → sai lệch tích lũy
cursor = pf_01.get_bottom()          # ❌ trả về center-x của dòng
cursor = note1.get_bottom()          # ❌ center-x khác với title.get_left()[0]
```

### Nguyên nhân

`mob.get_bottom()` trả về `np.array([center_x, bottom_y, 0])`. Nếu dùng trực tiếp làm cursor mới, `left_x` sẽ drift theo center của từng dòng — mỗi dòng lại bắt đầu ở vị trí x khác nhau.

### Giải pháp thủ công (nếu không dùng ProofColumn)

```python
left_x = title.get_left()[0]   # lấy 1 lần duy nhất, cố định cho cả scene
cursor = np.array([left_x, title.get_bottom()[1] - 0.4, 0])

# Sau mỗi ProofLine:
cursor = np.array([left_x, pf_01.get_bottom()[1] - 0.05, 0])

# Sau mỗi note Tex:
cursor = np.array([left_x, note1.get_bottom()[1] - 0.25, 0])
```

---

## 2. `ProofColumn` — quản lý cursor tự động

### Import

```python
from manim_helpers import ProofColumn
```

### Khởi tạo

```python
col = ProofColumn(
    scene=self,
    anchor_mob=title,     # lấy left_x và initial cursor từ title
    initial_gap=0.4,      # khoảng cách từ bottom(title) xuống dòng đầu tiên
    line_gap=0.05,        # khoảng giữa các ProofLine
    note_gap=0.25,        # khoảng sau mỗi Tex note
)
```

Sau khi khởi tạo:
- `col.left_x` = `title.get_left()[0]` — cố định suốt scene
- `col.cursor` = `[left_x, title.get_bottom()[1] - 0.4, 0]`
- `col.proof` = `VGroup()` rỗng

### API chính

```text
Method                  Mô tả
──────────────────────  ─────────────────────────────────────────────────────────
col.place_line(pf_mob)  place_below(cursor), scene.add, proof.add, update cursor
col.place_note(tex_mob) next_to(cursor, DOWN, LEFT), proof.add, update cursor
col.skip_gap(gap)       Dịch cursor xuống gap mà không add mobject
col.at_limit()          True nếu cursor y < -3.2 (gần mép dưới)
col.cursor              Property — cursor hiện tại [left_x, y, 0]
col.proof               VGroup tất cả dòng đã add — dùng FadeOut(col.proof)
```

---

## 3. Code pattern hoàn chỉnh với ProofColumn

```python
def scene07_chungMinhCauC(self):
    title = Tex(r"\textbf{CM ý c) – $\widehat{NEH} = \widehat{NME}$}",
                tex_template=viet_tex_template, font_size=32).to_corner(UL, buff=0.5)
    self.play(Write(title))

    goal = Tex(r"CM: $\widehat{NEH} = \widehat{NME}$",
               tex_template=viet_tex_template, font_size=28)
    goal.next_to(title, DOWN, aligned_edge=LEFT, buff=0.3)
    self.play(Write(goal))

    # Khởi tạo ProofColumn dưới goal
    col = ProofColumn(self, anchor_mob=goal, initial_gap=0.4)

    # --- Bước 1 ---
    pf_01 = ProofLine(
        ("ang_NEH", r"\widehat{NEH}"),
        ("eq",      "="),
        ("ang_NHE", r"\widehat{NHE}"),
        tex_template=viet_tex_template, font_size=26,
    )
    col.place_line(pf_01)   # place, scene.add, proof.add, cursor update

    with self.voiceover(text=(
        "<bookmark mark='ang_NEH_expr'/> Góc N E H "
        "<bookmark mark='eq_expr'/> bằng "
        "<bookmark mark='ang_NHE_expr'/> góc N H E."
    )) as ov:
        sync_angle(self, "ang_NEH_expr",
                   pf_01.write("ang_NEH"), self.geo.highlight_angle("NEH"))
        sync_relation(self, "eq_expr", pf_01.write("eq"))
        sync_angle(self, "ang_NHE_expr",
                   pf_01.write("ang_NHE"), self.geo.highlight_angle("NHE"))

    note1 = Tex(r"(góc nội tiếp cùng chắn cung $NE$)",
                tex_template=viet_tex_template, font_size=24)
    col.place_note(note1)       # position + proof.add + cursor update
    self.play(Write(note1))     # caller animate

    # --- Bước 2 (KHÔNG FadeOut giữa chừng) ---
    pf_02 = ProofLine(
        ("ang_NHE", r"\widehat{NHE}"),
        ("eq",      "="),
        ("ang_NME", r"\widehat{NME}"),
        tex_template=viet_tex_template, font_size=26,
    )
    col.place_line(pf_02)

    with self.voiceover(text="...") as ov:
        ...

    note2 = Tex(r"(góc nội tiếp cùng chắn cung $NE$)",
                tex_template=viet_tex_template, font_size=24)
    col.place_note(note2)
    self.play(Write(note2))

    # --- Kết luận ---
    if col.at_limit():
        # Tách scene nếu hết chỗ
        raise RuntimeError("Proof column overflow — tách thành 2 scene")

    pf_result = ProofLine(
        ("imp",     r"\Rightarrow"),
        ("ang_NEH", r"\widehat{NEH}"),
        ("eq",      "="),
        ("ang_NME", r"\widehat{NME}"),
        tex_template=viet_tex_template, font_size=26,
    )
    col.place_line(pf_result)
    box_c = SurroundingRectangle(pf_result, color=COLOR_RESULT_FINAL, buff=0.15)
    with self.voiceover(text="Vậy góc N E H bằng góc N M E.") as ov:
        self.play(pf_result.write_all(), Create(box_c), run_time=ov.duration * 0.8)

    # result_group không nằm trong col.proof → không bị FadeOut
    self.result_c = VGroup(pf_result, box_c)
    # Xóa pf_result khỏi col.proof vì đã chuyển vào result_c
    col.proof.remove(pf_result)
    self.play(self.result_c.animate.to_corner(UR, buff=0.5))

    # FadeOut proof column (không bao gồm result_c)
    self.play(FadeOut(col.proof), FadeOut(title), FadeOut(goal))
```

---

## 4. Layout màn hình chuẩn

```text
┌──────────────────────────────────────────────────────────────┐
│ [UL] title / GT-KL / proof column          [UR] result_group │
│                                                              │
│                              [RIGHT] diagram                 │
│                              scale 0.8                       │
│                              shift RIGHT*4, DOWN*1           │
└──────────────────────────────────────────────────────────────┘
```

### Vị trí cố định

| Vùng                 | Nội dung                         | Cách định vị                              |
|----------------------|----------------------------------|-------------------------------------------|
| Góc trên-trái (UL)   | Tiêu đề scene, GT/KL, proof column| `.to_corner(UL, buff=0.5)`                |
| Góc trên-phải (UR)   | Kết quả trung gian đóng khung    | `.to_corner(UR, buff=0.5)`                |
| Nửa phải màn hình    | Hình vẽ hình học                 | `.scale(0.8).shift(RIGHT * 4, DOWN * 1)`  |

### Vùng an toàn cho proof column

```python
# Proof column bắt đầu từ UL, chiều rộng khoảng 6–6.5 units
# Không vượt quá RIGHT * 3.0 (tránh đè lên diagram)
# Không vượt quá DOWN * 3.2 (mép dưới; col.at_limit() kiểm tra điều này)
```

---

## 5. Không dùng DiagramArea hay ResultArea

> Theo đánh giá ROI: `DiagramArea` và `ResultArea` quá phức tạp, ít lợi ích thực tế so với layout thủ công đơn giản:
> - `self.diagram = diagram_elements.scale(0.8).shift(RIGHT * 4.0, DOWN * 1.0)` — đủ và rõ ràng
> - `result_group.to_corner(UR, buff=0.5)` — đủ cho kết quả trung gian
>
> Chỉ cần `ProofColumn` để giải quyết cursor drift.

---

## 6. Checklist layout

- [ ] `ProofColumn` được khởi tạo từ `anchor_mob` có `left_x` rõ ràng (thường là `title`)
- [ ] Dùng `col.place_line(pf_mob)` thay vì `pf_mob.place_below(cursor)` thủ công
- [ ] Dùng `col.place_note(note)` thay vì `note.next_to(cursor, ...)` thủ công + tracker riêng
- [ ] `col.cursor` luôn là `[left_x, y, 0]` — không bao giờ có `center_x` của dòng trước
- [ ] Kiểm tra `col.at_limit()` trước khi add kết luận — nếu True thì tách scene
- [ ] Diagram luôn `scale(0.8).shift(RIGHT * 4.0, DOWN * 1.0)` — không thay đổi layout
- [ ] `col.proof` bao gồm mọi dòng chứng minh — FadeOut bằng `FadeOut(col.proof)`
- [ ] `result_group` không nằm trong `col.proof` — quản lý riêng, `to_corner(UR)`
