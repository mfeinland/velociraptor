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
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from PyQt5.QtWidgets import QApplication, QDialog, QMainWindow, QMessageBox, QTableWidgetItem, QHBoxLayout
from PyQt5.uic import loadUi
from PyQt5 import QtCore
from PyQt5.QtCore import QTimer, Qt, QThread
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from resize import worker
from math import floor
import pyrebase
from shapely.geometry import Point
import numpy
import geopandas as gpd
import time
from refl_zones import *
import fiona
from fastkml import kml
class MainMenu(QMainWindow):
    def __init__(self, parent = None):
        super().__init__(parent)
        
        self.w,self.h=pyautogui.size()
        
        
        temp=["./main.ui", "2736x1824",str(self.w)+"x"+str(self.h),"./mainadj.ui"]
        obj = worker(temp)
        obj.primary()
        loadUi("./mainadj.ui", self) 
        scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']
        credentials = ServiceAccountCredentials.from_json_keyfile_name('velociraptor-credentials.json', scope)
        self.client = gspread.authorize(credentials)
        
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
        self.label_67.setAlignment(Qt.AlignCenter)
        self.label_69.setAlignment(Qt.AlignCenter)
        self.box1.addItem('yes')
        self.box1.addItem('no')
        self.box3.addItem('yes')
        self.box3.addItem('no')
        self.box4.addItem('yes')
        self.box4.addItem('no')
        self.box5.addItem('yes')
        self.box5.addItem('no')
        self.box6.addItem('yes')
        self.box6.addItem('no')
        self.box2.addItem('5,10,15')
        self.box2.addItem('5,10,15,20,25')
        self.box2.addItem('5,7,10,12')
        self.box2.addItem('5,6,7')
        self.box2.addItem('10,15,20')
        self.box2.addItem('5,7,10')
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
        self.entry8.setStyleSheet("border:2px solid black;")
        self.entry9.setStyleSheet("border:2px solid black;")
        self.entry10.setStyleSheet("border:2px solid black;")
        self.entry11.setStyleSheet("border:2px solid black;")
        self.entry12.setStyleSheet("border:2px solid black;")
        self.entry20.setStyleSheet("border:2px solid black;")
        self.entry23.setStyleSheet("border:2px solid black;")
        self.entry24.setStyleSheet("border:2px solid black;")
        self.entry25.setStyleSheet("border:2px solid black;")
        self.entry26.setStyleSheet("border:2px solid black;")
        self.entry27.setStyleSheet("border:2px solid black;")
        self.box1.setStyleSheet("border:2px solid black;")
        self.box2.setStyleSheet("border:2px solid black;")
        self.box3.setStyleSheet("border:2px solid black;")
        self.box4.setStyleSheet("border:2px solid black;")
        self.box5.setStyleSheet("border:2px solid black;")
        self.box6.setStyleSheet("border:2px solid black;")
        
        self.submit1.setStyleSheet('background-color:rgb(211, 211, 211)')
        self.submit2.setStyleSheet('background-color:rgb(211, 211, 211)')
        self.submit3.setStyleSheet('background-color:rgb(211, 211, 211)')
        self.submit4.setStyleSheet('background-color:rgb(211, 211, 211)')
        self.submit5.setStyleSheet('background-color:rgb(211, 211, 211)')
        self.submit6.setStyleSheet('background-color:rgb(211, 211, 211)')
        self.submit7.setStyleSheet('background-color:rgb(211, 211, 211)')

       
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
        self.submit7.clicked.connect(self.reflections)
    
        
        
        self.label_17.setText("0 - 40")
        self.label_44.setText("0 - 40")
        self.label_63.setText("0 - 40")
        self.label_40.setText("NA")
        self.label_13.setText("NA")
        self.label_59.setText("NA")
        self.submit2.clicked.connect(self.updateeangle)
        self.label_16.setText("0 - 40")
        self.label_43.setText("0 - 40")
        self.label_62.setText("0 - 40")
        self.submit3.clicked.connect(self.updateaangle)
        self.submit6.clicked.connect(self.updatemultiple)
        config = {
        "apiKey": "AIzaSyBWn7Bslp1EdKc7JIRQgj5rJSf9frRDXmk",
        "authDomain": "velociraptor-74d11.firebaseapp.com",
        "databaseURL": "https://velociraptor-74d11-default-rtdb.firebaseio.com",
        "storageBucket": "velociraptor-74d11.appspot.com",
        #"serviceAccount": "velociraptor-74d11-firebase-adminsdk-jz0st-6782bdf95a.json"
        }
        self.index=1
        firebase = pyrebase.initialize_app(config)
        self.db = firebase.database()
        self.waterthread = QThread()
        self.tempthread = QThread()
        self.batterythread = QThread()
        templayout=QHBoxLayout(self.temp)
        canvas=FigureCanvas(Figure(figsize=(5,4)))
        templayout.addWidget(canvas)
        canvas.figure.set_facecolor("#D9DDDC")
        self.ax1=canvas.figure.subplots()
        

        waterlayout=QHBoxLayout(self.waterlevel)
        canvas=FigureCanvas(Figure(figsize=(5,4)))
        waterlayout.addWidget(canvas)
        canvas.figure.set_facecolor("#08008B")
        self.ax2=canvas.figure.subplots()
        
        batterylayout=QHBoxLayout(self.batterylevel)
        canvas=FigureCanvas(Figure(figsize=(5,4)))
        batterylayout.addWidget(canvas)
        canvas.figure.set_facecolor("#D9DDDC")
        self.ax3=canvas.figure.subplots()
        self.updatelat()
        self.updatelon()
        self.plotwater2()
        self.plottemp()
        self.plotbattery()
        self.filltable()
        self.waterthread.Timer = QTimer()
        self.waterthread.Timer.timeout.connect(self.plotwater)
        self.waterthread.Timer.start(7200000)
        self.tempthread.Timer = QTimer()
        self.tempthread.Timer.timeout.connect(self.plottemp)
        self.tempthread.Timer.start(7200000)
        self.batterythread.Timer = QTimer()
        self.batterythread.Timer.timeout.connect(self.plotbattery)
        self.batterythread.Timer.start(7200000)
    
    def filltable(self):
    
        self.gettranstime()
        self.table.setRowCount(len(self.water1))
        for x in range(len(self.water1)-1)
            item=QTableWidgetItem(self.timevar[x+1])
            self.table.setItem(x,0,item)
            item=QTableWidgetItem(self.batteryvar[x+1])
            self.table.setItem(x,1,item)
            item=QTableWidgetItem(self.tempvar[x+1])
            self.table.setItem(x,2,item)
            item=QTableWidgetItem(self.water1[x+1])
            self.table.setItem(x,3,item)
            item=QTableWidgetItem(self.water2[x+1])
            self.table.setItem(x,4,item)
    def reflections(self):
        freq=int(self.entry20.text())
        h=int(self.entry23.text())
        lat=int(self.entry26.text())
        lng=int(self.entry27.text())
        az1=int(self.entry24.text())
        az2=int(self.entry25.text())
        self.ellist()
        el_list=self.el
        print(str(el_list))
        make_FZ_kml('plot.kml',freq, el_list.tolist(), h, lat,lng, az1, az2)
        kml_file = 'plot.kml'
        fiona.drvsupport.supported_drivers['KML']='rw'
        polys=gpd.read_file(kml_file,driver='KML')
        print(polys)
        polys.plot()
        plt.savefig('test.jpg')

    
    def ellist(self):
        sele=self.box2.currentText()
        if sele=='5.10.15':
            self.el=numpy.array([5,10,15])
        elif sele=='5,10,15,20,25':
            self.el=numpy.array([5,10,15,20,25])
        elif sele=='5,7,10,12':
            self.el=numpy.array([5,7,10,12])
        elif sele=='5,6,7':
            self.el=numpy.array([5,6,7])
        elif sele=='10,15,20':
            self.el=numpy.array([10,15,20])
        elif sele=='5,7,10':
            self.el=numpy.array([5,7,10])
    def updatelat(self):   
        self.getlat()
        self.lat=self.lat[-1]
        self.label_61.setText(str(self.lat))
        self.label_42.setText(str(self.lat))
        self.label_15.setText(str(self.lat))
    def updatelon(self):   
        self.getlon()
        self.lon=self.lon[-2]
        self.label_60.setText(str(self.lon))
        self.label_41.setText(str(self.lon))
        self.label_14.setText(str(self.lon))
    def getlat(self):
        llDataSheet = self.client.open_by_url('https://docs.google.com/spreadsheets/d/1EDDa4DHF1ftID2VA9OQd_-QNtpyfb0WKxmtn8omho_E/edit#gid=0')
        llWorksheet = llDataSheet.worksheet('Sheet1')
        llMsgs = llWorksheet.get_all_values()
        self.lat=llMsgs[-1]

    def getlon(self):
        llDataSheet = self.client.open_by_url('https://docs.google.com/spreadsheets/d/1EDDa4DHF1ftID2VA9OQd_-QNtpyfb0WKxmtn8omho_E/edit#gid=0')
        llWorksheet = llDataSheet.worksheet('Sheet1')
        llMsgs = llWorksheet.get_all_values()
        self.lon=llMsgs[-1]
    def getwater(self):
        heightDataSheet = self.client.open_by_url('https://docs.google.com/spreadsheets/d/1wwkYuqRS5Lbr8krs7bAPIwdCNHBLG5ABYQpDBhBmhVs/edit#gid=117241294')
        heightWorksheet = heightDataSheet.worksheet('reflheights')
        self.water1= heightWorksheet.col_values(2)
        heightDataSheet = self.client.open_by_url('https://docs.google.com/spreadsheets/d/1wwkYuqRS5Lbr8krs7bAPIwdCNHBLG5ABYQpDBhBmhVs/edit#gid=117241294')
        heightWorksheet = heightDataSheet.worksheet('reflheights')
        self.water2 = heightWorksheet.col_values(3)

        self.watervar=self.water1+self.water2
        self.watervar[::2]=self.water1
        self.watervar[1::2]=self.water2

       
    def gettemp(self):
        heightDataSheet = self.client.open_by_url('https://docs.google.com/spreadsheets/d/1dP5lYNWDH8WmOhmmXGMeZ38cAguLz-OBBo3kVvlhw60/edit#gid=0')
        heightWorksheet = heightDataSheet.worksheet('Sheet1')
        self.tempvar= heightWorksheet.col_values(4)
    def gettranstime(self):
        heightDataSheet = self.client.open_by_url('https://docs.google.com/spreadsheets/d/1dP5lYNWDH8WmOhmmXGMeZ38cAguLz-OBBo3kVvlhw60/edit#gid=0')
        heightWorksheet = heightDataSheet.worksheet('Sheet1')
        self.timevar= heightWorksheet.col_values(1)

    def getbattery(self):
        heightDataSheet = self.client.open_by_url('https://docs.google.com/spreadsheets/d/1dP5lYNWDH8WmOhmmXGMeZ38cAguLz-OBBo3kVvlhw60/edit#gid=0')
        heightWorksheet = heightDataSheet.worksheet('Sheet1')
        self.batteryvar= heightWorksheet.col_values(3)
    def plotwater(self):
        self.ax2.clear()
        #time.sleep(10)
        self.plotwater2()
    def plotwater2(self):
        self.getwater()
        temp=self.watervar[-33:-1]+[(self.watervar[-1])]
        
        self.time=[24,23.25,22.5,21.75,21,20.25,19.5,18.75,18,17.25,16.5,15.75,15,14.25,13.5,12.75,12,11.25,10.5,9.75,9,8.25,7.5,6.75,6,5.25,4.5,3.75,3,2.25,1.5,0.75,0]
        remove=np.array([])
        for x in range(len(temp)):
            if temp[x]=='None':
                remove=np.append(remove,int(x),axis=None)
         
        for x in range (len(remove)):
            self.time.pop(int(remove[x]))         
            temp.pop(int(remove[x]))
            remove=remove-1
    
        
        for x in range(len(temp)):
            temp[x]=float(temp[x])
        baseline=temp[0]
        
        for x in range(len(temp)):
            temp[x]=temp[x]-baseline 
            
        time=np.array([24,23.25,22.5,21.75,21,20.25,19.5,18.75,18,17.25,16.5,15.75,15,14.25,13.5,12.75,12,11.25,10.5,9.75,9,8.25,7.5,6.75,6,5.25,4.5,3.75,3,2.25,1.5,0.75,0])
        self.ref=0*np.array([1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1])
        self.ax2.cla()
        self.ax2.grid()
        temp.reverse()
        self.ax2.plot(self.time,temp,label= "Variation")
        self.ax2.plot(time,self.ref,label="Reference Water Level",linestyle='dashed',linewidth='5')
        self.ax2.legend(prop={"size":floor(20*(self.h/1800))})
        self.ax2.set_xlim([0, 24])
        self.ax2.set_ylim([-2, 2])
        self.ax2.set_xticks([0,2,4,6,8,10,12,14,16,18,20,22,24])
        self.ax2.set_xticklabels(['24','22','20','18','16','14','12','10','8','6','4','2','0'])
        self.ax2.set_title("Water Level Variation (Last 24 Hours)", color="#FFFFFF", fontdict={'family' : 'Tahoma', 'weight' : 'bold', 'size' : floor(30*(self.h/1800))})
        self.ax2.set_xlabel("Time [Hours past]", color="#FFFFFF", fontdict={'family' : 'Tahoma', 'size' : floor(26*(self.h/1800))}) 
        self.ax2.set_ylabel("Variation in Water Level [m]", color="#FFFFFF", fontdict={'family' : 'Tahoma', 'size' : floor(26*(self.h/1800))})
        self.ax2.grid()
        self.ax2.set_facecolor("#AEEAFF")
        self.ax2.tick_params(labelcolor="#FFFFFF",labelsize=floor(20*(self.h/1800)))

    def plottemp(self):    
        self.gettemp()
        temp=self.tempvar[-13:-1]+[(self.tempvar[-1])]
        temp.reverse()
        self.time=np.array([24,22,20,18,16,14,12,10,8,6,4,2,0])
        self.good=np.array([40,40,40,40,40,40,40,40,40,40,40,40,40])
        self.bad=np.array([-30,-30,-30,-30,-30,-30,-30,-30,-30,-30,-30,-30,-30])
        self.ax1.cla()
        self.ax1.grid()
        self.ax1.plot(self.time,temp,label= "Temperature",linewidth='7',color='black')
        self.ax1.plot(self.time,self.good,label="Upper Limit",linestyle='dashed',linewidth='5',color='red')
        self.ax1.plot(self.time,self.bad,label="Lower Limit",linestyle='dashed',linewidth='5',color="#82EEFD")
        self.ax1.legend(prop={"size":floor(20*(self.h/1800))})
        self.ax1.set_xlim([0, 24])
        self.ax1.set_xticks([0,2,4,6,8,10,12,14,16,18,20,22,24])
        self.ax1.set_xticklabels(['24','22','20','18','16','14','12','10','8','6','4','2','0'])
        self.ax1.set_title("System Temperature (Last 24 Hours)", color="#000000", fontdict={'family' : 'Tahoma', 'weight' : 'bold', 'size' : floor(30*(self.h/1800))})
        self.ax1.set_xlabel("Time [Hours past]", color="#000000", fontdict={'family' : 'Tahoma', 'size' : floor(26*(self.h/1800))}) 
        self.ax1.set_ylabel("System Temperature [C]", color="#000000", fontdict={'family' : 'Tahoma', 'size' : floor(26*(self.h/1800))})
        self.ax1.grid()
        self.ax1.set_facecolor("#D9DDDC")
        self.ax1.tick_params(labelcolor="#000000",labelsize=floor(20*(self.h/1800)))
    def plotbattery(self): 
        self.getbattery()
        temp=self.batteryvar[-13:-1]+[(self.batteryvar[-1])]
        temp.reverse()
        
        self.time=np.array([24,22,20,18,16,14,12,10,8,6,4,2,0])
        self.good=np.array([90,90,90,90,90,90,90,90,90,90,90,90,90])
        self.bad=np.array([15,15,15,15,15,15,15,15,15,15,15,15,15])
        self.ax3.cla()
        self.ax3.grid()
        self.ax3.plot(self.time,temp,label= "Level",linewidth='7',color='black')
        self.ax3.plot(self.time,self.good,label="Good",linestyle='dashed',linewidth='5',color='green')
        self.ax3.plot(self.time,self.bad,label="Bad",linestyle='dashed',linewidth='5',color='red')
        self.ax3.legend(prop={"size":floor(20*(self.h/1800))})
        self.ax3.set_xlim([0, 24])
        self.ax3.set_xticks([0,2,4,6,8,10,12,14,16,18,20,22,24])
        self.ax3.set_xticklabels(['24','22','20','18','16','14','12','10','8','6','4','2','0'])
        self.ax3.set_title("Battery Level (Last 24 Hours)", color="#000000", fontdict={'family' : 'Tahoma', 'weight' : 'bold', 'size' : floor(30*(self.h/1800))})
        self.ax3.set_xlabel("Time [Hours past]", color="#000000", fontdict={'family' : 'Tahoma', 'size' : floor(26*(self.h/1800))}) 
        self.ax3.set_ylabel("Battery Level [%]", color="#000000", fontdict={'family' : 'Tahoma', 'size' : floor(26*(self.h/1800))})
        self.ax3.grid()
        self.ax3.set_facecolor("#D9DDDC")
        self.ax3.tick_params(labelcolor="#000000",labelsize=floor(20*(self.h/1800)))

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

        if (self.change5==False or self.change6==False):    
            QMessageBox.critical(self,"Error","Invalid input")
            self.entry4.setText("")
            self.entry5.setText("")
        else:
            if (float(self.mina)>=float(self.maxa)):    
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
            QMessageBox.critical(self,"Error","Invalid input")
            self.entry2.setText("")
            self.entry3.setText("")
        else:
            if (float(self.mine)>float(self.maxe)):    
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

        if self.change==False:    
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

        if self.change2==False:    
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
            QMessageBox.critical(self,"Error","Invalid input")
            self.entry1.setText("")
        else:
            self.label_18.setText(self.mode)
            self.label_45.setText(self.mode)
            self.label_64.setText(self.mode)
            self.send_MT('mode='+self.mode)
        
        self.entry1.setText("")

    def updatemultiple(self):
        
             
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
            self.send_MT('el='+self.entry2.text()+','+self.entry3.text()+';'+'sf='+self.entry6.text())
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
        elif(self.entry4.text()==""):
            self.send_MT('mode='+self.entry1.text()+';'+'el='+self.entry2.text()+','+self.entry3.text()+';'+'sf='+self.entry6.text()+';'+'tres='+self.entry7.text())
        elif(self.entry6.text()==""):
            self.send_MT('mode='+self.entry1.text()+';'+'el='+self.entry2.text()+','+self.entry3.text()+';'+'az='+self.entry4.text()+','+self.entry5.text()+';'+'tres='+self.entry7.text())
        elif(self.entry7.text()==""):
            self.send_MT('mode='+self.entry1.text()+';'+'el='+self.entry2.text()+','+self.entry3.text()+';'+'az='+self.entry4.text()+','+self.entry5.text()+';'+'sf='+self.entry6.text())
        else:
            self.send_MT('mode='+self.entry1.text()+';'+'el='+self.entry2.text()+','+self.entry3.text()+';'+'az='+self.entry4.text()+','+self.entry5.text()+';'+'sf='+self.entry6.text()+';'+'tres='+self.entry7.text())

        self.entry1.setText("")
        self.entry2.setText("")
        self.entry3.setText("")
        self.entry4.setText("")
        self.entry5.setText("")
        self.entry6.setText("")
        self.entry7.setText("")
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
