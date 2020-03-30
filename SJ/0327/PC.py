#!/usr/bin/env python
# -*- coding: utf-8 -*-
from typing import List, Any

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
# from PyQt5 import uic
# from PyQt5 import QtWidgets, QtGui
from PyQt5 import QtGui, QtCore
import sys
import socket
import pymysql
import numpy as np
#import server
from PyQt5.QtCore import QTimer, QTime
from threading import Timer, Thread
import time
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm

QApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)



# - 안드로이드 어플에서 송신하는 값 -
# 0번 로그인 요청
# 1번 관리자로 로그인
# 2번 직원으로 로그인
# 3번 로그인 거절
# 4번 회원 조회
# 5번 매출 확인 - 일별 매출
# 6번 매출 확인-  월별 매출
# 7번 재고관리 표
# 8번 재고 관리 - 상품 추가
# 9번 재고 관리 - 재고 수정
# 10번 재고 관리 - 상품 삭제
# 11번 직원 정보 수정
# 12번 상품 정보 확인

# 유저 데이터베이스
HOST = '192.168.0.2'
# HOST = 'localhost'
USER = 'user'
PASSWORD = '1541'
DB = 'mydb'

# 상품 데이터베이스
STOCK_DB = 'pro_info'

# 멀티 스레드 서버
SERVER_HOST = ''
SERVER_PORT = 8888
user_list = {}
flag = 0
multi_port = 8080


# PC GUI

# 직원 메뉴
class staff_menu(QMainWindow):
    def __init__(self, parent=None):
        super(staff_menu, self).__init__(parent)

        self.mainlabel_txt = QLabel(self)
        self.mainlabel_txt.setText("직원 메뉴")
        mainlabel_txt_font = QtGui.QFont()
        mainlabel_txt_font.setPointSize(23)
        mainlabel_txt_font.setFamily("서울남산 장체M")
        self.mainlabel_txt.setFont(mainlabel_txt_font)
        self.mainlabel_txt.setGeometry(QtCore.QRect(540, 260, 341, 41))

        self.staff_info_btn = QPushButton(self)
        self.staff_info_btn.setText('상품 정보')
        staff_info_font = QtGui.QFont()
        staff_info_font.setPointSize(20)
        staff_info_font.setFamily("서울남산 장체M")
        self.staff_info_btn.setFont(staff_info_font)
        self.staff_info_btn.setGeometry(QtCore.QRect(430, 410, 150, 150))
        self.staff_info_btn.clicked.connect(self.staff_info_btn_clicked)
        self.staff_info_btn_dialogs = list()
        self.staff_info_btn.setCursor(QtGui.QCursor(QtCore.Qt.ClosedHandCursor))
        self.staff_info_btn.setStyleSheet('color:white; background:#0a326f')

        self.staff_stock_btn = QPushButton(self)
        self.staff_stock_btn.setText('재고 관리')
        staff_stock_font = QtGui.QFont()
        staff_stock_font.setPointSize(18)
        staff_stock_font.setFamily("서울남산 장체M")
        self.staff_stock_btn.setFont(staff_stock_font)
        self.staff_stock_btn.setGeometry(QtCore.QRect(630, 410, 150, 150))
        self.staff_stock_btn.clicked.connect(self.staff_stock_btn_clicked)
        self.staff_stock_btn_dialogs = list()
        self.staff_stock_btn.setCursor(QtGui.QCursor(QtCore.Qt.ClosedHandCursor))
        self.staff_stock_btn.setStyleSheet('color:white; background:#0a326f')

        self.logout_btn = QPushButton(self)
        self.logout_btn.setText('로그아웃')
        logout_btn_font = QtGui.QFont()
        logout_btn_font.setPointSize(9)
        logout_btn_font.setFamily("서울남산 장체M")
        self.logout_btn.setFont(logout_btn_font)
        self.logout_btn.setGeometry(QtCore.QRect(800, 230, 70, 30))
        self.logout_btn.clicked.connect(self.logout_btn_clicked)
        self.logout_btn_dialogs = list()
        self.logout_btn.setCursor(QtGui.QCursor(QtCore.Qt.ClosedHandCursor))
        self.logout_btn.setStyleSheet('color:white; background:#0a326f')

        self.logo = QLabel(self)
        self.logo.setGeometry(QtCore.QRect(-50, 30, 500, 100))
        icon = QPixmap("logo500.png")
        self.logo.setPixmap(QPixmap(icon))

        olmage = QImage("./back.JPG")
        slmage = olmage.scaled(QSize(1200, 800))
        palette = QPalette()
        palette.setBrush(10, QBrush(slmage))
        self.setPalette(palette)

        # self.retranslateUi(QMainWindow)
        # QtCore.QMetaObject.connectSlotsByName(QMainWindow)

        self.setGeometry(150, 100, 1200, 800)
        self.setWindowTitle('직원 메뉴')
        self.show()

    def staff_info_btn_clicked(self):
        self.close()
        staff_info_btn_dialogs = staff_info_menu(self)
        self.staff_info_btn_dialogs.append(staff_info_btn_dialogs)
        staff_info_btn_dialogs.show()

    def staff_stock_btn_clicked(self):
        self.staff_stock_btn.setCursor(QtGui.QCursor(QtCore.Qt.ClosedHandCursor))
        self.close()
        staff_stock_btn_dialogs = staff_stock_menu(self)
        self.staff_info_btn_dialogs.append(staff_stock_btn_dialogs)
        staff_stock_btn_dialogs.show()

    def logout_btn_clicked(self):
        self.close()
        logout_btn_dialogs = login_window(self)
        self.logout_btn_dialogs.append(logout_btn_dialogs)
        logout_btn_dialogs.show()

    # def retranslateUi(self, MainWindow):
    #     _translate = QtCore.QCoreApplication.translate
    #     MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
    #     self.staff_stock_btn.setText(_translate("MainWindow", "closehand"))
    #     self.staff_info_btn.setText(_translate("MainWindow", "openhand"))


# 직원 메뉴 - 상품 정보
class staff_info_menu(QMainWindow):
    def __init__(self, parent=None):
        global datalist, datalist2, datalist3, datalist4, datalist5, datalist6
        global b
        super(staff_info_menu, self).__init__(parent)

        con = pymysql.connect(host="192.168.0.19", user=USER, password="1234",
                              db='mydb', charset='utf8', autocommit=True)
        curs = con.cursor()
        sql = "SELECT idproducts FROM timetable ORDER BY idtime DESC LIMIT 1"
        idx = curs.execute(sql)
        data = curs.fetchone()

        for j in range(0, idx):
            datalist = data[j]

        sql2 = "SELECT brand FROM pro_info where idproducts = %s"
        idx2 = curs.execute(sql2, datalist)
        data2 = curs.fetchone()

        for b in range(0, idx2):
            datalist2 = data2[b]
            print(datalist2)

        sql3 = "SELECT model FROM pro_info where idproducts = %s"
        idx3 = curs.execute(sql3, datalist)
        data3 = curs.fetchone()

        for c in range(0, idx3):
            datalist3 = data3[c]
            print(datalist3)

        sql4 = "SELECT codenum FROM pro_info where idproducts = %s"
        idx4 = curs.execute(sql4, datalist)
        data4 = curs.fetchone()

        for d in range(0, idx4):
            datalist4 = data4[d]
            print(datalist4)

        sql5 = "SELECT unitprice FROM pro_info where idproducts = %s"
        idx5 = curs.execute(sql5, datalist)
        data5 = curs.fetchone()

        for e in range(0, idx5):
            datalist5 = data5[b]
            print(datalist5)

        sql6 = "SELECT inventory FROM pro_info where idproducts = %s"
        idx6 = curs.execute(sql6, datalist)
        data6 = curs.fetchone()

        for e in range(0, idx6):
            datalist6 = data6[b]
            print(datalist6)

        self.mainlabel_txt = QLabel(self)
        self.mainlabel_txt.setText("상품 정보 확인")
        mainlabel_txt_font = QtGui.QFont()
        mainlabel_txt_font.setPointSize(20)
        mainlabel_txt_font.setFamily("서울남산 장체M")
        self.mainlabel_txt.setFont(mainlabel_txt_font)
        self.mainlabel_txt.setGeometry(QtCore.QRect(520, 220, 341, 41))

        self.brand_label = QLabel(self)
        self.brand_label.setText("· 상품 브랜드 :")
        brand_label_font = QtGui.QFont()
        brand_label_font.setPointSize(13)
        brand_label_font.setFamily("서울남산 장체M")
        self.brand_label.setFont(brand_label_font)
        self.brand_label.setGeometry(QtCore.QRect(400, 340, 150, 41))

        self.brand_txt = QLabel(self)
        self.brand_txt.setText(datalist2)
        brand_txt_font = QtGui.QFont()
        brand_txt_font.setPointSize(13)
        brand_txt_font.setFamily("서울남산 장체M")
        self.brand_txt.setFont(brand_txt_font)
        self.brand_txt.setGeometry(QtCore.QRect(550, 340, 150, 41))

        self.namelabel = QLabel(self)
        self.namelabel.setText("· 상품 종류 :")
        namelabel_font = QtGui.QFont()
        namelabel_font.setPointSize(13)
        namelabel_font.setFamily("서울남산 장체M")
        self.namelabel.setFont(namelabel_font)
        self.namelabel.setGeometry(QtCore.QRect(400, 400, 150, 41))

        self.namelabel = QLabel(self)
        self.namelabel.setText(datalist3)
        namelabel_font = QtGui.QFont()
        namelabel_font.setPointSize(13)
        namelabel_font.setFamily("서울남산 장체M")
        self.namelabel.setFont(namelabel_font)
        self.namelabel.setGeometry(QtCore.QRect(550, 400, 150, 41))

        self.codelabel = QLabel(self)
        self.codelabel.setText("· 상품 코드 :")
        codelabel_font = QtGui.QFont()
        codelabel_font.setPointSize(13)
        codelabel_font.setFamily("서울남산 장체M")
        self.codelabel.setFont(codelabel_font)
        self.codelabel.setGeometry(QtCore.QRect(400, 460, 150, 41))

        self.codelabel = QLabel(self)
        self.codelabel.setText(datalist4)
        codelabel_font = QtGui.QFont()
        codelabel_font.setPointSize(13)
        codelabel_font.setFamily("서울남산 장체M")
        self.codelabel.setFont(codelabel_font)
        self.codelabel.setGeometry(QtCore.QRect(550, 460, 150, 41))

        self.pricelabel = QLabel(self)
        self.pricelabel.setText("· 상품 단가 :")
        pricelabel_font = QtGui.QFont()
        pricelabel_font.setPointSize(13)
        pricelabel_font.setFamily("서울남산 장체M")
        self.pricelabel.setFont(pricelabel_font)
        self.pricelabel.setGeometry(QtCore.QRect(400, 520, 150, 41))

        self.pricelabel = QLabel(self)
        self.pricelabel.setText(datalist5)
        pricelabel_font = QtGui.QFont()
        pricelabel_font.setPointSize(13)
        pricelabel_font.setFamily("서울남산 장체M")
        self.pricelabel.setFont(pricelabel_font)
        self.pricelabel.setGeometry(QtCore.QRect(550, 520, 150, 41))

        self.pricelabel = QLabel(self)
        self.pricelabel.setText("· 상품 재고량 :")
        pricelabel_font = QtGui.QFont()
        pricelabel_font.setPointSize(13)
        pricelabel_font.setFamily("서울남산 장체M")
        self.pricelabel.setFont(pricelabel_font)
        self.pricelabel.setGeometry(QtCore.QRect(400, 580, 150, 41))

        self.pricelabel = QLabel(self)
        self.pricelabel.setText(datalist6)
        pricelabel_font = QtGui.QFont()
        pricelabel_font.setPointSize(13)
        pricelabel_font.setFamily("서울남산 장체M")
        self.pricelabel.setFont(pricelabel_font)
        self.pricelabel.setGeometry(QtCore.QRect(550, 580, 150, 41))

        self.logo = QLabel(self)
        self.logo.setGeometry(QtCore.QRect(-50, 30, 500, 100))
        icon = QPixmap("logo500.png")
        self.logo.setPixmap(QPixmap(icon))

        olmage = QImage("./back.JPG")
        slmage = olmage.scaled(QSize(1200, 800))
        palette = QPalette()
        palette.setBrush(10, QBrush(slmage))
        self.setPalette(palette)

        self.back_btn = QPushButton(self)
        self.back_btn.setGeometry(QtCore.QRect(0, 89, 80, 52))
        self.back_btn.setText("뒤로가기")
        back_btn_font = QtGui.QFont()
        back_btn_font.setPointSize(10)
        back_btn_font.setFamily("서울남산 장체M")
        self.back_btn.setFont(back_btn_font)
        self.back_btn.clicked.connect(self.back_btn_clicked)
        self.back_btn_dialogs = list()
        self.back_btn.setCursor(QtGui.QCursor(QtCore.Qt.ClosedHandCursor))
        self.back_btn.setStyleSheet('color:white; background-color:rgba(1, 0, 0, 0.1)')

        self.setGeometry(150, 100, 1200, 800)
        self.setWindowTitle('[직원 메뉴] 상품 정보')
        self.show()

    def back_btn_clicked(self):
        self.close()
        back_btn_dialogs = staff_menu(self)
        self.back_btn_dialogs.append(back_btn_dialogs)
        back_btn_dialogs.show()


# 직원 메뉴 - 재고 관리
class staff_stock_menu(QMainWindow):
    con = pymysql.connect(host=HOST, user=USER, password=PASSWORD, db=DB, charset='utf8')
    cur_num = con.cursor()
    sql_num = "SELECT * FROM pro_info;"
    cur_num.execute(sql_num)
    data_num = cur_num.fetchall()

    li_num = len([x[0] for x in data_num])

    def __init__(self, parent=None):
        super(staff_stock_menu, self).__init__(parent)

        con = pymysql.connect(host=HOST, user=USER, password=PASSWORD, db=DB, charset='utf8')
        cur_num = con.cursor()
        sql_num = "SELECT * FROM pro_info;"
        cur_num.execute(sql_num)
        data_num = cur_num.fetchall()
        li_num = [x[0] for x in data_num]

        self.mainlabel_txt = QLabel(self)
        self.mainlabel_txt.setText("재고 관리 및 수정")
        mainlabel_txt_font = QtGui.QFont()
        mainlabel_txt_font.setPointSize(15)
        mainlabel_txt_font.setFamily("서울남산 장체M")
        self.mainlabel_txt.setFont(mainlabel_txt_font)
        self.mainlabel_txt.setGeometry(QtCore.QRect(520, 250, 341, 41))

        # 테이블 설정
        self.stock_table = QTableWidget(self)
        self.stock_table.setColumnCount(5)
        self.stock_table.setRowCount(len(li_num))
        self.stock_table.setGeometry(QtCore.QRect(350, 320, 521, 247))
        self.stock_table.setHorizontalHeaderLabels([
            "브랜드", "종류", "모델명", "가격", "재고량"])
        # self.stock_table.setItem(0, 0, QTableWidgetItem(" ༼ ༎ຶ ෴ ༎ຶ༽ "))
        # self.stock_table.setItem(0, 1, QTableWidgetItem(" ༼;´༎ຶ ۝༎ຶ`༽ "))
        # self.stock_table.setItem(0, 2, QTableWidgetItem(" ༽΄◞ิ౪◟ิ‵༼ "))
        # self.stock_table.setItem(0, 3, QTableWidgetItem(" ⎛⎝⎛° ͜ʖ°⎞⎠⎞ "))
        # self.stock_table.setItem(1, 0, QTableWidgetItem(" ξ(｡◕ˇ◊ˇ◕｡)ξ "))
        # self.stock_table.setItem(1, 1, QTableWidgetItem("  (๑¯ਊ¯)σ "))
        # self.stock_table.setItem(1, 2, QTableWidgetItem(" (っ˘ڡ˘ς) "))
        # self.stock_table.setItem(1, 3, QTableWidgetItem(" ( ≖ଳ≖) "))
        # self.stock_table.setItem(2, 0, QTableWidgetItem(" (´ε｀ ʃƪ)♡ "))
        # self.stock_table.setItem(2, 1, QTableWidgetItem(" (ʃƪ ˘ ³˘) "))

        pro_len = len(li_num)
        # 테이블위젯 - 데이터베이스 연동
        for x in range(pro_len):
            for i in range(0, 5):
                li = [x[i+1] for x in data_num]
                self.stock_table.setItem(x, i, QTableWidgetItem(li[x]))

        self.stock_add_btn = QPushButton(self)
        self.stock_add_btn.setGeometry(QtCore.QRect(350, 600, 130, 50))
        self.stock_add_btn.setText("상품 추가")
        stock_add_btn_font = QtGui.QFont()
        stock_add_btn_font.setPointSize(10)
        stock_add_btn_font.setFamily("서울남산 장체M")
        self.stock_add_btn.setFont(stock_add_btn_font)
        self.stock_add_btn.clicked.connect(self.stock_add_btn_clicked)
        self.stock_add_btn_dialogs = list()
        self.stock_add_btn.setStyleSheet('color:white; background:#0a326f')

        self.stock_edit_btn = QPushButton(self)
        self.stock_edit_btn.setGeometry(QtCore.QRect(530, 600, 130, 50))
        self.stock_edit_btn.setText("재고 수정")
        stock_edit_btn_font = QtGui.QFont()
        stock_edit_btn_font.setPointSize(10)
        stock_edit_btn_font.setFamily("서울남산 장체M")
        self.stock_edit_btn.setFont(stock_edit_btn_font)
        self.stock_edit_btn.clicked.connect(self.stock_edit_btn_clicked)
        self.stock_edit_btn_dialogs = list()
        self.stock_edit_btn.setStyleSheet('color:white; background:#0a326f')

        self.stock_delete_btn = QPushButton(self)
        self.stock_delete_btn.setGeometry(QtCore.QRect(720, 600, 130, 50))
        self.stock_delete_btn.setText("상품 삭제")
        stock_delete_font = QtGui.QFont()
        stock_delete_font.setPointSize(10)
        stock_delete_font.setFamily("서울남산 장체M")
        self.stock_delete_btn.setFont(stock_delete_font)
        self.stock_delete_btn.clicked.connect(self.stock_delete_btn_clicked)
        self.stock_delete_btn_dialogs = list()
        self.stock_delete_btn.setStyleSheet('color:white; background:#0a326f')

        self.logo = QLabel(self)
        self.logo.setGeometry(QtCore.QRect(-50, 30, 500, 100))
        icon = QPixmap("logo500.png")
        self.logo.setPixmap(QPixmap(icon))

        # 테이블 수정 금지 모드
        self.stock_table.setEditTriggers(QAbstractItemView.NoEditTriggers)

        olmage = QImage("./back.JPG")
        slmage = olmage.scaled(QSize(1200, 800))
        palette = QPalette()
        palette.setBrush(10, QBrush(slmage))
        self.setPalette(palette)

        self.back_btn = QPushButton(self)
        self.back_btn.setGeometry(QtCore.QRect(0, 89, 80, 52))
        self.back_btn.setText("뒤로가기")
        back_btn_font = QtGui.QFont()
        back_btn_font.setPointSize(10)
        back_btn_font.setFamily("서울남산 장체M")
        self.back_btn.setFont(back_btn_font)
        self.back_btn.clicked.connect(self.back_btn_clicked)
        self.back_btn_dialogs = list()
        self.back_btn.setCursor(QtGui.QCursor(QtCore.Qt.ClosedHandCursor))
        self.back_btn.setStyleSheet('color:white; background-color:rgba(1, 0, 0, 0.1)')

        self.setGeometry(150, 100, 1200, 800)
        self.setWindowTitle('[직원 메뉴] 재고 관리')
        self.show()

    def stock_add_btn_clicked(self):
        self.close()
        stock_add_btn_dialogs = staff_stock_add(self)
        self.stock_add_btn_dialogs.append(stock_add_btn_dialogs)
        stock_add_btn_dialogs.show()

    def stock_edit_btn_clicked(self):
        self.close()
        stock_edit_btn_dialogs = staff_stock_edit(self)
        self.stock_edit_btn_dialogs.append(stock_edit_btn_dialogs)
        stock_edit_btn_dialogs.show()

    def stock_delete_btn_clicked(self):
        self.close()
        stock_delete_btn_dialogs = staff_stock_delete(self)
        self.stock_delete_btn_dialogs.append(stock_delete_btn_dialogs)
        stock_delete_btn_dialogs.show()

    def back_btn_clicked(self):
        self.close()
        back_btn_dialogs = staff_menu(self)
        self.back_btn_dialogs.append(back_btn_dialogs)
        back_btn_dialogs.show()

    def stock_num(self):
        print(len(self.li_num))


# 직원 메뉴 - 재고 관리 - 상품 추가 화면
class staff_stock_add(QMainWindow):
    def __init__(self, parent=None):
        super(staff_stock_add, self).__init__(parent)

        self.mainlabel_txt = QLabel(self)
        self.mainlabel_txt.setText("상품 추가")
        mainlabel_txt_font = QtGui.QFont()
        mainlabel_txt_font.setPointSize(15)
        mainlabel_txt_font.setFamily("서울남산 장체M")
        self.mainlabel_txt.setFont(mainlabel_txt_font)
        self.mainlabel_txt.setGeometry(QtCore.QRect(540, 250, 350, 40))

        self.brand = QLabel(self)
        self.brand.setText("상품 브랜드 : ")
        brand_font = QtGui.QFont()
        brand_font.setPointSize(10)
        brand_font.setFamily("서울남산 장체M")
        self.brand.setFont(brand_font)
        self.brand.setGeometry(QtCore.QRect(400, 350, 350, 60))

        self.kinds = QLabel(self)
        self.kinds.setText("상품 종류 : ")
        kinds_font = QtGui.QFont()
        kinds_font.setPointSize(10)
        kinds_font.setFamily("서울남산 장체M")
        self.kinds.setFont(kinds_font)
        self.kinds.setGeometry(QtCore.QRect(400, 390, 350, 60))

        self.model_name = QLabel(self)
        self.model_name.setText("상품 모델명 : ")
        model_name_font = QtGui.QFont()
        model_name_font.setPointSize(10)
        model_name_font.setFamily("서울남산 장체M")
        self.model_name.setFont(model_name_font)
        self.model_name.setGeometry(QtCore.QRect(400, 430, 350, 60))

        self.price = QLabel(self)
        self.price.setText("상품 가격 : ")
        price_font = QtGui.QFont()
        price_font.setPointSize(10)
        price_font.setFamily("서울남산 장체M")
        self.price.setFont(price_font)
        self.price.setGeometry(QtCore.QRect(400, 470, 350, 60))

        self.inventory = QLabel(self)
        self.inventory.setText("상품 재고량 : ")
        inventory_font = QtGui.QFont()
        inventory_font.setPointSize(10)
        inventory_font.setFamily("서울남산 장체M")
        self.inventory.setFont(inventory_font)
        self.inventory.setGeometry(QtCore.QRect(400, 510, 350, 60))

        self.brand_txt = QLineEdit(self)
        self.brand_txt.setText("")
        brand_txt_font = QtGui.QFont()
        brand_txt_font.setPointSize(10)
        brand_txt_font.setFamily("서울남산 장체M")
        self.brand_txt.setFont(brand_txt_font)
        self.brand_txt.setGeometry(QtCore.QRect(500, 365, 230, 30))

        self.kinds_txt = QLineEdit(self)
        self.kinds_txt.setText("")
        kinds_txt_font = QtGui.QFont()
        kinds_txt_font.setPointSize(10)
        kinds_txt_font.setFamily("서울남산 장체M")
        self.kinds_txt.setFont(kinds_txt_font)
        self.kinds_txt.setGeometry(QtCore.QRect(500, 405, 230, 30))

        self.model_txt = QLineEdit(self)
        self.model_txt.setText("")
        model_txt_font = QtGui.QFont()
        model_txt_font.setPointSize(10)
        model_txt_font.setFamily("서울남산 장체M")
        self.model_txt.setFont(model_txt_font)
        self.model_txt.setGeometry(QtCore.QRect(500, 445, 230, 30))

        self.price_txt = QLineEdit(self)
        self.price_txt.setText("")
        price_txt_font = QtGui.QFont()
        price_txt_font.setPointSize(10)
        price_txt_font.setFamily("서울남산 장체M")
        self.price_txt.setFont(price_txt_font)
        self.price_txt.setGeometry(QtCore.QRect(500, 485, 230, 30))

        self.inventory_txt = QLineEdit(self)
        self.inventory_txt.setText("")
        inventory_txt_font = QtGui.QFont()
        inventory_txt_font.setPointSize(10)
        inventory_txt_font.setFamily("서울남산 장체M")
        self.inventory_txt.setFont(inventory_txt_font)
        self.inventory_txt.setGeometry(QtCore.QRect(500, 525, 230, 30))

        self.stock_add_alarm_btn = QPushButton(self)
        self.stock_add_alarm_btn.setGeometry(QtCore.QRect(530, 600, 130, 50))
        self.stock_add_alarm_btn.setText("저장")
        stock_add_alarm_btn_font = QtGui.QFont()
        stock_add_alarm_btn_font.setPointSize(10)
        stock_add_alarm_btn_font.setFamily("서울남산 장체M")
        self.stock_add_alarm_btn.setFont(stock_add_alarm_btn_font)
        self.stock_add_alarm_btn.clicked.connect(self.staff_stock_add_alarm_btn_clicked)
        self.stock_add_alarm_btn_dialogs = list()
        self.stock_add_alarm_btn.setStyleSheet('color:white; background:#0a326f')

        self.logo = QLabel(self)
        self.logo.setGeometry(QtCore.QRect(-50, 30, 500, 100))
        icon = QPixmap("logo500.png")
        self.logo.setPixmap(QPixmap(icon))

        olmage = QImage("./back.JPG")
        slmage = olmage.scaled(QSize(1200, 800))
        palette = QPalette()
        palette.setBrush(10, QBrush(slmage))
        self.setPalette(palette)

        self.back_btn = QPushButton(self)
        self.back_btn.setGeometry(QtCore.QRect(0, 89, 80, 52))
        self.back_btn.setText("뒤로가기")
        back_btn_font = QtGui.QFont()
        back_btn_font.setPointSize(10)
        back_btn_font.setFamily("서울남산 장체M")
        self.back_btn.setFont(back_btn_font)
        self.back_btn.clicked.connect(self.back_btn_clicked)
        self.back_btn_dialogs = list()
        self.back_btn.setCursor(QtGui.QCursor(QtCore.Qt.ClosedHandCursor))
        self.back_btn.setStyleSheet('color:white; background-color:rgba(1, 0, 0, 0.1)')

        self.setGeometry(150, 100, 1200, 800)
        self.setWindowTitle('[직원 메뉴] 재고 관리 - 상품 추가')
        self.show()

    def staff_stock_add_alarm_btn_clicked(self):
        con = pymysql.connect(host=HOST, user=USER, password=PASSWORD, db=DB, charset='utf8', autocommit=True)
        cur_insert = con.cursor()

        sql_num = "SELECT * FROM pro_info;"
        cur_insert.execute(
            "INSERT INTO pro_info(brand, model, codenum, unitprice, inventory) VALUES('%s', '%s', '%s', '%s', '%s')" % (
                ''.join(self.brand_txt.text()), ''.join(self.kinds_txt.text()), ''.join(self.model_txt.text()),
                ''.join(self.price_txt.text()), ''.join(self.inventory_txt.text())))

        self.close()
        stock_add_alarm_btn_dialogs = staff_stock_menu(self)
        self.stock_add_alarm_btn_dialogs.append(stock_add_alarm_btn_dialogs)
        stock_add_alarm_btn_dialogs.show()

    def back_btn_clicked(self):
        self.close()
        back_btn_dialogs = staff_stock_menu(self)
        self.back_btn_dialogs.append(back_btn_dialogs)
        back_btn_dialogs.show()


# 직원 메뉴 - 재고 관리 - 재고 수정 화면
class staff_stock_edit(QMainWindow):
    def __init__(self, parent=None):
        super(staff_stock_edit, self).__init__(parent)

        self.model_combobox = QComboBox(self)
        self.model_combobox.setGeometry(QtCore.QRect(720, 350, 100, 30))
        self.model_combobox.setStyleSheet('color:white; background:#0a326f')

        self.kinds_combobox = QComboBox(self)
        self.kinds_combobox.setGeometry(QtCore.QRect(560, 350, 100, 30))
        self.kinds_combobox.setStyleSheet('color:white; background:#0a326f')

        con = pymysql.connect(host=HOST, user=USER, password=PASSWORD, db=DB, charset='utf8', autocommit=True)

        cur_brand = con.cursor()
        sql_brand = "SELECT distinct brand FROM pro_info;"
        cur_brand.execute(sql_brand)
        data_brand = cur_brand.fetchall()
        li_brand = [x[0] for x in data_brand]

        self.mainlabel_txt = QLabel(self)
        self.mainlabel_txt.setText("재고 수정")
        mainlabel_txt_font = QtGui.QFont()
        mainlabel_txt_font.setPointSize(15)
        mainlabel_txt_font.setFamily("서울남산 장체M")
        self.mainlabel_txt.setFont(mainlabel_txt_font)
        self.mainlabel_txt.setGeometry(QtCore.QRect(540, 250, 341, 41))

        self.brand = QLabel(self)
        self.brand.setText("브랜드")
        brand_font = QtGui.QFont()
        brand_font.setPointSize(10)
        brand_font.setFamily("서울남산 장체M")
        self.brand.setFont(brand_font)
        self.brand.setGeometry(QtCore.QRect(420, 320, 100, 30))

        self.brand_combobox = QComboBox(self)
        self.brand_combobox.addItem('')
        self.brand_combobox.addItems(li_brand)
        self.brand_combobox.activated.connect(self.brand_combo_change)
        self.brand_combobox.setGeometry(QtCore.QRect(400, 350, 100, 30))
        self.brand_combobox.setStyleSheet('color:white; background:#0a326f')

        self.kinds = QLabel(self)
        self.kinds.setText("종류")
        kinds_font = QtGui.QFont()
        kinds_font.setPointSize(10)
        kinds_font.setFamily("서울남산 장체M")
        self.kinds.setFont(kinds_font)
        self.kinds.setGeometry(QtCore.QRect(590, 320, 100, 30))

        #
        cur_search_brand = con.cursor()
        sql_search_brand = "SELECT distinct model FROM pro_info WHERE brand = %s;"
        cur_search_brand.execute(sql_search_brand, (self.brand_combobox.currentText()))
        data_search_brand = cur_search_brand.fetchall()
        li_search_brand = [x[0] for x in data_search_brand]
        #

        self.model = QLabel(self)
        self.model.setText("모델명")
        model_font = QtGui.QFont()
        model_font.setPointSize(10)
        model_font.setFamily("서울남산 장체M")
        self.model.setFont(model_font)
        self.model.setGeometry(QtCore.QRect(740, 320, 100, 30))

        #
        self.model = QLabel(self)
        self.model.setText("재고량을")
        model_font = QtGui.QFont()
        model_font.setPointSize(15)
        model_font.setFamily("서울남산 장체M")
        self.model.setFont(model_font)
        self.model.setGeometry(QtCore.QRect(480, 500, 100, 30))

        self.inventory_num_txt = QLineEdit(self)
        self.inventory_num_txt.setText("")
        inventory_num_font = QtGui.QFont()
        inventory_num_font.setPointSize(15)
        inventory_num_font.setFamily("서울남산 장체M")
        self.inventory_num_txt.setFont(inventory_num_font)
        self.inventory_num_txt.setGeometry(QtCore.QRect(590, 500, 55, 30))

        self.model = QLabel(self)
        self.model.setText("개로 변경.")
        mode_font = QtGui.QFont()
        model_font.setPointSize(15)
        model_font.setFamily("서울남산 장체M")
        self.model.setFont(model_font)
        self.model.setGeometry(QtCore.QRect(650, 500, 100, 30))
        #

        self.stock_add_alarm_btn = QPushButton(self)
        self.stock_add_alarm_btn.setGeometry(QtCore.QRect(530, 600, 130, 50))
        self.stock_add_alarm_btn.setText("저장")
        stock_add_alarm_btn_font = QtGui.QFont()
        stock_add_alarm_btn_font.setPointSize(10)
        stock_add_alarm_btn_font.setFamily("서울남산 장체M")
        self.stock_add_alarm_btn.setFont(stock_add_alarm_btn_font)
        self.stock_add_alarm_btn.clicked.connect(self.staff_stock_add_alarm_btn_clicked)
        self.stock_add_alarm_btn_dialogs = list()
        self.stock_add_alarm_btn.setStyleSheet('color:white; background:#0a326f')

        self.logo = QLabel(self)
        self.logo.setGeometry(QtCore.QRect(-50, 30, 500, 100))
        icon = QPixmap("logo500.png")
        self.logo.setPixmap(QPixmap(icon))

        olmage = QImage("./back.JPG")
        slmage = olmage.scaled(QSize(1200, 800))
        palette = QPalette()
        palette.setBrush(10, QBrush(slmage))
        self.setPalette(palette)

        self.back_btn = QPushButton(self)
        self.back_btn.setGeometry(QtCore.QRect(0, 89, 80, 52))
        self.back_btn.setText("뒤로가기")
        back_btn_font = QtGui.QFont()
        back_btn_font.setPointSize(10)
        back_btn_font.setFamily("서울남산 장체M")
        self.back_btn.setFont(back_btn_font)
        self.back_btn.clicked.connect(self.back_btn_clicked)
        self.back_btn_dialogs = list()
        self.back_btn.setCursor(QtGui.QCursor(QtCore.Qt.ClosedHandCursor))
        self.back_btn.setStyleSheet('color:white; background-color:rgba(1, 0, 0, 0.1)')

        self.setGeometry(150, 100, 1200, 800)
        self.setWindowTitle('[직원 메뉴] 재고 관리 - 재고 수정')
        self.show()

    def brand_combo_change(self):
        print(self.brand_combobox.currentText())
        con = pymysql.connect(host=HOST, user=USER, password=PASSWORD, db=DB, charset='utf8', autocommit=True)

        cur_search_brand = con.cursor()
        sql_search_brand = "SELECT distinct model FROM pro_info WHERE brand = %s;"
        cur_search_brand.execute(sql_search_brand, (self.brand_combobox.currentText()))
        data_search_brand = cur_search_brand.fetchall()
        li_search_brand = [x[0] for x in data_search_brand]

        self.kinds_combobox.addItem('')
        self.kinds_combobox.addItems(li_search_brand)
        self.kinds_combobox.activated.connect(self.kinds_combo_change)
        self.kinds_combobox.setGeometry(QtCore.QRect(560, 350, 100, 30))
        self.kinds_combobox.setStyleSheet('color:white; background:#0a326f')

    def kinds_combo_change(self):
        print(self.kinds_combobox.currentText())
        con = pymysql.connect(host=HOST, user=USER, password=PASSWORD, db=DB, charset='utf8', autocommit=True)

        cur_search_model = con.cursor()
        sql_search_model = "SELECT distinct codenum FROM pro_info WHERE model = %s and brand = %s;"
        cur_search_model.execute(sql_search_model,
                                 (self.kinds_combobox.currentText(), self.brand_combobox.currentText()))
        data_search_model = cur_search_model.fetchall()
        li_search_model = [x[0] for x in data_search_model]

        self.model_combobox.addItem('')
        self.model_combobox.addItems(li_search_model)
        self.model_combobox.activated.connect(self.model_combo_change)
        self.model_combobox.setGeometry(QtCore.QRect(720, 350, 100, 30))
        self.model_combobox.setStyleSheet('color:white; background:#0a326f')

    def model_combo_change(self):
        print(self.model_combobox.currentText())

    def staff_stock_add_alarm_btn_clicked(self):
        con = pymysql.connect(host=HOST, user=USER, password=PASSWORD, db=DB, charset='utf8', autocommit=True)
        cur = con.cursor()
        sql_up = "UPDATE pro_info SET inventory = %s WHERE brand = %s and model = %s and codenum = %s;"
        cur.execute(sql_up, (
            self.inventory_num_txt.text(), self.brand_combobox.currentText(), self.kinds_combobox.currentText(),
            self.model_combobox.currentText()))

        print(self.inventory_num_txt.text())

        self.close()
        stock_add_alarm_btn_dialogs = staff_stock_menu(self)
        self.stock_add_alarm_btn_dialogs.append(stock_add_alarm_btn_dialogs)
        stock_add_alarm_btn_dialogs.show()

    def back_btn_clicked(self):
        self.close()
        back_btn_dialogs = staff_stock_menu(self)
        self.back_btn_dialogs.append(back_btn_dialogs)
        back_btn_dialogs.show()


# 직원 메뉴 - 재고 관리 - 상품 삭제 화면
class staff_stock_delete(QMainWindow):
    def __init__(self, parent=None):
        super(staff_stock_delete, self).__init__(parent)

        self.model_txtB = QTextBrowser(self)
        self.model_txtB.setGeometry(QtCore.QRect(390, 500, 430, 80))

        self.model_combobox = QComboBox(self)
        self.model_combobox.setGeometry(QtCore.QRect(720, 350, 100, 30))
        self.model_combobox.setStyleSheet('color:white; background:#0a326f')

        self.kinds_combobox = QComboBox(self)
        self.kinds_combobox.setGeometry(QtCore.QRect(560, 350, 100, 30))
        self.kinds_combobox.setStyleSheet('color:white; background:#0a326f')

        con = pymysql.connect(host=HOST, user=USER, password=PASSWORD, db=DB, charset='utf8', autocommit=True)

        cur_brand = con.cursor()
        sql_brand = "SELECT distinct brand FROM pro_info;"
        cur_brand.execute(sql_brand)
        data_brand = cur_brand.fetchall()
        li_brand = [x[0] for x in data_brand]

        self.mainlabel_txt = QLabel(self)
        self.mainlabel_txt.setText("상품 삭제")
        mainlabel_txt_font = QtGui.QFont()
        mainlabel_txt_font.setPointSize(15)
        mainlabel_txt_font.setFamily("서울남산 장체M")
        self.mainlabel_txt.setFont(mainlabel_txt_font)
        self.mainlabel_txt.setGeometry(QtCore.QRect(540, 250, 341, 41))

        self.brand = QLabel(self)
        self.brand.setText("브랜드")
        brand_font = QtGui.QFont()
        brand_font.setPointSize(10)
        brand_font.setFamily("서울남산 장체M")
        self.brand.setFont(brand_font)
        self.brand.setGeometry(QtCore.QRect(420, 320, 100, 30))

        self.brand_combobox = QComboBox(self)
        self.brand_combobox.addItem('')
        self.brand_combobox.addItems(li_brand)
        self.brand_combobox.activated.connect(self.brand_combo_change)
        self.brand_combobox.setGeometry(QtCore.QRect(400, 350, 100, 30))
        self.brand_combobox.setStyleSheet('color:white; background:#0a326f')

        self.kinds = QLabel(self)
        self.kinds.setText("종류")
        kinds_font = QtGui.QFont()
        kinds_font.setPointSize(10)
        kinds_font.setFamily("서울남산 장체M")
        self.kinds.setFont(kinds_font)
        self.kinds.setGeometry(QtCore.QRect(590, 320, 100, 30))

        #
        cur_search_brand = con.cursor()
        sql_search_brand = "SELECT distinct model FROM pro_info WHERE brand = %s;"
        cur_search_brand.execute(sql_search_brand, (self.brand_combobox.currentText()))
        data_search_brand = cur_search_brand.fetchall()
        li_search_brand = [x[0] for x in data_search_brand]
        #

        self.model = QLabel(self)
        self.model.setText("모델명")
        model_font = QtGui.QFont()
        model_font.setPointSize(10)
        model_font.setFamily("서울남산 장체M")
        self.model.setFont(model_font)
        self.model.setGeometry(QtCore.QRect(740, 320, 100, 30))

        #

        #

        self.stock_add_alarm_btn = QPushButton(self)
        self.stock_add_alarm_btn.setGeometry(QtCore.QRect(530, 600, 130, 50))
        self.stock_add_alarm_btn.setText("삭제")
        stock_add_alarm_btn_font = QtGui.QFont()
        stock_add_alarm_btn_font.setPointSize(10)
        stock_add_alarm_btn_font.setFamily("서울남산 장체M")
        self.stock_add_alarm_btn.setFont(stock_add_alarm_btn_font)
        self.stock_add_alarm_btn.clicked.connect(self.stock_delete_alarm_btn_clicked)
        self.stock_add_alarm_btn_dialogs = list()
        self.stock_add_alarm_btn.setStyleSheet('color:white; background:#0a326f')

        self.logo = QLabel(self)
        self.logo.setGeometry(QtCore.QRect(-50, 30, 500, 100))
        icon = QPixmap("logo500.png")
        self.logo.setPixmap(QPixmap(icon))

        olmage = QImage("./back.JPG")
        slmage = olmage.scaled(QSize(1200, 800))
        palette = QPalette()
        palette.setBrush(10, QBrush(slmage))
        self.setPalette(palette)

        self.back_btn = QPushButton(self)
        self.back_btn.setGeometry(QtCore.QRect(0, 89, 80, 52))
        self.back_btn.setText("뒤로가기")
        back_btn_font = QtGui.QFont()
        back_btn_font.setPointSize(10)
        back_btn_font.setFamily("서울남산 장체M")
        self.back_btn.setFont(back_btn_font)
        self.back_btn.clicked.connect(self.back_btn_clicked)
        self.back_btn_dialogs = list()
        self.back_btn.setCursor(QtGui.QCursor(QtCore.Qt.ClosedHandCursor))
        self.back_btn.setStyleSheet('color:white; background-color:rgba(1, 0, 0, 0.1)')

        self.setGeometry(150, 100, 1200, 800)
        self.setWindowTitle('[직원 메뉴] 재고 관리 - 상품 삭제')
        self.show()

    def brand_combo_change(self):
        con = pymysql.connect(host=HOST, user=USER, password=PASSWORD, db=DB, charset='utf8', autocommit=True)

        cur_search_brand = con.cursor()
        sql_search_brand = "SELECT distinct model FROM pro_info WHERE brand = %s;"
        cur_search_brand.execute(sql_search_brand, (self.brand_combobox.currentText()))
        data_search_brand = cur_search_brand.fetchall()
        li_search_brand = [x[0] for x in data_search_brand]

        self.kinds_combobox.addItem('')
        self.kinds_combobox.addItems(li_search_brand)
        self.kinds_combobox.activated.connect(self.kinds_combo_change)
        self.kinds_combobox.setGeometry(QtCore.QRect(560, 350, 100, 30))

    def kinds_combo_change(self):
        con = pymysql.connect(host=HOST, user=USER, password=PASSWORD, db=DB, charset='utf8', autocommit=True)

        cur_search_model = con.cursor()
        sql_search_model = "SELECT distinct codenum FROM pro_info WHERE model = %s and brand = %s;"
        cur_search_model.execute(sql_search_model,
                                 (self.kinds_combobox.currentText(), self.brand_combobox.currentText()))
        data_search_model = cur_search_model.fetchall()
        li_search_model = [x[0] for x in data_search_model]

        self.model_combobox.addItem('')
        self.model_combobox.addItems(li_search_model)
        self.model_combobox.activated.connect(self.model_combo_change)
        self.model_combobox.setGeometry(QtCore.QRect(720, 350, 100, 30))

    def model_combo_change(self):
        BRAND = self.brand_combobox.currentText()
        KINDS = self.kinds_combobox.currentText()
        MODEL = self.model_combobox.currentText()

        self.model_txtB.setText('''"''' + BRAND + '''" 의 ''' + KINDS + "'인 [" + MODEL + "]를 삭제하시겠습니까?")
        model_txtB_font = QtGui.QFont()
        model_txtB_font.setPointSize(10)
        model_txtB_font.setFamily("서울남산 장체M")
        self.model_txtB.setFont(model_txtB_font)
        self.model_txtB.setGeometry(QtCore.QRect(390, 500, 430, 80))

    def stock_delete_alarm_btn_clicked(self):
        con = pymysql.connect(host=HOST, user=USER, password=PASSWORD, db=DB, charset='utf8', autocommit=True)
        cur = con.cursor()
        sql_del = "DELETE FROM pro_info WHERE brand = %s and model = %s and codenum = %s;"
        cur.execute(sql_del, (
            self.brand_combobox.currentText(), self.kinds_combobox.currentText(),
            self.model_combobox.currentText()))

        self.close()
        stock_add_alarm_btn_dialogs = manager_menu_stockmenu(self)
        self.stock_add_alarm_btn_dialogs.append(stock_add_alarm_btn_dialogs)
        stock_add_alarm_btn_dialogs.show()

    def back_btn_clicked(self):
        self.close()
        back_btn_dialogs = staff_stock_menu(self)
        self.back_btn_dialogs.append(back_btn_dialogs)
        back_btn_dialogs.show()


# 관리자 메뉴
class manager_menu(QMainWindow):
    def __init__(self, parent=None):
        super(manager_menu, self).__init__(parent)

        self.mainlabel_txt = QLabel(self)
        self.mainlabel_txt.setText("관리자 메뉴")
        mainlabel_txt_font = QtGui.QFont()
        mainlabel_txt_font.setPointSize(23)
        mainlabel_txt_font.setFamily("서울남산 장체M")
        self.mainlabel_txt.setFont(mainlabel_txt_font)
        self.mainlabel_txt.setGeometry(QtCore.QRect(500, 260, 341, 41))

        self.info_btn = QPushButton(self)
        self.info_btn.setText('상품 정보')
        info_btn_font = QtGui.QFont()
        info_btn_font.setPointSize(20)
        info_btn_font.setFamily("서울남산 장체M")
        self.info_btn.setFont(info_btn_font)
        self.info_btn.setGeometry(QtCore.QRect(330, 350, 150, 150))
        self.info_btn_dialogs = list()
        self.info_btn.setStyleSheet('color:white; background:#0a326f')

        self.sales_btn = QPushButton(self)
        self.sales_btn.setText('매출 확인')
        sales_btn_font = QtGui.QFont()
        sales_btn_font.setPointSize(20)
        sales_btn_font.setFamily("서울남산 장체M")
        self.sales_btn.setFont(sales_btn_font)
        self.sales_btn.setGeometry(QtCore.QRect(330, 530, 150, 150))
        self.sales_btn_dialogs = list()
        self.sales_btn.setStyleSheet('color:white; background:#0a326f')

        self.control_btn = QPushButton(self)
        self.control_btn.setText('공장 제어')
        control_btn_font = QtGui.QFont()
        control_btn_font.setPointSize(18)
        control_btn_font.setFamily("서울남산 장체M")
        self.control_btn.setFont(control_btn_font)
        self.control_btn.setGeometry(QtCore.QRect(530, 350, 150, 150))
        self.control_btn_dialogs = list()
        self.control_btn.setStyleSheet('color:white; background:#0a326f')

        self.manager_btn = QPushButton(self)
        self.manager_btn.setText('직원 관리')
        manager_btn_font = QtGui.QFont()
        manager_btn_font.setPointSize(18)
        manager_btn_font.setFamily("서울남산 장체M")
        self.manager_btn.setFont(manager_btn_font)
        self.manager_btn.setGeometry(QtCore.QRect(530, 530, 150, 150))
        self.manager_btn_dialogs = list()
        self.manager_btn.setStyleSheet('color:white; background:#0a326f')

        self.stock_btn = QPushButton(self)
        self.stock_btn.setText('재고 관리')
        stock_btn_font = QtGui.QFont()
        stock_btn_font.setPointSize(18)
        stock_btn_font.setFamily("서울남산 장체M")
        self.stock_btn.setFont(stock_btn_font)
        self.stock_btn.setGeometry(QtCore.QRect(730, 350, 150, 150))
        self.stock_btn_dialogs = list()
        self.stock_btn.setStyleSheet('color:white; background:#0a326f')

        self.logout_btn = QPushButton(self)
        self.logout_btn.setText('로그아웃')
        logout_btn_font = QtGui.QFont()
        logout_btn_font.setPointSize(9)
        logout_btn_font.setFamily("서울남산 장체M")
        self.logout_btn.setFont(logout_btn_font)
        self.logout_btn.setGeometry(QtCore.QRect(800, 230, 70, 30))
        self.logout_btn_dialogs = list()
        self.logout_btn.setStyleSheet('color:white; background:#0a326f')

        self.info_btn.clicked.connect(self.info_btn_clicked)
        self.control_btn.clicked.connect(self.control_btn_clicked)
        self.stock_btn.clicked.connect(self.stock_btn_clicked)
        self.sales_btn.clicked.connect(self.sales_btn_clicked)
        self.manager_btn.clicked.connect(self.management_btn_clicked)
        self.logout_btn.clicked.connect(self.logout_btn_clicked)

        self.info_btn.setCursor(QtGui.QCursor(QtCore.Qt.ClosedHandCursor))
        self.control_btn.setCursor(QtGui.QCursor(QtCore.Qt.ClosedHandCursor))
        self.stock_btn.setCursor(QtGui.QCursor(QtCore.Qt.ClosedHandCursor))
        self.sales_btn.setCursor(QtGui.QCursor(QtCore.Qt.ClosedHandCursor))
        self.manager_btn.setCursor(QtGui.QCursor(QtCore.Qt.ClosedHandCursor))
        self.logout_btn.setCursor(QtGui.QCursor(QtCore.Qt.ClosedHandCursor))

        self.logo = QLabel(self)
        self.logo.setGeometry(QtCore.QRect(-50, 30, 500, 100))
        icon = QPixmap("logo500.png")
        self.logo.setPixmap(QPixmap(icon))

        olmage = QImage("./back.JPG")
        slmage = olmage.scaled(QSize(1200, 800))
        palette = QPalette()
        palette.setBrush(10, QBrush(slmage))
        self.setPalette(palette)

        self.setGeometry(150, 100, 1200, 800)
        self.setWindowTitle('관리자 메뉴')
        self.show()

    def info_btn_clicked(self):
        self.close()
        info_btn_dialogs = manager_menu_infomenu(self)
        self.info_btn_dialogs.append(info_btn_dialogs)
        info_btn_dialogs.show()

    def control_btn_clicked(self):
        self.close()
        control_btn_dialogs = manager_menu_controlmenu(self)
        self.control_btn_dialogs.append(control_btn_dialogs)
        control_btn_dialogs.show()

    def stock_btn_clicked(self):
        self.close()
        stock_btn_dialogs = manager_menu_stockmenu(self)
        self.stock_btn_dialogs.append(stock_btn_dialogs)
        stock_btn_dialogs.show()

    def sales_btn_clicked(self):
        self.close()
        sales_btn_dialogs = manager_menu_salesmenu(self)
        self.sales_btn_dialogs.append(sales_btn_dialogs)
        sales_btn_dialogs.show()

    def management_btn_clicked(self):
        self.close()
        manager_btn_dialogs = manager_menu_managermenu(self)
        self.manager_btn_dialogs.append(manager_btn_dialogs)
        manager_btn_dialogs.show()

    def logout_btn_clicked(self):
        self.close()
        logout_btn_dialogs = login_window(self)
        self.logout_btn_dialogs.append(logout_btn_dialogs)
        logout_btn_dialogs.show()


# 관리자 메뉴 - 상품 정보 메뉴
class manager_menu_infomenu(QMainWindow):
    def __init__(self, parent=None):
        global datalist, datalist2, datalist3, datalist4, datalist5, datalist6
        global b
        super(manager_menu_infomenu, self).__init__(parent)

        con = pymysql.connect(host=HOST, user=USER, password=PASSWORD,
                              db=DB, charset='utf8', autocommit=True)
        curs = con.cursor()
        sql = "SELECT idproducts FROM timetable ORDER BY idtime DESC LIMIT 1"
        idx = curs.execute(sql)
        data = curs.fetchone()

        for j in range(0, idx):
            datalist = data[j]

        sql2 = "SELECT brand FROM pro_info where idproducts = %s"
        idx2 = curs.execute(sql2, datalist)
        data2 = curs.fetchone()

        for b in range(0, idx2):
            datalist2 = data2[b]
            print(datalist2)

        sql3 = "SELECT model FROM pro_info where idproducts = %s"
        idx3 = curs.execute(sql3, datalist)
        data3 = curs.fetchone()

        for c in range(0, idx3):
            datalist3 = data3[c]
            print(datalist3)

        sql4 = "SELECT codenum FROM pro_info where idproducts = %s"
        idx4 = curs.execute(sql4, datalist)
        data4 = curs.fetchone()

        for d in range(0, idx4):
            datalist4 = data4[d]
            print(datalist4)

        sql5 = "SELECT unitprice FROM pro_info where idproducts = %s"
        idx5 = curs.execute(sql5, datalist)
        data5 = curs.fetchone()

        for e in range(0, idx5):
            datalist5 = data5[b]
            print(datalist5)

        sql6 = "SELECT inventory FROM pro_info where idproducts = %s"
        idx6 = curs.execute(sql6, datalist)
        data6 = curs.fetchone()

        for e in range(0, idx6):
            datalist6 = data6[b]
            print(datalist6)

        self.mainlabel_txt = QLabel(self)
        self.mainlabel_txt.setText("상품 정보 확인")
        mainlabel_txt_font = QtGui.QFont()
        mainlabel_txt_font.setPointSize(20)
        mainlabel_txt_font.setFamily("서울남산 장체M")
        self.mainlabel_txt.setFont(mainlabel_txt_font)
        self.mainlabel_txt.setGeometry(QtCore.QRect(520, 220, 341, 41))

        self.brand_label = QLabel(self)
        self.brand_label.setText("· 상품 브랜드 :")
        brand_label_font = QtGui.QFont()
        brand_label_font.setPointSize(13)
        brand_label_font.setFamily("서울남산 장체M")
        self.brand_label.setFont(brand_label_font)
        self.brand_label.setGeometry(QtCore.QRect(400, 340, 150, 41))

        self.brand_txt = QLabel(self)
        self.brand_txt.setText(datalist2)
        brand_txt_font = QtGui.QFont()
        brand_txt_font.setPointSize(13)
        brand_txt_font.setFamily("서울남산 장체M")
        self.brand_txt.setFont(brand_txt_font)
        self.brand_txt.setGeometry(QtCore.QRect(550, 340, 150, 41))

        self.namelabel = QLabel(self)
        self.namelabel.setText("· 상품 종류 :")
        namelabel_font = QtGui.QFont()
        namelabel_font.setPointSize(13)
        namelabel_font.setFamily("서울남산 장체M")
        self.namelabel.setFont(namelabel_font)
        self.namelabel.setGeometry(QtCore.QRect(400, 400, 150, 41))

        self.namelabel = QLabel(self)
        self.namelabel.setText(datalist3)
        namelabel_font = QtGui.QFont()
        namelabel_font.setPointSize(13)
        namelabel_font.setFamily("서울남산 장체M")
        self.namelabel.setFont(namelabel_font)
        self.namelabel.setGeometry(QtCore.QRect(550, 400, 150, 41))

        self.codelabel = QLabel(self)
        self.codelabel.setText("· 상품 코드 :")
        codelabel_font = QtGui.QFont()
        codelabel_font.setPointSize(13)
        codelabel_font.setFamily("서울남산 장체M")
        self.codelabel.setFont(codelabel_font)
        self.codelabel.setGeometry(QtCore.QRect(400, 460, 150, 41))

        self.codelabel = QLabel(self)
        self.codelabel.setText(datalist4)
        codelabel_font = QtGui.QFont()
        codelabel_font.setPointSize(13)
        codelabel_font.setFamily("서울남산 장체M")
        self.codelabel.setFont(codelabel_font)
        self.codelabel.setGeometry(QtCore.QRect(550, 460, 150, 41))

        self.pricelabel = QLabel(self)
        self.pricelabel.setText("· 상품 단가 :")
        pricelabel_font = QtGui.QFont()
        pricelabel_font.setPointSize(13)
        pricelabel_font.setFamily("서울남산 장체M")
        self.pricelabel.setFont(pricelabel_font)
        self.pricelabel.setGeometry(QtCore.QRect(400, 520, 150, 41))

        self.pricelabel = QLabel(self)
        self.pricelabel.setText(datalist5)
        pricelabel_font = QtGui.QFont()
        pricelabel_font.setPointSize(13)
        pricelabel_font.setFamily("서울남산 장체M")
        self.pricelabel.setFont(pricelabel_font)
        self.pricelabel.setGeometry(QtCore.QRect(550, 520, 150, 41))

        self.pricelabel = QLabel(self)
        self.pricelabel.setText("· 상품 재고량 :")
        pricelabel_font = QtGui.QFont()
        pricelabel_font.setPointSize(13)
        pricelabel_font.setFamily("서울남산 장체M")
        self.pricelabel.setFont(pricelabel_font)
        self.pricelabel.setGeometry(QtCore.QRect(400, 580, 150, 41))

        self.pricelabel = QLabel(self)
        self.pricelabel.setText(datalist6)
        pricelabel_font = QtGui.QFont()
        pricelabel_font.setPointSize(13)
        pricelabel_font.setFamily("서울남산 장체M")
        self.pricelabel.setFont(pricelabel_font)
        self.pricelabel.setGeometry(QtCore.QRect(550, 580, 150, 41))

        self.logo = QLabel(self)
        self.logo.setGeometry(QtCore.QRect(-50, 30, 500, 100))
        icon = QPixmap("logo500.png")
        self.logo.setPixmap(QPixmap(icon))

        olmage = QImage("./back.JPG")
        slmage = olmage.scaled(QSize(1200, 800))
        palette = QPalette()
        palette.setBrush(10, QBrush(slmage))
        self.setPalette(palette)

        self.back_btn = QPushButton(self)
        self.back_btn.setGeometry(QtCore.QRect(0, 89, 80, 52))
        self.back_btn.setText("뒤로가기")
        back_btn_font = QtGui.QFont()
        back_btn_font.setPointSize(10)
        back_btn_font.setFamily("서울남산 장체M")
        self.back_btn.setFont(back_btn_font)
        self.back_btn.clicked.connect(self.back_btn_clicked)
        self.back_btn_dialogs = list()
        self.back_btn.setCursor(QtGui.QCursor(QtCore.Qt.ClosedHandCursor))
        self.back_btn.setStyleSheet('color:white; background-color:rgba(1, 0, 0, 0.1)')

        self.setGeometry(150, 100, 1200, 800)
        self.setWindowTitle('[관리자 메뉴] 상품 정보')
        self.show()

    def back_btn_clicked(self):
        self.close()
        back_btn_dialogs = manager_menu(self)
        self.back_btn_dialogs.append(back_btn_dialogs)
        back_btn_dialogs.show()


# 관리자 메뉴 - 공장 제어 메뉴
class manager_menu_controlmenu(QMainWindow):
    def __init__(self, parent=None):
        super(manager_menu_controlmenu, self).__init__(parent)

        self.mainlabel_txt = QLabel(self)
        self.mainlabel_txt.setText("레일 가동 제어")
        mainlabel_txt_font = QtGui.QFont()
        mainlabel_txt_font.setPointSize(15)
        mainlabel_txt_font.setFamily("서울남산 장체M")
        self.mainlabel_txt.setFont(mainlabel_txt_font)
        self.mainlabel_txt.setGeometry(QtCore.QRect(520, 250, 341, 41))

        self.motorON_btn = QPushButton(self)
        self.motorON_btn.setGeometry(QtCore.QRect(370, 400, 180, 180))
        self.motorON_btn.setText("ON")
        motorON_btn_font = QtGui.QFont()
        motorON_btn_font.setPointSize(20)
        motorON_btn_font.setFamily("서울남산 장체M")
        self.motorON_btn.setFont(motorON_btn_font)
        self.motorON_btn.clicked.connect(self.motorON_btn_clicked)
        # self.motorON_btn_dialogs = list()
        self.motorON_btn.setCursor(QtGui.QCursor(QtCore.Qt.ClosedHandCursor))
        self.motorON_btn.setStyleSheet('color:white; background:#0a326f')

        self.motorOFF_btn = QPushButton(self)
        self.motorOFF_btn.setGeometry(QtCore.QRect(650, 400, 180, 180))
        self.motorOFF_btn.setText("OFF")
        motorOFF_btn_font = QtGui.QFont()
        motorOFF_btn_font.setPointSize(20)
        motorOFF_btn_font.setFamily("서울남산 장체M")
        self.motorOFF_btn.setFont(motorOFF_btn_font)
        self.motorOFF_btn.clicked.connect(self.motorOFF_btn_clicked)
        # self.motorOFF_btn_dialogs = list()
        self.motorOFF_btn.setCursor(QtGui.QCursor(QtCore.Qt.ClosedHandCursor))
        self.motorOFF_btn.setStyleSheet('color:white; background:#0a326f')

        self.logo = QLabel(self)
        self.logo.setGeometry(QtCore.QRect(-50, 30, 500, 100))
        icon = QPixmap("logo500.png")
        self.logo.setPixmap(QPixmap(icon))

        olmage = QImage("./back.JPG")
        slmage = olmage.scaled(QSize(1200, 800))
        palette = QPalette()
        palette.setBrush(10, QBrush(slmage))
        self.setPalette(palette)

        self.back_btn = QPushButton(self)
        self.back_btn.setGeometry(QtCore.QRect(0, 89, 80, 52))
        self.back_btn.setText("뒤로가기")
        back_btn_font = QtGui.QFont()
        back_btn_font.setPointSize(10)
        back_btn_font.setFamily("서울남산 장체M")
        self.back_btn.setFont(back_btn_font)
        self.back_btn.clicked.connect(self.back_btn_clicked)
        self.back_btn_dialogs = list()
        self.back_btn.setCursor(QtGui.QCursor(QtCore.Qt.ClosedHandCursor))
        self.back_btn.setStyleSheet('color:white; background-color:rgba(1, 0, 0, 0.1)')

        self.setGeometry(150, 100, 1200, 800)
        self.setWindowTitle('[관리자 메뉴] 공장 제어')
        self.show()

    def back_btn_clicked(self):
        self.close()
        back_btn_dialogs = manager_menu(self)
        self.back_btn_dialogs.append(back_btn_dialogs)
        back_btn_dialogs.show()

    def motorON_btn_clicked(self):
        print("ON")

    def motorOFF_btn_clicked(self):
        print("OFF")


# 관리자 메뉴 - 재고 관리 메뉴
class manager_menu_stockmenu(QMainWindow):
    con = pymysql.connect(host=HOST, user=USER, password=PASSWORD, db=DB, charset='utf8')
    cur_num = con.cursor()
    sql_num = "SELECT * FROM pro_info;"
    cur_num.execute(sql_num)
    data_num = cur_num.fetchall()

    li_num = len([x[0] for x in data_num])

    def __init__(self, parent=None):
        super(manager_menu_stockmenu, self).__init__(parent)
        # global li_num
        con = pymysql.connect(host=HOST, user=USER, password=PASSWORD, db=DB, charset='utf8')
        cur_num = con.cursor()
        sql_num = "SELECT * FROM pro_info;"
        cur_num.execute(sql_num)
        data_num = cur_num.fetchall()
        li_num = [x[0] for x in data_num]

        self.mainlabel_txt = QLabel(self)
        self.mainlabel_txt.setText("재고 관리 및 수정")
        mainlabel_txt_font = QtGui.QFont()
        mainlabel_txt_font.setPointSize(15)
        mainlabel_txt_font.setFamily("서울남산 장체M")
        self.mainlabel_txt.setFont(mainlabel_txt_font)
        self.mainlabel_txt.setGeometry(QtCore.QRect(520, 250, 341, 41))

        # 테이블 설정
        self.stock_table = QTableWidget(self)
        self.stock_table.setColumnCount(5)
        self.stock_table.setRowCount(len(li_num))
        self.stock_table.setGeometry(QtCore.QRect(350, 320, 521, 247))
        self.stock_table.setHorizontalHeaderLabels(["브랜드", "종류", "모델명", "가격", "재고량"])

        pro_len = len(li_num)
        # 테이블위젯 - 데이터베이스 연동
        for x in range(pro_len):
            for i in range(0, 5):
                li = [x[i+1] for x in data_num]
                self.stock_table.setItem(x, i, QTableWidgetItem(li[x]))

        self.stock_add_btn = QPushButton(self)
        self.stock_add_btn.setGeometry(QtCore.QRect(350, 600, 130, 50))
        self.stock_add_btn.setText("상품 추가")
        stock_add_btn_font = QtGui.QFont()
        stock_add_btn_font.setPointSize(10)
        stock_add_btn_font.setFamily("서울남산 장체M")
        self.stock_add_btn.setFont(stock_add_btn_font)
        self.stock_add_btn.clicked.connect(self.stock_add_btn_clicked)
        self.stock_add_btn_dialogs = list()
        self.stock_add_btn.setCursor(QtGui.QCursor(QtCore.Qt.ClosedHandCursor))
        self.stock_add_btn.setStyleSheet('color:white; background:#0a326f')

        self.stock_edit_btn = QPushButton(self)
        self.stock_edit_btn.setGeometry(QtCore.QRect(530, 600, 130, 50))
        self.stock_edit_btn.setText("재고 수정")
        stock_edit_btn_font = QtGui.QFont()
        stock_edit_btn_font.setPointSize(10)
        stock_edit_btn_font.setFamily("서울남산 장체M")
        self.stock_edit_btn.setFont(stock_edit_btn_font)
        self.stock_edit_btn.clicked.connect(self.stock_edit_btn_clicked)
        self.stock_edit_btn_dialogs = list()
        self.stock_edit_btn.setCursor(QtGui.QCursor(QtCore.Qt.ClosedHandCursor))
        self.stock_edit_btn.setStyleSheet('color:white; background:#0a326f')

        self.stock_delete_btn = QPushButton(self)
        self.stock_delete_btn.setGeometry(QtCore.QRect(720, 600, 130, 50))
        self.stock_delete_btn.setText("상품 삭제")
        stock_delete_font = QtGui.QFont()
        stock_delete_font.setPointSize(10)
        stock_delete_font.setFamily("서울남산 장체M")
        self.stock_delete_btn.setFont(stock_delete_font)
        self.stock_delete_btn.clicked.connect(self.stock_delete_btn_clicked)
        self.stock_delete_btn_dialogs = list()
        self.stock_delete_btn.setCursor(QtGui.QCursor(QtCore.Qt.ClosedHandCursor))
        self.stock_delete_btn.setStyleSheet('color:white; background:#0a326f')

        # 테이블 수정 금지 모드
        self.stock_table.setEditTriggers(QAbstractItemView.NoEditTriggers)

        self.logo = QLabel(self)
        self.logo.setGeometry(QtCore.QRect(-50, 30, 500, 100))
        icon = QPixmap("logo500.png")
        self.logo.setPixmap(QPixmap(icon))

        olmage = QImage("./back.JPG")
        slmage = olmage.scaled(QSize(1200, 800))
        palette = QPalette()
        palette.setBrush(10, QBrush(slmage))
        self.setPalette(palette)

        self.back_btn = QPushButton(self)
        self.back_btn.setGeometry(QtCore.QRect(0, 89, 80, 52))
        self.back_btn.setText("뒤로가기")
        back_btn_font = QtGui.QFont()
        back_btn_font.setPointSize(10)
        back_btn_font.setFamily("서울남산 장체M")
        self.back_btn.setFont(back_btn_font)
        self.back_btn.clicked.connect(self.back_btn_clicked)
        self.back_btn_dialogs = list()
        self.back_btn.setCursor(QtGui.QCursor(QtCore.Qt.ClosedHandCursor))
        self.back_btn.setStyleSheet('color:white; background-color:rgba(1, 0, 0, 0.1)')

        # manager_menu_stockmenu.update()

        self.setGeometry(150, 100, 1200, 800)
        self.setWindowTitle('[관리자 메뉴] 재고 관리')
        self.show()

    def stock_add_btn_clicked(self):
        self.close()
        stock_add_btn_dialogs = manager_stock_add(self)
        self.stock_add_btn_dialogs.append(stock_add_btn_dialogs)
        stock_add_btn_dialogs.show()

    def stock_edit_btn_clicked(self):
        self.close()
        stock_edit_btn_dialogs = manager_stock_edit(self)
        self.stock_edit_btn_dialogs.append(stock_edit_btn_dialogs)
        stock_edit_btn_dialogs.show()

    def stock_delete_btn_clicked(self):
        self.close()
        stock_delete_btn_dialogs = manager_stock_delete(self)
        self.stock_delete_btn_dialogs.append(stock_delete_btn_dialogs)
        stock_delete_btn_dialogs.show()

    def back_btn_clicked(self):
        self.close()
        back_btn_dialogs = manager_menu(self)
        self.back_btn_dialogs.append(back_btn_dialogs)
        back_btn_dialogs.show()

    def stock_num(self):
        print(len(self.li_num))


# 관리자 메뉴 - 재고 관리 - 상품 추가 화면
class manager_stock_add(QMainWindow):
    def __init__(self, parent=None):
        super(manager_stock_add, self).__init__(parent)

        self.mainlabel_txt = QLabel(self)
        self.mainlabel_txt.setText("상품 추가")
        mainlabel_txt_font = QtGui.QFont()
        mainlabel_txt_font.setPointSize(15)
        mainlabel_txt_font.setFamily("서울남산 장체M")
        self.mainlabel_txt.setFont(mainlabel_txt_font)
        self.mainlabel_txt.setGeometry(QtCore.QRect(560, 250, 350, 40))

        self.brand = QLabel(self)
        self.brand.setText("상품 브랜드 : ")
        brand_font = QtGui.QFont()
        brand_font.setPointSize(10)
        brand_font.setFamily("서울남산 장체M")
        self.brand.setFont(brand_font)
        self.brand.setGeometry(QtCore.QRect(400, 350, 350, 60))

        self.kinds = QLabel(self)
        self.kinds.setText("상품 종류 : ")
        kinds_font = QtGui.QFont()
        kinds_font.setPointSize(10)
        kinds_font.setFamily("서울남산 장체M")
        self.kinds.setFont(kinds_font)
        self.kinds.setGeometry(QtCore.QRect(400, 390, 350, 60))

        self.model_name = QLabel(self)
        self.model_name.setText("상품 모델명 : ")
        model_name_font = QtGui.QFont()
        model_name_font.setPointSize(10)
        model_name_font.setFamily("서울남산 장체M")
        self.model_name.setFont(model_name_font)
        self.model_name.setGeometry(QtCore.QRect(400, 430, 350, 60))

        self.price = QLabel(self)
        self.price.setText("상품 가격 : ")
        price_font = QtGui.QFont()
        price_font.setPointSize(10)
        price_font.setFamily("서울남산 장체M")
        self.price.setFont(price_font)
        self.price.setGeometry(QtCore.QRect(400, 470, 350, 60))

        self.inventory = QLabel(self)
        self.inventory.setText("상품 재고량 : ")
        inventory_font = QtGui.QFont()
        inventory_font.setPointSize(10)
        inventory_font.setFamily("서울남산 장체M")
        self.inventory.setFont(inventory_font)
        self.inventory.setGeometry(QtCore.QRect(400, 510, 350, 60))

        self.brand_txt = QLineEdit(self)
        self.brand_txt.setText("")
        brand_txt_font = QtGui.QFont()
        brand_txt_font.setPointSize(10)
        brand_txt_font.setFamily("서울남산 장체M")
        self.brand_txt.setFont(brand_txt_font)
        self.brand_txt.setGeometry(QtCore.QRect(500, 365, 230, 30))

        self.kinds_txt = QLineEdit(self)
        self.kinds_txt.setText("")
        kinds_txt_font = QtGui.QFont()
        kinds_txt_font.setPointSize(10)
        kinds_txt_font.setFamily("서울남산 장체M")
        self.kinds_txt.setFont(kinds_txt_font)
        self.kinds_txt.setGeometry(QtCore.QRect(500, 405, 230, 30))

        self.model_txt = QLineEdit(self)
        self.model_txt.setText("")
        model_txt_font = QtGui.QFont()
        model_txt_font.setPointSize(10)
        model_txt_font.setFamily("서울남산 장체M")
        self.model_txt.setFont(model_txt_font)
        self.model_txt.setGeometry(QtCore.QRect(500, 445, 230, 30))

        self.price_txt = QLineEdit(self)
        self.price_txt.setText("")
        price_txt_font = QtGui.QFont()
        price_txt_font.setPointSize(10)
        price_txt_font.setFamily("서울남산 장체M")
        self.price_txt.setFont(price_txt_font)
        self.price_txt.setGeometry(QtCore.QRect(500, 485, 230, 30))

        self.inventory_txt = QLineEdit(self)
        self.inventory_txt.setText("")
        inventory_txt_font = QtGui.QFont()
        inventory_txt_font.setPointSize(10)
        inventory_txt_font.setFamily("서울남산 장체M")
        self.inventory_txt.setFont(inventory_txt_font)
        self.inventory_txt.setGeometry(QtCore.QRect(500, 525, 230, 30))

        self.stock_add_alarm_btn = QPushButton(self)
        self.stock_add_alarm_btn.setGeometry(QtCore.QRect(530, 600, 130, 50))
        self.stock_add_alarm_btn.setText("저장")
        stock_add_alarm_btn_font = QtGui.QFont()
        stock_add_alarm_btn_font.setPointSize(10)
        stock_add_alarm_btn_font.setFamily("서울남산 장체M")
        self.stock_add_alarm_btn.setFont(stock_add_alarm_btn_font)
        self.stock_add_alarm_btn.clicked.connect(self.stock_add_alarm_btn_clicked)
        self.stock_add_alarm_btn_dialogs = list()
        self.stock_add_alarm_btn.setCursor(QtGui.QCursor(QtCore.Qt.ClosedHandCursor))
        self.stock_add_alarm_btn.setStyleSheet('color:white; background:#0a326f')

        self.logo = QLabel(self)
        self.logo.setGeometry(QtCore.QRect(-50, 30, 500, 100))
        icon = QPixmap("logo500.png")
        self.logo.setPixmap(QPixmap(icon))

        olmage = QImage("./back.JPG")
        slmage = olmage.scaled(QSize(1200, 800))
        palette = QPalette()
        palette.setBrush(10, QBrush(slmage))
        self.setPalette(palette)

        self.back_btn = QPushButton(self)
        self.back_btn.setGeometry(QtCore.QRect(0, 89, 80, 52))
        self.back_btn.setText("뒤로가기")
        back_btn_font = QtGui.QFont()
        back_btn_font.setPointSize(10)
        back_btn_font.setFamily("서울남산 장체M")
        self.back_btn.setFont(back_btn_font)
        self.back_btn.clicked.connect(self.back_btn_clicked)
        self.back_btn_dialogs = list()
        self.back_btn.setCursor(QtGui.QCursor(QtCore.Qt.ClosedHandCursor))
        self.back_btn.setStyleSheet('color:white; background-color:rgba(1, 0, 0, 0.1)')

        self.setGeometry(150, 100, 1200, 800)
        self.setWindowTitle('[관리자 메뉴] 재고 관리 - 상품 추가')
        self.show()

    def stock_add_alarm_btn_clicked(self):
        con = pymysql.connect(host=HOST, user=USER, password=PASSWORD, db=DB, charset='utf8', autocommit=True)
        # cur_num = con.cursor()
        cur_insert = con.cursor()

        sql_num = "SELECT * FROM pro_info;"
        cur_insert.execute(
            "INSERT INTO pro_info(brand, model, codenum, unitprice, inventory) VALUES('%s', '%s', '%s', '%s', '%s')" % (
                ''.join(self.brand_txt.text()), ''.join(self.kinds_txt.text()), ''.join(self.model_txt.text()),
                ''.join(self.price_txt.text()), ''.join(self.inventory_txt.text())))

        # sql_insert = "INSERT INTO pro_info (brand, kinds, model, price, inventory)"

        # data_num = cur_num.fetchall()
        # data_insert = cur_insert.fetchall()
        #
        # li_num = [x[0] for x in data_num]
        # li_brand = [x[0] for x in data_insert]

        # cur_insert.execute(sql_insert, (self.brand_txt.text(), self.kinds_txt.text(),
        #                                 self.model_txt.text(), self.price_txt.text(),
        #                                 self.inventory_txt.text()))

        self.close()
        stock_add_alarm_btn_dialogs = manager_menu_stockmenu(self)
        self.stock_add_alarm_btn_dialogs.append(stock_add_alarm_btn_dialogs)
        stock_add_alarm_btn_dialogs.show()

    def back_btn_clicked(self):
        self.close()
        back_btn_dialogs = manager_menu_stockmenu(self)
        self.back_btn_dialogs.append(back_btn_dialogs)
        back_btn_dialogs.show()


# 관리자 메뉴 - 재고 관리 - 재고 수정 화면
class manager_stock_edit(QMainWindow):
    def __init__(self, parent=None):
        super(manager_stock_edit, self).__init__(parent)

        self.model_combobox = QComboBox(self)
        self.model_combobox.setGeometry(QtCore.QRect(720, 350, 100, 30))
        self.model_combobox.setStyleSheet('color:white; background:#0a326f')

        self.kinds_combobox = QComboBox(self)
        self.kinds_combobox.setGeometry(QtCore.QRect(560, 350, 100, 30))
        self.kinds_combobox.setStyleSheet('color:white; background:#0a326f')

        con = pymysql.connect(host=HOST, user=USER, password=PASSWORD, db=DB, charset='utf8', autocommit=True)

        cur_brand = con.cursor()
        sql_brand = "SELECT distinct brand FROM pro_info;"
        cur_brand.execute(sql_brand)
        data_brand = cur_brand.fetchall()
        li_brand = [x[0] for x in data_brand]

        self.mainlabel_txt = QLabel(self)
        self.mainlabel_txt.setText("재고 수정")
        mainlabel_txt_font = QtGui.QFont()
        mainlabel_txt_font.setPointSize(15)
        mainlabel_txt_font.setFamily("서울남산 장체M")
        self.mainlabel_txt.setFont(mainlabel_txt_font)
        self.mainlabel_txt.setGeometry(QtCore.QRect(560, 250, 341, 41))

        #
        # # 테이블 설정
        # self.stock_table = QTableWidget(self)
        # self.stock_table.setColumnCount(7)
        # self.stock_table.setRowCount(len(li_num))
        # self.stock_table.setGeometry(QtCore.QRect(50, 120, 500, 250))
        # self.stock_table.setHorizontalHeaderLabels([
        #     "상품 번호", "브랜드", "종류", "모델명", "가격", "재고량", "출하량"])
        #
        # pro_len = len(li_num)
        # # 테이블위젯 - 데이터베이스 연동
        # for x in range(pro_len):
        #     for i in range(0, 7):
        #         li = [x[i] for x in data_num]
        #         self.stock_table.setItem(x, i, QTableWidgetItem(li[x]))

        # self.stock_table.itemClicked.connect(self.item_clicked)

        self.brand = QLabel(self)
        self.brand.setText("브랜드")
        brand_font = QtGui.QFont()
        brand_font.setPointSize(10)
        brand_font.setFamily("서울남산 장체M")
        self.brand.setFont(brand_font)
        self.brand.setGeometry(QtCore.QRect(420, 320, 100, 30))

        self.brand_combobox = QComboBox(self)
        self.brand_combobox.addItem('')
        self.brand_combobox.addItems(li_brand)
        self.brand_combobox.activated.connect(self.brand_combo_change)
        self.brand_combobox.setGeometry(QtCore.QRect(400, 350, 100, 30))
        self.brand_combobox.setStyleSheet('color:white; background:#0a326f')

        self.kinds = QLabel(self)
        self.kinds.setText("종류")
        kinds_font = QtGui.QFont()
        kinds_font.setPointSize(10)
        kinds_font.setFamily("서울남산 장체M")
        self.kinds.setFont(kinds_font)
        self.kinds.setGeometry(QtCore.QRect(590, 320, 100, 30))

        #
        cur_search_brand = con.cursor()
        sql_search_brand = "SELECT distinct model FROM pro_info WHERE brand = %s;"
        cur_search_brand.execute(sql_search_brand, (self.brand_combobox.currentText()))
        data_search_brand = cur_search_brand.fetchall()
        li_search_brand = [x[0] for x in data_search_brand]
        #

        self.model = QLabel(self)
        self.model.setText("모델명")
        model_font = QtGui.QFont()
        model_font.setPointSize(10)
        model_font.setFamily("서울남산 장체M")
        self.model.setFont(model_font)
        self.model.setGeometry(QtCore.QRect(740, 320, 100, 30))

        #
        self.model = QLabel(self)
        self.model.setText("재고량을")
        model_font = QtGui.QFont()
        model_font.setPointSize(15)
        model_font.setFamily("서울남산 장체M")
        self.model.setFont(model_font)
        self.model.setGeometry(QtCore.QRect(480, 500, 100, 30))

        self.inventory_num_txt = QLineEdit(self)
        self.inventory_num_txt.setText("")
        inventory_num_font = QtGui.QFont()
        inventory_num_font.setPointSize(15)
        inventory_num_font.setFamily("서울남산 장체M")
        self.inventory_num_txt.setFont(inventory_num_font)
        self.inventory_num_txt.setGeometry(QtCore.QRect(590, 500, 55, 30))

        self.model = QLabel(self)
        self.model.setText("개로 변경.")
        mode_font = QtGui.QFont()
        model_font.setPointSize(15)
        model_font.setFamily("서울남산 장체M")
        self.model.setFont(model_font)
        self.model.setGeometry(QtCore.QRect(650, 500, 100, 30))
        #

        self.stock_add_alarm_btn = QPushButton(self)
        self.stock_add_alarm_btn.setGeometry(QtCore.QRect(530, 600, 130, 50))
        self.stock_add_alarm_btn.setText("저장")
        stock_add_alarm_btn_font = QtGui.QFont()
        stock_add_alarm_btn_font.setPointSize(10)
        stock_add_alarm_btn_font.setFamily("서울남산 장체M")
        self.stock_add_alarm_btn.setFont(stock_add_alarm_btn_font)
        self.stock_add_alarm_btn.clicked.connect(self.stock_add_alarm_btn_clicked)
        self.stock_add_alarm_btn_dialogs = list()
        self.stock_add_alarm_btn.setCursor(QtGui.QCursor(QtCore.Qt.ClosedHandCursor))
        self.stock_add_alarm_btn.setStyleSheet('color:white; background:#0a326f')

        self.logo = QLabel(self)
        self.logo.setGeometry(QtCore.QRect(-50, 30, 500, 100))
        icon = QPixmap("logo500.png")
        self.logo.setPixmap(QPixmap(icon))

        olmage = QImage("./back.JPG")
        slmage = olmage.scaled(QSize(1200, 800))
        palette = QPalette()
        palette.setBrush(10, QBrush(slmage))
        self.setPalette(palette)

        self.back_btn = QPushButton(self)
        self.back_btn.setGeometry(QtCore.QRect(0, 89, 80, 52))
        self.back_btn.setText("뒤로가기")
        back_btn_font = QtGui.QFont()
        back_btn_font.setPointSize(10)
        back_btn_font.setFamily("서울남산 장체M")
        self.back_btn.setFont(back_btn_font)
        self.back_btn.clicked.connect(self.back_btn_clicked)
        self.back_btn_dialogs = list()
        self.back_btn.setCursor(QtGui.QCursor(QtCore.Qt.ClosedHandCursor))
        self.back_btn.setStyleSheet('color:white; background-color:rgba(1, 0, 0, 0.1)')

        self.setGeometry(150, 100, 1200, 800)
        self.setWindowTitle('[관리자 메뉴] 재고 관리 - 재고 수정')
        self.show()

    def brand_combo_change(self):
        print(self.brand_combobox.currentText())
        con = pymysql.connect(host=HOST, user=USER, password=PASSWORD, db=DB, charset='utf8', autocommit=True)

        cur_search_brand = con.cursor()
        sql_search_brand = "SELECT distinct model FROM pro_info WHERE brand = %s;"
        cur_search_brand.execute(sql_search_brand, (self.brand_combobox.currentText()))
        data_search_brand = cur_search_brand.fetchall()
        li_search_brand = [x[0] for x in data_search_brand]

        self.kinds_combobox.addItem('')
        self.kinds_combobox.addItems(li_search_brand)
        self.kinds_combobox.activated.connect(self.kinds_combo_change)
        self.kinds_combobox.setGeometry(QtCore.QRect(560, 350, 100, 30))

    def kinds_combo_change(self):
        print(self.kinds_combobox.currentText())
        con = pymysql.connect(host=HOST, user=USER, password=PASSWORD, db=DB, charset='utf8', autocommit=True)

        cur_search_model = con.cursor()
        sql_search_model = "SELECT distinct codenum FROM pro_info WHERE model = %s and brand = %s;"
        cur_search_model.execute(sql_search_model,
                                 (self.kinds_combobox.currentText(), self.brand_combobox.currentText()))
        data_search_model = cur_search_model.fetchall()
        li_search_model = [x[0] for x in data_search_model]

        self.model_combobox.addItem('')
        self.model_combobox.addItems(li_search_model)
        self.model_combobox.activated.connect(self.model_combo_change)
        self.model_combobox.setGeometry(QtCore.QRect(720, 350, 100, 30))

    def model_combo_change(self):
        print(self.model_combobox.currentText())

    def stock_add_alarm_btn_clicked(self):
        con = pymysql.connect(host=HOST, user=USER, password=PASSWORD, db=DB, charset='utf8', autocommit=True)
        cur = con.cursor()
        sql_up = "UPDATE pro_info SET inventory = %s WHERE brand = %s and model = %s and codenum = %s;"
        cur.execute(sql_up, (
            self.inventory_num_txt.text(), self.brand_combobox.currentText(), self.kinds_combobox.currentText(),
            self.model_combobox.currentText()))

        print(self.inventory_num_txt.text())

        self.close()
        stock_add_alarm_btn_dialogs = manager_menu_stockmenu(self)
        self.stock_add_alarm_btn_dialogs.append(stock_add_alarm_btn_dialogs)
        stock_add_alarm_btn_dialogs.show()

    def back_btn_clicked(self):
        self.close()
        back_btn_dialogs = manager_menu_stockmenu(self)
        self.back_btn_dialogs.append(back_btn_dialogs)
        back_btn_dialogs.show()


# 관리자 메뉴 - 재고 관리 - 상품 삭제 화면
class manager_stock_delete(QMainWindow):
    def __init__(self, parent=None):
        super(manager_stock_delete, self).__init__(parent)

        self.model_txtB = QTextBrowser(self)
        self.model_txtB.setGeometry(QtCore.QRect(390, 500, 430, 80))

        self.model_combobox = QComboBox(self)
        self.model_combobox.setGeometry(QtCore.QRect(720, 350, 100, 30))
        self.model_combobox.setStyleSheet('color:white; background:#0a326f')

        self.kinds_combobox = QComboBox(self)
        self.kinds_combobox.setGeometry(QtCore.QRect(560, 350, 100, 30))
        self.kinds_combobox.setStyleSheet('color:white; background:#0a326f')

        con = pymysql.connect(host=HOST, user=USER, password=PASSWORD, db=DB, charset='utf8', autocommit=True)

        cur_brand = con.cursor()
        sql_brand = "SELECT distinct brand FROM pro_info;"
        cur_brand.execute(sql_brand)
        data_brand = cur_brand.fetchall()
        li_brand = [x[0] for x in data_brand]

        self.mainlabel_txt = QLabel(self)
        self.mainlabel_txt.setText("재고 삭제")
        mainlabel_txt_font = QtGui.QFont()
        mainlabel_txt_font.setPointSize(15)
        mainlabel_txt_font.setFamily("서울남산 장체M")
        self.mainlabel_txt.setFont(mainlabel_txt_font)
        self.mainlabel_txt.setGeometry(QtCore.QRect(560, 250, 341, 41))

        #
        # # 테이블 설정
        # self.stock_table = QTableWidget(self)
        # self.stock_table.setColumnCount(7)
        # self.stock_table.setRowCount(len(li_num))
        # self.stock_table.setGeometry(QtCore.QRect(50, 120, 500, 250))
        # self.stock_table.setHorizontalHeaderLabels([
        #     "상품 번호", "브랜드", "종류", "모델명", "가격", "재고량", "출하량"])
        #
        # pro_len = len(li_num)
        # # 테이블위젯 - 데이터베이스 연동
        # for x in range(pro_len):
        #     for i in range(0, 7):
        #         li = [x[i] for x in data_num]
        #         self.stock_table.setItem(x, i, QTableWidgetItem(li[x]))

        # self.stock_table.itemClicked.connect(self.item_clicked)

        self.brand = QLabel(self)
        self.brand.setText("브랜드")
        brand_font = QtGui.QFont()
        brand_font.setPointSize(10)
        brand_font.setFamily("서울남산 장체M")
        self.brand.setFont(brand_font)
        self.brand.setGeometry(QtCore.QRect(420, 320, 100, 30))

        self.brand_combobox = QComboBox(self)
        self.brand_combobox.addItem('')
        self.brand_combobox.addItems(li_brand)
        self.brand_combobox.activated.connect(self.brand_combo_change)
        self.brand_combobox.setGeometry(QtCore.QRect(400, 350, 100, 30))
        self.brand_combobox.setStyleSheet('color:white; background:#0a326f')

        self.kinds = QLabel(self)
        self.kinds.setText("종류")
        kinds_font = QtGui.QFont()
        kinds_font.setPointSize(10)
        kinds_font.setFamily("서울남산 장체M")
        self.kinds.setFont(kinds_font)
        self.kinds.setGeometry(QtCore.QRect(590, 320, 100, 30))

        #
        cur_search_brand = con.cursor()
        sql_search_brand = "SELECT distinct model FROM pro_info WHERE brand = %s;"
        cur_search_brand.execute(sql_search_brand, (self.brand_combobox.currentText()))
        data_search_brand = cur_search_brand.fetchall()
        li_search_brand = [x[0] for x in data_search_brand]
        #

        self.model = QLabel(self)
        self.model.setText("모델명")
        model_font = QtGui.QFont()
        model_font.setPointSize(10)
        model_font.setFamily("서울남산 장체M")
        self.model.setFont(model_font)
        self.model.setGeometry(QtCore.QRect(740, 320, 100, 30))

        #

        #

        self.stock_add_alarm_btn = QPushButton(self)
        self.stock_add_alarm_btn.setGeometry(QtCore.QRect(530, 600, 130, 50))
        self.stock_add_alarm_btn.setText("삭제")
        stock_add_alarm_btn_font = QtGui.QFont()
        stock_add_alarm_btn_font.setPointSize(10)
        stock_add_alarm_btn_font.setFamily("서울남산 장체M")
        self.stock_add_alarm_btn.setFont(stock_add_alarm_btn_font)
        self.stock_add_alarm_btn.clicked.connect(self.stock_add_alarm_btn_clicked)
        self.stock_add_alarm_btn_dialogs = list()
        self.stock_add_alarm_btn.setCursor(QtGui.QCursor(QtCore.Qt.ClosedHandCursor))
        self.stock_add_alarm_btn.setStyleSheet('color:white; background:#0a326f')

        self.logo = QLabel(self)
        self.logo.setGeometry(QtCore.QRect(-50, 30, 500, 100))
        icon = QPixmap("logo500.png")
        self.logo.setPixmap(QPixmap(icon))

        olmage = QImage("./back.JPG")
        slmage = olmage.scaled(QSize(1200, 800))
        palette = QPalette()
        palette.setBrush(10, QBrush(slmage))
        self.setPalette(palette)

        self.back_btn = QPushButton(self)
        self.back_btn.setGeometry(QtCore.QRect(0, 89, 80, 52))
        self.back_btn.setText("뒤로가기")
        back_btn_font = QtGui.QFont()
        back_btn_font.setPointSize(10)
        back_btn_font.setFamily("서울남산 장체M")
        self.back_btn.setFont(back_btn_font)
        self.back_btn.clicked.connect(self.back_btn_clicked)
        self.back_btn_dialogs = list()
        self.back_btn.setCursor(QtGui.QCursor(QtCore.Qt.ClosedHandCursor))
        self.back_btn.setStyleSheet('color:white; background-color:rgba(1, 0, 0, 0.1)')

        self.setGeometry(150, 100, 1200, 800)
        self.setWindowTitle('[관리자 메뉴] 재고 관리 - 재고 삭제')
        self.show()

    def brand_combo_change(self):
        con = pymysql.connect(host=HOST, user=USER, password=PASSWORD, db=DB, charset='utf8', autocommit=True)

        cur_search_brand = con.cursor()
        sql_search_brand = "SELECT distinct model FROM pro_info WHERE brand = %s;"
        cur_search_brand.execute(sql_search_brand, (self.brand_combobox.currentText()))
        data_search_brand = cur_search_brand.fetchall()
        li_search_brand = [x[0] for x in data_search_brand]

        self.kinds_combobox.addItem('')
        self.kinds_combobox.addItems(li_search_brand)
        self.kinds_combobox.activated.connect(self.kinds_combo_change)
        self.kinds_combobox.setGeometry(QtCore.QRect(560, 350, 100, 30))

    def kinds_combo_change(self):
        con = pymysql.connect(host=HOST, user=USER, password=PASSWORD, db=DB, charset='utf8', autocommit=True)

        cur_search_model = con.cursor()
        sql_search_model = "SELECT distinct codenum FROM pro_info WHERE model = %s and brand = %s;"
        cur_search_model.execute(sql_search_model,
                                 (self.kinds_combobox.currentText(), self.brand_combobox.currentText()))
        data_search_model = cur_search_model.fetchall()
        li_search_model = [x[0] for x in data_search_model]

        self.model_combobox.addItem('')
        self.model_combobox.addItems(li_search_model)
        self.model_combobox.activated.connect(self.model_combo_change)
        self.model_combobox.setGeometry(QtCore.QRect(720, 350, 100, 30))

    def model_combo_change(self):
        BRAND = self.brand_combobox.currentText()
        KINDS = self.kinds_combobox.currentText()
        MODEL = self.model_combobox.currentText()

        self.model_txtB.setText('''"''' + BRAND + '''" 의 ''' + KINDS + "'인 [" + MODEL + "]를 삭제하시겠습니까?")
        model_txtB_font = QtGui.QFont()
        model_txtB_font.setPointSize(10)
        model_txtB_font.setFamily("서울남산 장체M")
        self.model_txtB.setFont(model_txtB_font)
        self.model_txtB.setGeometry(QtCore.QRect(390, 500, 430, 80))

    def stock_add_alarm_btn_clicked(self):
        con = pymysql.connect(host=HOST, user=USER, password=PASSWORD, db=DB, charset='utf8', autocommit=True)
        cur = con.cursor()
        sql_del = "DELETE FROM pro_info WHERE brand = %s and model = %s and codenum = %s;"
        cur.execute(sql_del, (
            self.brand_combobox.currentText(), self.kinds_combobox.currentText(),
            self.model_combobox.currentText()))

        # sql_1 = "ALTER TABLE pro_info DROP idproducts"
        # sql_2 = "ALTER TABLE pro_info ADD idproducts INT PRIMARY KEY NOT NULL AUTO_INCREMENT FIRST;"
        #
        # cur.execute(sql_1)
        # cur.execute(sql_2)

        self.close()
        stock_add_alarm_btn_dialogs = manager_menu_stockmenu(self)
        self.stock_add_alarm_btn_dialogs.append(stock_add_alarm_btn_dialogs)
        stock_add_alarm_btn_dialogs.show()

    def back_btn_clicked(self):
        self.close()
        back_btn_dialogs = manager_menu_stockmenu(self)
        self.back_btn_dialogs.append(back_btn_dialogs)
        back_btn_dialogs.show()


# 관리자 메뉴 - 매출 확인 메뉴
class manager_menu_salesmenu(QMainWindow):
    def __init__(self, parent=None):
        super(manager_menu_salesmenu, self).__init__(parent)

        self.profile = QLabel(self)
        con = pymysql.connect(host=HOST, user=USER, password=PASSWORD, db=DB, charset='utf8', autocommit=True)
        cur1 = con.cursor()
        sql1 = "SELECT distinct date1 FROM timetable ORDER BY date1 ASC"
        cur1.execute(sql1)
        li = [data[0] for data in cur1.fetchall()]

        self.stock_date = QComboBox(self)
        self.stock_date.addItem('')
        self.stock_date.addItems(li)
        stock_date_font = QtGui.QFont()
        stock_date_font.setPointSize(15)
        stock_date_font.setFamily("서울남산 장체M")
        self.stock_date.setFont(stock_date_font)
        self.stock_date.setGeometry(QtCore.QRect(450, 220, 250, 40))
        self.stock_date.setStyleSheet('color:white; background:#0a326f')

        # self.stock_sales_label = QLabel(self)
        # stock_sales_label_font = QtGui.QFont()
        # stock_sales_label_font.setPointSize(15)
        # stock_sales_label_font.setFamily("서울남산 장체M")
        # self.stock_sales_label.setFont(stock_sales_label_font)
        # self.stock_sales_label.setGeometry(QtCore.QRect(220, 520, 800, 40))

        self.stock_btn = QPushButton(self)
        self.stock_btn.setText('선택')
        stock_btn_font = QtGui.QFont()
        stock_btn_font.setPointSize(15)
        stock_btn_font.setFamily("서울남산 장체M")
        self.stock_btn.setFont(stock_btn_font)
        self.stock_btn.setGeometry(QtCore.QRect(800, 220, 100, 40))
        self.stock_btn.clicked.connect(self.stock_btn_clicked)
        self.stock_btn_dialogs = list()
        self.stock_btn.setCursor(QtGui.QCursor(QtCore.Qt.ClosedHandCursor))
        self.stock_btn.setStyleSheet('color:white; background:#0a326f')

        self.logo = QLabel(self)
        self.logo.setGeometry(QtCore.QRect(-50, 30, 500, 100))
        icon = QPixmap("logo500.png")
        self.logo.setPixmap(QPixmap(icon))

        olmage = QImage("./back.JPG")
        slmage = olmage.scaled(QSize(1200, 800))
        palette = QPalette()
        palette.setBrush(10, QBrush(slmage))
        self.setPalette(palette)

        self.back_btn = QPushButton(self)
        self.back_btn.setGeometry(QtCore.QRect(0, 89, 80, 52))
        self.back_btn.setText("뒤로가기")
        back_btn_font = QtGui.QFont()
        back_btn_font.setPointSize(10)
        back_btn_font.setFamily("서울남산 장체M")
        self.back_btn.setFont(back_btn_font)
        self.back_btn.clicked.connect(self.back_btn_clicked)
        self.back_btn_dialogs = list()
        self.back_btn.setCursor(QtGui.QCursor(QtCore.Qt.ClosedHandCursor))
        self.back_btn.setStyleSheet('color:white; background-color:rgba(1, 0, 0, 0.1)')

        self.setGeometry(150, 100, 1200, 800)
        self.setWindowTitle('[관리자 메뉴] 매출 확인')
        self.show()

    def stock_btn_clicked(self):
        # count = 0
        # con = pymysql.connect(host="192.168.0.19", user="root", password="1234", db='mydb', charset='utf8')
        # cur_data = con.cursor()
        # cur_sales = con.cursor()
        #
        # cur_name = con.cursor()
        # sql_name = "SELECT idproducts FROM pro_info WHERE codenum = %s"
        # cur_name.execute(sql_name, (self.stock_num.text()))
        # data_list = [data[0] for data in cur_name.fetchall()]
        #
        # sql_data = "SELECT idproducts FROM timetable WHERE date1 = %s"
        # num = cur_data.execute(sql_data, (self.stock_date.text()))
        # goods_li = [data[0] for data in cur_data.fetchall()]
        # try:
        #     for i in range(num):
        #         if goods_li[i] == data_list[0]:
        #             count += 1
        #     sql_sales = "SELECT unitprice FROM pro_info WHERE idproducts = %s"
        #     num_price = cur_sales.execute(sql_sales, str(data_list[0]))
        #     price = [column[0] for column in cur_sales.fetchall()]
        #     sales = int(price[0]) * count
        #     self.stock_sales_label.setText("'{0}' 상품 {1}개 판매 금액 : {2}".format(self.stock_num.text(), count, sales))
        # except:
        #     print("오류")
        # self.profile.setGeometry(QtCore.QRect(310, 180, 960, 720))
        # icon = QPixmap("blank.JPG")
        # self.profile.setPixmap(QPixmap(icon))
        plt.close()

        fm.get_fontconfig_fonts()
        font_location = 'C:/Windows/Fonts/malgun.ttf'
        font_name = fm.FontProperties(fname=font_location).get_name()
        plt.rc('font', family=font_name)

        con = pymysql.connect(host=HOST, user=USER, password=PASSWORD, db=DB, charset='utf8')

        cur = con.cursor()
        cur_x = con.cursor()
        cur_y = con.cursor()
        count = 0
        sales_sum = 0
        plot_cnt = []

        sql = "SELECT idproducts FROM pro_info;"
        num_goods = cur.execute(sql)
        goods_li = [data[0] for data in cur.fetchall()]

        #plot 차트 x축 상품 모델명
        sql_x = "SELECT model FROM pro_info"
        num_price = cur_x.execute(sql_x)
        plot_model = [column[0] for column in cur_x.fetchall()]

        #plot 차트 y축 상품 모델명
        sql_y = "SELECT idproducts FROM timetable WHERE date1 = %s"
        num_sell = cur_y.execute(sql_y, (self.stock_date.currentText()))
        sell_li = [data[0] for data in cur_y.fetchall()]

        for i in range(num_goods):
            for j in range(num_sell):
                if goods_li[i] == sell_li[j]:
                    count += 1

            sql_for = "SELECT unitprice FROM pro_info WHERE idproducts = %s"
            num_price = cur.execute(sql_for, (goods_li[i]))
            price = [column[0] for column in cur.fetchall()]

            sales = int(price[0]) * count
            print("{0}번 상품 판매금액: {1}".format(goods_li[i], sales))
            plot_cnt.append(sales)
            count = 0
            sales_sum += sales

        day_total = sales_sum

        day = str(day_total)
        x = plot_model
        y = plot_cnt

        plt.bar(x, y, align='center', color='#0a326f')

        plt.xlabel('금일 총 매출 : ' + day + '원', fontsize=15, color='#0a326f')
        plt.ylabel('판매량')
        plt.title(self.stock_date.currentText() + '일 매출', fontsize=30, color='#0a326f')
        plt.savefig('da_test.jpg', format='jpg', dpi=100)
        # plt.show()

        self.profile.setGeometry(QtCore.QRect(310, 180, 960, 720))
        icon = QPixmap("da_test.JPG")
        self.profile.setPixmap(QPixmap(icon))

    def back_btn_clicked(self):
        self.close()
        back_btn_dialogs = manager_menu(self)
        self.back_btn_dialogs.append(back_btn_dialogs)
        back_btn_dialogs.show()


# 관리자 메뉴 - 직원 관리 메뉴
class manager_menu_managermenu(QMainWindow):
    def __init__(self, parent=None):
        super(manager_menu_managermenu, self).__init__(parent)

        fm.get_fontconfig_fonts()
        font_location = 'C:/Windows/Fonts/malgun.ttf'
        font_name = fm.FontProperties(fname=font_location).get_name()
        plt.rc('font', family=font_name)

        con = pymysql.connect(host=HOST, user=USER, password=PASSWORD, db=DB, charset='utf8')
        cur = con.cursor()
        sql = "select name from user_info;"
        cur.execute(sql)
        data = cur.fetchall()
        li = [x[0] for x in data]

        self.mainlabel_txt = QLabel(self)
        self.mainlabel_txt.setText("· 확인할 직원 이름을 선택하세요.")
        mainlabel_txt_font = QtGui.QFont()
        mainlabel_txt_font.setPointSize(9)
        mainlabel_txt_font.setFamily("서울남산 장체M")
        self.mainlabel_txt.setFont(mainlabel_txt_font)
        self.mainlabel_txt.setGeometry(QtCore.QRect(500, 240, 341, 41))

        self.namecombobox = QComboBox(self)
        self.namecombobox.addItem("")
        self.namecombobox.addItems(li)
        # self.namecombobox.insertSeparator(4)
        self.namecombobox.activated.connect(self.combo_change)
        self.namecombobox.setGeometry(QtCore.QRect(550, 280, 100, 30))
        self.namecombobox.setStyleSheet('color:white; background:#0a326f')

        # self.combo_btn = QPushButton(self)
        # self.combo_btn.setText('선택')
        # combo_btn_font = QtGui.QFont()
        # combo_btn_font.setPointSize(10)
        # combo_btn_font.setFamily("서울남산 장체M")
        # self.combo_btn.setFont(combo_btn_font)
        # self.combo_btn.setGeometry(QtCore.QRect(320, 80, 70, 30))
        # self.combo_btn.clicked.connect(self.combo_btn_clicked)

        self.namelabel = QLabel(self)
        self.namelabel.setText("· 이름 : ")
        namelabel_font = QtGui.QFont()
        namelabel_font.setPointSize(10)
        namelabel_font.setFamily("서울남산 장체M")
        self.namelabel.setFont(namelabel_font)
        self.namelabel.setGeometry(QtCore.QRect(600, 340, 100, 100))

        # 데이터베이스 연동 이름 부분
        self.namelabel_txt = QLabel(self)
        self.namelabel_txt.setText("")
        namelabel_txt_font = QtGui.QFont()
        namelabel_txt_font.setPointSize(10)
        namelabel_txt_font.setFamily("서울남산 장체M")
        self.namelabel_txt.setFont(namelabel_txt_font)
        self.namelabel_txt.setGeometry(QtCore.QRect(660, 340, 300, 100))

        self.positionlabel = QLabel(self)
        self.positionlabel.setText("· 직책 : ")
        positionlabel_font = QtGui.QFont()
        positionlabel_font.setPointSize(10)
        positionlabel_font.setFamily("서울남산 장체M")
        self.positionlabel.setFont(positionlabel_font)
        self.positionlabel.setGeometry(QtCore.QRect(600, 380, 100, 100))

        # 데이터베이스 연동 직책 부분
        self.positionlabel_txt = QLabel(self)
        self.positionlabel_txt.setText("")
        positionlabel_txt_font = QtGui.QFont()
        positionlabel_txt_font.setPointSize(10)
        positionlabel_txt_font.setFamily("서울남산 장체M")
        self.positionlabel_txt.setFont(positionlabel_txt_font)
        self.positionlabel_txt.setGeometry(QtCore.QRect(660, 380, 300, 100))

        self.idlabel = QLabel(self)
        self.idlabel.setText("· ID : ")
        idlabel_font = QtGui.QFont()
        idlabel_font.setPointSize(10)
        idlabel_font.setFamily("서울남산 장체M")
        self.idlabel.setFont(idlabel_font)
        self.idlabel.setGeometry(QtCore.QRect(600, 420, 100, 100))

        # 데이터베이스 연동 ID 부분
        self.idlabel_txt = QLabel(self)
        self.idlabel_txt.setText("")
        idlabel_txt_font = QtGui.QFont()
        idlabel_txt_font.setPointSize(10)
        idlabel_txt_font.setFamily("서울남산 장체M")
        self.idlabel_txt.setFont(idlabel_txt_font)
        self.idlabel_txt.setGeometry(QtCore.QRect(650, 420, 300, 100))

        self.birthlabel = QLabel(self)
        self.birthlabel.setText("· 생년월일 : ")
        birthlabel_font = QtGui.QFont()
        birthlabel_font.setPointSize(10)
        birthlabel_font.setFamily("서울남산 장체M")
        self.birthlabel.setFont(birthlabel_font)
        self.birthlabel.setGeometry(QtCore.QRect(600, 460, 100, 100))

        # 데이터베이스 연동 생년월일 부분
        self.birthlabel_txt = QLabel(self)
        self.birthlabel_txt.setText("")
        birthlabel_txt_font = QtGui.QFont()
        birthlabel_txt_font.setPointSize(10)
        birthlabel_txt_font.setFamily("서울남산 장체M")
        self.birthlabel_txt.setFont(birthlabel_txt_font)
        self.birthlabel_txt.setGeometry(QtCore.QRect(690, 460, 300, 100))

        self.emaillabel = QLabel(self)
        self.emaillabel.setText("· E-Mail : ")
        emaillabel_font = QtGui.QFont()
        emaillabel_font.setPointSize(10)
        emaillabel_font.setFamily("서울남산 장체M")
        self.emaillabel.setFont(emaillabel_font)
        self.emaillabel.setGeometry(QtCore.QRect(600, 500, 100, 100))

        # 데이터베이스 연동 이메일 부분
        self.emaillabel_txt = QLabel(self)
        self.emaillabel_txt.setText("")
        emaillabel_txt_font = QtGui.QFont()
        emaillabel_txt_font.setPointSize(10)
        emaillabel_txt_font.setFamily("서울남산 장체M")
        self.emaillabel_txt.setFont(emaillabel_txt_font)
        self.emaillabel_txt.setGeometry(QtCore.QRect(680, 500, 300, 100))

        self.profile = QLabel(self)
        self.profile.setGeometry(QtCore.QRect(360, 375, 175, 175))
        icon = QPixmap("profile.png")
        self.profile.setPixmap(QPixmap(icon))

        self.logo = QLabel(self)
        self.logo.setGeometry(QtCore.QRect(-50, 30, 500, 100))
        icon = QPixmap("logo500.png")
        self.logo.setPixmap(QPixmap(icon))

        olmage = QImage("./back.JPG")
        slmage = olmage.scaled(QSize(1200, 800))
        palette = QPalette()
        palette.setBrush(10, QBrush(slmage))
        self.setPalette(palette)

        self.back_btn = QPushButton(self)
        self.back_btn.setGeometry(QtCore.QRect(0, 89, 80, 52))
        self.back_btn.setText("뒤로가기")
        back_btn_font = QtGui.QFont()
        back_btn_font.setPointSize(10)
        back_btn_font.setFamily("서울남산 장체M")
        self.back_btn.setFont(back_btn_font)
        self.back_btn.clicked.connect(self.back_btn_clicked)
        self.back_btn_dialogs = list()
        self.back_btn.setCursor(QtGui.QCursor(QtCore.Qt.ClosedHandCursor))
        self.back_btn.setStyleSheet('color:white; background-color:rgba(1, 0, 0, 0.1)')

        self.setGeometry(150, 100, 1200, 800)
        self.setWindowTitle('[관리자 메뉴] 직원 관리')
        self.show()

    def combo_change(self, text):
        con = pymysql.connect(host=HOST, user=USER, password=PASSWORD, db=DB, charset='utf8')

        cur_name = con.cursor()
        cur_position = con.cursor()
        cur_id = con.cursor()
        cur_birth = con.cursor()
        cur_email = con.cursor()

        sql_name = "select name from user_info;"
        sql_position = "select position from user_info;"
        sql_id = "select id from user_info;"
        sql_birth = "select birth from user_info;"
        sql_email = "select email from user_info;"

        cur_name.execute(sql_name)
        cur_position.execute(sql_position)
        cur_id.execute(sql_id)
        cur_birth.execute(sql_birth)
        cur_email.execute(sql_email)

        data_name = cur_name.fetchall()
        data_position = cur_position.fetchall()
        data_id = cur_id.fetchall()
        data_birth = cur_birth.fetchall()
        data_email = cur_email.fetchall()

        li_name = [x[0] for x in data_name]
        li_position = [x[0] for x in data_position]
        li_id = [x[0] for x in data_id]
        li_birth = [x[0] for x in data_birth]
        li_email = [x[0] for x in data_email]

        user_len = len(li_name)

        for x in range(user_len):
            for y in range(0, 7):
                if self.namecombobox.currentText() == str(li_name[x]):
                    self.namelabel_txt.setText(li_name[x])
                    self.positionlabel_txt.setText(li_position[x])
                    self.idlabel_txt.setText(li_id[x])
                    self.birthlabel_txt.setText(li_birth[x])
                    self.emaillabel_txt.setText(li_email[x])

    def back_btn_clicked(self):
        self.close()
        back_btn_dialogs = manager_menu(self)
        self.back_btn_dialogs.append(back_btn_dialogs)
        back_btn_dialogs.show()


# 슈퍼 관리자 메뉴
class sudo_menu(QMainWindow):
    def __init__(self, parent=None):
        super(sudo_menu, self).__init__(parent)

        self.mainlabel_txt = QLabel(self)
        self.mainlabel_txt.setText("슈퍼 관리자 메뉴")
        mainlabel_txt_font = QtGui.QFont()
        mainlabel_txt_font.setPointSize(23)
        mainlabel_txt_font.setFamily("서울남산 장체M")
        self.mainlabel_txt.setFont(mainlabel_txt_font)
        self.mainlabel_txt.setGeometry(QtCore.QRect(460, 260, 341, 41))

        self.search_btn = QPushButton(self)
        self.search_btn.setText('직원 확인')
        search_btn_font = QtGui.QFont()
        search_btn_font.setPointSize(20)
        search_btn_font.setFamily("서울남산 장체M")
        self.search_btn.setFont(search_btn_font)
        self.search_btn.setGeometry(QtCore.QRect(330, 410, 150, 150))
        self.search_btn.setCursor(QtGui.QCursor(QtCore.Qt.ClosedHandCursor))
        self.search_btn.setStyleSheet('color:white; background:#0a326f')

        self.edit_btn = QPushButton(self)
        self.edit_btn.setText('직원 정보\n수정')
        edit_btn_font = QtGui.QFont()
        edit_btn_font.setPointSize(18)
        edit_btn_font.setFamily("서울남산 장체M")
        self.edit_btn.setFont(edit_btn_font)
        self.edit_btn.setGeometry(QtCore.QRect(530, 410, 150, 150))
        self.edit_btn.setCursor(QtGui.QCursor(QtCore.Qt.ClosedHandCursor))
        self.edit_btn.setStyleSheet('color:white; background:#0a326f')

        self.delete_btn = QPushButton(self)
        self.delete_btn.setText('관리자/\n직원\n삭제')
        delete_btn_font = QtGui.QFont()
        delete_btn_font.setPointSize(18)
        delete_btn_font.setFamily("서울남산 장체M")
        self.delete_btn.setFont(delete_btn_font)
        self.delete_btn.setGeometry(QtCore.QRect(730, 410, 150, 150))
        self.delete_btn.setCursor(QtGui.QCursor(QtCore.Qt.ClosedHandCursor))
        self.delete_btn.setStyleSheet('color:white; background:#0a326f')

        self.logout_btn = QPushButton(self)
        self.logout_btn.setText('로그아웃')
        logout_btn_font = QtGui.QFont()
        logout_btn_font.setPointSize(9)
        logout_btn_font.setFamily("서울남산 장체M")
        self.logout_btn.setFont(logout_btn_font)
        self.logout_btn.setGeometry(QtCore.QRect(800, 230, 70, 30))
        self.logout_btn.setCursor(QtGui.QCursor(QtCore.Qt.ClosedHandCursor))
        self.logout_btn.setStyleSheet('color:white; background:#0a326f')

        self.search_btn.clicked.connect(self.search_btn_clicked)
        self.search_btn_dialogs = list()

        self.edit_btn.clicked.connect(self.edit_btn_clicked)
        self.edit_btn_dialogs = list()

        self.delete_btn.clicked.connect(self.delete_btn_clicked)
        self.delete_btn_dialogs = list()

        self.logout_btn.clicked.connect(self.logout_btn_clicked)
        self.logout_btn_dialogs = list()

        self.logo = QLabel(self)
        self.logo.setGeometry(QtCore.QRect(-50, 30, 500, 100))
        icon = QPixmap("logo500.png")
        self.logo.setPixmap(QPixmap(icon))

        olmage = QImage("./back.JPG")
        slmage = olmage.scaled(QSize(1200, 800))
        palette = QPalette()
        palette.setBrush(10, QBrush(slmage))
        self.setPalette(palette)

        self.setGeometry(150, 100, 1200, 800)
        self.setWindowTitle('슈퍼 관리자 메뉴')
        self.show()

    def search_btn_clicked(self):
        self.close()
        search_btn_dialogs = sudo_menu_searchmenu(self)
        self.search_btn_dialogs.append(search_btn_dialogs)
        search_btn_dialogs.show()

    def edit_btn_clicked(self):
        self.close()
        edit_btn_dialogs = sudo_menu_editmenu(self)
        self.edit_btn_dialogs.append(edit_btn_dialogs)
        edit_btn_dialogs.show()

    def delete_btn_clicked(self):
        self.close()
        delete_btn_dialogs = sudo_menu_deletemenu(self)
        self.delete_btn_dialogs.append(delete_btn_dialogs)
        delete_btn_dialogs.show()

    def logout_btn_clicked(self):
        self.close()
        logout_btn_dialogs = login_window(self)
        self.logout_btn_dialogs.append(logout_btn_dialogs)
        logout_btn_dialogs.show()


# 슈퍼 관리자 메뉴 - 직원 확인
class sudo_menu_searchmenu(QMainWindow):
    def __init__(self, parent=None):
        super(sudo_menu_searchmenu, self).__init__(parent)

        con = pymysql.connect(host=HOST, user=USER, password=PASSWORD, db=DB, charset='utf8')
        cur = con.cursor()
        sql = "select name from user_info;"
        cur.execute(sql)
        data = cur.fetchall()
        li = [x[0] for x in data]

        self.mainlabel_txt = QLabel(self)
        self.mainlabel_txt.setText("· 확인할 직원 이름을 선택하세요.")
        mainlabel_txt_font = QtGui.QFont()
        mainlabel_txt_font.setPointSize(9)
        mainlabel_txt_font.setFamily("서울남산 장체M")
        self.mainlabel_txt.setFont(mainlabel_txt_font)
        self.mainlabel_txt.setGeometry(QtCore.QRect(500, 240, 341, 41))

        self.namecombobox = QComboBox(self)
        self.namecombobox.addItem("")
        self.namecombobox.addItems(li)
        # self.namecombobox.insertSeparator(4)
        self.namecombobox.activated.connect(self.combo_change)
        self.namecombobox.setGeometry(QtCore.QRect(550, 280, 100, 30))
        self.namecombobox.setStyleSheet('color:white; background:#0a326f')

        self.namelabel = QLabel(self)
        self.namelabel.setText("· 이름 : ")
        namelabel_font = QtGui.QFont()
        namelabel_font.setPointSize(10)
        namelabel_font.setFamily("서울남산 장체M")
        self.namelabel.setFont(namelabel_font)
        self.namelabel.setGeometry(QtCore.QRect(600, 340, 100, 100))

        # 데이터베이스 연동 이름 부분
        self.namelabel_txt = QLabel(self)
        self.namelabel_txt.setText("")
        namelabel_txt_font = QtGui.QFont()
        namelabel_txt_font.setPointSize(10)
        namelabel_txt_font.setFamily("서울남산 장체M")
        self.namelabel_txt.setFont(namelabel_txt_font)
        self.namelabel_txt.setGeometry(QtCore.QRect(660, 340, 300, 100))

        self.positionlabel = QLabel(self)
        self.positionlabel.setText("· 직책 : ")
        positionlabel_font = QtGui.QFont()
        positionlabel_font.setPointSize(10)
        positionlabel_font.setFamily("서울남산 장체M")
        self.positionlabel.setFont(positionlabel_font)
        self.positionlabel.setGeometry(QtCore.QRect(600, 380, 100, 100))

        # 데이터베이스 연동 직책 부분
        self.positionlabel_txt = QLabel(self)
        self.positionlabel_txt.setText("")
        positionlabel_txt_font = QtGui.QFont()
        positionlabel_txt_font.setPointSize(10)
        positionlabel_txt_font.setFamily("서울남산 장체M")
        self.positionlabel_txt.setFont(positionlabel_txt_font)
        self.positionlabel_txt.setGeometry(QtCore.QRect(660, 380, 300, 100))

        self.idlabel = QLabel(self)
        self.idlabel.setText("· ID : ")
        idlabel_font = QtGui.QFont()
        idlabel_font.setPointSize(10)
        idlabel_font.setFamily("서울남산 장체M")
        self.idlabel.setFont(idlabel_font)
        self.idlabel.setGeometry(QtCore.QRect(600, 420, 100, 100))

        # 데이터베이스 연동 ID 부분
        self.idlabel_txt = QLabel(self)
        self.idlabel_txt.setText("")
        idlabel_txt_font = QtGui.QFont()
        idlabel_txt_font.setPointSize(10)
        idlabel_txt_font.setFamily("서울남산 장체M")
        self.idlabel_txt.setFont(idlabel_txt_font)
        self.idlabel_txt.setGeometry(QtCore.QRect(650, 420, 300, 100))

        self.birthlabel = QLabel(self)
        self.birthlabel.setText("· 생년월일 : ")
        birthlabel_font = QtGui.QFont()
        birthlabel_font.setPointSize(10)
        birthlabel_font.setFamily("서울남산 장체M")
        self.birthlabel.setFont(birthlabel_font)
        self.birthlabel.setGeometry(QtCore.QRect(600, 460, 100, 100))

        # 데이터베이스 연동 생년월일 부분
        self.birthlabel_txt = QLabel(self)
        self.birthlabel_txt.setText("")
        birthlabel_txt_font = QtGui.QFont()
        birthlabel_txt_font.setPointSize(10)
        birthlabel_txt_font.setFamily("서울남산 장체M")
        self.birthlabel_txt.setFont(birthlabel_txt_font)
        self.birthlabel_txt.setGeometry(QtCore.QRect(690, 460, 300, 100))

        self.emaillabel = QLabel(self)
        self.emaillabel.setText("· E-Mail : ")
        emaillabel_font = QtGui.QFont()
        emaillabel_font.setPointSize(10)
        emaillabel_font.setFamily("서울남산 장체M")
        self.emaillabel.setFont(emaillabel_font)
        self.emaillabel.setGeometry(QtCore.QRect(600, 500, 100, 100))

        # 데이터베이스 연동 이메일 부분
        self.emaillabel_txt = QLabel(self)
        self.emaillabel_txt.setText("")
        emaillabel_txt_font = QtGui.QFont()
        emaillabel_txt_font.setPointSize(10)
        emaillabel_txt_font.setFamily("서울남산 장체M")
        self.emaillabel_txt.setFont(emaillabel_txt_font)
        self.emaillabel_txt.setGeometry(QtCore.QRect(680, 500, 300, 100))

        self.profile = QLabel(self)
        self.profile.setGeometry(QtCore.QRect(360, 375, 175, 175))
        icon = QPixmap("profile.png")
        self.profile.setPixmap(QPixmap(icon))

        self.logo = QLabel(self)
        self.logo.setGeometry(QtCore.QRect(-50, 30, 500, 100))
        icon = QPixmap("logo500.png")
        self.logo.setPixmap(QPixmap(icon))

        olmage = QImage("./back.JPG")
        slmage = olmage.scaled(QSize(1200, 800))
        palette = QPalette()
        palette.setBrush(10, QBrush(slmage))
        self.setPalette(palette)

        self.back_btn = QPushButton(self)
        self.back_btn.setGeometry(QtCore.QRect(0, 89, 80, 52))
        self.back_btn.setText("뒤로가기")
        back_btn_font = QtGui.QFont()
        back_btn_font.setPointSize(10)
        back_btn_font.setFamily("서울남산 장체M")
        self.back_btn.setFont(back_btn_font)
        self.back_btn.clicked.connect(self.back_btn_clicked)
        self.back_btn_dialogs = list()
        self.back_btn.setCursor(QtGui.QCursor(QtCore.Qt.ClosedHandCursor))
        self.back_btn.setStyleSheet('color:white; background-color:rgba(1, 0, 0, 0.1)')

        self.setGeometry(150, 100, 1200, 800)
        self.setWindowTitle('[슈퍼 관리자] 직원 확인')
        self.show()

    # 콤보박스 선택시 변경
    def combo_change(self, text):

        con = pymysql.connect(host=HOST, user=USER, password=PASSWORD, db=DB, charset='utf8')

        cur_name = con.cursor()
        cur_position = con.cursor()
        cur_id = con.cursor()
        cur_birth = con.cursor()
        cur_email = con.cursor()

        sql_name = "select name from user_info;"
        sql_position = "select position from user_info;"
        sql_id = "select id from user_info;"
        sql_birth = "select birth from user_info;"
        sql_email = "select email from user_info;"

        cur_name.execute(sql_name)
        cur_position.execute(sql_position)
        cur_id.execute(sql_id)
        cur_birth.execute(sql_birth)
        cur_email.execute(sql_email)

        data_name = cur_name.fetchall()
        data_position = cur_position.fetchall()
        data_id = cur_id.fetchall()
        data_birth = cur_birth.fetchall()
        data_email = cur_email.fetchall()

        li_name = [x[0] for x in data_name]
        li_position = [x[0] for x in data_position]
        li_id = [x[0] for x in data_id]
        li_birth = [x[0] for x in data_birth]
        li_email = [x[0] for x in data_email]

        user_len = len(li_name)

        for x in range(user_len):
            for y in range(0, 7):
                if self.namecombobox.currentText() == str(li_name[x]):
                    self.namelabel_txt.setText(li_name[x])
                    self.positionlabel_txt.setText(li_position[x])
                    self.idlabel_txt.setText(li_id[x])
                    self.birthlabel_txt.setText(li_birth[x])
                    self.emaillabel_txt.setText(li_email[x])

        # if self.namecombobox.currentText() == str(li_name[0]):
        #     self.namelabel_txt.setText(li_name[0])
        #     self.positionlabel_txt.setText(li_position[0])
        #     self.idlabel_txt.setText(li_id[0])
        #     self.birthlabel_txt.setText(li_birth[0])
        #     self.emaillabel_txt.setText(li_email[0])
        #
        # if self.namecombobox.currentText() == str(li_name[1]):
        #     self.namelabel_txt.setText(li_name[1])
        #     self.positionlabel_txt.setText(li_position[1])
        #     self.idlabel_txt.setText(li_id[1])
        #     self.birthlabel_txt.setText(li_birth[1])
        #     self.emaillabel_txt.setText(li_email[1])
        #
        # if self.namecombobox.currentText() == str(li_name[2]):
        #     self.namelabel_txt.setText(li_name[2])
        #     self.positionlabel_txt.setText(li_position[2])
        #     self.idlabel_txt.setText(li_id[2])
        #     self.birthlabel_txt.setText(li_birth[2])
        #     self.emaillabel_txt.setText(li_email[2])
        #
        # if self.namecombobox.currentText() == str(li_name[3]):
        #     self.namelabel_txt.setText(li_name[3])
        #     self.positionlabel_txt.setText(li_position[3])
        #     self.idlabel_txt.setText(li_id[3])
        #     self.birthlabel_txt.setText(li_birth[3])
        #     self.emaillabel_txt.setText(li_email[3])
        #
        # if self.namecombobox.currentText() == str(li_name[4]):
        #     self.namelabel_txt.setText(li_name[4])
        #     self.positionlabel_txt.setText(li_position[4])
        #     self.idlabel_txt.setText(li_id[4])
        #     self.birthlabel_txt.setText(li_birth[4])
        #     self.emaillabel_txt.setText(li_email[4])
        #
        # if self.namecombobox.currentText() == "" or self.namecombobox.currentText() == '초코파이':
        #     self.namelabel_txt.setText("")
        #     self.positionlabel_txt.setText("")
        #     self.idlabel_txt.setText("")
        #     self.birthlabel_txt.setText("")
        #     self.emaillabel_txt.setText("")
        #
        # if self.namecombobox.currentText() == '초코파이':
        #     self.namelabel_txt.setText("")
        #     self.positionlabel_txt.setText("Super Manager")
        #     self.idlabel_txt.setText("")
        #     self.birthlabel_txt.setText("")
        #     self.emaillabel_txt.setText("")

        # elif self.namecombobox.currentText() == str(li_name[6]):
        #     self.namelabel_txt.setText(li_name[4])
        #     self.positionlabel_txt.setText(li_position[0])
        #     self.idlabel_txt.setText(li_id[4])
        #     self.birthlabel_txt.setText(li_birth[4])
        #     self.emaillabel_txt.setText(li_email[4])

    def back_btn_clicked(self):
        self.close()
        back_btn_dialogs = sudo_menu(self)
        self.back_btn_dialogs.append(back_btn_dialogs)
        back_btn_dialogs.show()


# 슈퍼 관리자 메뉴 - 직원 정보 수정
class sudo_menu_editmenu(QMainWindow):
    def __init__(self, parent=None):
        super(sudo_menu_editmenu, self).__init__(parent)

        con = pymysql.connect(host=HOST, user=USER, password=PASSWORD, db=DB, charset='utf8')
        cur = con.cursor()
        cur_po = con.cursor()
        sql_po = "SELECT distinct position FROM user_info;"
        sql = "select name from user_info;"
        cur.execute(sql)
        cur_po.execute(sql_po)
        data = cur.fetchall()
        data_po = cur_po.fetchall()
        # data_po = cur_po.fe
        li = [x[0] for x in data]
        li_po = [x[0] for x in data_po]

        self.mainlabel_txt = QLabel(self)
        self.mainlabel_txt.setText("· 수정할 직원 이름을 선택하세요.")
        mainlabel_txt_font = QtGui.QFont()
        mainlabel_txt_font.setPointSize(9)
        mainlabel_txt_font.setFamily("서울남산 장체M")
        self.mainlabel_txt.setFont(mainlabel_txt_font)
        self.mainlabel_txt.setGeometry(QtCore.QRect(500, 240, 341, 41))

        self.namecombobox = QComboBox(self)
        self.namecombobox.addItem("")
        self.namecombobox.addItems(li)
        # self.namecombobox.insertSeparator(4)
        self.namecombobox.activated.connect(self.combo_change)
        self.namecombobox.setGeometry(QtCore.QRect(550, 280, 100, 30))
        self.namecombobox.setStyleSheet('color:white; background:#0a326f')

        self.namelabel = QLabel(self)
        self.namelabel.setText("· 이름 : ")
        namelabel_font = QtGui.QFont()
        namelabel_font.setPointSize(10)
        namelabel_font.setFamily("서울남산 장체M")
        self.namelabel.setFont(namelabel_font)
        self.namelabel.setGeometry(QtCore.QRect(600, 340, 100, 100))

        # 직원 정보 수정(이름) -> 데이터베이스 연동해야함
        self.namelabel_txt = QLineEdit(self)
        self.namelabel_txt.setText("")
        namelabel_txt_font = QtGui.QFont()
        namelabel_txt_font.setPointSize(10)
        namelabel_txt_font.setFamily("서울남산 장체M")
        self.namelabel_txt.setFont(namelabel_txt_font)
        self.namelabel_txt.setGeometry(QtCore.QRect(660, 375, 100, 30))

        self.positionlabel = QLabel(self)
        self.positionlabel.setText("· 직책 : ")
        positionlabel_font = QtGui.QFont()
        positionlabel_font.setPointSize(10)
        positionlabel_font.setFamily("서울남산 장체M")
        self.positionlabel.setFont(positionlabel_font)
        self.positionlabel.setGeometry(QtCore.QRect(600, 380, 100, 100))

        # 직원 정보 수정(직책) -> 데이터베이스 연동해야함
        self.positionlabel_txt = QComboBox(self)
        self.positionlabel_txt.addItem('')
        self.positionlabel_txt.addItems(["employee", "manager", "super"])
        positionlabel_txt_font = QtGui.QFont()
        positionlabel_txt_font.setPointSize(10)
        positionlabel_txt_font.setFamily("서울남산 장체M")
        self.positionlabel_txt.setFont(positionlabel_txt_font)
        self.positionlabel_txt.setGeometry(QtCore.QRect(660, 415, 120, 30))
        self.positionlabel_txt.setStyleSheet('color:white; background:#0a326f')

        self.idlabel = QLabel(self)
        self.idlabel.setText("· ID : ")
        idlabel_font = QtGui.QFont()
        idlabel_font.setPointSize(10)
        idlabel_font.setFamily("서울남산 장체M")
        self.idlabel.setFont(idlabel_font)
        self.idlabel.setGeometry(QtCore.QRect(600, 420, 100, 100))

        # 직원 정보 수정(ID) -> 데이터베이스 연동해야함
        self.idlabel_txt = QLineEdit(self)
        self.idlabel_txt.setText("")
        idlabel_txt_font = QtGui.QFont()
        idlabel_txt_font.setPointSize(10)
        idlabel_txt_font.setFamily("서울남산 장체M")
        self.idlabel_txt.setFont(idlabel_txt_font)
        self.idlabel_txt.setGeometry(QtCore.QRect(660, 455, 130, 30))

        self.birthlabel = QLabel(self)
        self.birthlabel.setText("· 생년월일 : ")
        birthlabel_font = QtGui.QFont()
        birthlabel_font.setPointSize(10)
        birthlabel_font.setFamily("서울남산 장체M")
        self.birthlabel.setFont(birthlabel_font)
        self.birthlabel.setGeometry(QtCore.QRect(600, 460, 100, 100))

        # 직원 정보 수정(생년월일) -> 데이터베이스 연동해야함
        self.birthlabel_txt = QLineEdit(self)
        self.birthlabel_txt.setText("")
        birthlabel_txt_font = QtGui.QFont()
        birthlabel_txt_font.setPointSize(10)
        birthlabel_txt_font.setFamily("서울남산 장체M")
        self.birthlabel_txt.setFont(birthlabel_txt_font)
        self.birthlabel_txt.setGeometry(QtCore.QRect(690, 495, 120, 30))

        self.emaillabel = QLabel(self)
        self.emaillabel.setText("· E-Mail : ")
        emaillabel_font = QtGui.QFont()
        emaillabel_font.setPointSize(10)
        emaillabel_font.setFamily("서울남산 장체M")
        self.emaillabel.setFont(emaillabel_font)
        self.emaillabel.setGeometry(QtCore.QRect(600, 500, 100, 100))

        # 직원 정보 수정(이메일) -> 데이터베이스 연동해야함
        self.emaillabel_txt = QLineEdit(self)
        self.emaillabel_txt.setText("")
        emaillabel_txt_font = QtGui.QFont()
        emaillabel_txt_font.setPointSize(10)
        emaillabel_txt_font.setFamily("서울남산 장체M")
        self.emaillabel_txt.setFont(emaillabel_txt_font)
        self.emaillabel_txt.setGeometry(QtCore.QRect(680, 535, 200, 30))

        self.profile = QLabel(self)
        self.profile.setGeometry(QtCore.QRect(360, 375, 175, 175))
        icon = QPixmap("profile.png")
        self.profile.setPixmap(QPixmap(icon))

        self.save_btn = QPushButton(self)
        self.save_btn.setGeometry(QtCore.QRect(550, 600, 100, 50))
        self.save_btn.setText("저장")
        save_btn_font = QtGui.QFont()
        save_btn_font.setPointSize(12)
        save_btn_font.setFamily("서울남산 장체M")
        self.save_btn.setFont(save_btn_font)
        self.save_btn.clicked.connect(self.save_btn_clicked)
        self.save_btn_dialogs = list()
        self.save_btn.setCursor(QtGui.QCursor(QtCore.Qt.ClosedHandCursor))
        self.save_btn.setStyleSheet('color:white; background:#0a326f')

        self.logo = QLabel(self)
        self.logo.setGeometry(QtCore.QRect(-50, 30, 500, 100))
        icon = QPixmap("logo500.png")
        self.logo.setPixmap(QPixmap(icon))

        olmage = QImage("./back.JPG")
        slmage = olmage.scaled(QSize(1200, 800))
        palette = QPalette()
        palette.setBrush(10, QBrush(slmage))
        self.setPalette(palette)

        self.back_btn = QPushButton(self)
        self.back_btn.setGeometry(QtCore.QRect(0, 89, 80, 52))
        self.back_btn.setText("뒤로가기")
        back_btn_font = QtGui.QFont()
        back_btn_font.setPointSize(10)
        back_btn_font.setFamily("서울남산 장체M")
        self.back_btn.setFont(back_btn_font)
        self.back_btn.clicked.connect(self.back_btn_clicked)
        self.back_btn_dialogs = list()
        self.back_btn.setCursor(QtGui.QCursor(QtCore.Qt.ClosedHandCursor))
        self.back_btn.setStyleSheet('color:white; background-color:rgba(1, 0, 0, 0.1)')

        self.setGeometry(150, 100, 1200, 800)
        self.setWindowTitle('[슈퍼 관리자] 직원 정보 수정')
        self.show()

    def save_btn_clicked(self):
        con = pymysql.connect(host=HOST, user=USER, password=PASSWORD, db=DB, charset='utf8')

        cur_up_name = con.cursor()
        cur_up_position = con.cursor()
        cur_up_id = con.cursor()
        cur_up_birth = con.cursor()
        cur_up_email = con.cursor()

        cur_name = con.cursor()
        cur_position = con.cursor()
        cur_id = con.cursor()
        cur_birth = con.cursor()
        cur_email = con.cursor()

        sql_name = "SELECT distinct name FROM user_info;"
        sql_position = "SELECT position FROM user_info;"
        sql_id = "SELECT distinct id FROM user_info;"
        sql_birth = "SELECT distinct birth FROM user_info;"
        sql_email = "SELECT distinct email FROM user_info;"

        sql_up_name = "UPDATE user_info SET name = %s WHERE name = %s;"
        sql_up_position = "UPDATE user_info SET position = %s WHERE position = %s;"
        sql_up_id = "UPDATE user_info SET id = %s WHERE id = %s;"
        sql_up_birth = "UPDATE user_info SET birth = %s WHERE birth = %s;"
        sql_up_email = "UPDATE user_info SET email = %s WHERE email = %s;"

        cur_name.execute(sql_name)
        cur_position.execute(sql_position)
        cur_id.execute(sql_id)
        cur_birth.execute(sql_birth)
        cur_email.execute(sql_email)

        data_name = cur_name.fetchall()
        data_position = cur_position.fetchall()
        data_id = cur_id.fetchall()
        data_birth = cur_birth.fetchall()
        data_email = cur_email.fetchall()

        li_name = [x[0] for x in data_name]
        li_position = [x[0] for x in data_position]
        li_id = [x[0] for x in data_id]
        li_birth = [x[0] for x in data_birth]
        li_email = [x[0] for x in data_email]

        user_len = len(li_name)

        for x in range(user_len):  #
            # for y in range(0, 7):
            if self.namecombobox.currentText() == str(li_name[x]):
                cur_up_name.execute(sql_up_name, (self.namelabel_txt.text(), li_name[x]))
                # cur_up_position.execute(sql_up_position, (self.positionlabel_txt.currentText(), li_position[x]))
                cur_up_id.execute(sql_up_id, (self.idlabel_txt.text(), li_id[x]))
                cur_up_birth.execute(sql_up_birth, (self.birthlabel_txt.text(), li_birth[x]))
                cur_up_email.execute(sql_up_email, (self.emaillabel_txt.text(), li_email[x]))

                # print(self.positionlabel_txt.currentText())

                # 안됨
                if self.positionlabel_txt.currentText() == 'manager':
                    # cur_up_position.execute(sql_up_position, 'manager', li_position[x])
                    print('manager')
                elif self.positionlabel_txt.currentText() == 'employee':
                    # cur_up_position.execute(sql_up_position, 'employee', li_position[x])
                    print('employee')
                elif self.positionlabel_txt.currentText() == 'super':
                    # cur_up_position.execute(sql_up_position, 'super', li_position[x])
                    print('super')
                con.commit()

        # if self.namecombobox.currentText() == str(li_name[0]):
        #     cur_up_name.execute(sql_up_name, (self.namelabel_txt.text(), li_name[0]))
        #     cur_up_id.execute(sql_up_id, (self.idlabel_txt.text(), li_id[0]))
        #     cur_up_birth.execute(sql_up_birth, (self.birthlabel_txt.text(), li_birth[0]))
        #     cur_up_email.execute(sql_up_email, (self.emaillabel_txt.text(), li_email[0]))
        #
        #     if self.positionlabel_txt.currentText() == "manager":
        #         print("manager")
        #     if self.positionlabel_txt.currentText() == "employee":
        #         print("employee")
        #
        #
        # if self.namecombobox.currentText() == str(li_name[1]):
        #     cur_up_name.execute(sql_up_name, (self.namelabel_txt.text(), li_name[1]))
        #     cur_up_id.execute(sql_up_id, (self.idlabel_txt.text(), li_id[1]))
        #     cur_up_birth.execute(sql_up_birth, (self.birthlabel_txt.text(), li_birth[1]))
        #     cur_up_email.execute(sql_up_email, (self.emaillabel_txt.text(), li_email[1]))
        #     con.commit()
        #
        # if self.namecombobox.currentText() == str(li_name[2]):
        #     cur_up_name.execute(sql_up_name, (self.namelabel_txt.text(), li_name[2]))
        #     cur_up_id.execute(sql_up_id, (self.idlabel_txt.text(), li_id[2]))
        #     cur_up_birth.execute(sql_up_birth, (self.birthlabel_txt.text(), li_birth[2]))
        #     cur_up_email.execute(sql_up_email, (self.emaillabel_txt.text(), li_email[2]))
        #     con.commit()
        #
        # if self.namecombobox.currentText() == str(li_name[3]):
        #     cur_up_name.execute(sql_up_name, (self.namelabel_txt.text(), li_name[3]))
        #     cur_up_id.execute(sql_up_id, (self.idlabel_txt.text(), li_id[3]))
        #     cur_up_birth.execute(sql_up_birth, (self.birthlabel_txt.text(), li_birth[3]))
        #     cur_up_email.execute(sql_up_email, (self.emaillabel_txt.text(), li_email[3]))
        #     con.commit()
        #
        # if self.namecombobox.currentText() == str(li_name[4]):
        #     cur_up_name.execute(sql_up_name, (self.namelabel_txt.text(), li_name[4]))
        #     cur_up_id.execute(sql_up_id, (self.idlabel_txt.text(), li_id[4]))
        #     cur_up_birth.execute(sql_up_birth, (self.birthlabel_txt.text(), li_birth[4]))
        #     cur_up_email.execute(sql_up_email, (self.emaillabel_txt.text(), li_email[4]))
        #     con.commit()

        save_btn_dialogs = editalarm_window(self)
        self.save_btn_dialogs.append(save_btn_dialogs)
        save_btn_dialogs.show()

    def back_btn_clicked(self):
        self.close()
        back_btn_dialogs = sudo_menu(self)
        self.back_btn_dialogs.append(back_btn_dialogs)
        back_btn_dialogs.show()

    def combo_change(self, text):
        con = pymysql.connect(host=HOST, user=USER, password=PASSWORD, db=DB, charset='utf8')

        cur_name = con.cursor()
        cur_position = con.cursor()
        cur_id = con.cursor()
        cur_birth = con.cursor()
        cur_email = con.cursor()

        sql_name = "select name from user_info;"
        sql_position = "select position from user_info;"
        sql_id = "select id from user_info;"
        sql_birth = "select birth from user_info;"
        sql_email = "select email from user_info"

        cur_name.execute(sql_name)
        cur_position.execute(sql_position)
        cur_id.execute(sql_id)
        cur_birth.execute(sql_birth)
        cur_email.execute(sql_email)

        data_name = cur_name.fetchall()
        data_position = cur_position.fetchall()
        data_id = cur_id.fetchall()
        data_birth = cur_birth.fetchall()
        data_email = cur_email.fetchall()

        li_name = [x[0] for x in data_name]
        li_position = [x[0] for x in data_position]
        li_id = [x[0] for x in data_id]
        li_birth = [x[0] for x in data_birth]
        li_email = [x[0] for x in data_email]

        user_len = len(li_name)
        for x in range(user_len):
            for y in range(0, 7):
                if self.namecombobox.currentText() == str(li_name[x]):
                    self.namelabel_txt.setText(li_name[x])
                    # self.positionlabel_txt.setText(li_position[x])
                    self.idlabel_txt.setText(li_id[x])
                    self.birthlabel_txt.setText(li_birth[x])
                    self.emaillabel_txt.setText(li_email[x])

                    if str(li_position[x]) == 'employee':
                        self.positionlabel_txt.setCurrentText('employee')
                    if str(li_position[x]) == 'manager':
                        self.positionlabel_txt.setCurrentText('manager')
                    if str(li_position[x]) == 'super':
                        self.positionlabel_txt.setCurrentText('super')
                    if str(li_position[x]) == '':
                        self.positionlabel_txt.setCurrentText('')
                if self.namecombobox.currentText() == '':
                    self.namelabel_txt.setText('')
                    # self.positionlabel_txt.setText('')
                    self.idlabel_txt.setText('')
                    self.birthlabel_txt.setText('')
                    self.emaillabel_txt.setText('')


# 수정 확인 알림창
class editalarm_window(QDialog):
    def __init__(self, parent=None):
        super(editalarm_window, self).__init__(parent)

        self.mainlabel_txt = QLabel(self)
        self.mainlabel_txt.setText("수정되었습니다.")
        mainlabel_txt_font = QtGui.QFont()
        mainlabel_txt_font.setPointSize(9)
        mainlabel_txt_font.setFamily("서울남산 장체M")
        self.mainlabel_txt.setFont(mainlabel_txt_font)
        self.mainlabel_txt.setGeometry(QtCore.QRect(100, 50, 141, 41))

        self.accept_btn = QPushButton(self)
        self.accept_btn.setText('확인')
        accept_btn_font = QtGui.QFont()
        accept_btn_font.setPointSize(10)
        accept_btn_font.setFamily("서울남산 장체M")
        self.accept_btn.setFont(accept_btn_font)
        self.accept_btn.setGeometry(QtCore.QRect(120, 150, 70, 30))
        self.accept_btn.clicked.connect(self.accept_btn_clicked)
        self.accept_btn_dialogs = list()
        self.accept_btn.setCursor(QtGui.QCursor(QtCore.Qt.ClosedHandCursor))
        self.accept_btn.setStyleSheet('color:white; background:#0a326f')

        self.setGeometry(600, 450, 300, 200)
        self.setWindowTitle('알림')
        self.show()

    def accept_btn_clicked(self):
        self.close()


# 슈퍼 관리자 메뉴 - 관리자/직원 삭제
class sudo_menu_deletemenu(QMainWindow):
    def __init__(self, parent=None):
        super(sudo_menu_deletemenu, self).__init__(parent)

        con = pymysql.connect(host=HOST, user=USER, password=PASSWORD, db=DB, charset='utf8')
        cur = con.cursor()
        sql = "select name from user_info;"
        cur.execute(sql)
        data = cur.fetchall()
        li = [x[0] for x in data]

        self.mainlabel_txt = QLabel(self)
        self.mainlabel_txt.setText("· 삭제할 직원 이름을 선택하세요.")
        mainlabel_txt_font = QtGui.QFont()
        mainlabel_txt_font.setPointSize(9)
        mainlabel_txt_font.setFamily("서울남산 장체M")
        self.mainlabel_txt.setFont(mainlabel_txt_font)
        self.mainlabel_txt.setGeometry(QtCore.QRect(500, 370, 341, 41))

        self.namecombobox = QComboBox(self)
        # self.namecombobox.addItem("오종진")
        self.namecombobox.addItems(li)
        # self.namecombobox.insertSeparator(4)
        self.namecombobox.activated.connect(self.combo_change)
        self.namecombobox.setGeometry(QtCore.QRect(500, 410, 101, 30))
        self.namecombobox.setStyleSheet('color:white; background:#0a326f')

        self.combo_btn = QPushButton(self)
        self.combo_btn.setText('선택')
        combo_btn_font = QtGui.QFont()
        combo_btn_font.setPointSize(10)
        combo_btn_font.setFamily("서울남산 장체M")
        self.combo_btn.setFont(combo_btn_font)
        self.combo_btn.setGeometry(QtCore.QRect(620, 410, 70, 30))
        self.combo_btn.clicked.connect(self.combo_btn_clicked)
        self.combo_btn_dialogs = list()
        self.combo_btn.setCursor(QtGui.QCursor(QtCore.Qt.ClosedHandCursor))
        self.combo_btn.setStyleSheet('color:white; background:#0a326f')

        self.logo = QLabel(self)
        self.logo.setGeometry(QtCore.QRect(-50, 30, 500, 100))
        icon = QPixmap("logo500.png")
        self.logo.setPixmap(QPixmap(icon))

        olmage = QImage("./back.JPG")
        slmage = olmage.scaled(QSize(1200, 800))
        palette = QPalette()
        palette.setBrush(10, QBrush(slmage))
        self.setPalette(palette)

        self.back_btn = QPushButton(self)
        self.back_btn.setGeometry(QtCore.QRect(0, 89, 80, 52))
        self.back_btn.setText("뒤로가기")
        back_btn_font = QtGui.QFont()
        back_btn_font.setPointSize(10)
        back_btn_font.setFamily("서울남산 장체M")
        self.back_btn.setFont(back_btn_font)
        self.back_btn.clicked.connect(self.back_btn_clicked)
        self.back_btn_dialogs = list()
        self.back_btn.setCursor(QtGui.QCursor(QtCore.Qt.ClosedHandCursor))
        self.back_btn.setStyleSheet('color:white; background-color:rgba(1, 0, 0, 0.1)')

        self.setGeometry(150, 100, 1200, 800)
        self.setWindowTitle('[슈퍼 관리자] 관리자/직원 삭제')
        self.show()

    def combo_change(self, text):
        delete_a = self.namecombobox.itemText(text)

    def combo_btn_clicked(self):
        con = pymysql.connect(host=HOST, user=USER, password=PASSWORD, db=DB, charset='utf8', autocommit=True)
        cur = con.cursor()
        sql_del = "DELETE FROM user_info WHERE name = %s;"
        cur.execute(sql_del, (self.namecombobox.currentText()))

        combo_btn_dialogs = deletealarm_window(self)
        self.combo_btn_dialogs.append(combo_btn_dialogs)
        combo_btn_dialogs.show()

    def back_btn_clicked(self):
        self.close()
        back_btn_dialogs = sudo_menu(self)
        self.back_btn_dialogs.append(back_btn_dialogs)
        back_btn_dialogs.show()


# 삭제 확인 알림창
class deletealarm_window(QMainWindow):
    def __init__(self, parent=None):
        super(deletealarm_window, self).__init__(parent)

        self.mainlabel_txt = QLabel(self)
        self.mainlabel_txt.setText("삭제되었습니다.")
        mainlabel_txt_font = QtGui.QFont()
        mainlabel_txt_font.setPointSize(9)
        mainlabel_txt_font.setFamily("서울남산 장체M")
        self.mainlabel_txt.setFont(mainlabel_txt_font)
        self.mainlabel_txt.setGeometry(QtCore.QRect(100, 50, 141, 41))

        self.accept_btn = QPushButton(self)
        self.accept_btn.setText('확인')
        accept_btn_font = QtGui.QFont()
        accept_btn_font.setPointSize(10)
        accept_btn_font.setFamily("서울남산 장체M")
        self.accept_btn.setFont(accept_btn_font)
        self.accept_btn.setGeometry(QtCore.QRect(120, 150, 70, 30))
        self.accept_btn.clicked.connect(self.accept_btn_clicked)
        self.accept_btn_dialogs = list()
        self.accept_btn.setCursor(QtGui.QCursor(QtCore.Qt.ClosedHandCursor))
        self.accept_btn.setStyleSheet('color:white; background:#0a326f')

        self.setGeometry(600, 450, 300, 200)
        self.setWindowTitle('알림')
        self.show()

    def accept_btn_clicked(self, event):
        self.close()


# 테스트 메인 화면
class First(QMainWindow):
    def __init__(self, parent=None):
        super(First, self).__init__(parent)

        # server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        # server_socket.bind(('', 9999))
        # print("socket bind")
        # server_socket.listen()
        # print("socket listening...")
        #
        # try:
        #     while True:
        #         client_socket, addr = server_socket.accept()
        #         th = threading.Thread(target=self.binder, args=(client_socket, addr))
        # except:
        #     print("server")
        # finally:
        #     server_socket.close()

        # def initUI(self):
        self.input_text = QLineEdit(self)
        self.input_text.resize(300, 30)

        self.send_btn = QPushButton(self)
        self.send_btn.setText('보내기')
        self.send_btn.resize(70, 30)

        self.database_btn = QPushButton(self)
        self.database_btn.setText('데이터베이스 테스트')
        self.database_btn.resize(160, 30)

        self.sudo_btn = QPushButton(self)
        self.sudo_btn.setText('슈퍼 관리자 메뉴')
        self.sudo_btn.resize(160, 150)

        self.manager_btn = QPushButton(self)
        self.manager_btn.setText('관리자 메뉴')
        self.manager_btn.resize(160, 150)

        self.staff_btn = QPushButton(self)
        self.staff_btn.setText('직원 메뉴')
        self.staff_btn.resize(160, 150)

        self.login_btn = QPushButton(self)
        self.login_btn.setText('로그인')
        self.login_btn.resize(50, 30)

        self.send_txt = QLabel(self)
        self.send_txt.setText('송신')

        self.recv_txt = QLabel(self)
        self.recv_txt.setText('수신')

        self.send_txtB = QTextBrowser(self)
        self.send_txtB.resize(250, 150)

        self.recv_txtB = QTextBrowser(self)
        self.recv_txtB.resize(250, 150)

        self.input_text.move(325, 225)
        self.send_btn.move(650, 225)
        self.database_btn.move(730, 225)
        self.sudo_btn.move(325, 300)
        self.manager_btn.move(520, 300)
        self.staff_btn.move(715, 300)
        self.send_txt.move(430, 470)
        self.recv_txt.move(730, 470)
        self.send_txtB.move(325, 500)
        self.recv_txtB.move(625, 500)
        self.login_btn.move(575, 460)

        self.send_btn.clicked.connect(self.send_btn_clicked)

        self.database_btn.clicked.connect(self.database_btn_clicked)

        self.sudo_btn.clicked.connect(self.sudo_btn_clicked)
        self.sudo_btn_dialogs = list()

        self.manager_btn.clicked.connect(self.manager_btn_clicked)
        self.manager_btn_dialogs = list()

        self.staff_btn.clicked.connect(self.staff_btn_clicked)
        self.staff_btn_dialogs = list()

        self.login_btn.clicked.connect(self.login_btn_clicked)
        self.login_btn_dialogs = list()

        self.goto_server = QPushButton(self)
        self.goto_server.setText("서버로 이동")
        self.goto_server.resize(100, 40)
        self.goto_server.move(550, 655)
        self.goto_server.clicked.connect(self.goto_server_clicked)
        self.goto_server_dialogs = list()

        self.logo = QLabel(self)
        self.logo.setGeometry(QtCore.QRect(-50, 30, 500, 100))
        icon = QPixmap("logo500.png")
        self.logo.setPixmap(QPixmap(icon))

        olmage = QImage("./back.JPG")
        slmage = olmage.scaled(QSize(1200, 800))
        palette = QPalette()
        palette.setBrush(10, QBrush(slmage))
        self.setPalette(palette)

        self.setGeometry(150, 100, 1200, 800)
        self.setWindowTitle('스마트 팩토리')
        self.show()

    def goto_server_clicked(self):
        self.close()
        goto_server_dialogs = multi_thread(self)
        self.goto_server_dialogs.append(goto_server_dialogs)
        goto_server_dialogs.show()

    def send_btn_clicked(self):
        #        now = time.localtime()
        #        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        #        s.connect((HOST, PORT))
        #        msg = self.input_text.text()
        #        s.send(msg.encode(encoding='utf_8', errors='strict'))
        #
        #        data = s.recv(1024)
        #        self.send_txtB.append("%04d/%02d/%02d %02d:%02d:%02d" % (now.tm_year, now.tm_mon, now.tm_mday, now.tm_hour,
        #                                                                 now.tm_min, now.tm_sec)
        # + "\n송신 : " + msg + "\n")
        #        # self.send_txtB.adjustSize()
        #        self.recv_txtB.append("%04d/%02d/%02d %02d:%02d:%02d" % (now.tm_year, now.tm_mon, now.tm_mday, now.tm_hour,
        #                                                                 now.tm_min, now.tm_sec)
        # + "\n수신 : " + str(data) + "\n")
        #        # print('수신 데이터 : ' + data.decode('utf_8'))
        #        s.close()

        # con = pymysql.connect(host=HOST, user=USER, password=PASSWORD, db=DB, charset='utf8')
        # cur = con.cursor()
        # cur1 = con.cursor()
        #
        # sql = "UPDATE user_info SET name = %s WHERE name = %s"
        # sql1 = "SELECT name FROM user_info"
        # cur1.execute(sql1)
        #
        # data = cur1.fetchall()
        # li = [x[0] for x in data]
        #
        #
        # cur.execute(sql, (self.input_text.text(), li[1]))
        # con.commit()
        # print(cur.rowcount, '변경')

        #####################
        # def binder(client_socket, addr):
        #     try:
        #         while True:
        #             data = client_socket.recv(4)
        #             length = int.from_bytes(data, "little")
        #             data = client_socket.recv(length)
        #             msg = data.decode()
        #             print('Received from', addr, msg)
        #             msg = "echo : " + msg
        #             data = msg.encode()
        #             length = len(data)
        #             client_socket.sendall(length.to_bytes(4, byteorder='little'))
        #             client_socket.sendall(data)
        #     except:
        #         print("except : ", addr)
        #     finally:
        #         client_socket.close()
        print('send')

    def sudo_btn_clicked(self):
        self.close()
        sudo_btn_dialogs = sudo_menu(self)
        self.sudo_btn_dialogs.append(sudo_btn_dialogs)
        sudo_btn_dialogs.show()

    def manager_btn_clicked(self):
        self.close()
        manager_btn_dialogs = manager_menu(self)
        self.manager_btn_dialogs.append(manager_btn_dialogs)
        manager_btn_dialogs.show()

    def staff_btn_clicked(self):
        self.close()
        staff_menu_dialogs = staff_menu(self)
        self.staff_btn_dialogs.append(staff_menu_dialogs)
        staff_menu_dialogs.show()

    def login_btn_clicked(self):
        self.close()
        login_btn_dialogs = login_window(self)
        self.login_btn_dialogs.append(login_btn_dialogs)
        login_btn_dialogs.show()

    def database_btn_clicked(self):
        # 데이터베이스 연동 테스트
        # msg = self.input_text.text()
        # self.send_txtB.append('송신 : ' + msg)

        con = pymysql.connect(host=HOST, user=USER, password=PASSWORD, db=DB, charset='utf8')
        cur = con.cursor()
        sql = "SELECT * FROM user_info;"
        cur.execute(sql)
        data = cur.fetchall()
        data_li = list(data)

        user_len = len(data_li)
        for x in range(user_len):
            for y in range(0, 7):
                self.recv_txtB.setText(data_li)


# 로그인 화면, 시계
class login_window(QMainWindow):
    def __init__(self, parent=None):
        super(login_window, self).__init__(parent)

        self.ID_txt = QLineEdit(self)
        self.ID_txt.setText("")
        ID_txt_font = QtGui.QFont()
        ID_txt_font.setPointSize(15)
        ID_txt_font.setFamily("서울남산 장체M")
        self.ID_txt.setFont(ID_txt_font)
        self.ID_txt.setGeometry(QtCore.QRect(410, 400, 400, 40))
        self.ID_txt.setPlaceholderText("아이디")

        self.PW_txt = QLineEdit(self)
        self.PW_txt.setText("")
        PW_txt_font = QtGui.QFont()
        PW_txt_font.setPointSize(15)
        PW_txt_font.setFamily("서울남산 장체M")
        self.PW_txt.setFont(PW_txt_font)
        self.PW_txt.setGeometry(QtCore.QRect(410, 450, 400, 40))
        self.PW_txt.setPlaceholderText("비밀번호")
        self.PW_txt.setEchoMode(QLineEdit.Password)
        self.PW_txt.returnPressed.connect(self.login_btn_clicked)

        self.login_btn = QPushButton(self)
        self.login_btn.setGeometry(QtCore.QRect(410, 500, 400, 70))
        self.login_btn.setText("로그인")
        login_btn_font = QtGui.QFont()
        login_btn_font.setPointSize(15)
        login_btn_font.setFamily("서울남산 장체M")
        self.login_btn.setFont(login_btn_font)
        self.login_btn.clicked.connect(self.login_btn_clicked)
        self.login_btn_dialogs = list()
        self.login_btn.setStyleSheet('color:white; background:#0a326f')
        self.login_btn.setCursor(QtGui.QCursor(QtCore.Qt.ClosedHandCursor))

        self.signup_btn = QPushButton(self)
        self.signup_btn.setText("회원 가입")
        signup_btn_font = QtGui.QFont()
        signup_btn_font.setPointSize(10)
        signup_btn_font.setFamily("서울남산 장체M")
        signup_btn_font.setUnderline(True)
        self.signup_btn.setFont(signup_btn_font)
        self.signup_btn.setGeometry(QtCore.QRect(700, 580, 110, 40))
        self.signup_btn.clicked.connect(self.signup_clicked)
        self.signup_btn_dialogs = list()
        self.signup_btn.setStyleSheet('color:white; background:#0a326f')
        self.signup_btn.setCursor(QtGui.QCursor(QtCore.Qt.ClosedHandCursor))

        self.search_PW_btn = QPushButton(self)
        self.search_PW_btn.setText("비밀번호 찾기/변경")
        search_PW_btn_font = QtGui.QFont()
        search_PW_btn_font.setPointSize(10)
        search_PW_btn_font.setFamily("서울남산 장체M")
        search_PW_btn_font.setUnderline(True)
        self.search_PW_btn.setFont(search_PW_btn_font)
        self.search_PW_btn.setGeometry(QtCore.QRect(540, 580, 140, 40))
        self.search_PW_btn.clicked.connect(self.search_PW_clicked)
        self.search_PW_btn_dialogs = list()
        self.search_PW_btn.setStyleSheet('color:white; background:#0a326f')
        self.search_PW_btn.setCursor(QtGui.QCursor(QtCore.Qt.ClosedHandCursor))

        self.search_ID_btn = QPushButton(self)
        self.search_ID_btn.setText("아이디 찾기")
        search_ID_btn_font = QtGui.QFont()
        search_ID_btn_font.setPointSize(10)
        search_ID_btn_font.setFamily("서울남산 장체M")
        search_ID_btn_font.setUnderline(True)
        self.search_ID_btn.setFont(search_ID_btn_font)
        self.search_ID_btn.setGeometry(QtCore.QRect(410, 580, 110, 40))
        self.search_ID_btn.clicked.connect(self.search_ID_clicked)
        self.search_ID_btn_dialogs = list()
        self.search_ID_btn.setStyleSheet('color:white; background:#0a326f')
        self.search_ID_btn.setCursor(QtGui.QCursor(QtCore.Qt.ClosedHandCursor))

        self.logo = QLabel(self)
        self.logo.setGeometry(QtCore.QRect(350, 250, 500, 100))
        icon = QPixmap("logo500.png")
        self.logo.setPixmap(QPixmap(icon))

        olmage = QImage("./back.JPG")
        slmage = olmage.scaled(QSize(1200, 800))
        palette = QPalette()
        palette.setBrush(10, QBrush(slmage))
        self.setPalette(palette)

        self.hour = QLabel(self)
        self.min = QLabel(self)
        self.sec = QLabel(self)

        clock_font = QtGui.QFont()
        clock_font.setPointSize(15)
        clock_font.setFamily("서울남산 장체M")
        self.hour.setFont(clock_font)
        self.min.setFont(clock_font)
        self.sec.setFont(clock_font)
        self.hour.setStyleSheet('color:white')
        self.min.setStyleSheet('color:white')
        self.sec.setStyleSheet('color:white')

        self.hour.setGeometry(1110, 8, 50, 50)
        self.sec.setGeometry(1140, 8, 50, 50)
        self.min.setGeometry(1155, 8, 50, 50)

        self.showtime()

        #시계화면 부

        #

        self.setGeometry(150, 100, 1200, 800)
        self.setWindowTitle('스마트 팩토리 로그인')
        self.show()

    def showtime(self):
        t = time.time()
        kor = time.localtime(t)
        # self.hour.setText(kor.tm_hour)
        # self.min.setText(kor.tm_min)
        self.hour.setText(str(kor.tm_hour))
        self.min.setText(str(kor.tm_min))
        self.sec.setText(":")

        if (kor.tm_sec % 2) == 0:
            self.sec.setVisible(True)
        else:
            self.sec.setVisible(False)

        timer = Timer(1, self.showtime)
        timer.start()


    def login_btn_clicked(self):
        global data_employee, data_pos
        con = pymysql.connect(host=HOST, user=USER, password=PASSWORD, db=DB, charset="utf8")
        cur = con.cursor()
        sql = "SELECT pw FROM user_info WHERE id = %s"

        user_id = self.ID_txt.text()
        user_pw = self.PW_txt.text()

        num = cur.execute(sql, user_id)
        data = cur.fetchone()

        try:
            for j in range(0, num):
                for i in range(0, 2):
                    data_employee = data[j]
            if data_employee == user_pw:
                # print("로그인 성공!")

                sql_position = "SELECT position FROM user_info WHERE id = %s"
                num_position = cur.execute(sql_position, user_id)
                data_position = cur.fetchone()

                for a in range(0, num_position):
                    for b in range(0, 2):
                        data_pos = data_position[a]
                # print("직책 = " + data_pos)

                if data_pos == 'super':
                    self.close()
                    login_btn_dialogs = sudo_menu(self)
                    self.login_btn_dialogs.append(login_btn_dialogs)
                    login_btn_dialogs.show()

                if data_pos == 'manager':
                    self.close()
                    login_btn_dialogs = manager_menu(self)
                    self.login_btn_dialogs.append(login_btn_dialogs)
                    login_btn_dialogs.show()

                if data_pos == 'employee':
                    self.close()
                    login_btn_dialogs = staff_menu(self)
                    self.login_btn_dialogs.append(login_btn_dialogs)
                    login_btn_dialogs.show()

            else:
                login_btn_dialogs = loginalarm_window(self)
                self.login_btn_dialogs.append(login_btn_dialogs)
                login_btn_dialogs.show()
        except:
            login_btn_dialogs = loginalarm_window(self)
            self.login_btn_dialogs.append(login_btn_dialogs)
            login_btn_dialogs.show()
        # self.close()
        # login_btn_dialogs = First(self)
        # self.login_btn_dialogs.append(login_btn_dialogs)
        # login_btn_dialogs.show()

    def search_ID_clicked(self):
        self.close()
        search_ID_dialogs = search_ID(self)
        self.search_ID_btn_dialogs.append(search_ID_dialogs)
        search_ID_dialogs.show()

    def search_PW_clicked(self):
        self.close()
        search_PW_dialogs = search_PW(self)
        self.search_PW_btn_dialogs.append(search_PW_dialogs)
        search_PW_dialogs.show()

    # def back_btn_clicked(self):
    #     self.close()
    #     back_btn_dialogs = First(self)
    #     self.back_btn_dialogs.append(back_btn_dialogs)
    #     back_btn_dialogs.show()

    def signup_clicked(self):
        self.close()
        signup_btn_dialog = sign_up(self)
        self.signup_btn_dialogs.append(signup_btn_dialog)
        signup_btn_dialog.show()


#

# 아이디 찾기 화면
class search_ID(QMainWindow):
    def __init__(self, parent=None):
        super(search_ID, self).__init__(parent)

        #

        self.name_label = QLabel(self)
        self.name_label.setText("이름")
        name_label_font = QtGui.QFont()
        name_label_font.setPointSize(10)
        name_label_font.setFamily("서울남산 장체M")
        self.name_label.setFont(name_label_font)
        self.name_label.setGeometry(QtCore.QRect(440, 270, 350, 40))

        self.name_txt = QLineEdit(self)
        self.name_txt.setText("")
        name_txt_font = QtGui.QFont()
        name_txt_font.setPointSize(15)
        name_txt_font.setFamily("서울남산 장체M")
        self.name_txt.setFont(name_txt_font)
        self.name_txt.setGeometry(QtCore.QRect(440, 310, 350, 40))
        self.name_txt.setPlaceholderText("이름를 입력하세요.")

        #

        self.birth_label = QLabel(self)
        self.birth_label.setText("생년월일")
        birth_label_font = QtGui.QFont()
        birth_label_font.setPointSize(10)
        birth_label_font.setFamily("서울남산 장체M")
        self.birth_label.setFont(birth_label_font)
        self.birth_label.setGeometry(QtCore.QRect(440, 350, 350, 40))

        self.birth_year = QLineEdit(self)
        self.birth_year.setText("")
        birth_year_font = QtGui.QFont()
        birth_year_font.setPointSize(15)
        birth_year_font.setFamily("서울남산 장체M")
        self.birth_year.setFont(birth_year_font)
        self.birth_year.setGeometry(QtCore.QRect(440, 390, 100, 40))
        self.birth_year.setPlaceholderText("YYYY")
        self.birth_year.setValidator(QIntValidator(0, 1000))

        self.hipen1_label = QLabel(self)
        self.hipen1_label.setText("-")
        hipen1_label_font = QtGui.QFont()
        hipen1_label_font.setPointSize(10)
        hipen1_label_font.setFamily("서울남산 장체M")
        self.hipen1_label.setFont(hipen1_label_font)
        self.hipen1_label.setGeometry(QtCore.QRect(560, 390, 100, 40))

        self.birth_month = QLineEdit(self)
        self.birth_month.setText("")
        birth_month_font = QtGui.QFont()
        birth_month_font.setPointSize(15)
        birth_month_font.setFamily("서울남산 장체M")
        self.birth_month.setFont(birth_month_font)
        self.birth_month.setGeometry(QtCore.QRect(580, 390, 50, 40))
        self.birth_month.setPlaceholderText("MM")
        self.birth_month.setValidator(QIntValidator(0, 10))

        self.hipen2_label = QLabel(self)
        self.hipen2_label.setText("-")
        hipen2_label_font = QtGui.QFont()
        hipen2_label_font.setPointSize(10)
        hipen2_label_font.setFamily("서울남산 장체M")
        self.hipen2_label.setFont(hipen2_label_font)
        self.hipen2_label.setGeometry(QtCore.QRect(650, 390, 100, 40))

        self.birth_days = QLineEdit(self)
        self.birth_days.setText("")
        birth_days_font = QtGui.QFont()
        birth_days_font.setPointSize(15)
        birth_days_font.setFamily("서울남산 장체M")
        self.birth_days.setFont(birth_days_font)
        self.birth_days.setGeometry(QtCore.QRect(670, 390, 50, 40))
        self.birth_days.setPlaceholderText("DD")
        self.birth_days.setValidator(QIntValidator(0, 10))

        #

        self.email_label = QLabel(self)
        self.email_label.setText("이메일")
        email_label_font = QtGui.QFont()
        email_label_font.setPointSize(10)
        email_label_font.setFamily("서울남산 장체M")
        self.email_label.setFont(email_label_font)
        self.email_label.setGeometry(QtCore.QRect(440, 430, 350, 40))

        self.email_txt = QLineEdit(self)
        self.email_txt.setText("")
        email_txt_font = QtGui.QFont()
        email_txt_font.setPointSize(15)
        email_txt_font.setFamily("서울남산 장체M")
        self.email_txt.setFont(email_txt_font)
        self.email_txt.setGeometry(QtCore.QRect(440, 470, 350, 40))
        self.email_txt.setPlaceholderText("이메일을 입력하세요.")
        self.email_txt.returnPressed.connect(self.search_ID_btn_clicked)

        #

        # self.user_name = self.name_txt.text()
        # self.user_birth = "%s-%s-%s" % (self.birth_year.text(), self.birth_month.text(), self.birth_days.text())
        # self.user_email = self.email_txt.text()

        self.search_ID_btn = QPushButton(self)
        self.search_ID_btn.setText("아이디 찾기")
        search_ID_btn_font = QtGui.QFont()
        search_ID_btn_font.setPointSize(15)
        search_ID_btn_font.setFamily("서울남산 장체M")
        self.search_ID_btn.setFont(search_ID_btn_font)
        self.search_ID_btn.setGeometry(QtCore.QRect(440, 550, 350, 60))
        self.search_ID_btn.setStyleSheet('color:white; background:#0a326f')
        self.search_ID_btn.clicked.connect(self.search_ID_btn_clicked)
        self.search_ID_btn_dialogs = list()
        self.search_ID_btn.setCursor(QtGui.QCursor(QtCore.Qt.ClosedHandCursor))

        self.ID_label1 = QLabel(self)
        ID_label1_font = QtGui.QFont()
        ID_label1_font.setPointSize(15)
        ID_label1_font.setFamily("서울남산 장체M")
        self.ID_label1.setFont(ID_label1_font)
        self.ID_label1.setGeometry(QtCore.QRect(5200, 6300, 350, 60))

        self.ID_label2 = QLabel(self)
        ID_label2_font = QtGui.QFont()
        ID_label2_font.setPointSize(15)
        ID_label2_font.setFamily("서울남산 장체M")
        self.ID_label2.setFont(ID_label2_font)
        self.ID_label2.setGeometry(QtCore.QRect(5200, 6700, 350, 60))

        self.logo = QLabel(self)
        self.logo.setGeometry(QtCore.QRect(-50, 30, 500, 100))
        icon = QPixmap("logo500.png")
        self.logo.setPixmap(QPixmap(icon))

        olmage = QImage("./back.JPG")
        slmage = olmage.scaled(QSize(1200, 800))
        palette = QPalette()
        palette.setBrush(10, QBrush(slmage))
        self.setPalette(palette)

        self.back_btn = QPushButton(self)
        self.back_btn.setGeometry(QtCore.QRect(0, 89, 80, 52))
        self.back_btn.setText("뒤로가기")
        back_btn_font = QtGui.QFont()
        back_btn_font.setPointSize(10)
        back_btn_font.setFamily("서울남산 장체M")
        self.back_btn.setFont(back_btn_font)
        self.back_btn.clicked.connect(self.back_btn_clicked)
        self.back_btn_dialogs = list()
        self.back_btn.setCursor(QtGui.QCursor(QtCore.Qt.ClosedHandCursor))
        self.back_btn.setStyleSheet('color:white; background-color:rgba(1, 0, 0, 0.1)')

        self.setGeometry(150, 100, 1200, 800)
        self.setWindowTitle('아이디 찾기')
        self.show()

    def search_ID_btn_clicked(self):
        try:
            user_name = self.name_txt.text()
            user_birth = "%s-%s-%s" % (self.birth_year.text(), self.birth_month.text(), self.birth_days.text())
            user_email = self.email_txt.text()

            # print(user_name, user_birth, user_email)

            con = pymysql.connect(host=HOST, user=USER, password=PASSWORD, db=DB, charset="utf8")
            cur = con.cursor()
            sql = "SELECT id FROM user_info WHERE name = %s and birth = %s and email = %s"
            cur.execute(sql, (user_name, user_birth, user_email))
            data_list = [data[0] for data in cur.fetchall()]
            # print(data_list[0])

            # search_ID_btn_dialogs = show_ID(self)
            # self.search_ID_btn_dialogs.append(search_ID_btn_dialogs)
            # search_ID_btn_dialogs.show()

            self.ID_label1.setText("회원님의 아이디는")
            self.ID_label1.setGeometry(QtCore.QRect(520, 630, 350, 60))
            self.ID_label2.setText("'" + str(data_list[0]) + "' 입니다.")
            self.ID_label2.setGeometry(QtCore.QRect(520, 670, 350, 60))
        except:
            self.ID_label1.setText("입력한 정보를 다시 확인해주세요.")
            self.ID_label1.setGeometry(460, 630, 350, 60)

    def back_btn_clicked(self):
        self.close()
        back_btn_dialogs = login_window(self)
        self.back_btn_dialogs.append(back_btn_dialogs)
        back_btn_dialogs.show()


# 아이디 출력창
# class show_ID(QMainWindow):
#     def __init__(self, parent=None):
#         super(show_ID, self).__init__(parent)
#
#         con = pymysql.connect(host="192.168.0.19", user="root",
#                               password="1234", db="mydb", charset="utf8")
#         cur = con.cursor()
#         sql_name = "SELECT id FROM user_info WHERE name = %s WHERE birth = %s WHERE email = %s"
#
#
#         self.setGeometry(600, 450, 300, 200)
#         self.setWindowTitle('알림')
#         self.show()


class search_PW(QMainWindow):
    def __init__(self, parent=None):
        super(search_PW, self).__init__(parent)

        # self.search_PW_btn_dialogs = list()
        self.previous_ID_txt = QLineEdit(self)
        self.previous_ID_label = QLabel(self)
        self.PW_alarm_label1 = QLabel(self)
        self.PW_print_label2 = QLabel(self)
        self.PW_print_label1 = QLabel(self)
        self.change_PW_btn = QPushButton(self)
        self.name_txt = QLineEdit(self)
        self.name_label = QLabel(self)
        self.ID_txt = QLineEdit(self)
        self.ID_label = QLabel(self)
        self.previous_PW_label = QLabel(self)
        self.previous_PW_txt = QLineEdit(self)
        self.change_PW_label = QLabel(self)
        self.change_PW_txt = QLineEdit(self)
        self.change_PW_txt2 = QLineEdit(self)
        self.search_PW_btn = QPushButton(self)

        self.previous_ID_txt.setGeometry(5000, 5000, 350, 40)
        self.previous_ID_label.setGeometry(5000, 5000, 350, 40)
        self.PW_alarm_label1.setGeometry(5000, 5000, 350, 40)
        self.PW_print_label1.setGeometry(5000, 5000, 350, 40)
        self.PW_print_label2.setGeometry(5000, 5000, 350, 40)
        self.change_PW_btn.setGeometry(5000, 5000, 350, 40)
        self.name_txt.setGeometry(5000, 5000, 350, 40)
        self.name_label.setGeometry(5000, 5000, 350, 40)
        self.ID_txt.setGeometry(5000, 5000, 350, 40)
        self.ID_label.setGeometry(5000, 5000, 350, 40)
        self.previous_PW_txt.setGeometry(5000, 5000, 350, 40)
        self.previous_PW_label.setGeometry(5000, 5000, 350, 40)
        self.change_PW_label.setGeometry(5000, 5000, 350, 40)
        self.change_PW_txt.setGeometry(5000, 5000, 350, 40)
        self.change_PW_txt2.setGeometry(5000, 5000, 350, 40)
        self.search_PW_btn.setGeometry(5000, 5000, 350, 40)

        ##############

        self.PW_search_btn = QPushButton(self)
        self.PW_search_btn.setText("비밀번호 찾기")
        PW_search_btn_font = QtGui.QFont()
        PW_search_btn_font.setPointSize(15)
        PW_search_btn_font.setFamily("서울남산 장체M")
        self.PW_search_btn.setFont(PW_search_btn_font)
        self.PW_search_btn.setGeometry(QtCore.QRect(440, 250, 160, 60))
        self.PW_search_btn.setStyleSheet('color:white; background:#0a326f')
        self.PW_search_btn.clicked.connect(self.PW_search_btn_clicked)
        self.PW_search_btn_dialogs = list()
        self.PW_search_btn.setCursor(QtGui.QCursor(QtCore.Qt.ClosedHandCursor))

        self.PW_change_btn = QPushButton(self)
        self.PW_change_btn.setText("비밀번호 변경")
        PW_change_btn_font = QtGui.QFont()
        PW_change_btn_font.setPointSize(15)
        PW_change_btn_font.setFamily("서울남산 장체M")
        self.PW_change_btn.setFont(PW_change_btn_font)
        self.PW_change_btn.setGeometry(QtCore.QRect(630, 250, 160, 60))
        self.PW_change_btn.setStyleSheet('color:white; background:#0a326f')
        self.PW_change_btn.clicked.connect(self.PW_change_btn_clicked)
        self.PW_change_btn_dialogs = list()
        self.PW_change_btn.setCursor(QtGui.QCursor(QtCore.Qt.ClosedHandCursor))

        #

        #

        self.logo = QLabel(self)
        self.logo.setGeometry(QtCore.QRect(-50, 30, 500, 100))
        icon = QPixmap("logo500.png")
        self.logo.setPixmap(QPixmap(icon))

        olmage = QImage("./back.JPG")
        slmage = olmage.scaled(QSize(1200, 800))
        palette = QPalette()
        palette.setBrush(10, QBrush(slmage))
        self.setPalette(palette)

        self.back_btn = QPushButton(self)
        self.back_btn.setGeometry(QtCore.QRect(0, 89, 80, 52))
        self.back_btn.setText("뒤로가기")
        back_btn_font = QtGui.QFont()
        back_btn_font.setPointSize(10)
        back_btn_font.setFamily("서울남산 장체M")
        self.back_btn.setFont(back_btn_font)
        self.back_btn.clicked.connect(self.back_btn_clicked)
        self.back_btn_dialogs = list()
        self.back_btn.setCursor(QtGui.QCursor(QtCore.Qt.ClosedHandCursor))
        self.back_btn.setStyleSheet('color:white; background-color:rgba(1, 0, 0, 0.1)')

        self.setGeometry(150, 100, 1200, 800)
        self.setWindowTitle('비밀번호 찾기')
        self.show()

    def PW_search_btn_clicked(self):  # 비밀번호 찾기
        self.ID_label.setText("아이디")
        ID_label_font = QtGui.QFont()
        ID_label_font.setPointSize(10)
        ID_label_font.setFamily("서울남산 장체M")
        self.ID_label.setFont(ID_label_font)
        self.ID_label.setGeometry(QtCore.QRect(440, 310, 350, 40))

        self.ID_txt.setText("")
        ID_txt_font = QtGui.QFont()
        ID_txt_font.setPointSize(15)
        ID_txt_font.setFamily("서울남산 장체M")
        self.ID_txt.setFont(ID_txt_font)
        self.ID_txt.setGeometry(QtCore.QRect(440, 350, 350, 40))
        self.ID_txt.setPlaceholderText("아이디를 입력하세요..")

        #

        self.name_label.setText("이름")
        name_label_font = QtGui.QFont()
        name_label_font.setPointSize(10)
        name_label_font.setFamily("서울남산 장체M")
        self.name_label.setFont(name_label_font)
        self.name_label.setGeometry(QtCore.QRect(440, 390, 350, 40))

        self.name_txt.setText("")
        name_txt_font = QtGui.QFont()
        name_txt_font.setPointSize(15)
        name_txt_font.setFamily("서울남산 장체M")
        self.name_txt.setFont(name_txt_font)
        self.name_txt.setGeometry(QtCore.QRect(440, 430, 350, 40))
        self.name_txt.setPlaceholderText("이름를 입력하세요.")
        self.name_txt.returnPressed.connect(self.search_PW_btn_clicked)

        self.search_PW_btn.setText("비밀번호 찾기")
        search_PW_btn_font = QtGui.QFont()
        search_PW_btn_font.setPointSize(15)
        search_PW_btn_font.setFamily("서울남산 장체M")
        self.search_PW_btn.setFont(search_PW_btn_font)
        self.search_PW_btn.setGeometry(QtCore.QRect(440, 510, 350, 60))
        self.search_PW_btn.setStyleSheet('color:white; background:#0a326f')
        self.search_PW_btn.clicked.connect(self.search_PW_btn_clicked)
        self.search_PW_btn.setCursor(QtGui.QCursor(QtCore.Qt.ClosedHandCursor))

        PW_print_label1_font = QtGui.QFont()
        PW_print_label1_font.setPointSize(15)
        PW_print_label1_font.setFamily("서울남산 장체M")
        self.PW_print_label1.setFont(PW_print_label1_font)
        self.PW_print_label1.setGeometry(QtCore.QRect(5200, 6300, 350, 60))

        PW_print_label2_font = QtGui.QFont()
        PW_print_label2_font.setPointSize(15)
        PW_print_label2_font.setFamily("서울남산 장체M")
        self.PW_print_label2.setFont(PW_print_label2_font)
        self.PW_print_label2.setGeometry(QtCore.QRect(5200, 6300, 350, 60))

        self.previous_ID_label.setGeometry(5000, 5000, 350, 40)
        self.previous_ID_txt.setGeometry(5000, 5000, 350, 40)
        self.previous_PW_label.setGeometry(5000, 5000, 350, 40)
        self.previous_PW_txt.setGeometry(5000, 5000, 350, 40)
        self.change_PW_txt.setGeometry(5000, 5000, 350, 40)
        self.change_PW_label.setGeometry(5000, 5000, 350, 40)
        self.change_PW_txt2.setGeometry(5000, 5000, 350, 40)
        self.change_PW_btn.setGeometry(5000, 5000, 350, 40)
        self.PW_alarm_label1.setGeometry(5000, 5000, 350, 40)

    def search_PW_btn_clicked(self):
        try:
            user_ID = self.ID_txt.text()
            user_name = self.name_txt.text()

            con = pymysql.connect(host=HOST, user=USER, password=PASSWORD, db=DB, charset="utf8")
            cur = con.cursor()
            sql = "SELECT pw FROM user_info WHERE id = %s and name = %s"
            cur.execute(sql, (user_ID, user_name))
            data_list = [data[0] for data in cur.fetchall()]

            self.PW_print_label1.setText("회원님의 비밀번호는")
            self.PW_print_label1.setGeometry(QtCore.QRect(520, 590, 350, 60))
            self.PW_print_label2.setText("'" + str(data_list[0] + "' 입니다."))
            self.PW_print_label2.setGeometry(QtCore.QRect(520, 630, 350, 60))
        except:
            self.PW_print_label1.setText("입력한 정보를 다시 확인해주세요.")
            self.PW_print_label1.setGeometry(QtCore.QRect(460, 590, 350, 60))
            self.PW_print_label2.setGeometry(QtCore.QRect(5000, 5000, 350, 60))

    def PW_change_btn_clicked(self):  # 비밀번호 변경
        self.previous_ID_label.setText("아이디")
        previous_ID_label_font = QtGui.QFont()
        previous_ID_label_font.setPointSize(10)
        previous_ID_label_font.setFamily("서울남산 장체M")
        self.previous_ID_label.setFont(previous_ID_label_font)
        self.previous_ID_label.setGeometry(QtCore.QRect(440, 310, 350, 40))

        self.previous_ID_txt.setText("")
        previous_ID_txt_font = QtGui.QFont()
        previous_ID_txt_font.setPointSize(15)
        previous_ID_txt_font.setFamily("서울남산 장체M")
        self.previous_ID_txt.setFont(previous_ID_txt_font)
        self.previous_ID_txt.setGeometry(QtCore.QRect(440, 350, 350, 40))
        self.previous_ID_txt.setPlaceholderText("아이디를 입력하세요.")

        self.previous_PW_label.setText("현재 비밀번호")
        previous_PW_label_font = QtGui.QFont()
        previous_PW_label_font.setPointSize(10)
        previous_PW_label_font.setFamily("서울남산 장체M")
        self.previous_PW_label.setFont(previous_PW_label_font)
        self.previous_PW_label.setGeometry(QtCore.QRect(440, 390, 350, 40))

        self.previous_PW_txt.setText("")
        previous_PW_txt_font = QtGui.QFont()
        previous_PW_txt_font.setPointSize(15)
        previous_PW_txt_font.setFamily("서울남산 장체M")
        self.previous_PW_txt.setFont(previous_PW_txt_font)
        self.previous_PW_txt.setGeometry(QtCore.QRect(440, 430, 350, 40))
        self.previous_PW_txt.setPlaceholderText("현재 비밀번호를 입력하세요.")
        self.previous_PW_txt.setEchoMode(QLineEdit.PasswordEchoOnEdit)

        self.change_PW_label.setText("바꿀 비밀번호")
        change_PW_label_font = QtGui.QFont()
        change_PW_label_font.setPointSize(10)
        change_PW_label_font.setFamily("서울남산 장체M")
        self.change_PW_label.setFont(change_PW_label_font)
        self.change_PW_label.setGeometry(QtCore.QRect(440, 470, 350, 40))

        self.change_PW_txt.setText("")
        change_PW_txt_font = QtGui.QFont()
        change_PW_txt_font.setPointSize(15)
        change_PW_txt_font.setFamily("서울남산 장체M")
        self.change_PW_txt.setFont(change_PW_txt_font)
        self.change_PW_txt.setGeometry(QtCore.QRect(440, 510, 350, 40))
        self.change_PW_txt.setPlaceholderText("바꿀 비밀번호를 입력하세요.")
        self.change_PW_txt.setEchoMode(QLineEdit.PasswordEchoOnEdit)

        self.change_PW_txt2.setText("")
        change_PW_txt2_font = QtGui.QFont()
        change_PW_txt2_font.setPointSize(15)
        change_PW_txt2_font.setFamily("서울남산 장체M")
        self.change_PW_txt2.setFont(change_PW_txt2_font)
        self.change_PW_txt2.setGeometry(QtCore.QRect(440, 570, 350, 40))
        self.change_PW_txt2.setPlaceholderText("한번 더 입력하세요.")
        self.change_PW_txt2.setEchoMode(QLineEdit.PasswordEchoOnEdit)
        self.change_PW_txt2.returnPressed.connect(self.change_PW_btn_clicked)

        self.change_PW_btn.setText("비밀번호 변경")
        change_PW_btn_font = QtGui.QFont()
        change_PW_btn_font.setPointSize(15)
        change_PW_btn_font.setFamily("서울남산 장체M")
        self.change_PW_btn.setFont(change_PW_btn_font)
        self.change_PW_btn.setGeometry(QtCore.QRect(440, 650, 350, 60))
        self.change_PW_btn.setCursor(QtGui.QCursor(QtCore.Qt.ClosedHandCursor))
        self.change_PW_btn.setStyleSheet('color:white; background:#0a326f')
        self.change_PW_btn.clicked.connect(self.change_PW_btn_clicked)

        self.PW_alarm_label1.setText("회원님의 비밀번호는")
        # self.PW_alarm_label1.setGeometry(QtCore.QRect(5200, 6500, 350, 60))
        PW_alarm_label1_font = QtGui.QFont()
        PW_alarm_label1_font.setPointSize(15)
        PW_alarm_label1_font.setFamily("서울남산 장체M")
        self.PW_alarm_label1.setFont(PW_alarm_label1_font)

        self.ID_label.setGeometry(5000, 5000, 350, 40)
        self.ID_txt.setGeometry(5000, 5000, 350, 40)
        self.name_label.setGeometry(5000, 5000, 350, 40)
        self.name_txt.setGeometry(5000, 5000, 350, 40)
        self.search_PW_btn.setGeometry(5000, 5000, 350, 40)
        self.PW_print_label1.setGeometry(5000, 5000, 350, 40)
        self.PW_print_label2.setGeometry(5000, 5000, 350, 40)
        self.PW_alarm_label1.setGeometry(5000, 5000, 350, 40)

    def change_PW_btn_clicked(self):
        try:
            con = pymysql.connect(host=HOST, user=USER, password=PASSWORD, db=DB, charset='utf8', autocommit=True)
            cur = con.cursor()
            sql = "SELECT id FROM user_info WHERE id = %s and pw = %s"
            cur.execute(sql, (self.previous_ID_txt.text(), self.previous_PW_txt.text()))
            data_list = [data[0] for data in cur.fetchall()]

            cur_2 = con.cursor()
            sql_2 = "SELECT pw FROM user_info WHERE id = %s and pw = %s"
            cur_2.execute(sql_2, (self.previous_ID_txt.text(), self.previous_PW_txt.text()))
            data_list_2 = [data_2[0] for data_2 in cur_2.fetchall()]

            if data_list_2[0] == self.previous_PW_txt.text():
                if self.change_PW_txt.text() == self.change_PW_txt2.text():
                    if self.change_PW_txt.text() == "":
                        self.PW_alarm_label1.setText("바꿀 비밀번호를 다시 설정하세요.")
                        self.PW_alarm_label1.setGeometry(460, 710, 350, 60)

                    else:
                        sql_update = "UPDATE user_info SET pw = %s WHERE id = %s"
                        cur_update = con.cursor()
                        cur_update.execute(sql_update, (self.change_PW_txt.text(), data_list[0]))
                        self.PW_alarm_label1.setText("비밀번호가 변경되었습니다.")
                        self.PW_alarm_label1.setGeometry(480, 710, 350, 60)
                else:
                    self.PW_alarm_label1.setText("바꿀 비밀번호가 일치하지 않습니다.")
                    self.PW_alarm_label1.setGeometry(460, 710, 350, 60)
            else:
                self.PW_alarm_label1.setText("현재 비밀번호를 다시 입력하세요.")
                self.PW_alarm_label1.setGeometry(460, 710, 350, 60)
        except:
            self.PW_alarm_label1.setText("올바른 정보를 입력하세요.")
            self.PW_alarm_label1.setGeometry(480, 710, 350, 60)

    def back_btn_clicked(self):
        self.close()
        back_btn_dialogs = login_window(self)
        self.back_btn_dialogs.append(back_btn_dialogs)
        back_btn_dialogs.show()


#


class loginalarm_window(QDialog):
    def __init__(self, parent=None):
        super(loginalarm_window, self).__init__(parent)

        self.mainlabel_txt = QLabel(self)
        self.mainlabel_txt.setText("아이디 또는 비밀번호가 잘못되었습니다.")
        mainlabel_txt_font = QtGui.QFont()
        mainlabel_txt_font.setPointSize(10)
        mainlabel_txt_font.setFamily("서울남산 장체M")
        self.mainlabel_txt.setFont(mainlabel_txt_font)
        self.mainlabel_txt.setGeometry(QtCore.QRect(20, 50, 300, 41))

        self.accept_btn = QPushButton(self)
        self.accept_btn.setText('확인')
        accept_btn_font = QtGui.QFont()
        accept_btn_font.setPointSize(10)
        accept_btn_font.setFamily("서울남산 장체M")
        self.accept_btn.setFont(accept_btn_font)
        self.accept_btn.setGeometry(QtCore.QRect(105, 120, 100, 50))
        self.accept_btn.clicked.connect(self.accept_btn_clicked)
        self.accept_btn_dialogs = list()

        self.setGeometry(600, 450, 300, 200)
        self.setWindowTitle('로그인 실패')
        self.show()

    def accept_btn_clicked(self):
        self.close()


# 회원가입 화면
class sign_up(QMainWindow):
    def __init__(self, parent=None):
        super(sign_up, self).__init__(parent)

        self.ID_label = QLabel(self)
        self.ID_label.setText("아이디")
        ID_label_font = QtGui.QFont()
        ID_label_font.setPointSize(10)
        ID_label_font.setFamily("서울남산 장체M")
        self.ID_label.setFont(ID_label_font)
        self.ID_label.setGeometry(QtCore.QRect(440, 170, 350, 40))

        self.ID_txt = QLineEdit(self)
        self.ID_txt.setText("")
        ID_txt_font = QtGui.QFont()
        ID_txt_font.setPointSize(15)
        ID_txt_font.setFamily("서울남산 장체M")
        self.ID_txt.setFont(ID_txt_font)
        self.ID_txt.setGeometry(QtCore.QRect(440, 210, 350, 40))
        self.ID_txt.setPlaceholderText("아이디를 입력하세요.")

        #

        self.PW_label = QLabel(self)
        self.PW_label.setText("비밀번호")
        PW_label_font = QtGui.QFont()
        PW_label_font.setPointSize(10)
        PW_label_font.setFamily("서울남산 장체M")
        self.PW_label.setFont(PW_label_font)
        self.PW_label.setGeometry(QtCore.QRect(440, 250, 350, 40))

        self.PW_txt = QLineEdit(self)
        self.PW_txt.setText("")
        self.PW_txt.setEchoMode(QLineEdit.PasswordEchoOnEdit)
        PW_txt_font = QtGui.QFont()
        PW_txt_font.setPointSize(15)
        PW_txt_font.setFamily("서울남산 장체M")
        self.PW_txt.setFont(PW_txt_font)
        self.PW_txt.setGeometry(QtCore.QRect(440, 290, 350, 40))
        self.PW_txt.setPlaceholderText("비밀번호를 입력하세요.")

        #

        self.name_label = QLabel(self)
        self.name_label.setText("이름")
        name_label_font = QtGui.QFont()
        name_label_font.setPointSize(10)
        name_label_font.setFamily("서울남산 장체M")
        self.name_label.setFont(name_label_font)
        self.name_label.setGeometry(QtCore.QRect(440, 330, 350, 40))

        self.name_txt = QLineEdit(self)
        self.name_txt.setText("")
        name_txt_font = QtGui.QFont()
        name_txt_font.setPointSize(15)
        name_txt_font.setFamily("서울남산 장체M")
        self.name_txt.setFont(PW_txt_font)
        self.name_txt.setGeometry(QtCore.QRect(440, 370, 350, 40))
        self.name_txt.setPlaceholderText("이름를 입력하세요.")

        #

        self.position_label = QLabel(self)
        self.position_label.setText("직책")
        position_label_font = QtGui.QFont()
        position_label_font.setPointSize(10)
        position_label_font.setFamily("서울남산 장체M")
        self.position_label.setFont(position_label_font)
        self.position_label.setGeometry(QtCore.QRect(440, 410, 350, 40))

        self.position_CB = QComboBox(self)
        # self.position_CB.addItem("")
        self.position_CB.addItems(["직원", "관리자"])
        position_CB_font = QtGui.QFont()
        position_CB_font.setPointSize(15)
        position_CB_font.setFamily("서울남산 장체M")
        self.position_CB.setFont(position_CB_font)
        self.position_CB.setGeometry(QtCore.QRect(440, 450, 350, 40))

        #

        self.birth_label = QLabel(self)
        self.birth_label.setText("생년월일")
        birth_label_font = QtGui.QFont()
        birth_label_font.setPointSize(10)
        birth_label_font.setFamily("서울남산 장체M")
        self.birth_label.setFont(birth_label_font)
        self.birth_label.setGeometry(QtCore.QRect(440, 490, 350, 40))

        self.birth_year = QLineEdit(self)
        self.birth_year.setText("")
        birth_year_font = QtGui.QFont()
        birth_year_font.setPointSize(15)
        birth_year_font.setFamily("서울남산 장체M")
        self.birth_year.setFont(birth_year_font)
        self.birth_year.setGeometry(QtCore.QRect(440, 530, 100, 40))
        self.birth_year.setPlaceholderText("YYYY")

        self.hipen1_label = QLabel(self)
        self.hipen1_label.setText("-")
        hipen1_label_font = QtGui.QFont()
        hipen1_label_font.setPointSize(10)
        hipen1_label_font.setFamily("서울남산 장체M")
        self.hipen1_label.setFont(hipen1_label_font)
        self.hipen1_label.setGeometry(QtCore.QRect(560, 530, 100, 40))

        self.birth_month = QLineEdit(self)
        self.birth_month.setText("")
        birth_month_font = QtGui.QFont()
        birth_month_font.setPointSize(15)
        birth_month_font.setFamily("서울남산 장체M")
        self.birth_month.setFont(birth_month_font)
        self.birth_month.setGeometry(QtCore.QRect(580, 530, 50, 40))
        self.birth_month.setPlaceholderText("MM")

        self.hipen2_label = QLabel(self)
        self.hipen2_label.setText("-")
        hipen2_label_font = QtGui.QFont()
        hipen2_label_font.setPointSize(10)
        hipen2_label_font.setFamily("서울남산 장체M")
        self.hipen2_label.setFont(hipen2_label_font)
        self.hipen2_label.setGeometry(QtCore.QRect(650, 530, 100, 40))

        self.birth_days = QLineEdit(self)
        self.birth_days.setText("")
        birth_days_font = QtGui.QFont()
        birth_days_font.setPointSize(15)
        birth_days_font.setFamily("서울남산 장체M")
        self.birth_days.setFont(birth_days_font)
        self.birth_days.setGeometry(QtCore.QRect(670, 530, 50, 40))
        self.birth_days.setPlaceholderText("DD")

        #

        self.email_label = QLabel(self)
        self.email_label.setText("이메일")
        email_label_font = QtGui.QFont()
        email_label_font.setPointSize(10)
        email_label_font.setFamily("서울남산 장체M")
        self.email_label.setFont(email_label_font)
        self.email_label.setGeometry(QtCore.QRect(440, 570, 350, 40))

        self.email_txt = QLineEdit(self)
        self.email_txt.setText("")
        email_txt_font = QtGui.QFont()
        email_txt_font.setPointSize(15)
        email_txt_font.setFamily("서울남산 장체M")
        self.email_txt.setFont(email_txt_font)
        self.email_txt.setGeometry(QtCore.QRect(440, 610, 350, 40))
        self.email_txt.setPlaceholderText("이메일을 입력하세요.")

        #

        self.sign_up_btn = QPushButton(self)
        self.sign_up_btn.setText("회원 가입")
        sign_up_btn_font = QtGui.QFont()
        sign_up_btn_font.setPointSize(15)
        sign_up_btn_font.setFamily("서울남산 장체M")
        self.sign_up_btn.setFont(sign_up_btn_font)
        self.sign_up_btn.setGeometry(QtCore.QRect(440, 680, 350, 60))
        self.sign_up_btn.setStyleSheet('color:white; background:#0a326f')
        self.sign_up_btn.clicked.connect(self.sign_up_btn_clicked)
        self.sign_up_btn_dialogs = list()

        self.logo = QLabel(self)
        self.logo.setGeometry(QtCore.QRect(-50, 30, 500, 100))
        icon = QPixmap("logo500.png")
        self.logo.setPixmap(QPixmap(icon))

        olmage = QImage("./back.JPG")
        slmage = olmage.scaled(QSize(1200, 800))
        palette = QPalette()
        palette.setBrush(10, QBrush(slmage))
        self.setPalette(palette)

        self.back_btn = QPushButton(self)
        self.back_btn.setGeometry(QtCore.QRect(0, 89, 80, 52))
        self.back_btn.setText("뒤로가기")
        back_btn_font = QtGui.QFont()
        back_btn_font.setPointSize(10)
        back_btn_font.setFamily("서울남산 장체M")
        self.back_btn.setFont(back_btn_font)
        self.back_btn.clicked.connect(self.back_btn_clicked)
        self.back_btn_dialogs = list()
        self.back_btn.setCursor(QtGui.QCursor(QtCore.Qt.ClosedHandCursor))
        self.back_btn.setStyleSheet('color:white; background-color:rgba(1, 0, 0, 0.1)')

        self.setGeometry(150, 100, 1200, 800)
        self.setWindowTitle('스마트 팩토리 회원가입')
        self.show()

    def sign_up_btn_clicked(self):
        global sign_position
        con = pymysql.connect(host="192.168.0.19", user="root",
                              password="1234", db="mydb", charset="utf8", autocommit=True)
        cur_insert = con.cursor()

        sign_id = self.ID_txt.text()
        sign_pw = self.PW_txt.text()
        sign_name = self.name_txt.text()
        sign_birth = "%s-%s-%s" % (self.birth_year.text(), self.birth_month.text(), self.birth_days.text())
        sign_email = self.email_txt.text()

        if self.position_CB.currentText() == '관리자':
            sign_position = 'manager'
        if self.position_CB.currentText() == '직원':
            sign_position = 'employee'

        cur_insert.execute("INSERT INTO user_info(name, birth, id, pw, email, position) "
                           "VALUES ('%s', '%s', '%s', '%s', '%s', '%s')" %
                           (''.join(sign_name), ''.join(sign_birth),
                            ''.join(sign_id), ''.join(sign_pw),
                            ''.join(sign_email), ''.join(sign_position)))

        self.close()
        sign_up_btn_dialogs = login_window(self)
        self.sign_up_btn_dialogs.append(sign_up_btn_dialogs)
        sign_up_btn_dialogs.show()

    def back_btn_clicked(self):
        self.close()
        back_btn_dialogs = login_window(self)
        self.back_btn_dialogs.append(back_btn_dialogs)
        back_btn_dialogs.show()


# 멀티 소켓 통신 테스트
class multi_thread(QMainWindow):
    def __init__(self, parent=None):
        super(multi_thread, self).__init__(parent)

        self.s = server.ServerSocket(self)

        self.ip_label = QLabel(self)
        self.ip_label.setText("Server IP")
        ip_label_font = QtGui.QFont()
        ip_label_font.setPointSize(8)
        ip_label_font.setFamily("서울남산 장체M")
        self.ip_label.setFont(ip_label_font)
        self.ip_label.setGeometry(QtCore.QRect(320, 230, 200, 50))

        # a = socket.gethostbyname(socket.gethostbyname())

        self.serverIP_txt = QLineEdit(self)
        self.serverIP_txt.setText(socket.gethostbyname(socket.gethostname()))
        serverIP_txt_font = QtGui.QFont()
        serverIP_txt_font.setPointSize(10)
        serverIP_txt_font.setFamily("서울남산 장체M")
        self.serverIP_txt.setFont(serverIP_txt_font)
        self.serverIP_txt.setGeometry(QtCore.QRect(400, 240, 120, 30))

        self.port_label = QLabel(self)
        self.port_label.setText("Server Port")
        port_label_font = QtGui.QFont()
        port_label_font.setPointSize(8)
        port_label_font.setFamily("서울남산 장체M")
        self.port_label.setFont(port_label_font)
        self.port_label.setGeometry(QtCore.QRect(550, 230, 200, 50))

        self.serverPORT_txt = QLineEdit(self)
        self.serverPORT_txt.setText(str(multi_port))
        serverPORT_txt_font = QtGui.QFont()
        serverPORT_txt_font.setPointSize(10)
        serverPORT_txt_font.setFamily("서울남산 장체M")
        self.serverPORT_txt.setFont(serverPORT_txt_font)
        self.serverPORT_txt.setGeometry(QtCore.QRect(650, 240, 120, 30))

        self.server_start = QPushButton(self)
        self.server_start.setText("서버 실행")
        self.server_start.setCheckable(True)
        server_start_font = QtGui.QFont()
        server_start_font.setPointSize(10)
        server_start_font.setFamily("서울남산 장체M")
        self.server_start.setFont(server_start_font)
        self.server_start.setGeometry(QtCore.QRect(790, 240, 100, 30))
        self.server_start.clicked.connect(self.server_start_clicked)
        self.server_start.setStyleSheet('color:white; background:#0a326f')

        self.ip_info = QTableWidget(self)
        self.ip_info.setColumnCount(2)
        self.ip_info.setRowCount(5)
        self.ip_info.setGeometry(QtCore.QRect(320, 300, 280, 300))
        self.ip_info.setHorizontalHeaderItem(0, QTableWidgetItem('ip'))
        self.ip_info.setHorizontalHeaderItem(1, QTableWidgetItem('port'))

        self.recv_msg_label = QLabel(self)
        self.recv_msg_label.setText("받은 메세지")
        recv_msg_label_font = QtGui.QFont()
        recv_msg_label_font.setPointSize(10)
        recv_msg_label_font.setFamily("서울남산 장체M")
        self.recv_msg_label.setFont(recv_msg_label_font)
        self.recv_msg_label.setGeometry(QtCore.QRect(630, 285, 100, 50))

        self.msg_box = QTextBrowser(self)
        self.msg_box.setGeometry(QtCore.QRect(630, 330, 260, 180))

        self.send_msg_label = QLabel(self)
        self.send_msg_label.setText("보낼 메세지")
        send_msg_label_font = QtGui.QFont()
        send_msg_label_font.setPointSize(10)
        send_msg_label_font.setFamily("서울남산 장체M")
        self.send_msg_label.setFont(send_msg_label_font)
        self.send_msg_label.setGeometry(QtCore.QRect(630, 501, 100, 50))

        self.send_msg_txt = QLineEdit(self)
        self.send_msg_txt.setText("")
        send_msg_txt_font = QtGui.QFont()
        send_msg_txt_font.setPointSize(8)
        send_msg_txt_font.setFamily("서울남산 장체M")
        self.send_msg_txt.setFont(send_msg_txt_font)
        self.send_msg_txt.setGeometry(QtCore.QRect(630, 540, 260, 25))

        self.send_msg_btn = QPushButton(self)
        self.send_msg_btn.setText("보내기")
        send_msg_btn_font = QtGui.QFont()
        send_msg_btn_font.setPointSize(10)
        send_msg_btn_font.setFamily("서울남산 장체M")
        self.send_msg_btn.setFont(send_msg_btn_font)
        self.send_msg_btn.setGeometry(QtCore.QRect(630, 570, 130, 30))
        self.send_msg_btn.setStyleSheet('color:white; background:#0a326f')

        self.clear_msg = QPushButton(self)
        self.clear_msg.setText("채팅창 지움")
        clear_msg_font = QtGui.QFont()
        clear_msg_font.setPointSize(10)
        clear_msg_font.setFamily("서울남산 장체M")
        self.clear_msg.setFont(clear_msg_font)
        self.clear_msg.setGeometry(QtCore.QRect(770, 570, 120, 30))
        self.clear_msg.setStyleSheet('color:white; background:#0a326f')

        self.main = QPushButton(self)
        self.main.setText("스마트 팩토리로 이동")
        main_font = QtGui.QFont()
        main_font.setPointSize(13)
        main_font.setFamily("서울남산 장체M")
        self.main.setFont(main_font)
        self.main.setGeometry(QtCore.QRect(450, 630, 300, 50))
        self.main.clicked.connect(self.main_btn_clicked)
        self.main_btn_dialogs = list()
        self.main.setToolTip('스마트 팩토리 화면으로 이동한다.')
        self.main.setStyleSheet('color:white; background:#0a326f')

        # print(manager_menu_stockmenu.li_num)
        # self.setStyleSheet('color:white')

        self.logo = QLabel(self)
        self.logo.setGeometry(QtCore.QRect(-50, 30, 500, 100))
        icon = QPixmap("logo500.png")
        self.logo.setPixmap(QPixmap(icon))

        olmage = QImage("./back.JPG")
        slmage = olmage.scaled(QSize(1200, 800))
        palette = QPalette()
        palette.setBrush(10, QBrush(slmage))
        self.setPalette(palette)

        self.setGeometry(150, 100, 1200, 800)
        self.setWindowTitle('멀티 서버')
        self.show()

    def server_start_clicked(self, state):
        if state:
            ip = self.serverIP_txt.text()
            port = self.serverPORT_txt.text()

            if self.s.start(ip, int(port)):
                self.server_start.setText('서버 종료')
        else:
            self.s.stop()
            self.msg_box.clear()
            self.server_start.setText('서버 실행')
        # print(self.serverIP_txt.text())

    def updateClient(self):
        self.ip_info.clearContents()
        i = 0
        for ip in self.s.ip:
            self.ip_info.setItem(i, 0, QTableWidgetItem(ip[0]))
            self.ip_info.setItem(i, 1, QTableWidgetItem(str(ip[1])))
            i += 1

    def updateMsg(self, msg):
        self.msg.addItem(QListWidgetItem(msg))
        self.msg.setCurrentRow(self.msg.count() - 1)

    def sendMsg(self):
        if not self.s.bListen:
            self.send_msg_txt.clear()
            return
        sendmsg = self.send_msg_txt.text()
        self.updateMsg(sendmsg)
        print(sendmsg)
        self.s.send(sendmsg)
        self.sendmsg.clear()

    def clearMsg(self):
        self.msg_box.clear()

    def closeEvent(self, e):
        self.s.stop()

    def main_btn_clicked(self):
        self.close()
        main_btn_dialogs = First()
        self.main_btn_dialogs.append(main_btn_dialogs)
        main_btn_dialogs.show()


def main():
    app = QApplication(sys.argv)
    main1 = login_window()
    main1.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()