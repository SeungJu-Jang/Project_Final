import pymysql

con = pymysql.connect(host="192.168.0.19", user="root", password="1234",db='mydb', charset='utf8')
codenum=['cnb249',1]

cur = con.cursor()
sql='ALTER TABLE pro_info MODIFY inventory int'
cur.execute(sql)

sql="select inventory from pro_info where codenum=%s"
numb=cur.execute(sql,(codenum[0]))
data=[list(data_use) for data_use in cur.fetchall()]
print(data)
for i in range(numb):
    for j in range(0,1):
        inventory=data[i]
        print(inventory)
        if inventory[0]-codenum[1]>=0:
            inventory[0]-=codenum[1] #바코드 스캔시 감소되게 처리
        else:
            print("재고 처리가 반영되지 않았습니다.")
            
print(inventory[0])
con.commit()

sql="update pro_info set inventory=%s where codenum=%s" #초기 10 -1 한 9값을 재고에서 초기화 하는 부분
cur.execute(sql,(inventory[0], codenum[0]))
con.commit()

sql='ALTER TABLE pro_info MODIFY inventory varchar(20)'
cur.execute(sql)
con.commit()
con.close()
