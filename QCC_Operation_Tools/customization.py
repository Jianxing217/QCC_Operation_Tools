# -*- coding: utf-8 -*-
from six import with_metaclass
from collections import Counter
from .helpers import AppError, Singleton
from .global_settings import g
from .QCCAPI import QCCUSBDevice 
import time


class CustomizationError(AppError):
    pass


class Customization(with_metaclass(Singleton, object)):

    def __init__(self):
        self.g = g()
        self.qcclib = QCCUSBDevice()

        # End __init__
        # -------------------------------------------------------------------------

    def init_csr_module(self):
        print ("init_qcc_module")


    def ReadSpiPort(self,portnumber):
        print ("read usb port:")
        self.qcclib = QCCUSBDevice()
        self.qcclib.openTestEngineUSB(portnumber)
        self.qcclib.dutport = self.qcclib.usbHandle
        return self.qcclib.dutport

    def writeSerial(self,nap, uap, lap,portnumber):
        
        try:
            self.qccLib = QCCUSBDevice()
            dut_ble_port = portnumber
            cfg_db_parm = "hydracore_config.sdb:QCC515X_CONFIG"

            print(("Opening USB port for DUT:"+dut_ble_port))

            if(self.qccLib.openTestEngineUSB(dut_ble_port) == False):
                return False

            print("Writin QCC BDADDR... ")      
            QCC_BDADDR = str(nap+uap+lap)
            # self.qccLib.teConfigCacheWriteItem(self.qccLib.dutport,KEY_BD_ADDRESS,QCC_BDADDR) 
            #QCC_BDADDR = "aabbccddeeff"
            self.qccLib.teWriteBdAddr(self.qccLib.usbHandle,cfg_db_parm,QCC_BDADDR)

            #Verification if the input address is correct
            readBackAddr = self.qccLib.teReadBdAddr(self.qccLib.usbHandle,cfg_db_parm)
            print(("Read back address : {}".format(readBackAddr )))       
            if readBackAddr.upper() == QCC_BDADDR.upper():
                print ("Verification OK")
                self.IncrementSerial()
                self.qccLib.closeTestEngine(self.qccLib.usbHandle)
                return True

            else:
                print("Verification Fail")
                msg = '(0x21006) Write address error BT-ADDR:[' + str(self.g.serial) + ']'
                self.qccLib.closeTestEngine(self.qccLib.usbHandle)
                print(msg)
                return False
        except Exception as e:
            print("Opening USB port Fail!!!")
            self.qccLib.closeTestEngine(self.qccLib.usbHandle)
            return False


    def IncrementSerial(self):     
        self.g.serial = "{:012x}".format(int(self.g.serial, 16) + 1)


    def ReadSerial(self,portnumber):
        try:
            self.qccLib = QCCUSBDevice()
            dut_ble_port = portnumber
            cfg_db_parm = "hydracore_config.sdb:QCC515X_CONFIG"
            print(("Opening USB port for DUT:"+dut_ble_port))
            if(self.qccLib.openTestEngineUSB(dut_ble_port) == False):
                return False

            readBackAddr = self.qccLib.teReadBdAddr(self.qccLib.usbHandle,cfg_db_parm)
            print(("Read back address : {}".format(readBackAddr )))       
            nap = readBackAddr[0:4]
            uap = readBackAddr[4:6]
            lap = readBackAddr[6:12] 

        except Exception as e:
            nap = 0
            uap = 0
            lap = 0
            print("Opening USB port Fail!!!")

        finally:
            self.qccLib.closeTestEngine(self.qccLib.usbHandle)
            return (nap,uap,lap)

            


        