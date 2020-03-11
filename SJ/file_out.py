import pymysql
 
con = pymysql.connect(host="192.168.0.25", user="root", password="1541",
                       db='db1', charset='utf8')

curs = con.cursor()
sql="select distinct name from test1;"
curs.execute(sql)

data = curs.fetchall()
data1=list[data[0]
