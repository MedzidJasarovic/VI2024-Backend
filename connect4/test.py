import random

# Assume ConnectFourAgent and other necessary classes are already defined above.

class ConnectFourGame:
    def __init__(self):
        self.board = [[0 for _ in range(7)] for _ in range(6)]
        self.human_id = 1
        self.ai_id = 2
        self.ai_agent = ConnectFourAgent()
    
    def print_board(self):
        print("\nCurrent Board:")
        for row in self.board:
            print(' '.join(str(cell) for cell in row))
        print("0 1 2 3 4 5 6\n")  # Column numbers for easy reference
    
    def is_valid_column(self, col):
        return 0 <= col < 7 and self.board[0][col] == 0
    
    def make_move(self, col, player_id):
        for row in reversed(range(6)):
            if self.board[row][col] == 0:
                self.board[row][col] = player_id
                break

    def check_for_winner(self, player_id):
        # Horizontal check
        for row in range(6):
            for col in range(4):
                if all(self.board[row][col + i] == player_id for i in range(4)):
                    return True
        # Vertical check
        for col in range(7):
            for row in range(3):
                if all(self.board[row + i][col] == player_id for i in range(4)):
                    return True
        # Diagonal checks
        for row in range(3):
            for col in range(4):
                if all(self.board[row + i][col + i] == player_id for i in range(4)):
                    return True
            for col in range(3, 7):
                if all(self.board[row + i][col - i] == player_id for i in range(4)):
                    return True
        return False

    def is_board_full(self):
        return all(self.board[0][col] != 0 for col in range(7))

    def play_game(self):
        print("Welcome to Connect Four!")
        self.print_board()
        
        while True:
            # Human turn
            human_move = None
            while human_move is None:
                try:
                    human_move = int(input("Your turn! Enter the column (0-6): "))
                    if not self.is_valid_column(human_move):
                        print("Column is full or invalid. Try again.")
                        human_move = None
                except ValueError:
                    print("Invalid input. Enter a column number (0-6).")

            self.make_move(human_move, self.human_id)
            self.print_board()
            
            if self.check_for_winner(self.human_id):
                print("Congratulations! You won!")
                break

            if self.is_board_full():
                print("It's a tie!")
                break
            
            # AI turn
            print("AI is thinking...")
            ai_move = self.ai_agent.get_chosen_column(self.board, 4)  # Set depth of 4 for the AI's minimax
            self.make_move(ai_move, self.ai_id)
            self.print_board()

            if self.check_for_winner(self.ai_id):
                print("The AI won! Better luck next time.")
                break

            if self.is_board_full():
                print("It's a tie!")
                break

# Create a game instance and start the game
game = ConnectFourGame()
game.play_game()
