import pymysql
con = pymysql.connect(host="192.168.0.2", user="user", password="1234" ,db='mydb', charset='utf8')

cur = con.cursor()

cur.execute("desc pro_info")
print([column[0] for column in cur.fetchall()])

#sql='select idproducts from timetable where date1=%s'
#sql=sql="select unitprice from pro_info where idproducts=%s"
sql='select * from pro_info'
#sql='TRUNCATE TABLE graph'
num=cur.execute(sql)
#num=cur.execute(sql,(date))

#print(num)
row=cur.fetchall()
for i in range(num):
    print(row[i])

#sql='select codenum from pro_info where id
