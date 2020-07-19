"""Example Google style docstrings.

"""
from typing import List

from chessdb_api.domain import base_schemas
import pydantic


class _Base(pydantic.BaseModel):
    """_Base.
    """

    fen: pydantic.constr(max_length=90)


class Create(_Base):
    """Create.
    """

    pass


class Update(_Base):
    """Update.
    """

    pass


class DB(_Base):
    """DB.
    """

    bitboard_all: int
    bitboard_white: int
    bitboard_black: int
    bitboard_white_pawn: int
    bitboard_black_pawn: int
    bitboard_white_rook: int
    bitboard_black_rook: int
    bitboard_white_knight: int
    bitboard_black_knight: int
    bitboard_white_bishop: int
    bitboard_black_bishop: int
    bitboard_white_queen: int
    bitboard_black_queen: int
    bitboard_white_king: int
    bitboard_black_king: int

    class Config:
        """Config.
        """

        orm_mode = True


class Paginated(pydantic.BaseModel):
    """Paginated.
    """

    results: List[DB]
    pagination: base_schemas.Pagination
