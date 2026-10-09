# Scene Spec Lý Thuyết: HỆ THỨC VI-ÉT

## Thông tin chung

- **lesson_title**: HỆ THỨC VI-ÉT
- **lesson_type**: theory
- **subject**: algebra
- **section_heading**: 1. CÁC KIẾN THỨC CẦN NHỚ
- **total_scenes**: 3
- **estimated_duration**: 4–6 phút

---

## Scene 00 — Intro

- **method**: `scene00_intro`
- **duration**: 20–25s
- **content**: Tiêu đề bài + heading phần "1. CÁC KIẾN THỨC CẦN NHỚ"

- **narration**: |
    Hệ thức Vi-ét.
    Phần một. Các kiến thức cần nhớ.

- **animations**:
  - `Write(lesson_title)` — `Tex(r"\textbf{HỆ THỨC VI-ÉT}")`, `font_size=36`, `to_edge(UP, buff=0.4)`
  - `FadeIn(section_heading)` — `Tex(r"\textbf{1. CÁC KIẾN THỨC CẦN NHỚ}")`, `font_size=28`, dưới `lesson_title`, `buff=0.35`
  - `Wait(1.5)` — giữ tiêu đề trước khi chuyển scene

- **cleanup**:
  - `FadeOut(section_heading)`
  - Giữ `lesson_title` ở `to_edge(UP)` cho các scene sau

---

## Scene 01 — Hệ thức Vi-ét

- **method**: `scene01_heThucViet`
- **block_type**: `dinh_li`
- **duration**: 65–80s
- **heading**: "Hệ thức Vi-ét"

- **body_lines**:
  - `"Cho phương trình bậc hai $ax^2 + bx + c = 0$ với $a \neq 0$."`
  - `"Nếu $x_1, x_2$ là hai nghiệm của phương trình thì:"`

- **formulas**:
  - `formula_viet`: |
      r"\begin{cases} x_1 + x_2 = \dfrac{-b}{a} \\[6pt] x_1 \cdot x_2 = \dfrac{c}{a} \end{cases}"
  - `example_intro`: `"Ví dụ: Phương trình $2x^2 - 5x + 2 = 0$ có $\Delta = 9 > 0$ nên phương trình có hai nghiệm $x_1, x_2$."`
  - `example_label`: `"Theo hệ thức Vi-ét ta có:"`
  - `formula_example`: |
      r"\begin{cases} x_1 + x_2 = \dfrac{5}{2} \\[6pt] x_1 \cdot x_2 = \dfrac{2}{2} = 1 \end{cases}"

- **terms_bold**: [hệ thức Vi-ét, tổng hai nghiệm, tích hai nghiệm]

- **figure**:
  - type: `function`
  - panel: `right`
  - width_ratio: `0.45`
  - build:
    - `axes(x_range=[-0.5, 3, 0.5], y_range=[-1, 4, 1])` — trục tọa độ, màu `COLOR_GRID`
    - `curve(expr="2*x**2 - 5*x + 2", x_range=[-0.3, 2.8])` — parabol màu `COLOR_EQUAL_1`, `stroke_width=2.5`
    - `mark_roots(x_values=[0.5, 2])` — điểm giao trục hoành, bán kính `0.08`, màu `COLOR_ACTIVE`
    - `labels roots` — `x_1` tại `(0.5, 0)`, `x_2` tại `(2, 0)`, `buff=0.12`, `font_size=22`
    - `label equation` — `y = 2x^2 - 5x + 2` góc trên-phải panel, `font_size=20`, màu `COLOR_SECONDARY`
    - `x_axis highlight` — tô nhẹ đoạn `[x_1, x_2]` trên trục hoành khi đọc tổng hai nghiệm (Braces hoặc `Line` màu `COLOR_EQUAL_2`)

- **narration**: |
    Hệ thức Vi-ét.
    Cho phương trình bậc hai a x bình cộng b x cộng c bằng không,
    với a khác không.
    Nếu x một và x hai là hai nghiệm của phương trình thì
    tổng hai nghiệm bằng trừ b chia a,
    và tích hai nghiệm bằng c chia a.
    Ví dụ, phương trình hai x bình trừ năm x cộng hai bằng không
    có delta bằng chín, lớn hơn không,
    nên phương trình có hai nghiệm x một và x hai.
    Theo hệ thức Vi-ét, tổng hai nghiệm bằng năm phần hai,
    tích hai nghiệm bằng hai phần hai, tức bằng một.
    Trên đồ thị, parabol cắt trục hoành tại hai điểm
    x một bằng một phần hai và x hai bằng hai.

- **animations**:
  - `Write(block_heading)` — đầu scene, `to_corner(UL, buff=0.5)`
  - `FadeIn(body_lines[0])` — đồng thời `Create(axes)` + `Write(label equation)`
  - `FadeIn(body_lines[1])` — đồng thời `Create(curve)`
  - `Write(formula_viet)` — sau body dẫn, căn trái cột text
  - `Indicate(formula_viet[0])` — nhấn dòng tổng khi đọc "tổng hai nghiệm"
  - `Indicate(formula_viet[1])` — nhấn dòng tích khi đọc "tích hai nghiệm"
  - `FadeIn(example_intro)` — chuyển sang ví dụ
  - `mark_roots` + `Write(labels x_1, x_2)` — đồng thời khi đọc "có hai nghiệm"
  - `Write(example_label)` + `Write(formula_example)` — khi đọc "Theo hệ thức Vi-ét"
  - `Indicate(mark_roots)` — nhấn hai điểm giao trục hoành khi đọc giá trị nghiệm
  - `Indicate(terms_bold_mobs, scale_factor=1.15)` — cuối scene
  - `Wait(1)` — giữ công thức và hình

- **cleanup**:
  - `FadeOut(block_heading, body_group, formula_viet, example_intro, example_label, formula_example)`
  - **Giữ** `figure_group` (axes + parabol + roots) cho Scene 02 tham chiếu nếu cần, hoặc `FadeOut` nếu Scene 02 dùng hình mới

---

## Scene 02 — Ứng dụng của hệ thức Vi-ét

- **method**: `scene02_ungDungViet`
- **block_type**: `nhan_xet`
- **duration**: 70–85s
- **heading**: "Ứng dụng của hệ thức Vi-ét"

- **body_lines**:
  - `r"\textbf{a)} Xét phương trình bậc hai: $ax^2 + bx + c = 0$ với $a \neq 0$."`
  - `"Nếu phương trình có $a + b + c = 0$ thì phương trình có một nghiệm là $x_1 = 1$, nghiệm kia là $x_2 = \dfrac{c}{a}$."`
  - `"Nếu phương trình có $a - b + c = 0$ thì phương trình có một nghiệm là $x_1 = -1$, nghiệm kia là $x_2 = -\dfrac{c}{a}$."`
  - `r"\textbf{b)} Tìm hai số biết tổng và tích của chúng:"`
  - `"Nếu hai số có tổng bằng $S$ và tích bằng $P$ thì hai số đó là hai nghiệm của phương trình"`

- **formulas**:
  - `formula_find_numbers`: `r"X^2 - SX + P = 0 \quad (\text{ĐK: } S^2 \geq 4P)"`

- **terms_bold**: [a + b + c = 0, a - b + c = 0, tổng bằng S, tích bằng P]

- **figure**:
  - type: `function`
  - panel: `right`
  - width_ratio: `0.48`
  - build:
    - `VGroup.arrange(DOWN, buff=0.4)` — hai đồ thị nhỏ xếp dọc trong panel
    - **sub_figure_top** — trường hợp nghiệm bằng 1:
      - `axes_small(x_range=[-1, 4, 1], y_range=[-2, 5, 1])` — scale `0.55`
      - `curve(expr="x**2 - 3*x + 2", x_range=[-0.5, 3.5])` — ví dụ `a+b+c=0`: `1+(-3)+2=0`, màu `COLOR_EQUAL_1`
      - `mark_root(x=1, color=COLOR_ACTIVE)` — nghiệm `x_1 = 1` nổi bật
      - `mark_root(x=2, color=COLOR_SECONDARY)` — nghiệm kia `x_2 = c/a = 2`
      - `label`: `"a+b+c=0 \Rightarrow x_1=1"` — `font_size=18`, trên đồ thị
    - **sub_figure_bottom** — trường hợp nghiệm bằng -1:
      - `axes_small(x_range=[-4, 1, 1], y_range=[-2, 5, 1])` — scale `0.55`
      - `curve(expr="x**2 + 3*x + 2", x_range=[-3.5, 0.5])` — ví dụ `a-b+c=0`: `1-3+2=0`, màu `COLOR_EQUAL_2`
      - `mark_root(x=-1, color=COLOR_ACTIVE)` — nghiệm `x_1 = -1` nổi bật
      - `mark_root(x=-2, color=COLOR_SECONDARY)` — nghiệm kia `x_2 = -c/a = -2`
      - `label`: `"a-b+c=0 \Rightarrow x_1=-1"` — `font_size=18`, trên đồ thị

- **narration**: |
    Ứng dụng của hệ thức Vi-ét.
    Xét phương trình bậc hai a x bình cộng b x cộng c bằng không.
    Nếu a cộng b cộng c bằng không
    thì phương trình có một nghiệm là x bằng một,
    nghiệm kia là c chia a.
    Chẳng hạn, x bình trừ ba x cộng hai bằng không
    có một cộng trừ ba cộng hai bằng không,
    nên x bằng một là nghiệm.
    Nếu a trừ b cộng c bằng không
    thì phương trình có một nghiệm là x bằng trừ một,
    nghiệm kia là trừ c chia a.
    Ví dụ, x bình cộng ba x cộng hai bằng không
    có một trừ ba cộng hai bằng không,
    nên x bằng trừ một là nghiệm.
    Một ứng dụng quan trọng khác:
    tìm hai số biết tổng và tích của chúng.
    Nếu hai số có tổng bằng S và tích bằng P
    thì hai số đó chính là hai nghiệm
    của phương trình X bình trừ S X cộng P bằng không,
    với điều kiện S bình lớn hơn hoặc bằng bốn P.

- **animations**:
  - `Write(block_heading)` — đầu scene
  - `FadeOut(figure_group)` — từ Scene 01 nếu còn trên màn hình
  - `FadeIn(body_lines[0])` — mở đầu mục a
  - `FadeIn(body_lines[1])` — đồng thời `Create(sub_figure_top: axes + curve)` + `Write(sub_figure_top.label)`
  - `mark_root(x=1)` + `Indicate(root_at_1, color=COLOR_ACTIVE)` — khi đọc "nghiệm là x bằng một"
  - `mark_root(x=2)` — nghiệm kia, màu nhạt hơn
  - `FadeIn(body_lines[2])` — đồng thời `Create(sub_figure_bottom: axes + curve)` + `Write(sub_figure_bottom.label)`
  - `mark_root(x=-1)` + `Indicate(root_at_minus_1, color=COLOR_ACTIVE)` — khi đọc "x bằng trừ một"
  - `mark_root(x=-2)` — nghiệm kia
  - `FadeIn(body_lines[3..4])` — chuyển sang mục b
  - `Write(formula_find_numbers)` — công thức tìm hai số, căn trái cột text
  - `Indicate(formula_find_numbers)` — nhấn khi đọc phương trình X bình trừ S X cộng P
  - `Indicate(terms_bold_mobs, scale_factor=1.15)` — cuối scene
  - `Wait(1.5)`

- **cleanup**:
  - `FadeOut(block_heading, body_group, formula_find_numbers, figure_group)`
  - `FadeOut(lesson_title)` — kết thúc bài

---

## Ghi chú dựng hình

| Tham số | Giá trị |
|---------|---------|
| Parabol Scene 01 | `y = 2x² - 5x + 2`, nghiệm `x₁ = 0.5`, `x₂ = 2` |
| Parabol trên (Scene 02) | `y = x² - 3x + 2`, kiểm tra `a+b+c = 1-3+2 = 0`, nghiệm `1` và `2` |
| Parabol dưới (Scene 02) | `y = x² + 3x + 2`, kiểm tra `a-b+c = 1-3+2 = 0`, nghiệm `-1` và `-2` |
| Màu parabol chính | `COLOR_EQUAL_1` (Scene 01), `COLOR_EQUAL_1` / `COLOR_EQUAL_2` (Scene 02) |
| Màu nghiệm đặc biệt | `COLOR_ACTIVE` — nghiệm `±1` |
| Màu nghiệm còn lại | `COLOR_SECONDARY` |
| Scale sub-figure Scene 02 | `0.55` mỗi axes, `arrange(DOWN, buff=0.4)` |

**Quyết định kỹ thuật:**
- Scene 01 gộp **phát biểu hệ thức + ví dụ tính** trong cùng một scene theo yêu cầu chia theo mục SGK.
- Scene 02 gộp **hai trường hợp nghiệm đặc biệt + bài toán tìm hai số** — phần tìm hai số không có hình riêng, dùng công thức text.
- Ví dụ số trong Scene 02 (`x²-3x+2`, `x²+3x+2`) **minh hoạ** điều kiện `a±b+c=0`, không trùng ví dụ Scene 01.
- Voiceover: không đọc ký hiệu `Δ`, `≠`, `\dfrac` — dùng "delta", "khác không", "phần".
- `subject: algebra` → Step 2 dùng `SKILL-algebra.md` + `theory-figure/algebra` → `coordinate-plane`.
