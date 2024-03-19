import pyautogui
import sys
import os
import requests
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
from resize import worker
from math import floor

class MainMenu(QMainWindow):
    def __init__(self, parent = None):
        super().__init__(parent)
        
        w,h=pyautogui.size()
        
        
        temp=["./main.ui", "2736x1824",str(w)+"x"+str(h),"./mainadj.ui"]
        obj = worker(temp)
        obj.primary()
        loadUi("./mainadj.ui", self) 

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
        self.label_48.setAlignment(Qt.AlignCenter)
        self.label_49.setAlignment(Qt.AlignCenter)
        self.label_50.setAlignment(Qt.AlignCenter)
        self.label_51.setAlignment(Qt.AlignCenter)
        self.label_52.setAlignment(Qt.AlignCenter)
        self.label_53.setAlignment(Qt.AlignCenter)
        self.label_54.setAlignment(Qt.AlignCenter)
        self.label_55.setAlignment(Qt.AlignCenter)
        self.label_56.setAlignment(Qt.AlignCenter)
        self.label_57.setAlignment(Qt.AlignCenter)
        self.label_58.setAlignment(Qt.AlignCenter)
        self.label_59.setAlignment(Qt.AlignCenter)
        self.label_60.setAlignment(Qt.AlignCenter)
        self.label_61.setAlignment(Qt.AlignCenter)
        self.label_62.setAlignment(Qt.AlignCenter)
        self.label_63.setAlignment(Qt.AlignCenter)
        self.label_64.setAlignment(Qt.AlignCenter)
       
        
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
        ax.set_title("Water Level Variation (Last 24 Hours)", color="#FFFFFF", fontdict={'family' : 'Tahoma', 'weight' : 'bold', 'size' : floor(30*(h/1800))})
        ax.set_xlabel("Time [Hours past]", color="#FFFFFF", fontdict={'family' : 'Tahoma', 'size' : floor(26*(h/1800))}) 
        ax.set_ylabel("Variation in Water Level [cm]", color="#FFFFFF", fontdict={'family' : 'Tahoma', 'size' : floor(26*(h/1800))})
        ax.grid()
        ax.set_facecolor("#AEEAFF")
        ax.tick_params(labelcolor="#FFFFFF",labelsize=floor(20*(h/1800)))
        self.time=np.array([24,22,20,18,16,14,12,10,8,6,4,2,0])
        self.var=np.array([1,2,1.4,2.4,3.3,-1,-2.2,-2.3,-2.2,-3.4,-1.5,-0.5,1])
        self.ref=np.array([0,0,0,0,0,0,0,0,0,0,0,0,0])
        ax.plot(self.time,self.var,label= "Variation")
        ax.plot(self.time,self.ref,label="Reference Water Level",linestyle='dashed',linewidth='5')
        ax.legend(prop={"size":floor(20*(h/1800))})
        ax.set_xlim([0, 24])
        ax.set_xticks([0,2,4,6,8,10,12,14,16,18,20,22,24])
        ax.set_xticklabels(['24','22','20','18','16','14','12','10','8','6','4','2','0'])
        self.label_45.setText("Calibration")
        self.label_18.setText("Calibration")
        self.label_64.setText("Calibration")
        self.label_38.setText("0")
        self.label_57.setText("0")
        self.label_11.setText("0")
        self.label_12.setText("0")
        self.label_39.setText("0")
        self.label_58.setText("0")
        self.submit1.clicked.connect(self.updateMode)
        self.submit5.clicked.connect(self.updatetempres)
        self.submit4.clicked.connect(self.updatefreq)
        batterylayout=QHBoxLayout(self.batterylevel)
        canvas=FigureCanvas(Figure(figsize=(5,4)))
        batterylayout.addWidget(canvas)
        canvas.figure.set_facecolor("#D9DDDC")
        ax=canvas.figure.subplots()
        ax.set_title("Battery Level (Last 24 Hours)", color="#000000", fontdict={'family' : 'Tahoma', 'weight' : 'bold', 'size' : floor(30*(h/1800))})
        ax.set_xlabel("Time [Hours past]", color="#000000", fontdict={'family' : 'Tahoma', 'size' : floor(26*(h/1800))}) 
        ax.set_ylabel("Battery Level [%]", color="#000000", fontdict={'family' : 'Tahoma', 'size' : floor(26*(h/1800))})
        ax.grid()
        ax.set_facecolor("#D9DDDC")
        ax.tick_params(labelcolor="#000000",labelsize=floor(20*(h/1800)))
        self.time=np.array([24,22,20,18,16,14,12,10,8,6,4,2,0])
        self.var=np.array([80,90,92,87,88,85,86,90,83,87,83,79,75])
        self.good=np.array([90,90,90,90,90,90,90,90,90,90,90,90,90])
        self.bad=np.array([15,15,15,15,15,15,15,15,15,15,15,15,15])
        ax.plot(self.time,self.var,label= "Level",linewidth='7',color='black')
        ax.plot(self.time,self.good,label="Good",linestyle='dashed',linewidth='5',color='green')
        ax.plot(self.time,self.bad,label="Bad",linestyle='dashed',linewidth='5',color='red')
        ax.legend(prop={"size":floor(20*(h/1800))})
        ax.set_xlim([0, 24])
        ax.set_xticks([0,2,4,6,8,10,12,14,16,18,20,22,24])
        ax.set_xticklabels(['24','22','20','18','16','14','12','10','8','6','4','2','0'])

        templayout=QHBoxLayout(self.temp)
        canvas=FigureCanvas(Figure(figsize=(5,4)))
        templayout.addWidget(canvas)
        canvas.figure.set_facecolor("#D9DDDC")
        ax=canvas.figure.subplots()
        ax.set_title("System Temperature (Last 24 Hours)", color="#000000", fontdict={'family' : 'Tahoma', 'weight' : 'bold', 'size' : floor(30*(h/1800))})
        ax.set_xlabel("Time [Hours past]", color="#000000", fontdict={'family' : 'Tahoma', 'size' : floor(26*(h/1800))}) 
        ax.set_ylabel("System Temperature [C]", color="#000000", fontdict={'family' : 'Tahoma', 'size' : floor(26*(h/1800))})
        ax.grid()
        ax.set_facecolor("#D9DDDC")
        ax.tick_params(labelcolor="#000000",labelsize=floor(20*(h/1800)))
        self.time=np.array([24,22,20,18,16,14,12,10,8,6,4,2,0])
        self.var=np.array([20.2,22.5,23.6,25.8,23.9,21,19,18.4,17,16.4,18.9,22,25.7])
        self.good=np.array([40,40,40,40,40,40,40,40,40,40,40,40,40])
        self.bad=np.array([-30,-30,-30,-30,-30,-30,-30,-30,-30,-30,-30,-30,-30])
        ax.plot(self.time,self.var,label= "Temperature",linewidth='7',color='black')
        ax.plot(self.time,self.good,label="Upper Limit",linestyle='dashed',linewidth='5',color='red')
        ax.plot(self.time,self.bad,label="Lower Limit",linestyle='dashed',linewidth='5',color="#82EEFD")
        ax.legend(prop={"size":floor(20*(h/1800))})
        ax.set_xlim([0, 24])
        ax.set_xticks([0,2,4,6,8,10,12,14,16,18,20,22,24])
        ax.set_xticklabels(['24','22','20','18','16','14','12','10','8','6','4','2','0'])
        self.label_17.setText("0 - 40")
        self.label_44.setText("0 - 40")
        self.label_63.setText("0 - 40")
        self.submit2.clicked.connect(self.updateeangle)
        self.label_16.setText("0 - 40")
        self.label_43.setText("0 - 40")
        self.label_62.setText("0 - 40")
        self.submit3.clicked.connect(self.updateaangle)
        self.submit6.clicked.connect(self.updatemultiple)
        



    def updateaangle(self):
        self.mina= self.entry4.text()
        self.maxa= self.entry5.text()
        try:
            float(self.mina)
            self.change5=True
        except:    
            self.change5=False
        try:
            float(self.maxa)
            self.change6=True
        except:    
            self.change6=False

        if (self.change4==False or self.change6==False):    
            QMessageBox.critical(self,"Error","invalid input")
            self.entry4.setText("")
            self.entry5.setText("")
        else:
            if ((self.mina>=self.maxa)or(self.maxa<0)or(self.mina<0)):    
                QMessageBox.critical(self,"Error","invalid input")
                self.entry4.setText("")
                self.entry5.setText("")
            else:
                self.label_16.setText(self.mina+" - "+self.maxa)
                self.label_43.setText(self.mina+" - "+self.maxa)
                self.label_62.setText(self.mina+" - "+self.maxa)
                self.entry4.setText("")
                self.entry5.setText("")
                self.send_MT('az='+self.mina+','+self.maxa)
        
                

    def updateeangle(self):
        self.mine= self.entry2.text()
        self.maxe= self.entry3.text()
        try:
            float(self.mine)
            self.change3=True
        except:    
            self.change3=False
        try:
            float(self.maxe)
            self.change4=True
        except:    
            self.change4=False

        if (self.change3==False or self.change4==False):    
            QMessageBox.critical(self,"Error","invalid input")
            self.entry2.setText("")
            self.entry3.setText("")
        else:
            if ((self.mine>self.maxe)or (self.mine<0)or (self.maxe<0)):    
                QMessageBox.critical(self,"Error","invalid input")
                self.entry2.setText("")
                self.entry3.setText("")
            else:
                self.label_17.setText(self.mine+" - "+self.maxe)
                self.label_44.setText(self.mine+" - "+self.maxe)
                self.label_63.setText(self.mine+" - "+self.maxe)
                self.entry2.setText("")
                self.entry3.setText("")
                self.send_MT('el='+self.mine+','+self.maxe)

    def updatetempres(self):
        self.tempres= self.entry7.text()
        try:
            float(self.tempres)
            self.change=True
        except:    
            self.change=False

        if ((self.change==False)or(self.tempres<0)):    
            QMessageBox.critical(self,"Error","invalid input")
            self.entry7.setText("")
        else:
            self.label_38.setText(self.tempres)
            self.label_57.setText(self.tempres)
            self.label_11.setText(self.tempres)
            self.entry7.setText("")
            self.send_MT('tres='+self.tempres)


    def updatefreq(self):
        self.freq= self.entry6.text()
        try:
            float(self.freq)
            self.change2=True
        except:    
            self.change2=False

        if ((self.change2==False)or (self.freq<0)):    
            QMessageBox.critical(self,"Error","invalid input")
            self.entry6.setText("")
        else:
            self.label_12.setText(self.freq)
            self.label_39.setText(self.freq)
            self.label_58.setText(self.freq)
            self.entry6.setText("")
            self.send_MT('sf='+self.freq)

    def updateMode(self):
        self.mode= self.entry1.text()
        if not (self.mode == "Calibration" or self.mode== "Normal"):
            QMessageBox.critical(self,"Error","invalid input")
            self.entry1.setText("")
        else:
            self.label_18.setText(self.mode)
            self.label_45.setText(self.mode)
            self.label_64.setText(self.mode)
            self.send_MT('mode='+self.mode)

    def updatemultiple(self):
        try:
            float(self.entry1.text())
            self.c1=True
        except:    
            self.c1=False
        try:
            float(self.entry2.text())
            self.c2=True
        except:    
            self.c2=False
        try:
            float(self.entry3.text())
            self.c3=True
        except:    
            self.c3=False
        try:
            float(self.entry4.text())
            self.c4=True
        except:    
            self.c4=False
        try:
            float(self.entry5.text())
            self.c5=True
        except:    
            self.c5=False
        try:
            float(self.entry6.text())
            self.c6=True
        except:    
            self.c6=False
        try:
            float(self.entry7.text())
            self.c7=True
        except:    
            self.c7=False

        if ((self.c1)or(self.c2)or(self.c3)or(self.c4)or(self.c5)or(self.c6)or(self.c7)):    
            QMessageBox.critical(self,"Error","invalid input")
            self.entry6.setText("")
            
        if ((self.entry1.text()=="")and(self.entry2.text()=="")and(self.entry4.text()=="")and(self.entry6.text()=="")and(self.entry7.text()=="")):
            print("Missing Input")
        elif ((self.entry1.text()=="")and(self.entry2.text()=="")and(self.entry4.text()=="")and(self.entry6.text()=="")):
            self.send_MT('tres='+self.entry7.text())
        elif ((self.entry1.text()=="")and(self.entry2.text()=="")and(self.entry4.text()=="")and(self.entry7.text()=="")):
            self.send_MT('sf='+self.entry6.text()) 
        elif ((self.entry1.text()=="")and(self.entry2.text()=="")and(self.entry6.text()=="")and(self.entry7.text()=="")):
            self.send_MT('az='+self.entry4.text()+','+self.entry5.text())
        elif ((self.entry1.text()=="")and(self.entry4.text()=="")and(self.entry6.text()=="")and(self.entry7.text()=="")):
            self.send_MT('el='+self.entry2.text()+','+self.entry3.text()) 
        elif ((self.entry2.text()=="")and(self.entry4.text()=="")and(self.entry6.text()=="")and(self.entry7.text()=="")):
            self.send_MT('mode='+self.entry1.text()) 
        elif ((self.entry4.text()=="")and(self.entry6.text()=="")and(self.entry7.text()=="")):
            self.send_MT('mode='+self.entry1.text()+';'+'el='+self.entry2.text()+','+self.entry3.text())
        elif ((self.entry2.text()=="")and(self.entry6.text()=="")and(self.entry7.text()=="")):
            self.send_MT('mode='+self.entry1.text()+';'+'az='+self.entry4.text()+','+self.entry5.text())
        elif ((self.entry2.text()=="")and(self.entry4.text()=="")and(self.entry7.text()=="")):
            self.send_MT('mode='+self.entry1.text()+';'+'sf='+self.entry6.text())
        elif ((self.entry2.text()=="")and(self.entry4.text()=="")and(self.entry6.text()=="")):
            self.send_MT('mode='+self.entry1.text()+';'+'tres='+self.entry7.text())
        elif ((self.entry1.text()=="")and(self.entry6.text()=="")and(self.entry7.text()=="")):
            self.send_MT('el='+self.entry2.text()+','+self.entry3.text()+';'+'az='+self.entry4.text()+','+self.entry5.text())
        elif ((self.entry1.text()=="")and(self.entry4.text()=="")and(self.entry7.text()=="")):
            self.send_MT('el='+self.entry2.text()+','+self.entry3.text()+';'+'fs='+self.entry6.text())
        elif ((self.entry1.text()=="")and(self.entry4.text()=="")and(self.entry6.text()=="")):
            self.send_MT('el='+self.entry2.text()+','+self.entry3.text()+';'+'tres='+self.entry7.text())
        elif ((self.entry1.text()=="")and(self.entry2.text()=="")and(self.entry7.text()=="")):
            self.send_MT('az='+self.entry4.text()+','+self.entry5.text()+';'+'sf='+self.entry6.text())
        elif ((self.entry1.text()=="")and(self.entry2.text()=="")and(self.entry6.text()=="")):
            self.send_MT('az='+self.entry4.text()+','+self.entry5.text()+';'+'tres='+self.entry7.text())
        elif ((self.entry1.text()=="")and(self.entry2.text()=="")and(self.entry4.text()=="")):
            self.send_MT('sf='+self.entry6.text()+';'+'tres='+self.entry7.text())
        elif ((self.entry6.text()=="")and(self.entry7.text()=="")):
            self.send_MT('mode='+self.entry1.text()+';'+'el='+self.entry2.text()+','+self.entry3.text()+';'+'az='+self.entry4.text()+','+self.entry5.text())
        elif ((self.entry4.text()=="")and(self.entry7.text()=="")):
            self.send_MT('mode='+self.entry1.text()+';'+'el='+self.entry2.text()+','+self.entry3.text()+';'+'sf='+self.entry6.text())
        elif ((self.entry4.text()=="")and(self.entry6.text()=="")):
            self.send_MT('mode='+self.entry1.text()+';'+'el='+self.entry2.text()+','+self.entry3.text()+';'+'tres='+self.entry7.text())
        elif ((self.entry2.text()=="")and(self.entry7.text()=="")):
            self.send_MT('mode='+self.entry1.text()+';'+'az='+self.entry4.text()+','+self.entry5.text()+';'+'sf='+self.entry6.text())
        elif ((self.entry2.text()=="")and(self.entry6.text()=="")):
            self.send_MT('mode='+self.entry1.text()+';'+'az='+self.entry4.text()+','+self.entry5.text()+';'+'tres='+self.entry7.text())
        elif ((self.entry1.text()=="")and(self.entry7.text()=="")):
            self.send_MT('el='+self.entry2.text()+','+self.entry3.text()+';'+'az='+self.entry4.text()+','+self.entry5.text()+';'+'sf='+self.entry6.text())
        elif ((self.entry1.text()=="")and(self.entry6.text()=="")):
            self.send_MT('el='+self.entry2.text()+','+self.entry3.text()+';'+'az='+self.entry4.text()+','+self.entry5.text()+';'+'tres='+self.entry7.text())
        elif ((self.entry1.text()=="")and(self.entry2.text()=="")):
            self.send_MT('az='+self.entry4.text()+','+self.entry5.text()+';'+'sf='+self.entry6.text()+';'+'tres='+self.entry7.text())
        elif(self.entry1.text()==""):
            self.send_MT('el='+self.entry2.text()+','+self.entry3.text()+';'+'az='+self.entry4.text()+','+self.entry5.text()+';'+'sf='+self.entry6.text()+';'+'tres='+self.entry7.text())
        elif(self.entry2.text()==""):
            self.send_MT('mode='+self.entry1.text()+';'+'az='+self.entry4.text()+','+self.entry5.text()+';'+'sf='+self.entry6.text()+';'+'tres='+self.entry7.text())
        elif(self.entry3.text()==""):
            self.send_MT('mode='+self.entry1.text()+';'+'el='+self.entry2.text()+','+self.entry3.text()+';'+'sf='+self.entry6.text()+';'+'tres='+self.entry7.text())
        elif(self.entry4.text()==""):
            self.send_MT('mode='+self.entry1.text()+';'+'el='+self.entry2.text()+','+self.entry3.text()+';'+'az='+self.entry4.text()+','+self.entry5.text()+';'+'tres='+self.entry7.text())
        elif(self.entry5.text()==""):
            self.send_MT('mode='+self.entry1.text()+';'+'el='+self.entry2.text()+','+self.entry3.text()+';'+'az='+self.entry4.text()+','+self.entry5.text()+';'+'sf='+self.entry6.text())
        else:
            self.send_MT('mode='+self.entry1.text()+';'+'el='+self.entry2.text()+','+self.entry3.text()+';'+'az='+self.entry4.text()+','+self.entry5.text()+';'+'sf='+self.entry6.text()+';'+'tres='+self.entry7.text())

    def send_MT(self,message):
        # function to send MT (mobile-terminated) message to RockBlock using HTTP Post endpoint
        # (i.e. to send from ground station to on-site system)

        # in terminal before running: python -m pip install requests

        # query parameters
        # it would be a good idea to have these as inputs at the beginning so a different user could set up their RockBlock with our code
        imei = "300434068462010"
        username1 = "max.feinland%40colorado.edu"
        username2 = "max.feinland@colorado.edu" # this is just how they did the RockBlock example code I'm not sure why
        password = "Velociraptor"

        # convert user input to hex (this is required by RockBlock)
        ascii_bytes = message.encode('ascii')
        hex_list = [format(byte, '02x') for byte in ascii_bytes]
        msg_hex = ''
        for n in range(len(hex_list)):
            msg_hex = msg_hex+hex_list[n]

        # url format required by RockBlock
        url = 'https://rockblock.rock7.com/rockblock/MT?imei=300434068462010&username='+username1+'&username='+username2+'&password='+password+'&data='+msg_hex

        headers = {"accept": "text/plain"} # also how they did the RockBlock example code
        # Response body will be list of values separated by commas
        # first value: status ("OK" or "FAILED")
        # if status "OK":
        # second value: mtId (mobile-terminated identfier)
        # if status "FAILED"
        # second value: integer error code
        # third value: error code text description
        response = requests.post(url, headers=headers)
        print(response.text)

        

app = QApplication(sys.argv)
window = MainMenu()
window.show()
app.exec()
