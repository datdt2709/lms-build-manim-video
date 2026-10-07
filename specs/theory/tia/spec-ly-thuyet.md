# Scene Spec Lý Thuyết: CÁC DẤU HIỆU NHẬN BIẾT MỘT TIA NẰM GIỮA HAI TIA KHÁC

## Thông tin chung

- **lesson_title**: CÁC DẤU HIỆU NHẬN BIẾT MỘT TIA NẰM GIỮA HAI TIA KHÁC
- **lesson_type**: theory
- **subject**: geometry
- **section_heading**: A. KIẾN THỨC CẦN NHỚ
- **total_scenes**: 8
- **estimated_duration**: 8–10 phút

> **Layout 3 tầng:** `lesson_title` (tầng 0) → `section_heading` persistent scenes 01–07 (tầng 1) → `block_heading` đổi mỗi scene, neo dưới `section_heading` (tầng 2).

> **Ghi chú nguồn:** Ảnh SGK — Chuyên đề nâng cao, phần **A. Kiến thức cần nhớ** (Các dấu hiệu nhận biết một tia nằm giữa hai tia khác). Mọi scene nội dung đều có hình minh họa SGK (Hình 33–37).

---

## Scene 00 — Intro

- **method**: `scene00_intro`
- **duration**: 20–25s
- **content**: Tiêu đề bài + heading phần "A. KIẾN THỨC CẦN NHỚ"

- **figure**:
  - type: `none`
  - panel: `none`

- **narration**: |
    Các dấu hiệu nhận biết một tia nằm giữa hai tia khác.
    Phần A. Kiến thức cần nhớ.
    Khi tia Oy nằm giữa Ox và Oz,
    tổng góc x Oy cộng góc y Oz bằng góc x Oz.
    Bài học giúp rèn luyện lập luận chính xác
    khi xét vị trí tương đối của các tia.

- **animations**:
  - `Write(lesson_title)` — `Tex(r"\textbf{CÁC DẤU HIỆU NHẬN BIẾT MỘT TIA NẰM GIỮA HAI TIA KHÁC}")`, `font_size=36`, `to_edge(UP, buff=0.4)`
  - `FadeIn(section_heading)` — `Tex(r"\textbf{A. KIẾN THỨC CẦN NHỚ}")`, `font_size=28`, dưới `lesson_title`, `buff=0.35`
  - `Wait(1.5)` — giữ tiêu đề trước khi chuyển scene

- **cleanup**: giữ `lesson_title` + `section_heading` cho scenes 01–07

---

## Scene 01 — Dấu hiệu 1

- **method**: `scene01_dauHieu1`
- **block_type**: `dinh_li`
- **duration**: 55–65s
- **heading**: "Dấu hiệu 1"

- **body_lines**:
  - `"Cho tia $Oy$ cắt đoạn thẳng $AB$ tại điểm $M$ nằm giữa hai điểm $A$ và $B$"`
  - `"($A, B$ khác $O$; $A$ thuộc tia $Ox$; $B$ thuộc tia $Oz$)."`
  - `"Khi đó tia $Oy$ nằm giữa hai tia $Ox$ và $Oz$."`

- **terms_bold**: [tia Oy nằm giữa hai tia Ox và Oz]

- **figure**:
  - type: `geometry`
  - panel: `right`
  - width_ratio: `0.45`
  - sgk_ref: Hình 33
  - build:
    - `dot(O)` — gốc `O = ORIGIN`, màu `COLOR_DEFAULT`
    - `ray Ox` — góc phương vị `0°`, độ dài `3.0`, màu `COLOR_DEFAULT`, `stroke_width=2`
    - `ray Oy` — góc phương vị `~40°` (CCW từ Ox), độ dài `3.0`
    - `ray Oz` — góc phương vị `~95°`, độ dài `3.0`
    - `point A on Ox` — khoảng cách `dist=2.5` từ O
    - `point B on Oz` — khoảng cách `dist=2.5` từ O
    - `segment AB` — nối A và B, màu `COLOR_DEFAULT`, `stroke_width=2`
    - `point M` — giao `Oy ∩ AB` (tính toán giao điểm, không hardcode tọa độ)
    - `dot M` — màu `COLOR_HIGHLIGHT`, `radius=0.07`
    - `labels` — `O` (dưới gốc), `x`, `y`, `z` (cạnh đầu mút tia), `A`, `B`, `M` (buff=0.15)

- **narration**: |
    Dấu hiệu một.
    Cho tia Oy cắt đoạn thẳng A B tại điểm M
    nằm giữa hai điểm A và B.
    A và B khác O; A thuộc tia Ox; B thuộc tia Oz.
    Khi đó tia Oy nằm giữa hai tia Ox và Oz.
    Chẳng hạn, trên hình vẽ,
    tia Oy cắt đoạn A B tại M nằm giữa A và B.

- **animations**:
  - `Write(block_heading)` — đầu scene, neo dưới `section_heading`, `buff=0.25`
  - `Create(ray Ox)` + `Create(ray Oz)` — vẽ hai tia biên trước
  - `FadeIn(body_lines[0..2])` — đồng thời `Create(dots A, B)` + `Create(segment AB)`
  - `Create(ray Oy)` + `FadeIn(dot M)` + `Write(label M)` — khi nhấn giao điểm
  - `Indicate(dot M, dot A, dot B, color=COLOR_HIGHLIGHT)` — nhấn M nằm giữa A và B
  - `Indicate(ray Oy, color=COLOR_HIGHLIGHT)` — kết luận Oy nằm giữa Ox và Oz
  - `Wait(1)` — giữ hình trước cleanup

- **cleanup**:
  - `FadeOut(block_heading, body_group)`
  - **Giữ** `figure_group` (Hình 33: Ox, Oy, Oz, A, B, AB, M, labels) cho Scene 02 tái dùng

---

## Scene 02 — Dấu hiệu 2

- **method**: `scene02_dauHieu2`
- **block_type**: `dinh_li`
- **duration**: 50–60s
- **heading**: "Dấu hiệu 2"

- **body_lines**:
  - `"Nếu tổng số đo hai góc $x\widehat{O}y$ và $y\widehat{O}z$ bằng số đo góc $x\widehat{O}z$ thì tia $Oy$ nằm giữa hai tia $Ox$ và $Oz$."`

- **formulas**:
  - `formula_sum`: `r"x\widehat{O}y + y\widehat{O}z = x\widehat{O}z"`

- **figure**:
  - type: `geometry`
  - panel: `right`
  - width_ratio: `0.45`
  - sgk_ref: Hình 33 (tái dùng)
  - build:
    - `reuse` — giữ nguyên `figure_group` từ Scene 01 (Ox, Oy, Oz, A, B, AB, M, labels)
  - additions:
    - `angle_arc xOy` — cung nhỏ giữa Ox và Oy, màu `COLOR_EQUAL_1`, `radius=0.45`
    - `angle_arc yOz` — cung nhỏ giữa Oy và Oz, màu `COLOR_EQUAL_2`, `radius=0.55`
    - `angle_arc xOz` — cung lớn giữa Ox và Oz (cung tổng), màu `COLOR_EQUAL_3`, `radius=0.75`

- **narration**: |
    Dấu hiệu hai.
    Nếu tổng số đo hai góc x Oy và y Oz
    bằng số đo góc x Oz
    thì tia Oy nằm giữa hai tia Ox và Oz.
    Trên hình, góc x Oy cộng góc y Oz
    bằng góc x Oz.

- **animations**:
  - `Write(block_heading)` — đầu scene
  - `FadeIn(body_lines[0])` + `Write(formula_sum)` — phát biểu và công thức
  - `Create(angle_arc xOy)` — màu `COLOR_EQUAL_1`
  - `Create(angle_arc yOz)` — màu `COLOR_EQUAL_2`
  - `Create(angle_arc xOz)` — màu `COLOR_EQUAL_3` (cung lớn)
  - `Indicate(angle_arc xOy, angle_arc yOz, color=COLOR_EQUAL_1)` — nhấn hai góc nhỏ
  - `Indicate(angle_arc xOz, color=COLOR_EQUAL_3)` — nhấn góc tổng
  - `Wait(1)`

- **cleanup**:
  - `FadeOut(block_heading, body_group, formula_sum, angle_arcs)`
  - **Giữ** base figure (Ox, Oy, Oz, A, B, AB, M, labels) cho Scene 03

---

## Scene 03 — Dấu hiệu 3

- **method**: `scene03_dauHieu3`
- **block_type**: `dinh_li`
- **duration**: 50–60s
- **heading**: "Dấu hiệu 3"

- **body_lines**:
  - `"Trên cùng một nửa mặt phẳng bờ chứa tia $Ox$, nếu $x\widehat{O}y < x\widehat{O}z$ thì tia $Oy$ nằm giữa hai tia $Ox$ và $Oz$."`

- **formulas**:
  - `formula_compare`: `r"x\widehat{O}y < x\widehat{O}z"`

- **figure**:
  - type: `geometry`
  - panel: `right`
  - width_ratio: `0.45`
  - sgk_ref: Hình 33 (tái dùng)
  - build:
    - `reuse` — giữ nguyên base figure từ Scene 02 (Ox, Oy, Oz, A, B, AB, M, labels)
  - additions:
    - `half_plane_shade` — nửa mặt phẳng bờ chứa Ox (phía trên đường Ox), `fill_opacity=0.12`, màu `COLOR_EQUAL_1`
    - `angle_arc xOy` — cung nhỏ, màu `COLOR_EQUAL_1`, `radius=0.45`
    - `angle_arc xOz` — cung lớn hơn xOy, màu `COLOR_EQUAL_3`, `radius=0.75`

- **narration**: |
    Dấu hiệu ba.
    Trên cùng một nửa mặt phẳng bờ chứa tia Ox,
    nếu góc x Oy nhỏ hơn góc x Oz
    thì tia Oy nằm giữa hai tia Ox và Oz.
    Trên hình, góc x Oy nhỏ hơn góc x Oz
    nên Oy nằm giữa Ox và Oz.

- **animations**:
  - `Write(block_heading)` — đầu scene
  - `FadeIn(half_plane_shade)` — tô nửa mặt phẳng
  - `FadeIn(body_lines[0])` — phát biểu dấu hiệu
  - `Create(angle_arc xOy)` + `Create(angle_arc xOz)` — hai cung so sánh
  - `Indicate(angle_arc xOy, angle_arc xOz)` — so sánh kích thước
  - `Write(formula_compare)` — bất phương trình
  - `Indicate(ray Oy, color=COLOR_HIGHLIGHT)` — kết luận Oy nằm giữa
  - `Wait(1)`

- **cleanup**:
  - `FadeOut(block_heading, body_group, formula_compare, half_plane_shade, angle_arcs)`
  - `FadeOut(figure_group)` — **toàn bộ** Hình 33 (Scene 04 dựng Hình 34 mới)

---

## Scene 04 — Dấu hiệu 4

- **method**: `scene04_dauHieu4`
- **block_type**: `dinh_li`
- **duration**: 55–65s
- **heading**: "Dấu hiệu 4"

- **body_lines**:
  - `"Sau đây ta thừa nhận ba dấu hiệu mới để nhận biết một tia nằm giữa hai tia khác."`
  - `"Cho bốn tia $Ox$, $Oy$, $Oz$, $Ot$ cùng nằm trên một nửa mặt phẳng bờ chứa tia $Ox$."`
  - `"Nếu $x\widehat{O}y < x\widehat{O}z < x\widehat{O}t$ thì tia $Oz$ nằm giữa hai tia $Oy$ và $Ot$."`

- **formulas**:
  - `formula_chain`: `r"x\widehat{O}y < x\widehat{O}z < x\widehat{O}t"`

- **figure**:
  - type: `geometry`
  - panel: `right`
  - width_ratio: `0.45`
  - sgk_ref: Hình 34
  - build:
    - `dot(O)` — gốc `O = ORIGIN`
    - `ray Ox` — góc phương vị `0°`, độ dài `3.0`
    - `ray Oy` — góc phương vị `~25°`
    - `ray Oz` — góc phương vị `~55°`
    - `ray Ot` — góc phương vị `~100°`
    - `half_plane_shade` — nửa mặt phẳng bờ chứa Ox, `fill_opacity=0.12`, màu `COLOR_EQUAL_1`
    - `labels` — `O`, `x`, `y`, `z`, `t` (buff=0.15)

- **narration**: |
    Dấu hiệu bốn.
    Sau đây ta thừa nhận ba dấu hiệu mới.
    Cho bốn tia Ox, Oy, Oz, Ot
    cùng nằm trên một nửa mặt phẳng bờ chứa tia Ox.
    Nếu góc x Oy nhỏ hơn góc x Oz,
    và góc x Oz nhỏ hơn góc x Ot,
    thì tia Oz nằm giữa hai tia Oy và Ot.
    Trên hình, các góc tăng dần theo thứ tự y, z, t.

- **animations**:
  - `Write(block_heading)` — đầu scene
  - `FadeIn(body_lines[0])` — câu dẫn thừa nhận
  - `Create(ray Ox)` + `FadeIn(half_plane_shade)` — tia gốc và nửa mặt phẳng
  - `Create(ray Oy)` → `Create(ray Oz)` → `Create(ray Ot)` — lần lượt theo thứ tự góc tăng
  - `FadeIn(body_lines[1..2])` — phát biểu dấu hiệu
  - `Write(formula_chain)` — chuỗi bất phương trình
  - `Indicate(ray Oy, ray Oz, ray Ot)` — nhấn thứ tự góc
  - `Indicate(ray Oz, color=COLOR_HIGHLIGHT)` — kết luận Oz nằm giữa Oy và Ot
  - `Wait(1)`

- **cleanup**: `FadeOut(block_heading, body_group, formula_chain, figure_group)`

---

## Scene 05 — Dấu hiệu 5

- **method**: `scene05_dauHieu5`
- **block_type**: `dinh_li`
- **duration**: 55–65s
- **heading**: "Dấu hiệu 5"

- **body_lines**:
  - `"Cho năm tia $Ox$, $Om$, $Ot$, $On$, $Oy$ cùng nằm trên một nửa mặt phẳng bờ chứa tia $Ox$."`
  - `"Nếu tia $Ot$ nằm giữa hai tia $Ox$ và $Oy$;"`
  - `"tia $Om$ nằm giữa hai tia $Ot$ và $Ox$;"`
  - `"tia $On$ nằm giữa hai tia $Ot$ và $Oy$ thì tia $Ot$ nằm giữa hai tia $Om$ và $On$."`

- **figure**:
  - type: `geometry`
  - panel: `right`
  - width_ratio: `0.45`
  - sgk_ref: Hình 35
  - build:
    - `dot(O)` — gốc `O = ORIGIN`
    - `ray Ox` — góc phương vị `0°`, độ dài `3.0`
    - `ray Om` — góc phương vị `~20°`
    - `ray Ot` — góc phương vị `~45°`
    - `ray On` — góc phương vị `~70°`
    - `ray Oy` — góc phương vị `~90°`
    - `labels` — `O`, `x`, `m`, `t`, `n`, `y` (buff=0.15)

- **narration**: |
    Dấu hiệu năm.
    Cho năm tia Ox, Om, Ot, On, Oy
    cùng nằm trên một nửa mặt phẳng bờ chứa tia Ox.
    Ot nằm giữa Ox và Oy;
    Om nằm giữa Ot và Ox;
    On nằm giữa Ot và Oy.
    Khi đó tia Ot nằm giữa hai tia Om và On.
    Trên hình, Ot nằm giữa Om và On.

- **animations**:
  - `Write(block_heading)` — đầu scene
  - `Create(ray Ox)` — tia gốc
  - `Create(ray Om)` → `Create(ray Ot)` → `Create(ray On)` → `Create(ray Oy)` — lần lượt CCW
  - `FadeIn(body_lines[0..3])` — phát biểu từng quan hệ
  - `Indicate(ray Ot, ray Ox, ray Oy)` — Ot giữa Ox và Oy
  - `Indicate(ray Om, ray Ot, ray Ox)` — Om giữa Ot và Ox
  - `Indicate(ray On, ray Ot, ray Oy)` — On giữa Ot và Oy
  - `Indicate(ray Ot, ray Om, ray On, color=COLOR_HIGHLIGHT)` — kết luận Ot giữa Om và On
  - `Wait(1)`

- **cleanup**: `FadeOut(block_heading, body_group, figure_group)`

---

## Scene 06 — Dấu hiệu 6 — a)

- **method**: `scene06_dauHieu6a`
- **block_type**: `dinh_li`
- **duration**: 50–60s
- **heading**: "Dấu hiệu 6 — a)"

- **body_lines**:
  - `"Cho hai góc kề $A\widehat{O}B$ và $A\widehat{O}C$."`
  - `"Nếu $A\widehat{O}B + A\widehat{O}C \leq 180^\circ$ thì tia $OA$ nằm giữa hai tia $OB$ và $OC$."`

- **formulas**:
  - `formula_leq`: `r"A\widehat{O}B + A\widehat{O}C \leq 180^\circ"`

- **figure**:
  - type: `geometry`
  - panel: `right`
  - width_ratio: `0.45`
  - sgk_ref: Hình 36
  - build:
    - `dot(O)` — gốc `O = ORIGIN`
    - `ray OA` — góc phương vị `0°`, độ dài `3.0`
    - `ray OB` — góc phương vị `~40°`
    - `ray OC` — góc phương vị `~320°` (tức `-40°`, góc kề hai phía OA)
    - `angle_arc AOB` — cung nhỏ, màu `COLOR_EQUAL_1`, `radius=0.5`
    - `angle_arc AOC` — cung nhỏ, màu `COLOR_EQUAL_2`, `radius=0.55`
    - `labels` — `O`, `A`, `B`, `C` (buff=0.15)

- **narration**: |
    Dấu hiệu sáu, phần a.
    Cho hai góc kề A O B và A O C.
    Nếu tổng hai góc không quá 180 độ
    thì tia O A nằm giữa hai tia O B và O C.
    Trên hình, hai góc kề có tổng không quá 180 độ,
    nên O A nằm giữa O B và O C.

- **animations**:
  - `Write(block_heading)` — đầu scene
  - `Create(ray OA)` — tia ở giữa
  - `Create(ray OB)` + `Create(ray OC)` — hai tia biên
  - `FadeIn(body_lines[0..1])` — phát biểu
  - `Create(angle_arc AOB)` + `Create(angle_arc AOC)` — hai cung nhỏ
  - `Write(formula_leq)` — công thức tổng
  - `Indicate(angle_arc AOB, angle_arc AOC)` — nhấn hai góc kề
  - `Indicate(ray OA, color=COLOR_HIGHLIGHT)` — OA nằm giữa OB và OC
  - `Wait(1)`

- **cleanup**: `FadeOut(block_heading, body_group, formula_leq, figure_group)`

---

## Scene 07 — Dấu hiệu 6 — b)

- **method**: `scene07_dauHieu6b`
- **block_type**: `dinh_li`
- **duration**: 55–65s
- **heading**: "Dấu hiệu 6 — b)"

- **body_lines**:
  - `"Nếu $A\widehat{O}B + A\widehat{O}C > 180^\circ$ thì tia $OA$ không nằm giữa hai tia $OB$ và $OC$."`
  - `"Tia đối $OA'$ của tia $OA$ nằm giữa hai tia $OB$ và $OC$."`

- **formulas**:
  - `formula_gt`: `r"A\widehat{O}B + A\widehat{O}C > 180^\circ"`

- **figure**:
  - type: `geometry`
  - panel: `right`
  - width_ratio: `0.45`
  - sgk_ref: Hình 37
  - build:
    - `dot(O)` — gốc `O = ORIGIN`
    - `ray OA` — góc phương vị `0°`, độ dài `3.0`
    - `ray OA_prime` — góc phương vị `180°` (tia đối của OA), vẽ sau khi nêu kết luận
    - `ray OB` — góc phương vị `~135°`
    - `ray OC` — góc phương vị `~225°`
    - `angle_arc AOB` — cung lớn (góc > 90°), màu `COLOR_EQUAL_1`, `radius=0.55`
    - `angle_arc AOC` — cung lớn, màu `COLOR_EQUAL_2`, `radius=0.6`
    - `labels` — `O`, `A`, `A'`, `B`, `C` (buff=0.15)

- **narration**: |
    Dấu hiệu sáu, phần b.
    Nếu tổng hai góc A O B và A O C
    lớn hơn 180 độ
    thì tia O A không nằm giữa hai tia O B và O C.
    Tia đối O A phẩy của tia O A
    nằm giữa hai tia O B và O C.
    Trên hình, tổng hai góc lớn hơn 180 độ;
    tia đối O A phẩy nằm giữa O B và O C.

- **animations**:
  - `Write(block_heading)` — đầu scene
  - `Create(ray OA)` + `Create(ray OB)` + `Create(ray OC)` — ba tia
  - `Create(angle_arc AOB)` + `Create(angle_arc AOC)` — hai cung lớn
  - `FadeIn(body_lines[0])` + `Write(formula_gt)` — phát biểu và công thức
  - `Indicate(ray OA, color=COLOR_DEFAULT)` — OA không nằm giữa (mờ hoặc gạch nhẹ)
  - `Create(ray OA_prime)` + `FadeIn(body_lines[1])` — tia đối
  - `Indicate(ray OA_prime, color=COLOR_HIGHLIGHT)` — OA' nằm giữa OB và OC
  - `Wait(1.5)`

- **cleanup**:
  - `FadeOut(block_heading, body_group, formula_gt, figure_group)`
  - `FadeOut(section_heading)` + `FadeOut(lesson_title)` — kết thúc bài

---

## Ghi chú dựng hình

| Tham số | Giá trị |
|---------|---------|
| Gốc `O` | `ORIGIN` trong hệ cục bộ trước `place_figure()` |
| Register điểm | **Sau** `place_figure()` qua `dot.get_center()` — không hardcode tọa độ world |
| Độ dài tia | `3.0` (Hình 33–37) |
| Khoảng cách A, B trên Ox, Oz | `dist=2.5` (Hình 33) |
| Góc Hình 33 | Ox `0°`, Oy `~40°`, Oz `~95°` |
| Góc Hình 34 | Ox `0°`, Oy `~25°`, Oz `~55°`, Ot `~100°` |
| Góc Hình 35 | Ox `0°`, Om `~20°`, Ot `~45°`, On `~70°`, Oy `~90°` |
| Góc Hình 36 | OA `0°`, OB `~40°`, OC `~320°` (−40°) |
| Góc Hình 37 | OA `0°`, OA' `180°`, OB `~135°`, OC `~225°` |
| Màu tia / cạnh | `COLOR_DEFAULT` |
| Màu góc nhỏ (dấu hiệu 2) | `COLOR_EQUAL_1`, `COLOR_EQUAL_2`, `COLOR_EQUAL_3` (cung tổng) |
| Màu điểm / tia kết luận | `COLOR_HIGHLIGHT` (M, Oy, Oz, Ot, OA, OA') |
| Nửa mặt phẳng | `fill_opacity=0.12`, màu `COLOR_EQUAL_1` |
| Panel | `right`, `width_ratio: 0.45` cho mọi scene có hình |

**Quyết định kỹ thuật:**
- Hình 33 tái dùng Scene 01 → 02 → 03; Scene 03 cleanup **toàn bộ** `figure_group` trước khi sang Hình 34.
- Điểm M (Scene 01): giao `Oy ∩ AB` — tính toán, không hardcode.
- Scene 07: vẽ `ray OA'` **sau** khi nêu "OA không nằm giữa" — tránh lộ kết luận sớm.
- Voiceover: không đọc ký hiệu `∠`, `°`, `\widehat{}` — dùng "góc x Oy", "180 độ", "tia đối O A phẩy".

**Lifecycle figure:**

| Scene | Hình SGK | Hành động |
|-------|----------|-----------|
| 01 | Hình 33 | Build mới |
| 02 | Hình 33 | Reuse + thêm angle arcs |
| 03 | Hình 33 | Reuse + half-plane + angle arcs → FadeOut all |
| 04 | Hình 34 | Build mới |
| 05 | Hình 35 | Build mới |
| 06 | Hình 36 | Build mới |
| 07 | Hình 37 | Build mới → FadeOut all + kết thúc bài |

---

## Checklist trước khi build (Step 2)

- [x] Mỗi scene có `method`, `block_type`, `heading`, `narration`, `animations`, `cleanup`
- [x] Mỗi `figure.type: geometry` có trích dẫn Hình SGK (33–37)
- [x] Không suy diễn figure type — mọi scene nội dung đều có hình SGK
- [x] Không `layout:` block (chỉ cần khi `figure.type: none` — chỉ Scene 00)
- [x] Không `GT:`, `KL:`, `proof_accumulator`, `ProofLine`
- [x] Scene 07 cleanup kết thúc bài (`FadeOut(section_heading)` + `FadeOut(lesson_title)`)
- [x] Narration không ký hiệu (∠, °); câu ≤ 20 từ; có "chẳng hạn/trên hình" khi có figure
- [x] `cleanup` ghi rõ giữ/tái dùng figure (Scene 01→03) và FadeOut toàn bộ trước Scene 04
