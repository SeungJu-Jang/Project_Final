import pymysql

con = pymysql.connect(host="192.168.0.2", user="root", password="1q2w3e",
                       db='db_1', charset='utf8' )

cur = con.cursor()
print("재고 최신화를 할 상품번호 입력")
goods=int(input()) # 1번은 샴푸 2번은 린스 등 일경우
print("감소할 재고의 량 입력 QR 에서는 무조건 1이겠죠?!")
num=int(input()) #qr 코드에서는 찍어서 나온값을 num에 넣어주세요!


sql="select inventory from test1 where goods_numb=%s"
numb=cur.execute(sql,(goods))
data=[list(data_use) for data_use in cur.fetchall()]
for j in range(numb):
    for i in range(0,1):
        inventory=data[j]
    inventory[0]-=num #바코드 스캔시 감소되게 처리
print(inventory[0])

sql="update test1 set inventory=%s where goods_numb=%s" #초기 10 -1 한 9값을 재고에서 초기화 하는 부분
cur.execute(sql,(inventory[0], goods))
con.commit()
con.close()
    
