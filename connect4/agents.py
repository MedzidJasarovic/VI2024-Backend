import random
import time


class Agent:
    ident = 2

    def __init__(self):
        self.id = Agent.ident
        Agent.ident += 1

    def get_chosen_column(self, state, max_depth):
        pass



class MiniMaxAgent(Agent):
    def __init__(self):
        # self.difficulty = difficulty
        super().__init__()

    def get_chosen_column(self, state, max_depth, difficulty, opponent):
        best_move = self.minimax(state, max_depth, difficulty, opponent, True, -float('inf'), float('inf'))
        return best_move['column'] if best_move['column'] is not None else random.choice(self.get_valid_moves(state))

    def minimax(self, state, depth, difficulty, opponent, maximizing_player, alpha, beta):
        valid_moves = self.get_valid_moves(state)
        
        # Base case: return the evaluation score if at max depth or no valid moves
        is_terminal = self.check_for_winner(state, self.id) or self.check_for_winner(state, opponent) or not valid_moves
        if depth == 0 or is_terminal:
            if self.check_for_winner(state, self.id):
                return {'column': None, 'score': float('inf')}  # AI wins
            elif self.check_for_winner(state, opponent):
                return {'column': None, 'score': -float('inf')}  # Opponent wins
            elif not valid_moves:
                return {'column': None, 'score': 0}  # Draw
            return {'column': None, 'score': self.evaluate_board(state, difficulty)}

        if maximizing_player:
            best_move = {'column': None, 'score': -float('inf')}
            for move in valid_moves:
                new_state = self.simulate_move(state, move, self.id)
                result = self.minimax(new_state, depth - 1, difficulty, opponent, False, alpha, beta)

                if result['score'] > best_move['score']:
                    best_move = {'column': move, 'score': result['score']}
                alpha = max(alpha, best_move['score'])
                if beta <= alpha:
                    break  # Alpha-beta pruning
        else:
            best_move = {'column': None, 'score': float('inf')}
            for move in valid_moves:
                new_state = self.simulate_move(state, move, opponent)
                result = self.minimax(new_state, depth - 1, difficulty, opponent, True, alpha, beta)

                if result['score'] < best_move['score']:
                    best_move = {'column': move, 'score': result['score']}
                beta = min(beta, best_move['score'])
                if beta <= alpha:
                    break  # Alpha-beta pruning

        # Ensure a valid column is always returned, even as a fallback
        if best_move['column'] is None and valid_moves:
            best_move['column'] = random.choice(valid_moves)

        return best_move

    def simulate_move(self, state, column, player_id):
        new_state = [row[:] for row in state]  # Create a copy of the board
        for row in reversed(range(len(state))):  # Drop piece from the bottom
            if new_state[row][column] == 0:  # Find the first empty row in the column
                new_state[row][column] = player_id
                break
        return new_state

    def get_valid_moves(self, state):
        return [col for col in range(len(state[0])) if state[0][col] == 0]  # If the top row is empty

    def check_for_winner(self, state, player_id):
        # Horizontal check
        for row in range(6):
            for col in range(4):
                if all(state[row][col + i] == player_id for i in range(4)):
                    return True
        # Vertical check
        for col in range(7):
            for row in range(3):
                if all(state[row + i][col] == player_id for i in range(4)):
                    return True
        # Diagonal checks
        for row in range(3):
            for col in range(4):
                if all(state[row + i][col + i] == player_id for i in range(4)):
                    return True
            for col in range(3, 7):
                if all(state[row + i][col - i] == player_id for i in range(4)):
                    return True
        return False

    def evaluate_board(self, state, difficulty):
        score = 0
        score += self.evaluate_center(state)
        score += self.evaluate_rows(state, difficulty)
        score += self.evaluate_columns(state, difficulty)
        score += self.evaluate_diagonals(state, difficulty)
        return score

    def evaluate_center(self, state):
        # Prioritize placing pieces in the center column
        center_column = [state[row][3] for row in range(6)]
        center_count = center_column.count(self.id)
        return center_count * 3  # Assign a high score for center column occupancy

    def evaluate_rows(self, state, difficulty):
        score = 0
        for row in state:
            for col in range(len(row) - 3):
                window = row[col:col + 4]
                score += difficulty.evaluate_window(window, self.id)
        return score

    def evaluate_columns(self, state, difficulty):
        score = 0
        for col in range(len(state[0])):
            for row in range(len(state) - 3):
                window = [state[row + i][col] for i in range(4)]
                score += difficulty.evaluate_window(window, self.id)
        return score

    def evaluate_diagonals(self, state, difficulty):
        score = 0
        for row in range(len(state) - 3):
            for col in range(len(state[0]) - 3):
                window = [state[row + i][col + i] for i in range(4)]
                score += difficulty.evaluate_window(window, self.id)
            for col in range(3, len(state[0])):
                window = [state[row + i][col - i] for i in range(4)]
                score += difficulty.evaluate_window(window, self.id)
        return score



class NegascoutAgent(Agent):
    def __init__(self):
        super().__init__()

    def get_chosen_column(self, state, max_depth, difficulty, opponent):
        best_move = self.negascout(state, max_depth, -float('inf'), float('inf'), 1, difficulty, opponent)
        return best_move['column'] if best_move['column'] is not None else random.choice(self.get_valid_moves(state))

    def negascout(self, state, depth, alpha, beta, color, difficulty, opponent):
        valid_moves = self.get_valid_moves(state)
        
        # Base case: return the evaluation score if at max depth or no valid moves
        is_terminal = self.check_for_winner(state, self.id) or self.check_for_winner(state, opponent) or not valid_moves
        if depth == 0 or is_terminal:
            if self.check_for_winner(state, self.id):
                return {'column': None, 'score': color * float('inf')}  # AI wins
            elif self.check_for_winner(state, opponent):
                return {'column': None, 'score': color * -float('inf')}  # Opponent wins
            elif not valid_moves:
                return {'column': None, 'score': 0}  # Draw
            return {'column': None, 'score': color * self.evaluate_board(state, difficulty)}

        best_move = {'column': None, 'score': -float('inf')}
        for i, move in enumerate(valid_moves):
            new_state = self.simulate_move(state, move, self.id if color == 1 else opponent)
            if i == 0:
                score = -self.negascout(new_state, depth - 1, -beta, -alpha, -color, difficulty, opponent)['score']
            else:
                score = -self.negascout(new_state, depth - 1, -alpha - 1, -alpha, -color, difficulty, opponent)['score']
                if alpha < score < beta:
                    score = -self.negascout(new_state, depth - 1, -beta, -score, -color, difficulty, opponent)['score']

            if score > best_move['score']:
                best_move = {'column': move, 'score': score}

            alpha = max(alpha, score)
            if alpha >= beta:
                break  # Beta cutoff

        # Ensure a valid column is always returned, even as a fallback
        if best_move['column'] is None and valid_moves:
            best_move['column'] = random.choice(valid_moves)

        return best_move

    def simulate_move(self, state, column, player_id):
        new_state = [row[:] for row in state]  # Create a copy of the board
        for row in reversed(range(len(state))):  # Drop piece from the bottom
            if new_state[row][column] == 0:  # Find the first empty row in the column
                new_state[row][column] = player_id
                break
        return new_state

    def get_valid_moves(self, state):
        return [col for col in range(len(state[0])) if state[0][col] == 0]  # If the top row is empty

    def check_for_winner(self, state, player_id):
        # Horizontal check
        for row in range(6):
            for col in range(4):
                if all(state[row][col + i] == player_id for i in range(4)):
                    return True
        # Vertical check
        for col in range(7):
            for row in range(3):
                if all(state[row + i][col] == player_id for i in range(4)):
                    return True
        # Diagonal checks
        for row in range(3):
            for col in range(4):
                if all(state[row + i][col + i] == player_id for i in range(4)):
                    return True
            for col in range(3, 7):
                if all(state[row + i][col - i] == player_id for i in range(4)):
                    return True
        return False

    def evaluate_board(self, state, difficulty):
        score = 0
        score += self.evaluate_center(state)
        score += self.evaluate_rows(state, difficulty)
        score += self.evaluate_columns(state, difficulty)
        score += self.evaluate_diagonals(state, difficulty)
        return score

    def evaluate_center(self, state):
        # Prioritize placing pieces in the center column
        center_column = [state[row][3] for row in range(6)]
        center_count = center_column.count(self.id)
        return center_count * 3  # Assign a high score for center column occupancy

    def evaluate_rows(self, state, difficulty):
        score = 0
        for row in state:
            for col in range(len(row) - 3):
                window = row[col:col + 4]
                score += difficulty.evaluate_window(window, self.id)
        return score

    def evaluate_columns(self, state, difficulty):
        score = 0
        for col in range(len(state[0])):
            for row in range(len(state) - 3):
                window = [state[row + i][col] for i in range(4)]
                score += difficulty.evaluate_window(window, self.id)
        return score

    def evaluate_diagonals(self, state, difficulty):
        score = 0
        for row in range(len(state) - 3):
            for col in range(len(state[0]) - 3):
                window = [state[row + i][col + i] for i in range(4)]
                score += difficulty.evaluate_window(window, self.id)
            for col in range(3, len(state[0])):
                window = [state[row + i][col - i] for i in range(4)]
                score += difficulty.evaluate_window(window, self.id)
        return score




# testAgent = ConnectFourAgent()
# board = [[0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 2, 0, 0, 0], [0, 0, 2, 1, 1, 1, 0]]
# col = testAgent.get_chosen_column(board, 3)
# print(col)


# import random
# from heuristics import *


# # Assume ConnectFourAgent and other necessary classes are already defined above.
# diff = Easy()
# class ConnectFourGame:
#     def __init__(self):
#         self.board = [[0 for _ in range(7)] for _ in range(6)]
#         self.human_id = 1
#         self.ai_id = 2
#         self.ai_agent = MiniMaxAgent()
#         print(self.ai_agent.id)
    
#     def print_board(self):
#         print("\nCurrent Board:")
#         for row in self.board:
#             print('     '.join(str(cell) for cell in row))
#         print("---------------------\n")
#         print("0 1 2 3 4 5 6\n")  # Column numbers for easy reference
    
#     def is_valid_column(self, col):
#         return 0 <= col < 7 and self.board[0][col] == 0
    
#     def make_move(self, col, player_id):
#         for row in reversed(range(6)):
#             if self.board[row][col] == 0:
#                 self.board[row][col] = player_id
#                 break

#     def check_for_winner(self, player_id):
#         # Horizontal check
#         for row in range(6):
#             for col in range(4):
#                 if all(self.board[row][col + i] == player_id for i in range(4)):
#                     return True
#         # Vertical check
#         for col in range(7):
#             for row in range(3):
#                 if all(self.board[row + i][col] == player_id for i in range(4)):
#                     return True
#         # Diagonal checks
#         for row in range(3):
#             for col in range(4):
#                 if all(self.board[row + i][col + i] == player_id for i in range(4)):
#                     return True
#             for col in range(3, 7):
#                 if all(self.board[row + i][col - i] == player_id for i in range(4)):
#                     return True
#         return False

#     def is_board_full(self):
#         return all(self.board[0][col] != 0 for col in range(7))

#     def play_game(self):
#         print("Welcome to Connect Four!")
#         self.print_board()
        
#         while True:
#             # Human turn
#             human_move = None
#             while human_move is None:
#                 try:
#                     human_move = int(input("Your turn! Enter the column (0-6): "))
#                     if not self.is_valid_column(human_move):
#                         print("Column is full or invalid. Try again.")
#                         human_move = None
#                 except ValueError:
#                     print("Invalid input. Enter a column number (0-6).")

#             self.make_move(human_move, self.human_id)
#             self.print_board()
            
#             if self.check_for_winner(self.human_id):
#                 print("Congratulations! You won!")
#                 break

#             if self.is_board_full():
#                 print("It's a tie!")
#                 break
            
#             # AI turn
#             print("AI is thinking...")

#             ai_move = self.ai_agent.get_chosen_column(self.board, 4, diff, 1)  # Set depth of 4 for the AI's minimax
#             self.make_move(ai_move, self.ai_id)
#             self.print_board()

#             if self.check_for_winner(self.ai_id):
#                 print("The AI won! Better luck next time.")
#                 break

#             if self.is_board_full():
#                 print("It's a tie!")
#                 break

# # Create a game instance and start the game
# game = ConnectFourGame()
# game.play_game()
