"""Layout helpers cho proof column management.

`ProofColumn` giải quyết bài toán cursor drift khi quản lý cột chứng minh:
- Tự động track `left_x` cố định — cursor luôn là `[left_x, y, 0]`, không bị drift
- Auto-update cursor sau mỗi dòng / note được thêm vào
- Expose `proof` VGroup để FadeOut toàn bộ cùng lúc ở cuối scene

Dùng:
    from manim_helpers import ProofColumn

    col = ProofColumn(self, anchor_mob=title, gap=0.4)

    pf_01 = ProofLine(...)
    col.place_line(pf_01)           # place tại cursor, scene.add, cập nhật cursor
    with self.voiceover(text="...") as ov:
        sync_angle(self, "mark1", pf_01.write("tok1"), ...)

    note1 = Tex(r"(lý do...)", ...)
    col.place_note(note1)           # next_to cursor, add to proof, cập nhật cursor
    self.play(Write(note1))         # caller tự animate

    # cuối scene:
    self.play(FadeOut(col.proof), FadeOut(title))
"""

from __future__ import annotations

import numpy as np
from manim import DOWN, VGroup, LEFT


class ProofColumn:
    """Quản lý cột chứng minh với cursor tự động cập nhật.

    Parameters
    ----------
    scene : VoiceoverScene
        Scene hiện tại (dùng để gọi `scene.add` khi `place_line` được gọi).
    anchor_mob : Mobject
        Mobject dùng làm anchor — `left_x` lấy từ `anchor_mob.get_left()[0]`
        và cursor ban đầu nằm ngay dưới `anchor_mob`.
    left_x : float | None
        Ghi đè `left_x` thủ công (nếu None → tự lấy từ anchor_mob).
    initial_gap : float
        Khoảng cách từ bottom của anchor_mob xuống dòng đầu tiên.
    line_gap : float
        Khoảng cách giữa bottom ProofLine và cursor mới (gap sau mỗi ProofLine).
    note_gap : float
        Khoảng cách từ bottom note lên cursor tiếp theo (thường lớn hơn line_gap).
    """

    def __init__(
        self,
        scene,
        anchor_mob,
        left_x: float | None = None,
        initial_gap: float = 0.4,
        line_gap: float = 0.05,
        note_gap: float = 0.25,
    ):
        self._scene = scene
        self._left_x: float = (
            left_x if left_x is not None else anchor_mob.get_left()[0]
        )
        self._line_gap = line_gap
        self._note_gap = note_gap

        self._cursor = np.array([
            self._left_x,
            anchor_mob.get_bottom()[1] - initial_gap,
            0,
        ])

        self.proof: VGroup = VGroup()

    # ------------------------------------------------------------------
    # Public properties
    # ------------------------------------------------------------------

    @property
    def cursor(self) -> np.ndarray:
        """Cursor hiện tại (bottom-left của phần tử vừa thêm vào).

        Luôn là `[left_x, y, 0]` — không bị drift sang phải.
        """
        return self._cursor.copy()

    @property
    def left_x(self) -> float:
        """Giá trị x cố định của cạnh trái cột."""
        return self._left_x

    # ------------------------------------------------------------------
    # Core placement methods
    # ------------------------------------------------------------------

    def place_line(self, pf_mob, extra_buff: float = 0.0) -> "ProofColumn":
        """Đặt ProofLine tại cursor, thêm vào proof và scene, cập nhật cursor.

        Sau khi gọi `place_line`, caller dùng `pf_mob.write(...)` bên trong
        voiceover block để animate từng token.

        Parameters
        ----------
        pf_mob : ProofLine
            ProofLine đã tạo, chưa được placed.
        extra_buff : float
            Thêm khoảng trắng xuống dưới sau dòng này (cộng vào `line_gap`).

        Returns
        -------
        self — để chain nếu muốn.
        """
        pf_mob.place_below(self._cursor)
        self._scene.add(pf_mob)
        self.proof.add(pf_mob)
        self._cursor = np.array([
            self._left_x,
            pf_mob.get_bottom()[1] - self._line_gap - extra_buff,
            0,
        ])
        return self

    def place_note(self, tex_mob, extra_buff: float = 0.0) -> "ProofColumn":
        """Đặt Tex note tại cursor, thêm vào proof, cập nhật cursor.

        Method chỉ position và track — **không** animate. Caller tự gọi
        `self.play(Write(tex_mob))` sau đó.

        Parameters
        ----------
        tex_mob : Tex | MathTex
            Note đã tạo, chưa được positioned.
        extra_buff : float
            Thêm khoảng trắng xuống dưới sau note này.

        Returns
        -------
        self — để chain nếu muốn.
        """
        tex_mob.next_to(self._cursor, DOWN, aligned_edge=LEFT, buff=0.18)
        self.proof.add(tex_mob)
        self._cursor = np.array([
            self._left_x,
            tex_mob.get_bottom()[1] - self._note_gap - extra_buff,
            0,
        ])
        return self

    # ------------------------------------------------------------------
    # Utility
    # ------------------------------------------------------------------

    def skip_gap(self, gap: float = 0.3) -> "ProofColumn":
        """Dịch cursor xuống `gap` mà không add mobject nào."""
        self._cursor = np.array([self._left_x, self._cursor[1] - gap, 0])
        return self

    def at_limit(self, max_y: float = -3.2) -> bool:
        """True nếu cursor đã xuống gần mép dưới màn hình (y < max_y).

        Dùng để kiểm tra có cần tách scene hay không (≤ 12 dòng font 26).
        """
        return bool(self._cursor[1] < max_y)

    def get_proof(self) -> VGroup:
        """Trả về `self.proof` VGroup để FadeOut cuối scene."""
        return self.proof


__all__ = ["ProofColumn"]
