class Hard:
	def evaluate_window(self, window, id):
		score = 0
		player_count = window.count(id)
		opponent_count = window.count(id - 1)
		empty_count = window.count(0)

		if player_count == 4:
			return float('inf') 
		if opponent_count == 4:
			return -float('inf')

		if player_count == 3 and empty_count == 1:
			score += 100 
		elif player_count == 2 and empty_count == 2:
			score += 10 

		elif opponent_count == 3 and empty_count == 1:
			score += 80

		elif player_count == 1 and empty_count == 3:
			score += 1 

		return score
	

class Medium:
	def evaluate_window(self, window, id):
		score = 0
		player_count = window.count(id)
		opponent_count = window.count(id - 1)
		empty_count = window.count(0)

		# Wins and losses
		if player_count == 4:
			return float('inf')  # AI wins
		if opponent_count == 4:
			return -float('inf')  # Opponent wins

		# Favorable situations for AI
		if player_count == 3 and empty_count == 1:
			score += 50  # AI is close to winning, less aggressive than hard
		elif player_count == 2 and empty_count == 2:
			score += 5  # Favorable for AI, but less weight than hard mode

		# Blocking opponent
		elif opponent_count == 3 and empty_count == 1:
			score += 40  # Block opponent, but less aggressive than hard

		# Neutral or slightly favorable situations
		elif player_count == 1 and empty_count == 3:
			score += 1  # Same as hard mode, slight advantage for setup

		return score

class Easy:
	def evaluate_window(self, window, id):
		score = 0
		player_count = window.count(id)
		opponent_count = window.count(id - 1)
		empty_count = window.count(0)

		# Wins and losses
		if player_count == 4:
			return float('inf')  # AI wins
		if opponent_count == 4:
			return -float('inf')  # Opponent wins

		# Favorable situations for AI
		if player_count == 3 and empty_count == 1:
			score += 20  # AI is close to winning, much less aggressive
		elif player_count == 2 and empty_count == 2:
			score += 2  # Favorable for AI, very minimal weight

		# Blocking opponent
		elif opponent_count == 3 and empty_count == 1:
			score += 10  # Less focus on blocking the opponent

		# Neutral or slightly favorable situations
		elif player_count == 1 and empty_count == 3:
			score += 1  # Same as hard and medium, setup value

		return score
