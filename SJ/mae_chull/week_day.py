import pymysql
import matplotlib.pyplot as plt

con = pymysql.connect(host="192.168.0.19", user="root", password="1234",db='mydb', charset='utf8')

cur = con.cursor()

sql='select date1 from graph'
num_day=cur.execute(sql)
plot_day=[column[0] for column in cur.fetchall()]

sql='select price from graph'
num_goods=cur.execute(sql)
plot_day_price=[column[0] for column in cur.fetchall()]


x = plot_day
y = plot_day_price

plt.bar(x,y, align='center', color ='#0a326f')

plt.xlabel('goods_number')
plt.ylabel('sales rate')
plt.title('weeks')
plt.savefig('we_test.png', format='png', dpi=150)
plt.show()
