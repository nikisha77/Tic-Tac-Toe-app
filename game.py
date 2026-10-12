"""Pure tic-tac-toe rules and an unbeatable minimax bot."""

from __future__ import annotations

from typing import List, Optional, Sequence, Tuple


Board = Sequence[Optional[str]]
WINNING_LINES: Tuple[Tuple[int, int, int], ...] = (
    (0, 1, 2),
    (3, 4, 5),
    (6, 7, 8),
    (0, 3, 6),
    (1, 4, 7),
    (2, 5, 8),
    (0, 4, 8),
    (2, 4, 6),
)


def winning_line(board: Board) -> Optional[Tuple[int, int, int]]:
    """Return the winning cells, or ``None`` when nobody has won."""
    for line in WINNING_LINES:
        first, second, third = line
        if board[first] and board[first] == board[second] == board[third]:
            return line
    return None


def winner(board: Board) -> Optional[str]:
    """Return ``X`` or ``O`` for a winning board."""
    line = winning_line(board)
    return board[line[0]] if line else None


def is_draw(board: Board) -> bool:
    """Return whether the board is full without a winner."""
    return winner(board) is None and all(cell is not None for cell in board)


def available_moves(board: Board) -> List[int]:
    return [index for index, cell in enumerate(board) if cell is None]


def best_move(board: Board, bot_mark: str) -> int:
    """Choose an optimal move for ``bot_mark`` using minimax."""
    if bot_mark not in {"X", "O"}:
        raise ValueError("bot_mark must be X or O")
    if winner(board) or is_draw(board):
        raise ValueError("the game is already over")

    mutable_board = list(board)
    opponent = "O" if bot_mark == "X" else "X"

    def minimax(maximizing: bool, depth: int) -> int:
        result = winner(mutable_board)
        if result == bot_mark:
            return 10 - depth
        if result == opponent:
            return depth - 10
        if is_draw(mutable_board):
            return 0

        if maximizing:
            value = -100
            for move in available_moves(mutable_board):
                mutable_board[move] = bot_mark
                value = max(value, minimax(False, depth + 1))
                mutable_board[move] = None
            return value

        value = 100
        for move in available_moves(mutable_board):
            mutable_board[move] = opponent
            value = min(value, minimax(True, depth + 1))
            mutable_board[move] = None
        return value

    chosen_move = -1
    chosen_score = -100
    for move in available_moves(mutable_board):
        mutable_board[move] = bot_mark
        score = minimax(False, 1)
        mutable_board[move] = None
        if score > chosen_score:
            chosen_move = move
            chosen_score = score

    return chosen_move
