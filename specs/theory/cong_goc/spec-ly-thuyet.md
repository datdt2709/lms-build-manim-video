# Scene Spec Lý Thuyết: CHUYÊN ĐỀ 2. CỘNG SỐ ĐO CÁC GÓC

## Thông tin chung

- **lesson_title**: CHUYÊN ĐỀ 2. CỘNG SỐ ĐO CÁC GÓC
- **lesson_type**: theory
- **subject**: geometry
- **section_heading**: A. KIẾN THỨC CẦN NHỚ
- **total_scenes**: 7
- **estimated_duration**: 8–10 phút

> **Layout 3 tầng:** `lesson_title` (tầng 0) → `section_heading` persistent scenes 01–06 (tầng 1) → `block_heading` đổi mỗi scene, neo dưới `section_heading` (tầng 2).

> **Ghi chú nguồn:** Ảnh SGK Chuyên đề 2 — phần **A. Kiến thức cần nhớ** (Cộng số đo các góc). Trang có 6 mục đánh số; 3 hình minh họa SGK: **Hình 14** (tiên đề cộng góc), **Hình 15** (góc kề bù), **Hình 16** (so sánh góc trên nửa mặt phẳng). Mục 1, 2, 5 không có hình trên SGK → `figure.type: none`.

---

## Scene 00 — Intro

- **method**: `scene00_intro`
- **duration**: 20–25s
- **content**: Tiêu đề bài + heading phần "A. KIẾN THỨC CẦN NHỚ"

- **figure**:
  - type: `none`
  - panel: `none`

- **narration**: |
    Chuyên đề hai. Cộng số đo các góc.
    Phần A. Kiến thức cần nhớ.
    Bài học trình bày số đo góc, các loại góc,
    tiên đề cộng góc và quan hệ giữa hai góc.
    Ta cũng học cách dựng và so sánh góc
    trên nửa mặt phẳng.

- **animations**:
  - `Write(lesson_title)` — `Tex(r"\textbf{CHUYÊN ĐỀ 2. CỘNG SỐ ĐO CÁC GÓC}")`, `font_size=36`, `to_edge(UP, buff=0.4)`
  - `FadeIn(section_heading)` — `Tex(r"\textbf{A. KIẾN THỨC CẦN NHỚ}")`, `font_size=28`, dưới `lesson_title`, `buff=0.35`
  - `Wait(1.5)` — giữ tiêu đề trước khi chuyển scene

- **cleanup**: giữ `lesson_title` + `section_heading` cho scenes 01–06

---

## Scene 01 — Số đo góc

- **method**: `scene01_soDoGoc`
- **block_type**: `dinh_nghia`
- **duration**: 45–55s
- **heading**: "1. Số đo góc"

- **body_lines**:
  - `"Mọi góc đều có số đo."`
  - `"Góc \textbf{bẹt} có số đo bằng $180^\circ$."`
  - `"Không có góc nào có số đo lớn hơn $180^\circ$."`

- **terms_bold**: [góc bẹt]

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
    - group: [body_lines[0], body_lines[1], body_lines[2]]

- **narration**: |
    Định nghĩa.
    Mọi góc đều có số đo.
    Góc bẹt có số đo bằng 180 độ.
    Không có góc nào có số đo lớn hơn 180 độ.

- **animations**:
  - `Write(block_heading)` — đầu scene, neo dưới `section_heading`, `buff=0.25`
  - `FadeIn(body_lines[0])` — câu đầu
  - `FadeIn(body_lines[1])` — góc bẹt
  - `FadeIn(body_lines[2])` — giới hạn 180 độ
  - `Indicate(terms_bold_mobs, scale_factor=1.15)` — nhấn thuật ngữ góc bẹt
  - `Wait(1)`

- **cleanup**: `FadeOut(block_heading, body_group)`

---

## Scene 02 — Các loại góc

- **method**: `scene02_cacLoaiGoc`
- **block_type**: `dinh_nghia`
- **duration**: 50–60s
- **heading**: "2. Các loại góc"

- **body_lines**:
  - `label_vuong`: `r"- \textbf{Góc vuông:} số đo bằng $90^\circ$"` *(list item)*
  - `label_nhon`: `r"- \textbf{Góc nhọn:} số đo nhỏ hơn góc vuông"` *(list item)*
  - `label_tu`: `r"- \textbf{Góc tù:} số đo lớn hơn góc vuông nhưng nhỏ hơn góc bẹt"` *(list item)*

- **formulas**:
  - `formula_vuong`: `r"$\bullet$ $90^\circ$"` *(sub-item, Tex)*
  - `formula_nhon`: `r"$\bullet$ $< 90^\circ$"` *(sub-item, Tex)*
  - `formula_tu`: `r"$\bullet$ $90^\circ < \ldots < 180^\circ$"` *(sub-item, Tex)*

- **terms_bold**: [góc vuông, góc nhọn, góc tù]

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
    - group: [label_vuong, formula_vuong]
    - group: [label_nhon, formula_nhon]
    - group: [label_tu, formula_tu]

- **narration**: |
    Định nghĩa.
    Góc vuông có số đo bằng 90 độ.
    Góc nhọn có số đo nhỏ hơn góc vuông.
    Góc tù có số đo lớn hơn góc vuông
    nhưng nhỏ hơn góc bẹt.

- **animations**:
  - `Write(block_heading)` — đầu scene
  - `FadeIn(label_vuong)` + `Write(formula_vuong)` — góc vuông
  - `Indicate(label_vuong, formula_vuong)` — nhấn góc vuông
  - `FadeIn(label_nhon)` + `Write(formula_nhon)` — góc nhọn
  - `Indicate(label_nhon, formula_nhon)` — nhấn góc nhọn
  - `FadeIn(label_tu)` + `Write(formula_tu)` — góc tù
  - `Indicate(label_tu, formula_tu)` — nhấn góc tù
  - `Wait(1)`

- **cleanup**: `FadeOut(block_heading, body_group, formula_group)`

---

## Scene 03 — Tiên đề cộng góc

- **method**: `scene03_tienDeCongGoc`
- **block_type**: `dinh_li`
- **duration**: 60–70s
- **heading**: "3. Tiên đề cộng góc"

- **body_lines**:
  - `line_forward`: `"Nếu tia $Oy$ nằm giữa hai tia $Ox$ và $Oz$ thì tổng số đo hai góc $x\widehat{O}y$ và $y\widehat{O}z$ bằng số đo góc $x\widehat{O}z$."`
  - `line_converse`: `"Ngược lại, nếu tổng số đo hai góc $x\widehat{O}y$ và $y\widehat{O}z$ bằng số đo góc $x\widehat{O}z$ thì tia $Oy$ nằm giữa hai tia $Ox$ và $Oz$."`

- **formulas**:
  - `formula_forward`: `r"x\widehat{O}y + y\widehat{O}z = x\widehat{O}z"`
  - `formula_converse`: `r"x\widehat{O}y + y\widehat{O}z = x\widehat{O}z"` *(phát biểu ngược — cùng công thức)*

- **terms_bold**: [tia Oy nằm giữa hai tia Ox và Oz]

- **figure**:
  - type: `geometry`
  - panel: `right`
  - width_ratio: `0.45`
  - sgk_ref: Hình 14
  - build:
    - `dot(O)` — gốc `O = ORIGIN`, màu `COLOR_DEFAULT`
    - `ray Ox` — góc phương vị `0°`, độ dài `3.0`, màu `COLOR_DEFAULT`, `stroke_width=2`
    - `ray Oy` — góc phương vị `~30°` (CCW từ Ox), độ dài `3.0`
    - `ray Oz` — góc phương vị `~75°`, độ dài `3.0` *(Oy nằm giữa Ox và Oz, cùng nửa mặt phẳng)*
    - `angle_arc xOy` — cung nhỏ giữa Ox và Oy, màu `COLOR_EQUAL_1`, `radius=0.45`
    - `angle_arc yOz` — cung nhỏ giữa Oy và Oz, màu `COLOR_EQUAL_2`, `radius=0.55`
    - `angle_arc xOz` — cung lớn giữa Ox và Oz (cung tổng), màu `COLOR_EQUAL_3`, `radius=0.75`
    - `labels` — `O` (dưới gốc), `x`, `y`, `z` (cạnh đầu mút tia, `buff=0.15`)

- **narration**: |
    Định lí.
    Nếu tia Oy nằm giữa hai tia Ox và Oz
    thì tổng góc x Oy và góc y Oz
    bằng góc x Oz.
    Chẳng hạn, trên hình vẽ,
    góc x Oy cộng góc y Oz bằng góc x Oz.
    Ngược lại, nếu tổng hai góc x Oy và y Oz
    bằng góc x Oz
    thì tia Oy nằm giữa hai tia Ox và Oz.

- **animations**:
  - `Write(block_heading)` — đầu scene, neo dưới `section_heading`, `buff=0.25`
  - `Create(ray Ox)` — tia gốc
  - `Create(ray Oy)` → `Create(ray Oz)` — hai tia còn lại
  - `FadeIn(line_forward)` + `Write(formula_forward)` — phát biểu xuôi và công thức
  - `Create(angle_arc xOy)` — màu `COLOR_EQUAL_1`
  - `Create(angle_arc yOz)` — màu `COLOR_EQUAL_2`
  - `Indicate(angle_arc xOy, angle_arc yOz, color=COLOR_EQUAL_1)` — nhấn hai góc nhỏ
  - `Create(angle_arc xOz)` — màu `COLOR_EQUAL_3` (cung tổng)
  - `Indicate(angle_arc xOz, color=COLOR_EQUAL_3)` — nhấn góc tổng
  - `FadeIn(line_converse)` + `Write(formula_converse)` — phát biểu ngược
  - `Indicate(ray Oy, color=COLOR_HIGHLIGHT)` — kết luận Oy nằm giữa
  - `Wait(1)`

- **cleanup**:
  - `FadeOut(block_heading, body_group, formula_group, angle_arcs)`
  - `FadeOut(figure_group)` — **toàn bộ** Hình 14 (Scene 04 dựng Hình 15 mới)

---

## Scene 04 — Quan hệ giữa hai góc

- **method**: `scene04_quanHeHaiGoc`
- **block_type**: `dinh_nghia`
- **duration**: 70–80s
- **heading**: "4. Quan hệ giữa hai góc"

- **body_lines**:
  - `label_ke`: `r"- \textbf{Hai góc kề nhau:} chung một cạnh; hai cạnh còn lại nằm ở hai nửa mặt phẳng đối nhau"` *(list item — tham chiếu Hình 14, không vẽ lại)*
  - `label_phu`: `r"- \textbf{Hai góc phụ nhau:} tổng số đo bằng $90^\circ$"` *(list item)*
  - `label_bu`: `r"- \textbf{Hai góc bù nhau:} tổng số đo bằng $180^\circ$"` *(list item)*
  - `label_ke_bu`: `r"- \textbf{Hai góc kề bù:} vừa kề nhau vừa bù nhau"` *(list item)*

- **formulas**:
  - `formula_phu`: `r"$\bullet$ $90^\circ$"` *(sub-item, Tex)*
  - `formula_bu`: `r"$\bullet$ $180^\circ$"` *(sub-item, Tex)*

- **nhan_xet**:
  - **block_type**: `nhan_xet`
  - **heading**: `"(*) Nhận xét"`
  - **body_style**: italic + `COLOR_WARNING`
  - **body_lines**:
    - `nhan_xet_1`: `r"\textit{- Nếu hai góc kề có hai cạnh ngoài là hai tia đối nhau thì chúng bù nhau.}"`
    - `nhan_xet_2`: `r"\textit{- Nếu hai góc kề bù thì tổng bằng $180^\circ$ và hai cạnh ngoài là hai tia đối nhau.}"`

- **terms_bold**: [hai góc kề nhau, hai góc phụ nhau, hai góc bù nhau, hai góc kề bù]

- **figure**:
  - type: `geometry`
  - panel: `right`
  - width_ratio: `0.45`
  - sgk_ref: Hình 15
  - build:
    - `line xz` — đường thẳng ngang qua `O`, điểm `x` (trái), `z` (phải) — hai tia đối nhau, màu `COLOR_DEFAULT`, `stroke_width=2`
    - `dot(O)` — tại giữa đường thẳng, màu `COLOR_DEFAULT`
    - `ray Oy` — từ `O` hướng lên, góc phương vị `~60°`, độ dài `3.0` *(tạo cặp kề bù)*
    - `angle_arc xOy` — cung lớn giữa Ox và Oy, màu `COLOR_EQUAL_1`, `radius=0.55`
    - `angle_arc yOz` — cung nhỏ giữa Oy và Oz, màu `COLOR_EQUAL_2`, `radius=0.45`
    - `labels` — `x` (trái), `O` (dưới gốc), `z` (phải), `y` (cạnh đầu mút Oy, `buff=0.15`)

- **narration**: |
    Định nghĩa.
    Hai góc kề nhau chung một cạnh;
    hai cạnh còn lại nằm ở hai nửa mặt phẳng đối nhau.
    Như đã thấy ở Hình 14, hai góc kề có thể nằm cùng nửa mặt phẳng.
    Hai góc phụ nhau có tổng số đo bằng 90 độ.
    Hai góc bù nhau có tổng số đo bằng 180 độ.
    Hai góc kề bù vừa kề nhau vừa bù nhau.
    Trên hình vẽ, hai góc kề bù có tổng bằng 180 độ.
    Nhận xét.
    Nếu hai góc kề có hai cạnh ngoài là hai tia đối nhau
    thì chúng bù nhau.
    Nếu hai góc kề bù thì tổng bằng 180 độ
    và hai cạnh ngoài là hai tia đối nhau.

- **animations**:
  - `Write(block_heading)` — đầu scene
  - `FadeIn(label_ke)` — định nghĩa góc kề
  - `FadeIn(label_phu)` + `Write(formula_phu)` — góc phụ nhau
  - `Indicate(label_phu, formula_phu)` — nhấn 90 độ
  - `FadeIn(label_bu)` + `Write(formula_bu)` — góc bù nhau
  - `Indicate(label_bu, formula_bu)` — nhấn 180 độ
  - `FadeIn(label_ke_bu)` — góc kề bù
  - `Create(line xz)` + `Write(labels x, O, z)` — đường thẳng và nhãn khi đến kề bù
  - `Create(ray Oy)` + `Create(angle_arc xOy, yOz)` — tia Oy và hai cung
  - `Indicate(angle_arc xOy, angle_arc yOz, color=COLOR_EQUAL_1)` — nhấn tổng 180 độ
  - `Write(nhan_xet heading)` — heading phụ `(*) Nhận xét`, màu `COLOR_WARNING`
  - `FadeIn(nhan_xet_1, color=COLOR_WARNING)` — nhận xét 1
  - `FadeIn(nhan_xet_2, color=COLOR_WARNING)` — nhận xét 2
  - `Wait(1)`

- **cleanup**: `FadeOut(block_heading, body_group, formula_group, nhan_xet_group, figure_group)` — Scene 05 không có hình

---

## Scene 05 — Dựng góc trên nửa mặt phẳng

- **method**: `scene05_dungGoc`
- **block_type**: `dinh_li`
- **duration**: 45–55s
- **heading**: "5. Dựng góc trên nửa mặt phẳng"

- **body_lines**:
  - `"Trên nửa mặt phẳng cho trước có bờ chứa tia $Ox$, tồn tại \textbf{duy nhất} một tia $Oy$ sao cho số đo góc $x\widehat{O}y$ bằng $m^\circ$."`

- **formulas**:
  - `formula_dung`: `r"x\widehat{O}y = m^\circ"`

- **terms_bold**: [duy nhất]

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
    - group: [body_lines[0], formula_dung]

- **narration**: |
    Định lí.
    Trên nửa mặt phẳng cho trước có bờ chứa tia Ox,
    tồn tại duy nhất một tia Oy
    sao cho góc x Oy bằng m độ.

- **animations**:
  - `Write(block_heading)` — đầu scene
  - `FadeIn(body_lines[0])` — phát biểu định lí
  - `Write(formula_dung)` — công thức góc
  - `Indicate(terms_bold_mobs, scale_factor=1.15)` — nhấn từ duy nhất
  - `Wait(1)`

- **cleanup**: `FadeOut(block_heading, body_group, formula_dung)`

---

## Scene 06 — So sánh góc trên nửa mặt phẳng

- **method**: `scene06_soSanhGoc`
- **block_type**: `dinh_li`
- **duration**: 60–70s
- **heading**: "6. So sánh góc trên nửa mặt phẳng"

- **body_lines**:
  - `"Trên nửa mặt phẳng bờ chứa tia $Ox$, nếu $x\widehat{O}y = m^\circ$, $x\widehat{O}z = n^\circ$ và $m < n$ thì tia $Oy$ nằm giữa hai tia $Ox$ và $Oz$."`

- **formulas**:
  - `formula_angles`: `r"x\widehat{O}y = m^\circ,\quad x\widehat{O}z = n^\circ"`
  - `formula_compare`: `r"m < n"`

- **terms_bold**: [tia Oy nằm giữa hai tia Ox và Oz]

- **figure**:
  - type: `geometry`
  - panel: `right`
  - width_ratio: `0.45`
  - sgk_ref: Hình 16
  - build:
    - `dot(O)` — gốc `O = ORIGIN`, màu `COLOR_DEFAULT`
    - `ray Ox` — góc phương vị `0°`, độ dài `3.0`, màu `COLOR_DEFAULT`, `stroke_width=2`
    - `ray Oy` — góc phương vị `~45°`, độ dài `3.0`
    - `ray Oz` — góc phương vị `~80°`, độ dài `3.0`
    - `half_plane_shade` — nửa mặt phẳng bờ chứa Ox (phía trên đường Ox), `fill_opacity=0.12`, màu `COLOR_EQUAL_1`
    - `angle_arc xOy` — cung nhỏ (góc m), màu `COLOR_EQUAL_1`, `radius=0.45`
    - `angle_arc xOz` — cung lớn hơn (góc n), màu `COLOR_EQUAL_3`, `radius=0.75`
    - `labels` — `O` (dưới gốc), `x`, `y`, `z` (cạnh đầu mút tia, `buff=0.15`)
    - `label_m` — nhãn `m^\circ` trên cung xOy *(optional, khớp SGK)*
    - `label_n` — nhãn `n^\circ` trên cung xOz *(optional, khớp SGK)*

- **narration**: |
    Định lí.
    Trên nửa mặt phẳng bờ chứa tia Ox,
    nếu góc x Oy bằng m độ,
    góc x Oz bằng n độ,
    và m nhỏ hơn n
    thì tia Oy nằm giữa hai tia Ox và Oz.
    Trên hình, góc m nhỏ hơn góc n
    nên Oy nằm giữa Ox và Oz.

- **animations**:
  - `Write(block_heading)` — đầu scene, neo dưới `section_heading`, `buff=0.25`
  - `Create(ray Ox)` — tia gốc
  - `FadeIn(half_plane_shade)` — tô nửa mặt phẳng
  - `Create(ray Oy)` + `Create(angle_arc xOy)` + `Write(label_m)` — góc m
  - `Create(ray Oz)` + `Create(angle_arc xOz)` + `Write(label_n)` — góc n
  - `FadeIn(body_lines[0])` — phát biểu định lí
  - `Write(formula_angles)` + `Write(formula_compare)` — công thức góc và so sánh
  - `Indicate(angle_arc xOy, angle_arc xOz)` — so sánh kích thước hai cung
  - `Indicate(ray Oy, color=COLOR_HIGHLIGHT)` — kết luận Oy nằm giữa
  - `Wait(1.5)`

- **cleanup**:
  - `FadeOut(block_heading, body_group, formula_group, figure_group)`
  - `FadeOut(section_heading)` + `FadeOut(lesson_title)` — kết thúc bài

---

## Ghi chú dựng hình

| Tham số | Giá trị |
|---------|---------|
| Gốc `O` | `ORIGIN` trong hệ cục bộ trước `place_figure()` |
| Register điểm | **Sau** `place_figure()` qua `dot.get_center()` — không hardcode tọa độ world cho `AngleMarker` |
| Độ dài tia | `3.0` (Hình 14, 16) |
| Góc Hình 14 | Ox `0°`, Oy `~30°`, Oz `~75°` |
| Góc Hình 15 | Oy `~60°`; đường xz ngang qua O (hai tia đối) |
| Góc Hình 16 | Ox `0°`, Oy `~45°`, Oz `~80°` |
| Màu tia / cạnh | `COLOR_DEFAULT` |
| Màu góc nhỏ | `COLOR_EQUAL_1`, `COLOR_EQUAL_2` |
| Màu góc tổng / lớn | `COLOR_EQUAL_3` |
| Màu điểm / tia kết luận | `COLOR_HIGHLIGHT` (Oy) |
| Nửa mặt phẳng | `fill_opacity=0.12`, màu `COLOR_EQUAL_1` (Hình 16) |
| Panel | `right`, `width_ratio: 0.45` cho mọi scene có hình |

**Quyết định kỹ thuật:**
- Pattern tia/góc tái dùng từ `specs/theory/tia/spec-ly-thuyet.md` scenes 01–03 (angle arcs, half-plane).
- Scene 03 cleanup **toàn bộ** `figure_group` trước Scene 04 (Hình 15 build mới).
- Scene 04: định nghĩa góc kề nhắc Hình 14 trong narration nhưng **không** vẽ lại; chỉ build Hình 15 khi đến góc kề bù.
- Scene 04 `nhan_xet`: heading `(*) Nhận xét` + body italic `COLOR_WARNING`.
- Scene 06 cleanup kết thúc bài: FadeOut cả `section_heading` + `lesson_title`.
- Voiceover: không đọc ký hiệu `∠`, `°`, `\widehat{}` — dùng "góc x Oy", "90 độ", "180 độ", "m độ", "n độ".
- Step 2 build: class `Conggoc` tại `scenes/theory/Conggoc.py` *(ngoài phạm vi spec này)*.

**Lifecycle figure:**

| Scene | Hình SGK | Hành động |
|-------|----------|-----------|
| 03 | Hình 14 | Build mới → FadeOut all |
| 04 | Hình 15 | Build mới → FadeOut all |
| 06 | Hình 16 | Build mới → FadeOut all + kết thúc bài |

---

## Checklist trước khi build (Step 2)

- [x] Mỗi scene có `method`, `block_type`, `heading`, `narration`, `animations`, `cleanup`
- [x] 3 scene có hình đều có `sgk_ref` + `figure.build` đủ thứ tự (Hình 14, 15, 16)
- [x] 4 scene `none` (00, 01, 02, 05) đều có `layout` (`place_formula_left`, `line_grouping`)
- [x] Không `GT:`, `KL:`, `proof_accumulator`, `ProofLine`
- [x] Scene 06 cleanup kết thúc bài (`FadeOut(section_heading)` + `FadeOut(lesson_title)`)
- [x] Narration không ký hiệu (∠, °); câu ≤ 20 từ; có "chẳng hạn/trên hình" khi có figure
- [x] `cleanup` ghi rõ FadeOut toàn bộ figure trước scene không có hình (03→04, 04→05)
