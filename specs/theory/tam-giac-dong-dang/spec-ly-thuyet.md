# Scene Spec Lý Thuyết: TAM GIÁC ĐỒNG DẠNG

## Thông tin chung

- **lesson_title**: TAM GIÁC ĐỒNG DẠNG
- **lesson_type**: theory
- **subject**: geometry
- **total_scenes**: 4
- **estimated_duration**: 6–8 phút

---

## Scene 00 — Intro

- **method**: `scene00_intro`
- **duration**: 25s
- **content**: Tiêu đề bài + heading phần
- **animations**:
  - `Write(lesson_title)` — "TAM GIÁC ĐỒNG DẠNG", font_size 40, to_edge(UP)
  - `FadeIn(section_heading)` — "I. CÁC KIẾN THỨC CẦN NHỚ", font_size 30, dưới lesson_title
- **cleanup**: `FadeOut(section_heading)` | thu nhỏ `lesson_title` to_edge(UP, buff=0.2)

---

## Scene 01 — Định nghĩa

- **method**: `scene01_dinhNghia`
- **block_type**: `dinh_nghia`
- **duration**: 65–75s
- **heading**: "1. Định nghĩa"

- **body_lines**:
  - `"Tam giác A'B'C' gọi là \textbf{đồng dạng} với tam giác ABC nếu:"`
  - `r"\frac{A'B'}{AB} = \frac{B'C'}{BC} = \frac{A'C'}{AC}"`
  - `r"\widehat{A'} = \widehat{A},\quad \widehat{B'} = \widehat{B},\quad \widehat{C'} = \widehat{C}"`
  - `r"\text{Kí hiệu: } \Delta A'B'C' \backsim \Delta ABC"`
  - `r"k = \frac{A'B'}{AB} = \frac{B'C'}{BC} = \frac{A'C'}{AC} \text{ là tỉ số đồng dạng}"`

- **formulas**:
  - `formula_ratio`: `r"\frac{A'B'}{AB} = \frac{B'C'}{BC} = \frac{A'C'}{AC}"`
  - `formula_angles`: `r"\widehat{A'} = \widehat{A},\quad \widehat{B'} = \widehat{B},\quad \widehat{C'} = \widehat{C}"`
  - `formula_symbol`: `r"\Delta A'B'C' \backsim \Delta ABC"`
  - `formula_k`: `r"k = \frac{A'B'}{AB} = \frac{B'C'}{BC} = \frac{A'C'}{AC}"`

- **terms_bold**: [đồng dạng, tỉ số đồng dạng]

- **figure**:
  - type: `dual_geometry`
  - panel: `right`
  - width_ratio: `0.48`
  - figure_left:
    - label: `r"\Delta ABC"`
    - build:
      - `point A at (-1.0, 1.5)` — đỉnh trên bên trái
      - `point B at (-1.8, -1.0)` — đỉnh dưới bên trái
      - `point C at (0.6, -1.0)` — đỉnh dưới bên phải
      - `triangle ABC — edges AB, BC, CA (stroke COLOR_DEFAULT)`
      - `labels A(UL), B(DL), C(DR)`
  - figure_right:
    - label: `r"\Delta A'B'C'"`
    - build:
      - `point A' at (0.5, 0.9)` — scale nhỏ hơn tam giác ABC (tỉ số ~0.6)
      - `point B' at (-0.1, -0.5)`
      - `point C' at (1.3, -0.5)`
      - `triangle A'B'C' — edges A'B', B'C', C'A' (stroke COLOR_HIGHLIGHT)`
      - `labels A'(UR), B'(DL), C'(DR)`
  - note: hai hình đặt cạnh nhau, cùng hàng, scale vừa panel phải

- **narration**: |
    Định nghĩa. Tam giác A B C và tam giác A phẩy B phẩy C phẩy.
    Ta nói tam giác A phẩy B phẩy C phẩy đồng dạng với tam giác A B C
    khi tỉ số các cạnh tương ứng bằng nhau
    và ba góc tương ứng cũng bằng nhau.
    Cụ thể, A phẩy B phẩy trên A B bằng B phẩy C phẩy trên B C bằng A phẩy C phẩy trên A C.
    Đồng thời, góc A phẩy bằng góc A, góc B phẩy bằng góc B, góc C phẩy bằng góc C.
    Ta viết: tam giác A phẩy B phẩy C phẩy đồng dạng với tam giác A B C.
    Giá trị k bằng tỉ số các cạnh tương ứng được gọi là tỉ số đồng dạng.

- **animations**:
  - `Write(block_heading)` at start
  - `FadeIn(body_lines[0])` + `Create(triangle ABC + labels)` — đồng thời
  - `Write(formula_ratio)` + `Create(triangle A'B'C' + labels)` — giới thiệu hai tam giác
  - `Write(formula_angles)` — sau khi có hai hình
  - `Write(formula_symbol)` — highlight tên kí hiệu đồng dạng ∽
  - `Write(formula_k)` — giới thiệu tỉ số k
  - `Indicate(terms_bold_mobs, scale_factor=1.15)` — nhấn "đồng dạng" và "tỉ số đồng dạng"

- **cleanup**: `FadeOut(block_heading, body_lines, formula_ratio, formula_angles, formula_symbol, formula_k)` | keep `figure_group` cho Scene 02

---

## Scene 02 — Nhận xét

- **method**: `scene02_nhanXet`
- **block_type**: `nhan_xet`
- **duration**: 50–65s
- **heading**: "Nhận xét"

- **body_lines**:
  - `r"(1)\; \Delta A'B'C' \backsim \Delta ABC \text{ tỉ số } k \Rightarrow \Delta ABC \backsim \Delta A'B'C' \text{ tỉ số } \tfrac{1}{k}"`
  - `"Ta nói hai tam giác A'B'C' và ABC \textbf{đồng dạng với nhau}."`
  - `r"(2)\; \text{Hai tam giác bằng nhau} \Rightarrow \text{đồng dạng, } k = 1."`
  - `r"\text{Mọi tam giác đồng dạng với chính nó.}"`
  - `r"(3)\; \Delta A''B''C'' \backsim \Delta A'B'C' \text{ tỉ số } k,\; \Delta A'B'C' \backsim \Delta ABC \text{ tỉ số } m"`
  - `r"\Rightarrow \Delta A''B''C'' \backsim \Delta ABC \text{ tỉ số } k \cdot m"`

- **formulas**:
  - `formula_1`: `r"\Delta A'B'C' \backsim \Delta ABC \text{ (tỉ số }k) \Rightarrow \Delta ABC \backsim \Delta A'B'C' \text{ (tỉ số }\tfrac{1}{k})"`
  - `formula_2`: `r"k = 1 \iff \Delta A'B'C' = \Delta ABC"`
  - `formula_3`: `r"k \cdot m \text{ là tỉ số đồng dạng của } \Delta A''B''C'' \text{ với } \Delta ABC"`

- **figure**:
  - type: `none`
  - note: dùng lại figure_group từ Scene 01 (hai tam giác đã có) nếu panel còn chỗ; nếu không thì FadeOut figure

- **narration**: |
    Nhận xét. Có ba tính chất quan trọng về quan hệ đồng dạng.
    Thứ nhất, nếu tam giác A phẩy B phẩy C phẩy đồng dạng với tam giác A B C theo tỉ số k,
    thì ngược lại, tam giác A B C đồng dạng với tam giác A phẩy B phẩy C phẩy theo tỉ số một phần k.
    Khi đó ta nói hai tam giác đồng dạng với nhau.
    Thứ hai, hai tam giác bằng nhau thì đồng dạng với tỉ số đồng dạng bằng một.
    Mọi tam giác đều đồng dạng với chính nó.
    Thứ ba, nếu tam giác A hai phẩy B hai phẩy C hai phẩy đồng dạng với tam giác A phẩy B phẩy C phẩy theo tỉ số k,
    và tam giác A phẩy B phẩy C phẩy đồng dạng với tam giác A B C theo tỉ số m,
    thì tam giác A hai phẩy B hai phẩy C hai phẩy đồng dạng với tam giác A B C theo tỉ số k nhân m.

- **animations**:
  - `Write(block_heading)` at start
  - `FadeIn(body_lines[0..1])` + `Write(formula_1)` — tính chất 1
  - `FadeIn(body_lines[2..3])` + `Write(formula_2)` — tính chất 2
  - `FadeIn(body_lines[4..5])` + `Write(formula_3)` — tính chất 3
  - `Indicate(formula_1, formula_2, formula_3)` lần lượt khi đọc đến từng công thức

- **cleanup**: `FadeOut(block_heading, body_lines, formula_1, formula_2, formula_3, figure_group)`

---

## Scene 03 — Định lí

- **method**: `scene03_dinhLi`
- **block_type**: `dinh_li`
- **duration**: 55–70s
- **heading**: "2. Định lí"

- **body_lines**:
  - `"Nếu một đường thẳng cắt hai cạnh của một tam giác"`
  - `"là \textbf{song song} với cạnh còn lại,"`
  - `"thì nó tạo thành một tam giác mới \textbf{đồng dạng} với tam giác đã cho."`

- **formulas**:
  - `formula_gt`: `r"\Delta ABC,\; MN \parallel BC \;(M \in AB,\; N \in AC)"`
  - `formula_kl`: `r"\Rightarrow \Delta AMN \backsim \Delta ABC"`

- **terms_bold**: [song song, đồng dạng]

- **figure**:
  - type: `geometry`
  - panel: `right`
  - width_ratio: `0.45`
  - build:
    - `point A at (0, 2.5)` — đỉnh trên
    - `point B at (-2.0, -1.0)` — đỉnh dưới trái
    - `point C at (2.0, -1.0)` — đỉnh dưới phải
    - `triangle ABC — edges AB, BC, CA (stroke COLOR_DEFAULT)`
    - `point M on AB at ratio 0.55 from A` — M ∈ AB
    - `point N on AC at ratio 0.55 from A` — N ∈ AC (cùng tỉ lệ AM/AB = AN/AC)
    - `segment MN (stroke COLOR_HIGHLIGHT, dashed NO)` — đường song song với BC
    - `parallel_mark on MN and BC` — dấu song song (//) trên MN và BC
    - `small triangle AMN filled COLOR_HIGHLIGHT opacity 0.15` — tô nhạt tam giác AMN
    - `labels A(UP), B(DL), C(DR), M(LEFT), N(RIGHT)`
  - note: MN // BC được minh họa bằng dấu song song; tam giác AMN tô màu nhẹ để phân biệt với ABC

- **narration**: |
    Định lí. Xét tam giác A B C.
    Nếu ta vẽ đường thẳng M N cắt cạnh A B tại M và cắt cạnh A C tại N,
    sao cho M N song song với B C,
    thì tam giác A M N đồng dạng với tam giác A B C.
    Chẳng hạn, trên hình, M nằm trên A B, N nằm trên A C, và M N song song với B C.
    Khi đó tam giác A M N đồng dạng với tam giác A B C.

- **animations**:
  - `Write(block_heading)` at start
  - `Create(triangle ABC + labels A, B, C)` + `FadeIn(body_lines[0])` — đồng thời
  - `Create(point M + point N)` + `Create(segment MN)` + `FadeIn(body_lines[1])` — vẽ đường MN
  - `FadeIn(parallel_marks MN và BC)` — nhấn song song
  - `FadeIn(body_lines[2])` + `Write(formula_gt)` — phát biểu GT
  - `FadeIn(fill AMN)` + `Write(formula_kl)` — kết luận đồng dạng
  - `Indicate(terms_bold_mobs, scale_factor=1.15)` — nhấn "song song" và "đồng dạng"

- **cleanup**: `FadeOut(all)`

---

## Ghi chú dựng hình

- **Màu sắc**:
  - Tam giác ABC: `COLOR_DEFAULT` (`#FFFFFF` trên nền tối hoặc `#212121` trên nền sáng)
  - Tam giác A'B'C' (Scene 01): `COLOR_HIGHLIGHT` (`#FFD600`)
  - Đường MN (Scene 03): `COLOR_HIGHLIGHT` (`#FFD600`)
  - Tô tam giác AMN: `COLOR_HIGHLIGHT` opacity `0.15`
  - Dấu song song: `COLOR_EQUAL_1` (`#E53935`)

- **Layout**:
  - Mặc định: text panel trái (width_ratio 0.52), figure panel phải (0.48)
  - Scene 02: text full width nếu figure_group đã FadeOut; hoặc text chiếm 0.60 nếu giữ hình

- **Kí hiệu đồng dạng**: dùng `\backsim` trong LaTeX (`∽`)

- **Tỉ lệ dựng M, N** (Scene 03): `AM/AB = AN/AC ≈ 0.55` để MN trông rõ, không quá gần đỉnh A
