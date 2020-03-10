import pymysql
 
con = pymysql.connect(host="192.168.0.25", user="root", password="1541",
                       db='db1', charset='utf8')


cur = con.cursor()
sql="INSERT INTO goods(num, name, price, inventory) VALUES (%s, %s)"
num=input()
name=input()
price=input()
inventory=input()
cur.execute(sql,(num,name))
con.commit()

