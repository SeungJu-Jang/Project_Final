import pymysql
 
con = pymysql.connect(host="192.168.0.2", user="root", password="1541",
                       db='db1', charset='utf8')

curs = con.cursor()
sql="select distinct inventory from goods;"
curs.execute(sql)
data = curs.fetchall()
newlist = [data[0] for data in data]
print(newlist[3])
