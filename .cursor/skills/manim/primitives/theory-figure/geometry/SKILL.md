---
name: manim-theory-figure-geometry
description: Dựng hình hình học cho scene bài giảng lý thuyết: 2 hình liên quan (arrange RIGHT), GeometryEngine post-place pattern, sync Indicate với voice. Dùng sau khi đã có spec-ly-thuyet.md và spec.subject == "geometry".
---

# Skill: Manim – Theory Figure (Geometry)

> Dành riêng cho `subject: geometry`. Kết hợp với `manim-theory-blocks` và `manim-theory-layout`.
> Đọc skill này khi spec có `figure.type: geometry` hoặc `figure.type: dual_geometry`.

---

## Section 1: 2 hình LIÊN QUAN (định nghĩa, định lí)

Khi một block có **2 hình phụ thuộc nhau** (cùng minh họa một khái niệm, VD: tam giác cân + trục đối xứng; đường tròn nội tiếp + ngoại tiếp), dùng `place_figure` với một `VGroup` duy nhất:

```python
# ĐÚNG — 2 hình liên quan → single VGroup + place_figure
fig_left  = VGroup(triangle_left, labels_left, ...)   # hình 1
fig_right = VGroup(triangle_right, labels_right, ...)  # hình 2
fig_pair  = VGroup(fig_left, fig_right).arrange(RIGHT, buff=0.3)
place_figure(fig_pair)   # FIG_MAX_W=3.5 → đủ chỗ cho 2 hình

# SAI — KHÔNG dùng place_dual_figures cho 2 hình liên quan
# place_dual_figures bị giới hạn DUAL_FIG_MAX_W=1.55 → hình nhỏ
```

**Khi nào là "liên quan":**
- Cùng minh họa một định nghĩa / định lí (VD: 2 tam giác bằng nhau)
- Một hình là biến thể/ví dụ của hình kia (VD: góc nội tiếp = 2× góc tâm)
- Cần nhìn cả 2 hình cùng lúc để hiểu nội dung

**Khi nào dùng `place_dual_figures`:** → Xem Section 4.

---

## Section 2: GeometryEngine — Critical Post-Place Pattern

`place_figure()` **scale và move_to** toàn bộ VGroup; mọi tọa độ hardcode trước lệnh này sẽ **sai vị trí** sau khi hình dịch chuyển.

### SAI vs ĐÚNG

```python
# ──────────────────────── SAI ────────────────────────
A_pos = np.array([-1.0, 1.5, 0])
dot_A = Dot(A_pos, color=COLOR_EQUAL_1)
figure_group = VGroup(circle, dot_A, ...)
place_figure(figure_group)  # ← move_to dịch chuyển figure_group

# Tọa độ cũ A_pos không đổi, nhưng dot_A đã ở chỗ khác!
geo.register_point("A", A_pos, dot=dot_A)        # ← A_pos stale → SAI
AngleMarker(A_pos, O_pos, B_pos)                 # ← vẽ sai chỗ

# ──────────────────────── ĐÚNG ───────────────────────
A_pos = np.array([-1.0, 1.5, 0])
dot_A = Dot(A_pos, color=COLOR_EQUAL_1)
figure_group = VGroup(circle, dot_A, ...)
place_figure(figure_group)  # ← place xong, các dot đã ở vị trí thực tế

# Register AFTER place_figure, dùng dot.get_center()
geo.register_point("A", dot_A.get_center(), dot=dot_A)   # ← tọa độ thực tế
geo.register_point("B", dot_B.get_center(), dot=dot_B)
geo.register_point("O", dot_O.get_center(), dot=dot_O)
```

### Checklist GeometryEngine cho lý thuyết

```python
# 1. Dựng hình với tọa độ cục bộ (chưa care vị trí màn hình)
circle = Circle(radius=2.2, color=COLOR_CIRCLE)
dot_A  = Dot(A_pos, color=COLOR_EQUAL_1)
# ...

# 2. Gom vào VGroup + place_figure
figure_group = VGroup(circle, dot_A, dot_B, dot_O, ...)
place_figure(figure_group)
self.figure_group = figure_group

# 3. Register GEO POINTS sau place_figure
geo = GeometryEngine()
geo.register_point("A", dot_A.get_center(), dot=dot_A)
geo.register_point("B", dot_B.get_center(), dot=dot_B)
geo.register_point("O", dot_O.get_center(), dot=dot_O)
# ... register tất cả points cần dùng cho AngleMarker / highlight

# 4. Tạo AngleMarker / SegmentMarker SAU khi đã register
sector_A = AngleMarker(geo.point("B"), geo.point("A"), geo.point("C"),
                       color=COLOR_EQUAL_1)
# Thêm sector_A vào scene (FadeIn hoặc Create) khi cần highlight
```

**Lý do quan trọng:** `place_figure()` gọi `scale_to_fit_width` và/hoặc `move_to` → toàn bộ VGroup dịch chuyển và scale. Tọa độ hardcode (e.g. `A_pos = [-1, 1.5, 0]`) chỉ đúng trước khi đặt hình. Sau `place_figure`, chỉ `dot.get_center()` mới trả về tọa độ thực tế.

---

## Section 3: Sync Indicate với Voice

Pattern đồng bộ `AngleMarker` / `SegmentMarker` với voiceover khi đọc tên góc hoặc cạnh:

```python
# Sau place_figure + register geo points:
# Khi voice đọc "góc A bằng góc A phẩy":
with self.voiceover("góc A bằng góc A phẩy...") as ov:
    self.play(Write(formula_angles), run_time=ov.duration * 0.5)
    # Cùng lúc hiện sector góc tương ứng:
    sec_A  = AngleMarker(geo.point("B"), geo.point("A"),  geo.point("C"),
                         color=COLOR_EQUAL_1)
    sec_Ap = AngleMarker(geo.point("Bp"), geo.point("Ap"), geo.point("Cp"),
                         color=COLOR_EQUAL_2)
    self.play(FadeIn(sec_A, sec_Ap), run_time=ov.duration * 0.5)

# Khi voice đọc "cạnh AB bằng cạnh A'B'":
with self.voiceover("cạnh A B bằng cạnh A phẩy B phẩy...") as ov:
    mark_AB  = TickMark(geo.point("A"), geo.point("B"),  n_ticks=1, color=COLOR_EQUAL_1)
    mark_ApBp = TickMark(geo.point("Ap"), geo.point("Bp"), n_ticks=1, color=COLOR_EQUAL_1)
    self.play(FadeIn(mark_AB, mark_ApBp), run_time=ov.duration)

# Indicate trên sector/tick đã tạo:
with self.voiceover("Suy ra hai tam giác bằng nhau...") as ov:
    self.play(
        Indicate(sec_A,    color=COLOR_EQUAL_1, scale_factor=1.2),
        Indicate(sec_Ap,   color=COLOR_EQUAL_2, scale_factor=1.2),
        run_time=ov.duration)
```

**Quy tắc timing:**
- `Write(formula)` + `FadeIn(markers)` trong cùng một `with voiceover`: chia theo `ov.duration * 0.5` / `0.5`
- Nếu chỉ Indicate (không Write thêm): dùng `run_time=ov.duration` toàn bộ
- Tổng hệ số trong 1 block voiceover ≤ 1.0

**Cleanup markers cuối scene:**
```python
# Thêm tất cả markers vào một VGroup để dễ FadeOut
markers = VGroup(sec_A, sec_Ap, mark_AB, mark_ApBp)
# ...
self.play(FadeOut(markers))  # FadeOut cùng với col.all
```

---

## Section 4: DualFigurePanel Scope

`place_dual_figures` **CHỈ dùng** cho `nhan_xet` hoặc `chu_y` có **2 hình ví dụ ĐỘC LẬP**:

```python
# ĐÚNG — 2 hình độc lập, minh họa 2 ví dụ khác nhau
# VD: "Hình chữ nhật và hình vuông đều là tứ giác nội tiếp"
dual_panel = place_dual_figures(
    rect_group, sq_group,
    label_left="Hình chữ nhật", label_right="Hình vuông",
    tex_template=viet_tex_template)
```

| Trường hợp | Dùng |
|---|---|
| 2 hình minh họa **cùng** một định nghĩa/định lí | `place_figure(VGroup(fig1, fig2).arrange(RIGHT, buff=0.3))` |
| 2 hình ví dụ **ĐỘC LẬP** trong `nhan_xet`/`chu_y` | `place_dual_figures(fig_left, fig_right, ...)` |

**Tại sao `DUAL_FIG_MAX_W=1.55`?** Intentional — 2 hình nhỏ vừa panel `FIG_MAX_W=3.5` với buff `DUAL_FIG_BUFF=0.35`. Nếu dùng `place_dual_figures` cho 2 hình liên quan, mỗi hình chỉ rộng 1.55 đơn vị → quá nhỏ, khó nhìn.
