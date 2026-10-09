r"""ProofLine – wrapper trên MathTex hỗ trợ semantic token cho dòng chứng minh.

Mỗi dòng chứng minh gồm nhiều "thực thể" (đoạn / góc / tam giác / quan hệ).
Thay vì index ``pf[0], pf[1], pf[2]`` mong manh khi đổi LaTeX, dùng tên semantic::

    pf5 = ProofLine(
        ("tri_OFB", r"\triangle OFB"),
        ("eq1",     "="),
        ("tri_OFC", r"\triangle OFC"),
        ("cgc",     r"\;(\text{c.g.c})"),
        ("seg_BF",  r";\quad BF"),
        ("seg_eq",  "="),
        ("seg_FC",  r"FC"),
        tex_template=viet_tex_template,
        font_size=26,
    )
    pf5.place_below(cursor)

    # Trong voiceover block:
    self.play(pf5.write("tri_OFB"))      # chỉ Write 1 token
    self.play(pf5.write("eq1", "tri_OFC"))  # Write nhiều token cùng lúc

``pf5.get(token_id)`` trả về Mobject của token (đã nằm trong VGroup), tiện cho
TransformFromCopy / Indicate / Circumscribe vào riêng token đó.
"""

from __future__ import annotations

from typing import Iterable, Tuple, Union

from manim import MathTex, VGroup, AddTextLetterByLetter, AnimationGroup, LEFT, DOWN
import numpy as np


TokenSpec = Tuple[str, str]  # (id, latex_string)


class ProofLine(VGroup):
    """Một dòng chứng minh = MathTex được wrap để truy cập theo tên semantic.

    Tham số:
        *tokens: chuỗi (id, latex_string). id phải duy nhất trong cùng ProofLine.
        font_size: cỡ chữ (mặc định 26 — chuẩn cho proof body).
        tex_template: viet_tex_template nếu có ký tự tiếng Việt.
        **kwargs: forward sang MathTex (color, ...).
    """

    def __init__(
        self,
        *tokens: TokenSpec,
        font_size: float = 26,
        tex_template=None,
        **kwargs,
    ):
        super().__init__()
        if not tokens:
            raise ValueError("ProofLine cần ít nhất 1 token.")
        ids = [t[0] for t in tokens]
        if len(set(ids)) != len(ids):
            raise ValueError(f"Token ids trùng nhau trong ProofLine: {ids}")

        latex_parts = [t[1] for t in tokens]
        mt_kwargs = dict(kwargs)
        if tex_template is not None:
            mt_kwargs["tex_template"] = tex_template
        self._mathtex = MathTex(*latex_parts, font_size=font_size, **mt_kwargs)

        self._index = {tid: i for i, tid in enumerate(ids)}
        self._token_ids = list(ids)
        self.add(self._mathtex)
        for sub in self._mathtex:
            sub.set_opacity(0)

    @property
    def token_ids(self):
        return list(self._token_ids)

    def get(self, token_id: str):
        """Trả về submobject (đoạn LaTeX) ứng với token_id."""
        if token_id not in self._index:
            raise KeyError(
                f"Token {token_id!r} không có trong ProofLine. "
                f"Token hiện có: {self._token_ids}"
            )
        return self._mathtex[self._index[token_id]]

    def __getitem__(self, key):
        if isinstance(key, str):
            return self.get(key)
        return super().__getitem__(key)

    def write(self, *token_ids: str, run_time=None) -> AnimationGroup:
        """Trả về Animation AddTextLetterByLetter 1+ token theo tên semantic.

        Dùng trực tiếp trong scene.play(...) hoặc truyền vào sync_*().
        """
        if not token_ids:
            raise ValueError("write() cần ít nhất 1 token id.")
        anims = []
        for tid in token_ids:
            tok = self.get(tid)
            tok.set_opacity(1)
            anims.append(AddTextLetterByLetter(tok))
        if len(anims) == 1:
            anim = anims[0]
        else:
            anim = AnimationGroup(*anims, lag_ratio=0.0)
        if run_time is not None:
            anim.run_time = run_time
        return anim

    def write_all(self, run_time=None) -> AnimationGroup:
        """Write toàn bộ token theo thứ tự."""
        return self.write(*self._token_ids, run_time=run_time)

    def place_below(self, anchor, buff: float = 0.18, aligned_edge=LEFT):
        """Đặt ProofLine bên dưới anchor (Mobject hoặc np.ndarray cursor).

        Trả về self để chain.
        """
        if isinstance(anchor, np.ndarray):
            self._mathtex.next_to(anchor, DOWN, aligned_edge=aligned_edge, buff=buff)
        else:
            self._mathtex.next_to(anchor, DOWN, aligned_edge=aligned_edge, buff=buff)
        return self

    def get_bottom_left_cursor(self) -> np.ndarray:
        """Trả về vị trí (left_x, bottom_y) để dùng làm cursor cho dòng tiếp theo."""
        left_x = self._mathtex.get_left()[0]
        bottom_y = self._mathtex.get_bottom()[1]
        return np.array([left_x, bottom_y, 0.0])
