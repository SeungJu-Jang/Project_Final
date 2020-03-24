import pymysql

con = pymysql.connect(host="192.168.0.2", user="root", password="1q2w3e",
                       db='db_1', charset='utf8' )
goods=[1,0]

cur = con.cursor()

sql="select inventory from test1 where goods_numb=%s"
numb=cur.execute(sql,(goods[0]))
data=[list(data_use) for data_use in cur.fetchall()]
print(data)
for i in range(numb):
    for j in range(0,1):
        inventory=data[i]
        print(inventory)
        if inventory[0]-goods[1]>=0:
            inventory[0]-=goods[1] #바코드 스캔시 감소되게 처리
        else:
            print("재고 처리가 반영되지 않았습니다.")
            pass
print(inventory[0])
con.commit()

sql="update test1 set inventory=%s where goods_numb=%s" #초기 10 -1 한 9값을 재고에서 초기화 하는 부분
cur.execute(sql,(inventory[0], goods[0]))
con.commit()
con.close()
    
