---
name: manim-theory-layout
description: Quản lý layout màn hình cho video lý thuyết toán: TheoryColumn (xếp text/công thức tuần tự không drift), FigurePanel (vùng hình phải), DualFigurePanel (2 hình cạnh nhau). Dùng trong mọi scene lý thuyết thay thế ProofColumn.
---

# Skill: Manim – Theory Layout

> Dùng thay `ProofColumn` trong file lý thuyết. Không có token proof, không bookmark.

## Import

```python
from manim_helpers.theory_helpers import TheoryColumn
```

Nếu `theory_helpers.py` chưa tồn tại → xem mục 4 để tạo file.

---

## 1. Hằng số vùng màn hình

```python
# Vùng text (trái)
TEXT_LEFT_X   = -6.5   # left edge — khớp with lesson_title.get_left()[0]
TEXT_RIGHT_WITH_FIG = 0.3    # right boundary khi có hình phải
TEXT_RIGHT_NO_FIG   = 5.8    # right boundary khi không có hình

# Vùng hình (phải)
FIG_CENTER_X  =  4.1   # center x của figure panel
FIG_CENTER_Y  = -0.3   # center y của figure panel
FIG_MAX_W     =  3.5   # max width hình đơn
FIG_MAX_H     =  4.6   # max height hình đơn

# Dual figure panel
DUAL_FIG_MAX_W  = 1.55  # max width mỗi hình trong dual
DUAL_FIG_BUFF   = 0.35  # khoảng cách giữa 2 hình
```

---

## 2. `TheoryColumn` — xếp text tuần tự không drift

### API

| Method | Mô tả |
|--------|-------|
| `col.place(mob, gap=0.20)` | Đặt mob tại cursor hiện tại, căn trái `left_x`, cập nhật cursor |
| `col.place_formula(mob, gap=0.35)` | Đặt formula căn giữa cột text, gap lớn hơn |
| `col.place_formula_left(mob, indent=0.6, gap=0.30)` | Đặt formula ngắn căn trái với indent — tránh công thức trôi ra giữa cột |
| `col.place_bullet(mob, indent=0.35, gap=0.18)` | Đặt bullet point thụt lề `indent` |
| `col.skip(gap)` | Dịch cursor xuống `gap` không add mob |
| `col.at_limit()` | `True` nếu cursor xuống quá `y < -3.4` |
| `col.all` | `VGroup` toàn bộ items đã add |

### Bảng quyết định method

| Tình huống | Dùng method |
|---|---|
| Câu văn, đoạn text | `place()` |
| Công thức display chiếm toàn cột | `place_formula()` |
| Công thức ngắn / inline / hệ thức trung gian | `place_formula_left()` |
| Bullet point | `place_bullet()` |

### Bảng gap chuẩn (cấm override < mức tối thiểu)

| Loại content | gap default | Tối thiểu |
|---|---|---|
| body text | 0.20 | 0.18 |
| formula inline | 0.30 | 0.25 |
| formula display | 0.40 | 0.30 |
| sau heading | 0.35 | 0.35 |

### Khởi tạo

`TheoryColumn(block_heading, ...)` — `block_heading` phải nằm dưới **heading anchor** đúng trước khi khởi tạo cột:

```
┌──────────────────────────────────────────────┐
│  lesson_title  (row 0, persistent)           │
├──────────────────────────────────────────────┤
│  section_heading (row 1, nếu spec có)        │  ← anchor khi có section_heading
├──────────────────────────────────────────────┤
│  block_heading (row 2, đổi mỗi scene)        │  ← TheoryColumn neo cursor từ đây
│  body / formulas                             │
└──────────────────────────────────────────────┘
```

- Có `section_heading` → `block_heading.next_to(section_heading, DOWN, buff=0.25)`
- Không có → `block_heading.next_to(lesson_title, DOWN, buff=0.35)`
- Luôn thêm `block_heading.align_to([TEXT_LEFT_X, 0, 0], LEFT)` sau `next_to`

```python
# SAU KHI đã Write(block_heading) và biết có/không có hình:
col = TheoryColumn(block_heading, has_figure=True)
# col.left_x  = block_heading.get_left()[0]
# col.cursor_y = block_heading.get_bottom()[1] - 0.35
```

### Ví dụ dùng trong scene

```python
def scene01_dinhNghia(self):
    block_heading = Tex(r"\textbf{1. Định nghĩa}",
                        tex_template=viet_tex_template, font_size=32)
    block_heading.next_to(self.lesson_title, DOWN, aligned_edge=LEFT, buff=0.35)
    self.play(Write(block_heading))

    col = TheoryColumn(block_heading, has_figure=True)

    line1 = Tex(r"Tứ giác có bốn đỉnh nằm trên một đường tròn gọi là",
                tex_template=viet_tex_template, font_size=26)
    col.place(line1)

    line2 = Tex(r"\textbf{tứ giác nội tiếp} đường tròn.",
                tex_template=viet_tex_template, font_size=26)
    col.place(line2)

    with self.voiceover("Định nghĩa. Tứ giác có bốn đỉnh nằm trên một đường tròn...") as ov:
        self.play(FadeIn(line1), Create(circle), run_time=ov.duration * 0.5)
        self.play(FadeIn(line2), Create(quad_ABCD), run_time=ov.duration * 0.5)

    self.play(FadeOut(block_heading, col.all), FadeOut(figure_group))
```

---

## 3. `FigurePanel` — vùng hình đơn bên phải

Không phải class — chỉ là quy ước đặt vị trí:

```python
def place_figure(figure_group: VGroup) -> VGroup:
    """Scale và đặt hình vào FigurePanel chuẩn."""
    if figure_group.width > FIG_MAX_W:
        figure_group.scale_to_fit_width(FIG_MAX_W)
    if figure_group.height > FIG_MAX_H:
        figure_group.scale_to_fit_height(FIG_MAX_H)
    figure_group.move_to([FIG_CENTER_X, FIG_CENTER_Y, 0])
    return figure_group
```

**Dùng:**
```python
figure_group = VGroup(circle, quad_ABCD, dot_O, label_O, ...)
place_figure(figure_group)
self.play(Create(circle), run_time=1.0)
self.play(Create(quad_ABCD), run_time=1.2)
```

---

## 4. `DualFigurePanel` — 2 hình cạnh nhau

Dùng cho block `nhan_xet` có 2 hình minh họa:

```python
def place_dual_figures(fig_left: VGroup, fig_right: VGroup,
                       label_left: str = None, label_right: str = None):
    """Scale 2 hình nhỏ, xếp cạnh nhau, đặt vào FigurePanel."""
    for fig in [fig_left, fig_right]:
        if fig.width > DUAL_FIG_MAX_W:
            fig.scale_to_fit_width(DUAL_FIG_MAX_W)
        if fig.height > 3.5:
            fig.scale_to_fit_height(3.5)

    dual = VGroup(fig_left, fig_right).arrange(RIGHT, buff=DUAL_FIG_BUFF)
    dual.move_to([FIG_CENTER_X, FIG_CENTER_Y, 0])

    mobs = VGroup(dual)
    if label_left:
        lbl_l = Tex(label_left, tex_template=viet_tex_template, font_size=20)
        lbl_l.next_to(fig_left, DOWN, buff=0.15)
        mobs.add(lbl_l)
    if label_right:
        lbl_r = Tex(label_right, tex_template=viet_tex_template, font_size=20)
        lbl_r.next_to(fig_right, DOWN, buff=0.15)
        mobs.add(lbl_r)
    return mobs
```

**Dùng:**
```python
rect_group = VGroup(rect_ABCD, diag_AC, diag_BD, dot_O, circle_rect)
sq_group   = VGroup(sq_EFGH, diag_EG, diag_FH, dot_O2, circle_sq)
dual_panel = place_dual_figures(rect_group, sq_group,
                                label_left="Hình chữ nhật",
                                label_right="Hình vuông")
self.play(Create(rect_ABCD), Create(sq_EFGH))
```

---

## 5. Layout text-only (`figure.type = none`)

Khi scene **không có hình**, text chiếm gần full width. **Bắt buộc** theo checklist dưới — **không** dùng `place_formula()` (căn giữa cột → khoảng trắng hai bên, công thức lơ lửng).

### Checklist bắt buộc

- [ ] `TheoryColumn(block_heading, has_figure=False)` — `col.max_width` tự mở rộng sang phải
- [ ] Body text: `font_size=28` (không dùng 26)
- [ ] Câu dài: wrap bằng `minipage` + `\raggedright` — tránh LaTeX tự xuống dòng căn giữa
- [ ] Công thức: `place_formula_left(indent=0.8, gap=0.25)` — **KHÔNG** `place_formula()`
- [ ] Gap body: `0.15–0.18` (không dùng 0.20–0.22 trở lên cho text-only ngắn)
- [ ] Gộp câu dài liên quan — không tách từng câu SGK thành nhiều `place()` nếu ảnh gốc < 2 dòng
- [ ] Spec phải có block `layout:` (xem `1-spec/SKILL.md`) — build agent không tự đoán

### Helper `tex_wrapped`

```python
TEXT_ONLY_FONT = 28
WRAP_WIDTH_CM = 14

def tex_wrapped(text: str, width_cm: float = WRAP_WIDTH_CM,
                font_size: int = TEXT_ONLY_FONT) -> Tex:
    body = (
        rf"\begin{{minipage}}{{{width_cm}cm}}"
        rf"\raggedright {text}\end{{minipage}}"
    )
    return Tex(body, tex_template=viet_tex_template, font_size=font_size)
```

- Mọi câu dài (> ~60 ký tự hoặc hay bị LaTeX wrap) **bắt buộc** qua `tex_wrapped`
- `wrap_width_cm`: 12–14 tùy độ dài block (spec ghi rõ)

### Pattern `TheoryColumn` text-only

```python
col = TheoryColumn(block_heading, has_figure=False)

line1 = tex_wrapped(r"Câu dẫn dài có thể xuống dòng...")
col.place(line1, gap=0.16)

formula = MathTex(r"\begin{cases} ... \end{cases}",
                  tex_template=viet_tex_template, font_size=32)
col.place_formula_left(formula, indent=0.8, gap=0.25)  # ✓ thẳng hàng body

# ✗ SAI — căn giữa cột, khoảng trắng hai bên
# col.place_formula(formula, gap=0.30)
```

| Tình huống text-only | Method / giá trị |
|---|---|
| Câu văn (ngắn hoặc dài) | `tex_wrapped` + `place(gap=0.15–0.18)` |
| Hệ thức, PT display | `place_formula_left(indent=0.8, gap=0.25)` |
| Label ngắn + công thức ngay dưới | label `gap=0.15`, formula `place_formula_left` |
| Bullet | `place_bullet(indent=0.35, gap=0.16)` |

### Pattern VGroup căn giữa toàn khối *(tuỳ chọn)*

Scene text-only ngắn có thể bỏ cursor drift — gom nội dung rồi căn giữa màn hình (giống SGK in giữa trang):

```python
content = VGroup(line1, line2, formula, example_block).arrange(
    DOWN, aligned_edge=LEFT, buff=0.18
)
content.move_to(ORIGIN + DOWN * 0.2)
self.add(content)
# voiceover: FadeIn/Write từng mob trong content
self.play(FadeOut(block_heading), FadeOut(content), run_time=MOTION_EXIT)
```

Dùng pattern này khi block ≤ 6 dòng và không cần `col.at_limit()`. Scene dài vẫn dùng `TheoryColumn`.

---

## 6. Tạo `manim_helpers/theory_helpers.py`

Thêm file này vào `manim_helpers/` nếu chưa có:

```python
# manim_helpers/theory_helpers.py
import numpy as np
from manim import VGroup

TEXT_LEFT_X          = -6.5
TEXT_RIGHT_WITH_FIG  =  0.3
TEXT_RIGHT_NO_FIG    =  5.8
FIG_CENTER_X         =  4.1
FIG_CENTER_Y         = -0.3
FIG_MAX_W            =  3.5
FIG_MAX_H            =  4.6
DUAL_FIG_MAX_W       =  1.55
DUAL_FIG_BUFF        =  0.35


class TheoryColumn:
    """Quản lý cursor text cho cột lý thuyết, tránh drift."""

    def __init__(self, anchor_mob, has_figure: bool = True,
                 initial_gap: float = 0.35):
        self.left_x    = anchor_mob.get_left()[0]
        self.cursor_y  = anchor_mob.get_bottom()[1] - initial_gap
        self.has_figure = has_figure
        self.max_width = (TEXT_RIGHT_WITH_FIG - self.left_x
                          if has_figure
                          else TEXT_RIGHT_NO_FIG - self.left_x)
        self._items = VGroup()

    def place(self, mob, gap: float = 0.20):
        mob.move_to([self.left_x, self.cursor_y - mob.height / 2, 0],
                    aligned_edge=LEFT)
        self._items.add(mob)
        self.cursor_y = mob.get_bottom()[1] - gap
        return mob

    def place_formula(self, mob, gap: float = 0.35):
        col_center_x = self.left_x + self.max_width / 2
        mob.move_to([col_center_x, self.cursor_y - mob.height / 2, 0])
        self._items.add(mob)
        self.cursor_y = mob.get_bottom()[1] - gap
        return mob

    def place_formula_left(self, mob, indent: float = 0.6, gap: float = 0.30):
        mob.move_to(
            [self.left_x + indent, self.cursor_y - mob.height / 2, 0],
            aligned_edge=LEFT)
        self._items.add(mob)
        self.cursor_y = mob.get_bottom()[1] - gap
        return mob

    def place_bullet(self, mob, indent: float = 0.35, gap: float = 0.18):
        mob.move_to([self.left_x + indent, self.cursor_y - mob.height / 2, 0],
                    aligned_edge=LEFT)
        self._items.add(mob)
        self.cursor_y = mob.get_bottom()[1] - gap
        return mob

    def skip(self, gap: float = 0.25):
        self.cursor_y -= gap

    def at_limit(self) -> bool:
        return self.cursor_y < -3.4

    @property
    def all(self) -> VGroup:
        return self._items
```

Sau khi tạo file, thêm export vào `manim_helpers/__init__.py`:
```python
from .theory_helpers import TheoryColumn
```
