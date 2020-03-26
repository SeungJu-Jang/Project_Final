import pymysql
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm

con = pymysql.connect(host="192.168.0.19", user="root", password="1234",db='mydb', charset='utf8')

fm.get_fontconfig_fonts()
font_location = 'C:/Windows/Fonts/malgun.ttf'
#font_location = 'C:/Users/JSJ_Note_Book/Documents/카카오톡 받은 파일/namsan.ttf'

font_name= fm.FontProperties(fname=font_location).get_name()
plt.rc('font', family=font_name)

cur = con.cursor()
print("원하는 날짜를 입력 하시오 예) 2020-03-24")
date=str(input())
cnt=0

sales_sum=0
plot_cnt=[]

sql='select idproducts from pro_info'
num_goods=cur.execute(sql)
goods_li=[data[0] for data in cur.fetchall()]
#print(goods_li)

#plot 차트 X 축 상품 모델명
sql='select model from pro_info'
num_price=cur.execute(sql)
plot_model=[column[0] for column in cur.fetchall()]
print(plot_model)


sql='select idproducts from timetable where date1=%s'
num_sell=cur.execute(sql,(date))
sell_li=[data[0] for data in cur.fetchall()]
#print(num_sell)
#print(sell_li)

#2중 for문을 통한 데이터 카운트
for i in range(num_goods):
    for j in range(num_sell):
        if goods_li[i]==sell_li[j]:
            cnt+=1
            
    sql="select unitprice from pro_info where idproducts=%s"
    num_price=cur.execute(sql,(goods_li[i]))
    price=[column[0] for column in cur.fetchall()]
    
    sales=int(price[0])*cnt
    print("{0}번 상품 판매금액: {1}".format(goods_li[i],sales))
    plot_cnt.append(cnt)
    cnt=0
    #plot_price.append(cnt*price[0])
    #print(plot_price)
    sales_sum+=sales
day_total=sales_sum
print("{0} 날짜 매출 : {1}".format(date,day_total))

#plot 그리기

day=str(day_total)
x = plot_model
y = plot_cnt

plt.bar(x,y, align='center', color ='#0a326f')

plt.xlabel('금일 총 매출 : ' + day + '원', fontsize=15, color ='#0a326f')
plt.ylabel('판매량')
plt.title(date +'일 매출', fontsize = 30,color ='#0a326f')
plt.savefig('da_test.png', format='png', dpi=150)
plt.show()


# graph 테이블 데이터 입력
#sql='insert into graph (date1, price) values (%s, %s)'
#cur.execute(sql,(date,day_total))
#con.commit()
