import pyautogui
import sys
import os
import numpy as np
from numpy import loadtxt
from os.path import exists
from os import makedirs
from math import floor
from PyQt5.QtGui import QColor, QFont, QKeySequence, QFontInfo, QPalette
from numpy import random, zeros, ones, concatenate
import xlrd
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from PyQt5.QtWidgets import QApplication, QDialog, QMainWindow, QMessageBox, QTableWidgetItem, QHBoxLayout
from PyQt5.uic import loadUi
from PyQt5 import QtCore
from PyQt5.QtCore import QTimer, Qt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

class MainMenu(QMainWindow):
    def __init__(self, parent = None):
        super().__init__(parent)
        
        loadUi("./main.ui", self) 
        self.label_2.setAlignment(Qt.AlignCenter)
        self.label_3.setAlignment(Qt.AlignCenter)
        self.label_4.setAlignment(Qt.AlignCenter)
        self.label_5.setAlignment(Qt.AlignCenter)
        self.label_6.setAlignment(Qt.AlignCenter)
        self.label_7.setAlignment(Qt.AlignCenter)
        self.label_8.setAlignment(Qt.AlignCenter)
        self.label_9.setAlignment(Qt.AlignCenter)
        self.label_10.setAlignment(Qt.AlignCenter)
        self.label_11.setAlignment(Qt.AlignCenter)
        self.label_12.setAlignment(Qt.AlignCenter)
        self.label_13.setAlignment(Qt.AlignCenter)
        self.label_14.setAlignment(Qt.AlignCenter)
        self.label_15.setAlignment(Qt.AlignCenter)
        self.label_16.setAlignment(Qt.AlignCenter)
        self.label_17.setAlignment(Qt.AlignCenter)
        self.label_18.setAlignment(Qt.AlignCenter)
        self.label_25.setAlignment(Qt.AlignCenter)
        self.label_26.setAlignment(Qt.AlignCenter)
        self.label_27.setAlignment(Qt.AlignCenter)
        self.label_28.setAlignment(Qt.AlignCenter)
        self.label_29.setAlignment(Qt.AlignCenter)
        self.label_30.setAlignment(Qt.AlignCenter)
        self.label_31.setAlignment(Qt.AlignCenter)
        self.label_32.setAlignment(Qt.AlignCenter)
        self.label_33.setAlignment(Qt.AlignCenter)
        self.label_34.setAlignment(Qt.AlignCenter)
        self.label_35.setAlignment(Qt.AlignCenter)
        self.label_36.setAlignment(Qt.AlignCenter)
        self.label_37.setAlignment(Qt.AlignCenter)
        self.label_38.setAlignment(Qt.AlignCenter)
        self.label_39.setAlignment(Qt.AlignCenter)
        self.label_40.setAlignment(Qt.AlignCenter)
        self.label_41.setAlignment(Qt.AlignCenter)
        self.label_42.setAlignment(Qt.AlignCenter)
        self.label_43.setAlignment(Qt.AlignCenter)
        self.label_44.setAlignment(Qt.AlignCenter)
        self.label_45.setAlignment(Qt.AlignCenter)
        self.label_46.setAlignment(Qt.AlignCenter)
        
        tabBar=self.tabWidget.tabBar()
        tabBar.setDocumentMode(True)
        tabBar.setExpanding(True)
        self.entry1.setStyleSheet("border:2px solid black;")
        self.entry2.setStyleSheet("border:2px solid black;")
        self.entry3.setStyleSheet("border:2px solid black;")
        self.entry4.setStyleSheet("border:2px solid black;")
        self.entry5.setStyleSheet("border:2px solid black;")
        self.entry6.setStyleSheet("border:2px solid black;")
        self.entry7.setStyleSheet("border:2px solid black;")
        self.submit1.setStyleSheet('background-color:rgb(211, 211, 211)')
        self.submit2.setStyleSheet('background-color:rgb(211, 211, 211)')
        self.submit3.setStyleSheet('background-color:rgb(211, 211, 211)')
        self.submit4.setStyleSheet('background-color:rgb(211, 211, 211)')
        self.submit5.setStyleSheet('background-color:rgb(211, 211, 211)')
        waterlayout=QHBoxLayout(self.waterlevel)
        canvas=FigureCanvas(Figure(figsize=(5,4)))
        waterlayout.addWidget(canvas)
        canvas.figure.set_facecolor("#08008B")
        ax=canvas.figure.subplots()
        ax.set_title("Water Level Variation (Last 24 Hours)", color="#FFFFFF", fontdict={'family' : 'Tahoma', 'weight' : 'bold', 'size' : 30})
        ax.set_xlabel("Time [Hours past]", color="#FFFFFF", fontdict={'family' : 'Tahoma', 'size' : 26}) 
        ax.set_ylabel("Variation in Water Level [cm]", color="#FFFFFF", fontdict={'family' : 'Tahoma', 'size' : 26})
        ax.grid()
        ax.set_facecolor("#AEEAFF")
        ax.tick_params(labelcolor="#FFFFFF",labelsize=20)
        self.time=np.array([24,22,20,18,16,14,12,10,8,6,4,2,0])
        self.var=np.array([1,2,1.4,2.4,3.3,-1,-2.2,-2.3,-2.2,-3.4,-1.5,-0.5,1])
        self.ref=np.array([0,0,0,0,0,0,0,0,0,0,0,0,0])
        ax.plot(self.time,self.var,label= "Variation")
        ax.plot(self.time,self.ref,label="Reference Water Level",linestyle='dashed',linewidth='5')
        ax.legend(prop={"size":20})
        ax.set_xlim([0, 24])
        ax.set_xticks([0,2,4,6,8,10,12,14,16,18,20,22,24])
        ax.set_xticklabels(['24','22','20','18','16','14','12','10','8','6','4','2','0'])
app = QApplication(sys.argv)
window = MainMenu()
window.show()
app.exec()