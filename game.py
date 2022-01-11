import sys
import random
import re
from typing import Optional, Union
import time


class TicTacToe:
    def __init__(self):
        self.__board = [
            [" ", " ", " "],
            [" ", " ", " "],
            [" ", " ", " "]
        ]

        self.__empty_squares = 9
        self.__gamemode = None
        self.__current_player = "X"
        self.__player_symbol = None
        self.__ai_symbol = None
        self.__coords = None
        self.__game_ongoing = True
        self.__winner = None  # "X" for X, "O" for O, "Tie" for tie

    def get_board(self) -> list[list[str, str, str]]:
        return self.__board

    def get_current_player(self) -> str:
        return self.__current_player

    def get_status(self) -> int:
        return self.__check_status(self.__coords)

    def __print_board(self) -> None:
        print("\n" + "\n---+---+---\n".join(" " + " | ".join(row)
                                            for row in self.__board) + "\n")

    def __make_player_move(self, player: str) -> tuple[int, int]:
        prompt = f'Player {player}, Enter coordinate in the form "row col": '

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

    def __change_board(self, coords: tuple[int, int]) -> None:
        self.__board[coords[0]][coords[1]] = self.__current_player
        self.__empty_squares -= 1
        self.__print_board()
        self.__check_status(coords)

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

    def __check_col(self, col: int) -> bool:
        if self.__board[0][col] != " ":
            return self.__board[0][col] == self.__board[1][col] == self.__board[2][col]
        return False

    def __check_diag(self) -> bool:
        if self.__board[1][1] != " ":
            tl_to_br = self.__board[0][0] == self.__board[1][1] == self.__board[2][2]
            tr_to_bl = self.__board[2][0] == self.__board[1][1] == self.__board[0][2]
            return tl_to_br or tr_to_bl
        return False

    def __check_status(self, prev_move: Optional[tuple[int, int]]) -> bool:
        # TODO debug return values
        if prev_move is not None:
            row, col = prev_move
            checks = [self.__check_row(row), self.__check_col(
                col), self.__check_diag()]
            if any(checks):
                self.__game_ongoing = False
                if self.__gamemode == "pvp":
                    print(f"{self.__current_player} has won!")
                elif self.__gamemode == "ai0" and self.__current_player == self.__player_symbol:
                    print("You've won!")
                elif self.__gamemode == "ai0" and self.__current_player == self.__ai_symbol:
                    print("Sadly, the computer has beaten you.")
                else:
                    if self.__current_player == self.__player_symbol:
                        return -5
                    else:
                        return 5
            elif self.__empty_squares == 0:
                if self.__gamemode != "ai1":
                    print("Tie!")
                else:
                    return 0
        return None

    def __setup_game(self):
        self.__print_board()
        time.sleep(1)

    def play(self):
        menu = """Welcome to my TicTacToe Game!
Please select a game mode using the names:
    - pvp
    - ai
    - quit"""
        print(menu)
        while True:
            mode = input("Selection (pvp, ai, quit): ").strip().lower()
            print()
            if mode in ("pvp", "ai", "quit"):
                break
            else:
                print("Invalid selection.\n")
        if mode == "quit":
            sys.exit()
        elif mode == "pvp":
            self.__gamemode = "pvp"
            self.__play_pvp()
        else:
            while True:
                difficulty = input(
                    "Difficulty (easy, medium, advanced): ").strip().lower()
                print()
                if difficulty in ("easy", "medium", "advanced"):
                    break
                else:
                    print("Invalid selection.\n")
            if difficulty == "easy":
                self.__gamemode = "ai0"
            else:
                self.__gamemode = "ai1"
            self.__play_ai()

    def __play_pvp(self) -> None:
        self.__setup_game()
        while self.__game_ongoing:
            self.__coords = self.__make_player_move(self.__current_player)
            self.__change_board(self.__coords)
            self.__current_player = "X" if self.__current_player == "O" else "O"

    def __play_ai(self) -> None:
        self.__player_symbol = random.choice(["X", "O"])
        self.__ai_symbol = {"X", "O"} - set(self.__player_symbol)
        print(f"You are Player {self.__player_symbol}.")
        time.sleep(2)
        self.__setup_game()
        while self.__game_ongoing:
            if self.__player_symbol == self.__current_player:
                self.__coords = self.__make_player_move(self.__player_symbol)
            else:
                if self.__gamemode == "ai0":
                    possible_squares = self.__find_empty_squares()
                    self.__coords = random.choice(possible_squares)
                else:
                    self.__find_best_move()
                    print(
                        f"The AI has decided to go ({self.__coords[0]+1}, {self.__coords[1]+1}).")

            self.__change_board(self.__coords)
            self.__current_player = "X" if self.__current_player == "O" else "O"

    def __find_best_move(self):
        best_evaluation = float("-infinity")
        for square_row, square_col in self.__find_empty_squares():
            self.__board[square_row][square_col] = self.__ai_symbol
            curr_evaluation = self.__minimax(1, True)
            print(f"curr_evaluation = {curr_evaluation}")
            self.__board[square_row][square_col] = " "
            if curr_evaluation > best_evaluation:
                best_evaluation = curr_evaluation
                best_move = (square_row, square_col)
        self.__coords = best_move

    # Computer is maximising player
    # Human is minimising player
    def __minimax(self, depth, maximizingPlayer):
        evaluation = self.__check_status(self.__coords)
        if depth == 0 or self.__coords is not None:
            return evaluation
        if maximizingPlayer:
            max_evaluation = float("-infinity")
            for square_row, square_col in self.__find_empty_squares():
                self.__board[square_row][square_col] = self.__ai_symbol
                evaluation = self.__minimax(depth - 1, False)
                print(f"evaluation = {evaluation}")
                max_evaluation = max(max_evaluation, evaluation)
                self.__board[square_row][square_col] = " "
            return max_evaluation
        else:
            min_evaluation = float("infinity")
            for square_row, square_col in self.__find_empty_squares():
                self.__board[square_row][square_col] = self.__player_symbol
                evaluation = self.__minimax(depth - 1, True)
                max_evaluation = min(max_evaluation, evaluation)
                self.__board[square_row][square_col] = " "
            return min_evaluation


if __name__ == "__main__":
    print("This script is not supposed to be run directly. Please use 'main.py'.")
