import pymysql

con = pymysql.connect(host="192.168.0.2", user="user", password="1234",
                       db='db1')
a=0;
"""while True:
    if a==0:
        cur = con.cursor()
        sql="create table person1(" \
            "i_d varchar(20),"\
            "pw int)"
        cur.execute(sql)
        con.commit()
        sql="INSERT INTO person1(i_d, pw) VALUES (%s, %s)"
        print("id 입력하시오 ")
        i_d=input()
        print("pw 입력하시오 ")
        pw=input()
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
        break"""

cur = con.cursor()
sql="select count(*) from person1"
num = cur.execute(sql)
print(num)
            
