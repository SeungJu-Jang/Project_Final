import pymysql
 
con = pymysql.connect(host="192.168.0.2", user="user", password="1234",
                       db='db1', charset='utf8')

cur = con.cursor()
sql="create table person(" \
    "id int," \
    "pw varchar(20))"
cur.execute(sql)
con.commit()
cur = con.cursor()
sql="INSERT INTO person(id, pw) VALUES (%s, %s)"
id=input()
pw=input()
cur.execute(sql,(num,name))
con.commit()

