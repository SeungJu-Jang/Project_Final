import pymysql
a=[]

con = pymysql.connect(host="192.168.0.19", user="root", password="1234",db='mydb', charset='utf8')

cur = con.cursor()
#sql='ALTER TABLE pro_info DROP COLUMN sale_amount'
#sql='SELECT DISTINCT date1 FROM timetable'
#sql='alter table timetable modify date1 int'
sql='ALTER TABLE pro_info MODIFY inventory varchar(20)'
cur.execute(sql)
num=cur.execute(sql)
row=cur.fetchall()
for i in range(num):
    a.append(row[i])
    print(a)
con.commit()


