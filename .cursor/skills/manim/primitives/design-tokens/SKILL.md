---
name: manim-design-tokens
description: Chuẩn hoá màu sắc, timing animation, z-index và tên biến hình học qua design token. Dùng cho mọi file Manim trong project để tránh hardcode giá trị màu, thời gian, hay z-index.
---

# Skill: Manim – Design Tokens (rule 4, 6, 7, 8)

## Khi nào dùng skill này?

Bất kỳ file Manim nào tạo ra Mobject có màu / có timing animation / có z-index / có đặt tên biến hình học. Tức là: **mọi scene Manim trong project**.

Skill này chuẩn hoá 4 nhóm token để mọi scene đều "trông giống nhau" và để code mới chỉ cần đổi 1 chỗ trong `manim_helpers/visual_tokens.py` là toàn bộ video đồng loạt cập nhật.

> **Quy tắc bất di bất dịch**: KHÔNG hardcode hex `"#E65100"`, KHÔNG hardcode `run_time=0.5`, KHÔNG hardcode `set_z_index(2)`. Mọi giá trị phải tới từ token.

```python
# ✗ SAI – hardcode
seg.set_stroke("#E65100", width=10)
self.play(FadeIn(sec), run_time=0.5)
dot.set_z_index(2)

# ✓ ĐÚNG – dùng token
from manim_helpers import COLOR_ACTIVE, TIMING_ANGLE, LAYER_MARKERS
seg.set_stroke(COLOR_ACTIVE, width=10)
self.play(FadeIn(sec), run_time=TIMING_ANGLE)
dot.set_z_index(LAYER_MARKERS)
```

---

## 1. Color tokens (rule 4)

Bảng màu chuẩn cho **nền sáng** `"#F5F1E8"`. Mọi scene phải dùng tên token, không hardcode hex.

### Bảng đầy đủ

```text
Token                  Hex       Vai trò
─────────────────────  ─────────  ─────────────────────────────────────────────
COLOR_DEFAULT          #2C2C2C   Text mặc định, stroke nét hình học mặc định
COLOR_BACKGROUND       #F5F1E8   self.camera.background_color
COLOR_GRID             #D6D0C4   NumberPlane line color
COLOR_EQUAL_1          #E65100   Cặp bằng nhau — đối tượng thứ 1 (mặc định)
COLOR_EQUAL_2          #2D6A2D   Cặp bằng nhau — đối tượng thứ 2
COLOR_EQUAL_3          #1565C0   Cặp bằng nhau — đối tượng thứ 3 (hoặc tam giác mặc định)
COLOR_ACTIVE           #E65100   Đối tượng active / highlight (alias EQUAL_1)
COLOR_SECONDARY        #546E7A   Đoạn phụ trợ (bán kính, đoạn nối)
COLOR_FADED            #9E9E9E   Đối tượng bị làm mờ
COLOR_WARNING          #BF360C   Cảnh báo / nhấn mạnh đặc biệt
COLOR_RESULT_KEY       #2D6A2D   Box GREEN — kết quả trung gian quan trọng
COLOR_RESULT_FINAL     #C62828   Box RED — kết luận đpcm
COLOR_CIRCLE           #1565C0   Đường tròn
COLOR_RIGHT_ANGLE      #37474F   RightAngle marker
COLOR_AUX_LINE         #546E7A   Đường phụ trợ (đường cao, đường trung trực ...)
COLOR_TANGENT          #2E7D32   Đường tiếp tuyến
```

### Quy tắc dùng (rule 5 – sẽ chi tiết trong `manim-geometry-engine`)

- **Bằng nhau** (đoạn = đoạn, góc = góc, tam giác = tam giác): dùng **CÙNG 1 màu** cho tất cả đối tượng → mặc định `COLOR_EQUAL_1`.
- **Phân biệt** (so sánh hai tam giác, tổng nhiều góc): mỗi đối tượng 1 màu khác nhau → `COLOR_EQUAL_1`, `COLOR_EQUAL_2`, `COLOR_EQUAL_3`.
- **Đoạn phụ trợ** mới kẻ: `COLOR_SECONDARY` hoặc `COLOR_AUX_LINE`.

---

## 2. Visual states (`STATE_*`)

Gói nhanh `{color, stroke_width, opacity}` thành một state, áp dụng qua `apply_state(mob, state)`.

```text
Token            color            stroke_width  opacity  Khi nào dùng
───────────────  ───────────────  ────────────  ───────  ─────────────────────────────────────
STATE_DEFAULT    COLOR_DEFAULT         2.0       1.0    Trạng thái gốc của mọi nét
STATE_HIGHLIGHT  COLOR_ACTIVE          6.0       1.0    Voiceover nhắc đối tượng; stroke_width
                                                        tái dùng bởi highlight_right_angle /
                                                        show_right_angle_equal
STATE_EQUAL      COLOR_EQUAL_1         4.0       1.0    Đoạn / cạnh trong cặp "bằng nhau"
STATE_SECONDARY  COLOR_SECONDARY       2.0       1.0    Đoạn phụ trợ
STATE_FADED      COLOR_FADED           1.5       0.4    Đối tượng tạm thời bị làm mờ
STATE_ACTIVE     COLOR_ACTIVE          4.0       1.0    Highlight nhẹ hơn HIGHLIGHT
```

```python
from manim_helpers import apply_state, STATE_HIGHLIGHT, STATE_DEFAULT

apply_state(seg_AB, STATE_HIGHLIGHT)   # nhấn mạnh
self.play(seg_AB.animate.set_color(COLOR_DEFAULT), run_time=TIMING_FADE)
```

---

## 3. Timing tokens (rule 6) – highlight effects

Bắt buộc dùng cho mọi `run_time` của **effect highlight**. Không hardcode số.

```text
Token                      Giá trị (s)  Dùng cho
─────────────────────────  ───────────  ─────────────────────────────────────────
TIMING_POINT                    0.2     Flash / Indicate dot
TIMING_SEGMENT                  0.4     Indicate đoạn thẳng (mặc định)
TIMING_ANGLE                    0.5     FadeIn / FadeOut sector góc
TIMING_INDICATE_SEGMENT         0.6     seg.animate.set_stroke(...) there_and_back
TIMING_INDICATE_TRIANGLE        0.7     tri.animate.set_fill(...) there_and_back
TIMING_PROOF_WRITE              0.5     Write toàn bộ ProofLine
TIMING_RELATION                 0.25    Write 1 token nhỏ ('=', '⇒', '(c.g.c)')
TIMING_CONCLUSION               0.8     Write kết luận cuối ý
TIMING_FADE                     0.3     FadeIn / FadeOut chuẩn
```

```python
self.play(FadeIn(sec_OFB), run_time=TIMING_ANGLE)
self.play(seg.animate.set_stroke(COLOR_ACTIVE, width=10),
          run_time=TIMING_INDICATE_SEGMENT, rate_func=there_and_back)
```

---

## 3b. Motion tokens (`MOTION_*`) – animation chuyển động

Dùng cho `run_time` của **chuyển động** Mobject (phân biệt với `TIMING_*` dành cho highlight effect). Không hardcode số.

```text
Token               Giá trị (s)  Dùng cho
──────────────────  ───────────  ─────────────────────────────────────────────
MOTION_ENTER             0.6    FadeIn / Create phần tử mới vào scene
MOTION_EXIT              0.4    FadeOut phần tử rời scene
MOTION_TRANSFORM         0.7    ReplacementTransform, TransformMatchingTex
MOTION_SHIFT             0.5    .animate.shift(...) / .animate.move_to(...)
MOTION_SCALE             0.4    .animate.scale(...)
MOTION_TO_CORNER         0.6    result_group.animate.to_corner(UR, ...)
MOTION_TITLE_IN          0.9    AddTextLetterByLetter(title) — tiêu đề xuất hiện
MOTION_TITLE_OUT         0.35   FadeOut(title) — tiêu đề biến mất
```

```python
from manim_helpers import MOTION_ENTER, MOTION_EXIT, MOTION_TO_CORNER, MOTION_TITLE_OUT

self.play(AddTextLetterByLetter(title), run_time=MOTION_TITLE_IN)
self.play(FadeIn(new_element), run_time=MOTION_ENTER)
self.play(result_group.animate.to_corner(UR, buff=0.5), run_time=MOTION_TO_CORNER)
self.play(FadeOut(title), run_time=MOTION_TITLE_OUT)
```

---

## 3c. Emphasis tokens (`EMPHASIS_*`) – Indicate / Circumscribe / Flash

Chuẩn hoá tham số cho `Indicate`, `Circumscribe`, `Flash`. Không hardcode `scale_factor=1.2`, `flash_radius=0.25`, v.v.

```text
Token                        Giá trị    Dùng cho
───────────────────────────  ─────────  ─────────────────────────────────────────
EMPHASIS_SCALE               1.15       scale_factor cho Indicate(...) thông thường
EMPHASIS_SCALE_STRONG        1.3        scale_factor cho kết luận quan trọng
EMPHASIS_COLOR               "#E65100"  color cho Indicate(...) (alias COLOR_ACTIVE)
EMPHASIS_FLASH_RADIUS        0.25       flash_radius cho Flash(dot, ...)
EMPHASIS_CIRCUMSCRIBE_TIME   1.2        run_time cho Circumscribe(..., fade_out=True)
EMPHASIS_INDICATE_TIME       0.7        run_time cho Indicate(...) thông thường
```

```python
from manim_helpers import (
    EMPHASIS_SCALE, EMPHASIS_SCALE_STRONG, EMPHASIS_COLOR,
    EMPHASIS_FLASH_RADIUS, EMPHASIS_CIRCUMSCRIBE_TIME, EMPHASIS_INDICATE_TIME,
)

# Nhấn mạnh mục tiêu vừa viết ra:
self.play(Indicate(goal, scale_factor=EMPHASIS_SCALE, color=EMPHASIS_COLOR),
          run_time=EMPHASIS_INDICATE_TIME)

# Flash tại điểm giao:
self.play(Flash(dot_H, color=EMPHASIS_COLOR, flash_radius=EMPHASIS_FLASH_RADIUS))

# Kết luận đpcm (Circumscribe + fade):
self.play(Circumscribe(result_tex, color=COLOR_RESULT_FINAL,
                       fade_out=True, run_time=EMPHASIS_CIRCUMSCRIBE_TIME))

# Kết luận quan trọng (scale mạnh hơn):
self.play(Indicate(pf_result, scale_factor=EMPHASIS_SCALE_STRONG,
                   color=COLOR_RESULT_FINAL), run_time=EMPHASIS_INDICATE_TIME)
```

---

## 4. Layer / z-index tokens (rule 7)

Tránh các trường hợp Dot bị Line đè lên do `z_index` mặc định = 0.

```text
Token               Giá trị  Dùng cho
──────────────────  ───────  ─────────────────────────────────────────────
LAYER_BACKGROUND         0   NumberPlane, ô lưới
LAYER_GEOMETRY          10   Arc, Circle, Line, Polygon
LAYER_MARKERS           20   Dot, label, RightAngle, AngleMarker
LAYER_PROOF_TEXT        30   MathTex / Tex của proof, title
LAYER_HIGHLIGHT         40   Highlight tạm (Sector fill, Indicate copy)
```

```python
dot_C = Dot(C, color=COLOR_DEFAULT, radius=0.06).set_z_index(LAYER_MARKERS)
sec   = AngleMarker(...).set_z_index(LAYER_MARKERS)   # Engine tự set
```

---

## 5. Naming convention (rule 8)

Tên biến Mobject phải theo pattern dưới đây để các skill khác (đặc biệt `GeometryEngine`) tự match được loại đối tượng.

```text
Loại              Pattern       Ví dụ đúng                    Ví dụ sai
────────────────  ────────────  ────────────────────────────  ─────────────────
Điểm              dot_<X>       dot_A, dot_M, dot_O           pointA, dotA1
Label điểm        label_<X>     label_A, label_O              lbl_A, tex_A
Đoạn thẳng        seg_<XY>      seg_AB, seg_BC, seg_OF        lineAB, seg_aB
Góc (Angle/arc)   ang_<XYZ>     ang_OAC, ang_AKI              angle_OAC
Tam giác          tri_<XYZ>     tri_OFB, tri_ABC              triOFB, tri_O_F_B
Tứ giác           quad_<WXYZ>   quad_ABCD                     quadABCD
Đường tròn        circ_<NAME>   circ_O, circ_AI               circle_O, circO
Sector / fill     sec_<XYZ>     sec_OFB, sec_AKI              sector_OFB
Góc vuông         ra_<X>        ra_D, ra_C                    rightAngle_D
Proof line        pf_<NN>       pf_01, pf_05                  proof_line1, pf1
```

Helper: `check_name(kind, name)` trả `True/False` để self-test trong unit test.

```python
from manim_helpers import check_name
assert check_name("triangle", "tri_OFB")
assert not check_name("triangle", "triOFB")
```

> Tên biến trong tiếng Việt **luôn** dùng chữ cái Latin in hoa cho điểm (`A, B, C, O, M, ...`) – không dùng `Á, Ô, ...`.

---

## 6. Code reference

Toàn bộ token được định nghĩa trong `manim_helpers/visual_tokens.py` ở root project. Luôn import qua:

```python
from manim_helpers import (
    COLOR_DEFAULT, COLOR_ACTIVE, COLOR_EQUAL_1, COLOR_EQUAL_2, COLOR_EQUAL_3,
    COLOR_SECONDARY, COLOR_RESULT_KEY, COLOR_RESULT_FINAL, COLOR_CIRCLE,
    COLOR_RIGHT_ANGLE, COLOR_AUX_LINE, COLOR_TANGENT,
    STATE_DEFAULT, STATE_HIGHLIGHT, STATE_EQUAL, apply_state,
    TIMING_POINT, TIMING_SEGMENT, TIMING_ANGLE, TIMING_INDICATE_SEGMENT,
    TIMING_INDICATE_TRIANGLE, TIMING_PROOF_WRITE, TIMING_RELATION,
    TIMING_CONCLUSION, TIMING_FADE,
    MOTION_ENTER, MOTION_EXIT, MOTION_TRANSFORM, MOTION_SHIFT,
    MOTION_SCALE, MOTION_TO_CORNER, MOTION_TITLE_IN, MOTION_TITLE_OUT,
    EMPHASIS_SCALE, EMPHASIS_SCALE_STRONG, EMPHASIS_COLOR,
    EMPHASIS_FLASH_RADIUS, EMPHASIS_CIRCUMSCRIBE_TIME, EMPHASIS_INDICATE_TIME,
    LAYER_BACKGROUND, LAYER_GEOMETRY, LAYER_MARKERS,
    LAYER_PROOF_TEXT, LAYER_HIGHLIGHT,
)
```

Khi cần thêm token mới (màu mới, timing mới): **chỉnh sửa `manim_helpers/visual_tokens.py`** và cập nhật bảng trong skill này — KHÔNG hardcode tại file scene.

---

## 7. Checklist

- [ ] File scene có `from manim_helpers import *` (hoặc named imports đầy đủ token)
- [ ] **Mọi** `color=` / `fill_color=` / `stroke_color=` dùng `COLOR_*`, không hardcode hex
- [ ] **Mọi** `run_time=` của highlight effect dùng `TIMING_*`, không hardcode số
- [ ] **Mọi** `run_time=` của chuyển động (FadeIn/FadeOut/move/transform) dùng `MOTION_*`, không hardcode số
- [ ] **Mọi** `scale_factor=`, `flash_radius=` trong Indicate/Flash/Circumscribe dùng `EMPHASIS_*`, không hardcode
- [ ] **Mọi** `.set_z_index(...)` dùng `LAYER_*`, không hardcode `2`, `5`, ...
- [ ] Đặt tên biến hình học theo bảng mục 5 (`dot_*`, `seg_*`, `ang_*`, `tri_*`, `quad_*`, `circ_*`, `ra_*`, `pf_*`)
- [ ] Khi cần "bằng nhau": dùng cùng 1 màu (`COLOR_EQUAL_1` mặc định) cho mọi đối tượng trong tập "bằng"
- [ ] Khi cần "phân biệt": dùng `COLOR_EQUAL_1` / `_2` / `_3` cho từng đối tượng
- [ ] Box kết quả trung gian: `COLOR_RESULT_KEY` (xanh lá); box kết luận đpcm: `COLOR_RESULT_FINAL` (đỏ)
