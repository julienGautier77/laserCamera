#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Oct 29 17:43:08 2019

@author: juliengautier
"""

from PyQt5.QtWidgets import QWidget,QApplication,QHBoxLayout,QPushButton
from pyqtgraph.Qt import QtCore,QtGui 
import sys,time,os
import pathlib
import qdarkstyle
import pyqtgraph as pg
from TiltGuiLight import TILTMOTORGUI
from oneMotorGuiNew import ONEMOTORGUI

class IMAGELASERP1(QWidget):
    
    def __init__(self,laser='1'):
        
        super(IMAGELASERP1, self).__init__()
        sepa=os.sep
        p = pathlib.Path(__file__)
        self.icon="C:/Users/Salle-Jaune/Desktop/Python/jouvenceCentreurLaserBas/icons/" #str(p.parent) + sepa+'icons' +sepa
        self.laser=laser
        self.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
        self.wid=QWidget(self)
        imgG=self.icon+"P"+self.laser+"JOUVENCE.JPEG"
        self.wid.setStyleSheet("background-image: url(%s);background-repeat :False" %imgG)
        
        self.hMainLayout=QHBoxLayout()
        self.hMainLayout.addWidget(self.wid)
        
        
        
        self.haut=QPushButton(self)
        self.haut.resize(61, 61)
        self.hautImg=self.icon+'P'+self.laser+'Haut.PNG'
        self.haut.setStyleSheet("border-image: url(%s)" % self.hautImg)
        
        
        self.Pepita=QPushButton(self)
        self.Pepita.resize(61, 61)
        self.PepitaImg=self.icon+'P'+self.laser+'PEPITA.PNG'
        self.Pepita.setStyleSheet("QPushButton:!pressed{border-image: url(%s);border-color: rgb(0, 0, 0,0);}""QPushButton:pressed{border-image: url(%s);background-color: rgb(100,100,0);}" % (self.PepitaImg,self.PepitaImg))
        
        
        
        self.Reseau=QPushButton(self)
        self.Reseau.resize(61, 61)
        self.ReseauImg=self.icon+'P'+self.laser+'EntreeReseau.PNG'
        self.Reseau.setStyleSheet("QPushButton:!pressed{border-image: url(%s);border-color: rgb(0, 0, 0,0);}""QPushButton:pressed{border-image: url(%s);background-color: rgb(100,100,0);}" % (self.ReseauImg,self.ReseauImg))
        
        
       
        
        self.PM1=QPushButton(self)
        self.PM1.resize(61, 61)
        self.PM1Img=self.icon+'P'+self.laser+'M1.PNG'
        self.PM1.setStyleSheet("QPushButton:!pressed{border-image: url(%s);border-color: rgb(0, 0, 0,0);}""QPushButton:pressed{border-image: url(%s);background-color: rgb(100,100,0);}" % (self.PM1Img,self.PM1Img))
        
        
        self.PM2=QPushButton(self)
        self.PM2.resize(64, 64)
        self.PM2Img=self.icon+'P'+self.laser+'M2.PNG'
        self.PM2.setStyleSheet("QPushButton:!pressed{border-image: url(%s);border-color: rgb(0, 0, 0,0);}""QPushButton:pressed{border-image: url(%s);background-color: rgb(100,100,0);}" % (self.PM2Img,self.PM2Img))
        
        
        
        
        self.PReseauTrans=QPushButton('P'+self.laser+' grating Trans',self)
        
        
        self.ccdImg=self.icon+'ccd.jpg'
        self.Pcam1=QPushButton(self)
        self.Pcam1.resize(30, 30)
        self.Pcam1.setStyleSheet("QPushButton:!pressed{border-image: url(%s);border-color: rgb(0, 0, 0,0);}""QPushButton:pressed{border-image: url(%s);background-color: rgb(100,100,0);}" % (self.ccdImg,self.ccdImg))
        
        self.ccdImgInv=self.icon+'ccdInv.jpg'
        self.Pcam2=QPushButton(self)
        self.Pcam2.resize(30, 30)
        self.Pcam2.setStyleSheet("QPushButton:!pressed{border-image: url(%s);border-color: rgb(0, 0, 0,0);}""QPushButton:pressed{border-image: url(%s);background-color: rgb(100,100,0);}" % (self.ccdImgInv,self.ccdImgInv))
        
        self.ccdImgBasler=self.icon+'basler.jpg'
        self.Pcam3=QPushButton('zero order',self)
        self.Pcam3.resize(80, 40)
        self.Pcam3.setIcon(QtGui.QIcon(self.ccdImgBasler))

        if self.laser=='1' or  self.laser=='2':
            self.PM2Trans=QPushButton('P'+self.laser+'M2 Trans',self)
            self.PM2Trans.resize(64, 34)
            self.PM2Trans.resize(64, 34)
            self.SortieZorba=QPushButton(self)
            self.SortieZorba.resize(61, 61)
            self.SortieZorbaImg=self.icon+'P'+self.laser+'SortieZorba.PNG'
            self.SortieZorba.setStyleSheet("QPushButton:!pressed{border-image: url(%s);border-color: rgb(0, 0, 0,0);}""QPushButton:pressed{border-image: url(%s);background-color: rgb(100,100,0);}" % (self.SortieZorbaImg,self.SortieZorbaImg))
            
            self.P1Doublet=QPushButton('Doublet',self)
            self.P1Doublet.resize(61,61)
            self.P1Doublet.move(900,250)
            self.Pcam4=QPushButton(self)
            self.Pcam4.resize(30, 30)
            self.Pcam4.setStyleSheet("QPushButton:!pressed{border-image: url(%s);border-color: rgb(0, 0, 0,0);}""QPushButton:pressed{border-image: url(%s);background-color: rgb(100,100,0);}" % (self.ccdImg,self.ccdImg))
            self.Pcam6=QPushButton('CL',self)
            self.Pcam6.resize(40, 30)
            self.Pcam6.setIcon(QtGui.QIcon(self.ccdImgBasler))
        
        self.Pcam5=QPushButton(self)
        self.Pcam5.resize(30, 30)
        self.Pcam5.setStyleSheet("QPushButton:!pressed{border-image: url(%s);border-color: rgb(0, 0, 0,0);}""QPushButton:pressed{border-image: url(%s);background-color: rgb(100,100,0);}" % (self.ccdImgInv,self.ccdImgInv))
        
        
        
        self.Pcam7=QPushButton('CL TB',self)
        self.Pcam7.resize(60, 30)
        self.Pcam7.setIcon(QtGui.QIcon(self.ccdImgBasler))
        
        
        if self.laser=='1':
            self.haut.move(56,35)
            self.Pepita.move(50,136)
            self.Pcam1.move(150,120)
            self.Pcam2.move(870,400)
            self.Pcam3.move(870,600)
            self.Pcam4.move(180,350)
            self.Pcam5.move(270,430)
            self.Pcam6.move(320,630)
            self.Pcam7.move(260,660)
            self.Reseau.move(905,134)
            self.PReseauTrans.move(880,511)
            self.SortieZorba.move(677,377)
            self.PM1.move(325,335)
            self.PM2.move(200,451)
            self.PM2Trans.move(406,462)
            
        if self.laser=='2':
            self.haut.move(56,30)
            self.Pepita.move(60,126)
            self.Pcam1.move(130,120)
            self.Pcam2.move(895,650)
            self.Pcam3.move(730,700)
            self.Pcam4.move(180,440)
            self.Pcam5.move(280,430)
            self.Pcam6.move(300,660)
            self.Pcam7.move(190,660)
            self.Reseau.move(905,134)
            self.Reseau.move(934,116)
            self.PReseauTrans.move(720,650)
            self.SortieZorba.move(894,457)
            self.PM1.move(326,433)
            self.PM2.move(245,554)
            self.PM2Trans.move(406,562) 
            self.P2ns=QPushButton('P2 ns',self)
            self.P2ns.move(450,662)
        if self.laser=='3':
            self.haut.move(56,30)
            self.Pepita.move(59,128)
            self.Pcam1.move(150,120)
            self.Pcam2.move(150,380)
            self.Pcam3.move(40,375)
            
            self.Pcam5.move(193,500)
            
            self.Pcam7.move(220,660)
            self.Reseau.move(412,397)
            self.PReseauTrans.move(100,470)
            self.PM1.move(219,374)
            self.PM2.move(204,532)
            
            
        self.setLayout(self.hMainLayout)
        self.actionButton()
        
    def actionButton(self):

        self.PepitaTilt=TILTMOTORGUI( motLat='P'+self.laser+'_Pepita_Lat', motorTypeName0='A2V', motVert='P'+self.laser+'_Pepita_Vert', motorTypeName1='A2V', nomWin='Tilt P'+self.laser, nomTilt='P'+self.laser+'Pepita')
        self.Pepita.clicked.connect(lambda:self.open_widget(self.PepitaTilt) )
        
        self.ReseauTilt=TILTMOTORGUI( motLat='P'+self.laser+'_Entree_Comp_Lat', motorTypeName0='A2V', motVert='P'+self.laser+'_Entree_Comp_Vert', motorTypeName1='A2V', nomWin='Tilt P'+self.laser, nomTilt='P'+self.laser+' Entree comp')
        self.Reseau.clicked.connect(lambda:self.open_widget(self.ReseauTilt) )
        
        if self.laser=='1' or self.laser=='2':
            self.SortieZorbaTilt=TILTMOTORGUI( motLat='P'+self.laser+'_Sortie_Comp_Lat', motorTypeName0='A2V', motVert='P'+self.laser+'_Sortie_Comp_Vert', motorTypeName1='A2V', nomWin='Tilt P'+self.laser, nomTilt='P'+self.laser+'Sortie Comp')
            self.SortieZorba.clicked.connect(lambda:self.open_widget(self.SortieZorbaTilt) )
            
            self.doubletWidget=TILTMOTORGUI(motLat='Doublet_Lat',motorTypeName0='RSAI',motVert='Doublet_Vert',motorTypeName1='RSAI')
            self.P1Doublet.clicked.connect(lambda:self.open_widget(self.doubletWidget))
            
        if self.laser=='1'   : 
            self.PM2TransWidget=ONEMOTORGUI( mot='P'+self.laser+'_M2_Trans',motorTypeName0='A2V',nomWin='control one motor:',showRef=True,unit=2,jogValue=1,parent=None)
            self.PM2Trans.clicked.connect(lambda:self.open_widget(self.PM2TransWidget) )
        if self.laser=='2' :   
            self.PM2TransWidget=ONEMOTORGUI( mot='P'+self.laser+'_M2_Trans',motorTypeName0='RSAI',nomWin='control one motor:',showRef=True,unit=2,jogValue=1,parent=None)
            self.PM2Trans.clicked.connect(lambda:self.open_widget(self.PM2TransWidget) )
            
            self.P2nsWidget=TILTMOTORGUI( motLat='P2_ns_Lat', motorTypeName0='A2V', motVert='P2_ns_Vert', motorTypeName1='A2V', nomWin='Tilt P2 ns'+self.laser, nomTilt='P2ns')
            self.P2ns.clicked.connect(lambda:self.open_widget(self.P2nsWidget) )
        
        self.PM1Tilt=TILTMOTORGUI( motLat='P'+self.laser+'_M1_Lat', motorTypeName0='A2V', motVert='P'+self.laser+'_M1_Vert', motorTypeName1='A2V', nomWin='Tilt P'+self.laser, nomTilt='P'+self.laser+' M1')
        self.PM1.clicked.connect(lambda:self.open_widget(self.PM1Tilt) )
        
        if self.laser=='1':   
            self.PM2Tilt=TILTMOTORGUI( motLat='P'+self.laser+'_M2_Lat', motorTypeName0='A2V', motVert='P'+self.laser+'_M2_Vert', motorTypeName1='RSAI', nomWin='Tilt P'+self.laser, nomTilt='P'+self.laser + 'M2')
            self.PM2.clicked.connect(lambda:self.open_widget(self.PM2Tilt) )
            print('')
        else:
            self.PM2Tilt=TILTMOTORGUI( motLat='P'+self.laser+'_M2_Lat', motorTypeName0='A2V', motVert='P'+self.laser+'_M2_Vert', motorTypeName1='A2V', nomWin='Tilt P'+self.laser, nomTilt='P'+self.laser + 'M2')
            self.PM2.clicked.connect(lambda:self.open_widget(self.PM2Tilt) )
            
        self.PReseauTransWidget=ONEMOTORGUI( mot='P'+self.laser+'_Reseau_Trans',motorTypeName0='RSAI',nomWin='control one motor:',showRef=False,unit=0,jogValue=50,parent=None)
        self.PReseauTrans.clicked.connect(lambda:self.open_widget(self.PReseauTransWidget) )
    
    def open_widget(self,fene):
        """ ouverture widget suplementaire 
        """
#        print(fene.isWinOpen)
           
        if fene.isWinOpen==False:
            print('open new')
            fene.startThread2()
            fene.setup
            fene.show()
            fene.isWinOpen=True
            
        else:
            
            fene.activateWindow()
            fene.raise_()
            fene.showNormal()
            
    def mouseReleaseEvent(self, QMouseEvent):
        print('(', QMouseEvent.x(), ', ', QMouseEvent.y(), ')')
#            
if __name__ == "__main__":
    
    appli = QApplication(sys.argv) 
    
    e = IMAGELASERP1(laser='2')#confMot='C:/Users/loa/Desktop/Princeton2019/')
    e.show()
    appli.exec_() 