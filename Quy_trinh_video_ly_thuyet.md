# Quy trình Video Bài Giảng Lý Thuyết

> Hướng dẫn thực hành: từ **ảnh trang sách / PDF** → **video Manim lý thuyết** (MP4 + SRT).  
> Mỗi bước ghi rõ **việc cần làm**, **prompt gợi ý**, **skill/rule áp dụng**, **output**.  
> **Kiến trúc skill & pipeline bài toán:** `Build_video_baigiang_workflow.md` · **Cây thư mục:** `.cursor/skills/README.md`

---

## Pipeline tổng quan

```
  [Ảnh/PDF trang lý thuyết]
              │
              ▼
  ┌───────────────────────────────────────┐
  │ Bước 1 — Lập kế hoạch                 │
  │         spec-ly-thuyet.md             │
  └───────────────────────────────────────┘
              │
              ▼
  ┌───────────────────────────────────────┐
  │ Bước 2 — Sinh code                    │
  │         scenes/theory/TenBai.py       │
  └───────────────────────────────────────┘
              │
              ▼
  ┌───────────────────────────────────────┐
  │ Bước 3 — Render thử                   │
  │         preview (480p / 1 scene)      │
  └───────────────────────────────────────┘
              │
              ▼
  ┌───────────────────────────────────────┐
  │ Bước 4 — Tinh chỉnh                   │
  │         sửa spec hoặc code            │
  └───────────────────────────────────────┘
              │
              ▼
  ┌───────────────────────────────────────┐
  │ Bước 5 — Render xuất bản              │
  │         video 1080p60 + SRT           │
  └───────────────────────────────────────┘
```

---

## Bảng tra nhanh

```
┌───────┬────────────┬──────────────────────────────┬──────────────────────────────────────────────┬──────────────────────────────┐
│ Bước  │ Input      │ Output                       │ Skill chính                                  │ Rule                         │
├───────┼────────────┼──────────────────────────────┼──────────────────────────────────────────────┼──────────────────────────────┤
│ 0     │ —          │ Thư mục theory/              │ —                                            │ —                            │
│ 1     │ Ảnh sách   │ spec-ly-thuyet.md            │ manim-spec-ly-thuyet                         │ —                            │
│ 2G    │ Spec (HH)  │ .py                          │ manim-build-ly-thuyet (SKILL-geometry.md)    │ manim-global.mdc             │
│       │            │                              │ + manim-theory-blocks                        │ manim-theory.mdc             │
│       │            │                              │ + manim-theory-layout                        │                              │
│ 2A    │ Spec (ĐS)  │ .py                          │ manim-build-ly-thuyet-algebra (SKILL-alg.md) │ manim-global.mdc             │
│       │            │                              │ + theory-blocks, theory-layout, design-tokens  │ manim-theory.mdc             │
│       │            │                              │ + C1 (khi figure ≠ none); A1 (giải PT từng bước) │                           │
│ 3     │ .py        │ Video thử                    │ —                                            │ —                            │
│ 4     │ Video thử  │ .py / spec sửa               │ Theo loại lỗi (xem Bước 4)                   │ manim-theory.mdc             │
│ 5     │ .py        │ MP4 + SRT                    │ —                                            │ —                            │
└───────┴────────────┴──────────────────────────────┴──────────────────────────────────────────────┴──────────────────────────────┘
```

---

## Bước 0 — Chuẩn bị thư mục (làm 1 lần / mỗi bdr bài)

### Việc cần làm

Tạo cấu trúc thư mục cho từng bài lý thuyết:

```
specs/theory/bai-3-tu-giac-noi-tiep/
    spec-ly-thuyet.md

scenes/theory/
    Bai3TuGiacNoiTiep.py
```

**Quy ước quan trọng:** File Python đặt trong `scenes/theory/` để rule `manim-theory.mdc` tự áp dụng (`globs: **/theory/**/*.py`).

### Skill / Rule

```
┌───────┬──────┬────────────────────────────────────────────────────────────┐
│ Loại  │ Tên  │ Ghi chú                                                    │
├───────┼──────┼────────────────────────────────────────────────────────────┤
│ —     │ —    │ Không cần gọi skill; chỉ cần đúng cấu trúc thư mục         │
└───────┴──────┴────────────────────────────────────────────────────────────┘
```

---

## Bước 1 — Từ ảnh → `spec-ly-thuyet.md`

### Việc cần làm

1. Chuẩn bị ảnh trang sách (Định nghĩa / Định lí / Nhận xét / …).
2. Gửi ảnh cho agent kèm yêu cầu tạo spec.
3. Duyệt spec: narration, chia scene, `figure.build`, `cleanup`.
4. Sửa spec nếu cần trước khi sang Bước 2.

### Prompt gợi ý

```
Dùng skill manim-spec-ly-thuyet.
Từ ảnh đính kèm, tạo file specs/theory/[ten-bai]/spec-ly-thuyet.md
cho bài [TÊN BÀI].
Chia scene theo từng mục (Định nghĩa / Định lí / Nhận xét).
Ghi đủ: narration, figure.build, animations, cleanup.

Chỉ thêm figure khi ảnh SGK có hình vẽ tương ứng.
Nếu trang chỉ có text/công thức → figure.type = none cho mọi scene.
Không tự thêm đồ thị parabol chỉ vì nội dung có phương trình bậc hai.
```

### Skill áp dụng

```
┌─────────────────────────┬──────────────────────────────────────────────────────────────┐
│ Skill                   │ Vai trò                                                      │
├─────────────────────────┼──────────────────────────────────────────────────────────────┤
│ manim-spec-ly-thuyet    │ Skill chính — nhận dạng block, chia scene, viết narration,   │
│                         │ template spec                                                │
└─────────────────────────┴──────────────────────────────────────────────────────────────┘
```

### Skill KHÔNG dùng

```
┌─────────────────────────────────────┬────────────────────────────────────────────────────┐
│ Skill                               │ Lý do                                              │
├─────────────────────────────────────┼────────────────────────────────────────────────────┤
│ manim-step-1-scene-spec-hinh-hoc    │ Dành cho bài toán (GT/KL/chứng minh)               │
│ manim-step-1-scene-spec-dai-so      │ Dành cho bài toán đại số                           │
│ manim-build-ly-thuyet               │ Chưa có spec thì chưa code                         │
└─────────────────────────────────────┴────────────────────────────────────────────────────┘
```

### Output mong đợi

File `spec-ly-thuyet.md` chứa:

- `lesson_title`, `subject`, `total_scenes`, `estimated_duration`
- Mỗi scene:
  - `method` (vd. `scene01_dinhNghia`)
  - `block_type` (`dinh_nghia` | `dinh_li` | `he_qua` | `nhan_xet` | `chu_y` | `vi_du` | `bai_tap`)
  - `heading`, `body_lines`, `formulas`, `terms_bold`
  - `figure.type` (`geometry` | `function` | `dual_geometry` | `table` | `none`)
  - `figure.build` (thứ tự dựng hình)
  - `narration`, `animations`, `cleanup`

### Checklist tự kiểm tra spec

- [ ] Mỗi mục sách (1, 2, 3…) tương ứng 1 scene (hoặc có lý do tách/gộp)
- [ ] `figure.build` ghi thứ tự dựng hình rõ (circle → points → edges → labels)
- [ ] Scene tái dùng hình ghi `cleanup: keep figure_group`
- [ ] Narration không chứa ký hiệu toán (∠, °, AB liền nhau)
- [ ] Không có GT/KL, proof_steps, ProofLine trong spec

---

## Bước 2 — Từ spec → file Python Manim

### Việc cần làm

1. Gửi `spec-ly-thuyet.md` + yêu cầu sinh code.
2. Agent sinh file `scenes/theory/TenBai.py`.
3. Kiểm tra nhanh: import, TeX template, không có ProofLine/GT/KL.

### Prompt gợi ý

```
Dùng skill manim-build-ly-thuyet.
Đọc specs/theory/[ten-bai]/spec-ly-thuyet.md (subject: geometry),
sinh file scenes/theory/[TenBai].py.
Áp dụng manim-theory-blocks và manim-theory-layout.
Dùng manim-design-tokens (không hardcode màu/timing).
Nếu có hình học: dùng manim-theory-figure-geometry
  (→ manim-hinh-phang + manim-geometry-engine).
Cuối figure.build phải gọi place_figure() hoặc place_dual_figures().
```

### Skill áp dụng

```
┌─────────────────────────────────┬────────────────────────────────────────────────────────────┐
│ Skill                           │ Vai trò                                                    │
├─────────────────────────────────┼────────────────────────────────────────────────────────────┤
│ manim-build-ly-thuyet           │ Skill chính — đọc spec geometry, sinh class + scene methods │
│ manim-theory-blocks             │ Pattern code cho 7 loại block                              │
│ manim-theory-layout             │ TheoryColumn, place_figure, place_dual_figures             │
│ manim-design-tokens             │ COLOR_*, TIMING_*, LAYER_* — không hardcode                │
│ manim-theory-figure-geometry    │ Orchestrate hình hình học → hinh-phang + geometry-engine   │
│ manim-hinh-phang                │ figure.type = geometry — tọa độ, circle, polygon, labels   │
│ manim-geometry-engine           │ Góc, Indicate cặp góc, AngleMarker                         │
└─────────────────────────────────┴────────────────────────────────────────────────────────────┘
```

### Rule áp dụng (tự load khi mở file `.py`)

```
┌─────────────────────┬──────────────────────────────────────────────────────────────────────┐
│ Rule                │ Phạm vi                                                              │
├─────────────────────┼──────────────────────────────────────────────────────────────────────┤
│ manim-global.mdc    │ **/*.py — TeX VN, VoiceoverScene, voiceover, palette                 │
│ manim-theory.mdc    │ **/theory/**/*.py — cấm ProofLine, GT/KL, persistent_geom            │
└─────────────────────┴──────────────────────────────────────────────────────────────────────┘
```

### Helper code (import)

```python
from manim_helpers import (
    TheoryColumn, place_figure, place_dual_figures,
    COLOR_DEFAULT, COLOR_BACKGROUND, COLOR_CIRCLE,
    COLOR_EQUAL_1, COLOR_EQUAL_2, COLOR_ACTIVE,
    TIMING_INDICATE_SEGMENT, TIMING_FADE,
)
```

File helper: `manim_helpers/theory_helpers.py`

### Skill KHÔNG dùng

```
┌──────────────────────────────────────┬──────────────────────────────────────────────────────────┐
│ Skill                                │ Lý do                                                    │
├──────────────────────────────────────┼──────────────────────────────────────────────────────────┤
│ manim-build-ly-thuyet-algebra        │ Dành cho subject: algebra                                │
│ manim-step-2-build-scenes            │ Pipeline bài toán                                        │
│ manim-proof-sync                     │ Không có bookmark proof token                            │
│ manim-layout-system                  │ Dùng ProofColumn — không phù hợp lý thuyết               │
│ manim-scene-lifecycle                │ Lifecycle bài toán; lý thuyết theo manim-theory.mdc §5   │
│ manim-theory-figure-algebra        │ Dành cho subject: algebra                                │
│ manim-algebra-step-solver          │ Dành cho subject: algebra                                │
│ manim-problem-circle-tangent         │ Pattern bài toán — manim/patterns/circle-tangent/        │
│ manim-problem-inscribed-angle        │ Pattern bài toán — manim/patterns/inscribed-angle/       │
│ manim-problem-triangle-congruence    │ Pattern bài toán — manim/patterns/triangle-congruence/   │
└──────────────────────────────────────┴──────────────────────────────────────────────────────────┘
```

### Output mong đợi

File Python với cấu trúc:

```python
class TenBaiLyThuyet(VoiceoverScene):
    def construct(self):
        self.set_speech_service(GTTSService(lang="vi", transcription_model="base"))
        self.setup_scene_style()
        self.scene00_intro()      # optional
        self.scene01_dinhNghia()
        self.scene02_dinhLi()
        self.scene03_nhanXet()
        # ...
```

---

## Bước 2A — Từ spec ĐẠI SỐ → file Python Manim

> Dùng khi `spec-ly-thuyet.md` có `subject: algebra`.

### Việc cần làm

1. Gửi `spec-ly-thuyet.md` (subject: algebra) + yêu cầu sinh code.
2. Agent sinh file `scenes/theory/TenBai.py`.
3. Kiểm tra nhanh: import đúng, C1 route đúng `figure.type`, không có ProofLine/GT/KL.

### Prompt gợi ý

```
Dùng skill manim-build-ly-thuyet-algebra.
Đọc specs/theory/[ten-bai]/spec-ly-thuyet.md (subject: algebra),
sinh file scenes/theory/[TenBai].py.
Áp dụng manim-theory-blocks, manim-theory-layout, manim-design-tokens.
Khi block có figure (figure.type ≠ none): dùng manim-theory-figure-algebra —
  skill này tự định tuyến primitive theo figure.type trong spec.
Khi spec có giải phương trình/BPT từng bước: thêm manim-algebra-step-solver (A1).
```

> **Không cần** liệt kê A2–B2 trong prompt — C1 đã chứa bảng routing; gọi tên từng primitive dễ khiến agent đọc thừa skill.

### Skill áp dụng

**Luôn gọi:**

```
┌───────────────────────────────┬──────────────────────────────────────────────────────────────┐
│ Skill                         │ Vai trò                                                      │
├───────────────────────────────┼──────────────────────────────────────────────────────────────┤
│ manim-build-ly-thuyet-algebra │ Skill chính — đọc spec algebra, sinh class + scene methods   │
│ manim-theory-blocks           │ Pattern code cho 7 loại block                                │
│ manim-theory-layout           │ TheoryColumn; place_figure khi có hình                       │
│ manim-design-tokens           │ COLOR_*, TIMING_*, LAYER_* — không hardcode                  │
└───────────────────────────────┴──────────────────────────────────────────────────────────────┘
```

**Khi `figure.type ≠ none` — thêm:**

```
┌──────────────────────────────────┬──────────────────────────────────────────────────────────────┐
│ Skill                            │ Vai trò                                                      │
├──────────────────────────────────┼──────────────────────────────────────────────────────────────┤
│ manim-theory-figure-algebra (C1) │ Orchestrate — tự chọn A2/A3/B1/B2 theo figure.type         │
└──────────────────────────────────┴──────────────────────────────────────────────────────────────┘
```

**Khi có giải PT/BPT từng bước — thêm (không phải mọi bài đại số):**

```
┌───────────────────────────────┬──────────────────────────────────────────────────────────────┐
│ Skill                         │ Vai trò                                                      │
├───────────────────────────────┼──────────────────────────────────────────────────────────────┤
│ manim-algebra-step-solver (A1)│ Layout giải dọc, TransformMatchingTex — độc lập với C1       │
└───────────────────────────────┴──────────────────────────────────────────────────────────────┘
```

### Tra cứu routing (C1 — không cần paste vào prompt)

```
┌───────────────────┬───────────────────────┬─────────────────────────────────────────────────────┐
│ figure.type       │ Ai xử lý              │ Mô tả                                               │
├───────────────────┼───────────────────────┼─────────────────────────────────────────────────────┤
│ none              │ theory-layout         │ TheoryColumn full width — không gọi C1              │
│ number_line       │ C1 → number-line (A2) │ Trục số, shade vùng, điểm mở ○ / đóng ●             │
│ function          │ C1 → coordinate-plane │ Axes 2D, plot_linear/quadratic, giao điểm           │
│ fraction          │ C1 → fraction-visual  │ FractionBar / FractionPie, quy đồng/rút gọn         │
│ identity          │ C1 → identity-figure  │ Hình ô diện tích (a+b)², (a-b)², (a+b)(a-b)        │
│ (giải PT từng bước)│ A1 (riêng)           │ Gọi thêm manim-algebra-step-solver — không qua C1   │
└───────────────────┴───────────────────────┴─────────────────────────────────────────────────────┘
```

### Helper code — import cơ bản

```python
from manim_helpers import (
    TheoryColumn, make_gtts_service,
    COLOR_DEFAULT, COLOR_BACKGROUND, COLOR_EQUAL_1,
    MOTION_ENTER, MOTION_EXIT, TIMING_FADE,
)
from manim_helpers.theory_helpers import place_figure
# Helper algebra cụ thể (shade_region, plot_linear, FractionBar, …):
# import theo hướng dẫn trong C1 hoặc A1 — không import hết một lần.
```

### Skill KHÔNG dùng cho algebra

```
┌──────────────────────────────────┬──────────────────────────────────────────────────────────────┐
│ Skill                            │ Lý do                                                        │
├──────────────────────────────────┼──────────────────────────────────────────────────────────────┤
│ manim-build-ly-thuyet            │ Dành cho subject: geometry                                   │
│ manim-hinh-phang                 │ Dành cho hình học phẳng                                      │
│ manim-geometry-engine            │ Góc/cạnh hình học — không dùng trong đại số                  │
│ manim-step-2-build-scenes        │ Pipeline bài toán                                            │
│ manim-proof-sync                 │ Không có bookmark proof token                                │
│ manim-layout-system              │ Dùng ProofColumn — không phù hợp lý thuyết                   │
│ manim-scene-lifecycle            │ Lifecycle bài toán                                           │
│ manim-problem-*                  │ Pattern bài toán — manim/patterns/                           │
└──────────────────────────────────┴──────────────────────────────────────────────────────────────┘
```

---

## Bước 3 — Render thử (preview)

### Việc cần làm

Render 1 scene hoặc cả bài ở chất lượng thấp để kiểm tra nhanh.

### Lệnh render

```bash
# Preview 1 scene
manim -pql scenes/theory/Bai3TuGiacNoiTiep.py scene01_dinhNghia

# Preview cả bài
manim -pql scenes/theory/Bai3TuGiacNoiTiep.py TenBaiLyThuyet
```

```
┌───────┬──────────────────────────────────────────────┐
│ Flag  │ Ý nghĩa                                      │
├───────┼──────────────────────────────────────────────┤
│ -p    │ Tự mở video sau render                       │
│ -q    │ Quality: l = 480p (nhanh), m = 720p, h = 1080p │
│ -l    │ Low quality (480p15)                         │
└───────┴──────────────────────────────────────────────┘
```

### Skill / Rule

Không cần skill — chỉ chạy Manim CLI.

### Checklist sau preview

- [ ] Text không tràn / không chồng lên hình
- [ ] Hình nằm đúng FigurePanel bên phải (`place_figure` đã gọi?)
- [ ] TeX tiếng Việt không lỗi (có `tex_template=viet_tex_template`?)
- [ ] Voiceover khớp thời lượng animation
- [ ] Góc `Indicate` đúng cặp (quadrant đúng?)
- [ ] FadeOut cuối scene đúng theo spec `cleanup`

---

## Bước 4 — Tinh chỉnh (nếu preview có lỗi)

### Việc cần làm

1. Ghi lại lỗi cụ thể (scene nào, đối tượng nào).
2. Sửa code hoặc quay lại sửa spec rồi build lại (Bước 2).
3. Render lại scene bị lỗi.

### Prompt gợi ý

```
Scene [NN]: [mô tả lỗi].
Sửa theo skill [tên skill phù hợp].
Giữ đúng manim-theory.mdc — không thêm ProofLine/GT/KL.
```

### Skill theo loại lỗi

```
┌─────────────────────────────────────┬──────────────────────────────────────────────────────────────┐
│ Loại lỗi                            │ Skill dùng                                                   │
├─────────────────────────────────────┼──────────────────────────────────────────────────────────────┤
│ Màu, timing, z-index sai            │ manim-design-tokens                                          │
│ Góc sai quadrant, highlight hình    │ manim-geometry-engine + manim-hinh-phang                     │
│ Text drift, layout lệch             │ manim-theory-layout                                          │
│ Block animation không đúng pattern  │ manim-theory-blocks                                          │
│ Animation chưa mượt                 │ manim-step-3-refine-effects (phần chung; bỏ phần proof)      │
│ Narration / chia scene sai          │ Quay lại Bước 1 — manim-spec-ly-thuyet                       │
│ Cấu trúc class/method sai           │ manim-theory.mdc + manim-build-ly-thuyet                     │
└─────────────────────────────────────┴──────────────────────────────────────────────────────────────┘
```

> **Lưu ý:** Chưa có skill `manim-refine-theory` riêng. Dùng `manim-step-3-refine-effects` (`manim/workflows/bai-toan/3-refine/`) cho hiệu ứng chung (Indicate, FadeOut, timing); bỏ mục proof/bookmark.

---

## Bước 5 — Render xuất bản

### Việc cần làm

Render chất lượng cao sau khi preview ổn.

### Lệnh render

```bash
manim -pqh scenes/theory/Bai3TuGiacNoiTiep.py TenBaiLyThuyet
```

### Output

```
┌─────────────┬──────────────────────────────────────────────────────────────┐
│ File        │ Vị trí                                                       │
├─────────────┼──────────────────────────────────────────────────────────────┤
│ Video MP4   │ media/videos/[TenFile]/1080p60/[ClassName].mp4               │
│ Phụ đề SRT  │ media/videos/[TenFile]/1080p60/[ClassName].srt               │
└─────────────┴──────────────────────────────────────────────────────────────┘
```

---

## Phân nhánh theo loại nội dung

```
  Ảnh đầu vào
      │
      ├─ subject: geometry
      │     │
      │     ├─ Hình học phẳng (đường tròn, tam giác, tứ giác)
      │     │     figure.type = geometry
      │     │     Bước 2G: manim-theory-figure-geometry
      │     │               → manim-hinh-phang + manim-geometry-engine
      │     │
      │     └─ Nhận xét có 2 hình (HCN + HV...)
      │           figure.type = dual_geometry
      │           Bước 2G: place_dual_figures() từ manim-theory-layout
      │
      └─ subject: algebra
            │
            ├─ Text + công thức, không hình
            │     figure.type = none
            │     Bước 2A: TheoryColumn full width
            │     (+ manim-algebra-step-solver nếu có giải PT/BPT từng bước)
            │
            └─ Có hình (trục số, đồ thị, phân số, HĐT)
                  figure.type = number_line | function | fraction | identity
                  Bước 2A: manim-theory-figure-algebra (C1 tự chọn A2–B2)
```

---

## Ví dụ thực tế: Bài 3 — Tứ giác nội tiếp (Hình học)

```
┌───┬──────────────────────────────────────┬──────────────────────────────────────────────────────────────┐
│ # │ Bạn làm                              │ Agent / lệnh dùng                                            │
├───┼──────────────────────────────────────┼──────────────────────────────────────────────────────────────┤
│ 1 │ Gửi ảnh trang sách                   │ manim-spec-ly-thuyet → spec-ly-thuyet.md (subject: geometry) │
│ 2 │ Duyệt spec, sửa narration nếu cần    │ —                                                            │
│ 3 │ "Sinh code từ spec"                  │ manim-build-ly-thuyet + theory-blocks + theory-layout        │
│   │                                      │ + manim-theory-figure-geometry → hinh-phang                  │
│ 4 │ manim -pql ... scene01_dinhNghia     │ —                                                            │
│ 5 │ manim -pql ... scene02_dinhLi        │ —                                                            │
│ 6 │ Báo lỗi (nếu có)                     │ manim-geometry-engine / manim-step-3-refine-effects          │
│ 7 │ manim -pqh ... TenBaiLyThuyet        │ —                                                            │
└───┴──────────────────────────────────────┴──────────────────────────────────────────────────────────────┘
```

**Scene dự kiến:**

```
┌───────┬──────────────┬──────────────────────────────────────────────────────────────┐
│ Scene │ Block        │ Nội dung                                                     │
├───────┼──────────────┼──────────────────────────────────────────────────────────────┤
│ 00    │ intro        │ Tiêu đề bài + I. TÓM TẮT LÝ THUYẾT                           │
│ 01    │ dinh_nghia   │ Tứ giác nội tiếp + hình ABCD trên đường tròn                 │
│ 02    │ dinh_li      │ Tổng góc đối = 180° + Indicate cặp góc                       │
│ 03    │ nhan_xet     │ HCN + HV + DualFigurePanel                                   │
└───────┴──────────────┴──────────────────────────────────────────────────────────────┘
```

---

## Ví dụ thực tế: Hàm số bậc nhất (Đại số lớp 7)

```
┌───┬──────────────────────────────────────┬──────────────────────────────────────────────────────────────┐
│ # │ Bạn làm                              │ Agent / lệnh dùng                                            │
├───┼──────────────────────────────────────┼──────────────────────────────────────────────────────────────┤
│ 1 │ Gửi ảnh trang sách                   │ manim-spec-ly-thuyet → spec-ly-thuyet.md (subject: algebra)  │
│ 2 │ Duyệt spec: figure_type=function     │ —                                                            │
│ 3 │ "Sinh code từ spec"                  │ manim-build-ly-thuyet-algebra + theory-blocks/layout       │
│   │                                      │ + manim-theory-figure-algebra (C1)                         │
│ 4 │ manim -pql ... scene01_dinhNghia     │ —                                                            │
│ 5 │ manim -pql ... scene02_dinhLi        │ —                                                            │
│ 6 │ Báo lỗi (nếu có)                     │ manim-coordinate-plane / manim-step-3-refine-effects         │
│ 7 │ manim -pqh ... TenBaiLyThuyet        │ —                                                            │
└───┴──────────────────────────────────────┴──────────────────────────────────────────────────────────────┘
```

**Scene dự kiến:**

```
┌───────┬──────────────┬──────────────────────────────────────────────────────────────┐
│ Scene │ Block        │ Nội dung                                                     │
├───────┼──────────────┼──────────────────────────────────────────────────────────────┤
│ 00    │ intro        │ Tiêu đề bài + I. TÓM TẮT LÝ THUYẾT                           │
│ 01    │ dinh_nghia   │ Định nghĩa hàm số bậc nhất y = ax + b (a ≠ 0)               │
│ 02    │ dinh_li      │ Tính đơn điệu + bảng giá trị + đồ thị tuyến tính             │
│ 03    │ nhan_xet     │ Giao điểm với trục tọa độ + plot_linear (A3)                  │
└───────┴──────────────┴──────────────────────────────────────────────────────────────┘
```

---

## Danh mục skill & rule (tham chiếu)

### Rules (`.cursor/rules/`)

```
┌─────────────────────┬──────────────────────────────────────────────────────────────┐
│ File                │ Áp dụng khi                                                  │
├─────────────────────┼──────────────────────────────────────────────────────────────┤
│ manim-global.mdc    │ Mọi file **/*.py                                             │
│ manim-theory.mdc    │ File **/theory/**/*.py                                       │
└─────────────────────┴──────────────────────────────────────────────────────────────┘
```

### Skills pipeline lý thuyết (`.cursor/skills/`)

Cấu trúc thư mục (Plan D): `manim/workflows/`, `manim/primitives/`, `manim/patterns/`.

```
┌──────────────────────────────────┬─────────────────────┬──────────────────────────────────────────────────┐
│ Skill (name)                     │ Bước                │ Đường dẫn                                        │
├──────────────────────────────────┼─────────────────────┼──────────────────────────────────────────────────┤
│ manim-spec-ly-thuyet             │ 1                   │ manim/workflows/ly-thuyet/1-spec/                │
│ manim-build-ly-thuyet            │ 2G (geometry)       │ manim/workflows/ly-thuyet/2-build/SKILL-geo.md   │
│ manim-build-ly-thuyet-algebra    │ 2A (algebra)        │ manim/workflows/ly-thuyet/2-build/SKILL-alg.md   │
│ manim-theory-blocks              │ 2G, 2A              │ manim/primitives/theory-blocks/                  │
│ manim-theory-layout              │ 2G, 2A, 4           │ manim/primitives/theory-layout/                  │
│ manim-design-tokens              │ 2G, 2A, 4           │ manim/primitives/design-tokens/                  │
│ manim-hinh-phang                 │ 2G, 4 (hình học)    │ manim/primitives/hinh-phang/                     │
│ manim-geometry-engine            │ 2G, 4 (highlight)   │ manim/primitives/geometry-engine/                │
│ manim-hinh-3d                    │ 2G (3D)             │ manim/primitives/hinh-3d/                        │
│ manim-theory-figure-geometry     │ 2G (figure HH)      │ manim/primitives/theory-figure/geometry/         │
│ manim-theory-figure-algebra (C1) │ 2A (figure ≠ none)  │ manim/primitives/theory-figure/algebra/          │
│ manim-algebra-step-solver (A1)   │ 2A (giải PT từng bước) │ manim/primitives/algebra/step-solver/       │
│ manim-number-line (A2)           │ qua C1              │ manim/primitives/algebra/number-line/            │
│ manim-coordinate-plane (A3)      │ qua C1              │ manim/primitives/algebra/coordinate-plane/       │
│ manim-fraction-visual (B1)       │ qua C1              │ manim/primitives/algebra/fraction-visual/        │
│ manim-identity-figure (B2)       │ qua C1              │ manim/primitives/algebra/identity-figure/        │
│ manim-step-3-refine-effects      │ 4                   │ manim/workflows/bai-toan/3-refine/               │
└──────────────────────────────────┴─────────────────────┴──────────────────────────────────────────────────┘
```

### Skills KHÔNG dùng cho lý thuyết

```
┌────────────────────────────────────┬────────────────────────────────────────────────────────────┐
│ Skill (name)                       │ Đường dẫn                                                  │
├────────────────────────────────────┼────────────────────────────────────────────────────────────┤
│ manim-step-1-scene-spec-hinh-hoc   │ manim/workflows/bai-toan/1-spec/SKILL-hinh-hoc.md          │
│ manim-step-1-scene-spec-dai-so     │ manim/workflows/bai-toan/1-spec/SKILL-dai-so.md            │
│ manim-step-2-build-scenes          │ manim/workflows/bai-toan/2-build/                        │
│ manim-proof-sync                   │ manim/primitives/proof-sync/                               │
│ manim-layout-system                │ manim/primitives/layout-system/                            │
│ manim-scene-lifecycle              │ manim/primitives/scene-lifecycle/                          │
│ manim-problem-circle-tangent       │ manim/patterns/circle-tangent/                             │
│ manim-problem-inscribed-angle      │ manim/patterns/inscribed-angle/                            │
│ manim-problem-triangle-congruence  │ manim/patterns/triangle-congruence/                        │
└────────────────────────────────────┴────────────────────────────────────────────────────────────┘
```

---

## Ghi chú

- Skill nằm dưới `.cursor/skills/manim/` — tên gọi trong prompt vẫn là `name:` trong YAML (vd. `manim-spec-ly-thuyet`), không phải tên thư mục.
- **Figure plug-in đã có:** `manim-theory-figure-geometry` (hình học) và `manim-theory-figure-algebra` (đại số, C1 tự chọn A2–B2). Prompt chỉ cần gọi C1 — không paste bảng routing. `manim-algebra-step-solver` (A1) gọi riêng khi có giải PT từng bước.
- Workflow `ly-thuyet/2-build/` nay có **hai file**: `SKILL-geometry.md` (hình học) và `SKILL-algebra.md` (đại số). Chọn đúng theo `subject:` trong spec.
- Kiến trúc & pipeline bài toán: `Build_video_baigiang_workflow.md`.
- Helper layout lý thuyết: `manim_helpers/theory_helpers.py` (`TheoryColumn`, `place_figure`, `place_dual_figures`).
- Cây thư mục skill đầy đủ: `.cursor/skills/README.md`.
