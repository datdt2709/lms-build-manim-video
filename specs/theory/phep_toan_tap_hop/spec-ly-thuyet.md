# Scene Spec Lý Thuyết: CHUYÊN ĐỀ 2. PHÉP TOÁN TRONG TẬP HỢP CÁC SỐ TỰ NHIÊN

## Thông tin chung

- **lesson_title**: CHUYÊN ĐỀ 2. PHÉP TOÁN TRONG TẬP HỢP CÁC SỐ TỰ NHIÊN
- **lesson_type**: theory
- **subject**: algebra
- **section_heading**: I. KIẾN THỨC CẦN NHỚ
- **total_scenes**: 6
- **estimated_duration**: 7–9 phút

> **Layout 3 tầng:** `lesson_title` (tầng 0) → `section_heading` persistent scenes 01–05 (tầng 1) → `block_heading` đổi mỗi scene, neo dưới `section_heading` (tầng 2).

> **Ghi chú nguồn:** Ảnh SGK (Chuyên đề 2 — I. Kiến thức cần nhớ) chỉ chứa text và công thức LaTeX — không có hình vẽ hình học hay đồ thị.
> Theo quy tắc: `figure.type: none` cho **toàn bộ** scene.

---

## Scene 00 — Intro

- **method**: `scene00_intro`
- **duration**: 20–25s
- **content**: Tiêu đề bài + heading phần "I. KIẾN THỨC CẦN NHỚ"
- **narration**: |
    Phép toán trong tập hợp các số tự nhiên.
    Phần một. Kiến thức cần nhớ.
- **animations**:
  - `Write(lesson_title)` — "CHUYÊN ĐỀ 2. PHÉP TOÁN TRONG TẬP HỢP CÁC SỐ TỰ NHIÊN", font_size 36, `to_edge(UP)`
  - `FadeIn(section_heading)` — "I. KIẾN THỨC CẦN NHỚ", font_size 28, dưới tiêu đề
  - `Wait(1.5)`
- **cleanup**: giữ `lesson_title` + `section_heading` cho scenes 01–05

---

## Scene 01 — Các tính chất cơ bản của phép cộng và phép nhân

- **method**: `scene01_tinhChatCongNhan`
- **block_type**: `dinh_li`
- **duration**: 65–75s
- **heading**: "1. Các tính chất cơ bản của phép cộng và phép nhân"

- **body_lines**:
  - `label_giao_hoan`: `r"- \textbf{Tính chất giao hoán:}"` *(list item)*
  - `formula_gh_cong`: `r"$\bullet$ $a + b = b + a$"` *(sub-item, Tex)*
  - `formula_gh_nhan`: `r"$\bullet$ $a \cdot b = b \cdot a$"` *(sub-item, Tex)*
  - `label_ket_hop`: `r"- \textbf{Tính chất kết hợp:}"` *(list item)*
  - `formula_kh_cong`: `r"$\bullet$ $(a + b) + c = a + (b + c)$"` *(sub-item, Tex)*
  - `formula_kh_nhan`: `r"$\bullet$ $(a \cdot b) \cdot c = a \cdot (b \cdot c)$"` *(sub-item, Tex)*
  - `label_cong_0`: `r"- \textbf{Cộng với không:}"` *(list item)*
  - `formula_cong_0`: `r"$\bullet$ $a + 0 = 0 + a = a$"` *(sub-item, Tex)*
  - `label_nhan_1`: `r"- \textbf{Nhân với một:}"` *(list item)*
  - `formula_nhan_1`: `r"$\bullet$ $a \cdot 1 = 1 \cdot a = a$"` *(sub-item, Tex)*
  - `label_phan_phoi`: `r"- \textbf{Tính chất phân phối:}"` *(list item)*
  - `formula_phan_phoi`: `r"$\bullet$ $a \cdot (b + c) = a \cdot b + a \cdot c$"` *(sub-item, Tex)*

- **terms_bold**: [tính chất giao hoán, tính chất kết hợp, tính chất phân phối]

- **figure**:
  - type: `none`
  - panel: `none`

- **layout**:
  - mode: `text_full_width`
  - wrap_width_cm: `14`
  - font_size: `27`
  - formula_method: `place_formula_left`
  - body_gap: `0.16`
  - formula_gap: `0.22`
  - formula_indent: `0.8`
  - line_grouping:
    - group: [label_giao_hoan, formula_gh_cong, formula_gh_nhan]
    - group: [label_ket_hop, formula_kh_cong, formula_kh_nhan]
    - group: [label_cong_0, formula_cong_0]
    - group: [label_nhan_1, formula_nhan_1]
    - group: [label_phan_phoi, formula_phan_phoi]

- **narration**: |
    Tính chất.
    Tính chất giao hoán: a cộng b bằng b cộng a;
    a nhân b bằng b nhân a.
    Tính chất kết hợp: a cộng b, cộng c bằng a cộng b cộng c;
    a nhân b, nhân c bằng a nhân b nhân c.
    Cộng với không: a cộng không bằng không cộng a bằng a.
    Nhân với một: a nhân một bằng một nhân a bằng a.
    Tính chất phân phối: a nhân tổng b cộng c
    bằng a nhân b cộng a nhân c.

- **animations**:
  - `Write(block_heading)` at start
  - `FadeIn(label_giao_hoan)` + `Write(formula_gh_cong, formula_gh_nhan)` — nhóm giao hoán
  - `Indicate(label_giao_hoan, formula_gh_cong, formula_gh_nhan)` — khi đọc giao hoán
  - `FadeIn(label_ket_hop)` + `Write(formula_kh_cong, formula_kh_nhan)` — nhóm kết hợp
  - `Indicate(label_ket_hop, formula_kh_cong, formula_kh_nhan)` — khi đọc kết hợp
  - `FadeIn(label_cong_0)` + `Write(formula_cong_0)` — cộng với không
  - `FadeIn(label_nhan_1)` + `Write(formula_nhan_1)` — nhân với một
  - `FadeIn(label_phan_phoi)` + `Write(formula_phan_phoi)` — phân phối
  - `Indicate(label_phan_phoi, formula_phan_phoi)` — khi đọc phân phối
  - `Indicate(terms_bold_mobs, scale_factor=1.15)` — cuối scene

- **cleanup**: `FadeOut(block_heading, body_group, formula_group)`

---

## Scene 02 — Điều kiện phép trừ

- **method**: `scene02_dieuKienTru`
- **block_type**: `dinh_nghia`
- **duration**: 50–60s
- **heading**: "2. Điều kiện để thực hiện phép trừ $a - b$ là $a \geq b$"

- **body_lines**:
  - `line1`: `"Điều kiện để thực hiện phép trừ $a - b$ là $a \geq b$."`
  - `line2`: `"- Tính chất phân phối của phép nhân đối với phép trừ:"` *(list item)*

- **formulas**:
  - `formula_dieu_kien`: `r"$\bullet$ $a \geq b$"` *(sub-item, Tex)*
  - `formula_phan_phoi_tru`: `r"$\bullet$ $a \cdot (b - c) = a \cdot b - a \cdot c$"` *(sub-item, Tex)*

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
    - group: [body_lines[0], formula_dieu_kien]
    - group: [body_lines[1], formula_phan_phoi_tru]

- **narration**: |
    Định nghĩa.
    Để thực hiện phép trừ a trừ b trong tập số tự nhiên,
    a phải lớn hơn hoặc bằng b.
    Phép nhân còn phân phối đối với phép trừ:
    a nhân hiệu b trừ c bằng a nhân b trừ a nhân c.

- **animations**:
  - `Write(block_heading)` at start
  - `FadeIn(body_lines[0])` + `Write(formula_dieu_kien)`
  - `Indicate(formula_dieu_kien, scale_factor=1.1)` — nhấn điều kiện a lớn hơn hoặc bằng b
  - `FadeIn(body_lines[1])` + `Write(formula_phan_phoi_tru)`

- **cleanup**: `FadeOut(block_heading, body_group, formula_group)`

---

## Scene 03 — Chia hết

- **method**: `scene03_chiaHet`
- **block_type**: `dinh_nghia`
- **duration**: 45–55s
- **heading**: "3. Điều kiện để số $a$ chia hết cho số $b \neq 0$"

- **body_lines**:
  - `"Số $a$ \textbf{chia hết} cho số $b \neq 0$ khi tồn tại số $q$ sao cho:"`

- **formulas**:
  - `formula_chia_het`: `r"$\bullet$ $a = b \cdot q$"` *(sub-item, Tex)*

- **terms_bold**: [chia hết]

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
    - group: [body_lines[0], formula_chia_het]

- **narration**: |
    Định nghĩa.
    Số a chia hết cho số b khác không
    khi tồn tại số q sao cho a bằng b nhân q.

- **animations**:
  - `Write(block_heading)` at start
  - `FadeIn(body_lines[0])`
  - `Write(formula_chia_het)`
  - `Indicate(terms_bold_mobs, scale_factor=1.15)` — cuối scene

- **cleanup**: `FadeOut(block_heading, body_group, formula_chia_het)`

---

## Scene 04 — Phép chia có dư

- **method**: `scene04_chiaCoDu`
- **block_type**: `dinh_li`
- **duration**: 50–60s
- **heading**: "4. Phép chia có dư"

- **body_lines**:
  - `"Chia số $a$ cho số $b \neq 0$ ta được:"`

- **formulas**:
  - `formula_chia_du`: `r"$\bullet$ $a = b \cdot q + r$"` *(sub-item, Tex)*
  - `formula_dieu_kien_r`: `r"$\bullet$ $0 \leq r < b$"` *(sub-item, Tex)*

- **figure**:
  - type: `none`
  - panel: `none`

- **layout**:
  - mode: `text_full_width`
  - wrap_width_cm: `14`
  - font_size: `28`
  - formula_method: `place_formula_left`
  - body_gap: `0.16`
  - formula_gap: `0.28`
  - formula_indent: `0.8`
  - line_grouping:
    - group: [body_lines[0], formula_chia_du]
    - group: [formula_dieu_kien_r]

- **narration**: |
    Định lí.
    Khi chia số a cho số b khác không,
    ta được a bằng b nhân q cộng r,
    với r lớn hơn hoặc bằng không và nhỏ hơn b.

- **animations**:
  - `Write(block_heading)` at start
  - `FadeIn(body_lines[0])`
  - `Write(formula_chia_du)`
  - `Write(formula_dieu_kien_r)`
  - `Indicate(formula_dieu_kien_r, scale_factor=1.1)` — nhấn điều kiện r

- **cleanup**: `FadeOut(block_heading, body_group, formula_chia_du, formula_dieu_kien_r)`

---

## Scene 05 — Nhận xét

- **method**: `scene05_nhanXet`
- **block_type**: `nhan_xet`
- **duration**: 70–80s
- **heading**: "(*) Nhận xét"
- **body_style**: italic + `COLOR_WARNING`

- **body_lines**:
  - `r"\textit{- $r \in \{0;\,1;\,2;\,\ldots;\,b-1\}$, nên khi chia một số cho $b$ thì số dư có $b$ khả năng.}"`
  - `r"\textit{- $(a - r) \vdots b$.}"`
  - `r"\textit{- Nếu $a \vdots c$ và $b \vdots c$ thì $(a \pm b) : c = a : c \pm b : c$.}"`
  - `r"\textit{- Nếu $a \vdots b$ và $b \vdots c$ thì $a \vdots c$ (tính chất bắc cầu).}"`

- **terms_bold**: [tính chất bắc cầu]

- **figure**:
  - type: `none`
  - panel: `none`

- **layout**:
  - mode: `text_full_width`
  - wrap_width_cm: `14`
  - font_size: `26`
  - formula_method: `place_formula_left`
  - body_gap: `0.18`
  - formula_gap: `0.25`
  - formula_indent: `0.8`
  - line_grouping:
    - group: [body_lines[0]]
    - group: [body_lines[1]]
    - group: [body_lines[2]]
    - group: [body_lines[3]]

- **narration**: |
    Nhận xét.
    Số dư r thuộc tập từ không đến b trừ một,
    nên khi chia một số cho b thì số dư có b khả năng.
    Hiệu a trừ r chia hết cho b.
    Nếu a chia hết cho c và b chia hết cho c
    thì a cộng b hoặc a trừ b cũng chia hết cho c.
    Nếu a chia hết cho b và b chia hết cho c
    thì a chia hết cho c — đây là tính chất bắc cầu.

- **animations**:
  - `Write(block_heading)` at start — heading màu `COLOR_WARNING`
  - `FadeIn(body_lines[0], color=COLOR_WARNING)` + `Indicate(body_lines[0])` — số dư có b khả năng
  - `FadeIn(body_lines[1], color=COLOR_WARNING)` + `Indicate(body_lines[1])` — a trừ r chia hết cho b
  - `FadeIn(body_lines[2], color=COLOR_WARNING)` + `Indicate(body_lines[2])` — phân phối phép chia
  - `FadeIn(body_lines[3], color=COLOR_WARNING)` + `Indicate(terms_bold_mobs)` — tính chất bắc cầu

- **cleanup**: `FadeOut(all)` + `FadeOut(section_heading)` + `FadeOut(lesson_title)` — kết thúc bài

---

## Ghi chú dựng hình

- **Không có hình vẽ** trong toàn bộ spec — ảnh SGK chỉ có text và công thức.
- Tất cả scene dùng `TheoryColumn(has_figure=False)` và `tex_wrapped` — **không** `place_formula()`.
- `formula_method: place_formula_left` áp dụng thống nhất cho mọi scene.
- Scene 01 có nhiều công thức → `font_size: 27` để tránh tràn màn hình.
- Scene 05 (`nhan_xet`): heading và body dùng `\textit{}` + `color=COLOR_WARNING` (`#BF360C`).
- Scene 04 cleanup không giữ gì — Scene 05 là nhận xét text-only độc lập.
