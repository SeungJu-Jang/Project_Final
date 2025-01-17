#!/usr/bin/env python
# -*- coding: utf-8 -*-
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
import server
import time
import threading
import socketserver
from matplotlib.backends.backend_template import FigureCanvas
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

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
HOST = '192.168.0.19'
USER = 'root'
PASSWORD = '1234'
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
        self.mainlabel_txt.setGeometry(QtCore.QRect(240, 60, 341, 41))

        self.staff_info_btn = QPushButton(self)
        self.staff_info_btn.setText('상품 정보')
        staff_info_font = QtGui.QFont()
        staff_info_font.setPointSize(20)
        staff_info_font.setFamily("서울남산 장체M")
        self.staff_info_btn.setFont(staff_info_font)
        self.staff_info_btn.setGeometry(QtCore.QRect(130, 210, 150, 150))
        self.staff_info_btn.clicked.connect(self.staff_info_btn_clicked)
        self.staff_info_btn_dialogs = list()

        self.staff_stock_btn = QPushButton(self)
        self.staff_stock_btn.setText('재고 관리')
        staff_stock_font = QtGui.QFont()
        staff_stock_font.setPointSize(18)
        staff_stock_font.setFamily("서울남산 장체M")
        self.staff_stock_btn.setFont(staff_stock_font)
        self.staff_stock_btn.setGeometry(QtCore.QRect(330, 210, 150, 150))
        self.staff_stock_btn.clicked.connect(self.staff_stock_btn_clicked)
        self.staff_stock_btn_dialogs = list()

        self.logout_btn = QPushButton(self)
        self.logout_btn.setText('로그아웃')
        logout_btn_font = QtGui.QFont()
        logout_btn_font.setPointSize(9)
        logout_btn_font.setFamily("서울남산 장체M")
        self.logout_btn.setFont(logout_btn_font)
        self.logout_btn.setGeometry(QtCore.QRect(500, 30, 70, 30))
        self.logout_btn.clicked.connect(self.logout_btn_clicked)
        self.logout_btn_dialogs = list()

        self.setGeometry(150, 100, 1200, 800)
        self.setWindowTitle('직원 메뉴')
        self.show()

    def staff_info_btn_clicked(self):
        self.close()
        staff_info_btn_dialogs = staff_info_menu(self)
        self.staff_info_btn_dialogs.append(staff_info_btn_dialogs)
        staff_info_btn_dialogs.show()

    def staff_stock_btn_clicked(self):
        self.close()
        staff_stock_btn_dialogs = staff_stock_menu(self)
        self.staff_info_btn_dialogs.append(staff_stock_btn_dialogs)
        staff_stock_btn_dialogs.show()

    def logout_btn_clicked(self):
        self.close()
        logout_btn_dialogs = First(self)
        self.logout_btn_dialogs.append(logout_btn_dialogs)
        logout_btn_dialogs.show()


# 직원 메뉴 - 상품 정보
class staff_info_menu(QMainWindow):
    def __init__(self, parent=None):
        super(staff_info_menu, self).__init__(parent)

        self.mainlabel_txt = QLabel(self)
        self.mainlabel_txt.setText("상품 정보 확인")
        mainlabel_txt_font = QtGui.QFont()
        mainlabel_txt_font.setPointSize(15)
        mainlabel_txt_font.setFamily("서울남산 장체M")
        self.mainlabel_txt.setFont(mainlabel_txt_font)
        self.mainlabel_txt.setGeometry(QtCore.QRect(220, 50, 341, 41))

        self.namelabel = QLabel(self)
        self.namelabel.setText("· 상품 이름 :")
        namelabel_font = QtGui.QFont()
        namelabel_font.setPointSize(10)
        namelabel_font.setFamily("서울남산 장체M")
        self.namelabel.setFont(namelabel_font)
        self.namelabel.setGeometry(QtCore.QRect(100, 140, 341, 41))

        self.codelabel = QLabel(self)
        self.codelabel.setText("· 상품 코드 :")
        codelabel_font = QtGui.QFont()
        codelabel_font.setPointSize(10)
        codelabel_font.setFamily("서울남산 장체M")
        self.codelabel.setFont(codelabel_font)
        self.codelabel.setGeometry(QtCore.QRect(100, 200, 341, 41))

        self.pricelabel = QLabel(self)
        self.pricelabel.setText("· 상품 단가 :")
        pricelabel_font = QtGui.QFont()
        pricelabel_font.setPointSize(10)
        pricelabel_font.setFamily("서울남산 장체M")
        self.pricelabel.setFont(pricelabel_font)
        self.pricelabel.setGeometry(QtCore.QRect(100, 260, 341, 41))

        self.back_btn = QPushButton(self)
        self.back_btn.setGeometry(QtCore.QRect(0, 0, 80, 52))
        self.back_btn.setText("뒤로가기")
        back_btn_font = QtGui.QFont()
        back_btn_font.setPointSize(10)
        back_btn_font.setFamily("서울남산 장체M")
        self.back_btn.setFont(back_btn_font)
        self.back_btn.clicked.connect(self.back_btn_clicked)
        self.back_btn_dialogs = list()

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
        self.mainlabel_txt.setGeometry(QtCore.QRect(220, 50, 341, 41))

        # 테이블 설정
        self.stock_table = QTableWidget(self)
        self.stock_table.setColumnCount(7)
        self.stock_table.setRowCount(len(li_num))
        self.stock_table.setGeometry(QtCore.QRect(50, 120, 500, 250))
        self.stock_table.setHorizontalHeaderLabels([
            "상품 번호", "브랜드", "종류", "모델명", "가격", "재고량", "출하량"])
        # self.stock_table.setItem(0, 0, QTableWidgetItem(" ༼ ༎ຶ ෴ ༎ຶ༽ "))
        # self.stock_table.setItem(0, 1, QTableWidgetItem(" ༼;´༎ຶ ۝༎ຶ`༽ "))
        # self.stock_table.setItem(0, 2, QTableWidgetItem(" ༽΄◞ิ౪◟ิ‵༼ "))
        # self.stock_table.setItem(0, 3, QTableWidgetItem(" ⎛⎝⎛° ͜ʖ°⎞⎠⎞ "))
        # self.stock_table.setItem(1, 0, QTableWidgetItem(" ξ(｡◕ˇ◊ˇ◕｡)ξ "))
        # self.stock_table.setItem(1, 1, QTableWidgetItem("  (๑¯ਊ¯)σ "))
        # self.stock_table.setItem(1, 2, QTableWidgetItem(" (っ˘ڡ˘ς) "))
        # self.stock_table.setItem(1, 3, QTableWidgetItem(" ( ≖ଳ≖) "))
        # self.stock_table.setItem(2, 0, QTableWidgetItem(" (´ε｀ ʃƪ)♡ "))
        # self.stock_table.setItem(2, 1, QTableWidgetItem(" (ʃƪ ˘ ³˘) "))

        pro_len = len(li_num)
        # 테이블위젯 - 데이터베이스 연동
        for x in range(pro_len):
            for i in range(0, 7):
                li = [x[i] for x in data_num]
                self.stock_table.setItem(x, i, QTableWidgetItem(li[x]))

        self.stock_add_btn = QPushButton(self)
        self.stock_add_btn.setGeometry(QtCore.QRect(50, 400, 130, 50))
        self.stock_add_btn.setText("상품 추가")
        stock_add_btn_font = QtGui.QFont()
        stock_add_btn_font.setPointSize(10)
        stock_add_btn_font.setFamily("서울남산 장체M")
        self.stock_add_btn.setFont(stock_add_btn_font)
        self.stock_add_btn.clicked.connect(self.stock_add_btn_clicked)
        self.stock_add_btn_dialogs = list()

        self.stock_edit_btn = QPushButton(self)
        self.stock_edit_btn.setGeometry(QtCore.QRect(230, 400, 130, 50))
        self.stock_edit_btn.setText("재고 수정")
        stock_edit_btn_font = QtGui.QFont()
        stock_edit_btn_font.setPointSize(10)
        stock_edit_btn_font.setFamily("서울남산 장체M")
        self.stock_edit_btn.setFont(stock_edit_btn_font)
        self.stock_edit_btn.clicked.connect(self.stock_edit_btn_clicked)
        self.stock_edit_btn_dialogs = list()

        self.stock_delete_btn = QPushButton(self)
        self.stock_delete_btn.setGeometry(QtCore.QRect(420, 400, 130, 50))
        self.stock_delete_btn.setText("상품 삭제")
        stock_delete_font = QtGui.QFont()
        stock_delete_font.setPointSize(10)
        stock_delete_font.setFamily("서울남산 장체M")
        self.stock_delete_btn.setFont(stock_delete_font)
        self.stock_delete_btn.clicked.connect(self.stock_delete_btn_clicked)
        self.stock_delete_btn_dialogs = list()

        self.back_btn = QPushButton(self)
        self.back_btn.setGeometry(QtCore.QRect(0, 0, 80, 52))
        self.back_btn.setText("뒤로가기")
        back_btn_font = QtGui.QFont()
        back_btn_font.setPointSize(10)
        back_btn_font.setFamily("서울남산 장체M")
        self.back_btn.setFont(back_btn_font)
        self.back_btn.clicked.connect(self.back_btn_clicked)
        self.back_btn_dialogs = list()

        # 테이블 수정 금지 모드
        self.stock_table.setEditTriggers(QAbstractItemView.NoEditTriggers)

        self.setGeometry(150, 100, 1200, 800)
        self.setWindowTitle('[직원 메뉴] 재고 관리')
        self.show()

    def stock_add_btn_clicked(self):
        self.close()
        stock_add_btn_dialogs = staff_stock_add(self)
        self.stock_add_btn_dialogs.append(stock_add_btn_dialogs)
        stock_add_btn_dialogs.show()

        print(self.stock_table.item(1, 1))

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
        self.mainlabel_txt.setGeometry(QtCore.QRect(250, 50, 341, 41))

        self.stock_add_alarm_btn = QPushButton(self)
        self.stock_add_alarm_btn.setGeometry(QtCore.QRect(230, 400, 130, 50))
        self.stock_add_alarm_btn.setText("저장")
        stock_add_alarm_btn_font = QtGui.QFont()
        stock_add_alarm_btn_font.setPointSize(10)
        stock_add_alarm_btn_font.setFamily("서울남산 장체M")
        self.stock_add_alarm_btn.setFont(stock_add_alarm_btn_font)
        self.stock_add_alarm_btn.clicked.connect(self.staff_stock_add_alarm_btn_clicked)
        self.stock_add_alarm_btn_dialogs = list()

        self.setGeometry(150, 100, 1200, 800)
        self.setWindowTitle('[직원 메뉴] 재고 관리 - 상품 추가')
        self.show()

    def staff_stock_add_alarm_btn_clicked(self):
        self.close()
        stock_add_alarm_btn_dialogs = staff_stock_menu(self)
        self.stock_add_alarm_btn_dialogs.append(stock_add_alarm_btn_dialogs)
        stock_add_alarm_btn_dialogs.show()


# 직원 메뉴 - 재고 관리 - 재고 수정 화면
class staff_stock_edit(QMainWindow):
    def __init__(self, parent=None):
        super(staff_stock_edit, self).__init__(parent)

        self.mainlabel_txt = QLabel(self)
        self.mainlabel_txt.setText("재고 수정")
        mainlabel_txt_font = QtGui.QFont()
        mainlabel_txt_font.setPointSize(15)
        mainlabel_txt_font.setFamily("서울남산 장체M")
        self.mainlabel_txt.setFont(mainlabel_txt_font)
        self.mainlabel_txt.setGeometry(QtCore.QRect(250, 50, 341, 41))

        self.stock_add_alarm_btn = QPushButton(self)
        self.stock_add_alarm_btn.setGeometry(QtCore.QRect(230, 400, 130, 50))
        self.stock_add_alarm_btn.setText("저장")
        stock_add_alarm_btn_font = QtGui.QFont()
        stock_add_alarm_btn_font.setPointSize(10)
        stock_add_alarm_btn_font.setFamily("서울남산 장체M")
        self.stock_add_alarm_btn.setFont(stock_add_alarm_btn_font)
        self.stock_add_alarm_btn.clicked.connect(self.staff_stock_add_alarm_btn_clicked)
        self.stock_add_alarm_btn_dialogs = list()

        self.setGeometry(150, 100, 1200, 800)
        self.setWindowTitle('[직원 메뉴] 재고 관리 - 재고 수정')
        self.show()

    def staff_stock_add_alarm_btn_clicked(self):
        self.close()
        stock_add_alarm_btn_dialogs = staff_stock_menu(self)
        self.stock_add_alarm_btn_dialogs.append(stock_add_alarm_btn_dialogs)
        stock_add_alarm_btn_dialogs.show()


# 직원 메뉴 - 재고 관리 - 상품 삭제 화면
class staff_stock_delete(QMainWindow):
    def __init__(self, parent=None):
        super(staff_stock_delete, self).__init__(parent)

        self.mainlabel_txt = QLabel(self)
        self.mainlabel_txt.setText("상품 삭제")
        mainlabel_txt_font = QtGui.QFont()
        mainlabel_txt_font.setPointSize(15)
        mainlabel_txt_font.setFamily("서울남산 장체M")
        self.mainlabel_txt.setFont(mainlabel_txt_font)
        self.mainlabel_txt.setGeometry(QtCore.QRect(250, 50, 341, 41))

        self.stock_add_alarm_btn = QPushButton(self)
        self.stock_add_alarm_btn.setGeometry(QtCore.QRect(230, 400, 130, 50))
        self.stock_add_alarm_btn.setText("저장")
        stock_add_alarm_btn_font = QtGui.QFont()
        stock_add_alarm_btn_font.setPointSize(10)
        stock_add_alarm_btn_font.setFamily("서울남산 장체M")
        self.stock_add_alarm_btn.setFont(stock_add_alarm_btn_font)
        self.stock_add_alarm_btn.clicked.connect(self.staff_stock_add_alarm_btn_clicked)
        self.stock_add_alarm_btn_dialogs = list()

        self.setGeometry(150, 100, 1200, 800)
        self.setWindowTitle('[직원 메뉴] 재고 관리 - 상품 삭제')
        self.show()

    def staff_stock_add_alarm_btn_clicked(self):
        self.close()
        stock_add_alarm_btn_dialogs = staff_stock_menu(self)
        self.stock_add_alarm_btn_dialogs.append(stock_add_alarm_btn_dialogs)
        stock_add_alarm_btn_dialogs.show()


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
        self.mainlabel_txt.setGeometry(QtCore.QRect(200, 60, 341, 41))

        self.info_btn = QPushButton(self)
        self.info_btn.setText('상품 정보')
        info_btn_font = QtGui.QFont()
        info_btn_font.setPointSize(20)
        info_btn_font.setFamily("서울남산 장체M")
        self.info_btn.setFont(info_btn_font)
        self.info_btn.setGeometry(QtCore.QRect(30, 150, 150, 150))
        self.info_btn_dialogs = list()

        self.sales_btn = QPushButton(self)
        self.sales_btn.setText('매출 확인')
        sales_btn_font = QtGui.QFont()
        sales_btn_font.setPointSize(20)
        sales_btn_font.setFamily("서울남산 장체M")
        self.sales_btn.setFont(sales_btn_font)
        self.sales_btn.setGeometry(QtCore.QRect(30, 330, 150, 150))
        self.sales_btn_dialogs = list()

        self.control_btn = QPushButton(self)
        self.control_btn.setText('공장 제어')
        control_btn_font = QtGui.QFont()
        control_btn_font.setPointSize(18)
        control_btn_font.setFamily("서울남산 장체M")
        self.control_btn.setFont(control_btn_font)
        self.control_btn.setGeometry(QtCore.QRect(230, 150, 150, 150))
        self.control_btn_dialogs = list()

        self.manager_btn = QPushButton(self)
        self.manager_btn.setText('직원 관리')
        manager_btn_font = QtGui.QFont()
        manager_btn_font.setPointSize(18)
        manager_btn_font.setFamily("서울남산 장체M")
        self.manager_btn.setFont(manager_btn_font)
        self.manager_btn.setGeometry(QtCore.QRect(230, 330, 150, 150))
        self.manager_btn_dialogs = list()

        self.stock_btn = QPushButton(self)
        self.stock_btn.setText('재고 관리')
        stock_btn_font = QtGui.QFont()
        stock_btn_font.setPointSize(18)
        stock_btn_font.setFamily("서울남산 장체M")
        self.stock_btn.setFont(stock_btn_font)
        self.stock_btn.setGeometry(QtCore.QRect(430, 150, 150, 150))
        self.stock_btn_dialogs = list()

        self.logout_btn = QPushButton(self)
        self.logout_btn.setText('로그아웃')
        logout_btn_font = QtGui.QFont()
        logout_btn_font.setPointSize(9)
        logout_btn_font.setFamily("서울남산 장체M")
        self.logout_btn.setFont(logout_btn_font)
        self.logout_btn.setGeometry(QtCore.QRect(500, 30, 70, 30))
        self.logout_btn_dialogs = list()

        self.info_btn.clicked.connect(self.info_btn_clicked)
        self.control_btn.clicked.connect(self.control_btn_clicked)
        self.stock_btn.clicked.connect(self.stock_btn_clicked)
        self.sales_btn.clicked.connect(self.sales_btn_clicked)
        self.manager_btn.clicked.connect(self.management_btn_clicked)
        self.logout_btn.clicked.connect(self.logout_btn_clicked)

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
        logout_btn_dialogs = First(self)
        self.logout_btn_dialogs.append(logout_btn_dialogs)
        logout_btn_dialogs.show()


# 관리자 메뉴 - 상품 정보 메뉴
class manager_menu_infomenu(QMainWindow):
    def __init__(self, parent=None):
        super(manager_menu_infomenu, self).__init__(parent)

        self.mainlabel_txt = QLabel(self)
        self.mainlabel_txt.setText("상품 정보 확인")
        mainlabel_txt_font = QtGui.QFont()
        mainlabel_txt_font.setPointSize(15)
        mainlabel_txt_font.setFamily("서울남산 장체M")
        self.mainlabel_txt.setFont(mainlabel_txt_font)
        self.mainlabel_txt.setGeometry(QtCore.QRect(220, 50, 341, 41))

        self.namelabel = QLabel(self)
        self.namelabel.setText("· 상품 이름 :")
        namelabel_font = QtGui.QFont()
        namelabel_font.setPointSize(10)
        namelabel_font.setFamily("서울남산 장체M")
        self.namelabel.setFont(namelabel_font)
        self.namelabel.setGeometry(QtCore.QRect(100, 140, 341, 41))

        self.codelabel = QLabel(self)
        self.codelabel.setText("· 상품 코드 :")
        codelabel_font = QtGui.QFont()
        codelabel_font.setPointSize(10)
        codelabel_font.setFamily("서울남산 장체M")
        self.codelabel.setFont(codelabel_font)
        self.codelabel.setGeometry(QtCore.QRect(100, 200, 341, 41))

        self.pricelabel = QLabel(self)
        self.pricelabel.setText("· 상품 단가 :")
        pricelabel_font = QtGui.QFont()
        pricelabel_font.setPointSize(10)
        pricelabel_font.setFamily("서울남산 장체M")
        self.pricelabel.setFont(pricelabel_font)
        self.pricelabel.setGeometry(QtCore.QRect(100, 260, 341, 41))

        self.back_btn = QPushButton(self)
        self.back_btn.setGeometry(QtCore.QRect(0, 0, 80, 52))
        self.back_btn.setText("뒤로가기")
        back_btn_font = QtGui.QFont()
        back_btn_font.setPointSize(10)
        back_btn_font.setFamily("서울남산 장체M")
        self.back_btn.setFont(back_btn_font)
        self.back_btn.clicked.connect(self.back_btn_clicked)
        self.back_btn_dialogs = list()

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
        self.mainlabel_txt.setGeometry(QtCore.QRect(220, 50, 341, 41))

        self.back_btn = QPushButton(self)
        self.back_btn.setGeometry(QtCore.QRect(0, 0, 80, 52))
        self.back_btn.setText("뒤로가기")
        back_btn_font = QtGui.QFont()
        back_btn_font.setPointSize(10)
        back_btn_font.setFamily("서울남산 장체M")
        self.back_btn.setFont(back_btn_font)
        self.back_btn.clicked.connect(self.back_btn_clicked)
        self.back_btn_dialogs = list()

        self.motorON_btn = QPushButton(self)
        self.motorON_btn.setGeometry(QtCore.QRect(70, 200, 180, 180))
        self.motorON_btn.setText("ON")
        motorON_btn_font = QtGui.QFont()
        motorON_btn_font.setPointSize(20)
        motorON_btn_font.setFamily("서울남산 장체M")
        self.motorON_btn.setFont(motorON_btn_font)
        self.motorON_btn.clicked.connect(self.motorON_btn_clicked)
        # self.motorON_btn_dialogs = list()

        self.motorOFF_btn = QPushButton(self)
        self.motorOFF_btn.setGeometry(QtCore.QRect(350, 200, 180, 180))
        self.motorOFF_btn.setText("OFF")
        motorOFF_btn_font = QtGui.QFont()
        motorOFF_btn_font.setPointSize(20)
        motorOFF_btn_font.setFamily("서울남산 장체M")
        self.motorOFF_btn.setFont(motorOFF_btn_font)
        self.motorOFF_btn.clicked.connect(self.motorOFF_btn_clicked)
        # self.motorOFF_btn_dialogs = list()

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
        self.mainlabel_txt.setGeometry(QtCore.QRect(220, 50, 341, 41))

        # 테이블 설정
        self.stock_table = QTableWidget(self)
        self.stock_table.setColumnCount(6)
        self.stock_table.setRowCount(len(li_num))
        self.stock_table.setGeometry(QtCore.QRect(50, 120, 1000, 250))
        self.stock_table.setHorizontalHeaderLabels(["브랜드", "종류", "모델명", "가격", "재고량", "출하량"])
        # self.stock_table.setItem(0, 0, QTableWidgetItem(" ༼ ༎ຶ ෴ ༎ຶ༽ "))
        # self.stock_table.setItem(0, 1, QTableWidgetItem(" ༼;´༎ຶ ۝༎ຶ`༽ "))
        # self.stock_table.setItem(0, 2, QTableWidgetItem(" ༽΄◞ิ౪◟ิ‵༼ "))
        # self.stock_table.setItem(0, 3, QTableWidgetItem(" ⎛⎝⎛° ͜ʖ°⎞⎠⎞ "))
        # self.stock_table.setItem(1, 0, QTableWidgetItem(" ξ(｡◕ˇ◊ˇ◕｡)ξ "))
        # self.stock_table.setItem(1, 1, QTableWidgetItem("  (๑¯ਊ¯)σ "))
        # self.stock_table.setItem(1, 2, QTableWidgetItem(" (っ˘ڡ˘ς) "))
        # self.stock_table.setItem(1, 3, QTableWidgetItem(" ( ≖ଳ≖) "))
        # self.stock_table.setItem(2, 0, QTableWidgetItem(" (´ε｀ ʃƪ)♡ "))
        # self.stock_table.setItem(2, 1, QTableWidgetItem(" (ʃƪ ˘ ³˘) "))

        pro_len = len(li_num)
        # 테이블위젯 - 데이터베이스 연동
        for x in range(pro_len):
            for i in range(0, 6):
                li = [x[i+1] for x in data_num]
                self.stock_table.setItem(x, i, QTableWidgetItem(li[x]))

        for a in range(pro_len):
            haha = [x[a] for x in data_num]
            print(haha)

        self.stock_add_btn = QPushButton(self)
        self.stock_add_btn.setGeometry(QtCore.QRect(50, 400, 130, 50))
        self.stock_add_btn.setText("상품 추가")
        stock_add_btn_font = QtGui.QFont()
        stock_add_btn_font.setPointSize(10)
        stock_add_btn_font.setFamily("서울남산 장체M")
        self.stock_add_btn.setFont(stock_add_btn_font)
        self.stock_add_btn.clicked.connect(self.stock_add_btn_clicked)
        self.stock_add_btn_dialogs = list()

        self.stock_edit_btn = QPushButton(self)
        self.stock_edit_btn.setGeometry(QtCore.QRect(230, 400, 130, 50))
        self.stock_edit_btn.setText("재고 수정")
        stock_edit_btn_font = QtGui.QFont()
        stock_edit_btn_font.setPointSize(10)
        stock_edit_btn_font.setFamily("서울남산 장체M")
        self.stock_edit_btn.setFont(stock_edit_btn_font)
        self.stock_edit_btn.clicked.connect(self.stock_edit_btn_clicked)
        self.stock_edit_btn_dialogs = list()

        self.stock_delete_btn = QPushButton(self)
        self.stock_delete_btn.setGeometry(QtCore.QRect(420, 400, 130, 50))
        self.stock_delete_btn.setText("상품 삭제")
        stock_delete_font = QtGui.QFont()
        stock_delete_font.setPointSize(10)
        stock_delete_font.setFamily("서울남산 장체M")
        self.stock_delete_btn.setFont(stock_delete_font)
        self.stock_delete_btn.clicked.connect(self.stock_delete_btn_clicked)
        self.stock_delete_btn_dialogs = list()

        self.back_btn = QPushButton(self)
        self.back_btn.setGeometry(QtCore.QRect(0, 0, 80, 52))
        self.back_btn.setText("뒤로가기")
        back_btn_font = QtGui.QFont()
        back_btn_font.setPointSize(10)
        back_btn_font.setFamily("서울남산 장체M")
        self.back_btn.setFont(back_btn_font)
        self.back_btn.clicked.connect(self.back_btn_clicked)
        self.back_btn_dialogs = list()

        # 테이블 수정 금지 모드
        self.stock_table.setEditTriggers(QAbstractItemView.NoEditTriggers)

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
        self.mainlabel_txt.setGeometry(QtCore.QRect(240, 50, 350, 40))

        self.brand = QLabel(self)
        self.brand.setText("상품 브랜드 : ")
        brand_font = QtGui.QFont()
        brand_font.setPointSize(10)
        brand_font.setFamily("서울남산 장체M")
        self.brand.setFont(brand_font)
        self.brand.setGeometry(QtCore.QRect(100, 150, 350, 60))

        self.kinds = QLabel(self)
        self.kinds.setText("상품 종류 : ")
        kinds_font = QtGui.QFont()
        kinds_font.setPointSize(10)
        kinds_font.setFamily("서울남산 장체M")
        self.kinds.setFont(kinds_font)
        self.kinds.setGeometry(QtCore.QRect(100, 190, 350, 60))

        self.model_name = QLabel(self)
        self.model_name.setText("상품 모델명 : ")
        model_name_font = QtGui.QFont()
        model_name_font.setPointSize(10)
        model_name_font.setFamily("서울남산 장체M")
        self.model_name.setFont(model_name_font)
        self.model_name.setGeometry(QtCore.QRect(100, 230, 350, 60))

        self.price = QLabel(self)
        self.price.setText("상품 가격 : ")
        price_font = QtGui.QFont()
        price_font.setPointSize(10)
        price_font.setFamily("서울남산 장체M")
        self.price.setFont(price_font)
        self.price.setGeometry(QtCore.QRect(100, 270, 350, 60))

        self.inventory = QLabel(self)
        self.inventory.setText("상품 재고량 : ")
        inventory_font = QtGui.QFont()
        inventory_font.setPointSize(10)
        inventory_font.setFamily("서울남산 장체M")
        self.inventory.setFont(inventory_font)
        self.inventory.setGeometry(QtCore.QRect(100, 310, 350, 60))

        self.brand_txt = QLineEdit(self)
        self.brand_txt.setText("")
        brand_txt_font = QtGui.QFont()
        brand_txt_font.setPointSize(10)
        brand_txt_font.setFamily("서울남산 장체M")
        self.brand_txt.setFont(brand_txt_font)
        self.brand_txt.setGeometry(QtCore.QRect(200, 165, 230, 30))

        self.kinds_txt = QLineEdit(self)
        self.kinds_txt.setText("")
        kinds_txt_font = QtGui.QFont()
        kinds_txt_font.setPointSize(10)
        kinds_txt_font.setFamily("서울남산 장체M")
        self.kinds_txt.setFont(kinds_txt_font)
        self.kinds_txt.setGeometry(QtCore.QRect(200, 205, 230, 30))

        self.model_txt = QLineEdit(self)
        self.model_txt.setText("")
        model_txt_font = QtGui.QFont()
        model_txt_font.setPointSize(10)
        model_txt_font.setFamily("서울남산 장체M")
        self.model_txt.setFont(model_txt_font)
        self.model_txt.setGeometry(QtCore.QRect(200, 245, 230, 30))

        self.price_txt = QLineEdit(self)
        self.price_txt.setText("")
        price_txt_font = QtGui.QFont()
        price_txt_font.setPointSize(10)
        price_txt_font.setFamily("서울남산 장체M")
        self.price_txt.setFont(price_txt_font)
        self.price_txt.setGeometry(QtCore.QRect(200, 285, 230, 30))

        self.inventory_txt = QLineEdit(self)
        self.inventory_txt.setText("")
        inventory_txt_font = QtGui.QFont()
        inventory_txt_font.setPointSize(10)
        inventory_txt_font.setFamily("서울남산 장체M")
        self.inventory_txt.setFont(inventory_txt_font)
        self.inventory_txt.setGeometry(QtCore.QRect(200, 325, 230, 30))

        self.back_btn = QPushButton(self)
        self.back_btn.setGeometry(QtCore.QRect(0, 0, 80, 52))
        self.back_btn.setText("뒤로가기")
        back_btn_font = QtGui.QFont()
        back_btn_font.setPointSize(10)
        back_btn_font.setFamily("서울남산 장체M")
        self.back_btn.setFont(back_btn_font)
        self.back_btn.clicked.connect(self.back_btn_clicked)
        self.back_btn_dialogs = list()

        self.stock_add_alarm_btn = QPushButton(self)
        self.stock_add_alarm_btn.setGeometry(QtCore.QRect(230, 400, 130, 50))
        self.stock_add_alarm_btn.setText("저장")
        stock_add_alarm_btn_font = QtGui.QFont()
        stock_add_alarm_btn_font.setPointSize(10)
        stock_add_alarm_btn_font.setFamily("서울남산 장체M")
        self.stock_add_alarm_btn.setFont(stock_add_alarm_btn_font)
        self.stock_add_alarm_btn.clicked.connect(self.stock_add_alarm_btn_clicked)
        self.stock_add_alarm_btn_dialogs = list()

        self.setGeometry(150, 100, 1200, 800)
        self.setWindowTitle('[관리자 메뉴] 재고 관리 - 상품 추가')
        self.show()

    def stock_add_alarm_btn_clicked(self):
        con = pymysql.connect(host=HOST, user=USER, password=PASSWORD, db=DB, charset='utf8', autocommit=True)
        # cur_num = con.cursor()
        cur_insert = con.cursor()

        sql_num = "SELECT * FROM pro_info;"
        cur_insert.execute("INSERT INTO pro_info(brand, model, codenum, unitprice, inventory) VALUES('%s', '%s', '%s', '%s', '%s')" % (''.join(self.brand_txt.text()), ''.join(self.kinds_txt.text()), ''.join(self.model_txt.text()), ''.join(self.price_txt.text()), ''.join(self.inventory_txt.text())))

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
        self.model_combobox.setGeometry(QtCore.QRect(420, 150, 100, 30))

        self.kinds_combobox = QComboBox(self)
        self.kinds_combobox.setGeometry(QtCore.QRect(260, 150, 100, 30))

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
        self.mainlabel_txt.setGeometry(QtCore.QRect(240, 50, 341, 41))

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
        self.brand.setGeometry(QtCore.QRect(120, 120, 100, 30))

        self.brand_combobox = QComboBox(self)
        self.brand_combobox.addItem('')
        self.brand_combobox.addItems(li_brand)
        self.brand_combobox.activated.connect(self.brand_combo_change)
        self.brand_combobox.setGeometry(QtCore.QRect(100, 150, 100, 30))

        self.kinds = QLabel(self)
        self.kinds.setText("종류")
        kinds_font = QtGui.QFont()
        kinds_font.setPointSize(10)
        kinds_font.setFamily("서울남산 장체M")
        self.kinds.setFont(kinds_font)
        self.kinds.setGeometry(QtCore.QRect(290, 120, 100, 30))


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
        self.model.setGeometry(QtCore.QRect(440, 120, 100, 30))

        #
        self.model = QLabel(self)
        self.model.setText("재고량을")
        model_font = QtGui.QFont()
        model_font.setPointSize(15)
        model_font.setFamily("서울남산 장체M")
        self.model.setFont(model_font)
        self.model.setGeometry(QtCore.QRect(180, 300, 100, 30))

        self.inventory_num_txt = QLineEdit(self)
        self.inventory_num_txt.setText("")
        inventory_num_font = QtGui.QFont()
        inventory_num_font.setPointSize(15)
        inventory_num_font.setFamily("서울남산 장체M")
        self.inventory_num_txt.setFont(inventory_num_font)
        self.inventory_num_txt.setGeometry(QtCore.QRect(290, 300, 55, 30))

        self.model = QLabel(self)
        self.model.setText("개로 변경.")
        mode_font = QtGui.QFont()
        model_font.setPointSize(15)
        model_font.setFamily("서울남산 장체M")
        self.model.setFont(model_font)
        self.model.setGeometry(QtCore.QRect(350, 300, 100, 30))
        #


        self.stock_add_alarm_btn = QPushButton(self)
        self.stock_add_alarm_btn.setGeometry(QtCore.QRect(230, 400, 130, 50))
        self.stock_add_alarm_btn.setText("저장")
        stock_add_alarm_btn_font = QtGui.QFont()
        stock_add_alarm_btn_font.setPointSize(10)
        stock_add_alarm_btn_font.setFamily("서울남산 장체M")
        self.stock_add_alarm_btn.setFont(stock_add_alarm_btn_font)
        self.stock_add_alarm_btn.clicked.connect(self.stock_add_alarm_btn_clicked)
        self.stock_add_alarm_btn_dialogs = list()

        self.back_btn = QPushButton(self)
        self.back_btn.setGeometry(QtCore.QRect(0, 0, 80, 52))
        self.back_btn.setText("뒤로가기")
        back_btn_font = QtGui.QFont()
        back_btn_font.setPointSize(10)
        back_btn_font.setFamily("서울남산 장체M")
        self.back_btn.setFont(back_btn_font)
        self.back_btn.clicked.connect(self.back_btn_clicked)
        self.back_btn_dialogs = list()

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
        self.kinds_combobox.setGeometry(QtCore.QRect(260, 150, 100, 30))

    def kinds_combo_change(self):
        print(self.kinds_combobox.currentText())
        con = pymysql.connect(host=HOST, user=USER, password=PASSWORD, db=DB, charset='utf8', autocommit=True)

        cur_search_model = con.cursor()
        sql_search_model = "SELECT distinct codenum FROM pro_info WHERE model = %s and brand = %s;"
        cur_search_model.execute(sql_search_model, (self.kinds_combobox.currentText(), self.brand_combobox.currentText()))
        data_search_model = cur_search_model.fetchall()
        li_search_model = [x[0] for x in data_search_model]

        self.model_combobox.addItem('')
        self.model_combobox.addItems(li_search_model)
        self.model_combobox.activated.connect(self.model_combo_change)
        self.model_combobox.setGeometry(QtCore.QRect(420, 150, 100, 30))

    def model_combo_change(self):
        print(self.model_combobox.currentText())

    def stock_add_alarm_btn_clicked(self):
        con = pymysql.connect(host=HOST, user=USER, password=PASSWORD, db=DB, charset='utf8', autocommit=True)
        cur = con.cursor()
        sql_up = "UPDATE pro_info SET inventory = %s WHERE brand = %s and model = %s and codenum = %s;"
        cur.execute(sql_up, (self.inventory_num_txt.text(), self.brand_combobox.currentText(), self.kinds_combobox.currentText(), self.model_combobox.currentText()))

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
        self.model_txtB.setGeometry(QtCore.QRect(90, 300, 430, 80))

        self.model_combobox = QComboBox(self)
        self.model_combobox.setGeometry(QtCore.QRect(420, 150, 100, 30))

        self.kinds_combobox = QComboBox(self)
        self.kinds_combobox.setGeometry(QtCore.QRect(260, 150, 100, 30))

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
        self.mainlabel_txt.setGeometry(QtCore.QRect(240, 50, 341, 41))

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
        self.brand.setGeometry(QtCore.QRect(120, 120, 100, 30))

        self.brand_combobox = QComboBox(self)
        self.brand_combobox.addItem('')
        self.brand_combobox.addItems(li_brand)
        self.brand_combobox.activated.connect(self.brand_combo_change)
        self.brand_combobox.setGeometry(QtCore.QRect(100, 150, 100, 30))

        self.kinds = QLabel(self)
        self.kinds.setText("종류")
        kinds_font = QtGui.QFont()
        kinds_font.setPointSize(10)
        kinds_font.setFamily("서울남산 장체M")
        self.kinds.setFont(kinds_font)
        self.kinds.setGeometry(QtCore.QRect(290, 120, 100, 30))

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
        self.model.setGeometry(QtCore.QRect(440, 120, 100, 30))

        #



        #

        self.stock_add_alarm_btn = QPushButton(self)
        self.stock_add_alarm_btn.setGeometry(QtCore.QRect(230, 400, 130, 50))
        self.stock_add_alarm_btn.setText("삭제")
        stock_add_alarm_btn_font = QtGui.QFont()
        stock_add_alarm_btn_font.setPointSize(10)
        stock_add_alarm_btn_font.setFamily("서울남산 장체M")
        self.stock_add_alarm_btn.setFont(stock_add_alarm_btn_font)
        self.stock_add_alarm_btn.clicked.connect(self.stock_add_alarm_btn_clicked)
        self.stock_add_alarm_btn_dialogs = list()

        self.back_btn = QPushButton(self)
        self.back_btn.setGeometry(QtCore.QRect(0, 0, 80, 52))
        self.back_btn.setText("뒤로가기")
        back_btn_font = QtGui.QFont()
        back_btn_font.setPointSize(10)
        back_btn_font.setFamily("서울남산 장체M")
        self.back_btn.setFont(back_btn_font)
        self.back_btn.clicked.connect(self.back_btn_clicked)
        self.back_btn_dialogs = list()

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
        self.kinds_combobox.setGeometry(QtCore.QRect(260, 150, 100, 30))

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
        self.model_combobox.setGeometry(QtCore.QRect(420, 150, 100, 30))

    def model_combo_change(self):
        BRAND = self.brand_combobox.currentText()
        KINDS = self.kinds_combobox.currentText()
        MODEL = self.model_combobox.currentText()


        self.model_txtB.setText('''"''' + BRAND + '''" 의 ''' + KINDS + "'인 [" + MODEL + "]를 삭제하시겠습니까?")
        model_txtB_font = QtGui.QFont()
        model_txtB_font.setPointSize(10)
        model_txtB_font.setFamily("서울남산 장체M")
        self.model_txtB.setFont(model_txtB_font)
        self.model_txtB.setGeometry(QtCore.QRect(90, 300, 430, 80))

    def stock_add_alarm_btn_clicked(self):
        con = pymysql.connect(host=HOST, user=USER, password=PASSWORD, db=DB, charset='utf8', autocommit=True)
        cur = con.cursor()
        sql_del = "DELETE FROM pro_info WHERE brand = %s and model = %s and codenum = %s;"
        cur.execute(sql_del, (self.brand_combobox.currentText(), self.kinds_combobox.currentText(), self.model_combobox.currentText()))

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
class manager_menu_salesmenu(QWidget):
    # def __init__(self, parent=None):
    #     super(manager_menu_salesmenu, self).__init__(parent)
    def __init__(self):
        super().__init__()

        self.initUI()
        self.setLayout(self.layout)
        self.setGeometry(150, 100, 1200, 800)

        # layout = QVBoxLayout()
        # layout.addWidget(self.canvas)
        #
        # cb = QComboBox()
        # cb.addItem('Graph1')
        # cb.addItem('Graph2')
        # cb.activated[str].connect(self.cb_change)
        # layout.addWidget(cb)
        #
        # self.layout = layout
        # self.cb_chang(cb.currentText())
        # self.graph = plt.Figure(self)
        # self.canvas = FigureCanvas(self.graph)

        # self.cb = QComboBox(self)
        # self.cb.addItem('Graph1')
        # self.cb.addItem('Graph2')
        # self.cb.actived[str].connect(self.cb_change)
        # self.cb.setGeometry(50, 400, 300, 30)



        # self.back_btn = QPushButton(self)
        # self.back_btn.setGeometry(QtCore.QRect(0, 0, 80, 52))
        # self.back_btn.setText("뒤로가기")
        # back_btn_font = QtGui.QFont()
        # back_btn_font.setPointSize(10)
        # back_btn_font.setFamily("서울남산 장체M")
        # self.back_btn.setFont(back_btn_font)
        # self.back_btn.clicked.connect(self.back_btn_clicked)
        # self.back_btn_dialogs = list()

        # self.setGeometry(150, 100, 1200, 800)
        # self.setWindowTitle('[관리자 메뉴] 매출 확인')
        # self.show()

        # self.setLayout(self.layout)
        # self.setGeometry(150, 100, 1200, 800)

    # def initUI(self):

        # layout = QVBoxLayout()
        # layout.addWidget(self.canvas)
        #
        # cb = QComboBox()
        # cb.addItem('Graph1')
        # cb.addItem('Graph2')
        # cb.activated[str].connect(self.cb_change)
        # layout.addWidget(cb)
        #
        # self.layout = layout
        # self.cb_chang(cb.currentText())

    # def cb_change(self, text):
    #     if text == 'Graph1':
    #         self.doGraph1()
    #     elif text == 'Graph2':
    #         self.doGraph2()

    def doGraph1(self):
        x = np.arange(0, 10, 0.5)
        y1 = np.sin(x)
        y2 = np.cos(x)
        self.fig.clear()

        ax = self.fig.add_subplot(111)
        ax.plot(x, y1, label="sin(x)")
        ax.plot(x, y2, label="cos(x)", linestyle="--")

        ax.set_xlabel("x")
        ax.set_xlabel("y")
        ax.set_title("sin & cos")
        ax.legend()
        self.canvas.draw()

    def doGraph2(self):
        X = np.arange(-5, 5, 0.25)
        Y = np.arange(-5, 5, 0.25)
        X, Y = np.meshgrid(X, Y)
        Z = X ** 2 + Y ** 2

        self.fig.clear()
        ax = self.fig.gca(projection='3d')
        ax.plot_wireframe(X, Y, Z, color='red')
        self.canvas.draw()

    #     self.back_btn = QPushButton(self)
    #     self.back_btn.setGeometry(QtCore.QRect(0, 0, 80, 52))
    #     self.back_btn.setText("뒤로가기")
    #     back_btn_font = QtGui.QFont()
    #     back_btn_font.setPointSize(10)
    #     back_btn_font.setFamily("서울남산 장체M")
    #     self.back_btn.setFont(back_btn_font)
    #     self.back_btn.clicked.connect(self.back_btn_clicked)
    #     self.back_btn_dialogs = list()
    #
    #     self.setGeometry(150, 100, 1200, 800)
    #     self.setWindowTitle('[관리자 메뉴] 매출 확인')
    #     self.show()
    #
    def back_btn_clicked(self):
        self.close()
        back_btn_dialogs = manager_menu(self)
        self.back_btn_dialogs.append(back_btn_dialogs)
        back_btn_dialogs.show()


# 관리자 메뉴 - 직원 관리 메뉴
class manager_menu_managermenu(QMainWindow):
    def __init__(self, parent=None):
        super(manager_menu_managermenu, self).__init__(parent)

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
        self.mainlabel_txt.setGeometry(QtCore.QRect(200, 40, 341, 41))

        self.namecombobox = QComboBox(self)
        self.namecombobox.addItem("")
        self.namecombobox.addItems(li)
        # self.namecombobox.insertSeparator(4)
        self.namecombobox.activated.connect(self.combo_change)
        self.namecombobox.setGeometry(QtCore.QRect(250, 80, 100, 30))

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
        self.namelabel.setGeometry(QtCore.QRect(300, 140, 100, 100))

        # 데이터베이스 연동 이름 부분
        self.namelabel_txt = QLabel(self)
        self.namelabel_txt.setText("")
        namelabel_txt_font = QtGui.QFont()
        namelabel_txt_font.setPointSize(10)
        namelabel_txt_font.setFamily("서울남산 장체M")
        self.namelabel_txt.setFont(namelabel_txt_font)
        self.namelabel_txt.setGeometry(QtCore.QRect(360, 140, 300, 100))

        self.positionlabel = QLabel(self)
        self.positionlabel.setText("· 직책 : ")
        positionlabel_font = QtGui.QFont()
        positionlabel_font.setPointSize(10)
        positionlabel_font.setFamily("서울남산 장체M")
        self.positionlabel.setFont(positionlabel_font)
        self.positionlabel.setGeometry(QtCore.QRect(300, 180, 100, 100))

        # 데이터베이스 연동 직책 부분
        self.positionlabel_txt = QLabel(self)
        self.positionlabel_txt.setText("")
        positionlabel_txt_font = QtGui.QFont()
        positionlabel_txt_font.setPointSize(10)
        positionlabel_txt_font.setFamily("서울남산 장체M")
        self.positionlabel_txt.setFont(positionlabel_txt_font)
        self.positionlabel_txt.setGeometry(QtCore.QRect(360, 180, 300, 100))

        self.idlabel = QLabel(self)
        self.idlabel.setText("· ID : ")
        idlabel_font = QtGui.QFont()
        idlabel_font.setPointSize(10)
        idlabel_font.setFamily("서울남산 장체M")
        self.idlabel.setFont(idlabel_font)
        self.idlabel.setGeometry(QtCore.QRect(300, 220, 100, 100))

        # 데이터베이스 연동 ID 부분
        self.idlabel_txt = QLabel(self)
        self.idlabel_txt.setText("")
        idlabel_txt_font = QtGui.QFont()
        idlabel_txt_font.setPointSize(10)
        idlabel_txt_font.setFamily("서울남산 장체M")
        self.idlabel_txt.setFont(idlabel_txt_font)
        self.idlabel_txt.setGeometry(QtCore.QRect(350, 220, 300, 100))

        self.birthlabel = QLabel(self)
        self.birthlabel.setText("· 생년월일 : ")
        birthlabel_font = QtGui.QFont()
        birthlabel_font.setPointSize(10)
        birthlabel_font.setFamily("서울남산 장체M")
        self.birthlabel.setFont(birthlabel_font)
        self.birthlabel.setGeometry(QtCore.QRect(300, 260, 100, 100))

        # 데이터베이스 연동 생년월일 부분
        self.birthlabel_txt = QLabel(self)
        self.birthlabel_txt.setText("")
        birthlabel_txt_font = QtGui.QFont()
        birthlabel_txt_font.setPointSize(10)
        birthlabel_txt_font.setFamily("서울남산 장체M")
        self.birthlabel_txt.setFont(birthlabel_txt_font)
        self.birthlabel_txt.setGeometry(QtCore.QRect(390, 260, 300, 100))

        self.emaillabel = QLabel(self)
        self.emaillabel.setText("· E-Mail : ")
        emaillabel_font = QtGui.QFont()
        emaillabel_font.setPointSize(10)
        emaillabel_font.setFamily("서울남산 장체M")
        self.emaillabel.setFont(emaillabel_font)
        self.emaillabel.setGeometry(QtCore.QRect(300, 300, 100, 100))

        # 데이터베이스 연동 이메일 부분
        self.emaillabel_txt = QLabel(self)
        self.emaillabel_txt.setText("")
        emaillabel_txt_font = QtGui.QFont()
        emaillabel_txt_font.setPointSize(10)
        emaillabel_txt_font.setFamily("서울남산 장체M")
        self.emaillabel_txt.setFont(emaillabel_txt_font)
        self.emaillabel_txt.setGeometry(QtCore.QRect(380, 300, 300, 100))

        self.profile = QLabel(self)
        self.profile.setGeometry(QtCore.QRect(60, 175, 175, 175))
        icon = QPixmap("icon1.png")
        self.profile.setPixmap(QPixmap(icon))

        self.back_btn = QPushButton(self)
        self.back_btn.setGeometry(QtCore.QRect(0, 0, 80, 52))
        self.back_btn.setText("뒤로가기")
        back_btn_font = QtGui.QFont()
        back_btn_font.setPointSize(10)
        back_btn_font.setFamily("서울남산 장체M")
        self.back_btn.setFont(back_btn_font)
        self.back_btn.clicked.connect(self.back_btn_clicked)
        self.back_btn_dialogs = list()

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
        self.mainlabel_txt.setGeometry(QtCore.QRect(160, 60, 341, 41))

        self.search_btn = QPushButton(self)
        self.search_btn.setText('직원 확인')
        search_btn_font = QtGui.QFont()
        search_btn_font.setPointSize(20)
        search_btn_font.setFamily("서울남산 장체M")
        self.search_btn.setFont(search_btn_font)
        self.search_btn.setGeometry(QtCore.QRect(30, 210, 150, 150))

        self.edit_btn = QPushButton(self)
        self.edit_btn.setText('직원 정보\n수정')
        edit_btn_font = QtGui.QFont()
        edit_btn_font.setPointSize(18)
        edit_btn_font.setFamily("서울남산 장체M")
        self.edit_btn.setFont(edit_btn_font)
        self.edit_btn.setGeometry(QtCore.QRect(230, 210, 150, 150))

        self.delete_btn = QPushButton(self)
        self.delete_btn.setText('관리자/\n직원\n삭제')
        delete_btn_font = QtGui.QFont()
        delete_btn_font.setPointSize(18)
        delete_btn_font.setFamily("서울남산 장체M")
        self.delete_btn.setFont(delete_btn_font)
        self.delete_btn.setGeometry(QtCore.QRect(430, 210, 150, 150))

        self.logout_btn = QPushButton(self)
        self.logout_btn.setText('로그아웃')
        logout_btn_font = QtGui.QFont()
        logout_btn_font.setPointSize(9)
        logout_btn_font.setFamily("서울남산 장체M")
        self.logout_btn.setFont(logout_btn_font)
        self.logout_btn.setGeometry(QtCore.QRect(500, 30, 70, 30))

        self.search_btn.clicked.connect(self.search_btn_clicked)
        self.search_btn_dialogs = list()

        self.edit_btn.clicked.connect(self.edit_btn_clicked)
        self.edit_btn_dialogs = list()

        self.delete_btn.clicked.connect(self.delete_btn_clicked)
        self.delete_btn_dialogs = list()

        self.logout_btn.clicked.connect(self.logout_btn_clicked)
        self.logout_btn_dialogs = list()

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
        logout_btn_dialogs = First(self)
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
        self.mainlabel_txt.setGeometry(QtCore.QRect(200, 40, 341, 41))

        self.namecombobox = QComboBox(self)
        self.namecombobox.addItem("")
        self.namecombobox.addItems(li)
        # self.namecombobox.insertSeparator(4)
        self.namecombobox.activated.connect(self.combo_change)
        self.namecombobox.setGeometry(QtCore.QRect(250, 80, 100, 30))

        self.namelabel = QLabel(self)
        self.namelabel.setText("· 이름 : ")
        namelabel_font = QtGui.QFont()
        namelabel_font.setPointSize(10)
        namelabel_font.setFamily("서울남산 장체M")
        self.namelabel.setFont(namelabel_font)
        self.namelabel.setGeometry(QtCore.QRect(300, 140, 100, 100))

        # 데이터베이스 연동 이름 부분
        self.namelabel_txt = QLabel(self)
        self.namelabel_txt.setText("")
        namelabel_txt_font = QtGui.QFont()
        namelabel_txt_font.setPointSize(10)
        namelabel_txt_font.setFamily("서울남산 장체M")
        self.namelabel_txt.setFont(namelabel_txt_font)
        self.namelabel_txt.setGeometry(QtCore.QRect(360, 140, 300, 100))

        self.positionlabel = QLabel(self)
        self.positionlabel.setText("· 직책 : ")
        positionlabel_font = QtGui.QFont()
        positionlabel_font.setPointSize(10)
        positionlabel_font.setFamily("서울남산 장체M")
        self.positionlabel.setFont(positionlabel_font)
        self.positionlabel.setGeometry(QtCore.QRect(300, 180, 100, 100))

        # 데이터베이스 연동 직책 부분
        self.positionlabel_txt = QLabel(self)
        self.positionlabel_txt.setText("")
        positionlabel_txt_font = QtGui.QFont()
        positionlabel_txt_font.setPointSize(10)
        positionlabel_txt_font.setFamily("서울남산 장체M")
        self.positionlabel_txt.setFont(positionlabel_txt_font)
        self.positionlabel_txt.setGeometry(QtCore.QRect(360, 180, 300, 100))

        self.idlabel = QLabel(self)
        self.idlabel.setText("· ID : ")
        idlabel_font = QtGui.QFont()
        idlabel_font.setPointSize(10)
        idlabel_font.setFamily("서울남산 장체M")
        self.idlabel.setFont(idlabel_font)
        self.idlabel.setGeometry(QtCore.QRect(300, 220, 100, 100))

        # 데이터베이스 연동 ID 부분
        self.idlabel_txt = QLabel(self)
        self.idlabel_txt.setText("")
        idlabel_txt_font = QtGui.QFont()
        idlabel_txt_font.setPointSize(10)
        idlabel_txt_font.setFamily("서울남산 장체M")
        self.idlabel_txt.setFont(idlabel_txt_font)
        self.idlabel_txt.setGeometry(QtCore.QRect(350, 220, 300, 100))

        self.birthlabel = QLabel(self)
        self.birthlabel.setText("· 생년월일 : ")
        birthlabel_font = QtGui.QFont()
        birthlabel_font.setPointSize(10)
        birthlabel_font.setFamily("서울남산 장체M")
        self.birthlabel.setFont(birthlabel_font)
        self.birthlabel.setGeometry(QtCore.QRect(300, 260, 100, 100))

        # 데이터베이스 연동 생년월일 부분
        self.birthlabel_txt = QLabel(self)
        self.birthlabel_txt.setText("")
        birthlabel_txt_font = QtGui.QFont()
        birthlabel_txt_font.setPointSize(10)
        birthlabel_txt_font.setFamily("서울남산 장체M")
        self.birthlabel_txt.setFont(birthlabel_txt_font)
        self.birthlabel_txt.setGeometry(QtCore.QRect(390, 260, 300, 100))

        self.emaillabel = QLabel(self)
        self.emaillabel.setText("· E-Mail : ")
        emaillabel_font = QtGui.QFont()
        emaillabel_font.setPointSize(10)
        emaillabel_font.setFamily("서울남산 장체M")
        self.emaillabel.setFont(emaillabel_font)
        self.emaillabel.setGeometry(QtCore.QRect(300, 300, 100, 100))

        # 데이터베이스 연동 이메일 부분
        self.emaillabel_txt = QLabel(self)
        self.emaillabel_txt.setText("")
        emaillabel_txt_font = QtGui.QFont()
        emaillabel_txt_font.setPointSize(10)
        emaillabel_txt_font.setFamily("서울남산 장체M")
        self.emaillabel_txt.setFont(emaillabel_txt_font)
        self.emaillabel_txt.setGeometry(QtCore.QRect(380, 300, 300, 100))

        self.profile = QLabel(self)
        self.profile.setGeometry(QtCore.QRect(60, 175, 175, 175))
        icon = QPixmap("icon1.png")
        self.profile.setPixmap(QPixmap(icon))

        self.back_btn = QPushButton(self)
        self.back_btn.setGeometry(QtCore.QRect(0, 0, 80, 52))
        self.back_btn.setText("뒤로가기")
        back_btn_font = QtGui.QFont()
        back_btn_font.setPointSize(10)
        back_btn_font.setFamily("서울남산 장체M")
        self.back_btn.setFont(back_btn_font)
        self.back_btn.clicked.connect(self.back_btn_clicked)
        self.back_btn_dialogs = list()

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
        self.mainlabel_txt.setGeometry(QtCore.QRect(200, 40, 341, 41))

        self.namecombobox = QComboBox(self)
        self.namecombobox.addItem("")
        self.namecombobox.addItems(li)
        # self.namecombobox.insertSeparator(4)
        self.namecombobox.activated.connect(self.combo_change)
        self.namecombobox.setGeometry(QtCore.QRect(250, 80, 100, 30))

        self.namelabel = QLabel(self)
        self.namelabel.setText("· 이름 : ")
        namelabel_font = QtGui.QFont()
        namelabel_font.setPointSize(10)
        namelabel_font.setFamily("서울남산 장체M")
        self.namelabel.setFont(namelabel_font)
        self.namelabel.setGeometry(QtCore.QRect(300, 140, 100, 100))

        # 직원 정보 수정(이름) -> 데이터베이스 연동해야함
        self.namelabel_txt = QLineEdit(self)
        self.namelabel_txt.setText("")
        namelabel_txt_font = QtGui.QFont()
        namelabel_txt_font.setPointSize(10)
        namelabel_txt_font.setFamily("서울남산 장체M")
        self.namelabel_txt.setFont(namelabel_txt_font)
        self.namelabel_txt.setGeometry(QtCore.QRect(360, 175, 100, 30))

        self.positionlabel = QLabel(self)
        self.positionlabel.setText("· 직책 : ")
        positionlabel_font = QtGui.QFont()
        positionlabel_font.setPointSize(10)
        positionlabel_font.setFamily("서울남산 장체M")
        self.positionlabel.setFont(positionlabel_font)
        self.positionlabel.setGeometry(QtCore.QRect(300, 180, 100, 100))

        # 직원 정보 수정(직책) -> 데이터베이스 연동해야함
        self.positionlabel_txt = QComboBox(self)
        self.positionlabel_txt.addItem('')
        self.positionlabel_txt.addItems(["employee", "manager", "super"])
        positionlabel_txt_font = QtGui.QFont()
        positionlabel_txt_font.setPointSize(10)
        positionlabel_txt_font.setFamily("서울남산 장체M")
        self.positionlabel_txt.setFont(positionlabel_txt_font)
        self.positionlabel_txt.setGeometry(QtCore.QRect(360, 215, 120, 30))

        self.idlabel = QLabel(self)
        self.idlabel.setText("· ID : ")
        idlabel_font = QtGui.QFont()
        idlabel_font.setPointSize(10)
        idlabel_font.setFamily("서울남산 장체M")
        self.idlabel.setFont(idlabel_font)
        self.idlabel.setGeometry(QtCore.QRect(300, 220, 100, 100))

        # 직원 정보 수정(ID) -> 데이터베이스 연동해야함
        self.idlabel_txt = QLineEdit(self)
        self.idlabel_txt.setText("")
        idlabel_txt_font = QtGui.QFont()
        idlabel_txt_font.setPointSize(10)
        idlabel_txt_font.setFamily("서울남산 장체M")
        self.idlabel_txt.setFont(idlabel_txt_font)
        self.idlabel_txt.setGeometry(QtCore.QRect(360, 255, 130, 30))

        self.birthlabel = QLabel(self)
        self.birthlabel.setText("· 생년월일 : ")
        birthlabel_font = QtGui.QFont()
        birthlabel_font.setPointSize(10)
        birthlabel_font.setFamily("서울남산 장체M")
        self.birthlabel.setFont(birthlabel_font)
        self.birthlabel.setGeometry(QtCore.QRect(300, 260, 100, 100))

        # 직원 정보 수정(생년월일) -> 데이터베이스 연동해야함
        self.birthlabel_txt = QLineEdit(self)
        self.birthlabel_txt.setText("")
        birthlabel_txt_font = QtGui.QFont()
        birthlabel_txt_font.setPointSize(10)
        birthlabel_txt_font.setFamily("서울남산 장체M")
        self.birthlabel_txt.setFont(birthlabel_txt_font)
        self.birthlabel_txt.setGeometry(QtCore.QRect(390, 295, 120, 30))

        self.emaillabel = QLabel(self)
        self.emaillabel.setText("· E-Mail : ")
        emaillabel_font = QtGui.QFont()
        emaillabel_font.setPointSize(10)
        emaillabel_font.setFamily("서울남산 장체M")
        self.emaillabel.setFont(emaillabel_font)
        self.emaillabel.setGeometry(QtCore.QRect(300, 300, 100, 100))

        # 직원 정보 수정(이메일) -> 데이터베이스 연동해야함
        self.emaillabel_txt = QLineEdit(self)
        self.emaillabel_txt.setText("")
        emaillabel_txt_font = QtGui.QFont()
        emaillabel_txt_font.setPointSize(10)
        emaillabel_txt_font.setFamily("서울남산 장체M")
        self.emaillabel_txt.setFont(emaillabel_txt_font)
        self.emaillabel_txt.setGeometry(QtCore.QRect(380, 335, 200, 30))

        self.profile = QLabel(self)
        self.profile.setGeometry(QtCore.QRect(60, 175, 175, 175))
        icon = QPixmap("icon1.png")
        self.profile.setPixmap(QPixmap(icon))

        self.back_btn = QPushButton(self)
        self.back_btn.setGeometry(QtCore.QRect(0, 0, 80, 52))
        self.back_btn.setText("뒤로가기")
        back_btn_font = QtGui.QFont()
        back_btn_font.setPointSize(10)
        back_btn_font.setFamily("서울남산 장체M")
        self.back_btn.setFont(back_btn_font)
        self.back_btn.clicked.connect(self.back_btn_clicked)
        self.back_btn_dialogs = list()

        self.save_btn = QPushButton(self)
        self.save_btn.setGeometry(QtCore.QRect(250, 400, 100, 50))
        self.save_btn.setText("저장")
        save_btn_font = QtGui.QFont()
        save_btn_font.setPointSize(12)
        save_btn_font.setFamily("서울남산 장체M")
        self.save_btn.setFont(save_btn_font)
        self.save_btn.clicked.connect(self.save_btn_clicked)
        self.save_btn_dialogs = list()

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

                    # print(self.positionlabel_txt.currentText())

        # if self.namecombobox.currentText() == str(li_name[0]):
        #     self.namelabel_txt.setText(str(li_name[0]))
        #     # self.positionlabel_txt.setText(str(li_position[0]))
        #     self.idlabel_txt.setText(str(li_id[0]))
        #     self.birthlabel_txt.setText(str(li_birth[0]))
        #     self.emaillabel_txt.setText(str(li_email[0]))
        #
        #     if li_position[0] == 'employee':
        #         self.positionlabel_txt.setCurrentText("employee")
        #     else:
        #         self.positionlabel_txt.setCurrentText("manager")
        #
        # if self.namecombobox.currentText() == str(li_name[1]):
        #     self.namelabel_txt.setText(li_name[1])
        #     # self.positionlabel_txt.setText(li_position[1])
        #     self.idlabel_txt.setText(li_id[1])
        #     self.birthlabel_txt.setText(li_birth[1])
        #     self.emaillabel_txt.setText(li_email[1])
        #
        #     if li_position[1] == 'employee':
        #         self.positionlabel_txt.setCurrentText("employee")
        #     else:
        #         self.positionlabel_txt.setCurrentText("manager")
        #
        # if self.namecombobox.currentText() == str(li_name[2]):
        #     self.namelabel_txt.setText(li_name[2])
        #     #self.positionlabel_txt.setText(li_position[2])
        #     self.idlabel_txt.setText(li_id[2])
        #     self.birthlabel_txt.setText(li_birth[2])
        #     self.emaillabel_txt.setText(li_email[2])
        #
        #     if li_position[2] == 'employee':
        #         self.positionlabel_txt.setCurrentText("employee")
        #     else:
        #         self.positionlabel_txt.setCurrentText("manager")
        #
        # if self.namecombobox.currentText() == str(li_name[3]):
        #     self.namelabel_txt.setText(li_name[3])
        #     #self.positionlabel_txt.setText(li_position[3])
        #     self.idlabel_txt.setText(li_id[3])
        #     self.birthlabel_txt.setText(li_birth[3])
        #     self.emaillabel_txt.setText(li_email[3])
        #
        #     if li_position[3] == 'employee':
        #         self.positionlabel_txt.setCurrentText("employee")
        #     else:
        #         self.positionlabel_txt.setCurrentText("manager")
        #
        # if self.namecombobox.currentText() == str(li_name[4]):
        #     self.namelabel_txt.setText(li_name[4])
        #     #self.positionlabel_txt.setText(li_position[4])
        #     self.idlabel_txt.setText(li_id[4])
        #     self.birthlabel_txt.setText(li_birth[4])
        #     self.emaillabel_txt.setText(li_email[4])
        #
        #     if li_position[4] == 'employee':
        #         self.positionlabel_txt.setCurrentText("employee")
        #     else:
        #         self.positionlabel_txt.setCurrentText("manager")

    # def combo_btn_clicked(self, text):
    #     self.namelabel_txt.setText(self.namecombobox.itemText(text))


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

        self.setGeometry(300, 450, 300, 200)
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
        self.mainlabel_txt.setGeometry(QtCore.QRect(200, 170, 341, 41))

        self.namecombobox = QComboBox(self)
        # self.namecombobox.addItem("오종진")
        self.namecombobox.addItems(li)
        # self.namecombobox.insertSeparator(4)
        self.namecombobox.activated.connect(self.combo_change)
        self.namecombobox.setGeometry(QtCore.QRect(200, 210, 101, 30))

        self.combo_btn = QPushButton(self)
        self.combo_btn.setText('선택')
        combo_btn_font = QtGui.QFont()
        combo_btn_font.setPointSize(10)
        combo_btn_font.setFamily("서울남산 장체M")
        self.combo_btn.setFont(combo_btn_font)
        self.combo_btn.setGeometry(QtCore.QRect(320, 210, 70, 30))
        self.combo_btn.clicked.connect(self.combo_btn_clicked)
        self.combo_btn_dialogs = list()

        self.back_btn = QPushButton(self)
        self.back_btn.setGeometry(QtCore.QRect(0, 0, 80, 52))
        self.back_btn.setText("뒤로가기")
        back_btn_font = QtGui.QFont()
        back_btn_font.setPointSize(10)
        back_btn_font.setFamily("서울남산 장체M")
        self.back_btn.setFont(back_btn_font)
        self.back_btn.clicked.connect(self.back_btn_clicked)
        self.back_btn_dialogs = list()

        self.setGeometry(150, 100, 1200, 800)
        self.setWindowTitle('[슈퍼 관리자] 관리자/직원 삭제')
        self.show()

    def combo_change(self, text):
        delete_a = self.namecombobox.itemText(text)

    def combo_btn_clicked(self):
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

        self.setGeometry(300, 450, 300, 200)
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

        self.input_text.move(25, 25)
        self.send_btn.move(350, 25)
        self.database_btn.move(430, 25)
        self.sudo_btn.move(25, 100)
        self.manager_btn.move(220, 100)
        self.staff_btn.move(415, 100)
        self.send_txt.move(130, 270)
        self.recv_txt.move(430, 270)
        self.send_txtB.move(25, 300)
        self.recv_txtB.move(325, 300)
        self.login_btn.move(275, 260)

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
        self.goto_server.move(250, 455)
        self.goto_server.clicked.connect(self.goto_server_clicked)
        self.goto_server_dialogs = list()


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
        # self.login_btn_dialogs

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


class login_window(QMainWindow):
    def __init__(self, parent=None):
        super(login_window, self).__init__(parent)

        self.back_btn = QPushButton(self)
        self.back_btn.setGeometry(QtCore.QRect(0, 0, 80, 52))
        self.back_btn.setText("뒤로가기")
        back_btn_font = QtGui.QFont()
        back_btn_font.setPointSize(10)
        back_btn_font.setFamily("서울남산 장체M")
        self.back_btn.setFont(back_btn_font)
        self.back_btn.clicked.connect(self.back_btn_clicked)
        self.back_btn_dialogs = list()

        self.setGeometry(150, 100, 1200, 800)
        self.setWindowTitle('스마트 팩토리 로그인')
        self.show()

    def back_btn_clicked(self):
        self.close()
        back_btn_dialogs = First(self)
        self.back_btn_dialogs.append(back_btn_dialogs)
        back_btn_dialogs.show()


#멀티 소켓 통신 테스트
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
        self.ip_label.setGeometry(QtCore.QRect(20, 30, 200, 50))

        # a = socket.gethostbyname(socket.gethostbyname())

        self.serverIP_txt = QLineEdit(self)
        self.serverIP_txt.setText(socket.gethostbyname(socket.gethostname()))
        serverIP_txt_font = QtGui.QFont()
        serverIP_txt_font.setPointSize(10)
        serverIP_txt_font.setFamily("서울남산 장체M")
        self.serverIP_txt.setFont(serverIP_txt_font)
        self.serverIP_txt.setGeometry(QtCore.QRect(100, 40, 120, 30))

        self.port_label = QLabel(self)
        self.port_label.setText("Server Port")
        port_label_font = QtGui.QFont()
        port_label_font.setPointSize(8)
        port_label_font.setFamily("서울남산 장체M")
        self.port_label.setFont(port_label_font)
        self.port_label.setGeometry(QtCore.QRect(250, 30, 200, 50))

        self.serverPORT_txt = QLineEdit(self)
        self.serverPORT_txt.setText(str(multi_port))
        serverPORT_txt_font = QtGui.QFont()
        serverPORT_txt_font.setPointSize(10)
        serverPORT_txt_font.setFamily("서울남산 장체M")
        self.serverPORT_txt.setFont(serverPORT_txt_font)
        self.serverPORT_txt.setGeometry(QtCore.QRect(350, 40, 120, 30))

        self.server_start = QPushButton(self)
        self.server_start.setText("서버 실행")
        self.server_start.setCheckable(True)
        server_start_font = QtGui.QFont()
        server_start_font.setPointSize(10)
        server_start_font.setFamily("서울남산 장체M")
        self.server_start.setFont(server_start_font)
        self.server_start.setGeometry(QtCore.QRect(490, 40, 100, 30))
        self.server_start.clicked.connect(self.server_start_clicked)

        self.ip_info = QTableWidget(self)
        self.ip_info.setColumnCount(2)
        self.ip_info.setRowCount(5)
        self.ip_info.setGeometry(QtCore.QRect(20, 100, 280, 300))
        self.ip_info.setHorizontalHeaderItem(0, QTableWidgetItem('ip'))
        self.ip_info.setHorizontalHeaderItem(1, QTableWidgetItem('port'))

        self.recv_msg_label = QLabel(self)
        self.recv_msg_label.setText("받은 메세지")
        recv_msg_label_font = QtGui.QFont()
        recv_msg_label_font.setPointSize(10)
        recv_msg_label_font.setFamily("서울남산 장체M")
        self.recv_msg_label.setFont(recv_msg_label_font)
        self.recv_msg_label.setGeometry(QtCore.QRect(330, 85, 100, 50))

        self.msg_box = QTextBrowser(self)
        self.msg_box.setGeometry(QtCore.QRect(330, 130, 260, 180))

        self.send_msg_label = QLabel(self)
        self.send_msg_label.setText("보낼 메세지")
        send_msg_label_font = QtGui.QFont()
        send_msg_label_font.setPointSize(10)
        send_msg_label_font.setFamily("서울남산 장체M")
        self.send_msg_label.setFont(send_msg_label_font)
        self.send_msg_label.setGeometry(QtCore.QRect(330, 301, 100, 50))

        self.send_msg_txt = QLineEdit(self)
        self.send_msg_txt.setText("")
        send_msg_txt_font = QtGui.QFont()
        send_msg_txt_font.setPointSize(8)
        send_msg_txt_font.setFamily("서울남산 장체M")
        self.send_msg_txt.setFont(send_msg_txt_font)
        self.send_msg_txt.setGeometry(QtCore.QRect(330, 340, 260, 25))

        self.send_msg_btn = QPushButton(self)
        self.send_msg_btn.setText("보내기")
        send_msg_btn_font = QtGui.QFont()
        send_msg_btn_font.setPointSize(10)
        send_msg_btn_font.setFamily("서울남산 장체M")
        self.send_msg_btn.setFont(send_msg_btn_font)
        self.send_msg_btn.setGeometry(QtCore.QRect(330, 370, 130, 30))

        self.clear_msg = QPushButton(self)
        self.clear_msg.setText("채팅창 지움")
        clear_msg_font = QtGui.QFont()
        clear_msg_font.setPointSize(10)
        clear_msg_font.setFamily("서울남산 장체M")
        self.clear_msg.setFont(clear_msg_font)
        self.clear_msg.setGeometry(QtCore.QRect(470, 370, 120, 30))

        self.main = QPushButton(self)
        self.main.setText("스마트 팩토리로 이동")
        main_font = QtGui.QFont()
        main_font.setPointSize(13)
        main_font.setFamily("서울남산 장체M")
        self.main.setFont(main_font)
        self.main.setGeometry(QtCore.QRect(150, 430, 300, 50))
        self.main.clicked.connect(self.main_btn_clicked)
        self.main_btn_dialogs = list()
        self.main.setToolTip('스마트 팩토리 화면으로 이동한다.')

        print(manager_menu_stockmenu.li_num)
        # self.setStyleSheet('background:#F1F4FC')

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
    main1 = multi_thread()
    main1.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
