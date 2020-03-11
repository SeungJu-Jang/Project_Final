import pymysql

con = pymysql.connect(host="192.168.0.25", user="root", password="1541",
                       db='db1', charset='utf8')
a=0;
while True:
    if a==0:
        cur = con.cursor()
        sql="create table goodsss(" \
            "num int primary key,"\
            "name varchar(20),"\
            "price int,"\
            "inventory int)"
        cur.execute(sql)
        con.commit()
        sql="INSERT INTO goodsss(num, name, price, inventory) VALUES (%s, %s, %s, %s)"
        num=input()
        name=input()
        price=input()
        inventory=input()
        cur.execute(sql,(num,name,price,inventory))
        con.commit()
        a+=1;
    if a>0 | a<6:
        sql="INSERT INTO goodsss(num, name, price, inventory) VALUES (%s, %s, %s, %s)"
        num=input()
        name=input()
        price=input()
        inventory=input()
        cur.execute(sql,(num,name,price,inventory))
        con.commit()
        a+=1;
            
