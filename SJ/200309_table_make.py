import pymysql
 
con = pymysql.connect(host="192.168.0.25", user="root", password="1541",
                       db='db1', charset='utf8')

cur = con.cursor()
 
sql="create table goods_ex(" \"num int," \"goods_name varchar(20)," \"primary key (num))"
 
cur.execute(sql)
con.commit()
