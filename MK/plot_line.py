# -*- coding: utf-8 -*-

import sys
import self as self
from PyQt5.QtWidgets import QHBoxLayout, QDialog, QApplication
from matplotlib.backends.backend_template import FigureCanvas
from numpy import nan as NA
import pandas as pd
import numpy as np
from pandas import Series, DataFrame
import matplotlib.pyplot as plt
import pymysql

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

class MainDialog(QDialog):
    def __init__(self):
        QDialog.__init__(self, None)

        fig = plt.figure()

        ax = fig.add_subplot(1, 1, 1)

        # data = DataFrame(np.random.rand(30), columns=['col'])

        ax.set_title('test')
        ax.set_xlabel('x')
        ax.set_ylabel('y')

        con = pymysql.connect(host="192.168.0.34", user="root", password="1234", db='mydb', charset='utf8')
        cur = con.cursor()
        sql = "select inventory*unitprice from pro_info WHERE idproducts = '1'";
        cur.execute(sql)
        data = cur.fetchone()
        price1 = data[0]
        ax.plot(data[0])

        sql = "select inventory*unitprice from pro_info WHERE idproducts = '2'";
        cur.execute(sql)
        data = cur.fetchone()
        price2 = data[0]
        ax.plot(data[0])

        sql = "select inventory*unitprice from pro_info WHERE idproducts = '3'";
        cur.execute(sql)
        data = cur.fetchone()
        price3 = data[0]
        ax.plot(data[0])

        sql = "select inventory*unitprice from pro_info WHERE idproducts = '4'";
        cur.execute(sql)
        data = cur.fetchone()
        price4 = data[0]
        ax.plot(data[0])


        ax.set_xticks([price1, price2, price3, price4])
        ax.set_xticklabels(['one', 'two', 'three', 'four'], rotation=30, fontsize=7)

        # ax.set_ylim([0, 1.5])

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