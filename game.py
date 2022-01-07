# import random
import re


class TicTacToe:
    def __init__(self):
        self.__board = [
            [" ", " ", " "],
            [" ", " ", " "],
            [" ", " ", " "]
        ]

    def get_board(self):
        return self.__board

    def __print_board(self):
        print("\n" + "\n---+---+---\n".join(" " + " | ".join(row)
                                            for row in self.board) + "\n")

    def __make_player_move(self, player: int):
        symbol = "X" if player == 0 else "O"
        prompt = f'Player {symbol}, Enter coordinate in the form "row col": '
        while True:
            coords = input(prompt)
            if (coords := self.__check_valid_move(coords)):
                self.board[coords[0]][coords[1]] = symbol
                self.print_board()
                break

    def __check_valid_move(self, coords: str):
        if not re.fullmatch(r"\d\s\d", coords):
            print('Invalid input: Please enter integers in the form "row col".\n')
            return False

        x, y = tuple(map(lambda x: int(x)-1, coords.split()))
        coord_reqs = (0 <= x <= 2, 0 <= y <= 2)
        if not all(coord_reqs):
            print("Invalid input: Given coordinates does not correspond with a square.\n")
            return False
        elif self.board[x][y] != " ":
            print("Invalid input: Space already taken.\n")
            return False
        else:
            return x, y


tictactoe = TicTacToe()
tictactoe.print_board()
tictactoe.make_player_move(0)
tictactoe.make_player_move(1)
tictactoe.make_player_move(0)
