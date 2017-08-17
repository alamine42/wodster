import sqlite3

WORKOUTS_FILE = 'invictus.db'

def exec_sql(sql):
		conn = sqlite3.connect(WORKOUTS_FILE)
		c = conn.cursor()
		c.execute(sql)
		results = c.fetchall()
		conn.commit()
		conn.close()
		return results