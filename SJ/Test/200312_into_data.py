import pymysql

con = pymysql.connect(host="192.168.0.16", user="root", password="1234",
                       db='mydb')
a=0;
while True:
    if a==0:
        cur = con.cursor()
        sql="create table login" \
            "i_d varchar(20),"\
            "pw int,"\
            "name varchar(20),"\
            "birth int,"\
            "email varchar(20),"\
            "position varchar(20))"
        cur.execute(sql)
        con.commit()
        sql="INSERT INTO person1(i_d, pw) VALUES (%s, %s)"
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
        email=input()
        cur.execute(sql,(i_d,pw))
        con.commit()

        a=a+1;
    if a<3:
        sql="INSERT INTO person1(i_d, pw) VALUES (%s, %s)"
        print("id 입력하시오 ")
        i_d=input()
        print("pw 입력하시오 ")
        pw=input()
        cur.execute(sql,(i_d,pw))
        con.commit()
        a=a+1;
    else:
        break

cur = con.cursor()
sql="select count(*) from person1"
num = cur.execute(sql)
print(num)
            
