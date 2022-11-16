# -*- coding: utf-8 -*-
#!usr/bin/python
"""
Created on Wed Nov  28 15:15:26 2018
Camera Imaging sources
Modified on Wed Dec 12 11:08:56 2018
@author: loa Julien Gautier

12 cameras imaging source
"""
from CameraTiltMotor import CAMMOT # class lecture 1 camera
import sys
from PyQt5.QtWidgets import QGridLayout,QVBoxLayout,QWidget,QApplication,QGroupBox,QTabWidget
from PyQt5.QtWidgets import QSizePolicy,QDockWidget
from PyQt5.QtGui import QIcon
from pyqtgraph.Qt import QtCore
import qdarkstyle # pip install qdakstyle https://github.com/ColinDuquesnoy/QDarkStyleSheet a faire dans anaconda prompt
import pathlib,os,time
# from TiltGuiNew import TILTMOTORGUI
from pathLaser import IMAGELASERP1
from CP_HASO import CAMERABASLERACQHaso

class App6Cam(QWidget):
    #class 6 camera
    def __init__(self,camName0=None,motOn0=False,camName1=None,motOn1=False,camName2=None,motOn2=False,camName3=None,motOn3=False,camName4=None,motOn4=False,camName5=None,motOn5=False,parent=None):
        super().__init__()
        self.parent=parent
        self.left=100
        self.top=30
        self.width=1000
        self.height=200
        #self.setGeometry(self.left,self.top,self.width,self.height)
        self.setWindowTitle('Laser Alignment' )
       
        self.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
        p = pathlib.Path(__file__)
        sepa=os.sep
        self.icon=str(p.parent) + sepa + 'icons' +sepa
        self.setWindowIcon(QIcon(self.icon+'LOA.png'))
        try :
            self.cam0 =  CAMMOT(name=camName0,motOn=motOn0,visuGauche=True)
        except :
            self.cam0 =  CAMMOT(name=None,motOn=motOn0,visuGauche=True)
        try :
            self.cam1 = CAMMOT(name=camName1,motOn=motOn1)
        except:
            self.cam1 =  CAMMOT(name=None,motOn=motOn1,visuGauche=True)
        try:
            self.cam2 = CAMMOT(name=camName2,motOn=motOn2,visuGauche=True)
        except :
            self.cam2 =  CAMMOT(name=None,motOn=motOn2,visuGauche=True)
        try :
            self.cam3 =CAMMOT(name=camName3,motOn=motOn3)
        except :
            self.cam3 =  CAMMOT(name=None,motOn=motOn3,visuGauche=True)
        try :
            self.cam4 =CAMMOT(name=camName4,motOn=motOn4)
        except :
            self.cam4 =  CAMMOT(name=None,motOn=motOn4,visuGauche=True)
        try :
            self.cam5 =CAMMOT(name=camName5,motOn=motOn5)
        except :
            self.cam5 =  CAMMOT(name=None,motOn=motOn5,visuGauche=True)
        
        self.cam=[self.cam0,self.cam1,self.cam2,self.cam3,self.cam4,self.cam5]
        self.setup()
        
        self.actionButton()
        
    def setup(self):

        grid_layout = QGridLayout()
        grid_layout.setVerticalSpacing(3)
        grid_layout.setHorizontalSpacing(10)
        self.setStyleSheet("QDockWidget""{""border: 10px solid white""}")
        width=10
        height=15
        self.dock0=QDockWidget(self)
        self.dock0.setWindowTitle(self.cam0.cam.ccdName)
        self.dock0.setStyleSheet("QDockWidget""{""background-color: white""}")
        self.dock0.setWidget(self.cam0)
        self.dock0.setFeatures(QDockWidget.DockWidgetFloatable)
        self.dock0.setContentsMargins(0,0,10,10)
        self.dock0.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.dock0.resize(QtCore.QSize(width, height))
        
#        self.dock0.setWindowState(Qt::WindowFullScreen)
        
        self.dock1=QDockWidget(self)
        self.dock1.setWindowTitle(self.cam1.cam.ccdName)
        self.dock1.setWidget(self.cam1)
        self.dock1.setFeatures(QDockWidget.DockWidgetFloatable)
        self.dock1.resize(QtCore.QSize(width, height))
        self.dock1.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        
        self.dock2=QDockWidget(self)
        self.dock2.setWindowTitle(self.cam2.cam.ccdName)
        self.dock2.setWidget(self.cam2)
        self.dock2.setFeatures(QDockWidget.DockWidgetFloatable)
        self.dock2.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.dock2.resize(QtCore.QSize(width, height))
        
        self.dock3=QDockWidget(self)
        self.dock3.setWindowTitle(self.cam3.cam.ccdName)
        self.dock3.setWidget(self.cam3)
        self.dock3.setFeatures(QDockWidget.DockWidgetFloatable)
        self.dock3.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.dock3.resize(QtCore.QSize(width, height))
        
        self.dock4=QDockWidget(self)
        self.dock4.setWindowTitle(self.cam4.cam.ccdName)
        self.dock4.setWidget(self.cam4)
        self.dock4.setFeatures(QDockWidget.DockWidgetFloatable)
        self.dock4.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.dock4.resize(QtCore.QSize(width, height))
        
        self.dock5=QDockWidget(self)
        self.dock5.setWindowTitle(self.cam5.cam.ccdName)
        self.dock5.setWidget(self.cam5)
        self.dock5.setFeatures(QDockWidget.DockWidgetFloatable)
        self.dock5.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.dock5.resize(QtCore.QSize(width, height))
        
        
        grid_layout.addWidget(self.dock0, 0, 0)
        grid_layout.addWidget(self.dock1, 0, 1)
        grid_layout.addWidget(self.dock2, 0, 2)
        grid_layout.addWidget(self.dock3, 1,0)
        grid_layout.addWidget(self.dock4, 1,1)
        grid_layout.addWidget(self.dock5, 1,2)
        
        grid_layout.setContentsMargins(0,0,0,0)
        grid_layout.setVerticalSpacing(50)
        grid_layout.setHorizontalSpacing(10)
#        self.horizontalGroupBox=QGroupBox()
#        self.horizontalGroupBox.setLayout(grid_layout)
#        self.horizontalGroupBox.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        windowLayout=QVBoxLayout()
        windowLayout.addLayout(grid_layout)
        windowLayout.setContentsMargins(1,1,1,1)
#        windowLayout.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
#        MainWidget=QWidget()
#        MainWidget.setContentsMargins(0, 0, 0, 0)
#        MainWidget.setLayout(grid_layout)
#        self.setCentralWidget(MainWidget)
        
        self.setContentsMargins(5,5,5,5)
        self.setLayout(windowLayout) #
        
    def actionButton(self):
        self.dock0.topLevelChanged.connect(self.Dock0Changed)
        self.dock1.topLevelChanged.connect(self.Dock1Changed)
        self.dock2.topLevelChanged.connect(self.Dock2Changed)
        self.dock3.topLevelChanged.connect(self.Dock3Changed)
        self.dock4.topLevelChanged.connect(self.Dock4Changed)
        self.dock5.topLevelChanged.connect(self.Dock5Changed)
#        self.dock1.visibilityChanged.connect(self.Dock1Empty)
        
    def Dock1Empty (self):
        print('enpty')
    def Dock0Changed(self):
        self.dock0.showMaximized()
    def Dock0Maximisize(self):
        self.dock0.setFloating(True)
        self.dock0.showMaximized()
    def Dock1Changed(self):
        self.dock1.showMaximized()
    def Dock1Maximisize(self):
        self.dock1.setFloating(True)
        self.dock1.showMaximized()
    def Dock2Changed(self):
        self.dock2.showMaximized()
    def Dock2Maximisize(self):
        self.dock2.setFloating(True)
        self.dock2.showMaximized()
    def Dock3Changed(self):
        self.dock3.showMaximized()
    def Dock3Maximisize(self):
        self.dock3.setFloating(True)
        self.dock3.showMaximized()
    def Dock4Changed(self):
        self.dock4.showMaximized() 
    def Dock4Maximisize(self):
        self.dock4.setFloating(True)
        self.dock4.showMaximized()
    def Dock5Changed(self):
        self.dock5.showMaximized()
    def Dock5Maximisize(self):
        self.dock5.setFloating(True)
        self.dock5.showMaximized()
        
    def stopRun(self):
        self.cam0.cam.stopAcq()
        self.cam1.cam.stopAcq()
        self.cam2.cam.stopAcq()
        self.cam3.cam.stopAcq()
        self.cam4.cam.stopAcq()
        self.cam5.cam.stopAcq()
        
    def closeEvent(self,event):
        self.stopRun()
        sys.exit(0)
        event.accept()

class MainWindows(QWidget):
    ## Main class 3 tabs : 12 cameras
    def __init__(self,parent=None):
        super().__init__()
        print('intialisation ...')
        self.parent=parent
        self.left=100
        self.top=30
        self.width=1200
        self.height=300
        self.setGeometry(self.left,self.top,self.width,self.height)
        self.setWindowTitle('Laser Alignment' )
        self.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
        p = pathlib.Path(__file__)
        sepa=os.sep
        self.icon=str(p.parent) + sepa + 'icons' +sepa
        self.setWindowIcon(QIcon(self.icon+'LOA.png'))
        self.setup()
#        self.actionButton()
        
        
    def setup(self):
        
        self.layout=QVBoxLayout(self)
        self.layout.setContentsMargins(1,1,1,1)
        self.setContentsMargins(1,1,1,1)
        self.tabs=QTabWidget()
        self.tabs.setContentsMargins(1,1,1,1)
        self.tab0=App6Cam(camName0='cam11',motOn0=False,camName1='cam12',motOn1=True,camName2='cam13',motOn2=True,camName3='cam15',motOn3=True,camName4='cam16',motOn4=True,camName5='cam17',motOn5=True)
        self.tab1=App6Cam(camName0='cam21',motOn0=False,camName1='cam22',motOn1=True,camName2='cam23',motOn2=True,camName3='cam25',motOn3=True,camName4='cam26',motOn4=True,camName5='cam27',motOn5=True)
       
        self.tab2=App6Cam(camName0='cam31',motOn0=False,camName1='cam32',motOn1=True,camName2='cam33',motOn2=True,camName3='cam35',motOn3=True,camName4='cam36',motOn4=True,camName5='cam37',motOn5=True)
        
        self.tab3=App6Cam(camName0='cam14',motOn0=False,camName1='cam24',motOn1=False,camName2=None,motOn2=False,camName3='cam101',motOn3=False,camName4=None,motOn4=False,camName5=None,motOn5=False)
        
        time.sleep(2)
        self.tabs.addTab(self.tab0,'    P1    ')
        self.tabs.addTab(self.tab1,'    P2    ')
        self.tabs.addTab(self.tab2,'    P3    ')
        self.tabs.addTab(self.tab3,'    DM    ')
        
        self.P1=IMAGELASERP1(laser='1')
        self.tabs.addTab(self.P1,'P1 graph')
        self.P2=IMAGELASERP1(laser='2')
        self.tabs.addTab(self.P2,'P2 graph')
        self.P3=IMAGELASERP1(laser='3')
        self.tabs.addTab(self.P3,'P3 graph')
        
        self.CPHASO=CAMERABASLERACQHaso(cam='cam19') 
        self.tabs.addTab(self.CPHASO,'CP HASO')
        self.layout.addWidget(self.tabs)
        self.setLayout(self.layout)
        
        self.TFHASO=CAMERABASLERACQHaso(cam='cam111') 
        self.tabs.addTab(self.TFHASO,'TF HASO')
        
        self.layout.addWidget(self.tabs)
        
        self.setLayout(self.layout)


    def changeTab(self):
#        print('tab change', 'tab is',self.tabs.currentIndex())
#        self.tab=[self.tab0,self.tab1,self.tab2]
        self.tab0.stopRun()
        self.tab1.stopRun()
        self.tab2.stopRun()
        self.tab3.stopRun()
        
    def actionButton(self):
        self.tabs.currentChanged.connect(self.changeTab)
        self.P1.Pcam1.clicked.connect(self.tab0.Dock0Maximisize)#P1.MaxWingetP1cam0
        self.P1.Pcam2.clicked.connect(self.tab0.Dock1Maximisize)
        self.P1.Pcam3.clicked.connect(self.tab0.Dock2Maximisize)
        self.P1.Pcam5.clicked.connect(self.tab0.Dock3Maximisize)
        self.P1.Pcam6.clicked.connect(self.tab0.Dock4Maximisize)
        self.P1.Pcam7.clicked.connect(self.tab0.Dock5Maximisize)
        self.P1.Pcam4.clicked.connect(self.tab3.Dock0Maximisize)
        
        self.P2.Pcam1.clicked.connect(self.tab1.Dock0Maximisize)#P1.MaxWingetP1cam0
        self.P2.Pcam2.clicked.connect(self.tab1.Dock1Maximisize)
        self.P2.Pcam3.clicked.connect(self.tab1.Dock2Maximisize)
        self.P2.Pcam5.clicked.connect(self.tab1.Dock3Maximisize)
        self.P2.Pcam6.clicked.connect(self.tab1.Dock4Maximisize)
        self.P2.Pcam7.clicked.connect(self.tab1.Dock5Maximisize)
        self.P2.Pcam4.clicked.connect(self.tab3.Dock1Maximisize)
        
        self.P3.Pcam1.clicked.connect(self.tab2.Dock0Maximisize)
        self.P3.Pcam2.clicked.connect(self.tab2.Dock1Maximisize)
        self.P3.Pcam3.clicked.connect(self.tab2.Dock2Maximisize)
        self.P3.Pcam5.clicked.connect(self.tab2.Dock3Maximisize)
        self.P3.Pcam7.clicked.connect(self.tab2.Dock5Maximisize)
#    def MaxWingetP1cam0(self):
#        print('ici')
#        self.tab0.Dock0Maximisize()
#        print('la')
    def open_widget(self,fene):
        """ open new widget 
        """

        if fene.isWinOpen==False:
            fene.setup
            fene.isWinOpen=True
            fene.startThread2()
            #fene.Display(self.data)
            fene.show()
        else:
            #fene.activateWindow()
#            fene.raise_()
#            fene.showNormal()
            pass            
                
    def closeEvent(self,event):
        self.tab0.stopRun()
        self.tab1.stopRun()
        self.tab2.stopRun()
        self.tab3.stopRun()
    
        # sys.exit(0)
        event.accept()
        
        
        

if __name__=='__main__':
    
    app=QApplication(sys.argv)
    app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
    multiTab=MainWindows()#App6Cam(camName0='cam31',motOn0=False,camName1=None,motOn1=False,camName2='cam33',motOn2=False,camName3='cam35',motOn3=False,camName4='cam36',motOn4=False,camName5='cam37',motOn5=False)
        #App6Cam(camName0="cam11",camName1="cam12",camName2="cam13",camName3="cam15",camName4="cam16",camName5="cam17"  )    #
    
    #MainWindows()
    multiTab.show()
#    sys.exit(app.exec_() )
    app.exec_()

