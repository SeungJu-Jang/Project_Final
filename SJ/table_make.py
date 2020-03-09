import pymysql
 
con = pymysql.connect(host="192.168.0.37", user="root", password="1234",
                       db='mydb', charset='utf8')

cur = con.cursor()
 
sql="create table sabjill(" \
    "num int," \
    "goods varchar(20)," \
    "primary key (num))"
 
cur.execute(sql)
con.commit()
