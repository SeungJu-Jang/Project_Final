import pymysql

con = pymysql.connect(host="192.168.0.19", user="root", password="1234",db='mydb', charset='utf8')

cur = con.cursor()

sql='INSERT INTO timetable(date1, idproducts, out_goods) VALUES (%s, %s, %s)'
print("날짜를 입력 하시오. 예)2020-03-24")
date1=str(input())
print("상품의 번호를 입력하시오.")
idproducts=int(input())
out_goods=1

cur.execute(sql,(date1,idproducts,out_goods))
con.commit()

