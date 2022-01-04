import random

class TicTacToe:
    def __init__(self):
        self.board = [[" "] * 3] * 3
        
    def print_board(self):
        print("\n---+---+---\n".join(" " + " | ".join(row) for row in self.board) + " ")
    
    def make_player_move(self, player):
        symbol = "X" if player == 0 else "O"
        while True:
            try:
                x, y = map(int, input("Enter coordinate in the form row col: ").split())
            except TypeError:
                print("Invalid coordinate")
            if check_valid_move(x, y):
                self.board[x-1][y-1] = symbol
    def check_valid_move(self, x, y):
        return True
tictactoe = TicTacToe()
tictactoe.print_board()
tictactoe.make_player_move()