import sqlite3

def exec_sql(sql, db_file):
	# print(sql)
	conn = sqlite3.connect(db_file)
	c = conn.cursor()
	c.execute(sql)
	results = c.fetchall()
	conn.commit()
	conn.close()
	return results