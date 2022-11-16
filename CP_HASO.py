# -*- coding: utf-8 -*-
"""
Created on Tue Sep 24 15:07:12 2019

Camera Basler
Gui for basler camera use pypylon
pip install pypylon in conda sheel
PyQT5 and PyQtgraph
Pyhton 3.x
@author: LOA Julien Gautier
"""


from PyQt5.QtWidgets import QApplication,QVBoxLayout,QHBoxLayout,QWidget,QPushButton
from PyQt5.QtWidgets import QComboBox,QSlider,QCheckBox,QLabel,QSpinBox,QMessageBox,QSizePolicy
from pyqtgraph.Qt import QtCore
from pyqtgraph.Qt import QtGui 
from PyQt5.QtCore import Qt
import pyqtgraph as pg
from PyQt5.QtGui import QIcon

import sys,time

import numpy as np

from pypylon import pylon

try :
    from visu import SEE
except:
    print ('No visu module installed :see' )
    

import qdarkstyle # pip install qdakstyle https://github.com/ColinDuquesnoy/QDarkStyleSheet  sur conda
import pathlib,os

class CAMERABASLERACQHaso(QWidget) :

    def __init__(self,cam='camDefault',confVisu=None):
        super(CAMERABASLERACQHaso, self).__init__()
        self.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5()) # dark style 
        self.confVisu=confVisu
        if cam==None:
            self.nbcam='camTest'
        else:   
            self.nbcam=cam
        self.confCCD = QtCore.QSettings('confCameras.ini', QtCore.QSettings.IniFormat)
        self.camType=self.confCCD.value(self.nbcam+"/camType")
        self.pathRef=self.confCCD.value(self.nbcam+"/path")
        self.dataRefExist=False
        if self.camType != 'basler':
            print('error camera type')
        
        self.id=self.confCCD.value(self.nbcam+"/camId")
        self.camName=self.confCCD.value(self.nbcam+"/name")
        camConnected=None
        for i in pylon.TlFactory.GetInstance().EnumerateDevices():
            if i.GetSerialNumber()==self.id:
                camConnected=i
        try :
            if camConnected is not None:
                self.cam0= pylon.InstantCamera(pylon.TlFactory.GetInstance().CreateDevice(camConnected))
                self.isConnected=True
                print(self.camName,'connected @',i.GetSerialNumber())
#            else:
#                self.cam0= pylon.InstantCamera(pylon.TlFactory.GetInstance().CreateFirstDevice())
#                print('fisrt camera connected')
#                self.isConnected=True
            else:
                 self.isConnected=False
                 print('no camera connected')
        except:
            self.isConnected=False
            print('no camera connected')
            
        self.xc=int(self.confCCD.value(self.nbcam+"/xc"))
        self.yc=int(self.confCCD.value(self.nbcam+"/yc"))
        self.rx=int(self.confCCD.value(self.nbcam+"/rx"))
        self.ry=int(self.confCCD.value(self.nbcam+"/ry"))
        
        self.setup()
        
        self.cameName=self.confCCD.value(self.nbcam+"/name")
        self.setWindowTitle(self.cameName)
        p = pathlib.Path(__file__)
        sepa=os.sep
        self.icon=str(p.parent) + sepa + 'icons' +sepa
        self.setWindowIcon(QIcon(self.icon+'LOA.png'))
        #pg.setConfigOptions(antialias=True)
        
        self.actionButton()
        
        if self.isConnected==False:
        
        
            print ('not connected')
            self.nbcam='camTest'
            self.runButton.setEnabled(False)
            self.runButton.setStyleSheet("background-color:gray")
            self.runButton.setStyleSheet("QPushButton:!pressed{image: url(./icons/Circled Play-595b40b65ba036ed117d436f.svg);background-color: rgb(0, 0, 0,0) ;border-color: rgb(0, 0, 0,0)}""QPushButton:pressed{image: url(./icons/Circled Play-595b40b65ba036ed117d436f.svg);background-color: rgb(0, 0, 0,0) ;border-color: rgb(0, 0, 0)}")
            
            self.hSliderShutter.setEnabled(False)
            self.trigg.setEnabled(False)
            self.hSliderGain.setEnabled(False)
            self.stopButton.setEnabled(False)
            self.stopButton.setStyleSheet("background-color:gray")
            self.stopButton.setStyleSheet("QPushButton:!pressed{border-image: url(./icons/Stop.svg);background-color: rgb(0, 0, 0,0) ;border-color: rgb(0, 0, 0,0);}""QPushButton:pressed{image: url(./icons/Stop.svg);background-color: rgb(0, 0, 0,0) ;border-color: rgb(0, 0, 0)}")

            
        if self.isConnected==True:
            self.cam0.Open()
 
            self.cam0.GainAuto.SetValue('Off')
            self.cam0.TriggerMode.SetValue('Off')
            self.cam0.TriggerSelector.SetValue("AcquisitionStart")
            self.cam0.ExposureAuto.SetValue('Off')

            self.cam0.Width=self.cam0.Width.Max
            self.cam0.Height=self.cam0.Height.Max
#            self.hSliderShutter.setMinimum(self.cam0.ExposureTimeAbs.GetMin())
#            self.hSliderShutter.setMaximum(self.cam0.ExposureTimeAbs.GetMax())
            sh=int(self.confCCD.value(self.nbcam+"/shutter"))
            self.hSliderShutter.setValue(sh)
            self.shutterBox.setValue(int(sh))
            
            self.cam0.ExposureTimeAbs.SetValue(int(sh*1000))
            
            self.hSliderGain.setMinimum(self.cam0.GainRaw.GetMin())
            self.hSliderGain.setMaximum(self.cam0.GainRaw.GetMax())
            g=int(self.confCCD.value(self.nbcam+"/gain"))
            self.hSliderGain.setValue(g)
            self.cam0.GainRaw.SetValue(int(g))
            
            
            self.gainBox.setMinimum(self.cam0.GainRaw.GetMin())
            self.gainBox.setMaximum(self.cam0.GainRaw.GetMax())
            self.gainBox.setValue(int(self.cam0.GainRaw.GetValue()))
            
            
            self.dimy=self.cam0.SensorHeight.GetValue()
            self.dimx=self.cam0.SensorWidth.GetValue()
            print("number of pixels :",self.dimx,'*',self.dimy)
        
        else :
            self.dimy=960
            self.dimx=1240
            
        
        def twoD_Gaussian(x,y, amplitude, xo, yo, sigma_x, sigma_y, theta, offset):
            xo = float(xo)
            yo = float(yo)    
            a = (np.cos(theta)**2)/(2*sigma_x**2) + (np.sin(theta)**2)/(2*sigma_y**2)
            b = -(np.sin(2*theta))/(4*sigma_x**2) + (np.sin(2*theta))/(4*sigma_y**2)
            c = (np.sin(theta)**2)/(2*sigma_x**2) + (np.cos(theta)**2)/(2*sigma_y**2)
            return offset + amplitude*np.exp( - (a*((x-xo)**2) + 2*b*(x-xo)*(y-yo) + c*((y-yo)**2)))

        # Create x and y indices
        x = np.arange(0,self.dimx)
        y = np.arange(0,self.dimy)
        y,x = np.meshgrid(y, x)

        self.data=twoD_Gaussian(x, y,250, 300, 600, 40, 40, 0, 10)+(50*np.random.rand(self.dimx,self.dimy)).round() 
       
        self.Display(self.data)
        
        self.msg = QMessageBox()
        self.msg.setIcon(QMessageBox.Critical)
        self.msg.setText("Reference differente !!!!")
        self.msg.setInformativeText("Reference data is different")
        self.msg.setWindowTitle("Warning ...")
        
        
        self.msgErrorRef=QMessageBox()
        self.msgErrorRef.setIcon(QMessageBox.Critical)
        self.msgErrorRef.setText("No reference selected !!!!")
        self.msgErrorRef.setInformativeText("Reference file is not selected : Push set Ref")
        self.msgErrorRef.setWindowTitle("Warning ...")
        
    def setup(self):    
        
        vbox1=QVBoxLayout() 
        
        
        self.camNameLabel=QLabel('nomcam',self)
        
        self.camNameLabel.setText(self.confCCD.value(self.nbcam+"/name"))

        self.camNameLabel.setAlignment(Qt.AlignCenter)
        self.camNameLabel.setStyleSheet('font: bold 20px')
        self.camNameLabel.setStyleSheet('color: yellow')
        vbox1.addWidget(self.camNameLabel)
        
        hbox1=QHBoxLayout() # horizontal layout pour run et stop
        self.runButton=QPushButton(self)
        self.runButton.setMaximumWidth(60)
        self.runButton.setMinimumHeight(60)
        self.runButton.setStyleSheet("QPushButton:!pressed{border-image: url(./icons/Circled Play-595b40b65ba036ed117d436f.svg);background-color: rgb(0, 0, 0,0) ;border-color: green;}""QPushButton:pressed{image: url(./icons/Circled Play-595b40b65ba036ed117d436f.svg);background-color: rgb(0, 0, 0,0) ;border-color: rgb(0, 0, 0)}")
        self.stopButton=QPushButton(self)
        
        self.stopButton.setMaximumWidth(60)
        self.stopButton.setMinimumHeight(50)
        self.stopButton.setStyleSheet("QPushButton:!pressed{border-image: url(./icons/Stop.svg);background-color: rgb(0, 0, 0,0) ;border-color: rgb(0, 0, 0,0);}""QPushButton:pressed{image: url(./icons/Stop.svg);background-color: rgb(0, 0, 0,0) ;border-color: rgb(0, 0, 0)}")
        
        
        hbox1.addWidget(self.runButton)
        hbox1.addWidget(self.stopButton)
#        self.oneButton=QPushButton(self)
#        hbox1.addWidget(self.oneButton)
        
        vbox1.addLayout(hbox1)
        
        self.trigg=QComboBox()
        self.trigg.setMaximumWidth(60)
        self.trigg.addItem('OFF')
        self.trigg.addItem('ON')
        self.labelTrigger=QLabel('Trigger')
        self.labelTrigger.setMaximumWidth(60)
        self.itrig=self.trigg.currentIndex()
        hbox2=QHBoxLayout()
        hbox2.addWidget(self.labelTrigger)
        hbox2.addWidget(self.trigg)
        vbox1.addLayout(hbox2)
        
        self.labelExp=QLabel('Exposure (ms)')
        self.labelExp.setMaximumWidth(120)
        self.labelExp.setAlignment(Qt.AlignCenter)
        vbox1.addWidget(self.labelExp)
        self.hSliderShutter=QSlider(Qt.Horizontal)
        self.hSliderShutter.setMinimum(1)
        self.hSliderShutter.setMaximum(1000)
        self.hSliderShutter.setMaximumWidth(120)
        self.shutterBox=QSpinBox()
        self.shutterBox.setMinimum(1)
        self.shutterBox.setMaximum(1000)
        self.shutterBox.setMaximumWidth(60)
       
        hboxShutter=QHBoxLayout()
        hboxShutter.addWidget(self.hSliderShutter)
        hboxShutter.addWidget(self.shutterBox)
        vbox1.addLayout(hboxShutter)
        
        
        

        hboxGain=QHBoxLayout()
        self.labelGain=QLabel('Gain')
        self.labelGain.setMaximumWidth(120)
        self.labelGain.setAlignment(Qt.AlignCenter)
        vbox1.addWidget(self.labelGain)
        self.hSliderGain=QSlider(Qt.Horizontal)
        self.hSliderGain.setMaximumWidth(120)
        
        self.gainBox=QSpinBox()
        
           
        self.gainBox.setMaximumWidth(60)
        hboxGain.addWidget(self.hSliderGain)
        hboxGain.addWidget(self.gainBox)
        vbox1.addLayout(hboxGain)
        
        
        soustracBox=QHBoxLayout()
        self.checkBoxsousRef=QCheckBox('Ref substrac ',self)
        self.checkBoxsousRef.setChecked(False)
        self.checkBoxsousRef.setStyleSheet("QCheckBox::indicator{width: 30px;height: 30px;}""QCheckBox::indicator:unchecked { image : url(./icons/Toggle Off-595b40b85ba036ed117dac78.svg);}""QCheckBox::indicator:checked { image:  url(./icons/Toggle On-595b40b85ba036ed117dac79.svg);}")
    
        soustracBox.addWidget(self.checkBoxsousRef)
        self.setRefButton=QPushButton('Set Ref')
        soustracBox.addWidget(self.setRefButton)
        
           
        vbox1.addLayout(soustracBox)
        vbox1.addStretch(1)
        hboxRef=QHBoxLayout()
        

        
        
        self.winImageRef = pg.GraphicsLayoutWidget()
        self.winImageRef.setMaximumSize(200,200)
        self.winImageRef.setContentsMargins(0,0,0,0)
        self.winImageRef.setAspectLocked(True)
        self.winImageRef.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.winImageRef.ci.setContentsMargins(0,0,0,0)
        
        self.pRef=self.winImageRef.addPlot()
        self.imRef=pg.ImageItem()
        self.pRef.addItem(self.imRef)
        self.pRef.setMouseEnabled(x=False,y=False)
        self.pRef.setContentsMargins(0,0,0,0)
        self.pRef.setAspectLocked(True,ratio=1)
        self.pRef.showAxis('right',show=False)
        self.pRef.showAxis('top',show=False)
        self.pRef.showAxis('left',show=False)
        self.pRef.showAxis('bottom',show=False)
        self.histRef = pg.HistogramLUTItem() 
        self.histRef.setImageItem(self.imRef)
        self.histRef.autoHistogramRange()
        self.histRef.gradient.loadPreset('flame')
        
        hboxRef.addWidget(self.winImageRef)
        vbox1.addLayout(hboxRef)
        vbox1.addStretch(20)
        
        cameraWidget=QWidget()
        cameraWidget.setLayout(vbox1)
        cameraWidget.setMinimumSize(150,200)
        cameraWidget.setMaximumSize(200,900)
        hMainLayout=QHBoxLayout()
        hMainLayout.addWidget(cameraWidget)
        
        self.visualisation=SEE(confpath=self.confVisu) ## Widget for visualisation and tools  self.confVisu permet d'avoir plusieurs camera et donc plusieurs fichier ini de visualisation
        
        self.vLine2 = pg.InfiniteLine(angle=90, movable=False,pen='r')
        self.hLine2 = pg.InfiniteLine(angle=0, movable=False,pen='r')
        self.visualisation.p1.addItem(self.vLine2)
        self.visualisation.p1.addItem(self.hLine2, ignoreBounds=False)
        
        self.vLine2.setPos(self.xc)
        self.hLine2.setPos(self.yc)
        
        self.ro2=pg.EllipseROI([self.xc,self.yc],[self.rx,self.ry],pen='r',movable=False)#maxBounds=QtCore.QRectF(0,0,self.rx,self.ry)
        self.ro2.setPos([self.xc-(self.rx/2),self.yc-(self.ry/2)])
        self.visualisation.p1.addItem(self.ro2)
        
        
        vbox2=QVBoxLayout() 
        vbox2.addWidget(self.visualisation)
        hMainLayout.addLayout(vbox2)
        
        self.setLayout(hMainLayout)
        
        
        
        
    def actionButton(self):
        self.runButton.clicked.connect(self.acquireMultiImage)
        self.stopButton.clicked.connect(self.stopAcq)
        self.hSliderShutter.sliderMoved.connect(self.mSliderShutter)
        self.shutterBox.editingFinished.connect(self.shutter)
        self.hSliderGain.sliderMoved.connect(self.mSliderGain)
        self.gainBox.editingFinished.connect(self.gain)
        self.trigg.currentIndexChanged.connect(self.Trig)
        self.setRefButton.clicked.connect(self.setref)
        self.checkBoxsousRef.stateChanged.connect(self.checkBoxsousRefAct)
        
        

    def shutter(self):
        
        sh=self.shutterBox.value() # 
        self.hSliderShutter.setValue(sh) # set value of slider
        time.sleep(0.1)
        print(sh,'sh')
        self.cam0.ExposureTimeAbs.SetValue(int(sh*1000))
            
        self.confCCD.setValue(self.nbcam+"/shutter",float(sh))
        self.confCCD.sync()

    def mSliderShutter(self): # for shutter slider 
        sh=self.hSliderShutter.value() 
        self.shutterBox.setValue(sh) # 
        time.sleep(0.1)
        self.cam0.ExposureTimeAbs.SetValue(int(sh*1000)) # Set shutter CCD in microseconde
        self.confCCD.setValue(self.nbcam+"/shutter",float(sh))   
    
    
         
    def gain(self):
        g=self.gainBox.value() # 
        self.hSliderGain.setValue(g) # set slider value
        time.sleep(0.1)
        self.cam0.GainRaw.SetValue(int(g))
        
        self.confCCD.setValue(self.nbcam+"/gain",float(g))
        self.confCCD.sync()
    
    def mSliderGain(self):
        g=self.hSliderGain.value()
        self.gainBox.setValue(g) # set valeur de la box
        time.sleep(0.1)
        self.cam0.GainRaw.SetValue(int(g))
        self.confCCD.setValue(self.nbcam+"/gain",float(g))
        self.confCCD.sync()
        
    def Trig(self):
        self.itrig=self.trigg.currentIndex()
        
        if self.itrig==0:
            self.cam0.TriggerMode.SetValue('Off')
#            print ("trigger OFF")
        if self.itrig==1:
            self.cam0.TriggerMode.SetValue('On')
#            print("Trigger ON")
        
    def acquireMultiImage(self):   
        #print('live...')
        
        self.runButton.setEnabled(False)
        self.runButton.setStyleSheet("QPushButton:!pressed{border-image: url(./icons/Circled Play-595b40b65ba036ed117d436f.svg);background-color: gray ;border-color: rgb(0, 0, 0,0);}""QPushButton:pressed{image: url(./icons/Circled Play-595b40b65ba036ed117d436f.svg);background-color: gray ;border-color: rgb(0, 0, 0)}")
        #self.runButton.setStyleSheet("background-color:gray")
        try:
            self.threadRunAcq=ThreadRunAcq(self)
            self.threadRunAcq.newDataRun.connect(self.Display)
            self.threadRunAcq.start()
        except :
            pass
    
    
    def acquireOneImage(self):   
        
        
        self.runButton.setEnabled(False)
        self.runButton.setStyleSheet("QPushButton:!pressed{border-image: url(./icons/Circled Play-595b40b65ba036ed117d436f.svg);background-color: gray ;border-color: rgb(0, 0, 0,0);}""QPushButton:pressed{image: url(./icons/Circled Play-595b40b65ba036ed117d436f.svg);background-color: gray ;border-color: rgb(0, 0, 0)}")
        #self.runButton.setStyleSheet("background-color:gray")
        try:
            self.threadOneAcq=ThreadOneAcq(self)
            self.threadOneAcq.newDataOne.connect(self.Display)
            self.threadOneAcq.start()
        except :
            print('error')
            pass
        self.runButton.setEnabled(True)
        self.runButton.setStyleSheet("QPushButton:!pressed{border-image: url(./icons/Circled Play-595b40b65ba036ed117d436f.svg);background-color: rgb(0, 0, 0,0) ;border-color: rgb(0, 0, 0,0);}""QPushButton:pressed{image: url(./icons/Circled Play-595b40b65ba036ed117d436f.svg);background-color: rgb(0, 0, 0,0) ;border-color: rgb(0, 0, 0)}")
        
    
    
    def stopAcq(self):
#        print('Stop live')
        try:
            self.threadRunAcq.stopThreadRunAcq()
            
            self.cam0.ExecuteSoftwareTrigger()
        except :
            print('error stop thread')
            pass
        self.runButton.setEnabled(True)
        #self.runButton.setStyleSheet("background-color: rgb(0, 200, 0)")
        self.runButton.setStyleSheet("QPushButton:!pressed{border-image: url(./icons/Circled Play-595b40b65ba036ed117d436f.svg);background-color: rgb(0, 0, 0,0) ;border-color: rgb(0, 0, 0,0);}""QPushButton:pressed{image: url(./icons/Circled Play-595b40b65ba036ed117d436f.svg);background-color: rgb(0, 0, 0,0) ;border-color: rgb(0, 0, 0)}")
        
        #self.threadAcq.terminate()    
        
    def Display(self,data):
        '''Display data with Visu module
        '''
        self.data=data
        
        if self.dataRefExist==True and self.checkBoxsousRef.isChecked()==1:
            
            
            self.dataCut=self.data[0:self.dimx,100:self.dimy]
            self.dataRefCut=self.dataRef[0:self.dimx,100:self.dimy]
            
#            self.dataCut=self.dataCut/round(self.dataCut.mean(),3)
#            self.dataRefCut=self.dataRefCut/round(self.dataRefCut.mean(),3)
#   
            div=self.dataCut+self.dataRefCut+1 # to ovoid 0
            
            self.dataRefSous=(self.dataCut-self.dataRefCut)/div
            
            self.moy=round(self.dataRefSous.mean(),3)
            self.maxx=round(self.dataRefSous.max(),3)
            self.minn=round(self.dataRefSous.min(),3)
            
            self.imRef.setImage(self.dataRefSous,autoLevels=True) # visualisation of difference image
            print('moy dat-ref/data+ref',self.moy,self.maxx,self.minn)
            if (self.moy>0.1 or self.maxx>1 or self.minn<-1 or self.moy<-0.1 ):
                self.msg.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
                self.msg.exec_()
          
        self.visualisation.newDataReceived(self.data) # send data to visualisation widget
    
    


    def setref(self):
        # to select reference file
        fname=QtGui.QFileDialog.getOpenFileName(self,"Select a reference file",self.pathRef,"Images (*.txt );Text File(*.txt)")
        fichier=fname[0]
        ext=os.path.splitext(fichier)[1]
        
        self.pathRef=self.confCCD.value(self.nbcam+"/path")
        
        self.confCCD.setValue(self.nbcam+"/path",os.path.dirname(fichier))
        
        
        
        if ext=='.txt': # text file
            self.dataRef=np.loadtxt(str(fichier))
            self.dataRefNorm=self.dataRef/round(self.dataRef.mean(),3)
            self.dataRefExist=True
        else :
            self.dataRefExist=False
            



    def checkBoxsousRefAct(self):
        
        if self.checkBoxsousRef.isChecked()==1 and    self.dataRefExist==False:
            self.msgErrorRef.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
            self.msgErrorRef.exec_()
            
    def closeEvent(self,event):
        self.fin()
        event.accept()
    
    
    def fin(self):
        try :
            self.threadRunAcq.stopThreadRunAcq()
        except :
            pass
        try :
            self.cam0.close()
        except :
            pass
        sys.exit(0)  
        
        
class ThreadRunAcq(QtCore.QThread):
    
    newDataRun=QtCore.Signal(object)
    
    def __init__(self, parent=None):
        
        super(ThreadRunAcq,self).__init__(parent)
        self.parent=parent
        self.cam0 = self.parent.cam0
        self.stopRunAcq=False
        self.itrig= self.parent.itrig
        self.converter=pylon.ImageFormatConverter()
        
        
        
    def run(self):
        
        global data
        
        
        while True :
            
            if self.stopRunAcq:
                
                break
            
            #print('-----> Acquisition ended')
            
#            if self.itrig==0: # si cam pas en mode trig externe on envoi un trig soft...
#                self.cam0.send_trigger()
#               # print('trigg')
            
            data=self.cam0.GrabOne(20000000)

            data1=self.converter.Convert(data)
            data1 = data1.GetArray()#, dtype=np.double)
            data1.squeeze()
#            data=data1[:,:,0]
            data=np.rot90(data1,1)
            self.newDataRun.emit(data)
    
    def stopThreadRunAcq(self):
       
        try :
            self.cam0.ExecuteSoftwareTrigger()
            self.stopRunAcq=True
        except : 
            pass
        
        
class ThreadOneAcq(QtCore.QThread):
    
    newDataOne=QtCore.Signal(object)
    
    def __init__(self, parent=None):
        
        super(ThreadOneAcq,self).__init__(parent)
        self.parent=parent
        self.cam0 = self.parent.cam0
        self.stopOneAcq=False
        self.itrig= self.parent.itrig
        self.converter=pylon.ImageFormatConverter()
        print('one img')
    def run(self):
        
        data=self.cam0.GrabOne(20000000)

        data1=self.converter.Convert(data)
        data1 = data1.GetArray()#, dtype=np.double)
        data1.squeeze()
#            data=data1[:,:,0]
        data=np.rot90(data1,1)
        self.newDataOne.emit(data)
        
    def stopThreadOneAcq(self):
        #self.cam0.send_trigger()
       
        try :
            self.cam0.ExecuteSoftwareTrigger()
            self.stopRunAcq=True
        except : 
            pass
        self.cam0.stop_live()

if __name__ == "__main__":
    appli = QApplication(sys.argv)  
    e = CAMERABASLERACQHaso(cam='cam19')  
#    b = CAMERABASLERACQHaso(cam='cam111')
#    b.show()
    e.show()
    appli.exec_()         