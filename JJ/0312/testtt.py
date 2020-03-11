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

        self.sales_btn = QPushButton(self)
        self.sales_btn.setText('매출 확인')
        sales_btn_font = QtGui.QFont()
        sales_btn_font.setPointSize(20)
        sales_btn_font.setFamily("G마켓 산스 TTF Light")
        self.sales_btn.setFont(sales_btn_font)
        self.sales_btn.setGeometry(QtCore.QRect(30, 330, 150, 150))

        self.control_btn = QPushButton(self)
        self.control_btn.setText('공장 제어')
        control_btn_font = QtGui.QFont()
        control_btn_font.setPointSize(18)
        control_btn_font.setFamily("G마켓 산스 TTF Light")
        self.control_btn.setFont(control_btn_font)
        self.control_btn.setGeometry(QtCore.QRect(230, 150, 150, 150))

        self.management_btn = QPushButton(self)
        self.management_btn.setText('직원 관리')
        management_btn_font = QtGui.QFont()
        management_btn_font.setPointSize(18)
        management_btn_font.setFamily("G마켓 산스 TTF Light")
        self.management_btn.setFont(management_btn_font)
        self.management_btn.setGeometry(QtCore.QRect(230, 330, 150, 150))

        self.stock_btn = QPushButton(self)
        self.stock_btn.setText('재고 관리')
        stock_btn_font = QtGui.QFont()
        stock_btn_font.setPointSize(18)
        stock_btn_font.setFamily("G마켓 산스 TTF Light")
        self.stock_btn.setFont(stock_btn_font)
        self.stock_btn.setGeometry(QtCore.QRect(430, 150, 150, 150))

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
        self.setWindowTitle('관리자 메뉴')
        self.show()

    def logout_btn_clicked(self):
        self.close()
        logout_btn_dialogs = First(self)
        self.logout_btn_dialogs.append(logout_btn_dialogs)
        logout_btn_dialogs.show()


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

    def logout_btn_clicked(self):
        self.close()
        logout_btn_dialogs = First(self)
        self.logout_btn_dialogs.append(logout_btn_dialogs)
        logout_btn_dialogs.show()


#슈퍼 관리자 메뉴 - 직원 확인
class sudo_menu_searchmenu(QMainWindow):
    def __init__(self, parent=None):
        super(sudo_menu_searchmenu, self).__init__(parent)

        self.mainlabel_txt = QLabel(self)
        self.mainlabel_txt.setText("· 확인할 직원 이름을 선택하세요.")
        mainlabel_txt_font = QtGui.QFont()
        mainlabel_txt_font.setPointSize(9)
        mainlabel_txt_font.setFamily("G마켓 산스 TTF Light")
        self.mainlabel_txt.setFont(mainlabel_txt_font)
        self.mainlabel_txt.setGeometry(QtCore.QRect(200, 40, 341, 41))

        self.namecombobox = QComboBox(self)
        # self.namecombobox.addItem("오종진")
        self.namecombobox.addItems(["한민경", "문은오", "장승주", "오종진", "조아람"])
        self.namecombobox.insertSeparator(4)
        self.namecombobox.activated.connect(self.combo_change)
        self.namecombobox.setGeometry(QtCore.QRect(200, 80, 101, 30))

        self.combo_btn = QPushButton(self)
        self.combo_btn.setText('선택')
        combo_btn_font = QtGui.QFont()
        combo_btn_font.setPointSize(10)
        combo_btn_font.setFamily("G마켓 산스 TTF Light")
        self.combo_btn.setFont(combo_btn_font)
        self.combo_btn.setGeometry(QtCore.QRect(320, 80, 70, 30))
        self.combo_btn.clicked.connect(self.combo_btn_clicked)

        self.namelabel_txt = QLabel(self)
        self.namelabel_txt.setText("· 이름 : ")
        namelabel_txt_font = QtGui.QFont()
        namelabel_txt_font.setPointSize(10)
        namelabel_txt_font.setFamily("G마켓 산스 TTF Light")
        self.namelabel_txt.setFont(namelabel_txt_font)
        self.namelabel_txt.setGeometry(QtCore.QRect(300, 140, 100, 100))

        self.namelabel_txt = QLabel(self)
        self.namelabel_txt.setText("")
        namelabel_txt_font = QtGui.QFont()
        namelabel_txt_font.setPointSize(10)
        namelabel_txt_font.setFamily("G마켓 산스 TTF Light")
        self.namelabel_txt.setFont(namelabel_txt_font)
        self.namelabel_txt.setGeometry(QtCore.QRect(360, 140, 100, 100))

        self.positionlabel_txt = QLabel(self)
        self.positionlabel_txt.setText("· 직책 : ")
        positionlabel_txt_font = QtGui.QFont()
        positionlabel_txt_font.setPointSize(10)
        positionlabel_txt_font.setFamily("G마켓 산스 TTF Light")
        self.positionlabel_txt.setFont(positionlabel_txt_font)
        self.positionlabel_txt.setGeometry(QtCore.QRect(300, 180, 100, 100))

        self.idlabel_txt = QLabel(self)
        self.idlabel_txt.setText("· ID : ")
        idlabel_txt_font = QtGui.QFont()
        idlabel_txt_font.setPointSize(10)
        idlabel_txt_font.setFamily("G마켓 산스 TTF Light")
        self.idlabel_txt.setFont(idlabel_txt_font)
        self.idlabel_txt.setGeometry(QtCore.QRect(300, 220, 100, 100))

        self.birthlabel_txt = QLabel(self)
        self.birthlabel_txt.setText("· 생년월일 : ")
        birthlabel_txt_font = QtGui.QFont()
        birthlabel_txt_font.setPointSize(10)
        birthlabel_txt_font.setFamily("G마켓 산스 TTF Light")
        self.birthlabel_txt.setFont(birthlabel_txt_font)
        self.birthlabel_txt.setGeometry(QtCore.QRect(300, 260, 100, 100))

        self.emaillabel_txt = QLabel(self)
        self.emaillabel_txt.setText("· E-Mail : ")
        emaillabel_txt_font = QtGui.QFont()
        emaillabel_txt_font.setPointSize(10)
        emaillabel_txt_font.setFamily("G마켓 산스 TTF Light")
        self.emaillabel_txt.setFont(emaillabel_txt_font)
        self.emaillabel_txt.setGeometry(QtCore.QRect(300, 300, 100, 100))



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

        self.name_label = QLabel(self)
        self.name_label.setText("")
        self.name_label.setGeometry(QtCore.QRect(370, 100, 100, 100))

        self.setGeometry(150, 300, 610, 500)
        self.setWindowTitle('[슈퍼 관리자] 직원 확인')
        self.show()

    #콤보박스 선택시 레이블 변경
    def combo_change(self, text):
        # self.name_label.setText(self.namecombobox.itemData(text))
        name_label_font = QtGui.QFont()
        name_label_font.setPointSize(10)
        name_label_font.setFamily("G마켓 산스 TTF Light")
        self.name_label.setFont(name_label_font)
        self.namelabel_txt.setText(self.namecombobox.itemText(text))
        # print(self.namecombobox.itemText(text))

    def combo_btn_clicked(self, text):
        self.namelabel_txt.setText(self.namecombobox.itemText(text))


    def back_btn_clicked(self):
        self.close()
        back_btn_dialogs = sudo_menu(self)
        self.back_btn_dialogs.append(back_btn_dialogs)
        back_btn_dialogs.show()

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
        msg = self.input_text.text()
        self.send_txtB.append('송신 : ' + msg)

        con = pymysql.connect(host="192.168.0.2", user="root", password="123321", db='mydb', charset='utf_8')
        cur = con.cursor()
        # curs = con.cursor()
        sql = "select distinct name from goods;"
        cur.execute(sql)
        # con.commit()
        data = cur.fetchone()
        # data1 = curs.fetchone()
        # self.recv_txtB.setText(str(cur.execute(sql)))
        self.recv_txtB.append('이름 : ' + str(data[0]))


def main():

    app = QApplication(sys.argv)
    main1 = First()
    main1.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
