import pymysql
 
con = pymysql.connect(host="192.168.0.19", user="root", password="1234",
                       db='mydb', charset='utf8')

cur = con.cursor()
 
"""sql="create table goods(" \
    "num int," \
    "name varchar(20))"
cur.execute(sql)
con.commit()

sql="select * distinct name goods"
cur.execute(sql)
con.commit()"""


sql="select * from person1"
num = cur.execute(sql)
print(num)
