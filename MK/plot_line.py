# -*- coding: utf-8 -*-
import sys
from PyQt5.QtWidgets import QHBoxLayout, QDialog, QApplication
from matplotlib.backends.backend_template import FigureCanvas
import matplotlib.pyplot as plt
import pymysql
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

class MainDialog(QDialog):
    def __init__(self):
        QDialog.__init__(self, None)
        fig = plt.figure()
        ax = fig.add_subplot(1, 1, 1)

        con = pymysql.connect(host="192.168.0.19", user="root", password="1234", db='mydb', charset='utf8')
        cur = con.cursor()

        sql = "select inventory*unitprice from pro_info WHERE idproducts = '1'";
        cur.execute(sql)
        data = cur.fetchone()
        price1 = data[0]

        sql = "select inventory*unitprice from pro_info WHERE idproducts = '2'";
        cur.execute(sql)
        data = cur.fetchone()
        price2 = data[0]

        sql = "select inventory*unitprice from pro_info WHERE idproducts = '3'";
        cur.execute(sql)
        data = cur.fetchone()
        price3 = data[0]

        sql = "select inventory*unitprice from pro_info WHERE idproducts = '4'";
        cur.execute(sql)
        data = cur.fetchone()
        price4 = data[0]

        ax.set_title('inventory * priceN')
        ax.set_xlabel('N')
        ax.set_ylabel('result', rotation=0)
        ax.plot(['price1', 'price3', 'price2', 'price4'], [price1, price3, price2, price4])

        canvas = FigureCanvas(fig)
        canvas.draw()

        lay = QHBoxLayout()
        self.setLayout(lay)
        lay.addWidget(canvas)
        canvas.show()

app = QApplication(sys.argv)
main_dialog = MainDialog()
main_dialog.show()
app.exec_()