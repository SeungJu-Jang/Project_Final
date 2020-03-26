#-*- coding:utf-8 -*-
import pymysql
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm


con = pymysql.connect(host="192.168.0.19", user="root", password="1234",db='mydb', charset='utf8')


path = 'C:/Windows/Fonts/malgun.ttf'

font_name = fm.FontProperties(fname=path, size=50).get_name()

plt.rc('font', family=font_name)



cur = con.cursor()

sql='select date1 from graph'
num_day=cur.execute(sql)
plot_day=[column[0] for column in cur.fetchall()]

sql='select price from graph'
num_goods=cur.execute(sql)
plot_day_price=[column[0] for column in cur.fetchall()]

week=str(plot_day_price)

x = plot_day
y = plot_day_price

plt.bar(x,y, align='center', color ='#0a326f')

plt.xlabel('주간 총 매출 : ' '원', fontsize=15, color ='#0a326f')
plt.ylabel('판매량')
#set.axisbelow(True)
#plt.ylabel.grid(True, color='#0a326f', linestyle='dash', linewidth=0.5)
plt.title('주간 매출', fontsize = 30,color ='#0a326f')
plt.savefig('we_test.png', format='png', dpi=150)
plt.show()
