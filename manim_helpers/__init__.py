"""manim_helpers - Package shared utilities cho mọi video Manim toán học.

Re-export toàn bộ public API của các submodule để mọi scene chỉ cần:

    from manim_helpers import *

Module:
    visual_tokens   : COLOR_*, STATE_*, TIMING_*, LAYER_*, MOTION_*, EMPHASIS_*, naming helpers
    proof_line      : ProofLine (semantic-token MathTex wrapper)
    sync_helpers    : sync_point / sync_segment / sync_angle / sync_right_angle /
                      sync_triangle / sync_quadrilateral / sync_relation
    geo_engine      : line_intersection, AngleMarker, right_angle_square_fill_polygon, GeometryEngine
    layout_helpers  : ProofColumn (cursor-aware proof column manager)
    theory_helpers  : TheoryColumn, make_lesson_title, place_figure, place_dual_figures (video lý thuyết)
"""

from .visual_tokens import *  # noqa: F401,F403
from .proof_line import ProofLine  # noqa: F401
from .sync_helpers import (  # noqa: F401
    sync_point,
    sync_segment,
    sync_angle,
    sync_right_angle,
    sync_triangle,
    sync_quadrilateral,
    sync_relation,
)
from .geo_engine import (  # noqa: F401
    line_intersection,
    angle_between_vectors,
    cross2d,
    AngleMarker,
    right_angle_square_fill_polygon,
    GeometryEngine,
)
from .layout_helpers import ProofColumn  # noqa: F401
from .theory_helpers import (  # noqa: F401
    TheoryColumn,
    make_lesson_title,
    place_figure,
    place_dual_figures,
    TEXT_LEFT_X, TEXT_RIGHT_WITH_FIG, TEXT_RIGHT_NO_FIG,
    FIG_CENTER_X, FIG_CENTER_Y, FIG_MAX_W, FIG_MAX_H,
    DUAL_FIG_MAX_W, DUAL_FIG_BUFF,
)

from .voiceover_config import (  # noqa: F401
    VOICEOVER_GLOBAL_SPEED,
    make_gtts_service,
)
