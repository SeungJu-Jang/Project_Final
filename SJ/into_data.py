import pymysql
 
con = pymysql.connect(host="192.168.0.37", user="root", password="1234",
                       db='mydb', charset='utf8')

cur = con.cursor()
 
sql="create table goods_test(" \
    "num int," \
    "goods varchar(20)," \
    "price int," \
    "primary key (num))"
 
cur.execute(sql)
con.commit()
sql="insert into goods_test values ('1','샴푸', '3700')"
cur.execute(sql)
con.commit()
