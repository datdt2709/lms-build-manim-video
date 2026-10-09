# Build Video Bài Giảng — Kiến trúc skill & pipeline

> Tài liệu thiết kế: map skill ↔ thư mục sau refactor (Plan D).  
> **Thực hành lý thuyết:** xem `Quy_trinh_video_ly_thuyet.md`.  
> **Tra cây thư mục:** xem `.cursor/skills/README.md`.

---

## Cấu trúc `.cursor/skills/` (hiện tại)

```
skills/
├── README.md
├── manim/
│   ├── workflows/
│   │   ├── bai-toan/
│   │   │   ├── 1-spec/       SKILL-hinh-hoc.md, SKILL-dai-so.md
│   │   │   ├── 2-build/      SKILL.md
│   │   │   └── 3-refine/     SKILL.md
│   │   └── ly-thuyet/
│   │       ├── 1-spec/       SKILL.md
│   │       └── 2-build/      SKILL-algebra.md, SKILL-geometry.md
│   ├── primitives/
│   │   ├── design-tokens/
│   │   ├── scene-lifecycle/
│   │   ├── geometry-engine/
│   │   ├── hinh-phang/
│   │   ├── hinh-3d/
│   │   ├── proof-sync/
│   │   ├── layout-system/
│   │   ├── theory-layout/
│   │   ├── theory-blocks/
│   │   ├── algebra/
│   │   │   ├── step-solver/
│   │   │   ├── number-line/
│   │   │   ├── coordinate-plane/
│   │   │   ├── fraction-visual/
│   │   │   └── identity-figure/
│   │   └── theory-figure/
│   │       ├── algebra/
│   │       └── geometry/
│   └── patterns/
│       ├── circle-tangent/
│       ├── inscribed-angle/
│       └── triangle-congruence/
└── openspec/
    ├── explore/
    ├── propose/
    ├── apply-change/
    └── archive-change/
```

Tên gọi skill (`name:` trong YAML) **không đổi** — agent vẫn dùng `manim-spec-ly-thuyet`, `manim-step-2-build-scenes`, v.v.

---

## Pipeline lý thuyết HÌNH HỌC (đã triển khai)

```
  [Trang sách / PDF / ảnh]
              │
              ▼
  ┌───────────────────────────────────────┐
  │ Step 1: manim-spec-ly-thuyet          │
  │         manim/workflows/ly-thuyet/1-spec/
  └───────────────────────────────────────┘
              │  → spec-ly-thuyet.md (subject: geometry)
              ▼
  ┌───────────────────────────────────────┐
  │ Step 2: manim-build-ly-thuyet         │
  │         manim/workflows/ly-thuyet/2-build/SKILL-geometry.md
  └───────────────────────────────────────┘
              │  + manim-theory-layout      (primitives/theory-layout)
              │  + manim-theory-blocks      (primitives/theory-blocks)
              │  + manim-design-tokens      (primitives/design-tokens)
              │  + figure plug-in (tùy spec):
              │      manim-hinh-phang + manim-geometry-engine (geometry)
              │      manim-theory-figure-geometry (primitives/theory-figure/geometry)
              ▼
  ┌───────────────────────────────────────┐
  │ Step 3–4: render + tinh chỉnh         │
  │         manim-step-3-refine-effects   │  (chung với bài toán;
  │         manim/workflows/bai-toan/3-refine/   bỏ phần proof)
  └───────────────────────────────────────┘
              │
              ▼
         MP4 + SRT
```

## Pipeline lý thuyết ĐẠI SỐ (đã triển khai)

```
  [SGK Đại số / ảnh]
              │
              ▼
  ┌───────────────────────────────────────┐
  │ Step 1: manim-spec-ly-thuyet          │
  │         manim/workflows/ly-thuyet/1-spec/
  └───────────────────────────────────────┘
              │  → spec-ly-thuyet.md (subject: algebra)
              ▼
  ┌───────────────────────────────────────┐
  │ Step 2: manim-build-ly-thuyet-algebra │
  │         manim/workflows/ly-thuyet/2-build/SKILL-algebra.md
  └───────────────────────────────────────┘
              │  + manim-theory-figure-algebra (C1) [routing figure_type]
              │      ├── step-solver (A1)        figure_type: none / equation
              │      ├── number-line (A2)        figure_type: number_line
              │      ├── coordinate-plane (A3)   figure_type: function
              │      ├── fraction-visual (B1)    figure_type: fraction
              │      └── identity-figure (B2)    figure_type: identity
              │  + manim-theory-blocks, manim-theory-layout, manim-design-tokens
              ▼
  ┌───────────────────────────────────────┐
  │ Step 3–4: render + tinh chỉnh         │
  │         manim-step-3-refine-effects   │  (chung; bỏ phần proof)
  └───────────────────────────────────────┘
              │
              ▼
         MP4 + SRT
```

**Rule:** `manim-theory.mdc` (`**/theory/**/*.py`) + `manim-global.mdc` (`**/*.py`).

---

## Pipeline bài toán (đã triển khai)

```
  [Ảnh đề + lời giải]
              │
              ▼
  ┌───────────────────────────────────────┐
  │ Step 1: manim-step-1-scene-spec-hinh-hoc  │  hình phẳng
  │      hoặc manim-step-1-scene-spec-dai-so  │  đại số / HKG
  │         manim/workflows/bai-toan/1-spec/
  └───────────────────────────────────────┘
              │  → scene-spec.md
              ▼
  ┌───────────────────────────────────────┐
  │ Step 2: manim-step-2-build-scenes     │
  │         manim/workflows/bai-toan/2-build/
  └───────────────────────────────────────┘
              │  + manim-hinh-phang hoặc manim-dai-so-hinh-khong-gian
              │  + manim-design-tokens, manim-geometry-engine
              │  + manim-proof-sync, manim-layout-system
              │  + manim-scene-lifecycle
              │  + pattern (nếu khớp): manim-problem-* (manim/patterns/)
              ▼
  ┌───────────────────────────────────────┐
  │ Step 3: manim-step-3-refine-effects   │
  │         manim/workflows/bai-toan/3-refine/
  └───────────────────────────────────────┘
```

---

## Bảng skill — trạng thái & đường dẫn

### Workflow lý thuyết

| Skill (`name:`) | Đường dẫn | Trạng thái |
|-----------------|-----------|------------|
| `manim-spec-ly-thuyet` | `manim/workflows/ly-thuyet/1-spec/` | ✅ |
| `manim-build-ly-thuyet` | `manim/workflows/ly-thuyet/2-build/SKILL-geometry.md` | ✅ |
| `manim-build-ly-thuyet-algebra` | `manim/workflows/ly-thuyet/2-build/SKILL-algebra.md` | ✅ |
| `manim-theory-layout` | `manim/primitives/theory-layout/` | ✅ |
| `manim-theory-blocks` | `manim/primitives/theory-blocks/` | ✅ |
| `manim-refine-theory` | — | ❌ chưa có — dùng `manim-step-3-refine-effects` |
| `manim-theory-lifecycle` | — | ❌ chưa có — quy tắc trong `manim-theory.mdc` §5 |

### Workflow bài toán

| Skill (`name:`) | Đường dẫn | Trạng thái |
|-----------------|-----------|------------|
| `manim-step-1-scene-spec-hinh-hoc` | `manim/workflows/bai-toan/1-spec/SKILL-hinh-hoc.md` | ✅ |
| `manim-step-1-scene-spec-dai-so` | `manim/workflows/bai-toan/1-spec/SKILL-dai-so.md` | ✅ |
| `manim-step-2-build-scenes` | `manim/workflows/bai-toan/2-build/` | ✅ |
| `manim-step-3-refine-effects` | `manim/workflows/bai-toan/3-refine/` | ✅ |

### Primitives (dùng chéo)

| Skill (`name:`) | Đường dẫn | Phạm vi |
|-----------------|-----------|---------|
| `manim-design-tokens` | `manim/primitives/design-tokens/` | Mọi scene |
| `manim-hinh-phang` | `manim/primitives/hinh-phang/` | Bài toán HH phẳng; lý thuyết có hình |
| `manim-geometry-engine` | `manim/primitives/geometry-engine/` | Highlight góc/cạnh/tam giác |
| `manim-hinh-3d` | `manim/primitives/hinh-3d/` | Hình không gian 3D (ThreeDScene) |
| `manim-proof-sync` | `manim/primitives/proof-sync/` | Chỉ bài toán |
| `manim-layout-system` | `manim/primitives/layout-system/` | `ProofColumn` — bài toán |
| `manim-scene-lifecycle` | `manim/primitives/scene-lifecycle/` | Chủ yếu bài toán |
| `manim-step-solver` | `manim/primitives/algebra/step-solver/` | Lý thuyết đại số: phương trình/bất PT |
| `manim-number-line` | `manim/primitives/algebra/number-line/` | Trục số 1D lớp 6+ |
| `manim-coordinate-plane` | `manim/primitives/algebra/coordinate-plane/` | Axes 2D hàm số lớp 7+ |
| `manim-fraction-visual` | `manim/primitives/algebra/fraction-visual/` | Phân số trực quan lớp 4–6 |
| `manim-identity-figure` | `manim/primitives/algebra/identity-figure/` | Hằng đẳng thức lớp 8 |
| `manim-theory-figure-algebra` | `manim/primitives/theory-figure/algebra/` | Orchestrate routing figure_type → A1–B2 |
| `manim-theory-figure-geometry` | `manim/primitives/theory-figure/geometry/` | Dựng hình hình học cho lý thuyết |

### Patterns bài toán (`manim/patterns/`)

| Skill (`name:`) | Thư mục |
|-----------------|---------|
| `manim-problem-circle-tangent` | `circle-tangent/` |
| `manim-problem-inscribed-angle` | `inscribed-angle/` |
| `manim-problem-triangle-congruence` | `triangle-congruence/` |

Thêm pattern mới: tạo `manim/patterns/<ten-dang-bai>/SKILL.md`, `name:` theo dạng `manim-problem-<ten>`.

---

## Kiến trúc lý thuyết: Shared core + figure plug-in

```
┌─────────────────────────────────────────────────────────────────┐
│                  SHARED THEORY PIPELINE                         │
│                                                                 │
│  Rule: manim-theory.mdc  ←─── **/theory/**/*.py                 │
│  Rule: manim-global.mdc  ←─── **/*.py                           │
│                                                                 │
│  Step 1: manim-spec-ly-thuyet     (manim/workflows/ly-thuyet/1-spec/)
│                                                                 │
│  Core primitives:                                               │
│  ├── manim-theory-blocks          (7 block types)               │
│  ├── manim-theory-layout          (TheoryColumn, FigurePanel)   │
│  └── manim-design-tokens          (COLOR_*, TIMING_*, LAYER_*)  │
└────────────────────┬────────────────────────────────────────────┘
                     │
          ┌──────────┴──────────────────────────┐
          ▼ subject: geometry                    ▼ subject: algebra
┌──────────────────────────┐        ┌──────────────────────────────────┐
│ Step 2 GEOMETRY          │        │ Step 2 ALGEBRA                   │
│ manim-build-ly-thuyet    │        │ manim-build-ly-thuyet-algebra    │
│ (SKILL-geometry.md)      │        │ (SKILL-algebra.md)               │
│                          │        │                                  │
│ Figure plug-ins:         │        │ manim-theory-figure-algebra (C1) │
│ manim-theory-figure-     │        │ ├── step-solver (A1) none/eq     │
│   geometry               │        │ ├── number-line (A2) number_line │
│ manim-hinh-phang         │        │ ├── coordinate-plane (A3) func   │
│ manim-geometry-engine    │        │ ├── fraction-visual (B1) frac    │
└──────────────────────────┘        │ └── identity-figure (B2) ident   │
                                    └──────────────────────────────────┘
```

**Không dùng cho lý thuyết:** `manim-proof-sync`, `manim-layout-system` (`ProofColumn`), `manim-scene-lifecycle` (lifecycle bài toán), các `manim-problem-*`.

---

## Chi tiết skill lý thuyết (đã có)

### `manim-spec-ly-thuyet` (Step 1)

**Input:** ảnh trang sách / mô tả → **Output:** `spec-ly-thuyet.md`

**Khác spec bài toán** (`manim-step-1-scene-spec-hinh-hoc` / `dai-so`):

```
spec bài toán              spec lý thuyết
─────────────────          ─────────────────────────
lesson_type: problem       lesson_type: theory
GT / KL                    lesson_title, section_heading
scenes: CM ý a/b/c         blocks[]: type, heading, body, formulas...
proof_steps[]              narration: giải thích, không suy luận CM
```

**Output spec — trường chính:**

| Trường | Ví dụ |
|--------|-------|
| `lesson_title` | BÀI 3. TỨ GIÁC NỘI TIẾP |
| `section` | I. TÓM TẮT LÝ THUYẾT |
| `blocks[]` | `dinh_nghia` \| `dinh_li` \| `nhan_xet` \| … |
| `figure.type` | `geometry` \| `dual_geometry` \| `function` \| `none` |
| `figure.build` | circle → vertices → edges → labels |
| `narration` | giải thích, không "ta chứng minh" |

---

### `manim-theory-layout`

Bổ sung layout — **không dùng `ProofColumn`**.

| Thành phần | Mô tả |
|------------|-------|
| `TheoryColumn` | heading → text → công thức (gap cố định) |
| `FigurePanel` | một hình bên phải |
| `place_figure()` / `place_dual_figures()` | đặt hình vào panel |

Helper: `manim_helpers/theory_helpers.py`.

---

### `manim-theory-blocks`

Pattern cho 7 loại block: `dinh_nghia`, `dinh_li`, `he_qua`, `nhan_xet`, `chu_y`, `vi_du`, `bai_tap`.

| Block | Animation gợi ý |
|-------|-------------------|
| Định nghĩa | Tiêu đề → text (terms_bold) → figure reveal |
| Định lí | Phát biểu + MathTex → Indicate góc (nếu có) |
| Nhận xét | Bullet / dual figure (HCN + HV) |

---

### `manim-build-ly-thuyet` (Step 2 — Hình học)

- Đọc `spec-ly-thuyet.md` (subject: geometry) → `scene01_dinhNghia`, …
- Import `TheoryColumn` — không `ProofLine`, không `sync_*`
- Voiceover: `Write` / `FadeIn` tuần tự theo block
- Hình: `manim-theory-figure-geometry` → `manim-hinh-phang` + `place_figure()`; góc: `manim-geometry-engine`

### `manim-build-ly-thuyet-algebra` (Step 2 — Đại số)

- Đọc `spec-ly-thuyet.md` (subject: algebra) → `scene01_dinhNghia`, …
- Import `TheoryColumn` — không `ProofLine`, không `sync_*`
- Voiceover: `Write` / `FadeIn` tuần tự theo block
- Hình: `manim-theory-figure-algebra` (C1) routing `figure_type` → A1/A2/A3/B1/B2

---

## Đề xuất tương lai (chưa có skill riêng)

Các mục dưới **chưa** có thư mục trong `.cursor/skills/` — có thể bổ sung sau khi cần lặp lại nhiều lần.

| Đề xuất | Thay thế hiện tại |
|---------|-------------------|
| `manim-inscribed-figures` | Logic trong `manim-hinh-phang` + spec `figure.build` |
| `manim-theory-lifecycle` | `manim-theory.mdc` (FadeOut figure/text) |
| `manim-refine-theory` | `manim-step-3-refine-effects` (bỏ mục proof) |
| Pattern `SKILL-theory-cyclic-quad` | Spec + `manim-hinh-phang`; hoặc thêm `manim/patterns/theory-cyclic-quad/` |

---

## So sánh lý thuyết Hình học vs Đại số

80% pipeline giống nhau (spec → build → blocks → layout). Chỉ **figure plug-in** và **build skill** khác:

| | Hình học | Đại số / hàm số |
|--|----------|-----------------|
| Build skill | `manim-build-ly-thuyet` (SKILL-geometry.md) | `manim-build-ly-thuyet-algebra` (SKILL-algebra.md) |
| Figure routing | `manim-theory-figure-geometry` | `manim-theory-figure-algebra` (C1 → A1–B2) |
| Primitives | `manim-hinh-phang`, `manim-geometry-engine` | `step-solver`, `number-line`, `coordinate-plane`, `fraction-visual`, `identity-figure` |
| Spec | `figure.type: geometry / dual_geometry` | `figure.type: none / number_line / function / fraction / identity` |

---

## Khi nào thêm figure plug-in / pattern mới

| Môn / chủ đề | Figure | Skill hiện tại |
|--------------|--------|----------------|
| Hình phẳng, HKG | Hình học | `manim-theory-figure-geometry` → `manim-hinh-phang` + `manim-geometry-engine` |
| Phương trình, bất PT, hệ PT | Step-by-step | `manim-theory-figure-algebra` → `step-solver` (A1) |
| Trục số, bất PT số | Số nguyên / phân số | `manim-theory-figure-algebra` → `number-line` (A2) |
| Hàm số, đồ thị | Axes 2D | `manim-theory-figure-algebra` → `coordinate-plane` (A3) |
| Phân số lớp 4–6 | FractionBar / Pie | `manim-theory-figure-algebra` → `fraction-visual` (B1) |
| Hằng đẳng thức lớp 8 | Hình ô diện tích | `manim-theory-figure-algebra` → `identity-figure` (B2) |
| Thuần văn + công thức | Không hình | `figure.type: none`, `TheoryColumn` full width |
| Hình không gian 3D | Hộp/cầu/nón/trụ | `manim-hinh-3d` (ThreeDScene) |
| Lượng giác | Unit circle + đồ thị | Mở rộng `coordinate-plane` hoặc pattern mới |
| Tổ hợp, xác suất | Cây / bảng | Pattern mới trong `manim/patterns/` (về sau) |

---

## Rule `manim-theory.mdc`

**Globs:** `**/theory/**/*.py`

| Nhóm | Nội dung |
|------|----------|
| Method | `scene01_dinhNghia`, … — không `scene_CM*`, không GT/KL |
| Block | 7 loại `dinh_nghia` … `bai_tap` |
| Cấm | `ProofLine`, `proof_accumulator`, GT:, KL: |
| Figure | `place_figure()` khi có hình |
| Narration | "Định nghĩa", "Định lí" — không "Chứng minh" |

> Không gộp vào `manim-global.mdc` — tách mode lý thuyết vs bài toán.

---

## Thêm skill mới (quy ước)

| Loại | Đặt tại |
|------|---------|
| Bước workflow mới | `manim/workflows/<bai-toan\|ly-thuyet>/N-<ten>/SKILL.md` |
| Primitive | `manim/primitives/<ten>/SKILL.md` — lý thuyết: prefix `theory-` |
| Pattern bài toán | `manim/patterns/<ten>/SKILL.md`, `name: manim-problem-<ten>` |
| OpenSpec | `openspec/<ten>/SKILL.md` |

Cập nhật `.cursor/skills/README.md` và bảng tra trong `Quy_trinh_video_ly_thuyet.md` khi thêm skill.
