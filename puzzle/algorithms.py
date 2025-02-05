import time
from collections import deque
import heapq

class Algorithm:
    def __init__(self, size, heuristic=None):
        self.size = size
        self.heuristic = heuristic
        self.nodes_evaluated = 0
        self.nodes_generated = 0

    def get_legal_actions(self, state):
        self.nodes_evaluated += 1
        max_index = len(state)
        zero_tile_ind = state.index(0)
        legal_actions = []
        if 0 <= (up_ind := (zero_tile_ind - self.size)) < max_index:
            legal_actions.append(up_ind)
        if 0 <= (right_ind := (zero_tile_ind + 1)) < max_index and right_ind % self.size:
            legal_actions.append(right_ind)
        if 0 <= (down_ind := (zero_tile_ind + self.size)) < max_index:
            legal_actions.append(down_ind)
        if 0 <= (left_ind := (zero_tile_ind - 1)) < max_index and (left_ind + 1) % self.size:
            legal_actions.append(left_ind)
        return legal_actions

    def apply_action(self, state, action):
        self.nodes_generated += 1
        copy_state = list(state)
        zero_tile_ind = state.index(0)
        copy_state[action], copy_state[zero_tile_ind] = copy_state[zero_tile_ind], copy_state[action]
        return tuple(copy_state)

    def get_steps(self, initial_state, goal_state):
        pass

    def get_solution_steps(self, initial_state, goal_state):
        begin_time = time.time()
        solution_actions = self.get_steps(initial_state, goal_state)
        print(f'Execution time in seconds: {(time.time() - begin_time):.2f} | '
              f'Nodes generated: {self.nodes_generated} | '
              f'Nodes evaluated: {self.nodes_evaluated}')
        return solution_actions


class BreadthFirstSearch(Algorithm):
    def get_steps(self, initial_state, goal_state):
        # BFS uses a queue (FIFO) for storing states to be explored
        queue = deque([(initial_state, [])])  # Queue holds tuples of (state, path_to_state)
        visited = set()  # To keep track of visited states

        while queue:
            current_state, path = queue.popleft()
            
            # Check if the current state is the goal
            if current_state == goal_state:
                return path  # Path to goal
            
            # Mark the current state as visited
            visited.add(current_state)

            # Get possible moves and explore new states
            for action in self.get_legal_actions(current_state):
                next_state = self.apply_action(current_state, action)
                
                # Only explore new states that haven't been visited
                if next_state not in visited:
                    queue.append((next_state, path + [action]))  # Add new state with updated path

        # If goal is not reachable (shouldn't happen in a solvable puzzle)
        return None


class BestFirstSearch(Algorithm):
    def get_steps(self, initial_state, goal_state):
        pq = [(0, id(initial_state), initial_state, [])]
        visited = {tuple(initial_state)}
        
        while pq:
            _, _, current_state, path = heapq.heappop(pq)
            if current_state == goal_state:
                return path
            
            legal_actions = self.get_legal_actions(current_state)
            
            for action in legal_actions:
                new_state = self.apply_action(current_state, action)
                
                if tuple(new_state) not in visited:
                    visited.add(tuple(new_state))
                    h = self.heuristic.calculate(new_state, goal_state)
                    heapq.heappush(pq, (h, id(new_state), new_state, path + [action]))
        
        return []


class AStarSearch(Algorithm):
    def get_steps(self, initial_state, goal_state):
        pq = [(0, 0, id(initial_state), initial_state, [])]
        visited = {tuple(initial_state)}
        g_scores = {tuple(initial_state): 0}
        
        while pq:
            _, g, _, current_state, path = heapq.heappop(pq)
            if current_state == goal_state:
                return path
            
            legal_actions = self.get_legal_actions(current_state)
            
            for action in legal_actions:
                new_state = self.apply_action(current_state, action)
                new_g = g + 1
                
                if tuple(new_state) not in visited or new_g < g_scores[tuple(new_state)]:
                    visited.add(tuple(new_state))
                    g_scores[tuple(new_state)] = new_g
                    h = self.heuristic.calculate(new_state, goal_state)
                    f = new_g + h
                    heapq.heappush(pq, (f, new_g, id(new_state), new_state, path + [action]))
        
        return []

