import pymysql

con = pymysql.connect(host="192.168.0.19", user="root", password="1234",db='mydb', charset='utf8')

cur = con.cursor()
#sql='ALTER TABLE pro_info DROP COLUMN sale_amount'
sql='ALTER TABLE pro_info MODIFY inventory varchar(20)'


#sql='alter table timetable modify date1 varchar(20)' 
cur.execute(sql)
con.commit()
con.close()
