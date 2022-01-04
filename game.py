# import random


class TicTacToe:
    def __init__(self):
        self.board = [
            [" ", " ", " "],
            [" ", " ", " "],
            [" ", " ", " "]
        ]

    def print_board(self):
        print("\n---+---+---\n".join(" " + " | ".join(row)
                                     for row in self.board) + " ")

    def make_player_move(self, player: int):
        symbol = "X" if player == 0 else "O"
        prompt = 'Enter coordinate in the form "row col": '
        while True:
            coords = input(prompt)
            if (coords := self.check_valid_move(coords)):
                x, y = coords
                self.board[x-1][y-1] = symbol
                self.print_board()
                break

    def check_valid_move(self, coords: str):
        coords = coords.split()
        try:
            coords = tuple(map(int, coords))
            return coords if len(coords) == 2 else False
        except ValueError:
            return False


tictactoe = TicTacToe()
tictactoe.print_board()
tictactoe.make_player_move(0)
tictactoe.make_player_move(1)
