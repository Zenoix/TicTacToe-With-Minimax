import random
import re
from typing import Optional, Union


class TicTacToe:
    def __init__(self):
        self.__board = [
            [" ", " ", " "],
            [" ", " ", " "],
            [" ", " ", " "]
        ]

        self.__empty_squares = 9
        self.__print_board()

    def get_board(self) -> list[list[str, str, str]]:
        return self.__board

    def __print_board(self) -> None:
        print("\n" + "\n---+---+---\n".join(" " + " | ".join(row)
                                            for row in self.__board) + "\n")

    def __make_player_move(self, symbol: str) -> tuple[int, int]:
        prompt = f'Player {symbol}, Enter coordinate in the form "row col": '

        coords = input(prompt).strip()
        while not (coords := self.__check_valid_move(coords)):
            coords = input(prompt).strip()

        return coords

    def __check_valid_move(self, coords: str) -> Union[bool, tuple[int, int]]:
        if not re.fullmatch(r"\d\s\d", coords):
            print('Invalid input: Please enter integers in the form "row col".\n')
            return False

        row, col = tuple(map(lambda x: int(x)-1, coords.split()))
        coord_reqs = (0 <= row <= 2, 0 <= col <= 2)
        if not all(coord_reqs):
            print("Invalid input: Given coordinates does not correspond with a square.\n")
            return False
        elif self.__board[row][col] != " ":
            print("Invalid input: Space already taken.\n")
            return False
        else:
            return row, col

    def __change_board(self, symbol: str, coords: tuple[int, int]) -> None:
        self.__board[coords[0]][coords[1]] = symbol
        self.__empty_squares -= 1
        self.__print_board()
        self.__check_status()

    def __find_empty_squares(self) -> Optional[list[tuple[int, int]]]:
        empty_squares = []
        for i, _ in enumerate(self.__board):
            for j, square in enumerate(self.__board[i]):
                if square == " ":
                    empty_squares.append((i, j))
        return empty_squares

    def __check_row(self, row: int) -> bool:
        if self.__board[row][0] != " ":
            return self.__board[row][0] == self.__board[row][1] == self.__board[row][2]
        return False

    def __check_col(self, col: int) --> bool:
        if self.__board[0][col] != " ":
            return self.__board[0][col] == self.__board[1][col] == self.__board[2][col]
        return False

    def __check_diag(self) --> bool:
        if self.__board[1][1] != " ":
            tl_to_br = self.__board[0][0] == self.__board[1][1] == self.__board[2][2]
            tr_to_bl = self.__board[2][0] == self.__board[1][1] == self.__board[0][2]
            return tl_to_br or tr_to_bl
        return False

    def __check_status(self, symbol: str, prev_move: Optional[tuple[int, int]]) --> bool:
        if symbol is None or prev_move is None:
            return True
        
        row, col = prev_move
        checks = [self.__check_row(row), self.__check_col(
            col), self.__check_diag()]
        if any(checks):
            print(f"{symbol} has won!")
            return False
        elif self.__empty_squares == 0:
            print("Tie!")
            return False
        return True

    def __setup_game(self):
        self.__current_player = "X"
        self.__coords = None

    def play(self):
        self.__setup_game()

    def play_pvp(self) -> None:
        while self.__check_status(player, self.coords):
            self.coords = self.__make_player_move(player)
            self.__change_board(player, self.coords)
            player = "X" if player == "O" else "O"

    def play_ai(self, level: int = 0) -> None:
        player_symbol = random.choice(["X", "O"])
        while self.__check_status(self.__current_player, self.coords):
            if player_symbol == self.__current_player:
                self.coords = self.__make_player_move(player_symbol)
            elif level == 0:
                possible_squares = self.__find_empty_squares()
                self.coords = random.choice(possible_squares)
                print(
                    f"The AI has decided to go ({self.coords[0]+1}, {self.coords[1]+1}).")
            self.__change_board(self.__current_player, self.coords)
            self.__current_player = "X" if self.__current_player == "O" else "O"


if __name__ == "__main__":
    ttt = TicTacToe()
    ttt.play()
