# Scene Spec Lý Thuyết: BÀI 3. TỨ GIÁC NỘI TIẾP

## Thông tin chung

- **lesson_title**: BÀI 3. TỨ GIÁC NỘI TIẾP
- **lesson_type**: theory
- **subject**: geometry
- **section_heading**: I. TÓM TẮT LÝ THUYẾT
- **total_scenes**: 4
- **estimated_duration**: 5–7 phút

---

## Scene 00 — Intro

- **method**: `scene00_intro`
- **duration**: 25s
- **content**: Tiêu đề bài + heading phần "I. TÓM TẮT LÝ THUYẾT"

- **narration**: |
    Bài ba. Tứ giác nội tiếp.
    Phần một. Tóm tắt lý thuyết.

- **animations**:
  - `Write(lesson_title)` — `Tex(r"\textbf{BÀI 3. TỨ GIÁC NỘI TIẾP}")`, `font_size=36`, `to_edge(UP, buff=0.4)`
  - `FadeIn(section_heading)` — `Tex(r"\textbf{I. TÓM TẮT LÝ THUYẾT}")`, `font_size=28`, dưới `lesson_title`, `buff=0.35`
  - `Wait(1.5)` — giữ tiêu đề trước khi chuyển scene

- **cleanup**:
  - `FadeOut(section_heading)`
  - Giữ `lesson_title` ở `to_edge(UP)` cho các scene sau (có thể `scale(0.9)` nếu cần chỗ cho heading mục)

---

## Scene 01 — Định nghĩa

- **method**: `scene01_dinhNghia`
- **block_type**: `dinh_nghia`
- **duration**: 55–65s
- **heading**: "1. Định nghĩa"

- **body_lines**:
  - `"Tứ giác có bốn đỉnh nằm trên một đường tròn được gọi là"`
  - `r"\textbf{tứ giác nội tiếp đường tròn}"`
  - `r"(hoặc đơn giản là \textbf{tứ giác nội tiếp})"`
  - `"và đường tròn được gọi là"`
  - `r"\textbf{đường tròn ngoại tiếp tứ giác}."`

- **terms_bold**: [tứ giác nội tiếp đường tròn, tứ giác nội tiếp, đường tròn ngoại tiếp tứ giác]

- **figure**:
  - type: `geometry`
  - panel: `right`
  - width_ratio: `0.45`
  - build:
    - `circle(O, R=2.2)` — tâm `O = ORIGIN`, màu `COLOR_CIRCLE`, `stroke_width=2.5`
    - `dot(O)` — nhãn `O` phía dưới tâm, `font_size=24`
    - `points on circle` — góc phương vị (độ, CCW từ phải): `A=70°`, `B=160°`, `C=250°`, `D=340°` (tứ giác lồi, không đều)
    - `quad ABCD` — cạnh `AB`, `BC`, `CD`, `DA`, màu `COLOR_DEFAULT`, `stroke_width=2`
    - `dots A, B, C, D` — `radius=0.06`, màu `COLOR_DEFAULT`
    - `labels` — `A` (góc trên-trái), `B` (góc trên-phải), `C` (góc dưới-phải), `D` (góc dưới-trái), `buff=0.15`
    - *(không vẽ góc arc ở scene này — chỉ nhấn bốn đỉnh trên đường tròn)*

- **narration**: |
    Định nghĩa.
    Tứ giác có bốn đỉnh nằm trên một đường tròn
    được gọi là tứ giác nội tiếp đường tròn,
    hoặc đơn giản là tứ giác nội tiếp.
    Đường tròn đó được gọi là đường tròn ngoại tiếp tứ giác.
    Chẳng hạn, trên hình vẽ, tứ giác A B C D
    có bốn đỉnh A, B, C, D đều nằm trên đường tròn tâm O.

- **animations**:
  - `Write(block_heading)` — đầu scene, `to_corner(UL, buff=0.5)`
  - `FadeIn(body_lines[0])` — đồng thời `Create(circle)` + `FadeIn(dot O)` + `Write(label O)`
  - `FadeIn(body_lines[1..2])` — đồng thời `Create(dots A,B,C,D)` lần lượt trên đường tròn (0.4s mỗi điểm)
  - `FadeIn(body_lines[3..4])` — đồng thời `Create(quad ABCD)` + `Write(labels A,B,C,D)`
  - `Indicate(dots A,B,C,D, scale_factor=1.2)` — nhấn bốn đỉnh trên đường tròn khi đọc "bốn đỉnh... nằm trên đường tròn"
  - `Indicate(terms_bold_mobs, scale_factor=1.15)` — cuối scene, lần lượt từng thuật ngữ in đậm

- **cleanup**:
  - `FadeOut(block_heading, body_group)`
  - **Giữ** `figure_group` (circle + quad ABCD + labels) cho Scene 02 tái dùng

---

## Scene 02 — Định lí

- **method**: `scene02_dinhLi`
- **block_type**: `dinh_li`
- **duration**: 60–75s
- **heading**: "2. Định lí"

- **body_lines**:
  - `"Trong một tứ giác nội tiếp, tổng số đo hai góc đối nhau bằng 180°."`
  - `"Trên hình vẽ, tứ giác $ABCD$ nội tiếp $(O)$ nên"`

- **formulas**:
  - `formula_main`: `r"\widehat{A} + \widehat{C} = \widehat{B} + \widehat{D} = 180^\circ"`

- **figure**:
  - type: `geometry`
  - panel: `right`
  - width_ratio: `0.45`
  - build:
    - `reuse` — giữ nguyên `figure_group` từ Scene 01 (circle O, quad ABCD, labels)
    - `angle_arc A` — `AngleMarker` tại đỉnh A (cạnh DA, AB), màu `COLOR_EQUAL_1`, `radius=0.35`
    - `angle_arc C` — tại đỉnh C (cạnh BC, CD), màu `COLOR_EQUAL_1`, `radius=0.35`
    - `angle_arc B` — tại đỉnh B (cạnh AB, BC), màu `COLOR_EQUAL_2`, `radius=0.35`
    - `angle_arc D` — tại đỉnh D (cạnh CD, DA), màu `COLOR_EQUAL_2`, `radius=0.35`
    - `label angles` — ký hiệu góc nhỏ cạnh mỗi arc: `\widehat{A}`, `\widehat{B}`, `\widehat{C}`, `\widehat{D}`
  - additions (theo thứ tự animation):
    - Cặp đối 1: highlight `angle_A` + `angle_C` → hiện `formula_part_1`: `r"\widehat{A} + \widehat{C} = 180^\circ"` dưới hình hoặc cạnh công thức chính
    - Cặp đối 2: highlight `angle_B` + `angle_D` → hiện `formula_part_2`: `r"\widehat{B} + \widehat{D} = 180^\circ"`

- **narration**: |
    Định lí.
    Trong một tứ giác nội tiếp,
    tổng số đo hai góc đối nhau bằng 180 độ.
    Trên hình vẽ, tứ giác A B C D nội tiếp đường tròn tâm O
    nên góc A cộng góc C bằng 180 độ.
    Tương tự, góc B cộng góc D cũng bằng 180 độ.

- **animations**:
  - `Write(block_heading)` — đầu scene
  - `FadeIn(body_lines[0])` — đồng thời `Write(formula_main)` dưới body
  - `FadeIn(body_lines[1])` — đồng thời `Create(angle_arc A, angle_arc C)` màu `COLOR_EQUAL_1`
  - `Indicate(angle_arc A, angle_arc C, color=COLOR_EQUAL_1)` — khi đọc "góc A cộng góc C"
  - `Write(formula_part_1)` hoặc `Indicate` phần `\widehat{A}+\widehat{C}` trong `formula_main`
  - `Create(angle_arc B, angle_arc D)` màu `COLOR_EQUAL_2`
  - `Indicate(angle_arc B, angle_arc D, color=COLOR_EQUAL_2)` — khi đọc "góc B cộng góc D"
  - `Write(formula_part_2)` hoặc `Indicate` phần `\widehat{B}+\widehat{D}` trong `formula_main`
  - `Wait(1)` — giữ công thức và hình trướ khi cleanup

- **cleanup**:
  - `FadeOut(block_heading, body_group, formula_main, formula_part_1, formula_part_2)`
  - `FadeOut(angle_arcs, angle_labels)` — chỉ góc và nhãn góc
  - `FadeOut(figure_group)` — circle + quad + labels (scene sau dùng hình mới)

---

## Scene 03 — Nhận xét

- **method**: `scene03_nhanXet`
- **block_type**: `nhan_xet`
- **duration**: 55–70s
- **heading**: "3. Nhận xét"

- **body_lines**:
  - `"Hình chữ nhật và hình vuông là các tứ giác nội tiếp."`
  - `"Đường tròn ngoại tiếp của chúng có tâm là giao điểm của hai đường chéo"`
  - `"và bán kính bằng một nửa độ dài đường chéo."`

- **terms_bold**: [giao điểm của hai đường chéo, một nửa độ dài đường chéo]

- **figure**:
  - type: `dual_geometry`
  - panel: `right`
  - width_ratio: `0.50`
  - figure_left:
    - label: `"Hình chữ nhật"`
    - build:
      - `rect ABCD` — tâm panel trái, `width=2.8`, `height=1.6` (tỷ lệ 7:4), không xoay
      - `dots A, B, C, D` — đỉnh theo chiều kim đồng hồ từ góc trên-trái
      - `labels A(UL), B(UR), C(DR), D(DL)`
      - `diagonal AC` — nét đứt hoặc `COLOR_AUX_LINE`, `stroke_width=2`
      - `diagonal BD` — tương tự
      - `dot O` — giao `AC ∩ BD` (trung điểm hai đường chéo)
      - `label O` — tại giao điểm
      - `circle(O, R=|OA|)` — `COLOR_CIRCLE`, đi qua cả bốn đỉnh (R = nửa đường chéo)
  - figure_right:
    - label: `"Hình vuông"`
    - build:
      - `square EFGH` — cạnh `1.8`, tâm panel phải, xoay 0°
      - `dots E, F, G, H` — đỉnh theo chiều kim đồng hồ
      - `labels E(UL), F(UR), G(DR), H(DL)`
      - `diagonal EG` — `COLOR_AUX_LINE`
      - `diagonal FH` — `COLOR_AUX_LINE`
      - `dot O'` — giao hai đường chéo (trung điểm)
      - `label O'` — hoặc cùng ký hiệu `O` nếu không gây nhầm giữa hai panel
      - `circle(O', R=|OE|)` — `COLOR_CIRCLE`, đi qua bốn đỉnh

- **narration**: |
    Nhận xét.
    Hình chữ nhật và hình vuông là các tứ giác nội tiếp.
    Đường tròn ngoại tiếp của chúng
    có tâm là giao điểm của hai đường chéo.
    Bán kính bằng một nửa độ dài đường chéo.
    Trên hình bên trái, hai đường chéo của hình chữ nhật
    cắt nhau tại O, và đường tròn tâm O đi qua bốn đỉnh.
    Tương tự với hình vuông bên phải.

- **animations**:
  - `Write(block_heading)` — đầu scene
  - `FadeIn(body_lines[0])` — đồng thời `Create(rect ABCD)` + `Create(square EFGH)` + `Write(figure_left.label, figure_right.label)`
  - `FadeIn(body_lines[1])` — đồng thời `Create(diagonals AC, BD)` + `Create(diagonals EG, FH)`
  - `FadeIn(dot O, dot O')` + `Indicate(intersection_points)` — khi đọc "giao điểm hai đường chéo"
  - `FadeIn(body_lines[2])` — đồng thời `Create(circle left)` + `Create(circle right)` (radius = nửa đường chéo)
  - `Indicate(diagonal_AC, diagonal_BD)` trên HCN — nhấn đường chéo khi đọc "một nửa độ dài đường chéo"
  - `Indicate(terms_bold_mobs)` — cuối scene
  - `Wait(1.5)`

- **cleanup**:
  - `FadeOut(block_heading, body_group, figure_left_group, figure_right_group, dual_panel_labels)`
  - `FadeOut(lesson_title)` — kết thúc bài (hoặc giữ nếu có scene tổng kết sau)

---

## Ghi chú dựng hình

| Tham số | Giá trị |
|---------|---------|
| `O` (định lí) | `ORIGIN` |
| `R` đường tròn chính | `2.2` |
| Góc phương vị A,B,C,D | `70°, 160°, 250°, 340°` — tứ giác lồi không đều |
| Màu đường tròn | `COLOR_CIRCLE` |
| Màu cặp góc đối 1 (A,C) | `COLOR_EQUAL_1` |
| Màu cặp góc đối 2 (B,D) | `COLOR_EQUAL_2` |
| Màu đường chéo (nhận xét) | `COLOR_AUX_LINE` |
| Panel HCN (trái) | `shift LEFT * 2.8` trong `DualFigurePanel` |
| Panel HV (phải) | `shift RIGHT * 2.8` |
| Thứ tự lifecycle figure | Scene 01 build → Scene 02 reuse + góc → Scene 03 figure mới (dual), không reuse |

**Quyết định kỹ thuật:**
- Scene 01–02 dùng **cùng một** tứ giác ABCD nội tiếp (O) để người xem liên kết định nghĩa → định lí.
- Scene 03 **không** tái dùng hình Scene 01; dùng `dual_geometry` đúng SGK (HCN + HV cạnh nhau).
- Không animate di chuyển đỉnh trên đường tròn (tùy chọn mở rộng sau) — spec giữ đơn giản, chỉ `Indicate` góc đối.
- Voiceover: không đọc ký hiệu `(O)`, `°`, `\widehat{}` — dùng "đường tròn tâm O", "180 độ", "góc A".
