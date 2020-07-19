CREATE TABLE positions (
    fen VARCHAR(90),
    bitboard_all BIGINT NOT NULL,
    bitboard_white BIGINT NOT NULL,
    bitboard_black BIGINT NOT NULL,
    bitboard_white_pawn BIGINT NOT NULL,
    bitboard_black_pawn BIGINT NOT NULL,
    bitboard_white_rook BIGINT NOT NULL,
    bitboard_black_rook BIGINT NOT NULL,
    bitboard_white_knight BIGINT NOT NULL,
    bitboard_black_knight BIGINT NOT NULL,
    bitboard_white_bishop BIGINT NOT NULL,
    bitboard_black_bishop BIGINT NOT NULL,
    bitboard_white_queen BIGINT NOT NULL,
    bitboard_black_queen BIGINT NOT NULL,
    bitboard_white_king BIGINT NOT NULL,
    bitboard_black_king BIGINT NOT NULL,
    PRIMARY KEY (fen)
);

CREATE INDEX position_bitboard_idx ON positions (bitboard_all);
CREATE INDEX position_bitboard_white_idx ON positions (bitboard_white);
CREATE INDEX position_bitboard_black_idx ON positions (bitboard_black);
CREATE INDEX position_bitboard_white_pawn_idx ON positions (bitboard_white_pawn);
CREATE INDEX position_bitboard_black_pawn_idx ON positions (bitboard_black_pawn);
CREATE INDEX position_bitboard_white_rook_idx ON positions (bitboard_white_rook);
CREATE INDEX position_bitboard_black_rook_idx ON positions (bitboard_black_rook);
CREATE INDEX position_bitboard_white_bishop_idx ON positions (bitboard_white_bishop);
CREATE INDEX position_bitboard_black_bishop_idx ON positions (bitboard_black_bishop);
CREATE INDEX position_bitboard_white_queen_idx ON positions (bitboard_white_queen);
CREATE INDEX position_bitboard_black_queen_idx ON positions (bitboard_black_queen);
CREATE INDEX position_bitboard_white_king_idx ON positions (bitboard_white_king);
CREATE INDEX position_bitboard_black_king_idx ON positions (bitboard_black_king);
