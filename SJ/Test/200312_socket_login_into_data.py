import pymysql

con = pymysql.connect(host="192.168.0.16", user="root", password="1234",
                       db='mydb', charset='utf8' )

cur = con.cursor()

sql="drop table login"
cur.execute(sql)

sql="create table login(" \
    "i_d varchar(20),"\
    "pw varchar(20),"\
    "name varchar(20),"\
    "birth varchar(10),"\
    "email varchar(20),"\
    "position varchar(20))"

cur.execute(sql)
con.commit()

sql="INSERT INTO login(i_d, pw, name, birth, email, position) VALUES (%s, %s, %s, %s, %s, %s)"

print("아이디 입력하시오 ")
i_d=input()
print("암호 입력하시오 ")
pw=input()
print("이름 입력하시오 ")
name=input()
print("생년월일 입력하시오 ")
birth=input()
print("이메일 입력하시오 ")
email=input()
print("직책을 입력하시오 ")
position=input()
cur.execute(sql,(i_d, pw, name, birth, email, position))
con.commit()

print("조회할 회원의 번호를 입력 하시오") 
choice=int(input())

sql="select * from login where num='choice'"
cur.execute(sql)
data = cur.fetchall()
li = [x[0] for x in data]
print(li[0])
            
