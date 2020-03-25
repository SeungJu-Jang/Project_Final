import pymysql

con = pymysql.connect(host="192.168.0.19", user="root", password="1234",db='mydb', charset='utf8')

cur = con.cursor()
print("원하는 날짜를 입력 하시오 예) 2020-03-24")
date=str(input())
cnt=0
sales_sum=0

sql='select idproducts from pro_info'
num_goods=cur.execute(sql)
goods_li=[data[0] for data in cur.fetchall()]
print(goods_li)

sql='select idproducts from timetable where date1=%s'
num_sell=cur.execute(sql,(date))
sell_li=[data[0] for data in cur.fetchall()]
print(sell_li)

for i in range(num_goods):
    for j in range(num_sell):
        if goods_li[i]==sell_li[j]:
            cnt+=1
    print(cnt)
    sql="select unitprice from pro_info where idproducts=%s"
    num_price=cur.execute(sql,(goods_li[i]))
    price=[column[0] for column in cur.fetchall()]
    sales=int(price[0])*cnt
    print("{0}번 상품 판매금액: {1}".format(goods_li[i],sales))
    cnt=0
    sales_sum+=sales
    
day_total=sales_sum
print(day_total)
    
