---
name: manim-spec-ly-thuyet
description: Tạo Scene Spec Markdown cho video Manim bài giảng lý thuyết toán (Định nghĩa, Định lí, Nhận xét...). Dùng khi nhận ảnh/text trang sách giáo khoa hoặc tài liệu lý thuyết, cần lập kế hoạch video trước khi code. Áp dụng cho mọi môn: hình học, đại số, lượng giác, xác suất.
---

# Skill: Manim Step 1 – Scene Spec cho Bài Giảng Lý Thuyết

## Mục đích

Nhận **ảnh trang sách / mô tả lý thuyết** → Tạo file `spec-ly-thuyet.md` mô tả chi tiết từng scene. Spec này là đầu vào cho `manim-build-ly-thuyet` (Step 2).

---

## Khi nào dùng skill này?

- Người dùng cung cấp ảnh trang SGK hoặc tài liệu có Định nghĩa / Định lí / Nhận xét
- Người dùng muốn lên kế hoạch video lý thuyết trước khi code
- Phân biệt với `manim-spec-hinh-hoc` (bài toán có GT/KL/CM): lý thuyết **không có** chứng minh, chỉ **trình bày và minh họa**

---

## Quy trình 5 bước

### Bước 1 – Đọc và nhận dạng cấu trúc

Từ ảnh hoặc văn bản, xác định:

1. **Tiêu đề bài** — "BÀI 3. TỨ GIÁC NỘI TIẾP", "CHƯƠNG II. HÀM SỐ BẬC HAI"
2. **Số thứ tự phần** — I. Tóm tắt lý thuyết / II. Ví dụ / III. Bài tập
3. **Danh sách block** theo thứ tự xuất hiện — mỗi tiểu mục (1, 2, 3...) là 1 block

**Bảng nhận dạng block type:**

| Dấu hiệu trên trang sách              | Block type              | Heading prefix |
|---------------------------------------|-------------------------|----------------|
| "Định nghĩa", "Khái niệm"             | `dinh_nghia`            | Số. Tên |
| "Định lí", "Định lý", "Tính chất", …  | `dinh_li`               | Số. Tên |
| "Hệ quả"                              | `he_qua`                | `Hệ quả` |
| "Nhận xét", "Ghi nhớ"                 | `nhan_xet`              | `(*) Nhận xét` / `(*) Ghi nhớ` — dùng **đúng nhãn SGK** |
| "Chú ý", "Lưu ý"                      | `chu_y`                 | `(!) Chú ý` / `(!) Lưu ý` — dùng **đúng nhãn SGK** |
| "Ví dụ N", "Bài toán N"               | `vi_du`                 | `Ví dụ N` |
| "Bài tập", "Luyện tập"                | `bai_tap`               | `Bài tập` |

> **Quy tắc match nhãn cho `nhan_xet` / `chu_y`**: heading = prefix `(*)` hoặc `(!)` + **nhãn gốc từ ảnh SGK**. Không gộp (`"(*) Nhận xét / Ghi nhớ"` là sai). Body dùng italic + `color=COLOR_WARNING`.

4. **Môn học / chủ đề** — geometry / algebra / trigonometry / statistics / combinatorics
5. **Figure type của từng block:**

| Nội dung block | Figure type | Dùng skill |
|---|---|---|
| Hình phẳng (tam giác, đường tròn, tứ giác…) — bao gồm cả 2 hình liên quan (arrange RIGHT) | `geometry` | `theory-figure/geometry` |
| Hình không gian (hộp, hình cầu…) | `geometry_3d` | `primitives/hinh-3d` |
| Đồ thị hàm số, trục tọa độ 2D (y=ax+b, parabol…) | `function` | `theory-figure/algebra` → `algebra/coordinate-plane` |
| Trục số 1D (bất phương trình, tập nghiệm) | `number_line` | `theory-figure/algebra` → `algebra/number-line` |
| Thanh/hình tròn phân số, quy đồng, rút gọn | `fraction` | `theory-figure/algebra` → `algebra/fraction-visual` |
| Hằng đẳng thức ô diện tích (a+b)², (a-b)², (a+b)(a-b) | `identity` | `theory-figure/algebra` → `algebra/identity-figure` |
| Bảng giá trị, bảng biến thiên | `table` | — |
| Hai hình ví dụ ĐỘC LẬP (VD: HCN và HV) — **CHỈ cho `nhan_xet`/`chu_y`** | `dual_geometry` | `theory-figure/geometry` Section 4 |
| Không có hình | `none` | — |

> **Phân biệt `geometry` vs `dual_geometry`:**
> - `geometry`: 1 hình đơn **hoặc** 2 hình liên quan cùng minh họa một khái niệm (dùng `place_figure(VGroup(fig1, fig2).arrange(RIGHT, buff=0.3))`).
> - `dual_geometry`: 2 hình **ĐỘC LẬP** cho 2 ví dụ khác nhau — **CHỈ** hợp lệ cho `nhan_xet` và `chu_y`.

> **Lưu ý:** `function`, `number_line`, `fraction`, `identity` đều có skill riêng qua `theory-figure/algebra` (C1). `table` dùng `Table` Manim built-in. `geometry_3d` dùng `primitives/hinh-3d`.

### Quy tắc chọn `figure.type` từ ảnh SGK

**Mặc định:** nếu ảnh trang sách **không có hình vẽ** → `figure.type: none` cho mọi scene.

| Dấu hiệu trên ảnh SGK | Quyết định |
|---|---|
| Không có hình vẽ, chỉ text/công thức | `figure.type: none` — **mặc định** |
| Có tam giác, đường tròn, hình vẽ SGK | `geometry` / `dual_geometry` |
| Có trục tọa độ + đồ thị parabol/đường thẳng **in sẵn** | `function` |
| Có trục số 1D, tô vùng nghiệm | `number_line` |
| Có thanh/hình tròn phân số, ô diện tích hằng đẳng thức | `fraction` / `identity` |
| User prompt: "minh họa bằng đồ thị" (hoặc tương đương) | Mới được thêm `function` dù ảnh không có |

**Cấm suy diễn:**
- **Không** gán `function` chỉ vì block có phương trình bậc hai, parabol, hay hàm số trong text.
- **Không** tự thêm parabol/trục tọa độ để "minh họa thêm" khi ảnh SGK chỉ có công thức.
- Mỗi `figure.type ≠ none` phải trích dẫn **dấu hiệu trên ảnh** (hoặc yêu cầu rõ của user) trong spec.

---

### Bước 2 – Chia scene

**Nguyên tắc chia scene lý thuyết:**

| Tình huống                                              | Quyết định                          |
|---------------------------------------------------------|-------------------------------------|
| 1 block vừa phải (≤ 8 dòng + 1 công thức + 1 hình)      | → **1 scene**                       |
| Block `dinh_nghia` dài (> 8 dòng)                       | → **2 scene**: text + figure        |
| Block `vi_du` có nhiều bước tính                        | → **2 scene**: đề + giải            |
| Block `nhan_xet` với 2 hình cạnh nhau                   | → **1 scene** với `dual_geometry`   |
| Nhiều `chu_y` ngắn liên tiếp                            | → **gộp vào 1 scene**               |

**Bảng chia scene mẫu (bài 3–5 mục):**

| Scene    | Nội dung                              | Thời lượng |
|----------|---------------------------------------|------------|
| Scene 00 | Intro: tiêu đề bài + heading phần     | 20–30s     |
| Scene 01 | Block 1 (thường là `dinh_nghia`)      | 45–75s     |
| Scene 02 | Block 2 (thường là `dinh_li`)         | 45–75s     |
| Scene 03 | Block 3 (thường `nhan_xet` / `he_qua`)| 30–60s     |
| Scene 04 | Ví dụ / Tổng kết                      | 45–60s     |

**Tiêu chí scene tốt:**
- Mỗi scene có 1 mục tiêu: "trình bày định nghĩa", "phát biểu và minh họa định lí"
- Không quá 75 giây narration
- Kết thúc scene = người xem đã hiểu nội dung — hình chỉ khi ảnh SGK có hoặc user yêu cầu

---

### Bước 3 – Phân tích hình cho từng scene

**Với figure_type = `geometry`:**
- Liệt kê thứ tự dựng: `circle` → `points` → `edges` → `labels` → `angles`
- Ghi rõ: điểm nào trên đường tròn, điểm nào là giao điểm tính toán
- Mỗi yếu tố hình học = 1 dòng trong `figure_build`

**Với figure_type = `function`:**
- Liệt kê: `axes(x_range, y_range)` → `curve(expr, color)` → `special_points` → `labels`

**Với figure_type = `number_line`:**
- Liệt kê: `number_line(x_range)` → `inequality(boundary, closed, direction)` → `shade_region`

**Với figure_type = `fraction`:**
- Liệt kê: `FractionBar(n, d)` hoặc `FractionPie(n, d)` → animation nếu có (quy đồng/rút gọn)

**Với figure_type = `identity`:**
- Ghi tên hằng đẳng thức: `(a+b)²`, `(a-b)²`, hoặc `(a+b)(a-b)` + giá trị `a_val`, `b_val`

**Với figure_type = `dual_geometry`** (CHỈ cho `nhan_xet`/`chu_y` — 2 hình ĐỘC LẬP):
- `figure_left`: tên + build sequence
- `figure_right`: tên + build sequence
- Hai hình scale nhỏ hơn so với hình đơn
- Nếu 2 hình liên quan nhau → dùng `geometry` + arrange RIGHT, KHÔNG dùng `dual_geometry`

**Với figure_type = `none`:**
- Text chiếm full width; ghi `figure: none` và `panel: none`
- **Bắt buộc** thêm block `layout:` — Step 2 build không tự đoán wrap/gap/align

```yaml
layout:
  mode: text_full_width
  wrap_width_cm: 14          # 12–14 tùy độ dài block
  font_size: 28
  formula_method: place_formula_left   # KHÔNG place_formula
  body_gap: 0.16               # 0.15–0.18
  formula_gap: 0.25
  formula_indent: 0.8
  line_grouping:               # gộp câu — tránh 1 câu SGK = 1 dòng riêng nếu ảnh gốc gọn
    - group: [line1, line2]     # ví dụ: 2 câu dẫn liên tiếp → có thể giữ 2 mob hoặc 1 tex_wrapped
    - group: [example_label, formula_example]  # label + công thức sát nhau, gap 0.15
    - group: [line_c2, formula_find]           # câu dẫn + PT liền mạch
```

**Quy tắc `line_grouping`:**
- Câu dài hay bị LaTeX wrap (≥ ~60 ký tự) → **một** `body_lines` entry + ghi `wrap: true`
- Hai câu ngắn liên tiếp trên cùng đoạn SGK → gộp `group` hoặc một dòng `tex_wrapped`
- Label ("Theo hệ thức...", "Ta có:") + công thức ngay dưới → cùng một `group`, `gap: 0.15` giữa label và formula

**Định dạng danh sách (Section 9 manim-theory):**
- List item trong `body_lines`: prefix `-` (dash)
- Sub-item trong `formulas` hoặc body: prefix `$\bullet$` (Tex) — **không** dùng `.` (dễ nhầm `\cdot`)
- Ví dụ spec entry: `` `formula_gh_nhan`: `r"$\bullet$ $a \cdot b = b \cdot a$"` *(sub-item, Tex)* ``

---

### Bước 4 – Viết narration tiếng Việt

**Quy tắc cho lý thuyết (khác narration bài toán):**

- Bắt đầu scene bằng tên block: "Định nghĩa.", "Định lí.", "Nhận xét."
- **Giải thích** nội dung, không "chứng minh": "Điều này có nghĩa là...", "Chúng ta thấy rằng..."
- Đọc công thức bằng lời: "góc A cộng góc C bằng 180 độ" — không dùng ký hiệu
- Thuật ngữ in đậm đọc bình thường, không nhấn giọng đặc biệt
- Câu ≤ 20 từ; thêm "chẳng hạn", "ví dụ" khi scene **có hình** — không dẫn sang hình nếu `figure.type: none`
- **Không dùng**: "ta có", "ta chứng minh", "bây giờ chứng minh"

**Ví dụ:**
```
✗ SAI: "Ta có: góc A + góc C = 180°, ta chứng minh bằng cách..."
✓ ĐÚNG: "Trong tứ giác nội tiếp, tổng hai góc đối nhau luôn bằng 180 độ.
          Ví dụ, góc A cộng góc C bằng 180 độ. Tương tự, góc B cộng góc D cũng bằng 180 độ."
```

---

### Bước 5 – Output: file `spec-ly-thuyet.md`

Tạo file tại thư mục bài học với tên `spec-ly-thuyet.md`.

---

## Template Scene Spec Lý Thuyết

```markdown
# Scene Spec Lý Thuyết: [TIÊU ĐỀ BÀI]

## Thông tin chung

- **lesson_title**: BÀI X. TÊN BÀI
- **lesson_type**: theory
- **subject**: geometry | algebra | trigonometry | statistics | combinatorics
- **section_heading**: I. TÓM TẮT LÝ THUYẾT *(optional — nếu SGK có heading phần)*
- **total_scenes**: N
- **estimated_duration**: X–Y phút

> Nếu có `section_heading`: layout 3 tầng — `block_heading` neo dưới `section_heading`, không dưới `lesson_title`.

---

## Scene 00 — Intro *(optional)*

- **method**: `scene00_intro`
- **duration**: 20–30s
- **content**: Tiêu đề bài + heading phần (I. Tóm tắt lý thuyết)
- **animations**:
  - `Write(lesson_title)` — font_size 36, to_edge(UP)
  - `FadeIn(section_heading)` — "I. TÓM TẮT LÝ THUYẾT", font_size 28
- **cleanup**: giữ `lesson_title` + `section_heading` cho scenes 01–N *(không FadeOut section_heading sau scene00)*

> **Quy tắc `section_heading` persistent:** Nếu **Thông tin chung** khai báo `section_heading` → scene00 cleanup **không** FadeOut nó; `block_heading` các scene sau neo dưới `section_heading` (`buff=0.25`); cleanup cuối bài FadeOut cả `section_heading` + `lesson_title`. Nếu spec **không** có `section_heading` → bỏ qua, `block_heading` neo trực tiếp dưới `lesson_title` như cũ.

---

## Scene 01 — [Tên mục]

- **method**: `scene01_dinhNghia`
- **block_type**: `dinh_nghia`
- **duration**: 45–75s
- **heading**: "1. Định nghĩa"

- **body_lines**:
  - `"Câu dẫn hoặc đoạn văn dòng 1..."`
  - `r"\textbf{thuật ngữ chính} tiếp theo..."`
  - `"... phần còn lại của định nghĩa."`

- **formulas**:
  - `formula_1`: `r"\widehat{A} + \widehat{C} = \widehat{B} + \widehat{D} = 180^\circ"`
  - *(bỏ qua nếu không có công thức)*

- **terms_bold**: [thuật ngữ 1, thuật ngữ 2]

- **figure**:
  - type: `geometry` | `function` | `dual_geometry` | `table` | `none`
  - panel: `right` | `none`
  - width_ratio: `0.45` *(bỏ qua nếu type = none)*
  - *(nếu type = none, bắt buộc thêm block `layout:` — xem Bước 3)*

- **layout** *(bắt buộc khi figure.type = none)*:
  - mode: `text_full_width`
  - wrap_width_cm: `14`
  - font_size: `28`
  - formula_method: `place_formula_left`
  - body_gap: `0.16`
  - line_grouping:
    - group: [body_lines liên quan]

- **figure.build** *(bỏ qua nếu type = none)*:
  - build:
    - `circle(O, R)`
    - `points A, B, C, D on circle — angles [60, 140, 210, 320] degrees`
    - `quad ABCD — edges AB, BC, CD, DA`
    - `labels A(UL), B(UR), C(DR), D(DL)`
  - *(với dual_geometry thêm figure_left / figure_right)*
  - *(với `nhan_xet`/`chu_y`: body Tex phải có `color=COLOR_WARNING`)*

- **narration**: |
    Định nghĩa. Tứ giác có bốn đỉnh nằm trên một đường tròn
    được gọi là tứ giác nội tiếp đường tròn.
    Đường tròn đó được gọi là đường tròn ngoại tiếp tứ giác.
    Chẳng hạn, trên hình vẽ, tứ giác A B C D có bốn đỉnh nằm trên đường tròn tâm O.

- **animations**:
  - `Write(block_heading)` at start
  - `FadeIn(body_lines[0])` — cùng với `Create(circle)`
  - `FadeIn(body_lines[1..2])` — cùng với `Create(quad ABCD + labels)`
  - `Write(formula_1)` — sau body hoàn chỉnh
  - `Indicate(terms_bold_mobs, scale_factor=1.15)` — cuối scene

- **cleanup**: `FadeOut(block_heading, body_group, formula_group)` | keep hoặc FadeOut `figure_group`

---

## Scene 02 — [Tên mục]

*(lặp cấu trúc trên)*

---

## Ghi chú dựng hình

*(Tùy chọn — liệt kê tọa độ, màu, hoặc quyết định kỹ thuật đặc biệt)*
- `O = ORIGIN`, `R = 2.5`
- Màu đường tròn: `COLOR_CIRCLE` (`#1565C0`)
- Màu tứ giác: `COLOR_EQUAL_3` (`#1565C0`) hoặc stroke `COLOR_DEFAULT`
```

---

## Ví dụ ngắn: Bài 3 Tứ giác nội tiếp (4 scene)

```markdown
# Scene Spec Lý Thuyết: BÀI 3. TỨ GIÁC NỘI TIẾP

## Thông tin chung
- lesson_title: BÀI 3. TỨ GIÁC NỘI TIẾP
- lesson_type: theory
- subject: geometry
- total_scenes: 4
- estimated_duration: 5–7 phút

---

## Scene 00 — Intro
- method: scene00_intro
- duration: 25s
- content: lesson_title + "I. TÓM TẮT LÝ THUYẾT"
- animations: Write(lesson_title) → FadeIn(section_heading)
- cleanup: giữ lesson_title + section_heading cho scenes 01–03

## Scene 01 — Định nghĩa
- method: scene01_dinhNghia
- block_type: dinh_nghia
- heading: "1. Định nghĩa"
- body_lines:
  - "Tứ giác có bốn đỉnh nằm trên một đường tròn gọi là"
  - r"\textbf{tứ giác nội tiếp} đường tròn"
  - "Đường tròn đó gọi là \textbf{đường tròn ngoại tiếp tứ giác}."
- terms_bold: [tứ giác nội tiếp, đường tròn ngoại tiếp tứ giác]
- figure:
    type: geometry
    panel: right, width_ratio: 0.45
    build:
      - circle(O, R=2.2)
      - points A(top), B(right), C(bottom-right), D(left) on circle
      - quad ABCD
      - labels + dot O
- narration: |
    Định nghĩa. Tứ giác có bốn đỉnh nằm trên một đường tròn
    được gọi là tứ giác nội tiếp đường tròn.
    Đường tròn đó được gọi là đường tròn ngoại tiếp tứ giác.
- animations:
  - Write(block_heading) at start
  - FadeIn(body_lines[0..1]) + Create(circle + 4 points)
  - FadeIn(body_lines[2]) + Create(quad ABCD + labels)
  - Indicate(terms_bold_mobs)
- cleanup: FadeOut(block_heading, body_group) | keep figure_group cho scene 02

## Scene 02 — Định lí
- method: scene02_dinhLi
- block_type: dinh_li
- heading: "2. Định lí"
- body_lines:
  - "Trong một tứ giác nội tiếp, tổng số đo hai góc đối nhau bằng 180°."
- formulas:
  - formula_main: r"\widehat{A} + \widehat{C} = \widehat{B} + \widehat{D} = 180^\circ"
- figure:
    type: geometry
    panel: right, width_ratio: 0.45
    build: tái dùng figure scene 01 (circle + ABCD đã có)
    additions:
      - Indicate angle A + angle C (COLOR_EQUAL_1) → show sum = 180°
      - Indicate angle B + angle D (COLOR_EQUAL_2) → show sum = 180°
- narration: |
    Định lí. Trong một tứ giác nội tiếp,
    tổng hai góc đối nhau bằng 180 độ.
    Trên hình, góc A cộng góc C bằng 180 độ.
    Tương tự, góc B cộng góc D cũng bằng 180 độ.
- animations:
  - Write(block_heading) at start
  - FadeIn(body_lines[0]) + Write(formula_main)
  - Indicate(angle_A, angle_C, color=COLOR_EQUAL_1)
  - Indicate(angle_B, angle_D, color=COLOR_EQUAL_2)
- cleanup: FadeOut(block_heading, body_group, formula_main, angle_indicators) | keep figure_group

## Scene 03 — Nhận xét
- method: scene03_nhanXet
- block_type: nhan_xet
- heading: "(*) Nhận xét"        # prefix (*) + nhãn SGK; dùng "(*) Ghi nhớ" nếu SGK ghi "Ghi nhớ"
- body_style: italic + COLOR_WARNING   # mọi bullet/body của nhan_xet đều italic đỏ
- body_lines:
  - r"\textit{- Hình chữ nhật và hình vuông là các tứ giác nội tiếp.}"   # color=COLOR_WARNING
  - r"\textit{- Đường tròn ngoại tiếp có tâm là giao điểm hai đường chéo}"
  - r"\textit{- và bán kính bằng một nửa độ dài đường chéo.}"
- figure:
    type: dual_geometry
    figure_left:
      label: "Hình chữ nhật"
      build: rect ABCD → diagonals AC, BD → dot O (intersection) → circle(O, R=half_diag)
    figure_right:
      label: "Hình vuông"
      build: square EFGH → diagonals EG, FH → dot O → circle(O, R)
    panel: right, width_ratio: 0.50
- narration: |
    Nhận xét. Hình chữ nhật và hình vuông là các tứ giác nội tiếp.
    Đường tròn ngoại tiếp của chúng có tâm là giao điểm hai đường chéo.
    Bán kính bằng một nửa độ dài đường chéo.
- animations:
  - Write(block_heading) at start
  - FadeIn(body_lines[0]) + Create(rect + square outlines)
  - Create(diagonals cả hai hình) + FadeIn(dot O cả hai) + Create(both circles)
  - FadeIn(body_lines[1..2])
- cleanup: FadeOut(all)
```

---

## Checklist trước khi output spec

- [ ] Mỗi scene có `method`, `block_type`, `heading`, `narration`, `animations`, `cleanup`
- [ ] Mỗi `figure.type ≠ none` có trích dẫn **dấu hiệu trên ảnh SGK** (hoặc yêu cầu user)
- [ ] **Cấm** suy diễn: "có phương trình bậc hai → vẽ parabol"
- [ ] `figure.type: none` → ghi `panel: none` + block `layout:` (`wrap_width_cm`, `formula_method: place_formula_left`, `line_grouping`)
- [ ] `figure.type: none` → build Step 2 dùng `TheoryColumn(has_figure=False)`, `tex_wrapped`, **không** `place_formula()`
- [ ] `figure.build` liệt kê đủ thứ tự dựng (không để agent tự đoán) — bỏ qua nếu `figure.type: none`
- [ ] Narration không chứa ký hiệu toán học (∠, °, AB), câu ≤ 20 từ
- [ ] Không có `GT:`, `KL:`, `proof_accumulator`, `ProofLine` trong spec
- [ ] Tổng thời lượng ước tính hợp lý (45–75s/scene lý thuyết)
- [ ] `cleanup` ghi rõ FadeOut gì, giữ gì (đặc biệt khi scene sau tái dùng figure)
