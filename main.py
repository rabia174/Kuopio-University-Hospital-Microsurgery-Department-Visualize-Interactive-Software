# -*- coding: utf-8 -*-
"""
Created on Thu Apr  2 14:53:01 2020

@author: pc
"""

# ------------------------------------------------------
# ---------------------- main.py -----------------------
# ------------------------------------------------------
from PyQt5.QtWidgets import*
from PyQt5.uic import loadUi

from PyQt5 import QtWidgets, QtCore, uic, QtGui
from PyQt5 import QtMultimedia, QtMultimediaWidgets
import sys  # We need sys so that we can pass argv to QApplication
import os
from random import randint
import pandas as pd
import matplotlib.pyplot as plt 
import gtts
from playsound import playsound

from matplotlib.backends.backend_qt5agg import (NavigationToolbar2QT as NavigationToolbar)
from matplotlib.pyplot import ion
import numpy as np
import random
from PyQt5 import QtWidgets, QtCore, uic, QtGui

     
class MatplotlibWidget(QMainWindow):
    
    def __init__(self):
        
        QMainWindow.__init__(self)

        loadUi("qt_designer.ui",self)

        self.setWindowTitle("PyQt5 & Matplotlib Example GUI")
        self.position_ekg=0
        self.position=0
        self.lcd=0
        self.current_event=0
        self.current_int_start=0
        self.current_int_stop=0
        
        self.lcdNumber.display(self.lcd)
        
        openAction = QtWidgets.QAction(QtGui.QIcon('open.png'), '&Open Task Video', self)
        openAction.setShortcut('Ctrl+T')
        openAction.setStatusTip('Open task movie')
        openAction.triggered.connect(self.openFile)
        
        
        openActioneye = QtWidgets.QAction(QtGui.QIcon('open.png'), '&Open Eye Video', self)
        openActioneye.setShortcut('Ctrl+E')
        openActioneye.setStatusTip('Open eye movie')
        openActioneye.triggered.connect(self.openFile2)
        
        openDataAction = QtWidgets.QAction(QtGui.QIcon('open.png'), '&Open ASC File', self)
        openDataAction.triggered.connect(self.openDataFile)
        
        openDataAction2 = QtWidgets.QAction(QtGui.QIcon('open.png'), '&Open Tasks File', self)
        openDataAction2.triggered.connect(self.openDataFile2)
        
        self.menuSelect_File.addAction(openAction)
        self.menuSelect_File.addAction(openActioneye)
        
        self.menuSelect_Data_File.addAction(openDataAction)
        self.menuSelect_Data_File.addAction(openDataAction2)
        
        self.i=0
        
        self.mediaPlayer = QtMultimedia.QMediaPlayer(None, QtMultimedia.QMediaPlayer.VideoSurface)
        
        self.mediaPlayer2 = QtMultimedia.QMediaPlayer(None, QtMultimedia.QMediaPlayer.VideoSurface)
        
        videoWidget = QtMultimediaWidgets.QVideoWidget()
        videoWidget2 = QtMultimediaWidgets.QVideoWidget()

        self.lay.setContentsMargins(0, 0, 0, 0)
        self.lay.addWidget(videoWidget)
        
        self.lay2.setContentsMargins(0, 0, 0, 0)
        self.lay2.addWidget(videoWidget2)
        
        self.playButton.setEnabled(False)
        self.playButton.setIcon(self.style().standardIcon(QtWidgets.QStyle.SP_MediaPlay))
        self.playButton.clicked.connect(self.play)
        
        self.listen.setEnabled(True)
        self.listen.setIcon(self.style().standardIcon(QtWidgets.QStyle.SP_MediaPlay))
        self.listen.clicked.connect(self.listenEN)
        
        self.pauseButton.setEnabled(False)
        self.pauseButton.setIcon(self.style().standardIcon(QtWidgets.QStyle.SP_MediaPause))
        self.pauseButton.clicked.connect(self.stop)
        
        self.next.setEnabled(False)
        #self.next.setIcon(self.style().standardIcon(QtWidgets.QStyle.SP_MediaPlay))
        self.next.clicked.connect(self.nextEvent)
        
        self.previous.setEnabled(False)
        #self.previous.setIcon(self.style().standardIcon(QtWidgets.QStyle.SP_MediaPlay))
        self.previous.clicked.connect(self.previousEvent)
        
        
        self.positionSlider.setRange(0, 0)
        self.positionSlider.sliderMoved.connect(self.setPosition)
        self.positionSlider.setTickPosition(QSlider.TicksBothSides)
        self.positionSlider.setTickInterval(60000)
        

           
        self.i_int=10
        
        #self.MplWidget_8.canvas.axes.set_facecolor('xkcd:black')
        #self.MplWidget.canvas.axes.set_facecolor('xkcd:black')
        
        self.mediaPlayer.setVideoOutput(videoWidget)
        self.mediaPlayer2.setVideoOutput(videoWidget2)
        #self.mediaPlayer.stateChanged.connect(self.mediaStateChanged)
        self.mediaPlayer.positionChanged.connect(self.positionChanged)
        self.mediaPlayer2.positionChanged.connect(self.positionChanged)
        self.mediaPlayer.durationChanged.connect(self.durationChanged)
        self.mediaPlayer2.durationChanged.connect(self.durationChanged)
        
        self.border=5000
        self.border_ekg=5000
        
    def listenEN(self):
        engine.say("Click on the select data file on the top left menu and then choose to select the ASC file to upload the physiological signals file.")
        engine.runAndWait()
        playsound("FinceSignals.mp3")
        playsound("SwedishSignals.mp3")
        
    def nextEvent(self):
        
        if self.current_event % 2 ==0:
            position=self.start_events_list[self.current_int_start]*66.7
            self.prompt.setText("Task started\n"+self.df2.phase[self.current_event]+" "+self.df2.task[self.current_event]+"\n"+self.df2.name[self.current_event]+" "+self.df2.trial[self.current_event])
            self.current_int_start+=1
        else:
            position=self.stop_events_list[self.current_int_stop]*66.7
            self.prompt.setText("Task ended\n"+self.df2.phase[self.current_event]+" "+self.df2.task[self.current_event]+"\n"+self.df2.name[self.current_event]+" "+self.df2.trial[self.current_event])
            self.current_int_stop+=1
            
        #self.mediaPlayer.setPosition(position) 
        #self.mediaPlayer2.setPosition(position)
        self.setPosition(int(position))
        print(position)
        self.current_event+=1
    def previousEvent(self):
        
        if self.current_event % 2 ==0:
            position=self.start_events_list[self.current_int_start]*66.7
            self.prompt.setText("Task started\n"+self.df2.phase[self.current_event]+" "+self.df2.task[self.current_event]+"\n"+self.df2.name[self.current_event]+" "+self.df2.trial[self.current_event])
            self.current_int_start+=1
        else:
            position=self.stop_events_list[self.current_int_stop]*66.7
            self.prompt.setText("Task ended\n"+self.df2.phase[self.current_event]+" "+self.df2.task[self.current_event]+"\n"+self.df2.name[self.current_event]+" "+self.df2.trial[self.current_event])
            self.current_int_stop+=1
            
        #self.mediaPlayer.setPosition(position) 
        #self.mediaPlayer2.setPosition(position)
        self.setPosition(int(position))
        self.current_event-=1        
    def openFile(self):
     
        fileName, _ = QtWidgets.QFileDialog.getOpenFileName(self, "Open Movie",
                                                  QtCore.QDir.homePath(),"Video files (*.mp4)")
        #print(fileName)
        self.prompt.setText("Scene video is successfully uploaded!\n Please upload the eye video!")
        if fileName:
            self.mediaPlayer.setMedia(
                QtMultimedia.QMediaContent(QtCore.QUrl.fromLocalFile(fileName)))
            self.playButton.setEnabled(True)
            self.playButton.setEnabled(True)
            self.pauseButton.setEnabled(True)
            
    def openFile2(self):
     
        fileName, _ = QtWidgets.QFileDialog.getOpenFileName(self, "Open Movie",
                                                  QtCore.QDir.homePath(),"Video files (*.mp4)")
        #print(fileName)
        self.prompt.setText("Eye video is successfully uploaded!\nClick on the play button!")
        if fileName:
            self.mediaPlayer2.setMedia(
                QtMultimedia.QMediaContent(QtCore.QUrl.fromLocalFile(fileName)))
            self.playButton.setEnabled(True)
            self.playButton.setEnabled(True)
            self.pauseButton.setEnabled(True)
        engine.say("Files are received successfully. Please click on the play button to start the stream.")
        engine.runAndWait()
        playsound("FincePlay.mp3")
        playsound("SwedishPlay.mp3")
            
    def openDataFile2(self):
        fileName, _ = QtWidgets.QFileDialog.getOpenFileName(self, "Open Movie",
                                                  QtCore.QDir.homePath(),"CSV files (*.csv)")
        self.df2=pd.read_csv(filepath_or_buffer=fileName, 
                 sep=";")
        self.prompt.setText("Events file is successfully uploaded!\n Please upload the video files!")
        self.next.setEnabled(True)
        self.previous.setEnabled(True)
        
        self.df2.columns=[ "participant","phase","task","name","trial","start","stop","start_ms","stop_ms"]
        
        self.df2.sort_values(by=['start'])
        
        print(self.df2)
        
        self.start_events_list=list( self.df2.start)
        
        self.stop_events_list=list( self.df2.stop)
        
        
        print(self.start_events_list)
        
        engine.say("Events are received and processed successfully. To continue, please click on the select video File on the top left menu and then upload your video files.")
        engine.runAndWait()
        playsound("FinceVideost.mp3")
        playsound("SwedishVideost.mp3")
        #print(events_list[0])
        
       
    def openDataFile(self):
        fileName, _ = QtWidgets.QFileDialog.getOpenFileName(self, "Open Movie",
                                                  QtCore.QDir.homePath(),"CSV files (*.csv *.ASC)")
        self.df=pd.read_table(filepath_or_buffer=fileName, 
                 sep=";",  
                 skiprows = 70)
        self.prompt.setText("Signals file is successfully uploaded!\n Please upload the events file!\nClick on the select data file again\nand then choose open tasks file.")
        self.df=self.df.drop(self.df.columns[0], axis=1)

        self.df.columns=[ "Lihas1",
  "Lihas2",
  "Lihas3",
  "Lihas4",
  "EKG",
  "EOG",
  "Lampotila",
  "Kiihtyvyyx",
  "Kiihtyvyysy",
  "Kiihtyvyysz",
  "GSR"]
        #print(len(self.df.axes[0])) 
        self.x = list(range(1,5000))  # 100000 time points
        self.x_ekg = list( range(1,5000))
        self.ekg = list(self.df.EKG[1:5000])
        #self.temp = list(self.df.Lampotila[1:1500])
        #self.EOG = list(self.df.EOG[1:1500])# 100000 data points
        self.Lihas1= list(self.df.Lihas1[1:5000])
        self.Lihas2= list(self.df.Lihas2[1:5000])
        self.Lihas3= list(self.df.Lihas3[1:5000])
        self.Lihas4= list(self.df.Lihas4[1:5000])
        #self.GSR= list(self.df.GSR[1:1500])
        self.accx= list(self.df.Kiihtyvyyx[1:5000])
        self.accy= list(self.df.Kiihtyvyysy[1:5000])
        self.accz= list(self.df.Kiihtyvyysz[1:5000])
        #self.x_int = list(range(100))  # 100 time points
        #self.ekg_int = list(self.df.EKG[:100])
  

        self.MplWidget.canvas.axes.clear()
        self.MplWidget.canvas.axes.grid(color='red', linestyle='-', linewidth=0.5)
        self.MplWidget.canvas.axes.plot(self.x_ekg, self.ekg,marker='|',color='black')
        self.MplWidget.canvas.axes.axvline(self.position_ekg,  0, 20000, label='pyplot vertical line',color='white',lw=4)
        self.MplWidget.canvas.axes.legend(('EKG'),loc='upper left')
        #self.MplWidget.canvas.axes.set_title('EKG-Heart Rate')
        self.MplWidget.canvas.draw()
        
        #self.MplWidget_2.canvas.axes.clear()
        #self.MplWidget_2.canvas.axes.grid(color='black', linestyle='-', linewidth=0.2)
        #self.MplWidget_2.canvas.axes.plot(self.x, self.EOG, linestyle='dashed')
        #self.MplWidget_2.canvas.axes.axvline(self.position, 0, 20000, label='pyplot vertical line',color='r')
        #self.MplWidget_2.canvas.axes.legend(('Body Temperature'),loc='upper left')
        #self.MplWidget_2.canvas.axes.set_title('Lampötlila-Body Temperature')
        #self.MplWidget_2.canvas.draw()
        
        
        self.MplWidget_3.canvas.axes.clear()
        self.MplWidget_3.canvas.axes.grid(color='blue', linestyle='-', linewidth=0.5)
        self.MplWidget_3.canvas.axes.plot(self.x, self.Lihas1, linestyle='dashed')
        self.MplWidget_3.canvas.axes.axvline(self.position, 0, 20000, label='pyplot vertical line',color='r')
        self.MplWidget_3.canvas.axes.legend(('Lihas1'),loc='upper left')
        #self.MplWidget_3.canvas.axes.set_title('Lihas1')
        self.MplWidget_3.canvas.draw()
        
        self.MplWidget_4.canvas.axes.clear()
        self.MplWidget_4.canvas.axes.grid(color='blue', linestyle='-', linewidth=0.5)
        self.MplWidget_4.canvas.axes.plot(self.x, self.Lihas2, linestyle='dashed')
        self.MplWidget_4.canvas.axes.axvline(self.position, 0, 20000, label='pyplot vertical line',color='r')
        self.MplWidget_4.canvas.axes.legend(('Lihas2'),loc='upper left')
        #self.MplWidget_4.canvas.axes.set_title('Lihas 2')
        self.MplWidget_4.canvas.draw()
        
        self.MplWidget_5.canvas.axes.clear()
        self.MplWidget_5.canvas.axes.grid(color='blue', linestyle='-', linewidth=0.5)
        self.MplWidget_5.canvas.axes.plot(self.x, self.Lihas3, linestyle='dashed')
        self.MplWidget_5.canvas.axes.axvline(self.position, 0, 20000, label='pyplot vertical line',color='r')
        self.MplWidget_5.canvas.axes.legend(('Lihas3'),loc='upper left')
        #self.MplWidget_5.canvas.axes.set_title('Lihas3')
        self.MplWidget_5.canvas.draw()
        
        self.MplWidget_6.canvas.axes.clear()
        self.MplWidget_6.canvas.axes.grid(color='blue', linestyle='-', linewidth=0.5)
        self.MplWidget_6.canvas.axes.plot(self.x, self.Lihas4, linestyle='dashed')
        self.MplWidget_6.canvas.axes.axvline(self.position, 0, 20000, label='pyplot vertical line',color='r')
        self.MplWidget_6.canvas.axes.legend(('Lihas4'),loc='upper left')
        #self.MplWidget_6.canvas.axes.set_title('Lihas 4')
        self.MplWidget_6.canvas.draw()
        
        self.MplWidget_7.canvas.axes.clear()
        self.MplWidget_7.canvas.axes.grid(color='black', linestyle='-', linewidth=0.3)
        self.MplWidget_7.canvas.axes.plot(self.x, self.accx, linestyle='dashed')
        self.MplWidget_7.canvas.axes.plot(self.x, self.accy, linestyle='dashed')
        self.MplWidget_7.canvas.axes.plot(self.x, self.accz, linestyle='dashed')
        self.MplWidget_7.canvas.axes.axvline(self.position, 0, 20000, label='pyplot vertical line',color='r')
        self.MplWidget_7.canvas.axes.legend(('xyz'),loc='upper left')
        self.MplWidget_7.canvas.draw()
 
 
        self.playButton.setEnabled(True)
        self.pauseButton.setEnabled(True)
        
        engine.say("Signals are received and processed successfully. To continue, click on the select data file on the top left menu again and then choose to select the Tasks file to upload the events file.")
        engine.runAndWait()
        playsound("FinceEvent.mp3")
        playsound("SwedishEvent.mp3")
    
            
    def update_plot_data(self):   
        self.lcdNumber.display(self.lcd)
        self.lcd=self.lcd+1
        
        if self.position_ekg <= self.border_ekg:
           self.MplWidget.canvas.axes.grid(color='red', linestyle='-', linewidth=0.5)
           self.MplWidget.canvas.axes.lines[1].remove()
           self.MplWidget.canvas.axes.axvline(self.position_ekg, 0, 100000, label='pyplot vertical line',color='white',lw=4)
           self.MplWidget.canvas.draw()
           
           self.position_ekg=self.position_ekg+300
        else:
           self.x_ekg = list(range(self.border_ekg,self.border_ekg+5000))
           self.ekg = list(self.df.EKG[self.border_ekg:self.border_ekg+5000])     
           self.MplWidget.canvas.axes.clear()
           self.MplWidget.canvas.axes.plot(self.x_ekg, self.ekg,marker='|',color='black')
           self.MplWidget.canvas.axes.axvline(self.position_ekg,  0, 100000, label='pyplot vertical line',color='white',lw=4)
           
          
           self.MplWidget.canvas.draw()
           
           self.border_ekg+=5000    
        
        if self.position <= self.border:
        
            #self.MplWidget_2.canvas.axes.grid(color='black', linestyle='-', linewidth=0.2)
            #self.MplWidget_2.canvas.axes.lines[1].remove()
            #self.MplWidget_2.canvas.axes.axvline(self.position, 0, 100000, label='pyplot vertical line',color='r')
            #self.MplWidget_2.canvas.draw()
        
            self.MplWidget_3.canvas.axes.grid(color='blue', linestyle='-', linewidth=0.5)
            self.MplWidget_3.canvas.axes.lines[1].remove()
            self.MplWidget_3.canvas.axes.axvline(self.position, 0, 100000, label='pyplot vertical line',color='r')
            self.MplWidget_3.canvas.draw()
            
            self.MplWidget_4.canvas.axes.grid(color='blue', linestyle='-', linewidth=0.5)
            self.MplWidget_4.canvas.axes.lines[1].remove()
            self.MplWidget_4.canvas.axes.axvline(self.position, 0, 100000, label='pyplot vertical line',color='r')
            self.MplWidget_4.canvas.draw()
            
            self.MplWidget_5.canvas.axes.grid(color='blue', linestyle='-', linewidth=0.5)
            self.MplWidget_5.canvas.axes.lines[1].remove()
            self.MplWidget_5.canvas.axes.axvline(self.position, 0, 100000, label='pyplot vertical line',color='r')
            self.MplWidget_5.canvas.draw()
           
            self.MplWidget_6.canvas.axes.grid(color='blue', linestyle='-', linewidth=0.5)
            self.MplWidget_6.canvas.axes.lines[1].remove()
            self.MplWidget_6.canvas.axes.axvline(self.position, 0, 100000, label='pyplot vertical line',color='r')
            self.MplWidget_6.canvas.draw()
        
            self.MplWidget_7.canvas.axes.grid(color='white', linestyle='-', linewidth=0.3)
            self.MplWidget_7.canvas.axes.lines[3].remove()
            self.MplWidget_7.canvas.axes.axvline(self.position, 0, 100000, label='pyplot vertical line',color='r')
            self.MplWidget_7.canvas.draw()
    
            self.position=self.position+300
            
            
        else:
            
            
            
            self.x = list(range(self.border,self.border+5000))  # 100000 time points
            #self.temp = list(self.df.Lampotila[self.border:self.border+1500])
            #self.EOG = list(self.df.EOG[self.border:self.border+1500])# 100000 data points
            self.Lihas1= list(self.df.Lihas1[self.border:self.border+5000])
            self.Lihas2= list(self.df.Lihas2[self.border:self.border+5000])
            self.Lihas3= list(self.df.Lihas3[self.border:self.border+5000])
            self.Lihas4= list(self.df.Lihas4[self.border:self.border+5000])
            self.accx= list(self.df.Kiihtyvyyx[self.border:self.border+5000])
            self.accy= list(self.df.Kiihtyvyysy[self.border:self.border+5000])
            self.accz= list(self.df.Kiihtyvyysz[self.border:self.border+5000])
            #self.GSR= list(self.df.GSR[self.border:self.border+1500])
            
            
            
            #self.MplWidget_2.canvas.axes.clear()
            #self.MplWidget_2.canvas.axes.grid(color='black', linestyle='-', linewidth=0.2)
            #self.MplWidget_2.canvas.axes.plot(self.x, self.EOG, linestyle='dashed')
            #self.MplWidget_2.canvas.axes.axvline(self.position, 0, 100000, label='pyplot vertical line',color='r')
            #self.MplWidget_2.canvas.draw()
            
            self.MplWidget_3.canvas.axes.clear()
            self.MplWidget_3.canvas.axes.grid(color='blue', linestyle='-', linewidth=0.5)
            self.MplWidget_3.canvas.axes.plot(self.x, self.Lihas1, linestyle='dashed')
            self.MplWidget_3.canvas.axes.axvline(self.position, 0, 100000, label='pyplot vertical line',color='r')
            self.MplWidget_3.canvas.draw()
            
            self.MplWidget_4.canvas.axes.clear()
            self.MplWidget_4.canvas.axes.grid(color='blue', linestyle='-', linewidth=0.5)
            self.MplWidget_4.canvas.axes.plot(self.x, self.Lihas2, linestyle='dashed')
            self.MplWidget_4.canvas.axes.axvline(self.position, 0, 100000, label='pyplot vertical line',color='r')
            self.MplWidget_4.canvas.draw()
            
            self.MplWidget_5.canvas.axes.clear()
            self.MplWidget_5.canvas.axes.grid(color='blue', linestyle='-', linewidth=0.5)
            self.MplWidget_5.canvas.axes.plot(self.x, self.Lihas3, linestyle='dashed')
            self.MplWidget_5.canvas.axes.axvline(self.position, 0, 100000, label='pyplot vertical line',color='r')
            self.MplWidget_5.canvas.draw()
            
            self.MplWidget_6.canvas.axes.clear()
            self.MplWidget_6.canvas.axes.grid(color='blue', linestyle='-', linewidth=0.5)
            self.MplWidget_6.canvas.axes.plot(self.x, self.Lihas4, linestyle='dashed')
            self.MplWidget_6.canvas.axes.axvline(self.position, 0, 100000, label='pyplot vertical line',color='r')
            self.MplWidget_6.canvas.draw()
            
            self.MplWidget_7.canvas.axes.clear()
            self.MplWidget_7.canvas.axes.grid(color='green', linestyle='-', linewidth=0.3)
            self.MplWidget_7.canvas.axes.plot(self.x, self.accx, linestyle='dashed')
            self.MplWidget_7.canvas.axes.plot(self.x, self.accy, linestyle='dashed')
            self.MplWidget_7.canvas.axes.plot(self.x, self.accz, linestyle='dashed')
            self.MplWidget_7.canvas.axes.axvline(self.position, 0, 100000, label='pyplot vertical line',color='r')
            self.MplWidget_7.canvas.draw()

            self.border+=5000

            
            
    def stop(self):   
            self.mediaPlayer.pause()
            self.mediaPlayer2.pause()
            
            self.timer.stop()
            self.timer2.stop()
            
            self.pauseButton.setIcon(
                self.style().standardIcon(QtWidgets.QStyle.SP_MediaPause))
    
    def play(self):
        #if self.mediaPlayer.state() == QtMultimedia.QMediaPlayer.PlayingState:
            
            #self.timer2.stop()
          
        #else:
            self.mediaPlayer.play()
            self.mediaPlayer2.play()
            self.prompt.setText("Great! Now you can see the visualizations.\n To jump the nearest event\nclick on the next button!")
            #set the satrting position
            #self.setPosition(int(self.start_events_list[0])*66.7)
            self.timer = QtCore.QTimer(self)
            #self.timer2 = QtCore.QTimer(self)
            self.timer.setInterval(0.062)
            #self.timer2.setInterval(50)
            self.timer.timeout.connect(self.update_plot_data)
            #self.timer2.timeout.connect(self.update_plot_data_ekg)
            self.timer.start()
            #self.timer2.start()
            self.playButton.setIcon(
                self.style().standardIcon(QtWidgets.QStyle.SP_MediaPlay))
            
            self.next.setEnabled(True)
   
    def positionChanged(self, position):
        self.positionSlider.setValue(position)

    def durationChanged(self, duration):
        self.positionSlider.setRange(0, duration)
       
    def setPosition(self, position):
        self.mediaPlayer.setPosition(position) 
        self.mediaPlayer2.setPosition(position)
        #print(position)
        self.border=position
        self.border_ekg=position
        self.position=position
        self.position_ekg=position
        
        #print(position)
            
        #self.label_12.setText("Media is playing now.")
        
   

import pyttsx3        

app = QApplication([])
window = MatplotlibWidget()
window.show()
engine=pyttsx3.init()
engine.setProperty('rate', 130)
engine.say("Hi, this is Visualize Interactive! Visualize interactive is produced to visualize physiological signals during the activity of participants.")
engine.say("If you know how to use the program please go on. If you want to listen more about the instructions, click on the listen button on the main menu!")
engine.say("the visualize interactive is produced by the University of Eastern Finland on behalf of Kuopio University Hospital Microsurgery Department Research Team")
engine.runAndWait()
playsound("Fince.mp3")
playsound("Swedish.mp3")
app.exec_()
