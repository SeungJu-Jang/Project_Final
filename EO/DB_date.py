# -*- coding: utf-8 -*-
import pymysql
import time

con = pymysql.connect(host="192.168.0.19", user="root", password="1234",db='mydb', charset='utf8')

cur = con.cursor()

#파이썬 날짜 함수
inner = time.strftime('%Y-%m-%d', time.localtime(time.time()))

'''
ex날짜/샴푸 비누 이런거
13일   1
13일       1
14일            1
'''
cur = con.cursor()

#sql="update timetable set idproducts=%s where date1=%s"

sql="INSERT INTO timetable(date1, idproducts) VALUES(%s, %s)"

'''
insert 구문 수정 해서
if 찍힌 상품(data_li[0]) == 1 or 2, 3 이면 샴푸, 비누... 이런식으로 선택해서 들어가게
'''
cur.execute(sql,(inner, 1))

con.commit()
con.close()