import streamlit as st
import random

# Page config
st.set_page_config(page_title="Tic Tac Toe", page_icon="🎮", layout="centered")

# -------- Session Initialization --------
if "page" not in st.session_state:
    st.session_state.page = "home"
if "board" not in st.session_state:
    st.session_state.board = [""] * 9
if "current_player" not in st.session_state:
    st.session_state.current_player = "X"
if "mode" not in st.session_state:
    st.session_state.mode = ""
if "winner" not in st.session_state:
    st.session_state.winner = None
if "game_over" not in st.session_state:
    st.session_state.game_over = False

# -------- Helper Functions --------
def check_winner(board):
    win_conditions = [
        [0, 1, 2], [3, 4, 5], [6, 7, 8],  # Rows
        [0, 3, 6], [1, 4, 7], [2, 5, 8],  # Columns
        [0, 4, 8], [2, 4, 6]              # Diagonals
    ]
    for cond in win_conditions:
        if board[cond[0]] == board[cond[1]] == board[cond[2]] != "":
            return board[cond[0]]
    if "" not in board:
        return "Draw"
    return None

def restart_game():
    st.session_state.board = [""] * 9
    st.session_state.current_player = "X"
    st.session_state.winner = None
    st.session_state.game_over = False

def computer_move():
    board = st.session_state.board

    # Try to win if possible
    for i in range(9):
        if board[i] == "":
            board[i] = "O"
            if check_winner(board) == "O":
                return
            board[i] = ""

    # Block player if they are about to win
    for i in range(9):
        if board[i] == "":
            board[i] = "X"
            if check_winner(board) == "X":
                board[i] = "O"
                return
            board[i] = ""

    # Otherwise pick a random move
    empty_indices = [i for i, val in enumerate(board) if val == ""]
    if empty_indices:
        move = random.choice(empty_indices)
        board[move] = "O"

def handle_click(index):
    if st.session_state.board[index] == "" and not st.session_state.game_over:
        st.session_state.board[index] = st.session_state.current_player
        winner = check_winner(st.session_state.board)
        if winner:
            st.session_state.winner = winner
            st.session_state.game_over = True
            return
        if st.session_state.mode == "Player vs Computer":
            computer_move()
            winner = check_winner(st.session_state.board)
            if winner:
                st.session_state.winner = winner
                st.session_state.game_over = True
                return
        else:
            st.session_state.current_player = "O" if st.session_state.current_player == "X" else "X"

# -------- UI --------

def home_page():
    st.title("🎮 Tic Tac Toe")

    st.subheader("Choose Game Mode:")
    if st.button("👨‍👩‍👧‍👦 Player vs Player"):
        st.session_state.mode = "Player vs Player"
        st.session_state.page = "game"
        restart_game()
    if st.button("🧠 Player vs Computer"):
        st.session_state.mode = "Player vs Computer"
        st.session_state.page = "game"
        restart_game()

def game_page():
    st.title("🎮 Tic Tac Toe")
    st.markdown(f"**Mode:** {st.session_state.mode}")
    st.markdown(f"**Current Turn:** {'🧑' if st.session_state.current_player == 'X' else '🤖'} Player {st.session_state.current_player}")

    # 3x3 Grid Layout
    cols = st.columns(3)
    for i in range(3):
        for j in range(3):
            idx = i * 3 + j
            with cols[j]:
                if st.session_state.board[idx] == "":
                    if st.button(" ", key=idx, use_container_width=True):
                        handle_click(idx)
                else:
                    st.button(st.session_state.board[idx], key=idx, use_container_width=True, disabled=True)

    # Game Result
    if st.session_state.winner:
        if st.session_state.winner == "Draw":
            st.success("It's a Draw!")
        else:
            emoji = "🧑" if st.session_state.winner == "X" else "🤖"
            st.success(f"{emoji} Player {st.session_state.winner} wins!")

    # Controls
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🔁 Restart Game"):
            restart_game()
    with col2:
        if st.button("🏠 Go to Home"):
            st.session_state.page = "home"
            restart_game()

# -------- Main --------
if st.session_state.page == "home":
    home_page()
else:
    game_page()
