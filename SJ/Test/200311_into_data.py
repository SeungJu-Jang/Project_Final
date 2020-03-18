import pymysql

con = pymysql.connect(host="192.168.0.2", user="user", password="1234",
                       db='db1')
a=0;
while True:
    if a==0:
        cur = con.cursor()
        sql="create table gb(" \
            "num int,"\
            "name_kr varchar(20),"\
            "inventory int)DEFAULT CHARSET=utf8"
        cur.execute(sql)
        con.commit()
        
        sql="INSERT INTO gb(num, name_kr, inventory) VALUES (%s, %s, %s)"
        print("상품의 번호 입력 ")
        num=input()
        print("상품의 이름 입력 ")
        name=input()
        name_kr=str(name)
        print("상품의 재고 입력 ")
        inventory=input()
        cur.execute(sql,(num,name_kr,inventory))
        con.commit()

        a=a+1;
    if a<2:
        sql="INSERT INTO gb(num, name_kr, inventory) VALUES (%s, %s, %s)"
        print("상품의 번호 입력 ")
        num=input()
        print("상품의 이름 입력 ")
        name=input()
        name_kr=str(name)
        print("상품의 재고 입력 ")
        inventory=input()
        cur.execute(sql,(num,name_kr,inventory))
        con.commit()
        a=a+1;
    else:
        break
            
