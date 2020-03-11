#!/usr/bin/env python
# -*- coding: utf-8 -*-
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5 import uic
from PyQt5 import QtWidgets, QtGui
from PyQt5 import QtGui, QtCore
import sys
import socket

HOST = '192.168.0.144'
PORT = 8888


class sudo_menu(QMainWindow):
    def __init__(self, parent=None):
        super(sudo_menu, self).__init__(parent)
        self.setGeometry(350, 350, 600, 500)
        self.setWindowTitle('Second Page')
        self.show()


class First(QMainWindow):
    def __init__(self, parent=None):
        super(First, self).__init__(parent)

    # def initUI(self):
        self.input_text = QLineEdit(self)
        self.input_text.resize(300, 30)

        send_btn = QPushButton(self)
        send_btn.setText('보내기')
        send_btn.resize(70, 30)

        sudo_btn = QPushButton(self)
        sudo_btn.setText('슈퍼 관리자 메뉴')
        sudo_btn.resize(160, 150)

        manager_btn = QPushButton(self)
        manager_btn.setText('관리자 메뉴')
        manager_btn.resize(160, 150)

        staff_btn = QPushButton(self)
        staff_btn.setText('직원 메뉴')
        staff_btn.resize(160, 150)

        send_txt = QLabel(self)
        send_txt.setText('송신')

        recv_txt = QLabel(self)
        recv_txt.setText('수신')

        send_txtB = QTextBrowser(self)
        send_txtB.resize(250, 150)

        recv_txtB = QTextBrowser(self)
        recv_txtB.resize(250, 150)

        self.input_text.move(25, 25)
        send_btn.move(350, 25)
        sudo_btn.move(25, 100)
        manager_btn.move(220, 100)
        staff_btn.move(415, 100)
        send_txt.move(130, 270)
        recv_txt.move(430, 270)
        send_txtB.move(25, 300)
        recv_txtB.move(325, 300)

        send_btn.clicked.connect(self.send_btn_clicked)

        sudo_btn.clicked.connect(self.sudo_btn_clicked)
        sudo_btn_dialogs = list()

        manager_btn.clicked.connect(self.manager_btn_clicked)
        manager_btn_dialogs = list()

        self.setGeometry(150, 300, 610, 500)
        self.setWindowTitle('Testtt.py')
        self.show()

    def send_btn_clicked(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((HOST, PORT))
        msg = self.input_text()
        s.send(msg.encode(encoding='utf_8', errors='strict'))

        data = s.recv(1024)
        # self.send_txtB.setText("' " + self.send_txt.text() + " '")
        # self.send_txtB.adjustSize()
        # self.recv_txtB.setText("' " + data + " '")
        print('수신 데이터 : ' + data.decode('utf_8'))

    def sudo_btn_clicked(self):
        self.close()
        sudo_btn_dialogs = sudo_menu(self)
        self.sudo_btn_dialogs.append(sudo_btn_dialogs)
        sudo_btn_dialogs.show()

    def manager_btn_clicked(self):
        self.close()
        sudo_btn_dialogs = sudo_menu(self)
        self.sudo_btn_dialogs.append(sudo_btn_dialogs)
        sudo_btn_dialogs.show()


def main():

    app = QApplication(sys.argv)
    main1 = First()
    main1.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
