import tkinter
import datetime
from tkinter import *
import tkinter.messagebox as msgbox
import tkinter.filedialog as filedialog
import tkinter as tk
from tkinter import ttk

import platform
from stockfish import Stockfish
import chess
import chess.pgn
from tkinter import filedialog, messagebox
import os

# -------------------------------------------------------------------------------------------
# Unicode for chess pieces
# white king	  ♔   U+2654
# white queen	  ♕   U+2655
# white rook	  ♖   U+2656
# white bishop    ♗   U+2657
# white knight    ♘   U+2658
# white pawn	  ♙   U+2659
# black king	  ♚   U+265A
# black queen	  ♛   U+265B
# black rook	  ♜   U+265C
# black bishop    ♝   U+265D
# black knight    ♞   U+265E
# black pawn	  ♟   U+265F

PRIMARY_BG = "#2A9D8F"  # Teal for primary elements
SECONDARY_BG = "#264653"  # Dark teal for secondary elements
TEXT_COLOR = "#FFFFFF"  # White for text
BUTTON_BG = "#E9C46A"  # Soft gold for buttons
HOVER_BG = "#F4A261"  # Darker gold for hover state
CHESSBOARD_LIGHT = "#F0D9B5"  # Light squares on the chessboard
CHESSBOARD_DARK = "#B58863"  # Dark squares on the chessboard

FONT_LARGE = ("Helvetica", 14, 'bold')
FONT_SMALL = ("Helvetica", 12)


FONT = ("Work sans", 12)
BLUE = "#277595"
YELLOW = "#E9C46A"

import tkinter as tk
from tkinter import messagebox


global username
def submit_username():
    global username
    username = entry.get()
    if username:
        root.destroy()
    else:
        messagebox.showwarning("Input Error", "Please enter a username.")

def game_over_message(message):
    messagebox.showinfo("Game Over", message)


unicode_map = {"K": "\u2654",
               "Q": "\u2655",
               "R": "\u2656",
               "B": "\u2657",
               "N": "\u2658",
               "P": "\u2659",

               "k": "\u265A",
               "q": "\u265B",
               "r": "\u265C",
               "b": "\u265D",
               "n": "\u265E",
               "p": "\u265F",

               "-": " "
               }
# ----------------------------------------------------------------------------------
# Button map
btn_map = {
    "a8": 0, "b8": 1, "c8": 2, "d8": 3, "e8": 4, "f8": 5, "g8": 6, "h8": 7,
    "a7": 8, "b7": 9, "c7": 10, "d7": 11, "e7": 12, "f7": 13, "g7": 14, "h7": 15,
    "a6": 16, "b6": 17, "c6": 18, "d6": 19, "e6": 20, "f6": 21, "g6": 22, "h6": 23,
    "a5": 24, "b5": 25, "c5": 26, "d5": 27, "e5": 28, "f5": 29, "g5": 30, "h5": 31,
    "a4": 32, "b4": 33, "c4": 34, "d4": 35, "e4": 36, "f4": 37, "g4": 38, "h4": 39,
    "a3": 40, "b3": 41, "c3": 42, "d3": 43, "e3": 44, "f3": 45, "g3": 46, "h3": 47,
    "a2": 48, "b2": 49, "c2": 50, "d2": 51, "e2": 52, "f2": 53, "g2": 54, "h2": 55,
    "a1": 56, "b1": 57, "c1": 58, "d1": 59, "e1": 60, "f1": 61, "g1": 62, "h1": 63
}
# ----------------------------------------------------------------------------------


# Save moves to PGN format

class GUI(Tk):
    def __init__(self, width, height, name):
        super().__init__()

        self.username = name
        self.title("LeChess")
        self.geometry(f"{width}x{height}")
        self.wm_resizable(width=False, height=False)
        self.usr_move = ""
        self.game_over = False
        self.moves = []

        self.bot = Stockfish(r"stockfish/stockfish_13_win_x64_bmi2.exe")
        self.moves_pgn = []  # Stores the list of moves from the PGN
        self.current_move_index = 0  # Tracks the current move

    # -------------------------------------------------------------------------------

    def save_to_pgn(self, result):
        pgn_data = []
        pgn_data.append(f'[Event "LeChess Game"]')
        pgn_data.append(f'[Site "Unknown"]')
        pgn_data.append(f'[Date "{datetime.datetime.now().strftime("%Y.%m.%d")}"]')
        pgn_data.append(f'[Round "1"]')
        pgn_data.append(f'[White "{self.username}"]')
        pgn_data.append(f'[Black "Computer"]')
        pgn_data.append(f'[Result "{result}"]\n')

        # Format moves with a newline after every 6 moves for readability
        pgn_moves = ""
        for i in range(0, len(self.moves), 2):
            move_num = (i // 2) + 1
            user_move = self.moves[i]
            computer_move = self.moves[i + 1] if i + 1 < len(self.moves) else ""
            pgn_moves += f'{move_num}. {user_move} {computer_move} '

            if (i // 2 + 1) % 3 == 0:  # Add a newline after every 3 move pairs (6 moves)
                pgn_moves += "\n"

        pgn_data.append(pgn_moves.strip())
        current_time = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")

        file_path = filedialog.asksaveasfilename(
            defaultextension=".pgn",
            filetypes=[("PGN Files", "*.pgn")],
            initialfile=f"{self.username}_{current_time}.pgn"
        )

        if file_path:
            with open(file_path, "w") as pgn_file:
                pgn_file.write("\n".join(pgn_data))
            print(f"Game saved to {file_path}")


    def on_user_move(self, move):
        self.moves.append(move)  # Append user move

    def on_computer_move(self, move):
        self.moves.append(move)  # Append computer move


    #----------------------------------------------------------------------------------

    # Menu bar
    def new_game(self):
        self.bot.set_fen_position(
            "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1")
        self.update_board()
        self.remove_marking()
        self.usr_move = ""

    def recommend_move(self):
        m = self.bot.get_best_move()
        self.b_list[btn_map[m[:2]]].configure(bg='#AFFFAF')
        self.b_list[btn_map[m[2:]]].configure(bg='#AFFFAF')

    def about(self):
        about_text = '''
        LeChess
        '''
        msgbox.showinfo('About', about_text)

    def visualize_pgn(self):
        file_path = filedialog.askopenfilename(title="Open PGN File", filetypes=[("PGN Files", "*.pgn")])
        if not file_path:
            return

        try:
            # Open and parse the PGN file
            with open(file_path) as pgn_file:
                game = chess.pgn.read_game(pgn_file)
                if game is None:
                    messagebox.showerror("Error", "Failed to read PGN file. The file might be corrupted.")
                    return
                # Create the control buttons
                self.new_game()
                white_player = game.headers.get("White", "Unknown")
                self.status.config(text=f"{white_player} vs Computer")
                self.moves_pgn = [move.uci() for move in game.mainline_moves()]
                self.current_move_index = 0
                button_frame = tk.Frame(self)
                prev_button = ttk.Button(button_frame, text="Previous", command=self.prev_move)
                prev_button.pack(side=tk.LEFT)
                next_button = ttk.Button(button_frame, text="Next", command=self.next_move)
                next_button.pack(side=tk.LEFT)
                reset_button = ttk.Button(button_frame, text="Reset", command=self.new_game)
                reset_button.pack(side=tk.LEFT)
                button_frame.pack()

        except FileNotFoundError:
            messagebox.showerror("Failed to load PGN file! Please try again.")

    def next_move(self):
        if self.current_move_index < len(self.moves_pgn):
            # Get the next move and make it on the board
            self.remove_marking()
            move = self.moves_pgn[self.current_move_index]
            print(move)
            self.bot.make_moves_from_current_position([move])  # Use Stockfish to apply the move
            self.mark_move(move)  # Highlight the move on the board
            self.update_board()  # Update the visual board
            self.current_move_index += 1  # Move to the next move

    def prev_move(self):
        if self.current_move_index > 0:
            self.remove_marking()
            self.current_move_index -= 1  # Go back one move
            self.new_game()
            self.bot.make_moves_from_current_position(
                self.moves_pgn[:self.current_move_index])  # Replay moves up to current
            self.update_board()  # Update the visual board

    def create_menu_bar(self):
        self.menu = tk.Menu(self, background="#E9C46A")
        self.menu.add_command(label='New game', command=self.new_game)
        self.menu.add_command(label='Recommend move',
                              command=self.recommend_move)
        self.menu.add_command(label='Visualize with PGN', command=self.visualize_pgn)
        self.menu.add_command(label='Close', command=self.quit)

        self.config(menu=self.menu)

    # -------------------------------------------------------------------------------
    # Status bar
    def create_status_bar(self, username):
            style = ttk.Style()
            style.configure(
                'StatusBar.TLabel',
                background=PRIMARY_BG,
                foreground=TEXT_COLOR,
                font=FONT_SMALL,
                padding=10
            )

            # Add a separator for a cleaner layout
            separator = ttk.Separator(self, orient='horizontal')
            separator.pack(side=tk.BOTTOM, fill=tk.X)

            # Create the dynamic status bar
            self.status = ttk.Label(
                self,
                text=f"{username} vs Computer | LeChess V1.0",
                style='StatusBar.TLabel',
                anchor='center'
            )
            self.status.pack(side=tk.BOTTOM, fill=tk.X)

            # Periodic update for dynamic elements like time
            self.update_status_bar()

    def update_status_bar(self):
        current_time = datetime.datetime.now().strftime("%H:%M:%S")
        self.status.config(text=f"{self.username} vs Computer | LeChess V1.0 | {current_time}")
        self.after(1000, self.update_status_bar)


    # -------------------------------------------------------------------------------
    # Chessboard

    def create_chess_board(self, font, w, h):
        self.grid_map = Frame(window, bg=BLUE, padx=1, pady=1)

        # Generate 64 button widgets
        self.b_list = []
        font = f"Helvetica {font} bold"

        for each in range(0, 64):
            self.b_list.append(Button(
                self.grid_map,
                text=' ',
                command=lambda each=each: self.on_button_click(each),
                font=font,
                width=w,
                height=h,
                relief='flat',    # Use 'flat' relief for a modern look
                borderwidth=0     # Remove borders
            ))


        # Place 64 button widgets in a 8x8 grid
        each = 0
        for r in range(0, 8):
            for c in range(0, 8):
                self.b_list[each].grid(row=r, column=c)

                if r % 2 != 0:
                    if each % 2 == 0:
                        self.b_list[each].configure(bg='#B58863')
                else:
                    if each % 2 != 0:
                        self.b_list[each].configure(bg='#F0D9B5')
                each = each + 1

        self.grid_map.pack(side=BOTTOM)
        self.update_board()



    def game_over_message(self, message):
        messagebox.showinfo("Game Over", f"🏁 {message} 🏁\nThank you for playing, {self.username}!")


    # -------------------------------------------------------------------------------
    # Chessboard helper functions
    def mark_move(self, move):
        m = str(move)

        # Check if it's a promotion (which will have 5 characters, like 'c7c8q')
        if len(m) == 5:
            # Handle promotion moves (e.g., 'c7c8q' should be treated as 'c7c8')
            move_start = m[:2]
            move_end = m[2:4]
        else:
            move_start = m[:2]
            move_end = m[2:]

        self.b_list[btn_map[move_start]].configure(bg='#AFAFFF')
        self.b_list[btn_map[move_end]].configure(bg='#AFAFFF')


    def remove_marking(self):
        each = 0
        for r in range(0, 8):
            for c in range(0, 8):
                self.b_list[each].configure(bg='#F0F0F0')

                if r % 2 != 0:
                    if each % 2 == 0:
                        self.b_list[each].configure(bg='#B58863')
                else:
                    if each % 2 != 0:
                        self.b_list[each].configure(bg='#F0D9B5')
                each = each + 1

    def position_has_white_piece(self, position):
        board_state = ""

        fen = self.bot.get_fen_position()
        for x in str(fen).split(" ")[0]:
            if x.isnumeric():
                for n in range(0, int(x)):
                    board_state += "-"
            else:
                if x != "/":
                    board_state += x

        if len(position) == 2:
            if board_state[btn_map[position]] in ['K', 'Q', 'R', 'B', 'N', 'P']:
                return True
            else:
                return False

    def check_endgame_conditions(self):
        fen = self.bot.get_fen_position()
        board = chess.Board(fen)

        c = None
        if board.is_check():
            c = "Check"
        if board.is_checkmate():
            c = "Checkmate"

        return c

    def on_button_click(self, button):
        self.remove_marking()
        self.status.configure(text="")

        if self.game_over == False:
            # Get row
            if button >= 0 and button <= 31:
                if button >= 0 and button <= 7:
                    r = 8
                if button >= 8 and button <= 15:
                    r = 7
                if button >= 16 and button <= 23:
                    r = 6
                if button >= 24 and button <= 31:
                    r = 5
            else:
                if button >= 32 and button <= 39:
                    r = 4
                if button >= 40 and button <= 47:
                    r = 3
                if button >= 48 and button <= 55:
                    r = 2
                if button >= 56 and button <= 63:
                    r = 1

            # Get column
            c = chr(97 + button % 8)

            if len(self.usr_move) == 2:
                self.remove_marking()
                self.usr_move += c + str(r)
                print(f"User's move: {self.usr_move}")

                if self.position_has_white_piece(self.usr_move[:2]) and self.position_has_white_piece(self.usr_move[2:]):
                    self.usr_move = self.usr_move[2:]
                    self.remove_marking()
                    self.b_list[btn_map[self.usr_move]].configure(bg='#FFFFAF')
                    return

                if self.bot.is_move_correct(self.usr_move):
                    self.bot.make_moves_from_current_position([self.usr_move])
                    self.on_user_move(self.usr_move)
                    self.usr_move = ""
                else:
                    self.status.config(text="Invalid move")
                    self.usr_move = ""
                    return

                self.update_board()

                # End game condition check
                c = self.check_endgame_conditions()
                if c == 'Check':
                    self.status.config(text=c)
                elif c == 'Checkmate':
                    self.game_over = True
                    self.status.config(text=c)
                    print("User wins")
                    game_over_message(f"You win, {username} 🥳")
                    self.save_to_pgn("1-0")
                    return

                # Computers turn
                best_move = self.bot.get_best_move()
                self.on_computer_move(best_move)
                print(f"Computer's move: {best_move}\n")

                self.bot.make_moves_from_current_position([best_move])
                self.mark_move(best_move)
                self.update_board()

                # End game condition check
                c = self.check_endgame_conditions()
                if c == 'Check':
                    self.status.config(text=c)
                elif c == 'Checkmate':
                    self.game_over = True
                    self.status.config(text=c)
                    print("User lose")
                    game_over_message(f"You lost, {username} 🥹")
                    self.save_to_pgn("0-1")
                    return

            else:
                self.usr_move += c + str(r)

                if(self.position_has_white_piece(self.usr_move)):
                    self.b_list[btn_map[self.usr_move]].configure(bg='#FFFFAF')
                else:
                    self.usr_move = ""

    def update_board(self):
        board_state = ""
        fen = self.bot.get_fen_position()

        # print(fen)
        for x in str(fen).split(" ")[0]:
            if x.isnumeric():
                for n in range(0, int(x)):
                    board_state += "-"
            else:
                if x != "/":
                    board_state += x

        # print(board_state)

        for i in range(64):
            self.b_list[i].configure(text=unicode_map[board_state[i]])


# -------------------------------------------------------------------------------------------
if __name__ == '__main__':
    print("Welcome to LeChess! Minimize this window for better experience!")
    os_name = platform.system().lower()
    # Create the main window
    root = tk.Tk()
    root.title("Username Input")
    root.configure(bg="#ffffff")
    root.geometry("400x200")

    style = ttk.Style()
    style.configure('TButton', font=("Work sans", 12))

    # Create and place the label
    # Create and place the label
    label = ttk.Label(root, text="Enter your username:", font=FONT, background="#ffffff")
    label.pack(pady=20)

    # Create and place the entry field
    entry = ttk.Entry(root, width=30, font=('Work sans', 12))
    entry.pack(pady=5)

    # Create and place the submit button
    submit_button = ttk.Button(
        root,
        text="Submit",
        command=submit_username
    )
    submit_button.pack(pady=20)
    # Bind the Enter key to the submit function
    root.bind('<Return>', lambda event: submit_username())

    root.mainloop()

    if 'windows' in os_name:
        window = GUI(740, 680, name=username)
    else:
        window = GUI(700, 680, name=username)

    window.create_menu_bar()
    window.create_status_bar(username=username)

    if 'windows' in os_name:
        window.create_chess_board(18, 5, 2)
    else:
        window.create_chess_board(18, 4, 2)

    window.mainloop()

# -------------------------------------------------------------------------------------------
