import pymysql
 
con = pymysql.connect(host="192.168.0.2", user="root", password="1541",
                       db='db1', charset='utf8')

cur = con.cursor()
sql="select * distinct name goods_2"
cur.execute(sql)
con.commit()
print(cur.execute(sql))
