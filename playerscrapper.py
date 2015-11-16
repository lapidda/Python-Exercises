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

	if __name__ == "__main__":
		print("we did it reddit! Kappa")

