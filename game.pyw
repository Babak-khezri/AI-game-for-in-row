from tkinter import *
import numpy as np
from time import sleep
import random
import math


class Game:

    GAME = None
    BOARD = None
    empty_image = black_image = red_image = None
    buttons = []
    SIZE = None
    GAME_OVER = False

    def __init__(self, size):
        self.SIZE = size
        self.BOARD = np.zeros((size, size), int)
        self.GAME = Tk()  # create Graphic
        self.GAME.title("Word Game")
        self.GAME.resizable(False, False)

        self.empty_image = PhotoImage(file='.//c_emp.png')
        self.black_image = PhotoImage(file='.//c_black.png')
        self.red_image = PhotoImage(file='.//c_red.png')

        self.create_board_screen(size)

        Button(bg='black', state='disable').grid(
            row=15, columnspan=size, sticky='nesw')

        numbers_list = [PhotoImage(
            file=f".//numbers/{i+1}.png") for i in range(9)]

        for i in range(size):
            Button(self.GAME, bd=6, image=numbers_list[i], command=lambda x=i: self.select_column(self.BOARD, x, 1)).grid(
                row=size+50, column=i)
        mainloop()

    def create_board_screen(self, size):
        for r in range(size):
            buttons = []
            for c in range(size):
                if self.BOARD[r][c] == 0:
                    img = self.empty_image
                elif self.BOARD[r][c] == 1:
                    img = self.black_image
                elif self.BOARD[r][c] == 2:
                    img = self.red_image

                button = Button(self.GAME, bd=6, bg='#d9d1cf', relief="sunken", image=img,
                                command=lambda x=c: self.select_column(self.BOARD, x,  1))
                button.grid(row=r+4, column=c)
                buttons.append(button)
            else:
                self.buttons.append(buttons)

    def select_column(self, board, column, player):
        if self.GAME_OVER:
            return
        for r in range(self.SIZE - 1, -1, -1):
            if board[r][column] == 0:
                board[r][column] = player
                if board is self.BOARD:
                    self.animation(player, r, column)
                    if self.check_wining(self.BOARD, player):
                        self.game_over(player)

                break

    def restart(self):
        self.GAME.destroy()
        self.restart_win.destroy()
        game2 = Game(7)
        pass

    def animation(self, player, row, column):
        index = 0
        while index != row:
            if player == 1:
                self.buttons[index][column].config(image=self.black_image)
                self.GAME.update()
                self.buttons[index][column].config(image=self.empty_image)
                sleep(0.035)
            else:
                self.buttons[index][column].config(image=self.red_image)
                self.GAME.update()
                sleep(0.035)
                self.buttons[index][column].config(image=self.empty_image)
            index += 1
        if player == 1:
            self.buttons[index][column].config(image=self.black_image)
            self.GAME.update()
            self.bot_select()
        else:
            self.buttons[index][column].config(image=self.red_image)
            self.GAME.update()

    def game_over(self, player):
        win_line = self.check_wining(self.BOARD, player)[1]
        self.GAME_OVER = True
        for node in win_line:
            self.buttons[node[0]][node[1]].config(bg='#5dd55d')
        self.restart_win = Tk()
        # rest_img = PhotoImage(file='.//restart.png')
        Button(self.restart_win, text='restart', bg='green', width=20,
               command=self.restart).grid(row=0, column=0)
        self.restart_win.mainloop()

    def score_position(self, board, piece):
        score = 0

        # Score center column
        center_array = [int(i) for i in list(board[:, self.SIZE//2])]
        center_count = center_array.count(piece)
        score += center_count * 3
        win_reqire_count = 4

        # Score Horizontal
        for r in range(self.SIZE):
            row_array = [int(i) for i in list(board[r, :])]

            for c in range(self.SIZE-3):
                line = row_array[c:c+win_reqire_count]
                score += self.evaluate_line(line, piece)

        # Score Vertical
        for c in range(self.SIZE):
            col_array = [int(i) for i in list(board[:, c])]
            for r in range(self.SIZE-3):
                line = col_array[r:r+win_reqire_count]
                score += self.evaluate_line(line, piece)

        # Score posiive sloped diagonal
        for r in range(self.SIZE-3):
            for c in range(self.SIZE-3):
                line = [board[r+i][c+i] for i in range(win_reqire_count)]
                score += self.evaluate_line(line, piece)

        for r in range(self.SIZE-3):
            for c in range(self.SIZE-3):
                line = [board[r+3-i][c+i] for i in range(win_reqire_count)]
                score += self.evaluate_line(line, piece)
        return score

    def evaluate_line(self, line, piece):
        score = 0
        opp_piece = 1
        if piece == 1:
            opp_piece = 2

        if line.count(piece) == 4:
            score += 10000
        elif line.count(piece) == 3 and line.count(0) == 1:
            score += 5
        elif line.count(piece) == 2 and line.count(0) == 2:
            score += 2

        if line.count(opp_piece) == 3 and line.count(0) == 1:
            score -= 4

        return score

    def is_terminal_node(self, board):
        return self.check_wining(board, 1) or self.check_wining(board, 2) or len(self.get_valid_locations(board)) == 0

    def minimax(self, board, depth, alpha, beta, maximizingPlayer):
        valid_locations = self.get_valid_locations(board)
        is_terminal = self.is_terminal_node(board)
        if depth == 0 or is_terminal:
            if is_terminal:
                if self.check_wining(board, 2):
                    return (None, 100000000000000)
                elif self.check_wining(board, 1):
                    return (None, -10000000000000)
                else:  # Game is over, no more valid moves
                    return (None, 0)
            else:  # Depth is zero
                return (None, self.score_position(board, 2))
        if maximizingPlayer:
            value = -math.inf
            for col in valid_locations:
                b_copy = board.copy()
                self.select_column(b_copy, col, 2)
                new_score = self.minimax(
                    b_copy, depth-1, alpha, beta, False)[1]
                if new_score > value:
                    value = new_score
                    column = col
                alpha = max(alpha, value)
                if alpha >= beta:
                    break
            return column, value

        else:  # Minimizing player
            value = math.inf
            for col in valid_locations:
                b_copy = board.copy()
                self.select_column(b_copy, col, 1)
                new_score = self.minimax(b_copy, depth-1, alpha, beta, True)[1]
                if new_score < value:
                    value = new_score
                    column = col
                beta = min(beta, value)
                if alpha >= beta:
                    break
            return column, value

    def get_valid_locations(self, board):
        return [col for col in range(self.SIZE) if board[0][col] == 0]

    def bot_select(self):
        col, minimax_score = self.minimax(
            self.BOARD, 4, -math.inf, math.inf, True)
        self.select_column(self.BOARD, col,  2)

    def check_wining(self, board, piece):
        # Check horizontal locations for win
        for c in range(self.SIZE - 3):
            for r in range(self.SIZE):
                if board[r][c] == piece and board[r][c+1] == piece and board[r][c+2] == piece and board[r][c+3] == piece:
                    return True, [[r, c], [r, c+1], [r, c+2], [r, c+3]]

        # Check vertical locations for win
        for c in range(self.SIZE):
            for r in range(self.SIZE-3):
                if board[r][c] == piece and board[r+1][c] == piece and board[r+2][c] == piece and board[r+3][c] == piece:
                    return True, [[r, c], [r+1, c], [r+2, c], [r+3, c]]

        # Check positively sloped diaganols
        for c in range(self.SIZE - 3):
            for r in range(self.SIZE-3):
                if board[r][c] == piece and board[r+1][c+1] == piece and board[r+2][c+2] == piece and board[r+3][c+3] == piece:
                    return True, [[r, c], [r+1, c+1], [r+2, c+2], [r+3, c+3]]

        # Check negatively sloped diaganols
        for c in range(self.SIZE - 3):
            for r in range(3, self.SIZE):
                if board[r][c] == piece and board[r-1][c+1] == piece and board[r-2][c+2] == piece and board[r-3][c+3] == piece:
                    return True, [[r, c], [r-1, c+1], [r-2, c+2], [r-3, c+3]]


game = Game(7)
