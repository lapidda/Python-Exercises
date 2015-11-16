# coding: utf8
import ttr
from bs4 import BeautifulSoup
from decimal import *
import urllib.request
import time
import processing
import re
import sqlwork
import playerscrapper
start_time = time.time()

def get_matrixurls(url, verband = 0, bezirk = 0, kreis = 0):
	page = urllib.request.urlopen(url)
	soup = BeautifulSoup(page, "html.parser")
	relevant = soup.find("table", {"class":"matrix"})
	for td in relevant.find_all('td'):
		klasse = ''
		for child in td.findChildren(recursive=False):
			if not(child.find('a')):
				klasse = child.get_text()
				#print('Klasse: %s' % (klasse))
			else:
				for li in child.find_all('li'):
					league = li.find('a')
					league_urls = "http://bttv.click-tt.de%s" % (league['href'])
					#Liga Link
					#print(league_urls.encode('utf-8'))
					#Liga Name
					if(kreis != 0):
						print("Verband: %s -> Bezirk: %s -> Kreis: %s -> Klasse: %s -> Liga: %s" % (verband, bezirk, kreis, klasse, league.text))
					elif(bezirk != 0):
						print("Verband: %s -> Bezirk: %s -> Klasse: %s -> Liga: %s" % (verband, bezirk, klasse, league.text))
					else:
						print("Verband: %s -> Klasse: %s -> Liga: %s" % (verband, klasse, league.text))

def navigate_aufstellungen(url):
	#TODO navigate to Mannschaftsaufstellungen
	return

def get_subregions(url, verband = 0, bezirk = 0, kreis = 0):
	page = urllib.request.urlopen(url)
	soup = BeautifulSoup(page, "html.parser")

	#Find Div with Links other Sites
	relevant = soup.find("div", {"class":"liga-layer"})

	bzk = relevant.find_all("h2", {"class":"liga-layer-down"})
	krs = relevant.find_all("ul", {"class":"horizontal-menu"})
	for i in range(1,len(bzk)):
		bz_a = bzk[i].find('a')
		bezirk = bz_a.text
		follow_url = "http://bttv.click-tt.de%s" % (bz_a['href'])
		print("Verband: %s -> Bezirk: %s" % (verband, bezirk))
		get_matrixurls(follow_url, verband = verband, bezirk = bezirk)
		for kz_li in krs[i-1].find_all('li'):
			kz_a = kz_li.find('a')
			kreis = kz_a.text
			follow_url = "http://bttv.click-tt.de%s" % (kz_a['href'])
			print("Verband: %s -> Bezirk: %s -> Kreis: %s" % (verband, bezirk, kreis))
			get_matrixurls(follow_url, verband = verband, bezirk = bezirk, kreis = kreis)


			

				

def get_subregions_toplevel(url):
	#Needed to ignore a subset on DTTB Site
	page = urllib.request.urlopen(url)
	soup = BeautifulSoup(page, "html.parser")
	relevant = soup.find("div", {"class":"liga-layer"})
	for ul in relevant.find_all("ul", {"class":"horizontal-menu"}):
		for a in ul.find_all("a"):
			follow_url = "http://bttv.click-tt.de%s" % (a['href'])
			get_matrixurls(follow_url, verband = a.text)
			get_subregions(follow_url, verband = a.text)

def get_all(url):
	get_matrixurls(url, 'DTTB')
	get_subregions_toplevel(url)


#get_playerdata("http://bttv.click-tt.de/cgi-bin/WebObjects/nuLigaTTDE.woa/wa/groupPools?displayTyp=vorrunde&championship=V000+2015/16&group=251004")
#get_matrixurls("http://bttv.click-tt.de/cgi-bin/WebObjects/nuLigaTTDE.woa/wa/leaguePage?championship=V000+2015/16")
get_all("http://bttv.click-tt.de/cgi-bin/WebObjects/nuLigaTTDE.woa/wa/leaguePage?championship=DTTB+15/16")
#print("Paarkreuz 1: ", int(round(processing.get_avg(get_qttr("http://bttv.click-tt.de/cgi-bin/WebObjects/nuLigaTTDE.woa/wa/groupPools?displayTyp=vorrunde&championship=V000+2015/16&group=251004"),1),0)))
print("Runtime: %s s" % round(time.time() - start_time,2))