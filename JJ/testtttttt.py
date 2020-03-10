import pymysql
conn = pymysql.connect(host = '192.168.0.37', user = 'root', password = '1234', db = 'testdb')
curs = conn.cursor()

sql = "SELECT * FROM user"
curs.execute(sql)

rows = curs.fetchall()

for i in rows:
    print(i)

conn.close()