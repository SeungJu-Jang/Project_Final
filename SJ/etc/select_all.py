import pymysql

con = pymysql.connect(host="192.168.0.19", user="erum", password="1234",db='mydb', charset='utf8')

cur = con.cursor()

cur.execute("desc pro_info")
print([column[0] for column in cur.fetchall()])

#sql='select idproducts from timetable where date1=%s'

for i in range(num_goods):
    for j in range(num_sell):
        if goods_li[i]==sell_li[j]:
            cnt+=1
            
    sql="select unitprice from pro_info where idproducts=%s"
    num_price=cur.execute(sql,(goods_li[i]))
    price=[column[0] for column in cur.fetchall()]
print(num_price)
#sql=sql="select unitprice from pro_info where idproducts=%s"
#num=cur.execute(sql)

#num=cur.execute(sql,(date))
print(num)
row=cur.fetchall()
for i in range(num):
    print(row[i])

#sql='select codenum from pro_info where id
