---
name: manim-hinh-3d
description: Dựng scene hình không gian 3D (hộp, cầu, nón, trụ) với ThreeDScene, ThreeDAxes và camera animation. KHÔNG dùng cho bài đại số.
---

# Skill: Manim – Hình Không Gian 3D

## Khi nào dùng skill này?

Dùng khi bài toán liên quan đến **hình không gian 3D**: Khối hộp, hình cầu, hình nón, hình trụ, mặt phẳng, đường thẳng trong không gian.

**Không dùng** cho bài đại số (phương trình, bất phương trình) — xem `algebra/step-solver`.

---

## B1. Cấu trúc class 3D

```python
from manim import *

class HinhKhongGian(ThreeDScene):
    def construct(self):
        # Đặt góc camera ban đầu
        self.set_camera_orientation(phi=75 * DEGREES, theta=-45 * DEGREES)
        self.begin_ambient_camera_rotation(rate=0.1)  # Xoay tự động (tùy chọn)

        self.scene01_dungHinh()
        self.scene02_chungMinh()
```

**Lưu ý**: `ThreeDScene` **không tương thích** với `VoiceoverScene`. Khi cần voiceover cho 3D, render phần 3D riêng rồi ghép video.

---

## B2. Trục tọa độ 3D

```python
axes = ThreeDAxes(
    x_range=[-4, 4, 1],
    y_range=[-4, 4, 1],
    z_range=[-3, 3, 1],
    x_length=8,
    y_length=8,
    z_length=6,
)
x_label = axes.get_x_axis_label("x")
y_label = axes.get_y_axis_label("y")
z_label = axes.get_z_axis_label("z")

self.play(Create(axes), Write(x_label), Write(y_label), Write(z_label))
```

---

## B3. Khối hình 3D cơ bản

```python
# Hình cầu
sphere = Sphere(radius=1.5, resolution=(30, 30))
sphere.set_color(BLUE)
sphere.set_opacity(0.7)

# Hình trụ
cylinder = Cylinder(radius=1, height=3, direction=UP)
cylinder.set_color(GREEN)
cylinder.set_opacity(0.6)

# Hình nón
cone = Cone(base_radius=1.5, height=3, direction=UP)
cone.set_color(ORANGE)

# Hộp chữ nhật (Prism)
prism = Prism(dimensions=[2, 3, 4])  # [width, height, depth]
prism.set_color(YELLOW)
prism.set_opacity(0.5)
```

---

## B4. Mặt phẳng và đường thẳng trong không gian

```python
# Mặt phẳng (dùng Square/Rectangle rồi xoay)
plane = Square(side_length=4, color=BLUE, fill_opacity=0.3)
plane.rotate(PI/2, axis=RIGHT)  # Đặt nằm ngang

# Đường thẳng trong không gian
line_3d = Line3D(start=[-3, 0, 0], end=[3, 0, 0], color=WHITE)

# Điểm trong 3D
dot_3d = Dot3D(point=[1, 2, 1], color=RED, radius=0.1)
```

---

## B5. Điều chỉnh camera

```python
# Góc cố định
self.set_camera_orientation(phi=60 * DEGREES, theta=-30 * DEGREES)

# Di chuyển camera (animation)
self.move_camera(phi=45 * DEGREES, theta=30 * DEGREES, run_time=2)

# Xoay tự động
self.begin_ambient_camera_rotation(rate=0.05)   # Bắt đầu xoay
self.stop_ambient_camera_rotation()              # Dừng xoay
```

---

## B6. Nhãn trong 3D (luôn nhìn về phía camera)

```python
# Text trong 3D dùng always_redraw hoặc add_fixed_in_frame_mobjects
label = Text("A", font_size=24)
self.add_fixed_in_frame_mobjects(label)   # Label không bị ảnh hưởng bởi camera rotation
label.to_corner(UL)

# Thông thường: đặt nhãn 2D ở góc màn hình, giải thích qua voiceover
```

---

## B7. Pattern Scene 3D hoàn chỉnh

```python
def scene01_dungKhoi(self):
    # 1. Setup camera
    self.set_camera_orientation(phi=70 * DEGREES, theta=-45 * DEGREES)

    # 2. Trục tọa độ
    axes = ThreeDAxes(x_range=[-3,3], y_range=[-3,3], z_range=[-3,3])
    self.play(Create(axes))

    # 3. Dựng khối
    cube = Cube(side_length=2, fill_color=BLUE, fill_opacity=0.5, stroke_color=WHITE)
    self.play(Create(cube), run_time=2)

    # 4. Xoay để nhìn rõ
    self.begin_ambient_camera_rotation(rate=0.1)
    self.wait(3)
    self.stop_ambient_camera_rotation()

    # 5. Di chuyển camera đến góc nhìn cụ thể
    self.move_camera(phi=45 * DEGREES, theta=0 * DEGREES, run_time=2)
```

---

## Checklist trước khi render

- [ ] `ThreeDScene` (không `VoiceoverScene`) cho cảnh 3D
- [ ] `set_camera_orientation` ngay đầu `construct()`
- [ ] `Sphere`, `Cylinder`, `Cone` có `set_opacity()` để nhìn xuyên khối
- [ ] Nhãn 2D dùng `add_fixed_in_frame_mobjects` để không bị xoay theo camera
