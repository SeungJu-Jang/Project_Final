#!/usr/bin/env python
# -*- coding: utf-8 -*-
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5 import uic
from PyQt5 import QtWidgets, QtGui
from PyQt5 import QtGui, QtCore
import sys
import socket
import pymysql
import time

HOST = '192.168.0.144'
PORT = 8080


#직원 메뉴
class staff_menu(QMainWindow):
    def __init__(self, parent=None):
        super(staff_menu, self).__init__(parent)

        self.mainlabel_txt = QLabel(self)
        self.mainlabel_txt.setText("직원 메뉴")
        mainlabel_txt_font = QtGui.QFont()
        mainlabel_txt_font.setPointSize(23)
        mainlabel_txt_font.setFamily("G마켓 산스 TTF Light")
        self.mainlabel_txt.setFont(mainlabel_txt_font)
        self.mainlabel_txt.setGeometry(QtCore.QRect(240, 60, 341, 41))

        self.search_btn = QPushButton(self)
        self.search_btn.setText('상품 정보')
        search_btn_font = QtGui.QFont()
        search_btn_font.setPointSize(20)
        search_btn_font.setFamily("G마켓 산스 TTF Light")
        self.search_btn.setFont(search_btn_font)
        self.search_btn.setGeometry(QtCore.QRect(130, 210, 150, 150))

        self.edit_btn = QPushButton(self)
        self.edit_btn.setText('재고 관리')
        edit_btn_font = QtGui.QFont()
        edit_btn_font.setPointSize(18)
        edit_btn_font.setFamily("G마켓 산스 TTF Light")
        self.edit_btn.setFont(edit_btn_font)
        self.edit_btn.setGeometry(QtCore.QRect(330, 210, 150, 150))

        self.logout_btn = QPushButton(self)
        self.logout_btn.setText('로그아웃')
        logout_btn_font = QtGui.QFont()
        logout_btn_font.setPointSize(9)
        logout_btn_font.setFamily("G마켓 산스 TTF Light")
        self.logout_btn.setFont(logout_btn_font)
        self.logout_btn.setGeometry(QtCore.QRect(500, 30, 70, 30))

        self.logout_btn.clicked.connect(self.logout_btn_clicked)
        self.logout_btn_dialogs = list()

        self.setGeometry(150, 300, 610, 500)
        self.setWindowTitle('직원 메뉴')
        self.show()

    def logout_btn_clicked(self):
        self.close()
        logout_btn_dialogs = First(self)
        self.logout_btn_dialogs.append(logout_btn_dialogs)
        logout_btn_dialogs.show()

#관리자 메뉴
class manager_menu(QMainWindow):
    def __init__(self, parent=None):
        super(manager_menu, self).__init__(parent)

        self.mainlabel_txt = QLabel(self)
        self.mainlabel_txt.setText("관리자 메뉴")
        mainlabel_txt_font = QtGui.QFont()
        mainlabel_txt_font.setPointSize(23)
        mainlabel_txt_font.setFamily("G마켓 산스 TTF Light")
        self.mainlabel_txt.setFont(mainlabel_txt_font)
        self.mainlabel_txt.setGeometry(QtCore.QRect(200, 60, 341, 41))

        self.info_btn = QPushButton(self)
        self.info_btn.setText('상품 정보')
        info_btn_font = QtGui.QFont()
        info_btn_font.setPointSize(20)
        info_btn_font.setFamily("G마켓 산스 TTF Light")
        self.info_btn.setFont(info_btn_font)
        self.info_btn.setGeometry(QtCore.QRect(30, 150, 150, 150))
        self.info_btn_dialogs = list()

        self.sales_btn = QPushButton(self)
        self.sales_btn.setText('매출 확인')
        sales_btn_font = QtGui.QFont()
        sales_btn_font.setPointSize(20)
        sales_btn_font.setFamily("G마켓 산스 TTF Light")
        self.sales_btn.setFont(sales_btn_font)
        self.sales_btn.setGeometry(QtCore.QRect(30, 330, 150, 150))
        self.sales_btn_dialogs = list()

        self.control_btn = QPushButton(self)
        self.control_btn.setText('공장 제어')
        control_btn_font = QtGui.QFont()
        control_btn_font.setPointSize(18)
        control_btn_font.setFamily("G마켓 산스 TTF Light")
        self.control_btn.setFont(control_btn_font)
        self.control_btn.setGeometry(QtCore.QRect(230, 150, 150, 150))
        self.control_btn_dialogs = list()

        self.manager_btn = QPushButton(self)
        self.manager_btn.setText('직원 관리')
        manager_btn_font = QtGui.QFont()
        manager_btn_font.setPointSize(18)
        manager_btn_font.setFamily("G마켓 산스 TTF Light")
        self.manager_btn.setFont(manager_btn_font)
        self.manager_btn.setGeometry(QtCore.QRect(230, 330, 150, 150))
        self.manager_btn_dialogs = list()

        self.stock_btn = QPushButton(self)
        self.stock_btn.setText('재고 관리')
        stock_btn_font = QtGui.QFont()
        stock_btn_font.setPointSize(18)
        stock_btn_font.setFamily("G마켓 산스 TTF Light")
        self.stock_btn.setFont(stock_btn_font)
        self.stock_btn.setGeometry(QtCore.QRect(430, 150, 150, 150))
        self.stock_btn_dialogs = list()

        self.logout_btn = QPushButton(self)
        self.logout_btn.setText('로그아웃')
        logout_btn_font = QtGui.QFont()
        logout_btn_font.setPointSize(9)
        logout_btn_font.setFamily("G마켓 산스 TTF Light")
        self.logout_btn.setFont(logout_btn_font)
        self.logout_btn.setGeometry(QtCore.QRect(500, 30, 70, 30))
        self.logout_btn_dialogs = list()

        self.info_btn.clicked.connect(self.info_btn_clicked)
        self.control_btn.clicked.connect(self.control_btn_clicked)
        self.stock_btn.clicked.connect(self.stock_btn_clicked)
        self.sales_btn.clicked.connect(self.sales_btn_clicked)
        self.manager_btn.clicked.connect(self.management_btn_clicked)
        self.logout_btn.clicked.connect(self.logout_btn_clicked)

        self.setGeometry(150, 300, 610, 500)
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


#관리자 메뉴 - 상품 정보 메뉴
class manager_menu_infomenu(QMainWindow):
    def __init__(self, parent=None):
        super(manager_menu_infomenu, self).__init__(parent)

        self.mainlabel_txt = QLabel(self)
        self.mainlabel_txt.setText("상품 정보 확인")
        mainlabel_txt_font = QtGui.QFont()
        mainlabel_txt_font.setPointSize(15)
        mainlabel_txt_font.setFamily("G마켓 산스 TTF Light")
        self.mainlabel_txt.setFont(mainlabel_txt_font)
        self.mainlabel_txt.setGeometry(QtCore.QRect(220, 50, 341, 41))

        self.namelabel = QLabel(self)
        self.namelabel.setText("· 상품 이름 :")
        namelabel_font = QtGui.QFont()
        namelabel_font.setPointSize(10)
        namelabel_font.setFamily("G마켓 산스 TTF Light")
        self.namelabel.setFont(namelabel_font)
        self.namelabel.setGeometry(QtCore.QRect(100, 140, 341, 41))



        self.codelabel = QLabel(self)
        self.codelabel.setText("· 상품 코드 :")
        codelabel_font = QtGui.QFont()
        codelabel_font.setPointSize(10)
        codelabel_font.setFamily("G마켓 산스 TTF Light")
        self.codelabel.setFont(codelabel_font)
        self.codelabel.setGeometry(QtCore.QRect(100, 200, 341, 41))

        self.pricelabel = QLabel(self)
        self.pricelabel.setText("· 상품 단가 :")
        pricelabel_font = QtGui.QFont()
        pricelabel_font.setPointSize(10)
        pricelabel_font.setFamily("G마켓 산스 TTF Light")
        self.pricelabel.setFont(pricelabel_font)
        self.pricelabel.setGeometry(QtCore.QRect(100, 260, 341, 41))

        self.back_btn = QPushButton(self)
        self.back_btn.setGeometry(QtCore.QRect(0, 0, 80, 52))
        self.back_btn.setText("뒤로가기")
        back_btn_font = QtGui.QFont()
        back_btn_font.setPointSize(10)
        back_btn_font.setFamily("G마켓 산스 TTF Light")
        self.back_btn.setFont(back_btn_font)
        self.back_btn.clicked.connect(self.back_btn_clicked)
        self.back_btn_dialogs = list()

        self.setGeometry(150, 300, 610, 500)
        self.setWindowTitle('[관리자 메뉴] 상품 정보')
        self.show()

    def back_btn_clicked(self):
        self.close()
        back_btn_dialogs = manager_menu(self)
        self.back_btn_dialogs.append(back_btn_dialogs)
        back_btn_dialogs.show()


#관리자 메뉴 - 공장 제어 메뉴
class manager_menu_controlmenu(QMainWindow):
    def __init__(self, parent=None):
        super(manager_menu_controlmenu, self).__init__(parent)

        self.mainlabel_txt = QLabel(self)
        self.mainlabel_txt.setText("레일 가동 제어")
        mainlabel_txt_font = QtGui.QFont()
        mainlabel_txt_font.setPointSize(15)
        mainlabel_txt_font.setFamily("G마켓 산스 TTF Light")
        self.mainlabel_txt.setFont(mainlabel_txt_font)
        self.mainlabel_txt.setGeometry(QtCore.QRect(220, 50, 341, 41))

        self.back_btn = QPushButton(self)
        self.back_btn.setGeometry(QtCore.QRect(0, 0, 80, 52))
        self.back_btn.setText("뒤로가기")
        back_btn_font = QtGui.QFont()
        back_btn_font.setPointSize(10)
        back_btn_font.setFamily("G마켓 산스 TTF Light")
        self.back_btn.setFont(back_btn_font)
        self.back_btn.clicked.connect(self.back_btn_clicked)
        self.back_btn_dialogs = list()

        self.motorON_btn = QPushButton(self)
        self.motorON_btn.setGeometry(QtCore.QRect(70, 200, 180, 180))
        self.motorON_btn.setText("ON")
        motorON_btn_font = QtGui.QFont()
        motorON_btn_font.setPointSize(20)
        motorON_btn_font.setFamily("G마켓 산스 TTF Light")
        self.motorON_btn.setFont(motorON_btn_font)
        self.motorON_btn.clicked.connect(self.motorON_btn_clicked)
        # self.motorON_btn_dialogs = list()

        self.motorOFF_btn = QPushButton(self)
        self.motorOFF_btn.setGeometry(QtCore.QRect(350, 200, 180, 180))
        self.motorOFF_btn.setText("OFF")
        motorOFF_btn_font = QtGui.QFont()
        motorOFF_btn_font.setPointSize(20)
        motorOFF_btn_font.setFamily("G마켓 산스 TTF Light")
        self.motorOFF_btn.setFont(motorOFF_btn_font)
        self.motorOFF_btn.clicked.connect(self.motorOFF_btn_clicked)
        # self.motorOFF_btn_dialogs = list()

        self.setGeometry(150, 300, 610, 500)
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


#관리자 메뉴 - 재고 관리 메뉴
class manager_menu_stockmenu(QMainWindow):
    def __init__(self, parent=None):
        super(manager_menu_stockmenu, self).__init__(parent)

        self.mainlabel_txt = QLabel(self)
        self.mainlabel_txt.setText("재고 관리 및 수정")
        mainlabel_txt_font = QtGui.QFont()
        mainlabel_txt_font.setPointSize(15)
        mainlabel_txt_font.setFamily("G마켓 산스 TTF Light")
        self.mainlabel_txt.setFont(mainlabel_txt_font)
        self.mainlabel_txt.setGeometry(QtCore.QRect(220, 50, 341, 41))

        #테이블 설정
        self.stock_table = QTableWidget(self)
        self.stock_table.setColumnCount(7)
        self.stock_table.setRowCount(7)
        self.stock_table.setGeometry(QtCore.QRect(50, 120, 500, 250))
        self.stock_table.setHorizontalHeaderLabels([
            "브랜드", "종류", "모델명", "상품 코드", "상품 가격",
            "총 물량", "재고량", "판매량"])
        self.stock_table.setItem(0, 0, QTableWidgetItem(" ༼ ༎ຶ ෴ ༎ຶ༽ "))
        self.stock_table.setItem(0, 1, QTableWidgetItem(" ༼;´༎ຶ ۝༎ຶ`༽ "))
        self.stock_table.setItem(0, 2, QTableWidgetItem(" ༽΄◞ิ౪◟ิ‵༼ "))
        self.stock_table.setItem(0, 3, QTableWidgetItem(" ⎛⎝⎛° ͜ʖ°⎞⎠⎞ "))
        self.stock_table.setItem(1, 0, QTableWidgetItem(" ξ(｡◕ˇ◊ˇ◕｡)ξ "))
        self.stock_table.setItem(1, 1, QTableWidgetItem("  (๑¯ਊ¯)σ "))
        self.stock_table.setItem(1, 2, QTableWidgetItem(" (っ˘ڡ˘ς) "))
        self.stock_table.setItem(1, 3, QTableWidgetItem(" ( ≖ଳ≖) "))
        self.stock_table.setItem(2, 0, QTableWidgetItem(" (´ε｀ ʃƪ)♡ "))
        self.stock_table.setItem(2, 1, QTableWidgetItem(" (ʃƪ ˘ ³˘) "))





        self.stock_add_btn = QPushButton(self)
        self.stock_add_btn.setGeometry(QtCore.QRect(50, 400, 130, 50))
        self.stock_add_btn.setText("상품 추가")
        stock_add_btn_font = QtGui.QFont()
        stock_add_btn_font.setPointSize(10)
        stock_add_btn_font.setFamily("G마켓 산스 TTF Light")
        self.stock_add_btn.setFont(stock_add_btn_font)
        self.stock_add_btn.clicked.connect(self.stock_add_btn_clicked)
        self.stock_add_btn_dialogs = list()

        self.stock_edit_btn = QPushButton(self)
        self.stock_edit_btn.setGeometry(QtCore.QRect(230, 400, 130, 50))
        self.stock_edit_btn.setText("재고 수정")
        stock_edit_btn_font = QtGui.QFont()
        stock_edit_btn_font.setPointSize(10)
        stock_edit_btn_font.setFamily("G마켓 산스 TTF Light")
        self.stock_edit_btn.setFont(stock_edit_btn_font)
        self.stock_edit_btn.clicked.connect(self.stock_edit_btn_clicked)
        self.stock_edit_btn_dialogs = list()

        self.stock_delete_btn = QPushButton(self)
        self.stock_delete_btn.setGeometry(QtCore.QRect(420, 400, 130, 50))
        self.stock_delete_btn.setText("상품 삭제")
        stock_delete_font = QtGui.QFont()
        stock_delete_font.setPointSize(10)
        stock_delete_font.setFamily("G마켓 산스 TTF Light")
        self.stock_delete_btn.setFont(stock_delete_font)
        self.stock_delete_btn.clicked.connect(self.stock_delete_btn_clicked)
        self.stock_delete_btn_dialogs = list()

        self.back_btn = QPushButton(self)
        self.back_btn.setGeometry(QtCore.QRect(0, 0, 80, 52))
        self.back_btn.setText("뒤로가기")
        back_btn_font = QtGui.QFont()
        back_btn_font.setPointSize(10)
        back_btn_font.setFamily("G마켓 산스 TTF Light")
        self.back_btn.setFont(back_btn_font)
        self.back_btn.clicked.connect(self.back_btn_clicked)
        self.back_btn_dialogs = list()

        #테이블 수정 금지 모드
        self.stock_table.setEditTriggers(QAbstractItemView.NoEditTriggers)

        self.setGeometry(150, 300, 610, 500)
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


#관리자 메뉴 - 재고 관리 - 상품 추가 화면
class manager_stock_add(QMainWindow):
    def __init__(self, parent=None):
        super(manager_stock_add, self).__init__(parent)

        self.stock_add_alarm_btn = QPushButton(self)
        self.stock_add_alarm_btn.setGeometry(QtCore.QRect(230, 400, 130, 50))
        self.stock_add_alarm_btn.setText("확인")
        stock_add_alarm_btn_font = QtGui.QFont()
        stock_add_alarm_btn_font.setPointSize(10)
        stock_add_alarm_btn_font.setFamily("G마켓 산스 TTF Light")
        self.stock_add_alarm_btn.setFont(stock_add_alarm_btn_font)
        self.stock_add_alarm_btn.clicked.connect(self.stock_add_alarm_btn_clicked)
        self.stock_add_alarm_btn_dialogs = list()

    # def


#관리자 메뉴 - 재고 관리 - 재고 수정 화면
class manager_stock_edit(QMainWindow):
    def __init__(self, parent=None):
        super(manager_stock_edit, self).__init__(parent)



        self.setGeometry(150, 300, 610, 500)
        self.setWindowTitle('[관리자 메뉴] 매출 확인')
        self.show()


class manager_stock_delete(QMainWindow):
    def __init__(self, parent=None):
        super(manager_stock_delete, self).__init__(parent)

        self.setGeometry(150, 300, 610, 500)
        self.setWindowTitle('[관리자 메뉴] 매출 확인')
        self.show()







#관리자 메뉴 - 매출 확인 메뉴
class manager_menu_salesmenu(QMainWindow):
    def __init__(self, parent=None):
        super(manager_menu_salesmenu, self).__init__(parent)

        self.back_btn = QPushButton(self)
        self.back_btn.setGeometry(QtCore.QRect(0, 0, 80, 52))
        self.back_btn.setText("뒤로가기")
        back_btn_font = QtGui.QFont()
        back_btn_font.setPointSize(10)
        back_btn_font.setFamily("G마켓 산스 TTF Light")
        self.back_btn.setFont(back_btn_font)
        self.back_btn.clicked.connect(self.back_btn_clicked)
        self.back_btn_dialogs = list()


        self.setGeometry(150, 300, 610, 500)
        self.setWindowTitle('[관리자 메뉴] 매출 확인')
        self.show()

    def back_btn_clicked(self):
        self.close()
        back_btn_dialogs = manager_menu(self)
        self.back_btn_dialogs.append(back_btn_dialogs)
        back_btn_dialogs.show()


#관리자 메뉴 - 직원 관리 메뉴
class manager_menu_managermenu(QMainWindow):
    def __init__(self, parent=None):
        super(manager_menu_managermenu, self).__init__(parent)

        self.back_btn = QPushButton(self)
        self.back_btn.setGeometry(QtCore.QRect(0, 0, 80, 52))
        self.back_btn.setText("뒤로가기")
        back_btn_font = QtGui.QFont()
        back_btn_font.setPointSize(10)
        back_btn_font.setFamily("G마켓 산스 TTF Light")
        self.back_btn.setFont(back_btn_font)
        self.back_btn.clicked.connect(self.back_btn_clicked)
        self.back_btn_dialogs = list()


        self.setGeometry(150, 300, 610, 500)
        self.setWindowTitle('[관리자 메뉴] 직원 관리')
        self.show()

    def back_btn_clicked(self):
        self.close()
        back_btn_dialogs = manager_menu(self)
        self.back_btn_dialogs.append(back_btn_dialogs)
        back_btn_dialogs.show()


#슈퍼 관리자 메뉴
class sudo_menu(QMainWindow):
    def __init__(self, parent=None):
        super(sudo_menu, self).__init__(parent)

        self.mainlabel_txt = QLabel(self)
        self.mainlabel_txt.setText("슈퍼 관리자 메뉴")
        mainlabel_txt_font = QtGui.QFont()
        mainlabel_txt_font.setPointSize(23)
        mainlabel_txt_font.setFamily("G마켓 산스 TTF Light")
        self.mainlabel_txt.setFont(mainlabel_txt_font)
        self.mainlabel_txt.setGeometry(QtCore.QRect(160, 60, 341, 41))

        self.search_btn = QPushButton(self)
        self.search_btn.setText('직원 확인')
        search_btn_font = QtGui.QFont()
        search_btn_font.setPointSize(20)
        search_btn_font.setFamily("G마켓 산스 TTF Light")
        self.search_btn.setFont(search_btn_font)
        self.search_btn.setGeometry(QtCore.QRect(30, 210, 150, 150))

        self.edit_btn = QPushButton(self)
        self.edit_btn.setText('직원 정보\n수정')
        edit_btn_font = QtGui.QFont()
        edit_btn_font.setPointSize(18)
        edit_btn_font.setFamily("G마켓 산스 TTF Light")
        self.edit_btn.setFont(edit_btn_font)
        self.edit_btn.setGeometry(QtCore.QRect(230, 210, 150, 150))

        self.delete_btn = QPushButton(self)
        self.delete_btn.setText('관리자/\n직원\n삭제')
        delete_btn_font = QtGui.QFont()
        delete_btn_font.setPointSize(18)
        delete_btn_font.setFamily("G마켓 산스 TTF Light")
        self.delete_btn.setFont(delete_btn_font)
        self.delete_btn.setGeometry(QtCore.QRect(430, 210, 150, 150))

        self.logout_btn = QPushButton(self)
        self.logout_btn.setText('로그아웃')
        logout_btn_font = QtGui.QFont()
        logout_btn_font.setPointSize(9)
        logout_btn_font.setFamily("G마켓 산스 TTF Light")
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

        self.setGeometry(150, 300, 610, 500)
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


#슈퍼 관리자 메뉴 - 직원 확인
class sudo_menu_searchmenu(QMainWindow):
    def __init__(self, parent=None):
        super(sudo_menu_searchmenu, self).__init__(parent)

        con = pymysql.connect(host="192.168.0.34", user="root", password="1234", db='mydb', charset='utf8')
        cur = con.cursor()
        sql = "select name from user_info;"
        cur.execute(sql)
        data = cur.fetchall()
        li = [x[0] for x in data]
        user1 = str(li[0])
        user2 = str(li[1])
        user3 = str(li[2])
        user4 = str(li[3])
        user5 = str(li[4])

        self.mainlabel_txt = QLabel(self)
        self.mainlabel_txt.setText("· 확인할 직원 이름을 선택하세요.")
        mainlabel_txt_font = QtGui.QFont()
        mainlabel_txt_font.setPointSize(9)
        mainlabel_txt_font.setFamily("G마켓 산스 TTF Light")
        self.mainlabel_txt.setFont(mainlabel_txt_font)
        self.mainlabel_txt.setGeometry(QtCore.QRect(200, 40, 341, 41))

        self.namecombobox = QComboBox(self)
        # self.namecombobox.addItem("오종진")
        self.namecombobox.addItems([user1, user2, user3, user4, user5])
        self.namecombobox.insertSeparator(4)
        self.namecombobox.activated.connect(self.combo_change)
        self.namecombobox.setGeometry(QtCore.QRect(250, 80, 100, 30))

        # self.combo_btn = QPushButton(self)
        # self.combo_btn.setText('선택')
        # combo_btn_font = QtGui.QFont()
        # combo_btn_font.setPointSize(10)
        # combo_btn_font.setFamily("G마켓 산스 TTF Light")
        # self.combo_btn.setFont(combo_btn_font)
        # self.combo_btn.setGeometry(QtCore.QRect(320, 80, 70, 30))
        # self.combo_btn.clicked.connect(self.combo_btn_clicked)

        self.namelabel = QLabel(self)
        self.namelabel.setText("· 이름 : ")
        namelabel_font = QtGui.QFont()
        namelabel_font.setPointSize(10)
        namelabel_font.setFamily("G마켓 산스 TTF Light")
        self.namelabel.setFont(namelabel_font)
        self.namelabel.setGeometry(QtCore.QRect(300, 140, 100, 100))

        #데이터베이스 연동 이름 부분
        self.namelabel_txt = QLabel(self)
        self.namelabel_txt.setText("")
        namelabel_txt_font = QtGui.QFont()
        namelabel_txt_font.setPointSize(10)
        namelabel_txt_font.setFamily("G마켓 산스 TTF Light")
        self.namelabel_txt.setFont(namelabel_txt_font)
        self.namelabel_txt.setGeometry(QtCore.QRect(360, 140, 300, 100))

        self.positionlabel = QLabel(self)
        self.positionlabel.setText("· 직책 : ")
        positionlabel_font = QtGui.QFont()
        positionlabel_font.setPointSize(10)
        positionlabel_font.setFamily("G마켓 산스 TTF Light")
        self.positionlabel.setFont(positionlabel_font)
        self.positionlabel.setGeometry(QtCore.QRect(300, 180, 100, 100))

        # 데이터베이스 연동 직책 부분
        self.positionlabel_txt = QLabel(self)
        self.positionlabel_txt.setText("")
        positionlabel_txt_font = QtGui.QFont()
        positionlabel_txt_font.setPointSize(10)
        positionlabel_txt_font.setFamily("G마켓 산스 TTF Light")
        self.positionlabel_txt.setFont(positionlabel_txt_font)
        self.positionlabel_txt.setGeometry(QtCore.QRect(360, 180, 300, 100))

        self.idlabel = QLabel(self)
        self.idlabel.setText("· ID : ")
        idlabel_font = QtGui.QFont()
        idlabel_font.setPointSize(10)
        idlabel_font.setFamily("G마켓 산스 TTF Light")
        self.idlabel.setFont(idlabel_font)
        self.idlabel.setGeometry(QtCore.QRect(300, 220, 100, 100))

        # 데이터베이스 연동 ID 부분
        self.idlabel_txt = QLabel(self)
        self.idlabel_txt.setText("")
        idlabel_txt_font = QtGui.QFont()
        idlabel_txt_font.setPointSize(10)
        idlabel_txt_font.setFamily("G마켓 산스 TTF Light")
        self.idlabel_txt.setFont(idlabel_txt_font)
        self.idlabel_txt.setGeometry(QtCore.QRect(350, 220, 300, 100))

        self.birthlabel = QLabel(self)
        self.birthlabel.setText("· 생년월일 : ")
        birthlabel_font = QtGui.QFont()
        birthlabel_font.setPointSize(10)
        birthlabel_font.setFamily("G마켓 산스 TTF Light")
        self.birthlabel.setFont(birthlabel_font)
        self.birthlabel.setGeometry(QtCore.QRect(300, 260, 100, 100))

        # 데이터베이스 연동 생년월일 부분
        self.birthlabel_txt = QLabel(self)
        self.birthlabel_txt.setText("")
        birthlabel_txt_font = QtGui.QFont()
        birthlabel_txt_font.setPointSize(10)
        birthlabel_txt_font.setFamily("G마켓 산스 TTF Light")
        self.birthlabel_txt.setFont(birthlabel_txt_font)
        self.birthlabel_txt.setGeometry(QtCore.QRect(390, 260, 300, 100))

        self.emaillabel = QLabel(self)
        self.emaillabel.setText("· E-Mail : ")
        emaillabel_font = QtGui.QFont()
        emaillabel_font.setPointSize(10)
        emaillabel_font.setFamily("G마켓 산스 TTF Light")
        self.emaillabel.setFont(emaillabel_font)
        self.emaillabel.setGeometry(QtCore.QRect(300, 300, 100, 100))

        # 데이터베이스 연동 이메일 부분
        self.emaillabel_txt = QLabel(self)
        self.emaillabel_txt.setText("")
        emaillabel_txt_font = QtGui.QFont()
        emaillabel_txt_font.setPointSize(10)
        emaillabel_txt_font.setFamily("G마켓 산스 TTF Light")
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
        back_btn_font.setFamily("G마켓 산스 TTF Light")
        self.back_btn.setFont(back_btn_font)
        self.back_btn.clicked.connect(self.back_btn_clicked)
        self.back_btn_dialogs = list()

        # self.name_label = QLabel(self)
        # self.name_label.setText("")
        # self.name_label.setGeometry(QtCore.QRect(370, 100, 100, 100))

        self.setGeometry(150, 300, 610, 500)
        self.setWindowTitle('[슈퍼 관리자] 직원 확인')
        self.show()

    #콤보박스 선택시 변경
    def combo_change(self, text):

        con = pymysql.connect(host="192.168.0.34", user="root", password="1234", db='mydb', charset='utf8')

        cur_name = con.cursor()
        cur_position = con.cursor()
        cur_id = con.cursor()
        cur_birth = con.cursor()
        cur_email = con.cursor()

        sql_name = "select distinct name from user_info;"
        sql_position = "select distinct position from user_info;"
        sql_id = "select distinct id from user_info;"
        sql_birth = "select distinct birth from user_info;"
        sql_email = "select distinct email from user_info"

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

        if self.namecombobox.currentText() == '한민경':
            self.namelabel_txt.setText(li_name[0])
            self.positionlabel_txt.setText(li_position[0])
            self.idlabel_txt.setText(li_id[0])
            self.birthlabel_txt.setText(li_birth[0])
            self.emaillabel_txt.setText(li_email[0])

        if self.namecombobox.currentText() == '오종진':
            self.namelabel_txt.setText(li_name[1])
            self.positionlabel_txt.setText(li_position[1])
            self.idlabel_txt.setText(li_id[1])
            self.birthlabel_txt.setText(li_birth[1])
            self.emaillabel_txt.setText(li_email[1])

        if self.namecombobox.currentText() == '조아람':
            self.namelabel_txt.setText(li_name[2])
            self.positionlabel_txt.setText(li_position[0])
            self.idlabel_txt.setText(li_id[2])
            self.birthlabel_txt.setText(li_birth[2])
            self.emaillabel_txt.setText(li_email[2])

        if self.namecombobox.currentText() == '문은오':
            self.namelabel_txt.setText(li_name[3])
            self.positionlabel_txt.setText(li_position[0])
            self.idlabel_txt.setText(li_id[3])
            self.birthlabel_txt.setText(li_birth[3])
            self.emaillabel_txt.setText(li_email[3])

        if self.namecombobox.currentText() == '장승주':
            self.namelabel_txt.setText(li_name[4])
            self.positionlabel_txt.setText(li_position[0])
            self.idlabel_txt.setText(li_id[4])
            self.birthlabel_txt.setText(li_birth[4])
            self.emaillabel_txt.setText(li_email[4])

    # def combo_btn_clicked(self, text):
    #     self.namelabel_txt.setText(self.namecombobox.itemText(text))

    def back_btn_clicked(self):
        self.close()
        back_btn_dialogs = sudo_menu(self)
        self.back_btn_dialogs.append(back_btn_dialogs)
        back_btn_dialogs.show()


#슈퍼 관리자 메뉴 - 직원 정보 수정
class sudo_menu_editmenu(QMainWindow):
    def __init__(self, parent=None):
        super(sudo_menu_editmenu, self).__init__(parent)

        con = pymysql.connect(host="192.168.0.34", user="root", password="1234", db='mydb', charset='utf8')
        cur = con.cursor()
        sql = "select name from user_info;"
        cur.execute(sql)
        data = cur.fetchall()
        li = [x[0] for x in data]
        user1 = str(li[0])
        user2 = str(li[1])
        user3 = str(li[2])
        user4 = str(li[3])
        user5 = str(li[4])

        self.mainlabel_txt = QLabel(self)
        self.mainlabel_txt.setText("· 수정할 직원 이름을 선택하세요.")
        mainlabel_txt_font = QtGui.QFont()
        mainlabel_txt_font.setPointSize(9)
        mainlabel_txt_font.setFamily("G마켓 산스 TTF Light")
        self.mainlabel_txt.setFont(mainlabel_txt_font)
        self.mainlabel_txt.setGeometry(QtCore.QRect(200, 40, 341, 41))

        self.namecombobox = QComboBox(self)
        # self.namecombobox.addItem("오종진")
        self.namecombobox.addItems([user1, user2, user3, user4, user5])
        self.namecombobox.insertSeparator(4)
        self.namecombobox.activated.connect(self.combo_change)
        self.namecombobox.setGeometry(QtCore.QRect(250, 80, 100, 30))



        # self.combo_btn = QPushButton(self)
        # self.combo_btn.setText('선택')
        # combo_btn_font = QtGui.QFont()
        # combo_btn_font.setPointSize(10)
        # combo_btn_font.setFamily("G마켓 산스 TTF Light")
        # self.combo_btn.setFont(combo_btn_font)
        # self.combo_btn.setGeometry(QtCore.QRect(320, 80, 70, 30))
        # self.combo_btn.clicked.connect(self.combo_btn_clicked)

        self.namelabel = QLabel(self)
        self.namelabel.setText("· 이름 : ")
        namelabel_font = QtGui.QFont()
        namelabel_font.setPointSize(10)
        namelabel_font.setFamily("G마켓 산스 TTF Light")
        self.namelabel.setFont(namelabel_font)
        self.namelabel.setGeometry(QtCore.QRect(300, 140, 100, 100))

        #직원 정보 수정(이름) -> 데이터베이스 연동해야함
        self.namelabel_txt = QLineEdit(self)
        self.namelabel_txt.setText("")
        namelabel_txt_font = QtGui.QFont()
        namelabel_txt_font.setPointSize(10)
        namelabel_txt_font.setFamily("G마켓 산스 TTF Light")
        self.namelabel_txt.setFont(namelabel_txt_font)
        self.namelabel_txt.setGeometry(QtCore.QRect(360, 175, 100, 30))

        self.positionlabel = QLabel(self)
        self.positionlabel.setText("· 직책 : ")
        positionlabel_font = QtGui.QFont()
        positionlabel_font.setPointSize(10)
        positionlabel_font.setFamily("G마켓 산스 TTF Light")
        self.positionlabel.setFont(positionlabel_font)
        self.positionlabel.setGeometry(QtCore.QRect(300, 180, 100, 100))

        #직원 정보 수정(직책) -> 데이터베이스 연동해야함
        self.positionlabel_txt = QComboBox(self)
        self.positionlabel_txt.addItems(["관리자", "직원"])
        positionlabel_txt_font = QtGui.QFont()
        positionlabel_txt_font.setPointSize(10)
        positionlabel_txt_font.setFamily("G마켓 산스 TTF Light")
        self.positionlabel_txt.setFont(positionlabel_txt_font)
        self.positionlabel_txt.setGeometry(QtCore.QRect(360, 215, 100, 30))

        self.idlabel = QLabel(self)
        self.idlabel.setText("· ID : ")
        idlabel_font = QtGui.QFont()
        idlabel_font.setPointSize(10)
        idlabel_font.setFamily("G마켓 산스 TTF Light")
        self.idlabel.setFont(idlabel_font)
        self.idlabel.setGeometry(QtCore.QRect(300, 220, 100, 100))

        # 직원 정보 수정(ID) -> 데이터베이스 연동해야함
        self.idlabel_txt = QLineEdit(self)
        self.idlabel_txt.setText("jjoh9923")
        idlabel_txt_font = QtGui.QFont()
        idlabel_txt_font.setPointSize(10)
        idlabel_txt_font.setFamily("G마켓 산스 TTF Light")
        self.idlabel_txt.setFont(idlabel_txt_font)
        self.idlabel_txt.setGeometry(QtCore.QRect(360, 255, 130, 30))

        self.birthlabel = QLabel(self)
        self.birthlabel.setText("· 생년월일 : ")
        birthlabel_font = QtGui.QFont()
        birthlabel_font.setPointSize(10)
        birthlabel_font.setFamily("G마켓 산스 TTF Light")
        self.birthlabel.setFont(birthlabel_font)
        self.birthlabel.setGeometry(QtCore.QRect(300, 260, 100, 100))

        # 직원 정보 수정(생년월일) -> 데이터베이스 연동해야함
        self.birthlabel_txt = QLineEdit(self)
        self.birthlabel_txt.setText("951221")
        birthlabel_txt_font = QtGui.QFont()
        birthlabel_txt_font.setPointSize(10)
        birthlabel_txt_font.setFamily("G마켓 산스 TTF Light")
        self.birthlabel_txt.setFont(birthlabel_txt_font)
        self.birthlabel_txt.setGeometry(QtCore.QRect(390, 295, 100, 30))

        self.emaillabel = QLabel(self)
        self.emaillabel.setText("· E-Mail : ")
        emaillabel_font = QtGui.QFont()
        emaillabel_font.setPointSize(10)
        emaillabel_font.setFamily("G마켓 산스 TTF Light")
        self.emaillabel.setFont(emaillabel_font)
        self.emaillabel.setGeometry(QtCore.QRect(300, 300, 100, 100))

        # 직원 정보 수정(이메일) -> 데이터베이스 연동해야함
        self.emaillabel_txt = QLineEdit(self)
        self.emaillabel_txt.setText("jjoh4803@naver.com")
        emaillabel_txt_font = QtGui.QFont()
        emaillabel_txt_font.setPointSize(10)
        emaillabel_txt_font.setFamily("G마켓 산스 TTF Light")
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
        back_btn_font.setFamily("G마켓 산스 TTF Light")
        self.back_btn.setFont(back_btn_font)
        self.back_btn.clicked.connect(self.back_btn_clicked)
        self.back_btn_dialogs = list()

        self.save_btn = QPushButton(self)
        self.save_btn.setGeometry(QtCore.QRect(250, 400, 100, 50))
        self.save_btn.setText("저장")
        save_btn_font = QtGui.QFont()
        save_btn_font.setPointSize(12)
        save_btn_font.setFamily("G마켓 산스 TTF Light")
        self.save_btn.setFont(save_btn_font)
        self.save_btn.clicked.connect(self.save_btn_clicked)
        self.save_btn_dialogs = list()

        # self.name_label = QLabel(self)
        # self.name_label.setText("")
        # self.name_label.setGeometry(QtCore.QRect(370, 100, 100, 100))

        self.setGeometry(150, 300, 610, 500)
        self.setWindowTitle('[슈퍼 관리자] 직원 정보 수정')
        self.show()

    def save_btn_clicked(self):
        con = pymysql.connect(host="192.168.0.34", user="root", password="1234", db='mydb', charset='utf8')

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

        save_btn_dialogs = editalarm_window(self)
        self.save_btn_dialogs.append(save_btn_dialogs)
        save_btn_dialogs.show()

    def back_btn_clicked(self):
        self.close()
        back_btn_dialogs = sudo_menu(self)
        self.back_btn_dialogs.append(back_btn_dialogs)
        back_btn_dialogs.show()

    def combo_change(self, text):
        con = pymysql.connect(host="192.168.0.34", user="root", password="1234", db='mydb', charset='utf8')

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

        if self.namecombobox.currentText() == '한민경':
            self.namelabel_txt.setText(str(li_name[0]))
            # self.positionlabel_txt.setText(str(li_position[0]))
            self.idlabel_txt.setText(str(li_id[0]))
            self.birthlabel_txt.setText(str(li_birth[0]))
            self.emaillabel_txt.setText(str(li_email[0]))

            if li_position[0] == 'employee':
                self.positionlabel_txt.setCurrentText("직원")
            else:
                self.positionlabel_txt.setCurrentText("관리자")

        if self.namecombobox.currentText() == '오종진':
            self.namelabel_txt.setText(li_name[1])
            # self.positionlabel_txt.setText(li_position[1])
            self.idlabel_txt.setText(li_id[1])
            self.birthlabel_txt.setText(li_birth[1])
            self.emaillabel_txt.setText(li_email[1])

            if li_position[1] == 'employee':
                self.positionlabel_txt.setCurrentText("직원")
            else:
                self.positionlabel_txt.setCurrentText("관리자")

        if self.namecombobox.currentText() == '조아람':
            self.namelabel_txt.setText(li_name[2])
            #self.positionlabel_txt.setText(li_position[2])
            self.idlabel_txt.setText(li_id[2])
            self.birthlabel_txt.setText(li_birth[2])
            self.emaillabel_txt.setText(li_email[2])

            if li_position[2] == 'employee':
                self.positionlabel_txt.setCurrentText("직원")
            else:
                self.positionlabel_txt.setCurrentText("관리자")

        if self.namecombobox.currentText() == '문은오':
            self.namelabel_txt.setText(li_name[3])
            #self.positionlabel_txt.setText(li_position[3])
            self.idlabel_txt.setText(li_id[3])
            self.birthlabel_txt.setText(li_birth[3])
            self.emaillabel_txt.setText(li_email[3])

            if li_position[3] == 'employee':
                self.positionlabel_txt.setCurrentText("직원")
            else:
                self.positionlabel_txt.setCurrentText("관리자")

        if self.namecombobox.currentText() == '장승주':
            self.namelabel_txt.setText(li_name[4])
            #self.positionlabel_txt.setText(li_position[4])
            self.idlabel_txt.setText(li_id[4])
            self.birthlabel_txt.setText(li_birth[4])
            self.emaillabel_txt.setText(li_email[4])

            if li_position[4] == 'employee':
                self.positionlabel_txt.setCurrentText("직원")
            else:
                self.positionlabel_txt.setCurrentText("관리자")

    # def combo_btn_clicked(self, text):
    #     self.namelabel_txt.setText(self.namecombobox.itemText(text))


#수정 확인 알림창
class editalarm_window(QMainWindow):
    def __init__(self, parent=None):
        super(editalarm_window, self).__init__(parent)

        self.mainlabel_txt = QLabel(self)
        self.mainlabel_txt.setText("수정되었습니다.")
        mainlabel_txt_font = QtGui.QFont()
        mainlabel_txt_font.setPointSize(9)
        mainlabel_txt_font.setFamily("G마켓 산스 TTF Light")
        self.mainlabel_txt.setFont(mainlabel_txt_font)
        self.mainlabel_txt.setGeometry(QtCore.QRect(100, 50, 141, 41))

        self.accept_btn = QPushButton(self)
        self.accept_btn.setText('확인')
        accept_btn_font = QtGui.QFont()
        accept_btn_font.setPointSize(10)
        accept_btn_font.setFamily("G마켓 산스 TTF Light")
        self.accept_btn.setFont(accept_btn_font)
        self.accept_btn.setGeometry(QtCore.QRect(120, 150, 70, 30))
        self.accept_btn.clicked.connect(self.accept_btn_clicked)
        self.accept_btn_dialogs = list()

        self.setGeometry(300, 450, 300, 200)
        self.setWindowTitle('알림')
        self.show()

    def accept_btn_clicked(self):
        self.close()


#슈퍼 관리자 메뉴 - 관리자/직원 삭제
class sudo_menu_deletemenu(QMainWindow):
    def __init__(self, parent=None):
        super(sudo_menu_deletemenu, self).__init__(parent)

        con = pymysql.connect(host="192.168.0.34", user="root", password="1234", db='mydb', charset='utf8')
        cur = con.cursor()
        sql = "select name from user_info;"
        cur.execute(sql)
        data = cur.fetchall()
        li = [x[0] for x in data]
        user1 = str(li[0])
        user2 = str(li[1])
        user3 = str(li[2])
        user4 = str(li[3])
        user5 = str(li[4])

        self.mainlabel_txt = QLabel(self)
        self.mainlabel_txt.setText("· 삭제할 직원 이름을 선택하세요.")
        mainlabel_txt_font = QtGui.QFont()
        mainlabel_txt_font.setPointSize(9)
        mainlabel_txt_font.setFamily("G마켓 산스 TTF Light")
        self.mainlabel_txt.setFont(mainlabel_txt_font)
        self.mainlabel_txt.setGeometry(QtCore.QRect(200, 170, 341, 41))

        self.namecombobox = QComboBox(self)
        # self.namecombobox.addItem("오종진")
        self.namecombobox.addItems([user1, user2, user3, user4, user5])
        self.namecombobox.insertSeparator(4)
        self.namecombobox.activated.connect(self.combo_change)
        self.namecombobox.setGeometry(QtCore.QRect(200, 210, 101, 30))

        self.combo_btn = QPushButton(self)
        self.combo_btn.setText('선택')
        combo_btn_font = QtGui.QFont()
        combo_btn_font.setPointSize(10)
        combo_btn_font.setFamily("G마켓 산스 TTF Light")
        self.combo_btn.setFont(combo_btn_font)
        self.combo_btn.setGeometry(QtCore.QRect(320, 210, 70, 30))
        self.combo_btn.clicked.connect(self.combo_btn_clicked)
        self.combo_btn_dialogs = list()

        self.back_btn = QPushButton(self)
        self.back_btn.setGeometry(QtCore.QRect(0, 0, 80, 52))
        self.back_btn.setText("뒤로가기")
        back_btn_font = QtGui.QFont()
        back_btn_font.setPointSize(10)
        back_btn_font.setFamily("G마켓 산스 TTF Light")
        self.back_btn.setFont(back_btn_font)
        self.back_btn.clicked.connect(self.back_btn_clicked)
        self.back_btn_dialogs = list()

        self.setGeometry(150, 300, 610, 500)
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

#삭제 확인 알림창
class deletealarm_window(QMainWindow):
    def __init__(self, parent=None):
        super(deletealarm_window, self).__init__(parent)

        self.mainlabel_txt = QLabel(self)
        self.mainlabel_txt.setText("삭제되었습니다.")
        mainlabel_txt_font = QtGui.QFont()
        mainlabel_txt_font.setPointSize(9)
        mainlabel_txt_font.setFamily("G마켓 산스 TTF Light")
        self.mainlabel_txt.setFont(mainlabel_txt_font)
        self.mainlabel_txt.setGeometry(QtCore.QRect(100, 50, 141, 41))

        self.accept_btn = QPushButton(self)
        self.accept_btn.setText('확인')
        accept_btn_font = QtGui.QFont()
        accept_btn_font.setPointSize(10)
        accept_btn_font.setFamily("G마켓 산스 TTF Light")
        self.accept_btn.setFont(accept_btn_font)
        self.accept_btn.setGeometry(QtCore.QRect(120, 150, 70, 30))
        self.accept_btn.clicked.connect(self.accept_btn_clicked)
        self.accept_btn_dialogs = list()

        self.setGeometry(300, 450, 300, 200)
        self.setWindowTitle('알림')
        self.show()

    def accept_btn_clicked(self, event):
        self.close()


#테스트 메인 화면
class First(QMainWindow):
    def __init__(self, parent=None):
        super(First, self).__init__(parent)

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

        self.send_btn.clicked.connect(self.send_btn_clicked)

        self.database_btn.clicked.connect(self.database_btn_clicked)

        self.sudo_btn.clicked.connect(self.sudo_btn_clicked)
        self.sudo_btn_dialogs = list()

        self.manager_btn.clicked.connect(self.manager_btn_clicked)
        self.manager_btn_dialogs = list()

        self.staff_btn.clicked.connect(self.staff_btn_clicked)
        self.staff_btn_dialogs = list()

        self.setGeometry(150, 300, 610, 500)
        self.setWindowTitle('스마트 팩토리')
        self.show()

    def send_btn_clicked(self):
        now = time.localtime()
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((HOST, PORT))
        msg = self.input_text.text()
        s.send(msg.encode(encoding='utf_8', errors='strict'))

        data = s.recv(1024)
        self.send_txtB.append("%04d/%02d/%02d %02d:%02d:%02d" % (now.tm_year, now.tm_mon, now.tm_mday, now.tm_hour,
                                                                 now.tm_min, now.tm_sec)
 + "\n송신 : " + msg + "\n")
        # self.send_txtB.adjustSize()
        self.recv_txtB.append("%04d/%02d/%02d %02d:%02d:%02d" % (now.tm_year, now.tm_mon, now.tm_mday, now.tm_hour,
                                                                 now.tm_min, now.tm_sec)
 + "\n수신 : " + str(data) + "\n")
        # print('수신 데이터 : ' + data.decode('utf_8'))
        s.close()

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

    def database_btn_clicked(self):
        # 데이터베이스 연동 테스트
        # msg = self.input_text.text()
        # self.send_txtB.append('송신 : ' + msg)

        con = pymysql.connect(host="192.168.0.34", user="root", password="1234", db='mydb', charset='utf8')
        cur = con.cursor()
        sql = "select name from user_info;"
        cur.execute(sql)
        data = cur.fetchall()
        li = [x[0] for x in data]
        self.recv_txtB.append(str(li) + '\n')




def main():

    app = QApplication(sys.argv)
    main1 = First()
    main1.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
