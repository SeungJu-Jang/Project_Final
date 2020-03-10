import sys
import socket
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5 import uic
from PyQt5 import QtWidgets, QtGui

# main_ui = uic.loadUiType('_uiFiles/main.ui')[0]

HOST = '192.168.0.144'
PORT = 8888


class SuperdoApp(QMainWindow):
    def __init__(self, parent=None):
        super(SuperdoApp, self).__init__(parent)

        # 창 띄우는 부분
        # # self.setLayout(vbox)
        # self.setWindowTitle('버틍')
        # self.setGeometry(500, 500, 400, 400)
        # self.show()


class MyApp(QWidget):
    def __init__(self, parent=None):
        super(MyApp, self).__init__(parent)
        self.initUI()

    def initUI(self):
        # 버튼 누를때 작동
        btn = QPushButton(self)
        btn.setText('보내기')
        # 버튼 클릭하면 label이 변경되어야 한다.
        btn.clicked.connect(self.on_click)

        btn2 = QPushButton(self)
        btn2.setText('슈퍼 관리자 메뉴')
        btn2.clicked.connect(self.on_click2)

        btn3 = QPushButton(self)
        btn3.setText('관리자 메뉴')
        btn3.clicked.connect(self.on_click3)

        btn4 = QPushButton(self)
        btn4.setText('직원 메뉴')
        btn4.clicked.connect(self.on_click4)

        # LineEdit선언부, 입력 부분
        self.qle = QLineEdit(self)
        # Lable선언, 결과값 출력 예정
        self.lbl = QTextBrowser(self)
        self.lbl2 = QTextBrowser(self)

        windowExampe = QtWidgets.QWidget()
        lable1 = QtWidgets.QLabel(windowExampe)
        lable2 = QtWidgets.QLabel(windowExampe)

        lable1.setText('                송신')
        lable2.setText('                수신')

        # layout 설정
        vbox = QGridLayout()
        vbox.addWidget(self.qle, 0, 0, 1, 2)
        vbox.addWidget(btn, 1, 0, 1, 0)
        vbox.addWidget(btn2, 2, 0, 1, 0)
        vbox.addWidget(btn3, 3, 0, 1, 0)
        vbox.addWidget(btn4, 4, 0, 1, 0)
        # vbox.addWidget()
        vbox.addWidget(lable1, 6, 0)
        vbox.addWidget(lable2, 6, 1)
        vbox.addWidget(self.lbl, 7, 0)
        vbox.addWidget(self.lbl2, 7, 1)

        # 창 띄우는 부분
        self.setLayout(vbox)
        self.setWindowTitle('ProtoType')
        self.setGeometry(500, 400, 400, 400)
        self.show()

    def on_click(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((HOST, PORT))
        msg = self.qle.text()

        s.send(msg.encode(encoding='utf_8', errors='strict'))
        # data = s.recv(1024)

        if msg == 'exit':
            print('Program Close!')
            s.close()

        self.lbl.setText('결과 : ' + self.qle.text())
        self.lbl.adjustSize()
        # self.lbl2.setText('결과 : ' + data.decode('utf_8'))

    def on_click2(self):
        dialog = SuperdoApp(self)
        self.dialogs.appen(dialog)
        dialog.show()

    def on_click3(self):
        print("Manager Menu")

    def on_click4(self):
        print("Staff Menu")


def main():
    app = QApplication(sys.argv)
    main = MyApp()
    main.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()

# if __name__ == '__main__':
#     app = QApplication(sys.argv)
#     ex = MyApp()
#     sys.exit(app.exec_())
# app = QApplication(sys.argv)
# mywindow = MyApp()
# mywindow.show()
# app.exec_()