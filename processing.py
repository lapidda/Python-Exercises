#print(tr)
def get_avg(clubs, paarkreuz = 0):
	clubavg = 0
	clubavg_count = 0
	avg = 0
	avg_count = 0
	pk_set = [1,7]
	if paarkreuz == 1:
		pk_set = [1,3]
	elif paarkreuz == 2:
		pk_set = [3,5]
	elif paarkreuz == 3:
		pk_set = [5,7]
	for club in clubs:
		for i in range(pk_set[0], pk_set[1]):
			if clubs[club][i] > 0:
				clubavg += clubs[club][i]
				clubavg_count += 1				
		avg += clubavg
		avg_count += clubavg_count
		print("%s avg: %i" % (club, clubavg/clubavg_count)) 
		clubavg = 0
		clubavg_count = 0
	return avg/avg_count


#for club in clubs:
#	print(club)
#	for i in range(1,7):
#		print(clubs[club][i])
#print("Paarkreuz 1: ", int(round(get_avg(clubs,1),0)))
#print("Paarkreuz 2: ", int(round(get_avg(clubs,2),0)))
#print("Paarkreuz 3: ", int(round(get_avg(clubs,3),0)))