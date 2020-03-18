import pymysql

con = pymysql.connect(host="192.168.0.19", user="root", password="1234",
                       db='mydb', charset='utf8')
a=0;
while True:
    if a==0:
        cur = con.cursor()
        sql="create table goods_1(" \
            "num int primary key,"\
            "name varchar(20),"\
            "price int,"\
            "inventory int)"
        cur.execute(sql)
        con.commit()
        sql="INSERT INTO goods_1(num, name, price, inventory) VALUES (%s, %s, %s, %s)"
        print("상품의 번호 입력 ")
        num=input()
        print("상품의 이름 입력 ")
        name=input()
        print("상품의 가격 입력 ")
        price=input()
        print("상품의 재고 입력 ")
        inventory=input()
        cur.execute(sql,(num,name,price,inventory))
        con.commit()
        a=a+1;
    if a<24:
        sql="INSERT INTO goods_1(num, name, price, inventory) VALUES (%s, %s, %s, %s)"
        print("상품의 번호 입력 ")
        num=input()
        print("상품의 이름 입력 ")
        name=input()
        print("상품의 가격 입력 ")
        price=input()
        print("상품의 재고 입력 ")
        inventory=input()
        cur.execute(sql,(num,name,price,inventory))
        con.commit()
        a=a+1;
    else:
        break
            
