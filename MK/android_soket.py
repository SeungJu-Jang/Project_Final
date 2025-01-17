import sys
import socket
import threading
import pymysql
import time

HOST = ''
PORT = 8000

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
print('Socket created')
try:
    s.bind((HOST, PORT))
except socket.error as msg:
    print('Bind Failed. Error code : ' + str(msg[0]) + ' Message: ' + msg[1])

print('Bind success')
s.listen(10)
print('Socket now listening')
flag = 0

user_data = None
sel_code = None
mod_inven = None
login_data = None
add_data = None
total_data = None
sel_date_sales = None
data_sales = None

con = pymysql.connect(host="192.168.0.19", user="root",
                      password="1234", db="mydb", charset="utf8", autocommit=True)

while True:
    conn, addr = s.accept()
    curs = con.cursor()
    if flag == 0:
        print(str(addr) + ' - Connection.')

    data = None
    # sys.stdout.flush()

    data = conn.recv(4096).decode('utf8')
    print('\nReceive Data => ' + data)

    data = data.strip()

    ##로그인 [login]
    if data == "login":
        print("data == login")
        conn.send(str("0\n").encode('utf_8'))
        print("send ok 0")

        sys.stdout.flush()

        login_data = conn.recv(1024).decode('utf8')
        login_data = login_data.strip()

        if login_data is not None:
            print("login_data = " + login_data)

            login_id = None
            login_pw = None

            login_id, login_pw = login_data.split('-')

            print(login_id)
            print(login_pw)

            sql_login = "SELECT pw FROM user_info WHERE id = %s"
            idx_login = curs.execute(sql_login, (login_id))
            fetch_login = curs.fetchone()
            try:
                for j in range(0, idx_login):
                    for i in range(0, 2):
                        data_pw = fetch_login[j]
                    print("비밀번호" + data_pw)
                    print("입력된 비밀번호" + login_pw)

                if data_pw.strip() == login_pw.strip():
                    print("로그인 성공")

                    sql_pos = "SELECT position FROM user_info WHERE id = %s"
                    num_pos = curs.execute(sql_pos, (login_id))
                    cur_pos = curs.fetchone()

                    for a in range(0, num_pos):
                        for b in range(0, 2):
                            data_pos = cur_pos[a]

                    print("직책" + data_pos)
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

    ## 직원정보 조회(사용자 수 전달) [user]
    if data == "user":
        print("data == user")

        sql = "select iduser from user_info"
        usernum = curs.execute(sql)

        str_usernum = str(usernum)
        conn.send(str(str_usernum + '\n').encode('utf_8'))
        print("num : %s" % usernum)

        user_data = None
        user_data = conn.recv(1024).decode('utf8')
        user_data = user_data.strip()

        ## 직원정보 조회(정보) [send]
        if user_data == "send":
            print("user_data == send")

            for a in range(0, usernum):
                userid = curs.fetchone()
                for arow in userid:
                    str_arow = (str(arow) + '\n')
                    conn.send(str(str_arow).encode('utf_8'))
                    time.sleep(0.05)
                    print(str_arow)

            sql2 = "select position from user_info"
            usernum2 = curs.execute(sql2)

            for b in range(0, usernum2):
                userpos = curs.fetchone()
                for brow in userpos:
                    str_brow = (str(brow) + '\n')
                    conn.send(str(str_brow).encode('utf_8'))
                    time.sleep(0.1)
                    print(str_brow)

            sql3 = "select name from user_info"
            usernum3 = curs.execute(sql3)

            for c in range(0, usernum3):
                rows3 = curs.fetchone()
                for crow in rows3:
                    str_crow = (str(crow) + '\n')
                    conn.send(str(str_crow).encode('utf_8'))
                    time.sleep(0.1)
                    print(str_crow)

            sql4 = "select id from user_info"
            usernum4 = curs.execute(sql4)

            for d in range(0, usernum4):
                rows4 = curs.fetchone()
                for drow in rows4:
                    str_drow = (str(drow) + '\n')
                    conn.send(str(str_drow).encode('utf_8'))
                    time.sleep(0.1)
                    print(str_drow)


    ##최근 상품 정보 [goods]
    if data == "goods":
        print("data == goods")
        time.sleep(0.1)
        conn.send(str("0\n").encode('utf8'))
        print("send 0 success")

        sql_limit = "SELECT idproducts FROM timetable ORDER BY idtime DESC LIMIT 1"
        idx_limit = curs.execute(sql_limit)
        fetch_limit = curs.fetchone()

        for a in range(0, idx_limit):
            idproducts_list = fetch_limit[a]
            print(idproducts_list)

        sql_brand_limit = "SELECT brand FROM pro_info WHERE idproducts = %s"
        idx_brand_limit = curs.execute(sql_brand_limit, idproducts_list)
        fetch_brand_limit = curs.fetchone()

        for b in range(0, idx_brand_limit):
            brand_list_limit = fetch_brand_limit[b]
            print(brand_list_limit)
            conn.send(str(brand_list_limit + '\n').encode('utf8'))
            time.sleep(0.07)

        sql_model_limit = "SELECT model FROM pro_info WHERE idproducts = %s"
        idx_model_limit = curs.execute(sql_model_limit, idproducts_list)
        data_model_limit = curs.fetchone()

        for c in range(0, idx_model_limit):
            model_list_limit = data_model_limit[c]
            print(model_list_limit)
            conn.send(str(model_list_limit + '\n').encode('utf8'))
            time.sleep(0.07)

        sql_codenum_limit = "SELECT codenum FROM pro_info WHERE idproducts = %s"
        idx_codenum_limit = curs.execute(sql_codenum_limit, idproducts_list)
        fetch_codenum_limit = curs.fetchone()

        for d in range(0, idx_codenum_limit):
            codenum_list_limit = fetch_codenum_limit[d]
            print(codenum_list_limit)
            conn.send(str(codenum_list_limit + '\n').encode('utf8'))
            time.sleep(0.07)

        sql_unitprice_limit = "SELECT unitprice FROM pro_info WHERE idproducts = %s"
        idx_unitprice_limit = curs.execute(sql_unitprice_limit, idproducts_list)
        fetch_unitprice_limit = curs.fetchone()

        for e in range(0, idx_unitprice_limit):
            unitprice_list_limit = fetch_unitprice_limit[b]
            print(unitprice_list_limit)
            conn.send(str(unitprice_list_limit + '\n').encode('utf8'))
            time.sleep(0.07)

        sql_inven_limit = "SELECT inventory FROM pro_info WHERE idproducts = %s"
        idx_inven_limit = curs.execute(sql_inven_limit, idproducts_list)
        fetch_inven_limit = curs.fetchone()

        for f in range(0, idx_inven_limit):
            inven_list_limit = fetch_inven_limit[b]
            print(inven_list_limit)
            inven_list_limit = str(inven_list_limit)
            conn.send(str(inven_list_limit + '\n').encode('utf8'))
            time.sleep(0.07)


    ##재고 조회 (개수) [check]
    if data == "check":
        print("data == check")

        try:
            sqlnum = "select * from pro_info"
            pronum = curs.execute(sqlnum)

            str_pronum = str(pronum)
            time.sleep(0.1)
            conn.send(str(str_pronum + '\n').encode('utf_8'))
            print("num : %s" % pronum)

            inven_data = conn.recv(1024).decode('utf8')
            inven_data = inven_data.strip()
        except Exception as e:
            print(e)

        ## 재고 조회(정보) [ok]
        if inven_data == "ok":
            print("inven_data == ok")

            sql_show_brand = "SELECT brand FROM pro_info"
            idx_show_brand = curs.execute(sql_show_brand)

            for i in range(0, idx_show_brand):
                show_brand_fetch = curs.fetchone()
                for row_brand in show_brand_fetch:
                    print(row_brand)
                    time.sleep(0.05)
                    conn.send(str(row_brand + '\n').encode('utf8'))


            sql_show_codenum = "SELECT codenum FROM pro_info"
            idx_show_codenum = curs.execute(sql_show_codenum)

            for i in range(0, idx_show_codenum):
                pro_code = curs.fetchone()
                for row_code in pro_code:
                    print(row_code)
                    time.sleep(0.05)
                    conn.send(str(row_code + '\n').encode('utf8'))


            sql_show_model = "SELECT model FROM pro_info"
            idx_show_model = curs.execute(sql_show_model)

            for i in range(0, idx_show_model):
                pro_model = curs.fetchone()
                for row_model in pro_model:
                    print(row_model)
                    time.sleep(0.05)
                    conn.send(str(row_model + '\n').encode('utf8'))


            sql_show_ship = "SELECT shipment FROM pro_info"
            idx_show_ship = curs.execute(sql_show_ship)

            for i in range(0, idx_show_ship):
                pro_shipment = curs.fetchone()
                for row_shipment in pro_shipment:
                    print(row_shipment)
                    str_row_shipment = str(row_shipment)
                    time.sleep(0.05)
                    conn.send(str(str_row_shipment + '\n').encode('utf8'))


            sql_show_inven = "SELECT inventory FROM pro_info"
            idx_show_inven = curs.execute(sql_show_inven)

            for i in range(0, idx_show_inven):
                pro_inven = curs.fetchone()
                for row_inven in pro_inven:
                    print(row_inven)
                    str_row_inven = str(row_inven)
                    time.sleep(0.05)
                    conn.send(str(str_row_inven + '\n').encode('utf8'))


    ##상품 삭제 [delete]
    if data == "delete":
        print("data == delete")
        time.sleep(0.1)
        conn.send(str("0\n").encode('utf_8'))
        print("send ok 0")

        sel_code = None
        sys.stdout.flush()

        sel_code = conn.recv(1024).decode('utf8')
        sel_code = sel_code.strip()

        if sel_code is not None:
            print(sel_code)

            sql_code = "SELECT codenum FROM pro_info"
            idx_del = curs.execute(sql_code)
            codenum_list = [data_codenum[0] for data_codenum in curs.fetchall()]
            print(codenum_list)

            try:
                check_del_sel = None
                for i in range(0, idx_del):
                    if codenum_list[i] == sel_code:
                        print("상품 코드 확인 완료")
                        check_del_sel = 1
                        break
                    else:
                        check_del_sel = 2

                if check_del_sel == 1:
                    time.sleep(0.1)
                    conn.send(str("1\n").encode('utf8'))
                    print("send 1")

                    sql_del = "DELETE FROM pro_info where codenum = %s"
                    idx_del = curs.execute(sql_del, sel_code)
                    fetch_del = curs.fetchall()

                    conn.send(str("1\n").encode('utf8'))
                    print("success")
                elif check_del_sel == 2:
                    time.sleep(0.1)
                    conn.send(str("2\n").encode('utf8'))
                    print("send 2")

            except Exception as e:
                print(e)

    ##재고 수정 [update]
    if data == "update":
        print("data == update")
        time.sleep(0.1)
        conn.send(str("0\n").encode('utf_8'))
        print("send ok 0")

        mod_inven = None
        sys.stdout.flush()

        mod_inven = conn.recv(1024).decode('utf8')
        mod_inven = mod_inven.strip()

        if mod_inven is not None:
            print("mod_inven: " + mod_inven)
            try:
                input_code_set, input_inven_set = mod_inven.split('-')
                print("input_code_set" + input_code_set)
                print("input_inven_set" + input_inven_set)

                input_inven_set = int(input_inven_set)
            except Exception as e:
                conn.send(str("3\n").encode('utf8'))
                print("int 값 아님")

            sql_code = "SELECT codenum FROM pro_info"
            idx_del = curs.execute(sql_code)
            codenum_list = [data_codenum[0] for data_codenum in curs.fetchall()]
            print(codenum_list)

            try:
                check_inven = None
                for i in range(0, idx_del):
                    if codenum_list[i] == input_code_set:
                        check_inven = 1
                        print("상품 코드 확인")
                        break
                    else:
                        check_inven = 2
                        print("xxx")

                if check_inven == 1:
                    sql_update = "UPDATE pro_info SET inventory = %s WHERE codenum = %s"
                    idx_update = curs.execute(sql_update, (input_inven_set, input_code_set))
                    fetch_update = curs.fetchall()

                    conn.send(str("1\n").encode('utf8'))
                    print("send 1 : 재고 수정 완료")
                elif check_inven == 2:
                    conn.send(str("2\n").encode('utf8'))
                    print("send 2 : 상품 코드 없음")

            except Exception as e:
                print(e)


    ##개인 정보 수정 (비밀 번호 입력) [throwid]
    if data == "throwpw":
        print("data == throwpw")
        time.sleep(0.1)
        conn.send(str("0\n").encode('utf_8'))
        print("send ok 0")

        mod_info_pw = None
        mod_info_pw = conn.recv(1024).decode('utf8')
        mod_info_pw = mod_info_pw.strip()

        if mod_info_pw == login_pw:
            time.sleep(0.1)
            conn.send(str("1\n").encode('utf_8'))
            print("send 1 : 비밀번호 일치")
        else:
            time.sleep(0.1)
            conn.send(str("2\n").encode('utf_8'))
            print("send 2 : 비밀번호 일치하지 않음")

    ##직원 정보 수정 (정보 입력) [repairemp]
    if data == "repairemp":
        print("data == repairemp")
        time.sleep(0.1)
        conn.send(str("0\n").encode('utf_8'))
        print("send ok 0")

        input_info = None
        input_info = conn.recv(1024).decode('utf8')
        print("input_info: " + input_info)
        input_info = input_info.strip()

        if input_info is not None:
            try:
                update_name, update_pw, update_email = input_info.split('/')
                print(update_name, update_pw, update_email)

                sql_update = "UPDATE user_info SET name=%s, pw=%s, email=%s WHERE id = %s"
                idx_update = curs.execute(sql_update, (update_name, update_pw, update_email, login_id))
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

        add_data = None
        # sys.stdout.flush()

        add_data = conn.recv(1024).decode('utf8')
        print("input_data: " + add_data)
        add_data = add_data.strip()

        if add_data is not None:
            print("split data: " + add_data)

            try:
                new_brand, new_model, new_code, new_price, new_inven = add_data.split('/')
                print(new_brand, new_model, new_code, new_price, new_inven)

                new_price = int(new_price)
                new_inven = int(new_inven)

                sql_add = "INSERT INTO pro_info(brand,model,codenum,unitprice,inventory) VALUES (%s, %s, %s, %s, %s)"
                idx_add = curs.execute(sql_add, (new_brand, new_model, new_code, new_price, new_inven))
                fetch_add = curs.fetchall()

                time.sleep(0.1)
                conn.send(str("1\n").encode('utf8'))
                print("상품 추가 성공")

            except Exception as e:
                time.sleep(0.1)
                conn.send(str("2\n").encode('utf8'))
                print(e)


    ##매출 확인 조회 버튼
    if data == "money":
        try:
            print("data == money")

            sql_idpro = "SELECT idproducts FROM pro_info"
            idx_idpro = curs.execute(sql_idpro)
            keylist = [data[0] for data in curs.fetchall()]

            str_idx_idpro = str(idx_idpro)
            time.sleep(0.1)
            conn.send(str(str_idx_idpro + '\n').encode('utf8'))
            print("send " + str_idx_idpro + " ok")

            data_sales = None
            data_sales = conn.recv(1024).decode('utf8')
            data_sales = data_sales.strip()
        except Exception as e:
            print(e)


        ##총 매출 정보 전송
        if data_sales == "take":
            try:
                print("data_sales == take")
                time.sleep(0.1)
                conn.send(str('0\n').encode('utf8'))

                sel_date_sales = None
                sel_date_sales = conn.recv(1024).decode('utf8')
                sel_date_sales = sel_date_sales.strip()
            except Exception as e:
                print(e)

            if sel_date_sales is not None:
                print(sel_date_sales)
                cnt = 0
                sales_sum = 0
                sql_codenum_sales = "SELECT codenum FROM pro_info"
                idx_codenum_sales = curs.execute(sql_codenum_sales)

                for i in range(0, idx_codenum_sales):
                    pro_code = curs.fetchone()
                    for row_code in pro_code:
                        str_row_code = str(row_code)
                        time.sleep(0.05)
                        conn.send(str(str_row_code + '\n').encode('utf8'))
                        print(row_code)

                sql_model_sales = "SELECT model FROM pro_info"
                idx_model_sales = curs.execute(sql_model_sales)

                for i in range(0, idx_model_sales):
                    pro_model = curs.fetchone()
                    for row_model in pro_model:
                        time.sleep(0.05)
                        conn.send(str(row_model + '\n').encode('utf8'))
                        print(row_model)

                sql_date_idpro = "select idproducts from timetable where date1=%s"
                num_sell = curs.execute(sql_date_idpro, (sel_date_sales))
                salelist = [data[0] for data in curs.fetchall()]

                for i in range(0, idx_idpro):
                    for j in range(num_sell):
                        if keylist[i] == salelist[j]:
                            cnt += 1

                    sql4 = "select unitprice from pro_info where idproducts=%s"
                    curs.execute(sql4, (keylist[i]))
                    price = [column[0] for column in curs.fetchall()]

                    sales = int(price[0]) * cnt
                    str_sales = str(sales)
                    time.sleep(0.05)
                    conn.send(str(str_sales + '\n').encode('utf8'))
                    print(sales)
                    cnt = 0

                    sales_sum += sales

                total_data = conn.recv(1024).decode('utf8')
                total_data = total_data.strip()

                if total_data == "give":
                    try:
                        print(total_data)
                        day_total = sales_sum
                        str_day_total = str(day_total)
                        time.sleep(0.05)
                        conn.send(str(str_day_total + '\n').encode('utf8'))
                        print(day_total)
                    except Exception as e:
                        print(e)

    if not data:
        print("It's unuseable Data!")
        flag = 0
