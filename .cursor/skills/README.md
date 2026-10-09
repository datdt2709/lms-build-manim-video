# Cursor Skills — cấu trúc thư mục

Tổ chức theo **Plan D (hybrid)**: `system` → `workflows` / `primitives` / `patterns`.

Tên skill trong frontmatter YAML (`name:`) **không đổi** — agent vẫn gọi `manim-design-tokens`, `manim-spec-ly-thuyet`, v.v.

## Cây thư mục

```
skills/
├── manim/
│   ├── workflows/
│   │   ├── bai-toan/
│   │   │   ├── 1-spec/       SKILL-dai-so.md, SKILL-hinh-hoc.md
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

## Primitives — phạm vi dùng

| Primitive | Mới? | Phục vụ |
|---|---|---|
| `design-tokens` | | **Mọi** scene Manim (dùng chung tuyệt đối) |
| `scene-lifecycle` | | Mọi scene có hình học tích lũy (chủ yếu bài toán) |
| `geometry-engine` | | Bài toán hình học |
| `hinh-phang` | | Bài toán hình phẳng |
| `hinh-3d` | | Hình không gian 3D (ThreeDScene, hộp/cầu/nón/trụ) |
| `proof-sync` | | Bài toán (scene chứng minh) |
| `layout-system` | | Bài toán (`ProofColumn`) |
| `theory-layout` | | **Chỉ** lý thuyết (`TheoryColumn`, `FigurePanel`) |
| `theory-blocks` | | **Chỉ** lý thuyết (7 block types) |
| `algebra/step-solver` | MỚI | Đại số: phương trình / bất PT / hệ PT |
| `algebra/number-line` | MỚI | Trục số 1D lớp 6+ |
| `algebra/coordinate-plane` | MỚI | Axes 2D hàm số lớp 7+ |
| `algebra/fraction-visual` | MỚI | Phân số trực quan lớp 4–6 |
| `algebra/identity-figure` | MỚI | Hằng đẳng thức lớp 8 (hình ô diện tích) |
| `theory-figure/algebra` | MỚI | Orchestrate routing figure_type → A1–B2 cho lý thuyết đại số |
| `theory-figure/geometry` | MỚI | Dựng hình hình học cho lý thuyết |

## Chọn skill nhanh

| Bạn đang làm | Vào thư mục |
|---|---|
| Spec bài toán (ảnh đề → scene-spec.md) | `manim/workflows/bai-toan/1-spec/` |
| Code bài toán từ spec | `manim/workflows/bai-toan/2-build/` |
| Polish animation bài toán | `manim/workflows/bai-toan/3-refine/` |
| Spec lý thuyết (SGK → spec-ly-thuyet.md) | `manim/workflows/ly-thuyet/1-spec/` |
| Code lý thuyết **hình học** từ spec | `manim/workflows/ly-thuyet/2-build/SKILL-geometry.md` |
| Code lý thuyết **đại số** từ spec | `manim/workflows/ly-thuyet/2-build/SKILL-algebra.md` |
| Helper dùng chung (màu, layout, hình, proof) | `manim/primitives/` |
| Figure đại số (trục số, đồ thị, phân số, HĐT) | `manim/primitives/algebra/` |
| Routing figure_type → primitive đại số | `manim/primitives/theory-figure/algebra/` |
| Template dạng bài cụ thể | `manim/patterns/` |
| OpenSpec change | `openspec/` |

## Primitives algebra — cây con A/B/C

Khi `spec.subject == "algebra"`, dùng `theory-figure/algebra` để routing tự động:

| figure_type | Primitive | Ký hiệu |
|---|---|---|
| `none` (đại số thuần, phương trình) | `algebra/step-solver` | A1 |
| `number_line` | `algebra/number-line` | A2 |
| `function` (đồ thị y=f(x)) | `algebra/coordinate-plane` | A3 |
| `fraction` | `algebra/fraction-visual` | B1 |
| `identity` (hằng đẳng thức) | `algebra/identity-figure` | B2 |

Skill orchestrate: `theory-figure/algebra` (C1) — đọc `figure_type` từ spec, gọi đúng A1–B2, áp dụng post-place pattern.

---

## Thêm skill mới

- **Bước pipeline mới** (ví dụ `luyen-tap/`): `manim/workflows/<ten-workflow>/N-<ten>/SKILL.md`
- **Primitive mới**: `manim/primitives/<ten>/SKILL.md` — algebra dùng sub-folder `algebra/`; lý thuyết dùng prefix `theory-`
- **Pattern mới**: `manim/patterns/<ten-dang-bai>/SKILL.md`
