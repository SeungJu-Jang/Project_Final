import pymysql

con = pymysql.connect(host="192.168.0.19", user="root", password="1234",db='mydb', charset='utf8')

cur = con.cursor()
print("원하는 날짜를 입력 하시오 예) 2020-03-24")
date=str(input())

sales_sum=0

sql='select idproducts from pro_info'
num_limit=cur.execute(sql)
print(num_limit)

first_goods=[data[0] for data in cur.fetchall()]
want_goods=first_goods[0]

sql='select idproducts from timetable where date1=%s'
num=cur.execute(sql,(date))
goods_li=[data[0] for data in cur.fetchall()]
print(goods_li)

while first_goods<want_goods+num_limit-1:
    cnt=0
    for i in range(num):
        if goods_li[i]==want_goods:
            cnt+=1
    sql="select unitprice from pro_info where idproducts=%s"
    num_price=cur.execute(sql,(want_goods))
    price=[column[0] for column in cur.fetchall()]
    sales=int(price[0])*cnt
    print("{0}번 상품 판매금액: {1}".format(want_goods,sales))
    print(cnt)
    sales_sum+=sales
    if want_goods!=first_goods[0]+num_limit-1:
        want_goods+=1
    else:
        break
print("{0} 판매총액 : {1}".format(date, sales_sum))

    
