"""
Shared configuration for manim-voiceover (GTTS).

Goal: adjust global speaking speed in a single place.

On Windows, manim-voiceover uses SoX (CLI) to change tempo when global_speed != 1.
If `sox` / `soxi` are missing from PATH, we fall back to ffmpeg (already common in Manim setups).
"""

from __future__ import annotations

import shutil
import subprocess
import uuid
from pathlib import Path
from typing import Any

# 1.0 = normal speed; 1.25 ~= 25% faster (shorter voiceover duration).
VOICEOVER_GLOBAL_SPEED: float = 1.25

_speed_backend_patched = False


def _sox_cli_available() -> bool:
    return shutil.which("sox") is not None and shutil.which("soxi") is not None


def _atempo_filter_chain(tempo: float) -> str:
    """Build ffmpeg atempo chain (each stage must stay within 0.5–2.0)."""
    filters: list[str] = []
    t = tempo
    while t > 2.0:
        filters.append("atempo=2.0")
        t /= 2.0
    while t < 0.5:
        filters.append("atempo=0.5")
        t /= 0.5
    filters.append(f"atempo={t:.6f}".rstrip("0").rstrip("."))
    return ",".join(filters)


def _adjust_speed_ffmpeg(input_path: str, output_path: str, tempo: float) -> None:
    ffmpeg = shutil.which("ffmpeg")
    if ffmpeg is None:
        raise RuntimeError(
            "Neither SoX nor ffmpeg is available. Install SoX (sox.exe + soxi.exe on PATH) "
            "or ffmpeg, or set VOICEOVER_GLOBAL_SPEED=1.0."
        )

    same_destination = input_path == output_path
    if same_destination:
        path_, ext = Path(input_path).stem, Path(input_path).suffix
        output_path = str(Path(input_path).with_name(f"{path_}{uuid.uuid1()}{ext}"))

    subprocess.run(
        [
            ffmpeg,
            "-y",
            "-hide_banner",
            "-loglevel",
            "error",
            "-i",
            input_path,
            "-filter:a",
            _atempo_filter_chain(tempo),
            "-vn",
            output_path,
        ],
        check=True,
    )

    if same_destination:
        Path(output_path).replace(input_path)


def _ensure_speed_adjustment_backend() -> None:
    global _speed_backend_patched
    if _speed_backend_patched:
        return

    if _sox_cli_available():
        _speed_backend_patched = True
        return

    import manim_voiceover.modify_audio as modify_audio

    modify_audio.adjust_speed = _adjust_speed_ffmpeg

    # base.py dùng `from ... import adjust_speed` nên giữ tham chiếu riêng;
    # phải patch trực tiếp vào namespace của module đó.
    try:
        import manim_voiceover.services.base as _base_module
        _base_module.adjust_speed = _adjust_speed_ffmpeg
    except (ImportError, AttributeError):
        pass

    _speed_backend_patched = True

    try:
        from manim import logger

        logger.warning(
            "SoX CLI (sox/soxi) not found on PATH. "
            "Using ffmpeg for voiceover global_speed instead. "
            "Install SoX for the default manim-voiceover backend."
        )
    except ImportError:
        pass


def make_gtts_service(
    lang: str = "vi",
    transcription_model: str = "base",
    **kwargs: Any,
):
    """
    Factory for manim_voiceover.services.gtts.GTTSService.

    Uses VOICEOVER_GLOBAL_SPEED by default; caller can override via global_speed=...
    in kwargs.
    """
    _ensure_speed_adjustment_backend()

    from manim_voiceover.services.gtts import GTTSService

    global_speed = kwargs.pop("global_speed", VOICEOVER_GLOBAL_SPEED)
    return GTTSService(
        lang=lang,
        transcription_model=transcription_model,
        global_speed=global_speed,
        **kwargs,
    )
