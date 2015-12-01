import MySQLdb as sqlc
import sqldata
def sql_inserter(data_dic):
	con = sqlc.connect(host=info['host'], user=info['user'], passwd=info['password'], db=info['database'])
	cur = con.cursor()
	cur.execute("""INSERT INTO playerdata ( pid, vorname, nachname, qttr, position, mannschaft_no, clubid, %s) 
		VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
		ON DUPLICATE KEY UPDATE qttr='9999', position='0'""",
		(data_dic['liga']['geschlecht'], data_dic['pid'],data_dic['vorname'],data_dic['nachname'],data_dic['qttr'],data_dic['position'],data_dic['mannschaft_no'], data_dic['teaminfo']['clubid'], 'Oberfrankenliga'))
	con.commit()
	cur.close()
	con.close()
def add_verband(verband):
	con = sqlc.connect(host=info['host'], user=info['user'], passwd=info['password'], db=info['database'])
	cur = con.cursor()
	try:
		cur.execute(""" INSERT INTO verband (name)
			VALUES (%s) """, ([verband]))
		con.commit()
	except sqlc.Error as e:
		print(e)
	vid = ''
	try:
		cur.execute("SELECT vid FROM verband WHERE name = %s ", ([verband]))
		vid = cur.fetchone()[0]
	except sqlc.Error as e:
		print(e)
	finally:
		cur.close()
		con.close()
	return vid

def add_bezirk(bezirk, vid):
	con = sqlc.connect(host=info['host'], user=info['user'], passwd=info['password'], db=info['database'])
	cur = con.cursor()
	try:
		cur.execute(""" INSERT INTO bezirk (name,verband)
			VALUES (%s, %s) """, ([bezirk,vid]))
		con.commit()
	except sqlc.Error as e:
		print(e)
	bid = ''
	try:
		cur.execute("SELECT bid FROM bezirk WHERE name = %s AND verband = %s ", ([bezirk,vid]))
		bid = cur.fetchone()[0]
	except sqlc.Error as e:
		print(e)
	finally:
		cur.close()
		con.close()
	return bid

def add_kreis(kreis, vid, bid):
	con = sqlc.connect(host=info['host'], user=info['user'], passwd=info['password'], db=info['database'])
	cur = con.cursor()
	try:
		cur.execute(""" INSERT INTO kreis (name,bezirk,verband)
			VALUES (%s, %s, %s) """, ([kreis,bid,vid]))
		con.commit()
	except sqlc.Error as e:
		print(e)
	kid = ''
	try:
		cur.execute("SELECT kid FROM kreis WHERE name = %s AND bezirk = %s AND verband = %s ", ([kreis,bid,vid]))
		kid = cur.fetchone()[0]
	except sqlc.Error as e:
		print(e)
	finally:
		cur.close()
		con.close()
	return kid

def add_liga(liga, klasse, kid = 0, vid = 0, bid = 0):
	con = sqlc.connect(host=info['host'], user=info['user'], passwd=info['password'], db=info['database'])
	cur = con.cursor()
	try:
		cur.execute(""" INSERT INTO liga (name,klasse,kreis,bezirk,verband)
			VALUES (%s, %s, %s, %s, %s) """, ([liga,klasse,kid,bid,vid]))
		con.commit()
	except sqlc.Error as e:
		print(e)
	lid = ''
	try:
		cur.execute("SELECT lid FROM liga WHERE name = %s AND klasse = %s AND bezirk = %s AND verband = %s AND kreis = %s", ([liga,klasse,bid,vid,kid]))
		lid = cur.fetchone()[0]
	except sqlc.Error as e:
		print(e)
	finally:
		cur.close()
		con.close()
	return lid

info = sqldata.sqlinformations()
if __name__ == "__main__":
	#print(add_liga('donauwelle'))
	#print(add_kreis('Deine Mudda', -1, -1))
	#print(add_bezirk('Osterhausen123', -1))
	print("we did it reddit! Kappa")

