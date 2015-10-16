import MySQLdb as sqlc
def sql_inserter(data_dic):
	con = sqlc.connect(host='###', user='###', passwd='###', db='###')
	cur = con.cursor()
	cur.execute("""INSERT INTO playerdata ( pid, vorname, nachname, qttr, position, mannschaft_no, clubid, %s) 
		VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
		ON DUPLICATE KEY UPDATE qttr='9999', position='0'""",
		(data_dic['liga']['geschlecht'], data_dic['pid'],data_dic['vorname'],data_dic['nachname'],data_dic['qttr'],data_dic['position'],data_dic['mannschaft_no'], data_dic['teaminfo']['clubid'], 'Oberfrankenliga'))
	con.commit()
	cur.close()
	con.close()
if __name__ == "__main__":
	

