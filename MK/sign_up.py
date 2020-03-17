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
import pymysql
from openpyxl import Workbook
from openpyxl import load_workbook


#회원가입
class Ui_sign_up_MainWindow(object):
    def setupUi(self, sign_up_MainWindow):
        sign_up_MainWindow.setObjectName("sign_up_MainWindow")
        sign_up_MainWindow.resize(800, 601)
        self.centralwidget = QtWidgets.QWidget(sign_up_MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.sign_up_title_label = QtWidgets.QLabel(self.centralwidget)
        self.sign_up_title_label.setGeometry(QtCore.QRect(320, 20, 141, 91))
        font = QtGui.QFont()
        font.setPointSize(20)
        font.setBold(True)
        font.setWeight(75)
        self.sign_up_title_label.setFont(font)
        self.sign_up_title_label.setAlignment(QtCore.Qt.AlignCenter)
        self.sign_up_title_label.setObjectName("sign_up_title_label")
        self.sign_up_groupBox = QtWidgets.QGroupBox(self.centralwidget)
        self.sign_up_groupBox.setGeometry(QtCore.QRect(120, 100, 571, 361))
        font = QtGui.QFont()
        font.setPointSize(15)
        self.sign_up_groupBox.setFont(font)
        self.sign_up_groupBox.setObjectName("sign_up_groupBox")
        self.sign_up_name_label = QtWidgets.QLabel(self.sign_up_groupBox)
        self.sign_up_name_label.setGeometry(QtCore.QRect(90, 50, 81, 21))
        self.sign_up_name_label.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignTrailing | QtCore.Qt.AlignVCenter)
        self.sign_up_name_label.setObjectName("sign_up_name_label")
        self.sign_up_name_textEdit = QtWidgets.QTextEdit(self.sign_up_groupBox)
        self.sign_up_name_textEdit.setGeometry(QtCore.QRect(210, 40, 251, 41))
        self.sign_up_name_textEdit.setObjectName("sign_up_name_textEdit")

        self.sign_up_id_label = QtWidgets.QLabel(self.sign_up_groupBox)
        self.sign_up_id_label.setGeometry(QtCore.QRect(90, 100, 81, 21))
        self.sign_up_id_label.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignTrailing | QtCore.Qt.AlignVCenter)
        self.sign_up_id_label.setObjectName("sign_up_id_label")
        self.sign_up_id_textEdit = QtWidgets.QTextEdit(self.sign_up_groupBox)
        self.sign_up_id_textEdit.setGeometry(QtCore.QRect(210, 90, 251, 41))
        self.sign_up_id_textEdit.setObjectName("sign_up_id_textEdit")

        self.sign_up_pw_label = QtWidgets.QLabel(self.sign_up_groupBox)
        self.sign_up_pw_label.setGeometry(QtCore.QRect(40, 150, 141, 21))
        self.sign_up_pw_label.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignTrailing | QtCore.Qt.AlignVCenter)
        self.sign_up_pw_label.setObjectName("sign_up_pw_label")
        self.sign_up_pw_textEdit = QtWidgets.QTextEdit(self.sign_up_groupBox)
        self.sign_up_pw_textEdit.setGeometry(QtCore.QRect(210, 140, 251, 41))
        self.sign_up_pw_textEdit.setObjectName("sign_up_pw_textEdit")

        self.sign_up_email_label = QtWidgets.QLabel(self.sign_up_groupBox)
        self.sign_up_email_label.setGeometry(QtCore.QRect(40, 200, 141, 21))
        self.sign_up_email_label.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignTrailing | QtCore.Qt.AlignVCenter)
        self.sign_up_email_textEdit = QtWidgets.QTextEdit(self.sign_up_groupBox)
        self.sign_up_email_textEdit.setGeometry(QtCore.QRect(210, 190, 251, 41))
        self.sign_up_email_textEdit.setObjectName("sign_up_email_textEdit")

        self.sign_up_birth_label = QtWidgets.QLabel(self.sign_up_groupBox)
        self.sign_up_birth_label.setGeometry(QtCore.QRect(50, 250, 131, 21))
        self.sign_up_birth_label.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignTrailing | QtCore.Qt.AlignVCenter)
        self.sign_up_birth_label.setObjectName("sign_up_birth_label")
        self.dateEdit = QtWidgets.QDateEdit(self.sign_up_groupBox)
        self.dateEdit.setGeometry(QtCore.QRect(210, 240, 251, 41))
        self.dateEdit.setObjectName("dateEdit")

        self.sign_up_pos_label = QtWidgets.QLabel(self.sign_up_groupBox)
        self.sign_up_pos_label.setGeometry(QtCore.QRect(100, 300, 81, 21))
        self.sign_up_pos_label.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignTrailing | QtCore.Qt.AlignVCenter)
        self.sign_up_pos_label.setObjectName("sign_up_pos_label")

        self.sign_up_man_radio = QtWidgets.QRadioButton(self.sign_up_groupBox)
        self.sign_up_man_radio.setGeometry(QtCore.QRect(210, 290, 131, 31))
        self.sign_up_man_radio.setObjectName("sign_up_man_radio")
        self.sign_up_emp_radio = QtWidgets.QRadioButton(self.sign_up_groupBox)
        self.sign_up_emp_radio.setGeometry(QtCore.QRect(350, 290, 141, 31))
        self.sign_up_emp_radio.setObjectName("sign_up_emp_radio")

        self.sign_up_back_pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.sign_up_back_pushButton.setGeometry(QtCore.QRect(652, 20, 111, 41))
        self.sign_up_back_pushButton.setObjectName("sign_up_back_pushButton")
        self.sign_up_ok_pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.sign_up_ok_pushButton.setGeometry(QtCore.QRect(582, 497, 111, 41))
        self.sign_up_ok_pushButton.setObjectName("sign_up_ok_pushButton")
        sign_up_MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(sign_up_MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 26))
        self.menubar.setObjectName("menubar")
        sign_up_MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(sign_up_MainWindow)
        self.statusbar.setObjectName("statusbar")
        sign_up_MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(sign_up_MainWindow)
        QtCore.QMetaObject.connectSlotsByName(sign_up_MainWindow)

    def retranslateUi(self, sign_up_MainWindow):
        _translate = QtCore.QCoreApplication.translate
        sign_up_MainWindow.setWindowTitle(_translate("sign_up_MainWindow", "MainWindow"))
        self.sign_up_title_label.setText(_translate("sign_up_MainWindow", "회원가입"))
        self.sign_up_groupBox.setTitle(_translate("sign_up_MainWindow", "회원 정보 입력"))
        self.sign_up_name_label.setText(_translate("sign_up_MainWindow", "이름 :"))
        self.sign_up_id_label.setText(_translate("sign_up_MainWindow", "ID :"))
        self.sign_up_pw_label.setText(_translate("sign_up_MainWindow", "Password : "))
        self.sign_up_email_label.setText(_translate("sign_up_MainWindow", "Email : "))
        self.sign_up_birth_label.setText(_translate("sign_up_MainWindow", "생년월일 : "))
        self.sign_up_pos_label.setText(_translate("sign_up_MainWindow", "직책 : "))
        self.sign_up_man_radio.setText(_translate("sign_up_MainWindow", "Manager"))
        self.sign_up_emp_radio.setText(_translate("sign_up_MainWindow", "Employee"))
        self.sign_up_back_pushButton.setText(_translate("sign_up_MainWindow", "BACK"))
        self.sign_up_ok_pushButton.setText(_translate("sign_up_MainWindow", "OK"))
        self.sign_up_ok_pushButton.clicked.connect(self.sign_up_ok_pushButton_clicked)

    def insert_test(self):
        try:
            self.input_name = self.sign_up_name_textEdit.toPlainText()
            self.input_id = self.sign_up_id_textEdit.toPlainText()
            self.input_pw = self.sign_up_pw_textEdit.toPlainText()
            self.input_email = self.sign_up_email_textEdit.toPlainText()
            self.input_birth = self.dateEdit.text()

            if self.sign_up_emp_radio.isChecked():
                self.input_pos = "1"
            elif self.sign_up_man_radio.isChecked():
                self.input_pos = "2"
            else:
                self.input_pos = "1"

            conn = pymysql.connect(host="192.168.0.19", user="root", password="1234", db="mydb", charset="utf8", autocommit=True)
            curs = conn.cursor()
            sql = "insert into user_info (name, id, pw, email, birth, position) values (%s, %s, %s, %s, %s, %s)"
            curs.execute(sql, (self.input_name, self.input_id, self.input_pw, self.input_email, self.input_birth, self.input_pos))

        except:
            QMessageBox.information(self, "올바른 형식으로 입력하세요.", QMessageBox.Yes)
        finally:
            conn.close()



    def sign_up_ok_pushButton_clicked(self):
        self.insert_test()
        self.accept()

if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    sign_up_MainWindow = QtWidgets.QMainWindow()
    ui = Ui_sign_up_MainWindow()
    ui.setupUi(sign_up_MainWindow)
    sign_up_MainWindow.show()
    sys.exit(app.exec_())