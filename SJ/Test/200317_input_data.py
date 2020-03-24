import pymysql

con = pymysql.connect(host="192.168.0.2", user="root", password="1q2w3e",
                       db='db_1', charset='utf8' )
goods=['삼겹살',10]

cur = con.cursor()

sql="INSERT INTO test1(goods, inventory) VALUES (%s, %s)"

print("이름 입력하시오 ")
goods=goods[0]
print("재고 개수 입력")
inventory=goods[1]

cur.execute(sql,(goods, inventory))
con.commit()
