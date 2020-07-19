from chessdb_api.core.db import DB


class Model(DB.Model):
    """Model.
    """

    __tablename__ = "positions"

    fen = DB.Column(DB.String(90), primary_key=True, nullable=False)
    bitboard_all = DB.Column(DB.BigInteger, nullable=False)
    bitboard_white = DB.Column(DB.BigInteger, nullable=False)
    bitboard_black = DB.Column(DB.BigInteger, nullable=False)
    bitboard_white_pawn = DB.Column(DB.BigInteger, nullable=False)
    bitboard_black_pawn = DB.Column(DB.BigInteger, nullable=False)
    bitboard_white_rook = DB.Column(DB.BigInteger, nullable=False)
    bitboard_black_rook = DB.Column(DB.BigInteger, nullable=False)
    bitboard_white_knight = DB.Column(DB.BigInteger, nullable=False)
    bitboard_black_knight = DB.Column(DB.BigInteger, nullable=False)
    bitboard_white_bishop = DB.Column(DB.BigInteger, nullable=False)
    bitboard_black_bishop = DB.Column(DB.BigInteger, nullable=False)
    bitboard_white_queen = DB.Column(DB.BigInteger, nullable=False)
    bitboard_black_queen = DB.Column(DB.BigInteger, nullable=False)
    bitboard_white_king = DB.Column(DB.BigInteger, nullable=False)
    bitboard_black_king = DB.Column(DB.BigInteger, nullable=False)
