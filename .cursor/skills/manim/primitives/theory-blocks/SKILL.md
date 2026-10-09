---
name: manim-theory-blocks
description: Pattern code Manim cho 7 loại block bài giảng lý thuyết toán: dinh_nghia, dinh_li, he_qua, nhan_xet, chu_y, vi_du, bai_tap. Dùng khi code scene lý thuyết sau khi đã có spec-ly-thuyet.md. Kết hợp với manim-theory-layout (TheoryColumn, FigurePanel).
---

# Skill: Manim – Theory Blocks

> Mỗi block type = 1 pattern chuẩn: heading → body → formula → figure → Indicate.
> Dùng `TheoryColumn` từ `manim-theory-layout`. Không dùng `ProofLine`.
> Khi block có figure: xem thêm `theory-figure/{subject}` để dựng hình đúng.

---

## Quy tắc chung cho mọi block

```python
# Heading — đặt ngay dưới lesson_title nếu có, fallback to_corner(UL) nếu không
block_heading = Tex(r"\textbf{N. Tên mục}",
                    tex_template=viet_tex_template, font_size=32)
if hasattr(self, "lesson_title"):
    block_heading.next_to(self.lesson_title, DOWN, aligned_edge=LEFT, buff=0.35)
else:
    block_heading.to_corner(UL, buff=0.5)
self.play(Write(block_heading), run_time=0.6)

# TheoryColumn bắt đầu dưới heading
col = TheoryColumn(block_heading, has_figure=<True|False>)

# Cleanup cuối scene — luôn FadeOut block_heading + col.all + figure_group
self.play(FadeOut(block_heading), FadeOut(col.all), FadeOut(figure_group))
```

**Font size chuẩn:**
- Heading mục: 32 | Body text: 26 | Công thức inline: 28 | Công thức chính: 34 | Label hình: 24

**Gap chuẩn (xem bảng đầy đủ trong `manim-theory-layout`):**

| Loại content | gap default | Tối thiểu |
|---|---|---|
| body text | 0.20 | 0.18 |
| formula inline | 0.30 | 0.25 |
| formula display | 0.40 | 0.30 |
| sau heading | 0.35 | 0.35 |

**Bảng quyết định method TheoryColumn:**

| Tình huống | Dùng method |
|---|---|
| Câu văn, đoạn text | `col.place()` |
| Công thức display chiếm toàn cột | `col.place_formula()` |
| Công thức ngắn / inline | `col.place_formula_left()` |
| Bullet point | `col.place_bullet()` |

**Định dạng danh sách và đề mục đặc biệt:**

| Loại item | Ký hiệu prefix | Manim / Ghi chú |
|---|---|---|
| Bullet chính | `-` (dash) | `r"- Nội dung chính"` — KHÔNG dùng `$\bullet$` |
| Sub-item | `$\bullet$` (chấm tròn đặc) | `r"$\bullet$ Nội dung phụ"` hoặc `r"$\bullet$ $...$"` |
| Lưu ý / Chú ý | `(!) + nhãn SGK` | heading bold; body `\textit{}` + `color=COLOR_WARNING` |
| Nhận xét / Ghi nhớ | `(*) + nhãn SGK` | heading bold; body `\textit{}` + `color=COLOR_WARNING` |

> **Quy tắc match nhãn**: đọc nhãn thực tế từ ảnh SGK (`"Lưu ý"`, `"Chú ý"`, `"Nhận xét"`, `"Ghi nhớ"`) và ghép đúng prefix — **không** gộp nhãn với dấu `/`.

```python
# Sub-item text
label = Tex(r"- \textbf{Tính chất giao hoán:}", tex_template=viet_tex_template)

# Sub-item công thức — bullet tách biệt khỏi \cdot (xem Section 9 manim-theory.mdc)
formula = Tex(r"$\bullet$ $a \cdot b = b \cdot a$", tex_template=viet_tex_template)
```

---

## 1. `dinh_nghia` — Định nghĩa

**Đặc điểm**: text + thuật ngữ in đậm + hình minh họa.
> **Figure**: xem `theory-figure/geometry` để dựng hình và áp dụng GeometryEngine post-place pattern.

```python
def scene_dinhNghia(self):
    block_heading = Tex(r"\textbf{1. Định nghĩa}",
                        tex_template=viet_tex_template, font_size=32)
    block_heading.next_to(self.lesson_title, DOWN, aligned_edge=LEFT, buff=0.35)
    self.play(Write(block_heading), run_time=0.6)

    col = TheoryColumn(block_heading, has_figure=True)

    # Body lines — tạo sẵn, chưa add vào scene
    line1 = Tex(r"Tứ giác có bốn đỉnh nằm trên một đường tròn gọi là",
                tex_template=viet_tex_template, font_size=26)
    line2 = Tex(r"\textbf{tứ giác nội tiếp} đường tròn",
                tex_template=viet_tex_template, font_size=26)
    line3 = Tex(r"(hoặc đơn giản: \textbf{tứ giác nội tiếp}).",
                tex_template=viet_tex_template, font_size=26)
    col.place(line1); col.place(line2); col.place(line3)

    # [figure: xem theory-figure/geometry]
    # Dựng hình theo spec, gom vào figure_group → place_figure(figure_group)
    # Sau place_figure: register geo points bằng dot.get_center() (KHÔNG dùng tọa độ cũ)
    self.figure_group = figure_group  # lưu để scene sau tái dùng

    with self.voiceover("Định nghĩa. Tứ giác có bốn đỉnh nằm trên một đường tròn "
                        "được gọi là tứ giác nội tiếp đường tròn.") as ov:
        self.play(FadeIn(line1), run_time=ov.duration * 0.4)
        self.play(FadeIn(line2), FadeIn(line3), run_time=ov.duration * 0.6)

    # Indicate thuật ngữ in đậm
    terms = [line2[0][0:14], line3[0][9:24]]   # index slice của \textbf{}
    self.play(Indicate(VGroup(*terms), scale_factor=1.12, color=COLOR_ACTIVE),
              run_time=TIMING_INDICATE_SEGMENT)
    self.wait(0.5)

    self.play(FadeOut(block_heading), FadeOut(col.all), FadeOut(figure_group))
```

**Lưu ý:** Nếu cần tái dùng `figure_group` ở scene tiếp → **không** `FadeOut(figure_group)`, lưu `self.figure_group = figure_group`.

---

## 2. `dinh_li` — Định lí / Tính chất

**Đặc điểm**: phát biểu ngắn + công thức to căn giữa + Indicate trên hình.
> **Figure + GeometryEngine**: xem `theory-figure/geometry` cho post-place pattern và sync Indicate với voice.

```python
def scene_dinhLi(self):
    block_heading = Tex(r"\textbf{2. Định lí}",
                        tex_template=viet_tex_template, font_size=32)
    block_heading.next_to(self.lesson_title, DOWN, aligned_edge=LEFT, buff=0.35)
    self.play(Write(block_heading), run_time=0.6)

    col = TheoryColumn(block_heading, has_figure=True)

    # Phát biểu
    statement = Tex(
        r"Trong một tứ giác nội tiếp, tổng số đo hai góc đối nhau bằng $180^\circ$.",
        tex_template=viet_tex_template, font_size=26)
    col.place(statement, gap=0.30)

    # Công thức chính — căn giữa cột text, font lớn
    formula = MathTex(
        r"\widehat{A} + \widehat{C} = \widehat{B} + \widehat{D} = 180^\circ",
        tex_template=viet_tex_template, font_size=34)
    col.place_formula(formula)

    # Hình: tái dùng từ scene trước hoặc dựng mới
    figure_group = self.figure_group   # tái dùng

    with self.voiceover("Định lí. Trong một tứ giác nội tiếp, "
                        "tổng hai góc đối nhau bằng 180 độ.") as ov:
        self.play(FadeIn(statement), run_time=ov.duration * 0.4)
        self.play(Write(formula), run_time=ov.duration * 0.6)

    # [figure: xem theory-figure/geometry — Section 3 Sync Indicate với voice]
    # Tạo AngleMarker SAU place_figure, dùng geo.point("A").get_center()
    # Indicate cặp góc đối theo từng voiceover block:
    with self.voiceover("Ví dụ, góc A cộng góc C bằng 180 độ.") as ov:
        self.play(
            Indicate(sector_A, color=COLOR_EQUAL_1, scale_factor=1.2),
            Indicate(sector_C, color=COLOR_EQUAL_1, scale_factor=1.2),
            run_time=ov.duration)

    with self.voiceover("Tương tự, góc B cộng góc D cũng bằng 180 độ.") as ov:
        self.play(
            Indicate(sector_B, color=COLOR_EQUAL_2, scale_factor=1.2),
            Indicate(sector_D, color=COLOR_EQUAL_2, scale_factor=1.2),
            run_time=ov.duration)

    self.wait(0.5)
    self.play(FadeOut(block_heading), FadeOut(col.all))
    # figure_group giữ lại nếu scene sau cần → self.figure_group
```

---

## 3. `he_qua` — Hệ quả

**Đặc điểm**: giống `dinh_li` nhưng font nhỏ hơn, thường ngắn, không Indicate phức tạp.

```python
def scene_heQua(self):
    block_heading = Tex(r"\textbf{Hệ quả}",
                        tex_template=viet_tex_template, font_size=32)
    block_heading.next_to(self.lesson_title, DOWN, aligned_edge=LEFT, buff=0.35)
    self.play(Write(block_heading), run_time=0.5)

    col = TheoryColumn(block_heading, has_figure=False)   # thường không có hình riêng

    consequence = Tex(
        r"Hình chữ nhật và hình vuông là tứ giác nội tiếp.",
        tex_template=viet_tex_template, font_size=26)
    col.place(consequence)

    formula = MathTex(r"R = \dfrac{d}{2}", font_size=32)
    col.place_formula(formula)

    with self.voiceover("Hệ quả. Hình chữ nhật và hình vuông là tứ giác nội tiếp. "
                        "Bán kính đường tròn ngoại tiếp bằng một nửa đường chéo.") as ov:
        self.play(FadeIn(consequence), run_time=ov.duration * 0.5)
        self.play(Write(formula), run_time=ov.duration * 0.5)

    self.wait(0.5)
    self.play(FadeOut(block_heading), FadeOut(col.all))
```

---

## 4. `nhan_xet` — Nhận xét (có DualFigurePanel)

**Đặc điểm**: bullet points + 2 hình minh họa cạnh nhau.
> **DualFigurePanel scope**: CHỈ dùng `place_dual_figures` cho 2 hình ĐỘC LẬP (2 ví dụ riêng biệt). Nếu 2 hình liên quan → dùng `place_figure(VGroup(fig1, fig2).arrange(RIGHT, buff=0.3))`. Xem `theory-figure/geometry` Section 4.

```python
def scene_nhanXet(self):
    block_heading = Tex(r"\textbf{(*) Nhận xét}",  # prefix (*) + nhãn SGK
                        tex_template=viet_tex_template, font_size=32)
    block_heading.next_to(self.lesson_title, DOWN, aligned_edge=LEFT, buff=0.35)
    self.play(Write(block_heading), run_time=0.5)

    col = TheoryColumn(block_heading, has_figure=True)

    # Bullet points — dùng "- " (dash), italic + COLOR_WARNING
    bullets = [
        Tex(r"\textit{- Hình chữ nhật và hình vuông là tứ giác nội tiếp.}",
            tex_template=viet_tex_template, font_size=26, color=COLOR_WARNING),
        Tex(r"\textit{- Tâm đường tròn ngoại tiếp là giao điểm hai đường chéo.}",
            tex_template=viet_tex_template, font_size=26, color=COLOR_WARNING),
        Tex(r"\textit{- Bán kính bằng nửa độ dài đường chéo.}",
            tex_template=viet_tex_template, font_size=26, color=COLOR_WARNING),
    ]
    for b in bullets:
        col.place_bullet(b)

    # DualFigurePanel — 2 hình ĐỘC LẬP (xem theory-figure/geometry Section 4)
    # Dựng fig_left, fig_right riêng biệt theo spec
    dual_panel = place_dual_figures(
        fig_left, fig_right,
        label_left="Label trái", label_right="Label phải",
        tex_template=viet_tex_template)

    with self.voiceover("Nhận xét. [nội dung bullet 1]") as ov:
        self.play(FadeIn(bullets[0]), run_time=ov.duration * 0.3)
        self.play(Create(fig_left), Create(fig_right), run_time=ov.duration * 0.4)
        self.play(FadeIn(bullets[1]), run_time=ov.duration * 0.3)

    with self.voiceover("[nội dung bullet 2 và 3]") as ov:
        self.play(FadeIn(bullets[2]), run_time=ov.duration)

    self.wait(0.5)
    self.play(FadeOut(block_heading), FadeOut(col.all), FadeOut(dual_panel))
```

---

## 5. `chu_y` — Chú ý / Lưu ý

**Đặc điểm**: thường 1–3 dòng ngắn, có thể có box màu nhạt.

```python
def scene_chuY(self):
    block_heading = Tex(r"\textbf{(!) Chú ý}",  # prefix (!) + nhãn SGK; dùng "(!) Lưu ý" nếu SGK ghi "Lưu ý"
                        tex_template=viet_tex_template, font_size=32)
    block_heading.next_to(self.lesson_title, DOWN, aligned_edge=LEFT, buff=0.35)
    self.play(Write(block_heading), run_time=0.4)

    col = TheoryColumn(block_heading, has_figure=False)

    # Nội dung italic + COLOR_WARNING — KHÔNG dùng SurroundingRectangle
    note = Tex(r"\textit{Định lí trên còn có chiều đảo: Nếu tứ giác có tổng hai góc đối bằng "
               r"$180^\circ$ thì tứ giác đó nội tiếp được đường tròn.}",
               tex_template=viet_tex_template, font_size=26,
               color=COLOR_WARNING)
    col.place(note)

    with self.voiceover("Chú ý. Định lí còn có chiều đảo: nếu tứ giác có tổng "
                        "hai góc đối bằng 180 độ thì tứ giác đó nội tiếp được đường tròn.") as ov:
        self.play(FadeIn(note), run_time=ov.duration)

    self.wait(0.5)
    self.play(FadeOut(block_heading), FadeOut(col.all))
```

---

## 6. `vi_du` — Ví dụ

**Đặc điểm**: đề + lời giải ngắn (không phải proof đầy đủ).

```python
def scene_viDu(self):
    block_heading = Tex(r"\textbf{Ví dụ 1}",
                        tex_template=viet_tex_template, font_size=32)
    block_heading.next_to(self.lesson_title, DOWN, aligned_edge=LEFT, buff=0.35)
    self.play(Write(block_heading), run_time=0.5)

    col = TheoryColumn(block_heading, has_figure=True)

    # Đề bài
    problem = Tex(
        r"Cho tứ giác $ABCD$ nội tiếp đường tròn. "
        r"Biết $\widehat{A} = 110^\circ$. Tính $\widehat{C}$.",
        tex_template=viet_tex_template, font_size=26)
    col.place(problem, gap=0.35)

    # Phân cách (optional)
    col.skip(0.10)

    # Lời giải ngắn
    sol_heading = Tex(r"\textit{Giải:}", tex_template=viet_tex_template, font_size=26)
    col.place(sol_heading, gap=0.20)

    sol_line1 = Tex(r"Vì $ABCD$ nội tiếp nên $\widehat{A} + \widehat{C} = 180^\circ$.",
                    tex_template=viet_tex_template, font_size=26)
    col.place(sol_line1)

    sol_result = MathTex(r"\widehat{C} = 180^\circ - 110^\circ = 70^\circ",
                         tex_template=viet_tex_template, font_size=30)
    col.place_formula(sol_result)

    with self.voiceover("Ví dụ một. Cho tứ giác A B C D nội tiếp, biết góc A bằng 110 độ. "
                        "Tính góc C.") as ov:
        self.play(FadeIn(problem), run_time=ov.duration)

    with self.voiceover("Vì tứ giác nội tiếp nên góc A cộng góc C bằng 180 độ. "
                        "Suy ra góc C bằng 70 độ.") as ov:
        self.play(FadeIn(sol_heading), FadeIn(sol_line1), run_time=ov.duration * 0.6)
        self.play(Write(sol_result), run_time=ov.duration * 0.4)

    self.wait(0.5)
    self.play(FadeOut(block_heading), FadeOut(col.all))
```

---

## 7. `bai_tap` — Bài tập

**Đặc điểm**: chỉ đề, không giải (dùng cuối video).

```python
def scene_baiTap(self):
    block_heading = Tex(r"\textbf{Bài tập}",
                        tex_template=viet_tex_template, font_size=32)
    block_heading.next_to(self.lesson_title, DOWN, aligned_edge=LEFT, buff=0.35)
    self.play(Write(block_heading), run_time=0.5)

    col = TheoryColumn(block_heading, has_figure=False)

    exercises = [
        Tex(r"1. Tứ giác $ABCD$ nội tiếp, $\widehat{B} = 75^\circ$. Tính $\widehat{D}$.",
            tex_template=viet_tex_template, font_size=26),
        Tex(r"2. Hình thang $ABCD$ ($AB \parallel CD$) nội tiếp đường tròn."
            r" Chứng minh $ABCD$ là hình thang cân.",
            tex_template=viet_tex_template, font_size=26),
    ]
    for ex in exercises:
        col.place(ex, gap=0.30)

    with self.voiceover("Bài tập. Bài một: tứ giác A B C D nội tiếp, góc B bằng 75 độ, "
                        "tính góc D.") as ov:
        self.play(FadeIn(exercises[0]), run_time=ov.duration)

    with self.voiceover("Bài hai: hình thang A B C D nội tiếp đường tròn, "
                        "chứng minh đó là hình thang cân.") as ov:
        self.play(FadeIn(exercises[1]), run_time=ov.duration)

    self.wait(1.0)
    self.play(FadeOut(block_heading), FadeOut(col.all))
```

---

## Tóm tắt pattern chuẩn

| Block | Heading prefix | Content style | FigurePanel | Công thức | Indicate | FadeOut figure |
|-------|---------------|---------------|-------------|-----------|----------|----------------|
| `dinh_nghia` | Số. Tên | plain | Đơn (phải) | Không bắt buộc | terms_bold | Giữ nếu scene sau tái dùng |
| `dinh_li` | Số. Tên | plain | Tái dùng / Đơn | Bắt buộc, to | Cặp góc/đoạn trên hình | Giữ hoặc FadeOut |
| `he_qua` | `Hệ quả` | plain | Thường None | Có thể có | Không | N/A |
| `nhan_xet` | `(*) + nhãn SGK` | italic + `COLOR_WARNING` | Dual | Không | Không | FadeOut cuối scene |
| `chu_y` | `(!) + nhãn SGK` | italic + `COLOR_WARNING` | Thường None | Không | Không | N/A |
| `vi_du` | `Ví dụ N` | plain | Đơn (optional) | Kết quả cuối | Kết quả | FadeOut |
| `bai_tap` | `Bài tập` | plain | None | Không | Không | N/A |
