from rest_framework.decorators import api_view
from rest_framework.response import Response
from .algorithms import BreadthFirstSearch, BestFirstSearch, AStarSearch
from .heuristics import HammingDistance, ManhattanDistance
import time 

@api_view(['POST'])
def solve_puzzle(request):
    initial_state = tuple(request.data.get('initial_state'))
    goal_state = tuple(request.data.get('goal_state'))
    algorithm = request.data.get('algorithm')
    heuristic = request.data.get('heuristic')
    size = request.data.get('size')
    
    if not all([initial_state, goal_state, algorithm, size]):
        return Response({'error': 'Missing required parameters'}, status=400)
    
    algorithms = {
        'bfs': BreadthFirstSearch(size),
        'best_first': BestFirstSearch(size, heuristic=ManhattanDistance() if heuristic == 'manhattan' else HammingDistance()),
        'astar': AStarSearch(size, heuristic=ManhattanDistance() if heuristic == 'manhattan' else HammingDistance())
    }
    
    solver = algorithms.get(algorithm)
    if not solver:
        return Response({'error': 'Invalid algorithm'}, status=400)
    
    try:
        start_time = time.time()
        steps = solver.get_steps(initial_state, goal_state)
        end_time = time.time()

        # Calculate elapsed time
        elapsed_time = end_time - start_time

        return Response({
            'steps': steps,
            'time_taken': f"{elapsed_time:.4f} seconds"  # Time in seconds with 4 decimal places
        })
    except Exception as e:
        return Response({'error': str(e)}, status=400)