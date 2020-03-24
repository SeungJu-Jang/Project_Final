# -*- coding: utf-8 -*-
import pymysql
import time



con = pymysql.connect(host="192.168.0.19", user="root", password="1234",db='mydb', charset='utf8')

cur = con.cursor()

while True:
    print("판매량 확인이 필요한 품목의 번호를 입력하세요")
    goods_num=int(input())
    if goods_num==1:
        sql="select unitprice from pro_info where idproducts=%s"
        numm=cur.execute(sql,(goods_num))
        price=[list(price_data) for price_data in cur.fetchall()]
        price_re=int(price[0][0])
        sql="select out_goods from timetable where idproducts=%s  "
        num=cur.execute(sql,(goods_num))
        con.commit()
        print(price_re*num)
        continue
    if goods_num==2:
        sql="select out_goods from timetable where idproducts=%s  "
        num=cur.execute(sql,(goods_num))
        con.commit()
        print(num*goods_price_2)
        continue
    if goods_num==3:
        sql="select out_goods from timetable where idproducts=%s  "
        num=cur.execute(sql,(goods_num))
        con.commit()
        print(num*goods_price_3)
        continue
    if goods_num==4:
        sql="select out_goods from timetable where idproducts=%s  "
        num=cur.execute(sql,(goods_num))
        con.commit()
        print(num*goods_price_4)
        continue
    if goods_num==5:
        sql="select out_goods from timetable where idproducts=%s  "
        num=cur.execute(sql,(goods_num))
        con.commit()
        print(num*goods_price_5)
        continue
    else:
        print("해당 상품이 없습니다.")





    
#파이썬 날짜 함수
"""inner = time.strftime('%Y-%m-%d', time.localtime(time.time()))

cur = con.cursor()

#sql="update timetable set idproducts=%s where date1=%s"



con.commit()
con.close()"""
