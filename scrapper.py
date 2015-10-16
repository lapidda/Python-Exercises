#!/usr/bin/env python
import ttr
from bs4 import BeautifulSoup
from decimal import *
import urllib.request
import time
import processing
import re
import sqlwork
start_time = time.time()

def get_matrixurls(url):
	page = urllib.request.urlopen(url)
	soup = BeautifulSoup(page, "html.parser")
	relevant = soup.find("table", {"class":"matrix"})
	for span in relevant.find_all('span'):
		league_urls = "http://bttv.click-tt.de%s" % (span.find('a')['href'])
		print(league_urls.encode('utf-8'))

def navigate_aufstellungen(url):
	#TODO navigate to Mannschaftsaufstellungen
	return

def get_subregions(url):
	page = urllib.request.urlopen(url)
	soup = BeautifulSoup(page, "html.parser")

	#Find Div with Links other Sites
	relevant = soup.find("div", {"class":"liga-layer"})

	#Find Regional Sites
	for h2 in relevant.find_all("h2", {"class":"liga-layer-down"}):
		for a in h2.find_all('a'):
			follow_url = "http://bttv.click-tt.de%s" % (a['href'])
			print(follow_url.encode('utf-8'))
			get_matrixurls(follow_url)
			get_subregions(follow_url)
	#Find Sites in Regions
	for ul in relevant.find_all("ul", {"class":"horizontal-menu"}):
		for a in ul.find_all("a"):
			follow_url = "http://bttv.click-tt.de%s" % (a['href'])
			print(follow_url.encode('utf-8'))
			get_matrixurls(follow_url)
			get_subregions(follow_url)

def get_subregions_toplevel(url):
	#Needed to ignore a subset on DTTB Site

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

def get_playerdata(url):
	#url = "http://bttv.click-tt.de/cgi-bin/WebObjects/nuLigaTTDE.woa/wa/groupPools?displayTyp=vorrunde&championship=V000+2015/16&group=251004"
	page = urllib.request.urlopen(url)
	soup = BeautifulSoup(page, "html.parser")
	last_team = ''
	regioninfo = {}
	clubs = {}
	liga = {}
	region = soup.find(id='content-col1')
	region = region.find('h1')
	for line in region:
		if ('Herren' or 'Damen' or 'Jungen' or 'Mädchen' or 'Bambini') in line:
			tmp = line.strip().split(' ')
			liga['geschlecht'] = tmp[0]
			liga['klasse'] = str.join(' ', tmp[1:])
			print(liga)
	relevant = soup.find(id='content-row2')
	for tr in relevant.find_all('tr'):
		tdcheck = tr.find_all('td')
		if len(tr.find_all('th')) > 0:
			#do nothing
			pass
		elif tdcheck[0].has_attr('colspan'):
			last_team = tdcheck[0].h2.get_text()
			clubs[last_team] = {}
			clubs[last_team]['teaminfo'] = {}
			clubs[last_team]['teaminfo']['mannschaft'] = last_team
			#print(tdcheck[0].h2.get_text())
		else:
			position = Decimal(tdcheck[0].get_text().strip("\r\n"))
			rel_position = str(position-int(position))[2:]
			mannschaft = int(position)
			try:
	   			qttr = int(tdcheck[1].get_text())
			except ValueError:
				qttr = -1
			playerlink = tdcheck[2].find('a')['href']
			regex = re.search(r"person=(\d+)&", playerlink)
			pid = regex.group(1)
			regex = re.search(r"club=(\d+)", playerlink)
			clubid = regex.group(1)
			name = tdcheck[2].get_text().strip("\r\n").split(',')
			clubs[last_team]['position'] = int(rel_position)
			clubs[last_team]['mannschaft'] = mannschaft
			clubs[last_team]['teaminfo']['clubid'] = clubid
			clubs[last_team]['pid'] = pid
			clubs[last_team]['qttr'] = qttr
			clubs[last_team]['vorname'] = name[1][1:]
			clubs[last_team]['nachname'] = name[0]
			print(clubs[last_team])
			#sqlwork.sql_inserter(clubs[last_team])

			#print("%s %s hat %d Punkte." % (rel_position, name, qttr))
	#print(clubs)
	return clubs
get_playerdata("http://bttv.click-tt.de/cgi-bin/WebObjects/nuLigaTTDE.woa/wa/groupPools?displayTyp=vorrunde&championship=V000+2015/16&group=251004")
#get_matrixurls("http://bttv.click-tt.de/cgi-bin/WebObjects/nuLigaTTDE.woa/wa/leaguePage?championship=V000+2015/16")
#get_all("http://bttv.click-tt.de/cgi-bin/WebObjects/nuLigaTTDE.woa/wa/leaguePage?championship=DTTB+15/16")
#print("Paarkreuz 1: ", int(round(processing.get_avg(get_qttr("http://bttv.click-tt.de/cgi-bin/WebObjects/nuLigaTTDE.woa/wa/groupPools?displayTyp=vorrunde&championship=V000+2015/16&group=251004"),1),0)))
print("Runtime: %s s" % round(time.time() - start_time,2))