import sys
from pathlib import Path

# scenes/theory/ → project root (chứa manim_helpers/)
_PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(_PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(_PROJECT_ROOT))

from manim import *
import numpy as np
from manim_voiceover import VoiceoverScene

from manim_helpers import (
    COLOR_DEFAULT, COLOR_BACKGROUND, COLOR_GRID,
    COLOR_EQUAL_1, COLOR_EQUAL_2, COLOR_EQUAL_3,
    COLOR_ACTIVE, COLOR_SECONDARY, COLOR_CIRCLE, COLOR_AUX_LINE,
    TIMING_FADE,
    MOTION_ENTER, MOTION_EXIT,
    EMPHASIS_SCALE, EMPHASIS_INDICATE_TIME,
    LAYER_BACKGROUND, LAYER_GEOMETRY, LAYER_MARKERS,
    make_gtts_service,
    TheoryColumn,
    place_figure,
    FIG_CENTER_X, FIG_CENTER_Y, FIG_MAX_W, FIG_MAX_H,
)

viet_tex_template = TexTemplate(
    tex_compiler="xelatex",
    output_format=".xdv",
    preamble=r"""
\usepackage{fontspec}
\usepackage{amsmath}
\usepackage{amssymb}
\usepackage{vntex}
\setmainfont{Times New Roman}
""")


class DuongTron(VoiceoverScene):
    def construct(self):
        self.set_speech_service(make_gtts_service())
        self.setup_scene_style()
        self.scene00_intro()
        self.scene01_khaiNiem()
        self.scene02_chuY()
        self.scene03_nhanXet()
        self.scene04_tinhChat()

    # ── Thiết lập nền ──────────────────────────────────────────────────────────
    def setup_scene_style(self):
        Mobject.set_default(color=COLOR_DEFAULT)
        Tex.set_default(color=COLOR_DEFAULT)
        MathTex.set_default(color=COLOR_DEFAULT)
        self.camera.background_color = COLOR_BACKGROUND
        grid = NumberPlane(
            x_range=[-8, 8, 1], y_range=[-5, 5, 1],
            axis_config={"stroke_width": 0},
            background_line_style={
                "stroke_color": COLOR_GRID,
                "stroke_width": 1,
                "stroke_opacity": 0.4,
            })
        grid.set_z_index(LAYER_BACKGROUND - 10)
        self.add(grid)

    # ── Scene 00: Intro ────────────────────────────────────────────────────────
    def scene00_intro(self):
        self.lesson_title = Tex(
            r"\textbf{ĐƯỜNG TRÒN}",
            tex_template=viet_tex_template, font_size=40)
        self.lesson_title.to_edge(UP, buff=0.4)

        section = Tex(
            r"I. TÓM TẮT LÝ THUYẾT",
            tex_template=viet_tex_template, font_size=28)
        section.next_to(self.lesson_title, DOWN, buff=0.3)

        with self.voiceover(
            "Bài học hôm nay về Đường tròn. Phần một: Tóm tắt lý thuyết."
        ) as ov:
            self.play(Write(self.lesson_title), run_time=ov.duration * 0.6)
            self.play(FadeIn(section), run_time=ov.duration * 0.4)

        self.wait(0.5)
        self.play(FadeOut(section), run_time=MOTION_EXIT)
        self.play(
            self.lesson_title.animate.scale(0.7).to_edge(UP, buff=0.2),
            run_time=MOTION_EXIT)

    # ── Scene 01: Khái niệm đường tròn ────────────────────────────────────────
    def scene01_khaiNiem(self):
        # 1. Heading
        block_heading = Tex(
            r"\textbf{1. Khái niệm đường tròn}",
            tex_template=viet_tex_template, font_size=32)
        block_heading.to_corner(UL, buff=0.5)
        self.play(Write(block_heading), run_time=0.6)

        # 2. TheoryColumn
        col = TheoryColumn(block_heading, has_figure=True)

        # 3. Body lines (chưa add vào scene)
        line1 = Tex(
            r"Trong mặt phẳng, đường tròn tâm $O$ bán kính $R$ (với $R > 0$)",
            tex_template=viet_tex_template, font_size=26)
        line2 = Tex(
            r"là tập hợp các điểm cách điểm $O$ cố định một khoảng $R$,",
            tex_template=viet_tex_template, font_size=26)
        line3 = MathTex(
            r"\text{kí hiệu là: } (O;\,R)",
            tex_template=viet_tex_template, font_size=28)
        col.place(line1)
        col.place(line2)
        col.place_formula_left(line3, indent=0.6, gap=0.30)

        # 4. Dựng hình — tọa độ cục bộ trước place_figure
        R1 = 2.0
        circ_O = Circle(radius=R1, color=COLOR_CIRCLE).set_z_index(LAYER_GEOMETRY)
        dot_O = Dot(ORIGIN, color=COLOR_ACTIVE, radius=0.07).set_z_index(LAYER_MARKERS)
        # Lines/circles before dots in VGroup
        base_fig1 = VGroup(circ_O, dot_O)
        place_figure(base_fig1)

        # Post-place: tọa độ thực tế qua get_center()
        O1_true = dot_O.get_center()
        actual_R1 = circ_O.width / 2
        P1_true = O1_true + RIGHT * actual_R1

        seg_OR = DashedLine(
            O1_true, P1_true, color=COLOR_SECONDARY, dash_length=0.12
        ).set_z_index(LAYER_GEOMETRY)
        dot_P = Dot(P1_true, color=COLOR_DEFAULT, radius=0.05).set_z_index(LAYER_MARKERS)
        label_O = MathTex("O", font_size=24).next_to(dot_O, LEFT, buff=0.15).set_z_index(LAYER_MARKERS)
        label_R = MathTex("R", font_size=24).set_z_index(LAYER_MARKERS)
        label_R.move_to((O1_true + P1_true) / 2 + UP * 0.22)

        # Lưu để scene 02 tái dùng
        self.figure_group = VGroup(circ_O, dot_O, seg_OR, dot_P, label_O, label_R)
        self.circ_O_s01 = circ_O

        # 5. Voiceover + animations
        with self.voiceover(
            "Khái niệm. Trong mặt phẳng, đường tròn tâm O bán kính R "
            "là tập hợp tất cả các điểm cách điểm O một khoảng bằng R. "
            "Điều kiện là R phải lớn hơn không."
        ) as ov:
            self.play(
                FadeIn(line1), FadeIn(line2),
                Create(circ_O),
                run_time=ov.duration * 0.7)
            self.play(
                Create(dot_O), Write(label_O),
                run_time=ov.duration * 0.3)

        with self.voiceover(
            "Đường tròn này được kí hiệu là O chấm phẩy R. "
            "Trên hình vẽ, đoạn từ O đến đường tròn có độ dài R."
        ) as ov:
            self.play(
                FadeIn(line3),
                Create(seg_OR),
                run_time=ov.duration * 0.6)
            self.play(
                Create(dot_P), Write(label_R),
                run_time=ov.duration * 0.4)

        # Indicate dòng định nghĩa
        self.play(
            Indicate(line1, scale_factor=EMPHASIS_SCALE, color=COLOR_ACTIVE),
            run_time=EMPHASIS_INDICATE_TIME)
        self.wait(0.5)

        # Cleanup: giữ figure_group cho scene 02
        self.play(
            FadeOut(block_heading),
            FadeOut(col.all),
            run_time=MOTION_EXIT)

    # ── Scene 02: Chú ý ───────────────────────────────────────────────────────
    def scene02_chuY(self):
        # 1. Heading
        block_heading = Tex(
            r"\textbf{Chú ý:}",
            tex_template=viet_tex_template, font_size=32)
        block_heading.to_corner(UL, buff=0.5)
        self.play(Write(block_heading), run_time=0.6)

        # 2. TheoryColumn
        col = TheoryColumn(block_heading, has_figure=True)

        # 3. Body lines
        note1 = Tex(
            r"$\bullet$\; Một đường tròn hoàn toàn xác định khi biết tâm và bán kính.",
            tex_template=viet_tex_template, font_size=26)
        note2a = Tex(
            r"$\bullet$\; Khi không chú ý đến bán kính của đường tròn $(O;R)$,",
            tex_template=viet_tex_template, font_size=26)
        note2b = Tex(
            r"\quad ta cũng có thể kí hiệu là đường tròn $(O)$.",
            tex_template=viet_tex_template, font_size=26)
        col.place_bullet(note1)
        col.place_bullet(note2a)
        col.place_bullet(note2b, indent=0.70)

        # 4. Nhãn thêm vào hình tái dùng từ scene 01
        label_OR = MathTex(
            r"(O;\,R)", font_size=22, color=COLOR_SECONDARY
        ).next_to(self.circ_O_s01, UP, buff=0.15).set_z_index(LAYER_MARKERS)
        label_O_simple = MathTex(
            r"(O)", font_size=22, color=COLOR_ACTIVE
        ).next_to(self.circ_O_s01, UP, buff=0.15).set_z_index(LAYER_MARKERS)

        # 5. Voiceover + animations
        with self.voiceover(
            "Chú ý. Một đường tròn hoàn toàn xác định khi ta biết "
            "tâm và bán kính của nó."
        ) as ov:
            self.play(FadeIn(note1), run_time=ov.duration)

        with self.voiceover(
            "Ngoài ra, khi không cần nhấn mạnh bán kính, "
            "ta có thể kí hiệu đường tròn tâm O đơn giản là O trong ngoặc tròn."
        ) as ov:
            self.play(
                FadeIn(note2a), FadeIn(note2b),
                FadeIn(label_OR),
                run_time=ov.duration * 0.5)
            self.play(
                Indicate(label_OR, scale_factor=EMPHASIS_SCALE, color=COLOR_ACTIVE),
                run_time=ov.duration * 0.2)
            self.play(
                FadeOut(label_OR),
                FadeIn(label_O_simple),
                run_time=ov.duration * 0.2)
            self.play(
                Indicate(label_O_simple, scale_factor=EMPHASIS_SCALE, color=COLOR_ACTIVE),
                run_time=ov.duration * 0.1)

        self.wait(0.5)

        # Cleanup: giữ figure_group cho scene 03 (sẽ FadeOut đầu scene 03)
        self.play(
            FadeOut(block_heading),
            FadeOut(col.all),
            FadeOut(label_O_simple),
            run_time=MOTION_EXIT)

    # ── Scene 03: Nhận xét — Vị trí tương đối ────────────────────────────────
    def scene03_nhanXet(self):
        # Dọn hình từ scene 01/02
        self.play(FadeOut(self.figure_group), run_time=MOTION_EXIT)

        # 1. Heading
        block_heading = Tex(
            r"\textbf{Nhận xét:}",
            tex_template=viet_tex_template, font_size=32)
        block_heading.to_corner(UL, buff=0.5)
        self.play(Write(block_heading), run_time=0.6)

        # 2. TheoryColumn
        col = TheoryColumn(block_heading, has_figure=True)

        # 3. Body lines
        intro = Tex(
            r"$\bullet$\; Vị trí tương đối của một điểm đối với đường tròn:",
            tex_template=viet_tex_template, font_size=26)
        txt_on = Tex(
            r"$+\;$ Điểm $M$ nằm \textbf{trên} đường tròn $(O)$ nếu $OM = R$",
            tex_template=viet_tex_template, font_size=25)
        txt_in = Tex(
            r"$+\;$ Điểm $M$ nằm \textbf{trong} đường tròn $(O)$ nếu $OM < R$",
            tex_template=viet_tex_template, font_size=25)
        txt_out = Tex(
            r"$+\;$ Điểm $M$ nằm \textbf{ngoài} đường tròn $(O)$ nếu $OM > R$",
            tex_template=viet_tex_template, font_size=25)
        txt_hinh_tron = Tex(
            r"$\bullet$\; Hình tròn tâm $O$ bán kính $R$ gồm các điểm nằm"
            r" trên và nằm trong đường tròn $(O;R)$.",
            tex_template=viet_tex_template, font_size=26)
        col.place_bullet(intro)
        col.place_bullet(txt_on,  indent=0.70, gap=0.15)
        col.place_bullet(txt_in,  indent=0.70, gap=0.15)
        col.place_bullet(txt_out, indent=0.70, gap=0.20)
        col.place_bullet(txt_hinh_tron)

        # 4. Dựng hình — chỉ vòng tròn + tâm trước place_figure
        R3 = 1.8
        ang1 = 50  * DEGREES
        ang2 = 160 * DEGREES
        ang3 = 290 * DEGREES

        circ3 = Circle(radius=R3, color=COLOR_CIRCLE).set_z_index(LAYER_GEOMETRY)
        dot_O3 = Dot(ORIGIN, color=COLOR_DEFAULT, radius=0.06).set_z_index(LAYER_MARKERS)
        base3 = VGroup(circ3, dot_O3)
        place_figure(base3)

        # Post-place: tọa độ thực tế
        O3_true  = dot_O3.get_center()
        actual_R3 = circ3.width / 2

        M1_true = O3_true + actual_R3 * np.array([np.cos(ang1), np.sin(ang1), 0])
        M2_true = O3_true + 0.85 * actual_R3 * np.array([np.cos(ang2), np.sin(ang2), 0])
        M3_true = O3_true + 1.5  * actual_R3 * np.array([np.cos(ang3), np.sin(ang3), 0])

        # Đoạn dashed OM (tại tọa độ thực)
        seg_OM1 = DashedLine(
            O3_true, M1_true, color=COLOR_EQUAL_1, dash_length=0.1
        ).set_z_index(LAYER_GEOMETRY)
        seg_OM2 = DashedLine(
            O3_true, M2_true, color=COLOR_EQUAL_2, dash_length=0.1
        ).set_z_index(LAYER_GEOMETRY)
        seg_OM3 = DashedLine(
            O3_true, M3_true, color=COLOR_EQUAL_3, dash_length=0.1
        ).set_z_index(LAYER_GEOMETRY)

        # Điểm M và nhãn
        dot_M1 = Dot(M1_true, color=COLOR_EQUAL_1, radius=0.07).set_z_index(LAYER_MARKERS)
        dot_M2 = Dot(M2_true, color=COLOR_EQUAL_2, radius=0.07).set_z_index(LAYER_MARKERS)
        dot_M3 = Dot(M3_true, color=COLOR_EQUAL_3, radius=0.07).set_z_index(LAYER_MARKERS)

        label_O3 = MathTex("O", font_size=22).next_to(dot_O3, DOWN, buff=0.12).set_z_index(LAYER_MARKERS)
        label_M1 = MathTex("M", font_size=22, color=COLOR_EQUAL_1).next_to(dot_M1, UR, buff=0.10).set_z_index(LAYER_MARKERS)
        label_M2 = MathTex("M", font_size=22, color=COLOR_EQUAL_2).next_to(dot_M2, UL, buff=0.10).set_z_index(LAYER_MARKERS)
        label_M3 = MathTex("M", font_size=22, color=COLOR_EQUAL_3).next_to(dot_M3, DR, buff=0.10).set_z_index(LAYER_MARKERS)

        # Vùng tô (hình tròn) — opacity=0 ban đầu
        filled_circ = Circle(
            radius=actual_R3, color=COLOR_CIRCLE,
            fill_color=COLOR_CIRCLE, fill_opacity=0.0
        ).move_to(O3_true).set_z_index(LAYER_GEOMETRY - 1)

        # 5. Voiceover + animations
        with self.voiceover(
            "Nhận xét. Với điểm M trong mặt phẳng và đường tròn tâm O bán kính R, "
            "ta có ba vị trí tương đối."
        ) as ov:
            self.play(
                FadeIn(intro),
                Create(circ3),
                run_time=ov.duration * 0.7)
            self.play(
                Create(dot_O3), Write(label_O3),
                run_time=ov.duration * 0.3)

        with self.voiceover(
            "Điểm M nằm trên đường tròn khi O M bằng R."
        ) as ov:
            self.play(
                FadeIn(txt_on),
                Create(seg_OM1), Create(dot_M1), Write(label_M1),
                run_time=ov.duration * 0.7)
            self.play(
                Indicate(dot_M1, scale_factor=1.4, color=COLOR_EQUAL_1),
                run_time=ov.duration * 0.3)

        with self.voiceover(
            "Điểm M nằm trong đường tròn khi O M nhỏ hơn R."
        ) as ov:
            self.play(
                FadeIn(txt_in),
                Create(seg_OM2), Create(dot_M2), Write(label_M2),
                run_time=ov.duration * 0.7)
            self.play(
                Indicate(dot_M2, scale_factor=1.4, color=COLOR_EQUAL_2),
                run_time=ov.duration * 0.3)

        with self.voiceover(
            "Điểm M nằm ngoài đường tròn khi O M lớn hơn R."
        ) as ov:
            self.play(
                FadeIn(txt_out),
                Create(seg_OM3), Create(dot_M3), Write(label_M3),
                run_time=ov.duration * 0.7)
            self.play(
                Indicate(dot_M3, scale_factor=1.4, color=COLOR_EQUAL_3),
                run_time=ov.duration * 0.3)

        with self.voiceover(
            "Ngoài ra, hình tròn bao gồm tất cả các điểm "
            "nằm trên và nằm trong đường tròn đó."
        ) as ov:
            self.play(
                FadeIn(txt_hinh_tron),
                FadeIn(filled_circ),
                filled_circ.animate.set_fill(opacity=0.12),
                run_time=ov.duration)

        self.wait(0.5)

        # Cleanup all
        all_s03 = VGroup(
            base3, filled_circ,
            seg_OM1, seg_OM2, seg_OM3,
            dot_M1, dot_M2, dot_M3,
            label_O3, label_M1, label_M2, label_M3)
        self.play(
            FadeOut(block_heading),
            FadeOut(col.all),
            FadeOut(all_s03),
            run_time=MOTION_EXIT)

    # ── Scene 04: Tính chất đối xứng của đường tròn ───────────────────────────
    def scene04_tinhChat(self):
        # 1. Heading
        block_heading = Tex(
            r"\textbf{2. Tính chất đối xứng của đường tròn}",
            tex_template=viet_tex_template, font_size=30)
        block_heading.to_corner(UL, buff=0.5)
        self.play(Write(block_heading), run_time=0.6)

        # 2. TheoryColumn
        col = TheoryColumn(block_heading, has_figure=True)

        # 3. Body lines
        line_tam1 = Tex(
            r"$\bullet$\; Đường tròn là hình có \textbf{tâm đối xứng}:",
            tex_template=viet_tex_template, font_size=26)
        line_tam2 = Tex(
            r"\quad Tâm của đường tròn là tâm đối xứng của đường tròn đó.",
            tex_template=viet_tex_template, font_size=26)
        line_truc1 = Tex(
            r"$\bullet$\; Đường tròn là hình có \textbf{trục đối xứng}:",
            tex_template=viet_tex_template, font_size=26)
        line_truc2 = Tex(
            r"\quad Bất kì đường kính nào cũng là trục đối xứng của đường tròn đó.",
            tex_template=viet_tex_template, font_size=26)
        col.place_bullet(line_tam1)
        col.place_bullet(line_tam2, indent=0.70, gap=0.20)
        col.skip(0.10)
        col.place_bullet(line_truc1, gap=0.20)
        col.place_bullet(line_truc2, indent=0.70, gap=0.20)

        # 4. Dựng hình — chỉ circle + dot_O trước place_figure
        R4 = 2.0
        circ4 = Circle(radius=R4, color=COLOR_CIRCLE).set_z_index(LAYER_GEOMETRY)
        dot_O4 = Dot(ORIGIN, color=COLOR_ACTIVE, radius=0.07).set_z_index(LAYER_MARKERS)
        base4 = VGroup(circ4, dot_O4)
        place_figure(base4)

        # Post-place: tọa độ thực tế
        O4_true   = dot_O4.get_center()
        actual_R4 = circ4.width / 2

        A_true  = O4_true + LEFT  * actual_R4
        Ap_true = O4_true + RIGHT * actual_R4

        seg_AAp = Line(A_true, Ap_true, color=COLOR_DEFAULT).set_z_index(LAYER_GEOMETRY)

        # Trục đứng dashed
        axis_v = DashedLine(
            O4_true + DOWN * (actual_R4 + 0.5),
            O4_true + UP   * (actual_R4 + 0.5),
            color=COLOR_AUX_LINE, dash_length=0.14
        ).set_z_index(LAYER_GEOMETRY)

        # Trục chéo 45° (minh họa "bất kì đường kính nào")
        cos45 = np.cos(45 * DEGREES)
        axis_diag = DashedLine(
            O4_true + actual_R4 * np.array([-cos45, -cos45, 0]),
            O4_true + actual_R4 * np.array([ cos45,  cos45, 0]),
            color=COLOR_AUX_LINE, dash_length=0.14
        ).set_z_index(LAYER_GEOMETRY)

        # Dots và labels (sau place_figure)
        dot_A  = Dot(A_true,  color=COLOR_DEFAULT, radius=0.06).set_z_index(LAYER_MARKERS)
        dot_Ap = Dot(Ap_true, color=COLOR_DEFAULT, radius=0.06).set_z_index(LAYER_MARKERS)

        label_O4 = MathTex("O",  font_size=24).next_to(dot_O4, DOWN, buff=0.15).set_z_index(LAYER_MARKERS)
        label_A  = MathTex("A",  font_size=24).next_to(A_true,  LEFT,  buff=0.12).set_z_index(LAYER_MARKERS)
        label_Ap = MathTex("A'", font_size=24).next_to(Ap_true, RIGHT, buff=0.12).set_z_index(LAYER_MARKERS)

        # 5. Voiceover + animations
        with self.voiceover(
            "Tính chất đối xứng của đường tròn. "
            "Thứ nhất, đường tròn là hình có tâm đối xứng. "
            "Tâm của đường tròn chính là tâm đối xứng của đường tròn đó."
        ) as ov:
            self.play(
                FadeIn(line_tam1), FadeIn(line_tam2),
                Create(circ4),
                run_time=ov.duration * 0.5)
            self.play(
                Create(dot_O4), Write(label_O4),
                run_time=ov.duration * 0.2)
            self.play(
                Create(dot_A), Write(label_A),
                Create(dot_Ap), Write(label_Ap),
                Create(seg_AAp),
                run_time=ov.duration * 0.2)
            self.play(
                Indicate(dot_O4, scale_factor=1.5, color=COLOR_EQUAL_1),
                run_time=ov.duration * 0.1)

        with self.voiceover(
            "Thứ hai, đường tròn là hình có trục đối xứng. "
            "Bất kì đường kính nào của đường tròn cũng là một trục đối xứng. "
            "Điều này có nghĩa là đường tròn có vô số trục đối xứng."
        ) as ov:
            self.play(
                FadeIn(line_truc1), FadeIn(line_truc2),
                Create(axis_v),
                run_time=ov.duration * 0.5)
            self.play(
                Create(axis_diag),
                run_time=ov.duration * 0.3)
            self.play(
                Indicate(axis_v,    scale_factor=EMPHASIS_SCALE, color=COLOR_EQUAL_1),
                Indicate(axis_diag, scale_factor=EMPHASIS_SCALE, color=COLOR_EQUAL_1),
                run_time=ov.duration * 0.2)

        # Indicate terms_bold
        self.play(
            Indicate(line_tam1,  scale_factor=EMPHASIS_SCALE, color=COLOR_ACTIVE),
            Indicate(line_truc1, scale_factor=EMPHASIS_SCALE, color=COLOR_ACTIVE),
            run_time=EMPHASIS_INDICATE_TIME)
        self.wait(0.5)

        # Cleanup all
        all_s04 = VGroup(
            base4, seg_AAp, axis_v, axis_diag,
            dot_A, dot_Ap, label_O4, label_A, label_Ap)
        self.play(
            FadeOut(block_heading),
            FadeOut(col.all),
            FadeOut(all_s04),
            run_time=MOTION_EXIT)
