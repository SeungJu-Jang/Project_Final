import pymysql

con = pymysql.connect(host="192.168.0.19", user="root", password="1234",db='mydb', charset='utf8')

cur = con.cursor()
print("원하는 날짜를 입력 하시오 예) 2020-03-24")
date=str(input())
print("판매량이 궁금한 상품의 번호를 입력 하시오")
want_goods=int(input())
cnt=0 # 초기값

#cur.execute("desc timetable")
#print([column[0] for column in cur.fetchall()])

sql='select idproducts from timetable where date1=%s'
# sql='delete from timetable where idproducts=1'
num=cur.execute(sql,(date))
goods_li=[data[0] for data in cur.fetchall()]
for i in range(num):
    if goods_li[i]==want_goods:
        cnt+=1
print(cnt)
sql="select unitprice from pro_info where idproducts=%s"
num_price=cur.execute(sql,(want_goods))
price=[column[0] for column in cur.fetchall()]
sales=int(price[0])*cnt
print("{0}번 상품 판매금액: {1}".format(want_goods,sales))
        


    
#con.commit()
#print(data)
#print(data)
#for i in range(num):
    #for j in range(0,1):
        #price=[data[i][j]]
#print(price[1])

    
