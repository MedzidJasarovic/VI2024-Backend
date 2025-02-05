from rest_framework.decorators import api_view
from rest_framework.response import Response
from .agents import MiniMaxAgent, NegascoutAgent
from .heuristics import *

minimaxP1 = MiniMaxAgent()
negascoutP1 = NegascoutAgent()

minimaxP2 = MiniMaxAgent()
negascoutP2 = NegascoutAgent()


# Create your views here.

@api_view(['POST'])
def get_move(request):
	board_state = request.data.get('board_state')
	depth = request.data.get('depth')
	diff = request.data.get('difficulty')
	opponent = request.data.get('opponent')
	algorithm = request.data.get('algorithm')
	gamemode = request.data.get('gamemode')

	modes = {
		"easy": Easy(),
		"medium": Medium(),
		"hard": Hard()
	}

	difficulty = modes.get(diff)

	if not all([board_state, diff]):
		return Response({'error': 'Missing required parameters'}, status=400)

	try:
		# move = 0
		if algorithm == 'minimax':
			if gamemode == "aa ":
				if opponent == 2:
					move = minimaxP2.get_chosen_column(board_state, depth, difficulty, opponent)
				elif opponent == 4:
					move = minimaxP1.get_chosen_column(board_state, depth, difficulty, opponent)
			else:
				move = minimaxP1.get_chosen_column(board_state, depth, difficulty, opponent)
		elif algorithm == 'negascout':
			if gamemode == "aa ":
				if opponent == 3:
					move = negascoutP2.get_chosen_column(board_state, depth, difficulty, opponent)
				elif opponent == 5:
					move = negascoutP1.get_chosen_column(board_state, depth, difficulty, opponent)
			else:
				move = negascoutP1.get_chosen_column(board_state, depth, difficulty, opponent)
		# minimax.ident = minimax.id
		return Response({'column': move})
	except Exception as e:
		return Response({'error': str(e)}, status=400)