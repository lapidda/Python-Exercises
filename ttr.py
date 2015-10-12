

def calc_winpercent(ttr_own, ttr_other):
	winpercent = 1/(1+pow(10,(ttr_other-ttr_own)/150.0))
	return winpercent

def calc_points(winpercent, won_games):
	return round((won_games-winpercent)*16)
	
def calc_game(ttr_own, ttr_opponent, wins):
	winpercent = 0
	for opponent in ttr_opponent:
		winpercent += calc_winpercent(ttr_own, opponent)
	return calc_points(winpercent, wins)

if __name__ == "__main__":
	print("Test Settings: TTR: 1480, Opponents: 1600, 1700")
	opponent = [1600,1700]
	myttr = 1480
	print("Win 0: ",calc_game(myttr, opponent, 0))
	print("Win 1: ",calc_game(myttr, opponent, 1))
	print("Win 2: ",calc_game(myttr, opponent, 2))

