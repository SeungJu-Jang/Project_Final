import pymysql
 
con = pymysql.connect(host="localhost", user="아이디", password="패스워드",
                       db='디비명', charset='utf8')
 
 
cur = con.cursor()
 
sql="create table sabjill(" \
    "title varchar(100)," \
    "content text," \
    "primary key (title))"
 
cur.execute(sql)
con.commit()
sql="insert into sabjill values ('제목','내용')"
cur.execute(sql)
con.commit()
 
sql="select * from sabjill"
num = cur.execute(sql)
print(num)
 
for i in cur:
    print(i)
 
 
 
cur.execute(sql)
result = cur.fetchall()
print(result)
print(result[0])
print(result[1])
print("")
 
cur.execute(sql)
result = cur.fetchall()
for v in result:
    print("제목 : {} 내용 : {}".format(v[0],v[1]))
 
sql = "delete from sabjill"
cur.execute(sql)
con.commit()
 
 
 
sql = "select * from sabjill where title=%s"
cur.execute(sql,'제목')
