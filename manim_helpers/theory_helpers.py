"""theory_helpers – Layout utilities cho video bài giảng lý thuyết.

Cung cấp:
    TheoryColumn   : quản lý cursor text, tránh drift (tương tự ProofColumn nhưng không có token proof)
    place_figure   : scale và đặt hình đơn vào FigurePanel bên phải
    place_dual_figures : xếp 2 hình nhỏ cạnh nhau (DualFigurePanel)

Hằng số vùng màn hình:
    TEXT_LEFT_X, TEXT_RIGHT_WITH_FIG, TEXT_RIGHT_NO_FIG
    FIG_CENTER_X, FIG_CENTER_Y, FIG_MAX_W, FIG_MAX_H
    DUAL_FIG_MAX_W, DUAL_FIG_BUFF
"""

import numpy as np
from manim import config, VGroup, Tex, TexTemplate, Rectangle, LEFT, RIGHT, UP, DOWN, WHITE

# ---------------------------------------------------------------------------
# Layout zone constants
# ---------------------------------------------------------------------------

TEXT_LEFT_X          = -6.8   # left edge text column (khớp to_corner UL buff=0.5)
TEXT_RIGHT_WITH_FIG  =  0.3   # right boundary text khi có hình
TEXT_RIGHT_NO_FIG    =  5.8   # right boundary text khi không có hình

FIG_CENTER_X         =  4.1   # center x của FigurePanel
FIG_CENTER_Y         = -0.3   # center y của FigurePanel
FIG_MAX_W            =  3.5   # max width hình đơn
FIG_MAX_H            =  4.6   # max height hình đơn

DUAL_FIG_MAX_W       =  1.55  # max width mỗi hình trong DualFigurePanel
DUAL_FIG_BUFF        =  0.35  # khoảng cách giữa 2 hình trong dual


# ---------------------------------------------------------------------------
# TheoryColumn
# ---------------------------------------------------------------------------

class TheoryColumn:
    """Quản lý vị trí cursor cho cột text bài giảng lý thuyết.

    Giải quyết cùng vấn đề cursor-drift như ProofColumn nhưng dành cho
    text lý thuyết: không có token proof, không bookmark voiceover.

    Ví dụ::

        col = TheoryColumn(block_heading, has_figure=True)

        line1 = Tex("...", font_size=26)
        col.place(line1)

        formula = MathTex("...", font_size=34)
        col.place_formula(formula)

        bullet = Tex("...", font_size=26)
        col.place_bullet(bullet)

        # Dọn dẹp cuối scene:
        self.play(FadeOut(col.all))
    """

    def __init__(self, anchor_mob, has_figure: bool = True,
                 initial_gap: float = 0.35):
        """
        Args:
            anchor_mob: Mobject làm anchor (thường là block_heading).
                        TheoryColumn lấy left_x từ anchor_mob.get_left()[0].
            has_figure: True nếu scene có FigurePanel bên phải — thu hẹp
                        max_width để text không chồng lên hình.
            initial_gap: Khoảng cách từ bottom(anchor_mob) xuống dòng đầu tiên.
        """
        self.left_x     = anchor_mob.get_left()[0]
        self.cursor_y   = anchor_mob.get_bottom()[1] - initial_gap
        self.has_figure = has_figure
        self.max_width  = (TEXT_RIGHT_WITH_FIG - self.left_x
                           if has_figure
                           else TEXT_RIGHT_NO_FIG - self.left_x)
        self._items     = VGroup()

    # ------------------------------------------------------------------
    # Placement methods
    # ------------------------------------------------------------------

    def place(self, mob, gap: float = 0.20):
        """Đặt mob tại cursor, căn trái left_x, cập nhật cursor."""
        mob.move_to(
            [self.left_x, self.cursor_y - mob.height / 2, 0],
            aligned_edge=LEFT)
        self._items.add(mob)
        self.cursor_y = mob.get_bottom()[1] - gap
        return mob

    def place_formula(self, mob, gap: float = 0.35):
        """Đặt formula căn giữa cột text (không căn trái), gap lớn hơn."""
        col_center_x = self.left_x + self.max_width / 2
        mob.move_to([col_center_x, self.cursor_y - mob.height / 2, 0])
        self._items.add(mob)
        self.cursor_y = mob.get_bottom()[1] - gap
        return mob

    def place_formula_left(self, mob, indent: float = 0.6, gap: float = 0.30):
        """Công thức ngắn căn trái với indent nhỏ.

        Dùng thay ``place_formula()`` khi công thức không chiếm toàn cột
        (VD: hệ thức ngắn, kết quả trung gian). Tránh tình trạng công thức
        bị kéo ra giữa cột khi cột text hẹp (has_figure=True).
        """
        mob.move_to(
            [self.left_x + indent, self.cursor_y - mob.height / 2, 0],
            aligned_edge=LEFT)
        self._items.add(mob)
        self.cursor_y = mob.get_bottom()[1] - gap
        return mob

    def place_bullet(self, mob, indent: float = 0.35, gap: float = 0.18):
        """Đặt bullet point thụt lề indent so với left_x."""
        mob.move_to(
            [self.left_x + indent, self.cursor_y - mob.height / 2, 0],
            aligned_edge=LEFT)
        self._items.add(mob)
        self.cursor_y = mob.get_bottom()[1] - gap
        return mob

    def skip(self, gap: float = 0.25):
        """Dịch cursor xuống gap mà không add Mobject (tạo khoảng trống)."""
        self.cursor_y -= gap

    # ------------------------------------------------------------------
    # Utilities
    # ------------------------------------------------------------------

    def at_limit(self) -> bool:
        """True nếu cursor đã xuống gần mép dưới màn hình (y < -3.4)."""
        return self.cursor_y < -3.4

    @property
    def all(self) -> VGroup:
        """VGroup tất cả Mobjects đã add — dùng để FadeOut(col.all)."""
        return self._items


# ---------------------------------------------------------------------------
# FigurePanel helpers
# ---------------------------------------------------------------------------

def make_lesson_title(text: str, tex_template: TexTemplate,
                      font_size: int = 36,
                      bg_color: str = "#1565C0") -> VGroup:
    """Tạo tiêu đề bài giảng với nền màu, flush top màn hình.

    Args:
        text:         LaTeX string cho tiêu đề (VD: r"\\textbf{BÀI 1. TỨ GIÁC NỘI TIẾP}").
        tex_template: TexTemplate có hỗ trợ tiếng Việt (viet_tex_template).
        font_size:    Cỡ chữ tiêu đề, mặc định 36.
        bg_color:     Màu nền, mặc định xanh đậm ``"#1565C0"``.

    Returns:
        VGroup(title_bg, title_text) đã được ``to_edge(UP, buff=0.0)``.

    Ví dụ::

        self.lesson_title = make_lesson_title(
            r"\\textbf{BÀI 1. TỨ GIÁC NỘI TIẾP}", viet_tex_template)
        self.play(FadeIn(self.lesson_title))
    """
    title_bg = Rectangle(
        width=config.frame_width, height=0.78,
        fill_color=bg_color, fill_opacity=1.0, stroke_width=0,
    )
    title_text = Tex(text, tex_template=tex_template,
                     font_size=font_size, color=WHITE)
    title_text.move_to(title_bg.get_center())
    group = VGroup(title_bg, title_text)
    group.to_edge(UP, buff=0.0)
    return group


def place_figure(figure_group: VGroup) -> VGroup:
    """Scale và đặt hình đơn vào FigurePanel chuẩn (phải màn hình).

    Args:
        figure_group: VGroup chứa toàn bộ Mobjects của hình.

    Returns:
        figure_group đã được scale và move_to, để chaining tiện hơn.

    Ví dụ::

        figure_group = VGroup(circle, quad_ABCD, dot_O, *labels)
        place_figure(figure_group)
        self.play(Create(circle))
    """
    if figure_group.width > FIG_MAX_W:
        figure_group.scale_to_fit_width(FIG_MAX_W)
    if figure_group.height > FIG_MAX_H:
        figure_group.scale_to_fit_height(FIG_MAX_H)
    figure_group.move_to([FIG_CENTER_X, FIG_CENTER_Y, 0])
    return figure_group


def place_dual_figures(
    fig_left: VGroup,
    fig_right: VGroup,
    label_left: str = None,
    label_right: str = None,
    tex_template: TexTemplate = None,
) -> VGroup:
    """Scale 2 hình nhỏ, xếp cạnh nhau, đặt vào FigurePanel.

    Dùng cho block nhan_xet / chu_y có 2 hình minh họa cạnh nhau.

    Args:
        fig_left:      VGroup hình trái.
        fig_right:     VGroup hình phải.
        label_left:    Nhãn dưới hình trái (Tex string, optional).
        label_right:   Nhãn dưới hình phải (Tex string, optional).
        tex_template:  TeX template cho nhãn (cần nếu nhãn có tiếng Việt).

    Returns:
        VGroup bao gồm cả 2 hình và nhãn (nếu có).

    Ví dụ::

        dual = place_dual_figures(
            rect_group, sq_group,
            label_left="Hình chữ nhật", label_right="Hình vuông",
            tex_template=viet_tex_template)
        self.play(Create(rect_ABCD), Create(sq_EFGH))
        # Cleanup:
        self.play(FadeOut(dual))
    """
    for fig in (fig_left, fig_right):
        if fig.width > DUAL_FIG_MAX_W:
            fig.scale_to_fit_width(DUAL_FIG_MAX_W)
        if fig.height > 3.5:
            fig.scale_to_fit_height(3.5)

    dual = VGroup(fig_left, fig_right).arrange(RIGHT, buff=DUAL_FIG_BUFF)
    dual.move_to([FIG_CENTER_X, FIG_CENTER_Y, 0])

    result = VGroup(fig_left, fig_right)

    if label_left:
        lbl_l = Tex(label_left, font_size=20,
                    **({"tex_template": tex_template} if tex_template else {}))
        lbl_l.next_to(fig_left, DOWN, buff=0.15)
        result.add(lbl_l)

    if label_right:
        lbl_r = Tex(label_right, font_size=20,
                    **({"tex_template": tex_template} if tex_template else {}))
        lbl_r.next_to(fig_right, DOWN, buff=0.15)
        result.add(lbl_r)

    return result
