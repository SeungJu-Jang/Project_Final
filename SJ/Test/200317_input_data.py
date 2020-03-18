import pymysql

con = pymysql.connect(host="192.168.0.2", user="root", password="1q2w3e",
                       db='db_1', charset='utf8' )

cur = con.cursor()

sql="INSERT INTO employee_list(position, name, i_d, pw, email, birth) VALUES (%s, %s, %s, %s, %s, %s)"
print("직책을 입력하시오 ")
position=input()
print("이름 입력하시오 ")
name=input()
print("아이디 입력하시오 ")
i_d=input()
print("암호 입력하시오 ")
pw=input()
print("이메일 입력하시오 ")
email=input()
print("생년월일 입력하시오 ")
birth=input()

cur.execute(sql,(position, name, i_d, pw, email, birth))
con.commit()
