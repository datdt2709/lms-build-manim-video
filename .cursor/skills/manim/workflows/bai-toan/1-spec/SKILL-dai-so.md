---
name: manim-step-1-scene-spec-dai-so
description: Tạo Scene Spec Markdown từ ảnh đề/lời giải bài toán đại số. Dùng khi lập kế hoạch video đại số/hệ phương trình, chia scene và viết narration TTS tiếng Việt trước khi code Manim.
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
   - Loại toán: Hình phẳng / Đại số / Hình không gian
   - Giả thiết (GT): Liệt kê đầy đủ các điều kiện cho
   - Kết luận (KL): Những gì cần chứng minh / tìm

2. **Đọc lời giải** (nếu có):
   - Chia lời giải thành các **bước lập luận riêng biệt**
   - Mỗi bước = 1 ý tưởng logic = có thể thành 1 scene
   - Chú ý các điểm "pivotal": nơi chiến thuật thay đổi, nơi kết quả trung gian xuất hiện

3. **Xác định dạng toán** để chọn skill phù hợp ở Step 2:
   - Hình phẳng → dùng `manim-hinh-phang`
   - Đại số / Hình không gian → dùng `manim-dai-so-hinh-khong-gian`

### Bước 2 – Chia scene

Nguyên tắc chia scene:

| Scene         | Nội dung                              | Thời lượng ước tính |
|---------------|---------------------------------------|---------------------|
| Scene 01      | Intro + Đề bài (GT/KL) + Dựng hình    | 60–90s              |
| Scene 02      | Chiến thuật / Tổng quan hướng giải    | 30–45s              |
| Scene 03..N-1 | Mỗi bước chứng minh / lập luận chính  | 45–90s/scene        |
| Scene N       | Tổng kết, kết luận cuối               | 30–45s              |

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

Tạo file `scene-spec.md` trong thư mục làm việc với cấu trúc sau:

---

## Format Scene Spec chuẩn

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

**Mục đích**: Giới thiệu bài học, trình bày GT/KL, dựng hình

**Narration (phần 1 – Intro)**:
> "Chào các em! Hôm nay thầy trò chúng ta sẽ cùng nhau xử lý một bài hình học rất thú vị..."

**Elements**:
- `title1`: Text "Bài giảng Hình học Lớp 9"
- `title2`: Text "Chứng minh Trung điểm và Tiếp tuyến"
- `gt_vgroup`: VGroup các dòng giả thiết (lưu vào `self.gt_vgroup`)
- `kl_vgroup`: VGroup các dòng kết luận (lưu vào `self.kl_vgroup`)
- `diagram`: Hình vẽ đầy đủ (lưu vào `self.diagram`)

**Narration (phần 2 – Dựng hình)**:
> "Cho nửa đường tròn tâm O, đường kính A B. Lấy điểm C trên nửa đường tròn và điểm D trên A B..."

**Animation sequence**:
1. Write title1 → FadeOut → Write title2 → FadeOut
2. Write gt_vgroup[0:4] (4 dòng đầu GT)
3. Create diagram[0] (base: nửa đường tròn + đường kính)
4. Create diagram[1], Write diagram[2] (dot_C, label_C)
5. Create diagram[3], Write diagram[4] (dot_D, label_D)
6. Create diagram[5], Create diagram[6] (AC, BC)
7. Create diagram[7] (EF)
8. Create diagram[8..11] (E, F và nhãn)
9. Write gt_vgroup[4] + Create diagram[12..14] (tiếp tuyến CI, I)
10. Create diagram[15..16] (góc vuông)
11. Write kl_vgroup, Indicate kl_vgroup[1], Indicate kl_vgroup[2]

**Thời lượng ước tính**: 75s

**State lưu lại**: `self.gt_vgroup`, `self.kl_vgroup`, `self.diagram`, `self.dot_C`, `self.dot_D`, `self.dot_E`, `self.dot_F`, `self.dot_I`, `self.diameter`, `self.segment_AC`, `self.segment_BC`, `self.line_EF_obj`, `self.right_angle_C_ACB`

---

## Scene 02 – Chiến thuật câu a

**Mục đích**: Giải thích hướng tiếp cận: bắc cầu IE = IC = IF

**Narration**:
> "Câu a: Chứng minh I là trung điểm của E F. Để làm điều này, chúng ta sẽ dùng chiến thuật bắc cầu..."

**Elements**:
- `title_a`: Tiêu đề "Câu a: CM I là trung điểm EF"
- `muc_tieu_group`: "Mục tiêu: IE = IF"
- `strategy_text`: "Ý tưởng: Bắc cầu qua IC"
- Highlight `segment_IE` (YELLOW), `segment_IF` (YELLOW), `segment_IC` (GREEN)
- `tri_IEC` (YELLOW, fill_opacity=0.4) → FadeOut
- `tri_IFC` (GREEN, fill_opacity=0.4) → FadeOut
- `final_goal_text`: "Ta sẽ CM: IE = IC và IF = IC"

**Dọn dẹp đầu scene**: FadeOut(gt_vgroup, kl_vgroup)
**Thời lượng ước tính**: 40s

---

## Scene 03 – Chứng minh IE = IC

**Mục đích**: CM tam giác IEC cân tại I ⟹ IE = IC

**Narration**:
> "Chúng ta bắt đầu với mục tiêu đầu tiên: Chứng minh đoạn I E bằng đoạn I C..."

**Luận điểm chính** (mỗi luận điểm = 1 voiceover block):
1. Mục tiêu: CM góc IEC = góc ICE
2. Phân tích góc ICE: IC là tiếp tuyến → IC ⊥ OC → ∠OCI = 90° → ∠OCA + ∠ICE = 90°
3. △OAC cân tại O (OA = OC = R) → ∠OCA = ∠OAC
4. Phương trình 1: ∠OAC + ∠ICE = 90°
5. Phân tích góc IEC: ∠IEC đối đỉnh ∠AED
6. △AED vuông tại D → ∠DAE + ∠AED = 90°
7. Phương trình 2: ∠DAE + ∠IEC = 90°
8. Kết luận: ∠ICE = ∠IEC → △IEC cân tại I → **IE = IC** ✓

**Kết quả lưu**: `self.result1_group` (IE = IC + box GREEN) → `.to_corner(UR)`
**Thời lượng ước tính**: 90s

---

## Scene 04 – Chứng minh IF = IC

**Mục đích**: CM tam giác IFC cân tại I ⟹ IF = IC

**Luận điểm chính**:
1. Mục tiêu: CM góc IFC = góc ICF
2. C ∈ nửa đường tròn đk AB → ∠ACB = 90°
3. △ECF vuông tại C (vì E ∈ AC, F ∈ BC)
4. ∠CEF + ∠CFE = 90° (2 góc nhọn trong △ECF vuông)
5. Từ Scene 03: ∠CEF = ∠ICE
6. Suy ra: ∠CFE = ∠ICF → △IFC cân tại I → **IF = IC** ✓

**Thời lượng ước tính**: 75s

---

## Scene 05 – Tổng kết & Câu b

**Mục đích**: Tổng kết câu a, chứng minh câu b

**Câu a tổng kết**:
- IE = IC (result1_group từ UR)
- IF = IC (result2_group)
- ⟹ IE = IF ⟹ I là trung điểm EF (đóng khung RED)

**Câu b**:
1. △ECF vuông tại C, I là trung điểm EF (cạnh huyền) → I là tâm đường tròn ngoại tiếp △ECF
2. Đường tròn ngoại tiếp = (I, IC)
3. Cần CM: OC là tiếp tuyến của (I) ⟺ OC ⊥ IC
4. Điều này đúng vì IC là tiếp tuyến của (O) ⟹ IC ⊥ OC (gt) → **Q.E.D.**

**Thời lượng ước tính**: 60s
```

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
- [ ] Mỗi scene có tiêu đề, mục đích, narration rõ ràng
- [ ] Chỉ rõ `self.*` nào cần lưu để scene sau truy cập
- [ ] Narration không có ký hiệu toán học (viết bằng lời)
- [ ] Thời lượng mỗi scene ≤ 90s
- [ ] Tổng thời lượng video ≤ 8 phút
- [ ] Mỗi scene có kết quả trung gian rõ ràng (đóng khung)
