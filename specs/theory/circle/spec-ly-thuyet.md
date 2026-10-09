# Scene Spec Lý Thuyết: ĐƯỜNG TRÒN

## Thông tin chung

- **lesson_title**: ĐƯỜNG TRÒN
- **lesson_type**: theory
- **subject**: geometry
- **total_scenes**: 5
- **estimated_duration**: 6–8 phút

---

## Scene 00 — Intro

- **method**: `scene00_intro`
- **duration**: 20–25s
- **content**: Tiêu đề bài "ĐƯỜNG TRÒN" + heading "I. TÓM TẮT LÝ THUYẾT"
- **animations**:
  - `Write(lesson_title)` — font_size 40, to_edge(UP)
  - `FadeIn(section_heading)` — "I. TÓM TẮT LÝ THUYẾT", font_size 28
- **cleanup**: `FadeOut(section_heading)` | thu nhỏ `lesson_title` to_edge(UP, buff=0.2)

---

## Scene 01 — Khái niệm đường tròn

- **method**: `scene01_khaiNiem`
- **block_type**: `dinh_nghia`
- **duration**: 50–70s
- **heading**: "1. Khái niệm đường tròn"

- **body_lines**:
  - `"Trong mặt phẳng, đường tròn tâm \\(O\\) bán kính \\(R\\) (với \\(R > 0\\))"`
  - `"là tập hợp các điểm cách điểm \\(O\\) cố định một khoảng \\(R\\),"`
  - `r"\text{kí hiệu là: } (O;\,R)"`

- **terms_bold**: [đường tròn tâm O bán kính R, tập hợp các điểm]

- **figure**:
  - type: `geometry`
  - panel: `right`
  - width_ratio: `0.40`
  - build:
    - `circle(O, R=2.2)` — màu COLOR_CIRCLE (`#1565C0`)
    - `dot O` ở tâm, label `O` (LEFT)
    - `line segment từ O đến điểm trên đường tròn (góc 0°)` — dashed hoặc solid, label `R` (trên đoạn)
    - `arrow nhỏ hoặc tick tại điểm đầu mút của R`

- **narration**: |
    Khái niệm. Trong mặt phẳng, đường tròn tâm O bán kính R là tập hợp
    tất cả các điểm cách điểm O một khoảng bằng R.
    Điều kiện là R phải lớn hơn không.
    Đường tròn này được kí hiệu là O chấm phẩy R.
    Trên hình vẽ, điểm O là tâm và đoạn thẳng từ O đến đường tròn có độ dài R.

- **animations**:
  - `Write(block_heading)` at start
  - `FadeIn(body_lines[0..1])` + `Create(circle)` + `Create(dot O + label O)`
  - `FadeIn(body_lines[2])` + `Create(segment OR + label R)`
  - `Indicate(terms_bold_mobs, scale_factor=1.15)` — cuối scene

- **cleanup**: `FadeOut(block_heading, body_group)` | keep `figure_group` cho scene 02

---

## Scene 02 — Chú ý

- **method**: `scene02_chuY`
- **block_type**: `chu_y`
- **duration**: 35–50s
- **heading**: "Chú ý:"

- **body_lines**:
  - `"\\bullet\\;` Một đường tròn hoàn toàn xác định khi biết tâm và bán kính."`
  - `"\\bullet\\;` Khi không chú ý đến bán kính của đường tròn \\((O;R)\\),"`
  - `r"\quad\text{ta cũng có thể kí hiệu là đường tròn } (O)."`

- **terms_bold**: [(O;R), (O)]

- **figure**:
  - type: `geometry`
  - panel: `right`
  - width_ratio: `0.40`
  - build: tái dùng figure scene 01 (circle + dot O + segment R đã có)
  - additions:
    - Highlight label `(O;R)` bên cạnh đường tròn
    - Sau đó đổi/thêm label `(O)` — `Transform` hoặc `FadeIn`

- **narration**: |
    Chú ý. Một đường tròn hoàn toàn xác định khi ta biết tâm và bán kính của nó.
    Ngoài ra, khi không cần nhấn mạnh bán kính,
    ta có thể kí hiệu đường tròn tâm O đơn giản là O trong ngoặc tròn.

- **animations**:
  - `Write(block_heading)` at start
  - `FadeIn(body_lines[0])` — chú ý 1
  - `FadeIn(body_lines[1..2])` + `Indicate(label_OR)` + `FadeIn(label_O_simple)`
  - `Indicate(terms_bold_mobs)`

- **cleanup**: `FadeOut(block_heading, body_group, label_OR, label_O_simple)` | keep `figure_group`

---

## Scene 03 — Nhận xét: Vị trí tương đối của điểm

- **method**: `scene03_nhanXet`
- **block_type**: `nhan_xet`
- **duration**: 55–75s
- **heading**: "Nhận xét:"

- **body_lines**:
  - `"\\bullet\\;` Vị trí tương đối của một điểm đối với đường tròn:"`
  - `r"+\; M \text{ nằm \textbf{trên} đường tròn } (O) \text{ nếu } OM = R"`
  - `r"+\; M \text{ nằm \textbf{trong} đường tròn } (O) \text{ nếu } OM < R"`
  - `r"+\; M \text{ nằm \textbf{ngoài} đường tròn } (O) \text{ nếu } OM > R"`
  - `"\\bullet\\;` Hình tròn tâm O bán kính R gồm các điểm nằm trên và nằm trong đường tròn \\((O;R)\\)."`

- **terms_bold**: [trên, trong, ngoài, hình tròn]

- **figure**:
  - type: `geometry`
  - panel: `right`
  - width_ratio: `0.42`
  - build:
    - `circle(O, R=2.0)` — màu COLOR_CIRCLE
    - `dot O` + label `O` (DOWN)
    - `dot M1` trên đường tròn (góc ~50°) — label `M` (UR), màu COLOR_EQUAL_1; segment `OM1` dashed
    - `dot M2` trong đường tròn (khoảng cách ~0.9R, góc ~160°) — label `M` (UL), màu COLOR_EQUAL_2; segment `OM2` dashed
    - `dot M3` ngoài đường tròn (khoảng cách ~1.5R, góc ~290°) — label `M` (DR), màu COLOR_EQUAL_3; segment `OM3` dashed
    - Ba điểm M xuất hiện lần lượt, mỗi lần highlight kèm dòng text tương ứng

- **narration**: |
    Nhận xét. Với điểm M trong mặt phẳng và đường tròn tâm O bán kính R,
    ta có ba vị trí tương đối.
    Điểm M nằm trên đường tròn khi O M bằng R.
    Điểm M nằm trong đường tròn khi O M nhỏ hơn R.
    Điểm M nằm ngoài đường tròn khi O M lớn hơn R.
    Ngoài ra, hình tròn bao gồm tất cả điểm nằm trên và nằm trong đường tròn đó.

- **animations**:
  - `Write(block_heading)` at start
  - `FadeIn(body_lines[0])`
  - `FadeIn(body_lines[1])` + `Create(dot M1 + segment OM1)` + `Indicate(M1, color=COLOR_EQUAL_1)`
  - `FadeIn(body_lines[2])` + `Create(dot M2 + segment OM2)` + `Indicate(M2, color=COLOR_EQUAL_2)`
  - `FadeIn(body_lines[3])` + `Create(dot M3 + segment OM3)` + `Indicate(M3, color=COLOR_EQUAL_3)`
  - `FadeIn(body_lines[4])` + `FadeIn(filled_circle, opacity=0.15)` — vùng tô nhẹ bên trong
  - `Indicate(terms_bold_mobs)`

- **cleanup**: `FadeOut(all)` — không giữ hình cho scene 04 (figure mới hoàn toàn)

---

## Scene 04 — Tính chất đối xứng của đường tròn

- **method**: `scene04_tinhChat`
- **block_type**: `dinh_li`
- **duration**: 50–65s
- **heading**: "2. Tính chất đối xứng của đường tròn"

- **body_lines**:
  - `"\\bullet\\;` Đường tròn là hình có \\textbf{tâm đối xứng}:"`
  - `r"\quad\text{Tâm của đường tròn là tâm đối xứng của đường tròn đó.}"`
  - `"\\bullet\\;` Đường tròn là hình có \\textbf{trục đối xứng}:"`
  - `r"\quad\text{Bất kì đường kính nào cũng là trục đối xứng của đường tròn đó.}"`

- **terms_bold**: [tâm đối xứng, trục đối xứng]

- **figure**:
  - type: `geometry`
  - panel: `right`
  - width_ratio: `0.42`
  - build:
    - `circle(O, R=2.0)` — màu COLOR_CIRCLE
    - `dot O` + label `O` (DOWN)
    - `dot A` trên đường tròn (góc 180°, bên trái) + label `A` (LEFT)
    - `dot A'` đối xứng qua O (góc 0°, bên phải) + label `A'` (RIGHT)
    - `line segment AA'` (đường kính ngang) — màu COLOR_DEFAULT
    - `DashedLine` dọc qua O (trục đối xứng dọc) — màu `GRAY`, style dashed
    - `Brace hoặc right-angle mark` tại O giữa A-A' và trục dọc (chỉ tính đối xứng)
    - *(Tùy chọn)* thêm 1 đường kính nghiêng thứ hai để minh họa "bất kì đường kính nào"

- **narration**: |
    Tính chất đối xứng của đường tròn.
    Thứ nhất, đường tròn là hình có tâm đối xứng.
    Tâm của đường tròn chính là tâm đối xứng của đường tròn đó.
    Thứ hai, đường tròn là hình có trục đối xứng.
    Bất kì đường kính nào của đường tròn cũng là một trục đối xứng.
    Điều này có nghĩa là đường tròn có vô số trục đối xứng.

- **animations**:
  - `Write(block_heading)` at start
  - `FadeIn(body_lines[0..1])` + `Create(circle + dot O)`
  - `Create(dot A + dot A' + segment AA')` + `Indicate(dot O, color=COLOR_EQUAL_1)` — minh họa tâm đối xứng
  - `FadeIn(body_lines[2..3])` + `Create(DashedLine dọc)` — minh họa trục đối xứng
  - *(Tùy chọn)* `Create(đường kính nghiêng thứ hai, style dashed)` + narration "bất kì"
  - `Indicate(terms_bold_mobs, scale_factor=1.15)`

- **cleanup**: `FadeOut(all)`

---

## Ghi chú dựng hình

- `O = ORIGIN`, `R = 2.0` đến `2.2` (tùy scene)
- Màu đường tròn: `COLOR_CIRCLE` (`#1565C0`)
- Màu điểm M trên đường tròn: `COLOR_EQUAL_1` (xanh lá)
- Màu điểm M trong đường tròn: `COLOR_EQUAL_2` (cam)
- Màu điểm M ngoài đường tròn: `COLOR_EQUAL_3` (đỏ)
- Trục đối xứng: `GRAY`, `DashedLine`
- Scene 02 tái dùng figure của Scene 01 (không FadeOut figure khi chuyển cảnh)
- Scene 03 tạo figure mới hoàn toàn (3 điểm M ở ba vị trí khác nhau, animate từng bước)
- Scene 04 tạo figure mới: đường tròn + điểm A, A' + đường kính + trục dọc dashed
