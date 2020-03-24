import pymysql

con = pymysql.connect(host="192.168.0.2", user="root", password="1q2w3e",
                       db='db_1', charset='utf8' )
goods=[1,1]

cur = con.cursor()

sql="select goods_numb from test1"
num1=cur.execute(sql)
con.commit

for i in range(num1):
    if goods[0]==i+1:
        sql="select inventory from test1 where goods_numb=%s"
        num2=cur.execute(sql,(goods[0]))
        data=[list(data_use) for data_use in cur.fetchall()]
        for j in range(num2):
            for i in range(0,1):
                inventory=data[j]
                if inventory[0]-goods[1]>=0:
                    inventory[0]-=goods[1] #바코드 스캔시 감소되게 처리
                    socket_tr=inventory[0]
                    print(socket_tr)
                    con.commit()

                    sql="update test1 set inventory=%s where goods_numb=%s" #초기 10 -1 한 9값을 재고에서 초기화 하는 부분
                    cur.execute(sql,(inventory[0], goods[0]))
                    con.commit()
                    con.close()
                else:
                    continue
    else:
        print("{0}번 상품은 아닙니다.".format(i+1))
        continue
        
