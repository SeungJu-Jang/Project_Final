import pymysql

con = pymysql.connect(host="192.168.0.2", user="root", password="1q2w3e",
                       db='db_1', charset='utf8' )

print("아이디를 입력하시오")
user_id=input()
print("비밀번호를 입력 하시오")
user_pw=input()
cur = con.cursor()
print("4를 입력하면 직원조회를 합니다")
numb=int(input())
if numb==4:
    try:
        sql="select position, pw from employee_list where i_d=%s"
        num=cur.execute(sql,(user_id))
        data=[list(data_use) for data_use in cur.fetchall()]
        for j in range(0,num):
            for i in range(0,2):
                data_employee=data[j]
        if data_employee[1]==user_pw:
            print("로그인 성공")
            print(data_employee[0])
        else:
            print("로그인 실패 ID와 비밀번호를 다시 확인해 주세요")
    except:
        print("로그인 실패 ID와 비밀번호를 다시 확인해 주세요")
else:
    print("4이외의 숫자가 입력되었습니다")
            


