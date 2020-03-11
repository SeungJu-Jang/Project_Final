import pymysql


con = pymysql.connect(host="192.168.0.2", user="root", password="1541",
                       db='db1', charset='utf8')


cur = con.cursor()
sql="create table test(" \
    "num int primary key)"
cur.execute(sql)
con.commit()
sql="INSERT INTO goods(num) VALUES (%s)"
"""num=a"""


            
