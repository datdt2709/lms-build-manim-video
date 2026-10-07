# Scene Spec Lý Thuyết: HẰNG ĐẲNG THỨC ĐÁNG NHỚ

## Thông tin chung

- **lesson_title**: HẰNG ĐẲNG THỨC ĐÁNG NHỚ
- **lesson_type**: theory
- **subject**: algebra
- **total_scenes**: 6
- **estimated_duration**: 6–8 phút

> **Ghi chú nguồn:** Ảnh SGK chỉ chứa text và công thức LaTeX — không có hình vẽ hình học hay đồ thị.
> Theo quy tắc: `figure.type: none` cho **toàn bộ** scene.

---

## Scene 00 — Intro

- **method**: `scene00_intro`
- **duration**: 25s
- **content**: Tiêu đề bài + heading phần
- **animations**:
  - `Write(lesson_title)` — "HẰNG ĐẲNG THỨC ĐÁNG NHỚ", font_size 36, `to_edge(UP)`
  - `FadeIn(section_heading)` — "I. LÝ THUYẾT", font_size 28, dưới tiêu đề
- **cleanup**: `FadeOut(section_heading)` | giữ `lesson_title` to_edge(UP, buff=0.2) cho các scene sau

---

## Scene 01 — Định nghĩa hằng đẳng thức

- **method**: `scene01_dinhNghia`
- **block_type**: `dinh_nghia`
- **duration**: 50–65s
- **heading**: "1. Hằng đẳng thức"

- **body_lines**:
  - `"Nếu hai biểu thức P và Q nhận giá trị như nhau"`
  - `"với mọi giá trị của biến, thì"`
  - `r"P = Q \text{ là một \textbf{đồng nhất thức} hay một \textbf{hằng đẳng thức}}"`
  - `"Ví dụ: Đẳng thức"`

- **formulas**:
  - `formula_ex`: `r"3(x + y) = 3x + 3y"`
  - `formula_label`: `r"\text{là một hằng đẳng thức.}"`

- **terms_bold**: [đồng nhất thức, hằng đẳng thức]

- **figure**:
  - type: `none`
  - panel: `none`

- **layout**:
  - mode: `text_full_width`
  - wrap_width_cm: `14`
  - font_size: `28`
  - formula_method: `place_formula_left`
  - body_gap: `0.16`
  - formula_gap: `0.25`
  - formula_indent: `0.8`
  - line_grouping:
    - group: [body_lines[0], body_lines[1]]          # "Nếu hai biểu thức... với mọi giá trị..." — 2 câu liên tiếp
    - group: [body_lines[2]]                          # câu định nghĩa in đậm
    - group: [body_lines[3], formula_ex, formula_label]  # "Ví dụ:" + công thức + "là hằng đẳng thức"

- **narration**: |
    Định nghĩa. Nếu hai biểu thức P và Q nhận giá trị như nhau
    với mọi giá trị của biến,
    thì P bằng Q được gọi là một đồng nhất thức hay một hằng đẳng thức.
    Ví dụ, ba nhân tổng x cộng y bằng ba x cộng ba y
    là một hằng đẳng thức.

- **animations**:
  - `Write(block_heading)` at start
  - `FadeIn(body_lines[0..1])` — câu dẫn
  - `FadeIn(body_lines[2])` — định nghĩa, highlight terms_bold bằng `Indicate`
  - `FadeIn(body_lines[3])` + `Write(formula_ex)` + `FadeIn(formula_label)`
  - `Indicate(terms_bold_mobs, scale_factor=1.15)` — cuối scene

- **cleanup**: `FadeOut(block_heading, body_group, formula_group)`

---

## Scene 02 — 2.1 Bình phương của một tổng

- **method**: `scene02_binhPhuongTong`
- **block_type**: `dinh_li`
- **duration**: 55–70s
- **heading**: "2.1. Bình phương của một tổng"

- **body_lines**:
  - `"Với hai biểu thức A, B tùy ý, ta có:"`

- **formulas**:
  - `formula_main`: `r"(A + B)^2 = A^2 + 2AB + B^2"`

- **figure**:
  - type: `none`
  - panel: `none`

- **layout**:
  - mode: `text_full_width`
  - wrap_width_cm: `13`
  - font_size: `28`
  - formula_method: `place_formula_left`
  - body_gap: `0.16`
  - formula_gap: `0.28`
  - formula_indent: `0.8`
  - line_grouping:
    - group: [body_lines[0], formula_main]   # câu dẫn + công thức liền mạch

- **narration**: |
    Tính chất. Bình phương của một tổng.
    Với hai biểu thức A và B bất kỳ,
    bình phương của tổng A cộng B bằng A bình phương
    cộng hai lần A nhân B, cộng B bình phương.
    Đây là một trong những hằng đẳng thức đáng nhớ quan trọng nhất.

- **animations**:
  - `Write(block_heading)` at start
  - `FadeIn(body_lines[0])`
  - `Write(formula_main)` — dùng `TransformMatchingTex` nếu cần nhấn từng hạng tử
  - `Indicate(formula_main, scale_factor=1.05)` — cuối scene

- **cleanup**: `FadeOut(block_heading, body_group, formula_main)`

---

## Scene 03 — 2.1 Bình phương của một hiệu

- **method**: `scene03_binhPhuongHieu`
- **block_type**: `dinh_li`
- **duration**: 55–70s
- **heading**: "2.1. Bình phương của một hiệu"

- **body_lines**:
  - `"Với hai biểu thức A, B tùy ý, ta có:"`

- **formulas**:
  - `formula_main`: `r"(A - B)^2 = A^2 - 2AB + B^2"`

- **figure**:
  - type: `none`
  - panel: `none`

- **layout**:
  - mode: `text_full_width`
  - wrap_width_cm: `13`
  - font_size: `28`
  - formula_method: `place_formula_left`
  - body_gap: `0.16`
  - formula_gap: `0.28`
  - formula_indent: `0.8`
  - line_grouping:
    - group: [body_lines[0], formula_main]

- **narration**: |
    Bình phương của một hiệu.
    Với hai biểu thức A và B bất kỳ,
    bình phương của hiệu A trừ B bằng A bình phương
    trừ hai lần A nhân B, cộng B bình phương.
    Lưu ý dấu âm ở hạng tử giữa là điểm khác biệt so với bình phương của tổng.

- **animations**:
  - `Write(block_heading)` at start
  - `FadeIn(body_lines[0])`
  - `Write(formula_main)`
  - `Indicate(formula_main, scale_factor=1.05)` — cuối scene

- **cleanup**: `FadeOut(block_heading, body_group, formula_main)`

---

## Scene 04 — Ví dụ bình phương tổng và hiệu

- **method**: `scene04_viDu21`
- **block_type**: `vi_du`
- **duration**: 55–70s
- **heading**: "Ví dụ"

- **body_lines**:
  - `r"\bullet\ (x + 2)^2 = x^2 + 2 \cdot x \cdot 2 + 2^2 = x^2 + 4x + 4"`
  - `r"\bullet\ (x - 2)^2 = x^2 - 2 \cdot x \cdot 2 + 2^2 = x^2 - 4x + 4"`

- **figure**:
  - type: `none`
  - panel: `none`

- **layout**:
  - mode: `text_full_width`
  - wrap_width_cm: `14`
  - font_size: `27`
  - formula_method: `place_formula_left`
  - body_gap: `0.20`
  - formula_gap: `0.20`
  - formula_indent: `0.5`
  - line_grouping:
    - group: [body_lines[0]]   # ví dụ 1 — công thức dài, giữ nguyên 1 dòng
    - group: [body_lines[1]]   # ví dụ 2

- **narration**: |
    Ví dụ. Áp dụng hằng đẳng thức bình phương của một tổng:
    x cộng hai, tất cả bình phương,
    bằng x bình phương cộng bốn x cộng bốn.
    Áp dụng hằng đẳng thức bình phương của một hiệu:
    x trừ hai, tất cả bình phương,
    bằng x bình phương trừ bốn x cộng bốn.

- **animations**:
  - `Write(block_heading)` at start
  - `Write(body_lines[0])` — ví dụ 1, nhịp chậm theo từng đẳng thức
  - `Write(body_lines[1])` — ví dụ 2
  - `Indicate(body_lines[0], color=COLOR_EQUAL_1)` → `Indicate(body_lines[1], color=COLOR_EQUAL_2)`

- **cleanup**: `FadeOut(block_heading, body_group)`

---

## Scene 05 — 2.2 Hiệu hai bình phương

- **method**: `scene05_hieuHaiBinhPhuong`
- **block_type**: `dinh_li`
- **duration**: 50–65s
- **heading**: "2.2. Hiệu hai bình phương"

- **body_lines**:
  - `"Với hai biểu thức A, B tùy ý, ta có:"`

- **formulas**:
  - `formula_main`: `r"A^2 - B^2 = (A - B)(A + B)"`

- **figure**:
  - type: `none`
  - panel: `none`

- **layout**:
  - mode: `text_full_width`
  - wrap_width_cm: `13`
  - font_size: `28`
  - formula_method: `place_formula_left`
  - body_gap: `0.16`
  - formula_gap: `0.28`
  - formula_indent: `0.8`
  - line_grouping:
    - group: [body_lines[0], formula_main]

- **narration**: |
    Tính chất. Hiệu hai bình phương.
    Với hai biểu thức A và B bất kỳ,
    A bình phương trừ B bình phương
    bằng tích của A trừ B và A cộng B.
    Đây là hằng đẳng thức giúp phân tích nhân tử rất hiệu quả.

- **animations**:
  - `Write(block_heading)` at start
  - `FadeIn(body_lines[0])`
  - `Write(formula_main)` — có thể dùng `TransformMatchingTex` nhấn `A^2 - B^2` → `(A-B)(A+B)`
  - `Indicate(formula_main, scale_factor=1.05)` — cuối scene

- **cleanup**: `FadeOut(all)`

---

## Ghi chú dựng hình

- **Không có hình vẽ** trong toàn bộ spec — ảnh SGK chỉ có text và công thức.
- Tất cả scene dùng `TheoryColumn(has_figure=False)` và `tex_wrapped` — **không** `place_formula()`.
- Công thức dài (ví dụ Scene 04) cần `font_size: 27` và `wrap_width_cm: 14` để tránh tràn màn hình.
- `formula_method: place_formula_left` áp dụng thống nhất cho mọi scene.
- Màu nhấn mạnh: `COLOR_EQUAL_1` (#E53935) cho ví dụ tổng, `COLOR_EQUAL_2` (#1565C0) cho ví dụ hiệu.
- Scene 02 và 03 nên có `TransformMatchingTex` để highlight từng hạng tử `A²`, `2AB`, `B²` khi phát sinh.
