import pymysql

con = pymysql.connect(host="192.168.0.2", user="root", password="1q2w3e",
                       db='db_1', charset='utf8' )

cur = con.cursor()
print("재고 최신화를 할 상품명 입력")
goods=int(input())
num=int(input())
print(goods)
print(num)

sql="select inventory from test1 where goods_numb=%s"
numb=cur.execute(sql,(goods))
data=[list(data_use) for data_use in cur.fetchall()]
for j in range(numb):
    for i in range(0,1):
        inventory=data[j]
    inventory[0]-=num
    print(inventory)
    
