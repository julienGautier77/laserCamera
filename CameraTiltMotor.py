# -*- coding: utf-8 -*-
"""
Created on Wed Sep 11 16:51:01 2019

@author: SALLEJAUNE
"""

from PyQt5.QtWidgets import QApplication,QVBoxLayout,QHBoxLayout,QWidget,QMainWindow
from PyQt5 import QtCore
import sys
from PyQt5.QtWidgets import QSizePolicy
from TiltGuiLight import TILTMOTORGUI
import qdarkstyle
import pathlib,os
from PyQt5.QtGui import QIcon





from camera import CAMERA

class CAMMOT(QWidget) :
    
    def __init__(self,name=None,motOn=False,motLat=None,motorTypeName0=None, motVert=None,motorTypeName1=None,nomWin='',nomTilt='',unit=1,jogValue=1,visuGauche=False,parent=None):
        super().__init__()
        self.parent=parent
        self.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
        print('name',name)
        self.unit=unit
        self.jogValue=jogValue
        self.nomWin=nomWin
        p = pathlib.Path(__file__)
        sepa=os.sep
        self.icon=str(p.parent) + sepa + 'icons' +sepa
        self.setWindowIcon(QIcon(self.icon+'LOA.png'))
        self.confCCD = QtCore.QSettings('confCameras.ini', QtCore.QSettings.IniFormat)
        self.confpath=str(p.parent /'confCameras.ini')
        
#        print('conf path:',self.confpath)
        
        if name==None:
            self.nbcam='camTest'
        else:   
            self.nbcam=name
        self.camType=self.confCCD.value(self.nbcam+"/camType")
        
        self.cam=CAMERA(cam=name,fft='off',meas='on',affLight=True,aff='right',separate=True,confpath=self.confpath)
        
        
    
        
        if motLat==None and motOn==True:
            motLat=str(self.cam.conf.value(self.cam.nbcam+"/motLat"))
            print(motLat)
        if motVert==None and motOn==True:
            motVert=str(self.cam.conf.value(self.cam.nbcam+"/motVert")   ) 
        
        if motorTypeName0==None and motOn==True:
            motorTypeName0=str(self.cam.conf.value(self.cam.nbcam+"/motorTypeNameLat"))
        
        if motorTypeName1==None and motOn==True:
            motorTypeName1=str(self.cam.conf.value(self.cam.nbcam+"/motorTypeNameVert"))
            
            
        self.motLat=motLat
        self.motorTypeName0=motorTypeName0
        self.motVert=motVert
        self.motorTypeName1=motorTypeName1
        
        self.motor=TILTMOTORGUI(motLat=self.motLat,motorTypeName0=self.motorTypeName0, motVert=self.motVert,motorTypeName1=self.motorTypeName1,nomWin=self.nomWin,nomTilt='',unit=self.unit,jogValue=self.jogValue)
        
        if motOn==True:
            
            # self.motor.startThread2()
        
            self.motor.haut.setAutoRepeat(True)
            self.motor.bas.setAutoRepeat(True)
            self.motor.gauche.setAutoRepeat(True)
            self.motor.droite.setAutoRepeat(True)
            self.pasY=float(self.confCCD.value(self.nbcam+"/pasY"))
            self.pasX=float(self.confCCD.value(self.nbcam+"/pasX"))
            
        if motOn==False:  
            self.motor.setEnabled(False)

            
        self.setup()
#        self.actionButton()
       
    
    def setup(self):    
        
        self.hbox=QHBoxLayout()
        
        self.cam.vboxSup.addWidget(self.motor)
        self.cam.vboxSup.addStretch(2)
        self.cam.setContentsMargins(0, 0, 0, 0)
        self.hbox.addWidget(self.cam)
        self.hbox.setContentsMargins(0, 0, 0, 0)
#        
        
       
#
        
        
#        hMainLayout.addWidget(self.visualisation)
        self.setLayout(self.hbox)
            
#        MainWidget=QWidget()
#        MainWidget.setContentsMargins(0, 0, 0, 0)
#        MainWidget.setLayout(self.hbox)
#        self.setCentralWidget(MainWidget)
        self.setWindowTitle(self.cam.ccdName)
        self.setContentsMargins(0, 0, 0, 0)
#        self.setSizePolicy(QSizePolicy.Maximum, QSizePolicy.Maximum)




    
        
if __name__ == "__main__":
    appli = QApplication(sys.argv)  
    e = CAMMOT(name="cam12",motOn=False,visuGauche=True)#,motLat='NF_Lat',motorTypeName0='NewFocus', motVert='NF_Vert',motorTypeName1='NewFocus',nomWin='Tilts')
    e.show()
   
    appli.exec_()         