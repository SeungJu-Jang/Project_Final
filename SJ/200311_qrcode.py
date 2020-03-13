import pymysql

con = pymysql.connect(host="127.0.0.1", user="root", password="123321",
                       db='mydb', charset='utf8')

cur = con.cursor()
sql="INSERT INTO goods(num,name,price,inventory) VALUES (%s, %s, %s, %s)"
num=input()
name=input()
price=input()
inventory=input()


            
