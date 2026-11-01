from __future__ import annotations

import random
import tkinter as tk
from tkinter import messagebox
from typing import Optional

try:
    import winsound  
except ImportError:
    winsound = None



BG = "#0B1020"
SURFACE = "#121A2B"
SURFACE_2 = "#1A263B"
SURFACE_3 = "#23334D"
BORDER = "#293A55"
TEXT = "#F3F6FC"
MUTED = "#91A0B8"
CYAN = "#4DE1F0"
CYAN_DARK = "#173C4A"
VIOLET = "#A78BFA"
VIOLET_DARK = "#30264D"
GREEN = "#48D6A0"
GREEN_DARK = "#173D35"
RED = "#FF7185"
WHITE = "#FFFFFF"

EMPTY = ""
X = "X"
O = "O"


class SoundFX:
    """Small sound effects without external audio files or dependencies."""

    def __init__(self, root: tk.Tk):
        self.root = root
        self.enabled = True

    def play(self, effect: str) -> None:
        if not self.enabled:
            return

        
        if winsound is not None:
            patterns = {
                "move": ((620, 45),),
                "undo": ((430, 55),),
                "win": ((660, 90), (880, 110), (1040, 150)),
                "lose": ((500, 100), (360, 180)),
                "draw": ((540, 90), (540, 90)),
                "click": ((720, 30),),
            }
            try:
                for frequency, duration in patterns.get(effect, patterns["click"]):
                    winsound.Beep(frequency, duration)
            except RuntimeError:
                self.root.bell()
        else:
            
            try:
                self.root.bell()
            except tk.TclError:
                pass




class Game:
    """Game state and rules. No GUI code lives in this class."""

    WIN_LINES = (
        (0, 1, 2), (3, 4, 5), (6, 7, 8),
        (0, 3, 6), (1, 4, 7), (2, 5, 8),
        (0, 4, 8), (2, 4, 6),
    )

    def __init__(self):
        self.reset()

    def reset(self):
        self.board = [EMPTY] * 9
        self.history: list[tuple[int, str]] = []
        self.turn = X
        self.winner: Optional[str] = None
        self.winning_line: Optional[tuple[int, int, int]] = None
        self.draw = False

    @classmethod
    def get_result(cls, board):
        for line in cls.WIN_LINES:
            a, b, c = line
            if board[a] and board[a] == board[b] == board[c]:
                return board[a], line
        return None, None

    def available_moves(self, board=None):
        board = self.board if board is None else board
        return [i for i, cell in enumerate(board) if cell == EMPTY]

    def play(self, index: int) -> bool:
        if not 0 <= index < 9:
            return False
        if self.winner or self.draw or self.board[index] != EMPTY:
            return False

        symbol = self.turn
        self.board[index] = symbol
        self.history.append((index, symbol))
        self.winner, self.winning_line = self.get_result(self.board)

        if self.winner is None and EMPTY not in self.board:
            self.draw = True
        elif self.winner is None:
            self.turn = O if symbol == X else X
        return True

    def undo(self, count=1) -> int:
        removed = 0
        while self.history and removed < count:
            index, symbol = self.history.pop()
            self.board[index] = EMPTY
            self.turn = symbol
            removed += 1

        self.winner, self.winning_line = self.get_result(self.board)
        self.draw = self.winner is None and EMPTY not in self.board
        return removed


# ---------------------------------- AI -------------------------------------

class ComputerPlayer:
    """Easy=random, Medium=win/block heuristics, Hard=Minimax + alpha-beta."""

    @staticmethod
    def _winning_move(board, symbol):
        for index, cell in enumerate(board):
            if cell == EMPTY:
                board[index] = symbol
                winner, _ = Game.get_result(board)
                board[index] = EMPTY
                if winner == symbol:
                    return index
        return None

    def choose_move(self, board, difficulty):
        moves = [i for i, value in enumerate(board) if value == EMPTY]
        if not moves:
            return None

        if difficulty == "Easy":
            return random.choice(moves)

        if difficulty == "Medium":
            move = self._winning_move(board, O)
            if move is not None:
                return move
            move = self._winning_move(board, X)
            if move is not None:
                return move
            if 4 in moves:
                return 4
            corners = [i for i in (0, 2, 6, 8) if i in moves]
            return random.choice(corners or moves)

        best_score = float("-inf")
        best_moves = []
        for move in moves:
            board[move] = O
            score = self._minimax(board, False, 0, float("-inf"), float("inf"))
            board[move] = EMPTY
            if score > best_score:
                best_score, best_moves = score, [move]
            elif score == best_score:
                best_moves.append(move)
        return random.choice(best_moves)

    def _minimax(self, board, maximizing, depth, alpha, beta):
        winner, _ = Game.get_result(board)
        if winner == O:
            return 10 - depth
        if winner == X:
            return depth - 10
        if EMPTY not in board:
            return 0

        if maximizing:
            best = float("-inf")
            for move in range(9):
                if board[move] == EMPTY:
                    board[move] = O
                    best = max(best, self._minimax(
                        board, False, depth + 1, alpha, beta
                    ))
                    board[move] = EMPTY
                    alpha = max(alpha, best)
                    if beta <= alpha:
                        break
            return best

        best = float("inf")
        for move in range(9):
            if board[move] == EMPTY:
                board[move] = X
                best = min(best, self._minimax(
                    board, True, depth + 1, alpha, beta
                ))
                board[move] = EMPTY
                beta = min(beta, best)
                if beta <= alpha:
                    break
        return best


# --------------------------------- GUI -------------------------------------

class TicTacToeApp:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("TicTacToe++")
        self.root.geometry("780x850")
        self.root.minsize(620, 740)
        self.root.configure(bg=BG)

        self.game = Game()
        self.ai = ComputerPlayer()
        self.sound = SoundFX(root)
        self.mode = "computer"
        self.difficulty = "Hard"
        self.scores = {X: 0, O: 0, "Draw": 0}
        self.round_over = False
        self.ai_after_id = None
        self.board_canvas = None
        self.status_var = tk.StringVar()
        self.history_var = tk.StringVar()
        self.score_vars = {}

        self.root.bind("<Key>", self.on_key)
        self.show_menu()

    # ---- shared UI helpers -------------------------------------------------

    def clear(self):
        # Drop references to widgets that are about to be destroyed.
        self.board_canvas = None
        if self.ai_after_id is not None:
            try:
                self.root.after_cancel(self.ai_after_id)
            except tk.TclError:
                pass
            self.ai_after_id = None
        for child in self.root.winfo_children():
            child.destroy()

    def label(self, parent, text="", size=11, color=TEXT, weight="normal", **kwargs):
        return tk.Label(
            parent, text=text, bg=kwargs.pop("bg", SURFACE),
            fg=color, font=("Segoe UI", size, weight), **kwargs
        )

    def button(self, parent, text, command, bg=SURFACE_3, fg=TEXT,
               size=10, **kwargs):
        return tk.Button(
            parent, text=text, command=command, bg=bg, fg=fg,
            activebackground=BORDER, activeforeground=TEXT,
            relief="flat", bd=0, cursor="hand2",
            font=("Segoe UI", size, "bold"), padx=14, pady=10,
            highlightthickness=0, **kwargs
        )

    def card(self, parent, padx=18, pady=16):
        return tk.Frame(
            parent, bg=SURFACE, padx=padx, pady=pady,
            highlightthickness=1, highlightbackground=BORDER
        )

    

    def show_menu(self):
        self.clear()
        wrap = tk.Frame(self.root, bg=BG)
        wrap.pack(fill="both", expand=True, padx=38, pady=30)

        self.label(wrap, "TICTACTOE++", 30, TEXT, "bold", bg=BG).pack(pady=(42, 4))
        self.label(
            wrap, "THINK AHEAD. PLAY SMART.", 10, CYAN, "bold", bg=BG
        ).pack(pady=(0, 8))
        self.label(
            wrap, "A classic game with a little intelligence built in.",
            11, MUTED, bg=BG
        ).pack(pady=(0, 30))

        panel = self.card(wrap, 28, 26)
        panel.pack(fill="x", padx=28)

        self.label(panel, "CHOOSE YOUR GAME", 10, MUTED, "bold").pack(anchor="w", pady=(0, 13))
        self.button(
            panel, "2 PLAYERS     ·     LOCAL MATCH",
            lambda: self.start_game("local"),
            bg=CYAN_DARK, fg=CYAN, size=12
        ).pack(fill="x", pady=6)
        self.button(
            panel, "VS COMPUTER     ·     CHALLENGE THE AI",
            lambda: self.start_game("computer"),
            bg=VIOLET_DARK, fg=VIOLET, size=12
        ).pack(fill="x", pady=6)

        self.label(panel, "COMPUTER DIFFICULTY", 10, MUTED, "bold").pack(
            anchor="w", pady=(23, 8)
        )
        self.difficulty_var = tk.StringVar(value=self.difficulty)
        row = tk.Frame(panel, bg=SURFACE)
        row.pack(fill="x")
        for level in ("Easy", "Medium", "Hard"):
            tk.Radiobutton(
                row, text=level, value=level, variable=self.difficulty_var,
                command=lambda: setattr(self, "difficulty", self.difficulty_var.get()),
                bg=SURFACE, fg=TEXT, selectcolor=SURFACE_2,
                activebackground=SURFACE, activeforeground=CYAN,
                font=("Segoe UI", 10), padx=12
            ).pack(side="left", expand=True)

        self.label(
            wrap, "HARD MODE  ·  MINIMAX + ALPHA-BETA PRUNING",
            9, MUTED, "bold", bg=BG
        ).pack(pady=20)
        self.button(wrap, "QUIT", self.root.destroy, bg=BG, fg=MUTED, size=9).pack()

    
    def start_game(self, mode):
        self.mode = mode
        self.game.reset()
        self.round_over = False
        self.build_game_screen()
        self.refresh()

    def build_game_screen(self):
        self.clear()
        outer = tk.Frame(self.root, bg=BG)
        outer.pack(fill="both", expand=True, padx=30, pady=22)

        top = tk.Frame(outer, bg=BG)
        top.pack(fill="x", pady=(0, 18))
        self.button(top, "← MENU", self.show_menu, bg=BG, fg=MUTED, size=9).pack(side="left")
        self.label(top, "TICTACTOE++", 17, TEXT, "bold", bg=BG).pack(side="right")

        scores = self.card(outer, 12, 12)
        scores.pack(fill="x", pady=(0, 14))
        score_row = tk.Frame(scores, bg=SURFACE)
        score_row.pack(fill="x")
        self.score_vars = {
            X: tk.StringVar(), "Draw": tk.StringVar(), O: tk.StringVar()
        }
        for symbol, title, color in (
            (X, "PLAYER X", CYAN), ("Draw", "DRAWS", MUTED), (O, "PLAYER O", VIOLET)
        ):
            block = tk.Frame(score_row, bg=SURFACE)
            block.pack(side="left", expand=True, fill="x")
            self.label(block, title, 8, MUTED, "bold").pack()
            self.label(
                block, textvariable=self.score_vars[symbol],
                size=21, color=color, weight="bold"
            ).pack(pady=(2, 0))

        mode_text = (
            "LOCAL 2-PLAYER MATCH" if self.mode == "local"
            else f"PLAYER VS COMPUTER  ·  {self.difficulty.upper()}"
        )
        self.label(outer, mode_text, 9, MUTED, "bold", bg=BG).pack(pady=(4, 5))
        self.label(
            outer, textvariable=self.status_var, size=16,
            color=CYAN, weight="bold", bg=BG
        ).pack(pady=(0, 13))

        board_card = self.card(outer, 12, 12)
        board_card.pack(pady=2)
        self.board_canvas = tk.Canvas(
            board_card, width=420, height=420, bg=SURFACE,
            highlightthickness=0, cursor="hand2"
        )
        self.board_canvas.pack()
        self.board_canvas.bind("<Button-1>", self.on_board_click)
        self.board_canvas.bind("<Motion>", self.on_board_motion)
        self.board_canvas.bind("<Leave>", lambda _e: self.draw_board())

        controls = tk.Frame(outer, bg=BG)
        controls.pack(fill="x", pady=(16, 10))
        self.button(controls, "UNDO  [U]", self.undo, bg=SURFACE_3).pack(
            side="left", expand=True, fill="x", padx=4
        )
        self.button(controls, "RESTART  [R]", self.restart, bg=CYAN_DARK, fg=CYAN).pack(
            side="left", expand=True, fill="x", padx=4
        )
        self.button(controls, "RESET SCORES", self.reset_scores, bg=VIOLET_DARK, fg=VIOLET).pack(
            side="left", expand=True, fill="x", padx=4
        )
        self.sound_button = self.button(
            controls, "SOUND: ON", self.toggle_sound, bg=SURFACE_3
        )
        self.sound_button.pack(side="left", expand=True, fill="x", padx=4)

        bottom = self.card(outer, 14, 10)
        bottom.pack(fill="x", pady=(7, 0))
        self.label(bottom, "MOVE HISTORY", 8, MUTED, "bold").pack(anchor="w")
        self.label(
            bottom, "", 9, TEXT,
            bg=SURFACE, justify="left", wraplength=650,
            textvariable=self.history_var
        ).pack(anchor="w", pady=(5, 0))
        self.update_scores()

    # ---- board rendering ---------------------------------------------------

    def draw_board(self, hover_index=None):
        if self.board_canvas is None:
            return
        canvas = self.board_canvas
        canvas.delete("all")
        size = 420
        cell = size / 3
        pad = 12

        # Subtle cell backgrounds and grid lines.
        for index in range(9):
            row, col = divmod(index, 3)
            x1, y1 = col * cell + pad, row * cell + pad
            x2, y2 = (col + 1) * cell - pad, (row + 1) * cell - pad
            fill = SURFACE_2 if self.game.board[index] == EMPTY else SURFACE
            if hover_index == index and not self.round_over and self.game.board[index] == EMPTY:
                fill = SURFACE_3
            canvas.create_rectangle(x1, y1, x2, y2, fill=fill, outline="")

        for i in (1, 2):
            p = i * cell
            canvas.create_line(p, 10, p, size - 10, fill=BORDER, width=3)
            canvas.create_line(10, p, size - 10, p, fill=BORDER, width=3)

        for index, symbol in enumerate(self.game.board):
            if not symbol:
                continue
            row, col = divmod(index, 3)
            cx, cy = col * cell + cell / 2, row * cell + cell / 2
            radius = 43
            color = CYAN if symbol == X else VIOLET
            if symbol == X:
                canvas.create_line(
                    cx - radius, cy - radius, cx + radius, cy + radius,
                    fill=color, width=11, capstyle=tk.ROUND
                )
                canvas.create_line(
                    cx + radius, cy - radius, cx - radius, cy + radius,
                    fill=color, width=11, capstyle=tk.ROUND
                )
            else:
                canvas.create_oval(
                    cx - radius, cy - radius, cx + radius, cy + radius,
                    outline=color, width=11
                )

        if self.game.winning_line:
            centers = []
            for index in self.game.winning_line:
                row, col = divmod(index, 3)
                centers.append((col * cell + cell / 2, row * cell + cell / 2))
            (x1, y1), (_, _), (x2, y2) = centers
            canvas.create_line(
                x1, y1, x2, y2, fill=GREEN, width=7,
                capstyle=tk.ROUND
            )

    def on_board_motion(self, event):
        index = self.position_to_index(event.x, event.y)
        self.draw_board(index)

    @staticmethod
    def position_to_index(x, y):
        if not (0 <= x < 420 and 0 <= y < 420):
            return None
        col, row = int(x // 140), int(y // 140)
        return row * 3 + col

    def on_board_click(self, event):
        index = self.position_to_index(event.x, event.y)
        if index is not None:
            self.play_at(index)

    # ---- turns and results -------------------------------------------------

    def play_at(self, index):
        if self.round_over or self.game.board[index] != EMPTY:
            return
        if self.mode == "computer" and self.game.turn != X:
            return

        self.game.play(index)
        self.sound.play("move")
        if self.game.winner or self.game.draw:
            self.finish_round()
            return

        self.refresh()
        if self.mode == "computer" and self.game.turn == O:
            self.status_var.set("COMPUTER IS THINKING...")
            self.ai_after_id = self.root.after(280, self.computer_turn)

    def computer_turn(self):
        self.ai_after_id = None
        if self.round_over or self.game.turn != O:
            return
        move = self.ai.choose_move(self.game.board, self.difficulty)
        if move is not None:
            self.game.play(move)
            self.sound.play("move")
        if self.game.winner or self.game.draw:
            self.finish_round()
        else:
            self.refresh()

    def finish_round(self):
        self.round_over = True
        if self.game.winner:
            self.scores[self.game.winner] += 1
            if self.mode == "computer":
                self.sound.play("win" if self.game.winner == X else "lose")
            else:
                self.sound.play("win")
        else:
            self.scores["Draw"] += 1
            self.sound.play("draw")
        self.refresh()
        if self.game.winner == X:
            result = "PLAYER X WINS!"
        elif self.game.winner == O:
            result = "COMPUTER WINS!" if self.mode == "computer" else "PLAYER O WINS!"
        else:
            result = "IT'S A DRAW!"
        self.status_var.set(result)

    def refresh(self):
        if self.game.winner == X:
            status = "PLAYER X WINS!"
        elif self.game.winner == O:
            status = "COMPUTER WINS!" if self.mode == "computer" else "PLAYER O WINS!"
        elif self.game.draw:
            status = "IT'S A DRAW!"
        elif self.mode == "computer":
            status = "YOUR TURN  ·  X" if self.game.turn == X else "COMPUTER'S TURN  ·  O"
        else:
            status = f"PLAYER {self.game.turn}'S TURN"
        self.status_var.set(status)

        history = [
            f"{number}. {symbol} → {index + 1}"
            for number, (index, symbol) in enumerate(self.game.history, 1)
        ]
        self.history_var.set("     ".join(history) if history else "No moves yet.")
        self.update_scores()
        self.draw_board()

    def update_scores(self):
        for key in (X, "Draw", O):
            if key in self.score_vars:
                self.score_vars[key].set(str(self.scores[key]))

    # ---- controls ----------------------------------------------------------

    def undo(self):
        if not self.game.history:
            return
        if self.ai_after_id is not None:
            self.root.after_cancel(self.ai_after_id)
            self.ai_after_id = None

        # Undo a pair in computer mode when the computer has already replied.
        count = 1
        if self.mode == "computer" and self.game.history[-1][1] == O:
            count = 2
        removed = self.game.undo(count)
        if removed:
            self.round_over = False
            self.sound.play("undo")
            self.refresh()

    def restart(self):
        if self.ai_after_id is not None:
            self.root.after_cancel(self.ai_after_id)
            self.ai_after_id = None
        self.game.reset()
        self.round_over = False
        self.sound.play("click")
        self.refresh()

    def reset_scores(self):
        self.scores = {X: 0, O: 0, "Draw": 0}
        self.restart()

    def toggle_sound(self):
        self.sound.enabled = not self.sound.enabled
        self.sound_button.config(
            text=f"SOUND: {'ON' if self.sound.enabled else 'OFF'}",
            fg=GREEN if self.sound.enabled else MUTED
        )
        if self.sound.enabled:
            self.sound.play("click")

    def on_key(self, event):
        # Shortcuts only apply while the game screen is active.
        if self.board_canvas is None:
            return
        key = event.keysym.lower()
        if key in ("u",):
            self.undo()
        elif key in ("r",):
            self.restart()
        elif key in ("1", "2", "3", "4", "5", "6", "7", "8", "9"):
            self.play_at(int(key) - 1)

    def on_close(self):
        if self.ai_after_id is not None:
            try:
                self.root.after_cancel(self.ai_after_id)
            except tk.TclError:
                pass
        self.root.destroy()


def main():
    root = tk.Tk()
    app = TicTacToeApp(root)
    root.protocol("WM_DELETE_WINDOW", app.on_close)
    root.mainloop()


if __name__ == "__main__":
    main()
