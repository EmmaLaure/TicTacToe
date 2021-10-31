from tkinter import *
from tkinter import messagebox


class App:
    def __init__(self):
        self.gamestate = GameState()
        self.window = Window(self.gamestate)

    def start_game(self):
        self.window.mainloop()


class Window(Tk):
    def __init__(self, gamestate):
        super().__init__()
        menubar = Menu(self)
        menubar.add_command(label="Restart Game", command=self.reset_game)
        player_menu = Menu(menubar, tearoff=0)
        player_menu.add_command(label="3x3", command=lambda: self.set_boardsize(3))
        player_menu.add_command(label="4x4", command=lambda: self.set_boardsize(4))
        player_menu.add_command(label="5x5", command=lambda: self.set_boardsize(5))
        menubar.add_cascade(label="Board Size", menu=player_menu)
        self.config(menu=menubar)
        # size_board = self.determine_boardsize()
        self.gamestate = gamestate
        self.buttons = []
        self.create_buttons()
        self.title = "TicTacToe"

    def set_boardsize(self, size):
        self.gamestate.boardsize = size
        self.reset_game()

    def set_btn_text(self, x, y, text):
        self.buttons[y*self.gamestate.boardsize + x]['text'] = text

    def handle_click(self, button):
        player_turn = self.gamestate.turn
        self.gamestate.move(button.x, button.y, btn_callback=self.set_btn_text)

    def reset_game(self):
        if self.gamestate.boardsize**2 != len(self.buttons):
            for b in self.buttons:
                b.destroy()
            self.buttons.clear()
            self.create_buttons()
        self.gamestate.reset_game(self.set_btn_text)

    def create_buttons(self):
        # create board size * board size number of buttons
        for idx in range(self.gamestate.boardsize**2):
            x_coord = idx % self.gamestate.boardsize
            y_coord = int(idx/self.gamestate.boardsize)
            self.buttons.append(Button_xy(self, text=" ", font="Helvetica", height=5, width=9,
                                          bg="SystemButtonFace", x=x_coord, y=y_coord))
            self.buttons[idx].grid(row=x_coord, column=y_coord)
        for idx, b in enumerate(self.buttons):
            b.config(command=lambda current_button=b: self.handle_click(current_button))


class Button_xy(Button):
    def __init__(self, window, text, font, height, width, bg, x, y):
        super().__init__(window, text=text, font=font, height=height, width=width, bg=bg)
        self.x = x
        self.y = y


class GameState:
    def __init__(self):
        self.boardsize = 3
        self.board = Board(self.boardsize)
        self.players = [Player("X", 0), Player("O", 1)]
        self.turn = 0

    def tokens(self):
        return [p.token for p in self.players]

    def reset_game(self, btn_callback):
        self.board = Board(self.boardsize)
        self.turn = 0
        for x in range(self.boardsize):
            for y in range(self.boardsize):
                btn_callback(x, y, " ")

    def is_win(self):
        # ROW WIN
        for t in self.tokens():
            for row in self.board.board:
                if all(row[x] == t for x in range(self.boardsize)):
                    # print(f"~~~~~~~~ Player {t} has won! ~~~~~~~~")
                    return True

        # COLUMN WIN
        for t in self.tokens():
            for x in range(self.boardsize-1):
                if all(row[x] == t for row in self.board.board):
                    # print(f"~~~~~~~~ Player {t} has won! ~~~~~~~~")
                    return True

        # DIAGONAL WIN
        for t in self.tokens():
            if all(self.board[x][x] == t for x in range(self.boardsize)):
                # print(f"~~~~~~~~ Player {t} has won! ~~~~~~~~")
                return True

        return False

    def move(self, x, y, btn_callback):
        if self.is_win():
            messagebox.showerror(
                "Tic Tac Toe ~ À la Emma", f"Player {self.players[self.turn].token} has won the game! \nClick \"Restart Game\" to start a new game.")
            return
        if self.board[y][x] == " ":
            self.board[y][x] = self.players[self.turn].token
            btn_callback(x, y, self.players[self.turn].token)
        else:
            messagebox.showerror("Tic Tac Toe ~ À la Emma", "Choose an empty box!")
            return
        if self.is_win():
            messagebox.showerror("Tic Tac Toe ~ À la Emma", f"Player {self.players[self.turn].token} has won the game!")
            return
        # switch turns (for 2 players)
        self.turn = 1 - self.turn


class Board:
    def __init__(self, size):
        self.size = size
        self.board = [[" " for _ in range(size)] for _ in range(size)]

    def __str__(self):
        b = ""
        for lst in self.board:
            b += "|"
            for string in lst:
                b += string + "|"
            b += "\n"
        return b

    def __getitem__(self, idx):
        return self.board[idx]


class Player:
    def __init__(self, token, id):
        self.token = token
        self.id = id


game = App()
game.start_game()
