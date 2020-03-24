import pymysql

con = pymysql.connect(host="192.168.0.19", user="root", password="1234",db='mydb', charset='utf8')

cur = con.cursor()

sql='alter table timetable add ~~~~'


cur.execute(sql)
con.commit()
con.close()
