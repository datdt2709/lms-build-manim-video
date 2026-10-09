---
name: manim-step-3-refine-effects
description: Tinh chỉnh animation, đồng bộ nhịp voiceover và thêm hiệu ứng nhấn mạnh cho code Manim đã có. Dùng sau Step 2 để nâng chất lượng mà không phá cấu trúc bài học.
---

# Skill: Manim Step 3 – Tinh Chỉnh Hiệu Ứng

## Mục đích

Nhận **code Manim đã có** (từ Step 2 hoặc draft ban đầu) → Cải thiện chất lượng animation, đồng bộ nhịp với voiceover, thêm hiệu ứng nhấn mạnh, và tinh chỉnh chuyển cảnh mà **không phá vỡ cấu trúc bài học**.

---

## Khi nào dùng skill này?

- Code đã render được nhưng animation trông "phẳng", thiếu điểm nhấn
- Cần thêm hiệu ứng nhấn mạnh cho kết quả quan trọng
- Animation chạy quá nhanh / quá chậm so với lời thuyết minh
- Chuyển cảnh giữa các scene bị giật cục hoặc thiếu mượt
- Cần thêm `Brace`, highlight tạm thời, hoặc focus vào một vùng cụ thể
- Người dùng muốn thay đổi thứ tự reveal hoặc cách trình bày

---

## 1. Hiệu ứng nhấn mạnh (Emphasis Effects)

### Indicate – Nhấn mạnh nhẹ, scale lên rồi về

```python
# Nhấn mạnh một biểu thức / điểm
self.play(Indicate(mob, color=YELLOW, scale_factor=1.2), run_time=0.8)

# Nhấn mạnh nhiều thứ cùng lúc
self.play(
    Indicate(eq[0], color=RED, scale_factor=1.3),
    Indicate(dot_C, color=GREEN, scale_factor=1.5),
    run_time=1.0
)
```

### Flash – Nháy sáng tại một điểm

```python
# Nháy sáng tại điểm (thường dùng cho Dot)
self.play(Flash(dot_C, color=YELLOW, flash_radius=0.4, line_length=0.2))

# Flash + Indicate kết hợp
self.play(Flash(dot_I))
self.play(Indicate(dot_I, scale_factor=2, color=RED))
```

### Circumscribe – Vẽ đường viền xung quanh rồi biến mất

```python
# Viền hình chữ nhật (mặc định)
self.play(Circumscribe(eq_result, color=YELLOW, run_time=1.5))

# Viền hình tròn
self.play(Circumscribe(key_text, shape=Circle, color=RED, run_time=1.2))
```

### FocusOn – Zoom chú ý vào một điểm

```python
self.play(FocusOn(dot_C, color=YELLOW, run_time=1.0))
self.play(FocusOn(result_eq.get_center(), color=GREEN, run_time=0.8))
```

### ApplyWave – Gợn sóng trên text

```python
# Tạo hiệu ứng gợn sóng (dùng cho tiêu đề hoặc kết quả quan trọng)
self.play(ApplyWave(title_text, amplitude=0.1, run_time=1.0))
```

---

## 2. Highlight tạm thời (Temporary Highlight)

### Highlight đoạn thẳng rồi xóa

```python
seg_highlight = Line(I_pos, E_pos, color=YELLOW, stroke_width=6)
self.play(Create(seg_highlight), run_time=0.4)
self.play(Indicate(seg_highlight, color=YELLOW, scale_factor=1.05))
self.play(FadeOut(seg_highlight), run_time=0.3)
```

### Highlight tam giác tạm thời

```python
tri_temp = Polygon(A_pos, B_pos, C_pos, color=YELLOW, fill_opacity=0.35)
self.play(FadeIn(tri_temp), run_time=0.4)
# Hiệu ứng "thở" (phóng to rồi thu về)
self.play(tri_temp.animate.scale(1.08), run_time=0.6, rate_func=there_and_back)
self.play(FadeOut(tri_temp), run_time=0.3)
```

### Highlight phần MathTex cụ thể

```python
# Chia MathTex thành parts để highlight riêng
eq = MathTex(r"x^2", r"-", r"5x", r"+", r"6", r"=", r"0")
# Highlight chỉ phần "-5x"
self.play(eq[2].animate.set_color(YELLOW))
self.wait(0.5)
self.play(eq[2].animate.set_color(WHITE))  # Trả về màu gốc
```

---

## 3. Chuyển cảnh mượt (Smooth Transitions)

### FadeOut + Write (chuyển cảnh cơ bản)

```python
# Dọn dẹp scene cũ trước
self.play(FadeOut(VGroup(old_title, old_proof, old_temp)))
self.wait(0.5)
# Hiện scene mới
self.play(Write(new_title))
```

### ReplacementTransform (thay thế hoàn toàn)

```python
# Dùng khi muốn Mobject cũ "biến thành" Mobject mới
self.play(ReplacementTransform(old_text, new_text), run_time=1.0)
```

### AnimatedBoundary – Đường viền chạy liên tục

```python
# Dùng để thu hút chú ý trong khi giải thích
boundary = AnimatedBoundary(result_group, colors=[YELLOW, GREEN, BLUE])
self.add(boundary)
self.wait(2)  # Chạy 2 giây
self.remove(boundary)
```

### Chuyển cảnh có chiều sâu (FadeOut + di chuyển)

```python
# Scene cũ trượt ra, scene mới trượt vào
self.play(
    old_group.animate.shift(LEFT * 8),
    run_time=0.6
)
self.play(
    new_group.animate.shift(RIGHT * 0 + LEFT * 0),  # đã ở vị trí đúng
    run_time=0.6
)
```

---

## 4. Điều chỉnh tốc độ (Pacing)

### rate_func – Hàm tốc độ animation

```python
# Tuyến tính (mặc định)
self.play(Create(line), rate_func=linear, run_time=1.0)

# Smooth (tăng tốc đầu, giảm tốc cuối) - mặc định của Manim
self.play(Write(text), rate_func=smooth, run_time=1.0)

# Phóng to rồi thu về (dùng cho Indicate thủ công)
self.play(mob.animate.scale(1.2), rate_func=there_and_back, run_time=0.8)

# Giảm dần (ease_out)
self.play(mob.animate.shift(UP), rate_func=rush_from, run_time=0.6)

# Tăng dần (ease_in)
self.play(mob.animate.shift(DOWN), rate_func=rush_into, run_time=0.6)
```

### run_time – Căn thời gian với voiceover

```python
with self.voiceover(text="Đây là bước quan trọng...") as ov:
    # Chia thời gian: 30% + 50% + 20% = 100%
    self.play(Write(step1_text), run_time=ov.duration * 0.3)
    self.play(Create(highlight_shape), run_time=ov.duration * 0.5)
    self.wait(ov.duration * 0.2)
```

### self.wait() – Thêm khoảng nghỉ

```python
self.wait(0.3)   # Nghỉ ngắn giữa các ý
self.wait(1.0)   # Nghỉ bình thường sau một bước lớn
self.wait(2.0)   # Nghỉ dài sau kết quả quan trọng
```

---

## 5. Brace – Gộp và chú thích nhóm biểu thức

### Brace cơ bản

```python
# Brace bên dưới một nhóm
group = VGroup(eq1, eq2)
brace = Brace(group, direction=DOWN, color=WHITE)
label = brace.get_text("Phụ nhau")   # Text bên dưới brace
# hoặc
label = brace.get_tex(r"= 90^\circ")  # Formula bên dưới brace

self.play(Create(brace), Write(label))
```

### Brace bên phải (dùng cho chain suy luận)

```python
# Brace dọc bên phải → mũi tên suy ra
right_x = source_group.get_right()[0]
brace_spine = Line(
    [right_x + 0.1, source_group.get_top()[1] + 0.1, 0],
    [right_x + 0.1, source_group.get_bottom()[1] - 0.1, 0],
    stroke_opacity=0.0
)
brace = Brace(brace_spine, direction=RIGHT, color=WHITE)
result = MathTex(r"\Rightarrow \text{kết quả}").next_to(brace, RIGHT, buff=0.2)

self.play(Create(brace))
self.play(Write(result))
```

### Xóa brace sau khi dùng

```python
self.play(FadeOut(brace), FadeOut(label))
# Hoặc giữ kết quả, xóa brace
self.play(
    FadeOut(brace),
    result.animate.next_to(source_group, DOWN, buff=0.5)
)
```

---

## 6. Điều chỉnh vị trí và kích thước

### Scale text khi màn hình chật

```python
# Scale toàn bộ nhóm khi quá nhiều text
proof_group.scale(0.85)

# Hoặc animate scale + di chuyển xuống góc
self.play(
    proof_group.animate.scale(0.75).to_corner(DL, buff=0.3)
)
```

### Căn chỉnh lại vị trí

```python
# Di chuyển tương đối so với mob khác
new_eq.next_to(prev_eq, DOWN, buff=0.35, aligned_edge=LEFT)

# Di chuyển animation khi cần
self.play(mob.animate.next_to(reference, RIGHT, buff=0.5))

# Căn theo cột
col1 = VGroup(eq1, eq2, eq3).arrange(DOWN, aligned_edge=LEFT, buff=0.3)
col1.to_corner(UL, buff=0.5)
```

---

## 7. Các lỗi phổ biến và cách sửa

### Lỗi: Animation chạy quá nhanh

```python
# Trước (quá nhanh)
self.play(Write(long_text), run_time=0.5)

# Sau (vừa phải)
self.play(Write(long_text), run_time=1.5)
self.wait(0.5)
```

### Lỗi: Voiceover kết thúc trước animation

```python
# Nguyên nhân: tổng run_time > ov.duration
# Kiểm tra tổng các hệ số
with self.voiceover(text="...") as ov:
    self.play(A, run_time=ov.duration * 0.4)   # 40%
    self.play(B, run_time=ov.duration * 0.4)   # 40%
    self.wait(ov.duration * 0.2)               # 20% = tổng 100% ✓
```

### Lỗi: Màn hình chật vì quá nhiều text

```python
# Dọn các phương trình trung gian trước khi thêm mới
middle_eqs = VGroup(eq1, eq2, eq3)
self.play(
    FadeOut(middle_eqs),
    key_result.animate.next_to(title, DOWN, buff=0.3, aligned_edge=LEFT)
)
```

### Lỗi: `Indicate` không thấy rõ

```python
# Tăng scale_factor và run_time
self.play(Indicate(mob, color=YELLOW, scale_factor=1.4), run_time=1.2)

# Hoặc dùng Circumscribe thay thế
self.play(Circumscribe(mob, color=YELLOW, run_time=1.5))
```

### Lỗi: `RightAngle` hiện sai góc phần tư

```python
# Thử lần lượt 4 giá trị quadrant
# (1, 1)  → góc trên-phải
# (-1, 1) → góc trên-trái
# (1, -1) → góc dưới-phải
# (-1,-1) → góc dưới-trái
right_angle = RightAngle(line1, line2, length=0.3, quadrant=(-1, 1), color=WHITE)
```

---

## 8. Checklist tinh chỉnh

### Về nhịp điệu (Pacing)

- [ ] Mỗi ý quan trọng có `self.wait()` sau
- [ ] Kết quả đóng khung có ít nhất `self.wait(1.5)` để người xem đọc
- [ ] Dòng narration ngắn ≤ 5s → animation đơn giản, không quá nhiều bước
- [ ] Dòng narration dài ≥ 10s → chia thành 2–3 animation bước

### Về trực quan (Visual)

- [ ] Mỗi scene có ít nhất 1 `Indicate` hoặc `Flash` cho điểm nhấn
- [ ] Kết quả cuối được `Circumscribe` hoặc có `SurroundingRectangle` rõ ràng
- [ ] Không có quá 5 dòng text trên màn hình cùng lúc
- [ ] Hình vẽ không bị che bởi text chứng minh

### Về chuyển cảnh

- [ ] Mỗi scene kết thúc bằng `FadeOut` sạch (không để rác trên màn hình)
- [ ] Có `self.wait(0.5)` giữa FadeOut scene cũ và Write scene mới
- [ ] Kết quả trung gian (UR corner) không bị FadeOut khi chuyển scene

### Về code

- [ ] Không có Mobject bị `self.play(...)` sau khi đã `FadeOut`
- [ ] Mọi biến dùng ở scope sau đều được lưu vào `self.*`
- [ ] Không dùng `self.add()` thay `self.play(FadeIn(...))` cho Mobject quan trọng
