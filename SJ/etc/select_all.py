import pymysql

con = pymysql.connect(host="192.168.0.19", user="root", password="1234",db='mydb', charset='utf8')

cur = con.cursor()

cur.execute("desc pro_info")
print([column[0] for column in cur.fetchall()])

sql='select * from pro_info'
num=cur.execute(sql)
row=cur.fetchall()
for i in range(num):
    print(row[i])
