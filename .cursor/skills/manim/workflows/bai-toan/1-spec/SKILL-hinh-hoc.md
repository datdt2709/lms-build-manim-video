---
name: manim-step-1-scene-spec-hinh-hoc
description: Tạo Scene Spec Markdown từ ảnh đề/lời giải bài toán hình học phẳng. Dùng khi lập kế hoạch video hình học, chia scene và viết narration TTS tiếng Việt trước khi code Manim.
---

# Skill: Manim Step 1 – Tạo Scene Specification

## Mục đích

Nhận **ảnh đề bài + lời giải** (hoặc mô tả bài toán) → Tạo ra **Scene Spec** dạng Markdown mô tả chi tiết từng scene của video Manim. Spec này là "bản vẽ" chung để cả Cursor và Gemini đều có thể dùng để sinh code ở bước 2.

---

## Khi nào dùng skill này?

- Người dùng cung cấp ảnh đề bài / ảnh lời giải viết tay hoặc đánh máy
- Người dùng mô tả bài toán bằng lời
- Người dùng muốn lập kế hoạch video trước khi viết code
- Người dùng muốn chuẩn hóa một draft từ Gemini thành spec đầy đủ

---

## Quy trình thực hiện

### Bước 1 – Đọc và phân tích đầu vào

Khi nhận ảnh hoặc văn bản:

1. **Xác định bài toán**:
   - Loại toán: Hình phẳng
   - Giả thiết (GT): Liệt kê đầy đủ các điều kiện cho
   - Kết luận (KL): Những gì cần chứng minh / tìm

2. **Đọc lời giải** (nếu có):
   - Chia lời giải thành các **bước lập luận riêng biệt**
   - Mỗi bước = 1 ý tưởng logic = có thể thành 1 scene
   - Chú ý các điểm "pivotal": nơi chiến thuật thay đổi, nơi kết quả trung gian xuất hiện

3. **Xác định dạng toán** để chọn skill phù hợp ở Step 2:
   - Hình phẳng → dùng `manim-hinh-phang`

### Bước 2 – Chia scene

Nguyên tắc chia scene (tổng quát cho bài có K ý bất kỳ):

| Scene        | Nội dung                                      | Thời lượng ước tính |
|--------------|-----------------------------------------------|---------------------|
| Scene 01     | Intro + Đề bài (GT/KL) + Dựng hình CƠ BẢN    | 60–90s              |
| Scene 02     | Dựng thêm hình ý a (nếu cần) + Phân tích ý a | 30–60s              |
| Scene 03..M  | Các bước chứng minh / tính toán ý a           | 45–90s/scene        |
| Scene M+1    | Dựng thêm hình ý b (nếu cần) + Phân tích ý b | 30–60s              |
| Scene M+2..P | Các bước chứng minh / tính toán ý b           | 45–90s/scene        |
| ...          | *(lặp tương tự cho ý c, d, ...)*              | ...                 |
| Scene N      | Tổng kết toàn bài                             | 30–45s              |

**Nguyên tắc dựng hình theo tiến trình**:
- **Scene 01** chỉ dựng các yếu tố xuất hiện trong GT, không dựng bất kỳ yếu tố nào chỉ xuất hiện trong quá trình chứng minh.
- **Mỗi ý** (a, b, c, ...) mở đầu bằng 1 scene riêng: dựng thêm hình cần thiết cho ý đó + phân tích hướng giải. Không lộ hướng giải của ý sau.
- Nếu ý không cần dựng thêm hình, scene đầu của ý chỉ cần phần phân tích.
- **Phân biệt hai loại "nét phụ trợ"**:
  - **Loại A – Nét hình học mới** (cạnh tam giác mới, đường cao, đường nối hai điểm đã có, ví dụ `seg_AD`, `seg_DH`): dựng trong scene đầu của ý cần nó bằng `Create()` vĩnh viễn, đặt tên `seg_*`, lưu `self.seg_*`. Spec ghi là `Create(seg_AD)` **không có** `FadeOut`. Sau khi `Create`, phải liệt kê ngay `bring_to_front` cho tất cả dot và label bị che: `bring_to_front(dot_X, label_X, dot_Y, label_Y, ...)`.
  - **Loại B – Highlight tạm** (Polygon fill màu, `Angle` arc màu, đổi màu tạm để nhấn mạnh): `FadeIn` → animate → `FadeOut` trong cùng voiceover block. Spec ghi rõ cặp `FadeIn`/`FadeOut`. Đặt tên `*_fill` hoặc `*_temp` để phân biệt.

**Gộp bước khi cùng ý – bắt buộc**:

Khi lời giải chia một ý thành nhiều bước lập luận (Bước 1, Bước 2, ...) nhưng tất cả hướng đến **cùng 1 kết luận**, toàn bộ các bước phải nằm trong **1 scene method duy nhất** — không tạo scene riêng cho từng bước.

| Tình huống                                              | Quyết định                                      |
|---------------------------------------------------------|-------------------------------------------------|
| Bước 1 và 2 cùng phục vụ **1 kết luận của cùng 1 ý**   | → 1 scene, `proof_accumulator` (không FadeOut)  |
| Bước 2 dùng ngay kết quả Bước 1 (không KQ trung gian)   | → 1 scene, `proof_accumulator`                  |
| Bước 1 và 2 ra **hai KQ trung gian độc lập** (2 box)    | → 2 scene riêng biệt                            |

Tổng số dòng trong `proof_accumulator` **≤ 12 dòng** (font 26). Nếu vượt, mới tách thành 2 scene. Xem chi tiết code mẫu trong `SKILL-hinh-phang.md` mục 14.

**Tiêu chí chia scene tốt**:
- Mỗi scene có **1 mục tiêu rõ ràng** (CM IE=IC, CM IF=IC, ...)
- Scene không quá 90 giây narration
- Kết thúc scene = hoàn thành 1 kết quả trung gian (đóng khung)

### Bước 3 – Viết narration tiếng Việt

Quy tắc viết narration phù hợp TTS (Google Text-to-Speech):

- **Không dùng ký hiệu toán học** trong narration: Viết "góc I E C" thay vì "∠IEC", "đoạn A B" thay vì "AB"
- **Giải thích bằng lời tự nhiên**: "Chúng ta cần chứng minh..." thay vì "CM:"
- **Thêm chuyển tiếp**: "Tiếp theo...", "Bây giờ hãy xét...", "Điều này có nghĩa là..."
- **Không dùng emoji** trong narration (TTS đọc tên emoji)
- **Giữ câu ngắn**: Mỗi câu ≤ 20 từ để TTS phát âm tự nhiên
- **Đánh vần ký hiệu**: "tam giác O A C" (có dấu cách giữa các chữ cái)

### Bước 4 – Output Scene Spec

Tạo file `scene-spec.md` trong thư mục làm việc. **Tất cả scene đều dùng format segment** — không có format narration/animation sequence tách biệt. Scene 01 dùng chủ yếu `at: start`; scene từ 02 trở đi dùng bookmark đầy đủ.

---

## Template Scene Spec chuẩn (format segment)

```markdown
# Scene Spec: [Tên bài toán]

## Thông tin chung

- **Loại toán**: Hình phẳng / Đại số / Hình không gian
- **Skill cần dùng**: manim-hinh-phang / manim-dai-so-hinh-khong-gian
- **Tổng số scene**: N
- **Thời lượng ước tính**: X phút

---

## Giả thiết & Kết luận

**GT:**
- Nửa đường tròn (O), đường kính AB
- C ∈ (O), D ∈ AB
- EF ⊥ AB tại D (E ∈ AC, F ∈ BC)
- Tiếp tuyến tại C cắt EF tại I

**KL:**
- a) I là trung điểm EF
- b) OC là tiếp tuyến của đường tròn ngoại tiếp △ECF

---

## Scene 01 – Intro & Đề bài

### metadata
- title: "Intro và Đề bài"
- duration: "60–90s"
- cleanup_start: []
- cleanup_end: []
- persist: [gt_vgroup, kl_vgroup, diagram, dot_C, dot_D, dot_E, dot_F, diameter, segment_AC, segment_BC, line_EF_obj, right_angle_D]

### geometry
| Điểm |  x |  y | Ghi chú              |
|------|----|----|----------------------|
| O    |  0 |  0 | Tâm nửa đường tròn   |
| A    | -3 |  0 |                      |
| B    |  3 |  0 |                      |
| C    | 1.8| 2.4| Trên nửa đường tròn  |
| D    | 1.8|  0 | Hình chiếu C lên AB  |

### objects

*(Scene 01 không dựng thêm Loại A ngoài GT — bỏ qua section này)*

### segments

#### segment_1
- voice: >
    "Chào các em! Hôm nay thầy trò chúng ta sẽ cùng nhau xử lý một bài hình học rất thú vị
    về nửa đường tròn và tiếp tuyến."
- actions:
    - at: start → Write(title1), [after 1s] FadeOut(title1), Write(title2), [after 1s] FadeOut(title2)
- write: ~

#### segment_2
- voice: >
    "Cho nửa đường tròn tâm O, đường kính A B. <bookmark mark='bk_C'/> Lấy điểm C trên nửa đường tròn
    và điểm D trên đoạn A B. <bookmark mark='bk_EF'/> Đường thẳng E F vuông góc với A B tại D,
    với E thuộc A C và F thuộc B C. <bookmark mark='bk_gt_done'/> Tiếp tuyến tại C cắt E F tại I."
- actions:
    - at: start      → Write(gt_vgroup[0:2]), Create(semicircle), Create(diameter), Create(dot_A), Write(label_A), Create(dot_B), Write(label_B), Create(dot_O), Write(label_O)
    - at: bk_C       → Create(dot_C), Write(label_C), Create(dot_D), Write(label_D), Create(segment_AC), Create(segment_BC)
    - at: bk_EF      → Write(gt_vgroup[2:4]), Create(line_EF_obj), Create(dot_E), Write(label_E), Create(dot_F), Write(label_F), Create(right_angle_D)
    - at: bk_gt_done → Write(gt_vgroup[4])
- write: ~

#### segment_3
- voice: >
    "Bài toán yêu cầu: <bookmark mark='bk_kla'/> Câu a, chứng minh I là trung điểm của E F.
    <bookmark mark='bk_klb'/> Câu b, chứng minh O C là tiếp tuyến của đường tròn ngoại tiếp
    tam giác E C F."
- actions:
    - at: start   → Write(kl_vgroup[0])
    - at: bk_kla  → Write(kl_vgroup[1]), Indicate(kl_vgroup[1])
    - at: bk_klb  → Write(kl_vgroup[2]), Indicate(kl_vgroup[2])
- write: ~

### layout
- scale: 0.85
- shift: RIGHT * 3.5 + DOWN * 0.5

---

## Scene 02 – Dựng thêm hình + Phân tích ý a

### metadata
- title: "Ý a: CM I là trung điểm EF"
- duration: "40–60s"
- cleanup_start: [gt_vgroup, kl_vgroup]
- cleanup_end: [title_a, muc_tieu_group]
- persist: [segment_CI, dot_I, label_I]

### geometry
*(Copy từ Scene 01, bổ sung điểm I)*
| Điểm |  x |  y | Ghi chú                         |
|------|----|----|---------------------------------|
| I    | 1.8| 3.6| Giao tiếp tuyến tại C với EF    |

### objects  *(Loại A — Create vĩnh viễn, không FadeOut)*
| id         | definition                                      | add_to_persistent |
|------------|-------------------------------------------------|-------------------|
| segment_CI | Line(C_pos, I_pos, color="#1565C0")             | yes               |
| dot_I      | Dot(I_pos, color="#E65100", radius=0.07)        | yes               |
| label_I    | MathTex("I").next_to(I_pos, RIGHT, buff=0.12)   | yes               |

### segments

#### segment_1
- voice: >
    "Để giải câu a, ta cần dựng thêm tiếp tuyến tại C cắt đường thẳng E F tại điểm I.
    <bookmark mark='bk_I'/> Điểm I xuất hiện trên hình như sau."
- actions:
    - at: start → Write(title_a)
    - at: bk_I  → Create(segment_CI), Create(dot_I), Write(label_I), bring_to_front(dot_C, label_C, dot_E, label_E, dot_F, label_F)
- write: ~

#### segment_2
- voice: >
    "Câu a yêu cầu chứng minh <bookmark mark='bk_muc_tieu'/> I là trung điểm của đoạn E F,
    tức là I E bằng I F."
- actions:
    - at: start       → Write(muc_tieu_group[0])
    - at: bk_muc_tieu → Write(muc_tieu_group[1]), Indicate(muc_tieu_group[1]), Indicate(dot_I)
- write: ~

#### segment_3
- voice: >
    "Hướng tiếp cận: <bookmark mark='bk_hint'/> ta sẽ chứng minh tam giác I E C bằng
    tam giác I F C. Hãy chú ý đến hai tam giác vuông này."
- actions:
    - at: bk_hint → Indicate(dot_I), Indicate(dot_E), Indicate(dot_F), Indicate(dot_C)
- write: ~

### layout
- scale: 0.85
- shift: RIGHT * 3.5 + DOWN * 0.5

---

## Scene 03..M – [Các bước chứng minh / tính toán]

*(Lặp cấu trúc tương tự Scene 02 cho mỗi bước lập luận chính)*

### metadata
- title: "[Tên bước]"
- duration: "45–90s"
- cleanup_start: [title_prev]
- cleanup_end: [proof, title_scene]
- persist: [result_[tên]]

### geometry
*(Copy tọa độ cần dùng)*

### objects
*(Loại A nếu cần dựng thêm; bỏ qua section nếu không)*

### segments

#### segment_1
- voice: >
    "[Dẫn dắt, không dùng ký hiệu toán học. <bookmark mark='bk_goal'/> Mục tiêu bước này...]"
- actions:
    - at: start   → Write(title_scene), Write(muc_tieu)
    - at: bk_goal → Indicate(muc_tieu, color=YELLOW)
- write: ~

#### segment_K  *(kết luận)*
- voice: >
    "Vậy <bookmark mark='bk_result'/> [phát biểu kết quả]. Điều phải chứng minh."
- actions:
    - at: bk_result → Flash(dot_relevant), Write(result_tex)
- write:
    - text: "\Rightarrow \text{[Kết quả]} \quad \text{(đpcm)}"
    - at: bk_result
    - post: Circumscribe(result_tex, fade_out=True)

### layout
- scale: 0.85
- shift: RIGHT * 3.5 + DOWN * 0.5

---

## Scene N – Tổng kết

### metadata
- title: "Tổng kết"
- duration: "30–45s"
- cleanup_start: [title_prev, proof_prev]
- cleanup_end: []
- persist: []

### geometry
*(Giữ nguyên hình từ scene trước)*

### objects
*(Không dựng thêm Loại A)*

### segments

#### segment_1
- voice: >
    "Hôm nay chúng ta đã chứng minh được hai kết quả quan trọng.
    <bookmark mark='bk_kq1'/> Thứ nhất, I là trung điểm của E F.
    <bookmark mark='bk_kq2'/> Thứ hai, O C là tiếp tuyến của đường tròn ngoại tiếp tam giác E C F."
- actions:
    - at: start  → Write(title_tong_ket)
    - at: bk_kq1 → self.result_a.animate.next_to(title_tong_ket, DOWN, buff=0.3, aligned_edge=LEFT)
    - at: bk_kq2 → self.result_b.animate.next_to(self.result_a, DOWN, buff=0.3, aligned_edge=LEFT)
- write: ~

#### segment_2
- voice: >
    "Đây là hai tính chất đẹp của nửa đường tròn và tiếp tuyến.
    <bookmark mark='bk_final'/> Hẹn gặp lại các em ở bài học tiếp theo!"
- actions:
    - at: bk_final → Create(box_final), Flash(box_final)
- write: ~

### layout
- scale: 0.85
- shift: RIGHT * 3.5 + DOWN * 0.5
```

---

## Quy tắc viết segments – Bookmark-Driven

Mỗi `segment_N` gom `voice + actions + write` vào một đơn vị nguyên tử, ánh xạ 1-1 ra một `with self.voiceover(...)` block trong Python.

### Cấu trúc tổng thể một Scene (format mới)

```markdown
## Scene 02 – [Tiêu đề scene]

### metadata
- title: "[Tiêu đề hiển thị trong scene]"
- duration: "45–65s"
- cleanup_start: [tên_vgroup_1, tên_vgroup_2]   # FadeOut ở đầu scene
- cleanup_end: [proof, title_a]                  # FadeOut ở cuối scene
- persist: [tên_mob_1, tên_mob_2]               # Giữ lại sang scene sau (tự lưu self.*)

### geometry
Bảng tọa độ tham chiếu (copy từ Scene 01 nếu không đổi, hoặc bổ sung điểm mới):
| Điểm |  x |  y | Ghi chú              |
|------|----|----|----------------------|
| O    |  0 |  0 | Tâm đường tròn       |
| A    | -3 |  0 |                      |

### objects  *(Loại A — Create vĩnh viễn, không FadeOut)*
| id        | definition                                     | add_to_persistent |
|-----------|------------------------------------------------|-------------------|
| circle_AI | Circle(radius=R_circle, color="#1565C0")       | yes               |
| dot_O     | Dot(O_pos, color="#E65100", radius=0.07)       | yes               |
| label_O   | MathTex("O").next_to(O_pos, RIGHT, buff=0.12)  | yes               |

*(Bỏ qua nếu scene không dựng thêm yếu tố Loại A)*

### segments

#### segment_1
- voice: >
    "[Lời thoại với <bookmark mark='tên_bk'/> được đặt đúng vị trí trong câu.
    Bookmark đặt ngay trước từ/cụm từ tương ứng với animation sẽ kích hoạt.]"
- actions:
    - at: start        → [Animation chạy ngay khi voiceover bắt đầu]
    - at: tên_bk       → [Animation kích hoạt khi TTS đọc đến bookmark]
    - at: end          → [Animation chạy sau khi voiceover kết thúc (hiếm dùng)]
- write: ~   *(không ghi proof line ở segment này)*

#### segment_2
- voice: >
    "Vì B K là đường cao của tam giác A B C nên B K vuông góc với A C.
    <bookmark mark='bk_ang'/> Mà I thuộc đoạn B K nên góc A K I bằng 90 độ."
- actions:
    - at: start   → Indicate(seg_BK), Indicate(right_angle_K)
    - at: bk_ang  → Create(ang_AKI_temp), [after 0.5s] FadeOut(ang_AKI_temp)
- write:
    - text: "BK \perp AC \Rightarrow \angle AKI = 90°"
    - at: bk_ang   *(Write proof line đồng bộ với bookmark)*

#### segment_3  *(kết luận — Pattern B)*
- voice: >
    "Vậy <bookmark mark='bk_result'/> đường tròn đường kính A I đi qua K.
    Điều phải chứng minh."
- actions:
    - at: bk_result → Flash(dot_K), Indicate(circle_AI)
- write:
    - text: "\Rightarrow \text{Đường tròn đường kính } AI \text{ đi qua } K \quad \text{(đpcm)}"
    - at: bk_result
    - post: Circumscribe(result_tex, fade_out=True)   *(chạy sau khi Write xong)*

### layout
- scale: 0.85
- shift: RIGHT * 3.5 + DOWN * 0.5
```

### Quy tắc viết segments với bookmark

**Quy tắc 1 – Mỗi segment = 1 voiceover block**

Mỗi `segment_N` trong spec ánh xạ trực tiếp sang đúng 1 `with self.voiceover(...) as ov:` block. Không tách, không gộp tùy tiện.

**Quy tắc 2 – Bookmark phải nằm trong `voice`, action phải dùng đúng tên đó**

```
voice:  "... <bookmark mark='bk_circle'/> Gọi O là trung điểm ..."
actions:
    - at: bk_circle → Indicate(circle_AI)   ✓ tên khớp
    - at: bk_circel → Indicate(circle_AI)   ✗ sai tên → animation không chạy
```

Không được có action `at: tên_bk` mà trong `voice` không có `<bookmark mark='tên_bk'/>`.

**Quy tắc 3 – `at: start` cho animation không cần căn với lời**

Những animation chạy trong khi TTS vẫn đang nói (không cần sync chính xác) dùng `at: start`:
```
- at: start → Create(circle_AI), Create(dot_O), Write(label_O)
```
Trong code sẽ sinh ra `self.play(...)` ngay đầu block, trước `self.wait_until_bookmark(...)`.

**Quy tắc 4 – Loại B (highlight tạm) luôn có cặp FadeIn/FadeOut trong cùng segment**

```
- at: bk_ang → Create(ang_AKI_temp), [after 0.5s] FadeOut(ang_AKI_temp)
```

Nếu FadeOut phải xảy ra ở segment khác, ghi rõ `FadeOut(ang_AKI_temp)` trong `actions` của segment đó với `at: start`.

**Quy tắc 5 – `write` đồng bộ với bookmark**

Mỗi dòng `write` trong proof block phải chỉ định `at:` để biết khi nào `Write(proof_line)` được gọi:
```
- write:
    - text: "..."
    - at: bk_ang     # Write proof line khi TTS đọc đến bk_ang
```

Nếu `write: ~` thì segment không ghi thêm dòng proof nào.

**Quy tắc 6 – Số bookmark trong 1 segment (KHÔNG GIỚI HẠN)**

Một segment có thể chứa **nhiều bookmark (8–10 hoặc hơn)** khi voiceover liệt kê nhiều thực thể hình học liên tiếp (ví dụ phát biểu △OFB = △OFC (c.g.c) ⇒ BF = FC; ∠OFB = ∠OFC).

Mỗi **thực thể hình học** (đoạn, góc, tam giác, tứ giác, điểm, đường tròn, cung, bán kính, đường kính, dây cung, tiếp tuyến, cát tuyến) và mỗi **từ kết nối semantic** (`=`, `⇒`, `(c.g.c)`, `(g.c.g)`, `(c.c.c)`) **PHẢI có 1 bookmark riêng**. Không gộp 2 thực thể vào 1 bookmark, không gộp luận điểm "hình + lời" vào 1 bookmark.

> Quy tắc cũ "≤ 3 bookmark / segment" đã **HUỶ**.

**Quy tắc 7 – Đặt tên bookmark theo pattern `<type>_<name>_expr`**

Tên bookmark phải tự mô tả thực thể để dễ trace giữa spec, ProofLine, và sync_*.

| Loại                      | Pattern                  | Ví dụ                              |
|---------------------------|--------------------------|------------------------------------|
| Tam giác                  | `tri_<XYZ>_expr`         | `tri_OFB_expr`, `tri_ABC_expr`     |
| Tam giác — tiêu chí       | `tri_<criterion>_expr`   | `tri_cgc_expr`, `tri_ggg_expr`     |
| Tam giác — "bằng"         | `tri_equal_expr`         | (cố định)                          |
| Đoạn                      | `seg_<XY>_expr`          | `seg_BF_expr`, `seg_FC_expr`       |
| Đoạn — "bằng"             | `seg_equal_expr`         | (cố định)                          |
| Góc                       | `angle_<XYZ>_expr`       | `angle_OFB_expr`                   |
| Góc — "bằng"              | `angle_equal_expr`       | (cố định)                          |
| Tứ giác                   | `quad_<WXYZ>_expr`       | `quad_ABCD_expr`                   |
| Điểm                      | `dot_<X>_expr`           | `dot_M_expr`, `dot_I_expr`         |
| Đường tròn                | `circ_<NAME>_expr`       | `circ_O_expr`                      |
| Cung                      | `arc_<XY>_expr`          | `arc_BC_expr`                      |
| Bán kính                  | `radius_<XY>_expr`       | `radius_OA_expr`                   |
| Đường kính                | `diameter_<XY>_expr`     | `diameter_AB_expr`                 |
| Dây cung                  | `chord_<XY>_expr`        | `chord_CD_expr`                    |
| Tiếp tuyến                | `tangent_<XY>_expr`      | `tangent_AB_expr`                  |
| Cát tuyến                 | `secant_<XY>_expr`       | `secant_AB_expr`                   |
| Suy ra (`⇒`)             | `<context>_implies_expr` | `tri_implies_seg_expr`             |

> Pattern cũ `bk_<short>` (ví dụ `bk_circle`, `bk_ang`) **đã bỏ** — không dùng nữa.

**Quy tắc 8 – Mỗi segment chứng minh có nhiều thực thể: dùng `proof_tokens` + action `sync_*`**

Khi 1 segment chứng minh (`voice` chứa nhiều bookmark thực thể hình học), thay vì `write: text: "..."` một dòng cứng, spec phải khai báo:

1. `proof_tokens` — danh sách `(id, latex)` cho mỗi thực thể / từ kết nối, theo đúng thứ tự xuất hiện trong dòng MathTex.
2. `actions` — mỗi bookmark trỏ đến 1 lời gọi `sync_<type>(token=..., shape=..., color=...)` hoặc `sync_relation(token=...)` cho từ kết nối.

Xem template ở mục "Template segment chứng minh nhiều thực thể" bên dưới.

---

## Template segment chứng minh nhiều thực thể (`proof_tokens` + `sync_*`)

Khi voiceover của 1 segment chứng minh nhiều bước phát biểu trong cùng dòng (ví dụ "△OFB = △OFC (c.g.c) ⇒ BF = FC; ∠OFB = ∠OFC"), spec phải dùng pattern `proof_tokens` + action `sync_*`. Pattern này thay thế `write: text: "..."` đơn lẻ cho dòng có nhiều thực thể.

```markdown
#### segment_K
- voice: >
    "Do đó <bookmark mark='tri_OFB_expr'/> tam giác O F B
     <bookmark mark='tri_equal_expr'/> bằng
     <bookmark mark='tri_OFC_expr'/> tam giác O F C
     <bookmark mark='tri_cgc_expr'/> theo trường hợp cạnh góc cạnh.
     <bookmark mark='seg_BF_expr'/> Suy ra B F
     <bookmark mark='seg_equal_expr'/> bằng
     <bookmark mark='seg_FC_expr'/> F C."
- proof_tokens:
    - id: tri_OFB     latex: \triangle OFB
    - id: eq1         latex: =
    - id: tri_OFC     latex: \triangle OFC
    - id: cgc         latex: \;(\text{c.g.c})
    - id: seg_BF      latex: ;\quad BF
    - id: seg_eq      latex: =
    - id: seg_FC      latex: FC
- actions:
    - at: tri_OFB_expr   → sync_triangle(token=tri_OFB, shape=tri_OFB_fill, color=COLOR_EQUAL_1)
    - at: tri_equal_expr → sync_relation(token=eq1)
    - at: tri_OFC_expr   → sync_triangle(token=tri_OFC, shape=tri_OFC_fill, color=COLOR_EQUAL_2)
    - at: tri_cgc_expr   → sync_relation(token=cgc)
    - at: seg_BF_expr    → sync_segment(token=seg_BF, shape=seg_BF, color=COLOR_EQUAL_1)
    - at: seg_equal_expr → sync_relation(token=seg_eq)
    - at: seg_FC_expr    → sync_segment(token=seg_FC, shape=seg_FC, color=COLOR_EQUAL_1)
```

### Quy tắc của `proof_tokens` + `actions`

- **Mỗi token `proof_tokens` ↔ một sub-expression trong ProofLine.** Token `id` phải khớp với token id trong `pf_<NN> = ProofLine(...)` ở Step 2.
- **Mỗi `<type>_<name>_expr` bookmark trong `voice` PHẢI có đúng 1 action `at: <bookmark>` tương ứng** — không thiếu, không thừa.
- **Action format**: `sync_<type>(token=<token_id>, shape=<shape_var>, color=<COLOR_*>)`.
  - `sync_relation(token=<token_id>)` cho từ kết nối (`=`, `⇒`, `(c.g.c)`).
  - `sync_segment(token=..., shape=seg_XY, color=COLOR_EQUAL_*)` cho đoạn.
  - `sync_angle(token=..., shape=sec_XYZ, color=COLOR_EQUAL_*)` cho góc.
  - `sync_triangle(token=..., shape=tri_XYZ_fill, color=COLOR_EQUAL_*)` cho tam giác.
  - `sync_quadrilateral(token=..., shape=quad_WXYZ_fill, color=COLOR_EQUAL_*)` cho tứ giác.
  - `sync_point(token=..., shape=dot_X, color=COLOR_*)` cho điểm.
- Trường `write:` cũ vẫn hợp lệ cho segment ĐƠN GIẢN có 1 bookmark + 1 dòng MathTex; trường `proof_tokens` + actions `sync_*` là **bắt buộc** cho dòng chứng minh có nhiều thực thể.
- **Quy tắc màu** (rule 5 từ `manim-geometry-engine`):
  - Nhiều đoạn / nhiều góc **bằng nhau**: cùng `COLOR_EQUAL_1` cho mọi đối tượng.
  - **Hai tam giác bằng / đồng dạng**: `COLOR_EQUAL_1` cho tam giác 1, `COLOR_EQUAL_2` cho tam giác 2 (PHÂN BIỆT).
  - **Tổng / nhiều góc phân biệt** (∠A + ∠B + ∠C): `COLOR_EQUAL_1` / `_2` / `_3` cho từng góc.

---

## Ví dụ narration tốt vs xấu

| Xấu (TTS đọc sai)   | Tốt (TTS đọc tự nhiên)           |
|---------------------|----------------------------------|
| `∠IEC = ∠ICE`       | "góc I E C bằng góc I C E"       |
| `△OAC cân tại O`    | "tam giác O A C cân tại O"        |
| `IE = IC`           | "đoạn I E bằng đoạn I C"         |
| `⊥`                 | "vuông góc với"                  |
| `∈`                 | "thuộc" hoặc "nằm trên"          |
| `∀`                 | "với mọi"                        |

---

## Checklist hoàn thành Scene Spec

- [ ] Xác định đúng loại toán (hình phẳng / đại số / 3D)
- [ ] Liệt kê đầy đủ GT và KL
- [ ] Scene 01 chỉ dựng hình cơ bản theo GT, không dựng yếu tố phụ trợ của lời giải
- [ ] Mỗi ý (a, b, c, ...) có scene "Dựng thêm hình + Phân tích" riêng, không lộ hướng giải của ý sau
- [ ] Narration không có ký hiệu toán học (viết bằng lời)
- [ ] Thời lượng mỗi scene ≤ 90s
- [ ] Tổng thời lượng video ≤ 8 phút
- [ ] Mỗi scene có kết quả trung gian rõ ràng (đóng khung)
- [ ] Nét phụ trợ hình học mới (Loại A: `seg_*`): `Create` vĩnh viễn, lưu `self.seg_*`, không có `FadeOut`; spec ghi `bring_to_front` ngay sau
- [ ] Highlight tạm (Loại B: `*_fill`, `*_temp`): `FadeIn`/`FadeOut` trong cùng voiceover block, không để tồn tại vĩnh viễn
- [ ] Mỗi scene có nét Loại A mới: liệt kê `self.persistent_geom.add(seg_new, dot_new, label_new)` ngay sau `Create` trong spec
- [ ] Scene Tổng kết: `FadeOut` chỉ nhắm vào text/proof (title, eq_*, result cũ), không nhắm vào `self.persistent_geom` và nét Loại A
- [ ] Mỗi scene có đủ 5 section: `metadata`, `geometry`, `objects`, `segments`, `layout`
- [ ] `metadata` khai báo `cleanup_start`, `cleanup_end`, `persist` đầy đủ — trong đó `cleanup_end` gồm cả mọi dòng kết luận / `result_tex` / đpcm (hoặc spec ghi rõ `proof.add(result_tex)`); không để text chứng minh orphan khi scene sau có proof mới ở UL
- [ ] Mỗi `segment_N` có `voice`, `actions`, `write` (hoặc `write: ~`)
- [ ] Mọi `<bookmark mark='tên'/>` trong `voice` đều có action `at: tên` tương ứng; không có action thừa không có bookmark
- [ ] Tên bookmark theo pattern `<type>_<name>_expr` (`tri_OFB_expr`, `seg_BF_expr`, `angle_OFB_expr`, `tri_equal_expr`, `seg_equal_expr`, `tri_cgc_expr`, ...) — KHÔNG dùng prefix cũ `bk_`
- [ ] **Mỗi thực thể hình học** (đoạn / góc / tam giác / tứ giác / điểm / circle / arc / radius / diameter / chord / tangent / secant) trong dòng chứng minh đều có bookmark riêng `<type>_<name>_expr` và token tương ứng trong `proof_tokens`
- [ ] **Mỗi từ kết nối semantic** (`=`, `⇒`, `(c.g.c)`, `(g.c.g)`, `(c.c.c)`) có bookmark riêng và token tương ứng (action `sync_relation`)
- [ ] KHÔNG còn giới hạn "≤ 3 bookmark / segment" — segment chứng minh có thể có 8-10+ bookmark
- [ ] Mọi action highlight đều dùng `sync_*` (`sync_segment` / `sync_angle` / `sync_triangle` / `sync_quadrilateral` / `sync_point` / `sync_relation`), KHÔNG raw `Indicate(...)` / `FadeIn(Sector(...))` trong spec
- [ ] Segment chứng minh có nhiều thực thể: dùng `proof_tokens` + actions `sync_*` thay vì `write: text: "..."` đơn lẻ
- [ ] Quy tắc màu: cùng 1 màu (`COLOR_EQUAL_1`) cho tập "bằng nhau"; 2+ màu khác nhau (`COLOR_EQUAL_1` / `_2` / `_3`) khi PHÂN BIỆT 2 tam giác / nhiều góc
- [ ] Loại B (highlight tạm) có cặp FadeIn/FadeOut trong cùng segment hoặc ghi rõ FadeOut ở segment tiếp theo (hoặc dùng `geo.cleanup_temp()`)
- [ ] `write` dòng proof đều có `at:` chỉ định thời điểm Write; không có dòng proof bơ vơ (chỉ áp dụng cho format cũ — dòng đơn 1 bookmark)
