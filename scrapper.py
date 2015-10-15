#!/usr/bin/env python
import ttr
from bs4 import BeautifulSoup
from decimal import *
import urllib.request
import time
import processing
start_time = time.time()

def get_matrixurls(url):
	page = urllib.request.urlopen(url)
	soup = BeautifulSoup(page, "html.parser")
	relevant = soup.find("table", {"class":"matrix"})
	for span in relevant.find_all('span'):
		league_urls = "http://bttv.click-tt.de%s" % (span.find('a')['href'])
		print(league_urls.encode('utf-8'))

def get_subregions(url):
	page = urllib.request.urlopen(url)
	soup = BeautifulSoup(page, "html.parser")
	relevant = soup.find("div", {"class":"liga-layer"})
	for h2 in relevant.find_all("h2", {"class":"liga-layer-down"}):
		for a in h2.find_all('a'):
			follow_url = "http://bttv.click-tt.de%s" % (a['href'])
			print(follow_url.encode('utf-8'))
			get_matrixurls(follow_url)
			get_subregions(follow_url)
	for ul in relevant.find_all("ul", {"class":"horizontal-menu"}):
		for a in ul.find_all("a"):
			follow_url = "http://bttv.click-tt.de%s" % (a['href'])
			print(follow_url.encode('utf-8'))
			get_matrixurls(follow_url)
			get_subregions(follow_url)

def get_subregions_toplevel(url):
	page = urllib.request.urlopen(url)
	soup = BeautifulSoup(page, "html.parser")
	relevant = soup.find("div", {"class":"liga-layer"})
	for ul in relevant.find_all("ul", {"class":"horizontal-menu"}):
		for a in ul.find_all("a"):
			follow_url = "http://bttv.click-tt.de%s" % (a['href'])
			print(follow_url.encode('utf-8'))
			get_matrixurls(follow_url)
			get_subregions(follow_url)

def get_all(url):
	get_matrixurls(url)
	get_subregions_toplevel(url)

def get_qttr(url):
	#url = "http://bttv.click-tt.de/cgi-bin/WebObjects/nuLigaTTDE.woa/wa/groupPools?displayTyp=vorrunde&championship=V000+2015/16&group=251004"
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
	#print(clubs)
	return clubs
#get_matrixurls("http://bttv.click-tt.de/cgi-bin/WebObjects/nuLigaTTDE.woa/wa/leaguePage?championship=V000+2015/16")
get_all("http://bttv.click-tt.de/cgi-bin/WebObjects/nuLigaTTDE.woa/wa/leaguePage?championship=DTTB+15/16")
#print("Paarkreuz 1: ", int(round(processing.get_avg(get_qttr("http://bttv.click-tt.de/cgi-bin/WebObjects/nuLigaTTDE.woa/wa/groupPools?displayTyp=vorrunde&championship=V000+2015/16&group=251004"),1),0)))
print("Runtime: %s s" % round(time.time() - start_time,2))