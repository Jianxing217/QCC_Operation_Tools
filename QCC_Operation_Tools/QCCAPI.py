# -*- coding: utf-8 -*-
import os
import time
import re
import binascii
import ctypes
import ctypes.wintypes
import sys

#from ModuleTest_Tool.helpers import Singleton, AppError
from .helpers import Singleton, AppError

STRING_BUFFER_SIZE = 128

retVal_dict = {-1 : 'Invalid handle', 0:'Error', 1:'Success', 2:'Unsupported function'}

# Defines the protocol to be used when setting up the communication with the device
BCSP = 1  
USB = 2  
H4 = 4  
H5 = 8  
H4DS = 16  
PTAP = 64  
TRB = 128  
USBDBG = 256  


# Defines the key specifier
KEY_XTAL_FREQ_TRIM = "curator15:XtalFreqTrim"
KEY_BD_ADDRESS = "bt2:BD_ADDRESS"
KEY_DEVICE_NAME = "app5:DeviceName"
KEY_FeatureLicenseKey = "app3:FeatureLicenseKey"


# Defines the 3034 key specifier
KEY_3034_BD_ADDRESS = "bt2:PSKEY_BDADDR"
KEY_3034_DEVICE_NAME = "bt2:PSKEY_DEVICE_NAME"
KEY_3034_FeatureLicenseKey = "app2:FeatureLicenseKey"


class QCCAPIError(AppError):
    pass

#class SLABHIDDevice(with_metaclass(Singleton, object)):
class QCCUSBDevice():

    def __init__(self):
        self.qccLib = self.__getLib()
        self.usbHandle = 0
        self.comHandle = 0
        self.refport = 0
        self.dutport = 0

    def __getLib(self):

        # _environ = dict(os.environ)
        # _DIRNAME = os.path.dirname(os.path.abspath(__file__))
        # dll_path = os.path.join(_DIRNAME, "dlls", "QCC_BT")
        # os.environ['PATH'] += os.pathsep + dll_path
        # print (os.environ['PATH'])
        # _dll = ctypes.windll.LoadLibrary("TestEngine.dll")
        # print ("load library passed")
        # os.environ.clear()
        # os.environ.update(_environ)  

        _DIRNAME = os.path.dirname(os.path.abspath(sys.modules['__main__'].__file__))
        exe_path = os.path.join(_DIRNAME, "QCC_Operation_Tools","dlls", "QCC_BT","TestEngine.dll")
        # print(exe_path)
        _dll = ctypes.windll.LoadLibrary(exe_path)
        # print ("load library passed")

        return _dll

    #def _convert_str(self, buffer, length):
    #    return ''.join(map(chr, buffer[:length]))
    
    def openTestEngineUSB(self,DebugPort):
        if DebugPort[:3] =="TRB":
            transport_INT32 = ctypes.wintypes.DWORD(TRB) #TRB transport
            transportDevice_STR = DebugPort[3:]
        elif DebugPort[:6] == "USBDBG":
            transport_INT32 = ctypes.wintypes.DWORD(USBDBG) #USB transport
            transportDevice_STR = DebugPort[6:] 
        else:
             raise QCCAPIError("The dut_ble_port input format is incorrect!!!")
        
        dataRate_UNIT32 = ctypes.wintypes.DWORD(0) # baud rate
        retryTimeOut_UNIT32 = ctypes.wintypes.DWORD(5000) #5000 ms
        usbTimeOut_INT32 = ctypes.wintypes.DWORD(1000) #1000ms

        self.usbHandle = self.qccLib.openTestEngine(transport_INT32, transportDevice_STR, dataRate_UNIT32, retryTimeOut_UNIT32, usbTimeOut_INT32)
        if self.usbHandle == 0:  #try one more time
            # print ("Try one more time...")
            time.sleep(2)
            self.usbHandle = self.qccLib.openTestEngine(transport_INT32, transportDevice_STR, dataRate_UNIT32, retryTimeOut_UNIT32, usbTimeOut_INT32)
            if self.usbHandle == 0:
                raise QCCAPIError("openTestEngineUSB call failed")
        else:
            # print ("Test engine at sucessfully opened.")
            pass
  
    def closeTestEngine(self, deviceHandle):
        if deviceHandle != 0:
            value = self.qccLib.closeTestEngine(deviceHandle)
            if value != 1:
                raise QCCAPIError ("closeTestEngine call failed return value {}".format(retVal_dict[value]))

            # print ("Test engine at sucessfully close.")

    def teConfigCacheInit(self, deviceHandle, configDb):
        configFile = configDb.encode("utf-8")
        retVal = self.qccLib.teConfigCacheInit(deviceHandle, configFile)
        if retVal != 1:
            raise QCCAPIError ("ConfigCacheInit failed!")

    def teConfigCacheRead(self, deviceHandle):
        pathFile = None
        reserved_UINT16 = ctypes.wintypes.WORD(0)
        retVal = self.qccLib.teConfigCacheRead(deviceHandle, pathFile, reserved_UINT16)
        if retVal != 1:
            raise QCCAPIError ("ConfigCacheRead failed!")

    def teConfigCacheWrite(self, deviceHandle):
        pathFile = None
        reserved_UINT16 = ctypes.wintypes.WORD(0)
        retVal = self.qccLib.teConfigCacheWrite(deviceHandle, pathFile, reserved_UINT16)
        if retVal != 1:
            raise QCCAPIError ("ConfigCacheWrite call failed")

    def teConfigCacheWriteItem(self, deviceHandle,key,value):
        key = key.encode("utf-8")
        value = value.encode("utf-8")
        retVal = self.qccLib.teConfigCacheWriteItem(deviceHandle, key,value)
        if retVal != 1:
            raise QCCAPIError ("TeConfigCacheWriteItem call failed")
            

    def teConfigCacheReadItem(self, deviceHandle,key):
            value = []
            maxLen_UINT32 = ctypes.wintypes.DWORD(256)
            value_arry = (ctypes.c_char*256)()
            key = key.encode("utf-8")
            retVal = self.qccLib.teConfigCacheReadItem(deviceHandle, key, value_arry, ctypes.byref(maxLen_UINT32))
            if retVal != 1:
                raise QCCAPIError ("TeConfigCacheReadItem call failed")
            for item in range(0,256):
                value.append(value_arry[item])
            return value

    def teConfigCacheMerge(self, deviceHandle,file):
        pathFile = file
        retVal = self.qccLib.teConfigCacheMerge(deviceHandle, pathFile)
        if retVal != 1:
            raise QCCAPIError ("teConfigCacheMerge call failed")

    def teAppDisable(self, deviceHandle):
        reserved_UINT16 = ctypes.wintypes.WORD(0)
        retVal = self.qccLib.teAppDisable(deviceHandle, reserved_UINT16)
        if retVal != 1:
            raise QCCAPIError ("teAppDisable call failed")  

    def teRadTxCwStart(self, deviceHandle,channel,power):
        channel_UINT8 = ctypes.wintypes.BYTE(channel)
        power_UINT8 = ctypes.wintypes.BYTE(power)
        retVal = self.qccLib.teRadTxCwStart(deviceHandle, channel_UINT8,power_UINT8)
        if retVal != 1:
            raise QCCAPIError ("teRadTxCwStart call failed")

    def radiotestTxstart(self, deviceHandle, frequency, intPA, extPA, modulation):
    #deviceHandle coult be self.spiHandle (SPI) or self.comHandle (COM)
        freq_UINT16 = ctypes.wintypes.WORD(frequency)
        intPA_UINT16 = ctypes.wintypes.WORD(intPA)
        extPA_UINT16 = ctypes.wintypes.WORD(extPA)
        mod_UINT16 = ctypes.wintypes.WORD(modulation)

        retVal = self.qccLib.radiotestTxstart(deviceHandle,freq_UINT16, intPA_UINT16, extPA_UINT16, mod_UINT16 )
        if retVal != 1:
            raise QCCAPIError("radiotestTxstart call failed")

    def teRadStop(self,deviceHandle):
        retVal = self.qccLib.teRadStop(deviceHandle)
        if retVal != 1:
            raise QCCAPIError ("teRadStop call failed")  

    def radiotestPause(self, deviceHandle):
        retVal = self.qccLib.radiotestPause(deviceHandle)
        if retVal != 1:
            raise QCCAPIError("radiotestPause call failed")

    def teWriteBdAddr(self,deviceHandle,CFG_DB_PARAM,address):
            formatAddress = "[ "+ address[10:12]+" "+address[8:10]+" "+address[6:8]+" "+address[4:6]+" "+address[2:4]+" "+address[0:2]+" ]"
            self.teConfigCacheInit(deviceHandle,CFG_DB_PARAM)
            self.teConfigCacheRead(deviceHandle)
            self.teConfigCacheWriteItem(deviceHandle,KEY_BD_ADDRESS,formatAddress) 
            self.teConfigCacheWrite(deviceHandle)

    def teWriteFeatureLicenseKey(self,deviceHandle,CFG_DB_PARAM,LicenseKey):
            self.teConfigCacheInit(deviceHandle,CFG_DB_PARAM)
            self.teConfigCacheRead(deviceHandle)
            self.teConfigCacheWriteItem(deviceHandle,KEY_FeatureLicenseKey,LicenseKey) 
            self.teConfigCacheWrite(deviceHandle)
            
    def teWriteBdAddrAndLicenseKey(self,deviceHandle,CFG_DB_PARAM,address,LicenseKey):
            formatAddress = "[ "+ address[10:12]+" "+address[8:10]+" "+address[6:8]+" "+address[4:6]+" "+address[2:4]+" "+address[0:2]+" ]"
            self.teConfigCacheInit(deviceHandle,CFG_DB_PARAM)
            self.teConfigCacheRead(deviceHandle)
            self.teConfigCacheWriteItem(deviceHandle,KEY_BD_ADDRESS,formatAddress) 
            self.teConfigCacheWriteItem(deviceHandle,KEY_FeatureLicenseKey,LicenseKey) 
            self.teConfigCacheWrite(deviceHandle)

    def teReadLicenseKey(self,deviceHandle,CFG_DB_PARAM):
            self.teConfigCacheInit(deviceHandle,CFG_DB_PARAM)
            self.teConfigCacheRead(deviceHandle)
            LicenseKey = self.teConfigCacheReadItem(deviceHandle,KEY_FeatureLicenseKey) 
            self.teConfigCacheWrite(deviceHandle)
            LicenseKey = [x.decode('utf-8') for x in LicenseKey]
            LicenseKey = ''.join(LicenseKey)
            LicenseKey = LicenseKey.replace(" ","")
            LicenseKey = LicenseKey.replace("[","")
            LicenseKey = LicenseKey.replace("]","")
            LicenseKey = LicenseKey.rstrip("\x00")
            LicenseKey = LicenseKey.replace("\"","")
            return str(LicenseKey)

    def teReadBdAddrAndLicenseKey(self,deviceHandle,CFG_DB_PARAM):
            self.teConfigCacheInit(deviceHandle,CFG_DB_PARAM)
            self.teConfigCacheRead(deviceHandle)
            address = self.teConfigCacheReadItem(deviceHandle,KEY_BD_ADDRESS) 
            LicenseKey = self.teConfigCacheReadItem(deviceHandle,KEY_FeatureLicenseKey) 
            self.teConfigCacheWrite(deviceHandle)
            address = [x.decode('utf-8') for x in address]
            address = ''.join(address)
            address = address.replace(" ","")
            address = address.replace("[","")
            address = address.replace("]","")
            address = address.rstrip("\x00")
            address = address.replace("\"","")
            formatAddress = address[10:12]+address[8:10]+address[6:8]+address[4:6]+address[2:4]+address[0:2]
            LicenseKey = [x.decode('utf-8') for x in LicenseKey]
            LicenseKey = ''.join(LicenseKey)
            LicenseKey = LicenseKey.replace(" ","")
            LicenseKey = LicenseKey.replace("[","")
            LicenseKey = LicenseKey.replace("]","")
            LicenseKey = LicenseKey.rstrip("\x00")
            LicenseKey = LicenseKey.replace("\"","")
            return str(formatAddress),str(LicenseKey)

    def teReadFeatureLicenseKey(self,deviceHandle,CFG_DB_PARAM):
            self.teConfigCacheInit(deviceHandle,CFG_DB_PARAM)
            self.teConfigCacheRead(deviceHandle)
            LicenseKey = self.teConfigCacheReadItem(deviceHandle,KEY_FeatureLicenseKey) 
            self.teConfigCacheWrite(deviceHandle)
            LicenseKey = [x.decode('utf-8') for x in LicenseKey]
            LicenseKey = ''.join(LicenseKey)
            LicenseKey = LicenseKey.replace(" ","")
            LicenseKey = LicenseKey.replace("[","")
            LicenseKey = LicenseKey.replace("]","")
            LicenseKey = LicenseKey.rstrip("\x00")
            LicenseKey = LicenseKey.replace("\"","")
            return str(LicenseKey)

    def teReadBdAddr(self,deviceHandle,CFG_DB_PARAM):
            self.teConfigCacheInit(deviceHandle,CFG_DB_PARAM)
            self.teConfigCacheRead(deviceHandle)
            address = self.teConfigCacheReadItem(deviceHandle,KEY_BD_ADDRESS) 
            self.teConfigCacheWrite(deviceHandle)
            address = [x.decode('utf-8') for x in address]
            address = ''.join(address)
            address = address.replace(" ","")
            address = address.replace("[","")
            address = address.replace("]","")
            address = address.rstrip("\x00")
            address = address.replace("\"","")
            formatAddress = address[10:12]+address[8:10]+address[6:8]+address[4:6]+address[2:4]+address[0:2]
            return str(formatAddress)

    def setDeviceName(self,deviceHandle,CFG_DB_PARAM,name):
            name = "\""+name +"\""
            self.teConfigCacheInit(deviceHandle,CFG_DB_PARAM)
            self.teConfigCacheRead(deviceHandle)
            self.teConfigCacheWriteItem(deviceHandle,KEY_DEVICE_NAME,name) 
            self.teConfigCacheWrite(deviceHandle)

    def getDeviceName(self,deviceHandle,CFG_DB_PARAM):
            self.teConfigCacheInit(deviceHandle,CFG_DB_PARAM)
            self.teConfigCacheRead(deviceHandle)
            device_name = self.teConfigCacheReadItem(deviceHandle,KEY_DEVICE_NAME) 
            self.teConfigCacheWrite(deviceHandle)
            device_name = [x.decode('utf-8') for x in device_name]
            device_name = ''.join(device_name)
            device_name = device_name.rstrip("\x00")
            device_name = device_name.replace("\"","")
            return device_name

    def setXtalFreqTrim(self,deviceHandle,CFG_DB_PARAM,trimValue):
            self.teConfigCacheInit(deviceHandle,CFG_DB_PARAM)
            self.teConfigCacheRead(deviceHandle)            
            self.teConfigCacheWriteItem(deviceHandle,KEY_XTAL_FREQ_TRIM,trimValue)
            self.teConfigCacheWrite(deviceHandle)

    def getXtalFreqTrim(self,deviceHandle,CFG_DB_PARAM):
            self.teConfigCacheInit(deviceHandle,CFG_DB_PARAM)
            self.teConfigCacheRead(deviceHandle)
            trimValue = self.teConfigCacheReadItem(deviceHandle,KEY_XTAL_FREQ_TRIM) 
            self.teConfigCacheWrite(deviceHandle)
            return trimValue


    def teCheckLicense(self,deviceHandle,featureId):
        featureId_UINT8 = ctypes.wintypes.BYTE(featureId)
        result_UINT8 = (ctypes.wintypes.BYTE*1)(0)
        retVal = self.qccLib.teCheckLicense(deviceHandle,featureId_UINT8,result_UINT8)
        if retVal != 1:
            raise QCCAPIError("teCheckLicense call failed")
        return(result_UINT8[0])

    def teCheckLicenses(self,deviceHandle,featureIds):
        value_array = []
        numFeatureIds_UINT16 = ctypes.wintypes.WORD(len(featureIds))
        featureIds_UINT16 = (ctypes.wintypes.WORD* len(featureIds))()
        for item in range (0, len(featureIds)):
            featureIds_UINT16[item] = ctypes.wintypes.WORD(featureIds[item])
        result_UINT8 = (ctypes.wintypes.BYTE*len(featureIds))(0)
        retVal = self.qccLib.teCheckLicenses(deviceHandle,numFeatureIds_UINT16,featureIds_UINT16,result_UINT8)
        if retVal != 1:
            raise QCCAPIError("teCheckLicenses call failed")
        for item in range(0,len(featureIds)):
            value_array.append(result_UINT8[item])
        return value_array

    def teWrite3034FeatureLicenseKey(self,deviceHandle,CFG_DB_PARAM,LicenseKey):
            self.teConfigCacheInit(deviceHandle,CFG_DB_PARAM)
            self.teConfigCacheRead(deviceHandle)
            self.teConfigCacheWriteItem(deviceHandle,KEY_3034_FeatureLicenseKey,LicenseKey) 
            self.teConfigCacheWrite(deviceHandle)

    def teRead3034BdAddr(self,deviceHandle,CFG_DB_PARAM):
            self.teConfigCacheInit(deviceHandle,CFG_DB_PARAM)
            self.teConfigCacheRead(deviceHandle)
            address = self.teConfigCacheReadItem(deviceHandle,KEY_3034_BD_ADDRESS) 
            self.teConfigCacheWrite(deviceHandle)
            address = [x.decode('utf-8') for x in address]
            address = ''.join(address)
            address = address.replace(" ","")
            address = address.replace("[","")
            address = address.replace("]","")
            address = address.replace("{","")
            address = address.replace("}","")
            address = address.rstrip("\x00")
            address = address.replace("\"","")
            ListAddress = re.split(r'(?:,|;|s)s*', address)
            lap = '{:0>6s}'.format(ListAddress[0][2:])
            uap = '{:0>2s}'.format(ListAddress[1][2:])
            nap = '{:0>4s}'.format(ListAddress[2][2:])
            formatAddress = nap+uap+lap
            return str(formatAddress)

    def teWrite3034BdAddr(self,deviceHandle,CFG_DB_PARAM,address):
            formatAddress = "{ "+"0x"+ address[6:12]+", 0x"+address[4:6]+", 0x"+address[0:4]+" }"
            self.teConfigCacheInit(deviceHandle,CFG_DB_PARAM)
            self.teConfigCacheRead(deviceHandle)
            self.teConfigCacheWriteItem(deviceHandle,KEY_3034_BD_ADDRESS,formatAddress) 
            self.teConfigCacheWrite(deviceHandle)

    def set3034DeviceName(self,deviceHandle,CFG_DB_PARAM,name):
            name = "\""+name +"\""
            self.teConfigCacheInit(deviceHandle,CFG_DB_PARAM)
            self.teConfigCacheRead(deviceHandle)
            self.teConfigCacheWriteItem(deviceHandle,KEY_3034_DEVICE_NAME,name) 
            self.teConfigCacheWrite(deviceHandle)

    def get3034DeviceName(self,deviceHandle,CFG_DB_PARAM):
            self.teConfigCacheInit(deviceHandle,CFG_DB_PARAM)
            self.teConfigCacheRead(deviceHandle)
            device_name = self.teConfigCacheReadItem(deviceHandle,KEY_3034_DEVICE_NAME) 
            self.teConfigCacheWrite(deviceHandle)
            device_name = [x.decode('utf-8') for x in device_name]
            device_name = ''.join(device_name)
            device_name = device_name.rstrip("\x00")
            device_name = device_name.replace("\"","")
            return device_name

    #Set RX device to continuous receive
    def teRadRxPktCfg(self,deviceHandle,numPkts):
        numPkts_UINT16 = ctypes.wintypes.WORD(numPkts)
        retVal = self.qccLib.teRadRxPktCfg(deviceHandle,numPkts_UINT16)
        if retVal != 1:
            raise QCCAPIError ("teRadRxPktCfg call failed")  

    def teRadRxPktStart(self,deviceHandle,channels,payload,pktType,bdAddr,hopMode,pktLen,ltAddr):
        payload_UINT8 = ctypes.wintypes.BYTE(payload)
        pktType_UINT8 = ctypes.wintypes.BYTE(pktType)
        hopMode_UINT8 = ctypes.wintypes.BYTE(hopMode)
        pktLen_UINT16 = ctypes.wintypes.WORD(pktLen)
        ltAddr_UINT8 = ctypes.wintypes.BYTE(ltAddr)      
        reserved_UINT32 = ctypes.wintypes.DWORD(0) 
       
        channels_UINT8 = (ctypes.wintypes.BYTE * 1)()
        #print dataArray
        for item in range (0, 1):
            channels_UINT8[item] = ctypes.wintypes.BYTE(channels[item])

        retVal = self.qccLib.teRadRxPktStart(deviceHandle,channels_UINT8,payload_UINT8,pktType_UINT8,bdAddr,hopMode_UINT8,pktLen_UINT16,ltAddr_UINT8,reserved_UINT32)
        if retVal != 1:
            raise QCCAPIError ("teRadRxPktStart call failed")  

    def teChipReset(self,deviceHandle,mode):
        mode_UINT32 = ctypes.wintypes.DWORD(128)
        retVal = self.qccLib.teChipReset(deviceHandle,mode_UINT32)
        if retVal != 1:
            raise QCCAPIError("teChipReset call failed")


if __name__ == "__main__":
    import os
    import random

    LicenseKey = "[ 12 34 56 78 90 53 86 C2 24 1B C7 D2 7A 71 D4 62 9B 90 23 64 75 EF D0 35 5A 71 62 D3 45 B5 FA 4D AB EF C6 70 6E 5D C4 0E 76 C4 DE 5B B1 CA 08 D3 6E 79 B6 DD BD FA 61 65 58 F8 E0 98 C6 E6 2E 65 ]"

    CFG_DB_PARAM  = r"C:\GT-Tronics\MTT2\ModuleTest_Tool\ModuleTest_Tool\dlls\QCC_BT\hydracore_3034_config.sdb:QCC512X_CONFIG"
    # KEY_READ_BUFFER_LEN = ctypes.wintypes.DWORD(0)

    qccusb = QCCUSBDevice()
    qccusb.openTestEngineUSB("USBDBG100")

    # dataArray = []
    # qccusb.tePsRead(qccusb.usbHandle, PSKEY_BDADDR, 4, dataArray)
    # print dataArray

    serial = "123456789012"
    print("Writing CSR BDADDR... ")
    qccusb.teWrite3034BdAddr(qccusb.usbHandle,CFG_DB_PARAM,serial)
    # nap = int(serial[0:4], 16)
    # uap = int(serial[4:6], 16)
    # lap = int(serial[6:12], 16)
    # print nap, uap, lap
    # qccusb.psWriteBdAddr(qccusb.usbHandle, lap, uap, nap)

    # (lap,uap,nap) = qccusb.psReadBdAddr(qccusb.usbHandle)
    # readBackAddr = ("{:04X}{:02X}{:06X}".format(nap, uap, lap ))
    # print ("Read back address : {}".format(readBackAddr ))
    print("Writing CSR DeviceName....")
    qccusb.set3034DeviceName(qccusb.usbHandle,CFG_DB_PARAM,'NeckBand Recier v01')

    print("Reading CSR DeviceName....")
    qccusb.get3034DeviceName(qccusb.usbHandle,CFG_DB_PARAM)
    print("Reading CSR BDADR....")
    qccusb.teRead3034BdAddr(qccusb.usbHandle,CFG_DB_PARAM)
    #qccusb.teWriteFeatureLicenseKey(qccusb.usbHandle,CFG_DB_PARAM,LicenseKey)

    # qccusb.teConfigCacheInit(qccusb.usbHandle,CFG_DB_PARAM)
    # qccusb.teConfigCacheRead(qccusb.usbHandle)
    
    # #qccusb.teConfigCacheMerge(qccusb.usbHandle,"E:\\Work_File\\Software\\QCC_test\\dlls\\QCC_BT\\Mib.txt")
    # qccusb.teConfigCacheWriteItem(qccusb.usbHandle,KEY_XTAL_FREQ_TRIM, "5")

    # qccusb.teConfigCacheWriteItem(qccusb.usbHandle,KEY_BD_ADDRESS,"[ 00 11 22 33 aa bb]" ) 
    # qccusb.teConfigCacheWriteItem(qccusb.usbHandle,KEY_DEVICE_NAME,"\"QCC302X-Self_Left_v01\"" )  
    print("Write CSR LicenseKey....") 
    qccusb.teWrite3034FeatureLicenseKey(qccusb.usbHandle,CFG_DB_PARAM,LicenseKey ) 

    # qccusb.teConfigCacheReadItem(qccusb.usbHandle,KEY_BD_ADDRESS) 
    # qccusb.teConfigCacheReadItem(qccusb.usbHandle,KEY_DEVICE_NAME) 

    # qccusb.teConfigCacheWrite(qccusb.usbHandle)

    # qccusb.teAppDisable(qccusb.usbHandle)
    # qccusb.teRadTxCwStart(qccusb.usbHandle,39,6)

    # qccusb.teRadStop(qccusb.usbHandle)

    qccusb.teCheckLicense(qccusb.usbHandle,34)

    qccusb.teCheckLicenses(qccusb.usbHandle,[0,1,2,3,4,34])

    qccusb.closeTestEngine(qccusb.usbHandle)
