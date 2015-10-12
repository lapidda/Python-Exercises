#!/usr/bin/env python
import ttr
from bs4 import BeautifulSoup
from decimal import *
import urllib.request
import time
start_time = time.time()

url = "http://bttv.click-tt.de/cgi-bin/WebObjects/nuLigaTTDE.woa/wa/groupPools?displayTyp=vorrunde&championship=B500+2015/16&group=251183"
page = urllib.request.urlopen(url)
soup = BeautifulSoup(page, "html.parser")
relevant = soup.find(id='content-row2')
last_team = ''
clubs = {}
for tr in relevant.find_all('tr'):
	tdcheck = tr.find_all('td')
	if len(tr.find_all('th')) > 0:
		#do nothing
		pass
	elif tdcheck[0].has_attr('colspan'):
		last_team = tdcheck[0].h2.get_text()
		clubs[last_team] = {}
		#print(tdcheck[0].h2.get_text())
	else:
		position = Decimal(tdcheck[0].get_text().strip("\r\n"))
		rel_position = str(position-int(position))[2:]
		try:
   			qttr = int(tdcheck[1].get_text())
		except ValueError:
			qttr = -1
		name = tdcheck[2].get_text().strip("\r\n")
		clubs[last_team][int(rel_position)] = qttr
		#print("%s %s hat %d Punkte." % (rel_position, name, qttr))

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
print("Paarkreuz 1: ", int(round(get_avg(clubs,1),0)))
print("Paarkreuz 2: ", int(round(get_avg(clubs,2),0)))
print("Paarkreuz 3: ", int(round(get_avg(clubs,3),0)))
print("Runtime: %s s" % round(time.time() - start_time,2))