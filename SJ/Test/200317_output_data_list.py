import pymysql

con = pymysql.connect(host="192.168.0.2", user="root", password="1q2w3e",
                       db='db_1', charset='utf8' )

cur = con.cursor()
print("4를 입력하면 직원조회를 합니다")
num=int(input())
print(num)
if num==4:
    sql="select * from employee_list"
    num=cur.execute(sql)
    data=cur.fetchall()
    data_use=list(data)
    for i in data:
        print(data_use)
else:
    print("4이외의 숫자가 입력되었습니다")
