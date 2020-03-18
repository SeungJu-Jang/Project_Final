import pymysql

con = pymysql.connect(host="192.168.0.2", user="root", password="1q2w3e",
                       db='db_1', charset='utf8' )

cur = con.cursor()

sql="select * from employee_list where name='장승주'"
cur.execute(sql)
data=cur.fetchone()
data_use=list(data)
print(data_use)
