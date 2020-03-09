import pymysql

try:
    conn = pymysql.connect(host = '192.168.0.37',
                                       user = 'root', passwd = '1234',
                                       db = 'mydb',charset = 'utf8')
    curs = conn.cursor()


    sql = "SELECT * FROM user"
    curs.execute(sql)

    rows = curs.fetchall()

    for i in rows:
        print(i)

except Exception as e:
    print(e)

finally:
    conn.close()
