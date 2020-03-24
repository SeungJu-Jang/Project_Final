import pymysql

con = pymysql.connect(host="192.168.0.19", user="root", password="1234",db='mydb', charset='utf8')

cur = con.cursor()

sql='INSERT INTO pro_info(brand, model, codenum, unitprice, inventory) VALUES (%s, %s, %s, %s, %s)'
print("추가할 상품의 브랜드 명을 입력 하시오")
brand=str(input())
print("추가할 상품의 모델을 입력 하시오")
model=str(input())
print("추가할 상품의 코드명을 입력 하시오")
codenum=str(input())
print("추가할 상품의 가격을 입력 하시오")
unitprice=str(input())
print("추가할 상품의 재고량을 입력 하시오")
inventory=str(input())
cur.execute(sql,(brand,model,codenum,unitprice,inventory))
con.commit()

