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


class manager_menu(QMainWindow):
    def __init__(self, parent=None):
        super(manager_menu, self).__init__(parent)


class sudo_menu(QMainWindow):
    def __init__(self, parent=None):
        super(sudo_menu, self).__init__(parent)

        self.mainlabel_txt = QLabel(self)
        self.mainlabel_txt.setText("슈퍼 유저 메뉴")
        # self.mainlabel_txt.setFixedSize(1180, 512)

        self.mainlabel_txt.move(130, 80)

        self.setGeometry(150, 300, 610, 500)
        self.setWindowTitle('슈퍼 관리자 메뉴')
        self.show()


class First(QMainWindow):
    def __init__(self, parent=None):
        super(First, self).__init__(parent)

    # def initUI(self):
        self.input_text = QLineEdit(self)
        self.input_text.resize(300, 30)

        self.send_btn = QPushButton(self)
        self.send_btn.setText('보내기')
        self.send_btn.resize(70, 30)

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
        self.sudo_btn.move(25, 100)
        self.manager_btn.move(220, 100)
        self.staff_btn.move(415, 100)
        self.send_txt.move(130, 270)
        self.recv_txt.move(430, 270)
        self.send_txtB.move(25, 300)
        self.recv_txtB.move(325, 300)

        self.send_btn.clicked.connect(self.send_btn_clicked)

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
        self.send_txtB.append("%04d/%02d/%02d %02d:%02d:%02d" % (now.tm_year, now.tm_mon, now.tm_mday, now.tm_hour, now.tm_min, now.tm_sec)
 + "\n송신 : " + msg + "\n")
        # self.send_txtB.adjustSize()
        self.recv_txtB.append("%04d/%02d/%02d %02d:%02d:%02d" % (now.tm_year, now.tm_mon, now.tm_mday, now.tm_hour, now.tm_min, now.tm_sec)
 + "\n수신 : " + str(data) + "\n")
        # print('수신 데이터 : ' + data.decode('utf_8'))
        s.close()


    def sudo_btn_clicked(self):
        # self.close()
        # sudo_btn_dialogs = sudo_menu(self)
        # self.sudo_btn_dialogs.append(sudo_btn_dialogs)
        # sudo_btn_dialogs.show()

        #그냥 해본거
        msg = self.input_text.text()
        self.send_txtB.setText('송신 : ' + msg)

        con = pymysql.connect(host="192.168.0.2", user="root", password="1541", db='db1', charset='utf8')
        cur = con.cursor()
        # curs = con.cursor()
        sql = "select distinct name from goods;"
        cur.execute(sql)
        # con.commit()
        data = cur.fetchone()
        # data1 = curs.fetchone()
        # self.recv_txtB.setText(str(cur.execute(sql)))
        self.recv_txtB.setText('이름 : ' + str(data[0]))


    def manager_btn_clicked(self):
        self.close()
        manager_btn_dialogs = manager_menu(self)
        self.sudo_btn_dialogs.append(manager_btn_dialogs)
        manager_btn_dialogs.show()


    def staff_btn_clicked(self):
        self.close()


def main():

    app = QApplication(sys.argv)
    main1 = First()
    main1.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
