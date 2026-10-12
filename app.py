"""A polished, Python-only tic-tac-toe game built with Streamlit."""

from __future__ import annotations

import streamlit as st

from game import best_move, is_draw, winner, winning_line


st.set_page_config(
    page_title="Tic Tac Toe",
    page_icon="✦",
    layout="centered",
    initial_sidebar_state="collapsed",
)

st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;600;700&family=Space+Grotesk:wght@500;600;700&display=swap');
    :root { --ink:#17233b; --muted:#70809f; --x:#ff5d73; --o:#2962ff; --cream:#f7f4ed; }
    .stApp {
        background:
            radial-gradient(circle at 12% 4%, #ffd9de 0, transparent 25%),
            radial-gradient(circle at 92% 88%, #d8e5ff 0, transparent 28%),
            var(--cream);
        color:var(--ink);
    }
    [data-testid="stHeader"] { background:transparent; }
    .block-container { max-width:680px; padding-top:2.5rem; padding-bottom:3rem; }
    h1, h2, h3, p, label, button { font-family:'DM Sans',sans-serif !important; }
    [data-testid="stMarkdownContainer"] p,
    [data-testid="stRadio"] label,
    [data-testid="stRadio"] label p,
    [data-testid="stCaptionContainer"],
    [data-testid="stCaptionContainer"] p { color:var(--ink) !important; opacity:1 !important; }
    .brand {
        color:var(--o); font:700 .75rem 'Space Grotesk'; letter-spacing:.22em;
        text-align:center; text-transform:uppercase; margin-bottom:.8rem;
    }
    .title {
        color:var(--ink); font:700 clamp(2.7rem,9vw,5.2rem)/.95 'Space Grotesk';
        letter-spacing:-.065em; text-align:center; margin:0;
    }
    .subtitle { color:var(--muted); text-align:center; margin:.8rem 0 1.8rem; }
    .turn-card {
        background:#ffffffb8; border:1px solid #fff; border-radius:20px;
        box-shadow:0 16px 45px #39517a12; padding:1rem 1.2rem; text-align:center;
        margin:.7rem 0 1rem;
    }
    .turn-card .label { color:var(--muted); font-size:.76rem; font-weight:700; letter-spacing:.16em; text-transform:uppercase; }
    .turn-card .message { color:var(--ink); font:600 1.18rem 'Space Grotesk'; margin-top:.2rem; }
    .score-row { display:flex; gap:.65rem; justify-content:center; margin:.2rem 0 1.25rem; }
    .score-pill { background:#ffffffa8; border:1px solid #fff; border-radius:999px; color:var(--muted); padding:.45rem .85rem; font-size:.86rem; }
    .score-pill b { color:var(--ink); }
    div[data-testid="stHorizontalBlock"] { gap:.65rem; }
    .stButton > button {
        border:0; border-radius:22px; background:#fff; color:var(--ink);
        box-shadow:0 10px 28px #374e7817; font:700 clamp(2rem,8vw,3.4rem) 'Space Grotesk' !important;
        min-height:112px; transition:transform .12s ease, box-shadow .12s ease;
    }
    .stButton > button:hover:enabled { border:0; transform:translateY(-3px); box-shadow:0 15px 32px #374e7825; }
    .stButton > button:disabled { opacity:1; color:var(--ink); }
    .stButton > button[kind="primary"] { background:var(--ink); color:white; min-height:3rem; font-size:.95rem !important; border-radius:999px; }
    .stButton > button[kind="primary"] p { color:white !important; opacity:1 !important; }
    .stButton > button[kind="secondary"] { min-height:3rem; font-size:.95rem !important; border-radius:999px; }
    [data-testid="stVerticalBlockBorderWrapper"] {
        background:#fffdf8cc; border:1px solid #fff !important; border-radius:20px;
        box-shadow:0 10px 30px #39517a0d; margin-bottom:1rem;
    }
    .setup-heading { color:var(--ink); font:700 1rem 'Space Grotesk'; margin:0 0 .25rem; }
    .helper { color:var(--muted); font-size:.82rem; text-align:center; margin-top:1rem; }
    @media (max-width:520px) {
        .block-container { padding-top:1.4rem; }
        .stButton > button { min-height:88px; border-radius:18px; }
    }
    </style>
    """,
    unsafe_allow_html=True,
)


def other(mark: str) -> str:
    return "O" if mark == "X" else "X"


def player_name(mark: str) -> str:
    if st.session_state.mode == "Bot":
        return "You" if mark == st.session_state.chosen_mark else "Bot"
    return "Player 1" if mark == st.session_state.chosen_mark else "Player 2"


def finish_if_needed() -> bool:
    victor = winner(st.session_state.board)
    if victor:
        st.session_state.winner = victor
        st.session_state.winning_cells = winning_line(st.session_state.board)
        st.session_state.scores[victor] += 1
        return True
    if is_draw(st.session_state.board):
        st.session_state.winner = "Draw"
        st.session_state.scores["Draws"] += 1
        return True
    return False


def make_bot_move() -> None:
    bot_mark = other(st.session_state.chosen_mark)
    move = best_move(st.session_state.board, bot_mark)
    st.session_state.board[move] = bot_mark
    if not finish_if_needed():
        st.session_state.current_turn = st.session_state.chosen_mark


def start_round(*, reset_scores: bool = False) -> None:
    st.session_state.board = [None] * 9
    st.session_state.current_turn = "X"
    st.session_state.winner = None
    st.session_state.winning_cells = None
    if reset_scores or "scores" not in st.session_state:
        st.session_state.scores = {"X": 0, "O": 0, "Draws": 0}
    if st.session_state.mode == "Bot" and st.session_state.chosen_mark == "O":
        make_bot_move()


def play_cell(index: int) -> None:
    if st.session_state.board[index] is not None or st.session_state.winner:
        return
    st.session_state.board[index] = st.session_state.current_turn
    if finish_if_needed():
        return
    st.session_state.current_turn = other(st.session_state.current_turn)
    if st.session_state.mode == "Bot":
        make_bot_move()


st.markdown('<div class="brand">Classic game · clever opponent</div>', unsafe_allow_html=True)
st.markdown('<h1 class="title">Tic Tac Toe</h1>', unsafe_allow_html=True)
st.markdown(
    '<div class="subtitle">Pick your side, line up three, and claim the round.</div>',
    unsafe_allow_html=True,
)

with st.container(border=True):
    st.markdown('<div class="setup-heading">Game setup</div>', unsafe_allow_html=True)
    setup_left, setup_middle, setup_right = st.columns([1.25, 1.25, 1])
    with setup_left:
        mode = st.radio("Play mode", ["Bot", "Friends"], horizontal=True, key="mode_picker")
    with setup_middle:
        mark_label = "Your mark" if mode == "Bot" else "Player 1 mark"
        chosen_mark = st.radio(mark_label, ["X", "O"], horizontal=True, key="mark_picker")
    with setup_right:
        st.caption("X always goes first.")
        if st.button("Reset match", use_container_width=True):
            start_round(reset_scores=True)
            st.rerun()

    settings = (mode, chosen_mark)
    if st.session_state.get("active_settings") != settings:
        st.session_state.mode = mode
        st.session_state.chosen_mark = chosen_mark
        st.session_state.active_settings = settings
        start_round(reset_scores=True)

if st.session_state.winner == "Draw":
    message = "A perfect draw — nobody gets the square."
elif st.session_state.winner:
    victor = st.session_state.winner
    message = f"{player_name(victor)} wins with {victor}!"
else:
    turn = st.session_state.current_turn
    message = f"{player_name(turn)} to move · playing {turn}"

st.markdown(
    f'<div class="turn-card"><div class="label">Round status</div><div class="message">{message}</div></div>',
    unsafe_allow_html=True,
)
st.markdown(
    '<div class="score-row">'
    f'<div class="score-pill"><b>X</b> · {st.session_state.scores["X"]}</div>'
    f'<div class="score-pill"><b>Draws</b> · {st.session_state.scores["Draws"]}</div>'
    f'<div class="score-pill"><b>O</b> · {st.session_state.scores["O"]}</div>'
    '</div>',
    unsafe_allow_html=True,
)

for row in range(3):
    columns = st.columns(3)
    for column, index in zip(columns, range(row * 3, row * 3 + 3)):
        mark = st.session_state.board[index]
        disabled = mark is not None or st.session_state.winner is not None
        with column:
            st.button(
                mark or " ",
                key=f"cell-{index}",
                on_click=play_cell,
                args=(index,),
                disabled=disabled,
                use_container_width=True,
            )

st.write("")
left, middle, right = st.columns([1, 2, 1])
with middle:
    if st.button("Play another round", type="primary", use_container_width=True):
        start_round()
        st.rerun()

mode_hint = "The bot plays perfectly — a draw is a win in disguise." if mode == "Bot" else "Pass the device after each move."
st.markdown(f'<div class="helper">{mode_hint} Change mode or mark in the setup panel.</div>', unsafe_allow_html=True)
