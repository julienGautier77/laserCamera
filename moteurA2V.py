# -*- coding: utf-8 -*-
"""
Created on Wed Feb 28 11:43:51 2018
Pilotage des controleurs A2V TMCM via USB 
Pyserial
python 3.X pyQT5
@author: Gautier julien loa
"""


#%% Imports
from serial import Serial
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtCore import QSettings

from PyQt5 import QtCore
import time


#%% rack initialisation et connexion des racks logiciel TMCL verifier un par un que les ports com sont les bons.
#print('start')
portA='com28' 

mysA=Serial(port=portA,baudrate=115200,timeout=5)
confA2V=QSettings('fichiersConfig/configMoteurA2V.ini', QSettings.IniFormat) # motor configuration  files
mutexA=QtCore.QMutex()

def connectA():
    """
    ouverture du port A
    """
    
#    mysA.port=portA
#    mysA.timeout=1
#    mysA.Baudrate=115200
    if mysA.is_open==False:
        print('open port',portA)
        mysA.open()
    else:
        mysA.close()
        time.sleep(0.1)
        mysA.open()
    if mysA.is_open==True:
        print ('TMCM pepita A connected on port :',portA)
    else: print('TMCM pepita A on port',portA,' not connected')

try :
    
    connectA()
except:
    print( "Error connexion A2V rack A")
    msg = QMessageBox()
    msg.setIcon(QMessageBox.Critical)
    msg.setText("Error connexion A2V")
    msg.setInformativeText("Error connexion A2V rack A please chcek connexion or restart computeur")
    msg.setWindowTitle("Warning ...")
    msg.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
    msg.exec_()
    pass


def stopConnexion():
    
    if mysA.is_open==True:
        try :
            mysA.close()
        except:
            print('error closing', portA)
            pass
    print ("rack A2V disconnected")
    

#%% fonction for send and receive data    
def sendCommand(instruction, instr_type, mii, values_list,idRack=0x01):
    """
    Envoyer une commande au controleur
    'ROR':1, 'ROL':2, 'MST':3, 'MVP':4, 'SAP':5, 'GAP':6,
            'STAP':7, 'RSAP':8, 'SGP':9, 'GGP':10, 'RFS':13, 'SIO':14, 'GIO':15, 'WAIT':27, 'STOP':28,
                'SCO':30, 'GCO':31, 'CCO':32, 'VER':136, 'RST':255}
    """
    
    if len(values_list) > 4:
        print ("Command error: "+str(values_list).encode('hex'))
    idRack=int(idRack)   
    cmd = bytearray([idRack, instruction, instr_type, mii, 0x00, 0x00, 0x00, 0x00, 0x00])
    values_list.reverse()
    ii = 7
    for vii in values_list:
        cmd[ii] =( vii)
        ii = ii-1

        cmd[8] = sum(cmd[0:8])&0xff
   
    mutexA.lock()
    
    mysA.write(cmd)
    time.sleep(0.02)
    
    out = mysA.read(9)
    
    # time.sleep(0.02)
    mutexA.unlock()
    return bytearray(out)
    
    
    
def Format(value):
    """
    Met au format hex la valuer de la commande"
    """
    return [(value>>24), ((value>>16)&0xff), ((value>>8)&0xff), (value&0xff)]



#%% initialisation of all the motor

def ini(motor=0):
    """ intitialisation of one motor
    
    """
#    print('init',motor)
    Vmax=int(confA2V.value(motor+'/Vmax'))#1142
    Cmax=int(confA2V.value(motor+'/Cmax'))
    Cstby=int(confA2V.value(motor+'/Cstandby'))
    pulseD=int(confA2V.value(motor+'/PulseDiv'))
    rampD=int(confA2V.value(motor+'/RampDiv'))
    Amax=int(confA2V.value(motor+'/AccMax'))
    stepResol=int(confA2V.value(motor+'/stepResolution')) # step resolution (0-8)
    Mot=int(confA2V.value(motor+'/numMoteur'))
    rack=confA2V.value(motor+'/rack')
    
    cmd=5 # Set Axis parameter 
    Type=6 # max current
    value = Format(Cmax)
    sendCommand(cmd,Type,Mot,value,rack)

    cmd=5 # Set Axis parameter 
    Type=7 # standby current
    value = Format(Cstby)
    sendCommand(cmd,Type,Mot,value,rack)

    cmd=5 # Set Axis parameter 
    Type=4 # MAx speed
    value =Format(Vmax)
    #print value
    sendCommand(cmd,Type,Mot,value,rack)

    cmd=5 # Set Axis parameter 
    Type=4 # MAx acc
    value =Format(Amax)
    #print value
    sendCommand(cmd,Type,Mot,value,rack)
    
    cmd=5 # Set Axis parameter 
    Type=154 # pulse divisor 154
    value =Format(pulseD)
    #print value
    sendCommand(cmd,Type,Mot,value,rack)

    cmd=5 # Set Axis parameter 
    Type=153 # ramp divisor 153
    value =Format(rampD)
    #print value
    sendCommand(cmd,Type,Mot,value,rack)

    cmd=5 # Set Axis parameter 
    Type=12 # right limit switch disable
    value =Format(1)# disable
    #print value
    sendCommand(cmd,Type,Mot,value,rack)

    cmd=5 # Set Axis parameter 
    Type=13 # left limit switch disable
    value =Format(1) # disable
    #print value
    sendCommand(cmd,Type,Mot,value,rack)

    cmd=5 # Set Axis parameter 
    Type=140 # set step resolution
    value=Format(stepResol) # entre 0 et 8 = entre 1 et 256
    sendCommand(cmd,Type,Mot,value,rack)
#    print (" motor A2V inititalisation :  ",motor)
    
def iniTot():
    """ initialisation of all the motor present in the config.ini file
    """
    print('intialisation of all A2V motors ...')
    print('Wait ....')
    groups=confA2V.childGroups()
    i='.'
    for vi in groups:
        time.sleep(0.05)
        print(vi,i,end="\n")
        ini(vi)
       
        i=i+'.'
    print("")
    print('initialisation A2V :OK')
    
iniTot() # initialisation de tous les moteurs        
        
#%% class A2V motor
class MOTORA2V():
    
    def __init__(self, mot1='',parent=None):
        #super(MOTORA2V, self).__init__()
        self.moteurname=mot1
        self.numMoteur=int(confA2V.value(self.moteurname+'/numMoteur'))
        self.rack=confA2V.value(self.moteurname+'/rack')
        self.hyst=str(confA2V.value(self.moteurname+'/hyst'))
        self.hystValue=int(confA2V.value(self.moteurname+'/hystValue'))
   
    def position(self):
        """
        position du motor"
        """
        cmd=6
        Type=1
        value=[0]
        
        out2 = sendCommand(cmd,Type,self.numMoteur,value,self.rack)
        #out2 = receiveData()
        # if len(value) > 4:
        #     print ("Command error: "+str(value).encode('hex'))
        # idRack=int(self.rack)   
        # instruction=cmd
        # instr_type=Type
        # mii=self.numMoteur
        # cmd = bytearray([idRack, instruction, instr_type, mii, 0x00, 0x00, 0x00, 0x00, 0x00])
        # value.reverse()
        # ii = 7
        # for vii in value:
        #     cmd[ii] =( vii)
        # ii = ii-1

        # cmd[8] = sum(cmd[0:8])&0xff
   
        # mutexA.lock()
        # mysA.write(cmd)
        # time.sleep(0.02)
        # out = mysA.read(9)
        # out2=bytearray(out)
        # # time.sleep(0.02)
        # mutexA.unlock()
        
        try:
            pos= int(out2[4]<<24) + int(out2[5]<<16) + int(out2[6]<<8) + int(out2[7])
        except:
            pos=0
        if  pos> 0x80000000:
            pos = pos - 0xffffffff
        return int(pos)  
    
    def move(self,pos=0,vitesse=10000):
        cmd=4 #(MVP Move to position"#
        Type=0 # Abolute
        pos=int(pos)
        print (self.moteurname, "move to",pos)
        if pos >2000000000 or pos<-2000000000 :
            print ( "number of step to high")
        else :
            if pos < 0: pos = pos+0xffffffff
            value = Format(pos)
            sendCommand(cmd,Type,self.numMoteur,value,self.rack)
    
    def rmove(self,pos=0,vitesse=10000):
        cmd = 4
        Type = 1
        if self.hyst=='+' and pos<0:
            pos=pos-self.hystValue
#            print('hyst + et pos <0 ',pos)
        if self.hyst=='-' and pos>0: 
            pos=pos+self.hystValue
#            print('hyst - et pos >0 ',pos)
        if pos>=0:
            self.hyst='+'
            
        if pos<=0:
            self.hyst='-'    
        
        pos=int(pos)
        if pos >2000000000 or pos<-2000000000 :
            print ("number of step to high")
        else :
            print (self.moteurname, "relative move of ",pos )
            if pos < 0: pos = pos+0xffffffff
            value = Format(pos)
            confA2V.setValue(self.moteurname+'/hyst',self.hyst)
            sendCommand(cmd,Type,self.numMoteur,value,self.rack)
       
            

    def stopMotor(self):
        cmd = 3 # "Motor stop"
        Type = 0
        value =Format(0)
        sendCommand(cmd,Type,self.numMoteur,value,self.rack)
        print (self.moteurname,"stopped")

    def setzero(self):
        print ("motor",self.moteurname,"set to Zero")
        cmd= 5 #set Axis Parameter
        Type= 1 # Set Actual Postion Bizarre ....
        value = [0]
        sendCommand(cmd,Type,self.numMoteur,value,self.rack)


#if __name__ == "__main__":
#    print("test")


#%% not used: 
    

##def sendCommand(cmd,Type,motor,value):
##    adr = 1
##    tmp = struct.pack('BBBBi', adr, cmd, Type, motor, value)
##    checksum=sum(struct.unpack('BBBBBBBB',tmp))
##    TxBuffer=struct.pack('>BBBBiB',adr,cmd,Type,motor,value,checksum)
##    print TxBuffer 
##    return mys.write(TxBuffer)

#def receiveData():
#    RxBuffer = mys.read(9)
#    if RxBuffer.__len__() == 9:
#        data = struct.unpack('>BBBBiB', RxBuffer)
#        
#        return data
#    else:
#        print ("error recieve data A2V")
        
#def allPosition():
#groups=confA2V.childGroups()
#M={}
#for vi in groups:
#    time.sleep(0.05)
#    M[str(vi)]=position(vi)
#foldername=time.strftime("%Y_%m_%d")
#if not os.path.isdir(foldername):
#        os.mkdir(foldername)
#fichier=open(foldername+'/'+'sauvPosition.txt','a')
#fichier.write(time.strftime("%A %d %B %Y %H:%M:%S"))
#fichier.write(repr(M))
#fichier.write("\n")
#fichier.close()         
#return M