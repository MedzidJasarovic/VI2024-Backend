class HammingDistance:
    def calculate(self, current_state, goal_state):
        """Returns the number of tiles not in their goal position"""
        return sum(1 for i, j in zip(current_state, goal_state) if i != j and i != 0)

class ManhattanDistance:
    def calculate(self, current_state, goal_state):
        """Returns the sum of Manhattan distances of tiles from their goal positions"""
        size = int(len(current_state) ** 0.5)
        distance = 0
        
        for i in range(len(current_state)):
            if current_state[i] != 0:
                current_row, current_col = i // size, i % size
                goal_idx = goal_state.index(current_state[i])
                goal_row, goal_col = goal_idx // size, goal_idx % size
                distance += abs(current_row - goal_row) + abs(current_col - goal_col)
        
        return distance