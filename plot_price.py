# -*- coding: utf-8 -*-

import sys
import numpy as np
import matplotlib.pyplot as plt

import PyQt5
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

from PyQt5.QtWidgets import QApplication, QHBoxLayout, QDialog
import pymysql
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

class MainDialog(QDialog):


    def __init__(self):
        QDialog.__init__(self, None)

        con = pymysql.connect(host="192.168.0.34", user="root", password="1234", db='mydb', charset='utf8')
        cur = con.cursor()
        sql = "select distinct unitprice from pro_info WHERE idproducts = '1'";
        cur.execute(sql)
        data = cur.fetchone()
        price1 = data[0]

        sql = "select distinct unitprice from pro_info WHERE idproducts = '2'";
        cur.execute(sql)
        data = cur.fetchone()
        price2 = data[0]

        sql = "select distinct unitprice from pro_info WHERE idproducts = '3'";
        cur.execute(sql)
        data = cur.fetchone()
        price3 = data[0]

        sql = "select distinct unitprice from pro_info WHERE idproducts = '4'";
        cur.execute(sql)
        data = cur.fetchone()
        price4 = data[0]

        sql = "select distinct unitprice from pro_info WHERE idproducts = '5'";
        cur.execute(sql)
        data = cur.fetchone()
        price5 = data[0]

        N = 5
        value = (price1, price2, price3, price4, price5)
        ind = np.arange(N)
        width = 0.35


        fig = plt.Figure()

        ax = fig.add_subplot(111)
        # ax.set_ylim([0,100])
        ax.bar(ind, value, width)
        ax.set_xticks(ind + width / 20)
        ax.set_xticklabels(['price1', 'price2', 'price3', 'price4', 'price5'])


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
