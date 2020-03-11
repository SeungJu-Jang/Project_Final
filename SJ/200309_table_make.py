import pymysql
 
con = pymysql.connect(host="192.168.0.19", user="root", password="1234",
                       db='mydb', charset='utf8')

cur = con.cursor()
 
sql="create table goods(" \
    "num int," \
    "goods_name varchar(20)," \
    "inventory int)"
cur.execute(sql)
con.commit()
cur = con.cursor()
sql="select * distinct name goods"
cur.execute(sql)
con.commit()
