from typing import List, Optional

import pydantic

from chessdb_api.domain import base_schemas


class _Base(pydantic.BaseModel):
    fen: pydantic.constr(max_length=90)
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


class Create(_Base):
    pass


class Update(_Base):
    pass


class DB(_Base):

    class Config:
        orm_mode = True


class Paginated(pydantic.BaseModel):
    results: List[DB]
    pagination: base_schemas.Pagination
