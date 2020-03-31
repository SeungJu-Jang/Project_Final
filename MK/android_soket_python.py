import sys
import socket
import threading
import pymysql
import time


HOST = ''
PORT = 8000

s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
print('Socket created')
try:
    s.bind((HOST, PORT))
except scoket.error as msg:
    print('Bind Failed. Error code : ' + str(msg[0]) + ' Message: ' + msg[1])

print('Bind success')
s.listen(10)
print('Socket now listening')
flag = 0

con = pymysql.connect(host="192.168.0.19", user="root",
                      password="1234", db="mydb", charset="utf8", autocommit=True)


while True:
    conn, addr = s.accept()
    curs = con.cursor()    
    if flag == 0:
        print(str(addr) + ' - Connection.')

    sys.stdout.flush()
    data = conn.recv(4096).decode('utf8')

    print('\nReceive Data => ' + data)
    
    data=data.strip()

##로그인 [login]
    if data == "login":
        print("data == login")
        conn.send(str("0\n").encode('utf_8'))
        print("send ok 0")

        sys.stdout.flush()
        
        data100 = conn.recv(1024).decode('utf8')
        data100 = data100.strip()
        print(data100)
        
        if data100 is not None:
            print("data100 = " + data100)

            input_id = data100.split(' ')[0]
            input_pw = data100.split(' ')[2]

            print(input_id)
            print(input_pw)

            sql = "SELECT pw FROM user_info WHERE id = %s"
            num = curs.execute(sql,(input_id))
            fetch_data = curs.fetchone()
            try:
                for j in range(0, num):
                    for i in range(0, 2):
                        data_pw = fetch_data[j]
                    print("비밀번호"+data_pw)
                    print("입력된 비밀번호"+input_pw)

                if data_pw.strip() == input_pw.strip():
                    print("로그인 성공")
                    
                    sql_pos = "SELECT position FROM user_info WHERE id = %s"
                    num_pos = curs.execute(sql_pos,(input_id))
                    cur_pos = curs.fetchone()

                    for a in range(0, num_pos):
                        for b in range(0, 2):
                            data_pos = cur_pos[a]
                    print("직책"+data_pos)
                    if data_pos == 'manager' or data_pos == 'super':
                        conn.send(str("1\n").encode('utf_8'))
                        
                    elif data_pos == 'employee':
                        conn.send(str("2\n").encode('utf_8'))
                        
                else:
                    print("로그인 실패! 비밀번호를 다시 확인해 주세요")
                    conn.send(str("3\n").encode('utf_8'))
            except:
                print("로그인 실패! 아이디를 다시 확인해 주세요")
                conn.send(str("4\n").encode('utf_8'))

## 직원정보 조회(사용자 수) [user]
    if data == "user":
        print("data == user")
 
        sql = "select iduser from user_info"
        usernum = curs.execute(sql)

        str_usernum = str(usernum)
        conn.send(str(str_usernum+'\n').encode('utf_8'))
        print("num : %s" %usernum)

        data4 = conn.recv(1024).decode('utf8')
        data4 = data4.strip()

## 직원 정보 조회(정보) [send]
        if data4 == "send":
            print("data4 == send")

            for a in range(0,usernum):
                userid = curs.fetchone()
                for arow in userid:
                    str_arow = (str(arow)+'\n')
                    conn.send(str(str_arow).encode('utf_8'))
                    time.sleep(0.1)
                    print(str_arow+'---')

            sql2 = "select position from user_info"
            usernum2 = curs.execute(sql2)
        
            for b in range(0,usernum2):
                userpos = curs.fetchone()
                for brow in userpos:
                    str_brow = (str(brow)+'\n')
                    conn.send(str(str_brow).encode('utf_8'))
                    time.sleep(0.1)
                    print(str_brow+'---')

            sql3 = "select name from user_info"
            usernum3 = curs.execute(sql3)
            
            for c in range(0,usernum3):
                rows3 = curs.fetchone()
                for crow in rows3:
                    str_crow = (str(crow)+'\n')
                    conn.send(str(str_crow).encode('utf_8'))
                    time.sleep(0.1)
                    print(str_crow+'---')

            sql4 = "select id from user_info"
            usernum4 = curs.execute(sql4)
            
            for d in range(0,usernum4):
                rows4 = curs.fetchone()
                for drow in rows4:
                    str_drow = (str(drow)+'\n')
                    conn.send(str(str_drow).encode('utf_8'))
                    time.sleep(0.1)
                    print(str_drow+'---')

                    
##최근 상품 정보 [goods]
    if data == "goods":
        print("data == goods")
        conn.send(str("0\n").encode('utf8'))
        print("send 0 success")
        
        
        sql = "SELECT idproducts FROM timetable ORDER BY idtime DESC LIMIT 1"
        idx = curs.execute(sql)
        data = curs.fetchone()
        
        for i in range(0,idx):
            datalist = data[i]
            print(datalist)
        
        
        sql2 = "SELECT brand FROM pro_info WHERE idproducts = %s"
        idx2 = curs.execute(sql2,datalist)
        data2 = curs.fetchone()

        for b in range(0,idx2):
            datalist2 = data2[b]
            print(datalist2)
            conn.send(str(datalist2+'\n').encode('utf8'))
            time.sleep(0.1)

        sql3 = "SELECT model FROM pro_info WHERE idproducts = %s"
        idx3 = curs.execute(sql3,datalist)
        data3 = curs.fetchone()

        for c in range(0,idx3):
            datalist3 = data3[c]
            print(datalist3)
            conn.send(str(datalist3+'\n').encode('utf8'))
            time.sleep(0.1)


        sql4 = "SELECT codenum FROM pro_info WHERE idproducts = %s"
        idx4 = curs.execute(sql4,datalist)
        data4 = curs.fetchone()

        for d in range(0,idx4):
            datalist4 = data4[d]
            print(datalist4)
            conn.send(str(datalist4+'\n').encode('utf8'))
            time.sleep(0.1)

        sql5 = "SELECT unitprice FROM pro_info WHERE idproducts = %s"
        idx5 = curs.execute(sql5,datalist)
        data5 = curs.fetchone()

        for e in range(0,idx5):
            datalist5 = data5[b]
            print(datalist5)
            conn.send(str(datalist5+'\n').encode('utf8'))
            time.sleep(0.1)
            
        sql6 = "SELECT inventory FROM pro_info WHERE idproducts = %s"
        idx6 = curs.execute(sql6,datalist)
        data6 = curs.fetchone()

        for f in range(0,idx6):
            datalist6 = data6[b]
            print(datalist6)

            datalist6 = str(datalist6)
            
            conn.send(str(datalist6+'\n').encode('utf8'))
            time.sleep(0.1)


##재고 조회 (개수) [check]
    if data == "check":
        print("data == check")

        sqlnum = "select * from pro_info"
        pronum = curs.execute(sqlnum)

        str_pronum = str(pronum)
        conn.send(str(str_pronum+'\n').encode('utf_8'))
        time.sleep(0.1)
        print("num : %s" %pronum)

        data7 = conn.recv(1024).decode('utf8')
        data7 = data7.strip()

    ## 재고 조회(정보) [ok]
        if data7 == "ok":
            print("data4 == ok")

            sql = "SELECT brand FROM pro_info"
            idx = curs.execute(sql)
            
            for i in range(0,idx):
                pro_brand = curs.fetchone()
                for row_brand in pro_brand:
                    print(row_brand)
                    conn.send(str(row_brand+'\n').encode('utf8'))
                    time.sleep(0.1)

            sql1 = "SELECT codenum FROM pro_info"
            idx1 = curs.execute(sql1)

            for i in range(0,idx1):
                pro_code = curs.fetchone()
                for row_code in pro_code:
                    print(row_code)
                    conn.send(str(row_code+'\n').encode('utf8'))
                    time.sleep(0.1)
            
            
            sql2 = "SELECT model FROM pro_info"
            idx2 = curs.execute(sql2)

            for i in range(0,idx2):
                pro_model = curs.fetchone()
                for row_model in pro_model:
                    print(row_model)
                    conn.send(str(row_model+'\n').encode('utf8'))
                    time.sleep(0.1)

            sql3 = "SELECT shipment FROM pro_info"
            idx3 = curs.execute(sql3)

            for i in range(0,idx3):
                pro_shipment = curs.fetchone()
                for row_shipment in pro_shipment:
                    print(row_shipment)
                    str_row_shipment = str(row_shipment)
                    conn.send(str(str_row_shipment+'\n').encode('utf8'))
                    time.sleep(0.1)

            sql4 = "SELECT inventory FROM pro_info"
            idx4 = curs.execute(sql4)

            for i in range(0,idx4):
                pro_inven = curs.fetchone()
                for row_inven in pro_inven:
                    print(row_inven)
                    str_row_inven = str(row_inven)
                    conn.send(str(str_row_inven+'\n').encode('utf8'))
                    time.sleep(0.1)



##상품 삭제 [delete]
    if data == "delete":
        print("data == delete")
        time.sleep(0.1)
        conn.send(str("0\n").encode('utf_8'))
        print("send ok 0")

        sys.stdout.flush()
        
        data1 = conn.recv(1024).decode('utf8')
        print("data1: "+data1)
        data1 = data1.strip()
        
        
        if data1 is not None:
            print(data1)
            
            try:
                sql_del = "DELETE FROM pro_info where codenum = %s"
                idx_del = curs.execute(sql_del,data1)
                fetch_del = curs.fetchall()

                conn.send(str("1\n").encode('utf8'))
                print("success")
            except Exception as e:
                print(e)


##재고 수정 [22]
    if data == "update":
        print("data == update")
        time.sleep(0.1)
        conn.send(str("0\n").encode('utf_8'))
        print("send ok 0")

        sys.stdout.flush()
        
        data1 = conn.recv(1024).decode('utf8')
        print("data1: "+data1)
        data1 = data1.strip()
        
        
        if data1 is not None:
            print(data1)

            inven_code,inven_update = data1.split('-')
            print(inven_code, inven_update)
            inven_update = int(inven_update)
        
            sql_update = "UPDATE pro_info SET inventory = %s WHERE codenum = %s"
            idx_update = curs.execute(sql_update,(inven_update,inven_code))
            fetch_update = curs.fetchall()

            conn.send(str("1\n").encode('utf8'))
            print("success")



        
##직원 정보 수정 (아이디 입력) [throwid]
    if data == "throwid":
        print("data == throwid")
        time.sleep(0.1)
        conn.send(str("0\n").encode('utf_8'))
        time.sleep(0.1)
        print("send ok 0")

        sel_id = conn.recv(1024).decode('utf8')
        sel_id = sel_id.strip()

        sql_sel = "SELECT id FROM user_info"
        idx_sel = curs.execute(sql_sel)
        id_list = [data_id[0] for data_id in curs.fetchall()]
        print(id_list)


        try:
            for i in range(0,idx_sel):
                if id_list[i] == sel_id:
                    print("아이디 확인 완료")
                    check = 1
                    break
                else:
                    print("일치하는 아이디 없음")
                    check = 2

            if check == 1:
                time.sleep(0.1)
                conn.send(str("1\n").encode('utf_8'))
                print("send 1")
                
            elif check == 2:
                time.sleep(0.1)
                conn.send(str("2\n").encode('utf_8'))
                print("send 2")
        except Exception as e:
            print(e)
            
##직원 정보 수정 (정보 입력) [repairemp]
    if data == "repairemp":
        print("data == repairemp")
        time.sleep(0.1)
        conn.send(str("0\n").encode('utf_8'))
        print("send ok 0")
        
        input_info = conn.recv(1024).decode('utf8')
        print("input_info: " + input_info)
        input_info = input_info.strip()   

        if input_info is not None:
            update_name, update_pw, update_email = input_info.split('/')
            print(update_name, update_pw, update_email)

            try:            
                sql_update = "UPDATE user_info SET name=%s, pw=%s, email=%s WHERE id = %s"
                idx_update = curs.execute(sql_update,(update_name, update_pw, update_email,sel_id))
                fetch_update = curs.fetchall()

                
                conn.send(str("1\n").encode('utf8'))
                print("회원 정보 수정 완료")
            except Exception as e:
                conn.send(str("2\n").encode('utf_8'))
                print("정보 수정 오류 :" + e)


##상품 추가 [plus]
    if data == "plus":
        print("data == plus")
        time.sleep(0.1)
        conn.send(str("0\n").encode('utf_8'))
        print("send ok 0")

        sys.stdout.flush()
        
        data1 = conn.recv(1024).decode('utf8')
        print("data1: "+data1)
        data1 = data1.strip()
        
        
        if data1 is not None:
            print(data1)

            new_brand,new_model,new_code,new_price,new_inven = data1.split('/')
            print(new_brand,new_model,new_code,new_price,new_inven)

            new_price = int(new_price)
            new_inven = int(new_inven)

            sql_add = "INSERT INTO pro_info(brand,model,codenum,unitprice,inventory) VALUES (%s, %s, %s, %s, %s)"
            idx_add = curs.execute(sql_add,(new_brand,new_model,new_code,new_price,new_inven))
            fetch_add = curs.fetchall()

            conn.send(str("1\n").encode('utf8'))
            print("success")

##매출 확인 조회 버튼
    if data == "money":
        print("data == money")

        sql = "SELECT idproducts FROM pro_info"
        idx = curs.execute(sql)
        keylist = [data[0] for data in curs.fetchall()]

        str_idx = str(idx)
        time.sleep(0.1)
        conn.send(str(str_idx+'\n').encode('utf8'))
        print("send : " + str_idx + " ok")

        data52 = conn.recv(1024).decode('utf8')
        data52 = data52.strip()
    ##총 매출 정보 전송
        if data52 == "take":              
            print("data52 == take")
            time.sleep(0.1)
            conn.send(str('0\n').encode('utf8'))

            date = conn.recv(1024).decode('utf8')
            date = date.strip()

            if date is not None:
                print(date)
                cnt=0
                sales_sum=0
                sql1 = "SELECT codenum FROM pro_info"
                idx1 = curs.execute(sql1)
                
                for i in range(0,idx1):
                    pro_code = curs.fetchone()
                    for row_code in pro_code:
                        str_row_code = str(row_code)
                        time.sleep(0.1)
                        conn.send(str(str_row_code+'\n').encode('utf8'))
                        print(row_code)            

                sql2 = "SELECT model FROM pro_info"
                idx2 = curs.execute(sql2)

                for i in range(0,idx2):
                    pro_model = curs.fetchone()
                    for row_model in pro_model:
                        time.sleep(0.1)
                        conn.send(str(row_model+'\n').encode('utf8'))
                        print(row_model)


                sql3 = "select idproducts from timetable where date1=%s"
                num_sell=curs.execute(sql3,(date))
                salelist = [data[0] for data in curs.fetchall()]

                for i in range(0,idx):
                    for j in range(num_sell):
                        if keylist[i]==salelist[j]:
                            cnt+=1
                            
                    sql4="select unitprice from pro_info where idproducts=%s"
                    curs.execute(sql4,(keylist[i]))
                    price=[column[0] for column in curs.fetchall()]

                    sales=int(price[0])*cnt
                    str_sales = str(sales)
                    time.sleep(0.13)
                    conn.send(str(str_sales+'\n').encode('utf8'))
                    print(sales)
                    cnt=0

                    sales_sum+=sales
                    
                data53 = conn.recv(1024).decode('utf8')
                data53 = data53.strip()

                if data53 == "give":
                    print(data53)
                    day_total=sales_sum
                    str_day_total = str(day_total)
                    time.sleep(0.13)
                    conn.send(str(str_day_total+'\n').encode('utf8'))
                    print(day_total)




        
    if not data:
        print("It's unuseable Data!")
        flag = 0

    flag = 1
    
