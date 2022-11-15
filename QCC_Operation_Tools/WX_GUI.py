# -*- coding: utf-8 -*-

###########################################################################
## Python code generated with wxFormBuilder (version 3.10.1-0-g8feb16b3)
## http://www.wxformbuilder.org/
##
## PLEASE DO *NOT* EDIT THIS FILE!
###########################################################################

import wx
import wx.xrc
import os
import re
import time
import _thread 
import datetime
import subprocess
from .customization import *
from .global_settings import g
from .QCC_Test_Flash_API import*
from wx.lib.masked import numctrl

###########################################################################
## Class MyFrame1
###########################################################################

class MyFrame1 ( wx.Frame ):

	def __init__( self, parent ):
		wx.Frame.__init__ ( self, parent, id = wx.ID_ANY, title = "QCC Operation Tools", pos = wx.DefaultPosition, size = wx.Size( 447,450 ), style = wx.DEFAULT_FRAME_STYLE^wx.MAXIMIZE_BOX^wx.RESIZE_BORDER^wx.TAB_TRAVERSAL )
		
		self.g = g()
		self.tempTxt = ""
		self.working = 0  #Show current idle status
		self.devicenumber = 1 
		self.portnumber = 0
		self.DeviceErrorsNumber = 0 
		self.firmware = None
		self.cst=Customization() 
		self.qccflashlib = QCCFlashSPIDevice()
		self.Version = self.qccflashlib.flmGetVersion()
		(self.portsBuf,self.transBuf,self.numPortFound) = self.qccflashlib.flGetAvailablePorts()
		
		self.devicenumber = int(self.numPortFound)

		self.DeviceList = self.portsBuf.decode('utf-8').split(",")
		self.DeviceList[-1] = self.DeviceList[-1].rstrip("\x00")

		self.gthome = 'b42000cbac182df71bb94274b05c7086'
		self.hanpin = '4fa19a04307608438d5cdbe477aacba0'
		self.sugaHK = 'd6524e4981511efcd261c0735735818c'
		self.default = '00000000000000000000000000000000'

		self.SetSizeHints( wx.DefaultSize, wx.DefaultSize )

		gbSizer1 = wx.GridBagSizer( 0, 0 )
		gbSizer1.SetFlexibleDirection( wx.BOTH )
		gbSizer1.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )

		chUSBDBGChoices = self.DeviceList
		self.chUSBDBG = wx.Choice( self, wx.ID_ANY, wx.DefaultPosition, wx.Size( 120,-1 ), chUSBDBGChoices, 0 )
		self.chUSBDBG.SetSelection( 0 )
		self.USBDBG = self.chUSBDBG.GetString(self.chUSBDBG.GetSelection())
		gbSizer1.Add( self.chUSBDBG, wx.GBPosition( 1, 1 ), wx.GBSpan( 1, 2 ), wx.ALL, 5 )

		self.stUSBDBG = wx.StaticText( self, wx.ID_ANY, u"USBDBG", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.stUSBDBG.Wrap( -1 )

		gbSizer1.Add( self.stUSBDBG, wx.GBPosition( 1, 0 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )

		self.stOperation = wx.StaticText( self, wx.ID_ANY, u"Operation", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.stOperation.Wrap( -1 )

		gbSizer1.Add( self.stOperation, wx.GBPosition( 2, 0 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )

		self.stProject = wx.StaticText( self, wx.ID_ANY, u"Project", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.stProject.Wrap( -1 )

		gbSizer1.Add( self.stProject, wx.GBPosition( 0, 0 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )

		chProjectChoices = [ u"1.default", u"2.gthome", u"3.hanpin", u"4.sugahk" ]
		self.chProject = wx.Choice( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, chProjectChoices, 0 )
		self.chProject.SetSelection( 0 )
		gbSizer1.Add( self.chProject, wx.GBPosition( 0, 1 ), wx.GBSpan( 1, 2 ), wx.ALL, 5 )

		chOperationChoices = [ u"1. Brun", u"2. Read  BtAddr", u"3. Write  BtAddr", u"4. Read BtName", u"5. Write BtName", u"6.Read License key", u"7.Write License key" ]
		self.chOperation = wx.Choice( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, chOperationChoices, 0 )
		self.chOperation.SetSelection( 0 )
		gbSizer1.Add( self.chOperation, wx.GBPosition( 2, 1 ), wx.GBSpan( 1, 2 ), wx.ALL, 5 )

		self.stContent = wx.StaticText( self, wx.ID_ANY, u"Content", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.stContent.Wrap( -1 )

		gbSizer1.Add( self.stContent, wx.GBPosition( 3, 0 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )

		self.teContent = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 330,-1 ), 0 )
		gbSizer1.Add( self.teContent, wx.GBPosition( 3, 1 ), wx.GBSpan( 1, 2 ), wx.ALL, 5 )

		self.teFilePath = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 330,-1 ), 0 )
		gbSizer1.Add( self.teFilePath, wx.GBPosition( 4, 1 ), wx.GBSpan( 1, 2 ), wx.ALL, 5 )

		self.buFilePath = wx.Button( self, wx.ID_ANY, u"FilePath", wx.DefaultPosition, wx.DefaultSize, 0 )
		gbSizer1.Add( self.buFilePath, wx.GBPosition( 4, 0 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )

		self.buRun = wx.Button( self, wx.ID_ANY, u"Run", wx.DefaultPosition, wx.Size( 80,50 ), 0 )
		self.buRun.SetFont( wx.Font( 20, wx.FONTFAMILY_ROMAN, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, wx.EmptyString ) )

		gbSizer1.Add( self.buRun, wx.GBPosition( 5, 0 ), wx.GBSpan( 2, 1 ), wx.ALL, 1 )

		self.stStatus = wx.StaticText( self, wx.ID_ANY, u"Status", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.stStatus.Wrap( -1 )

		gbSizer1.Add( self.stStatus, wx.GBPosition( 5, 1 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )

		self.stConnect = wx.StaticText( self, wx.ID_ANY, u"Connect", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.stConnect.Wrap( -1 )

		gbSizer1.Add( self.stConnect, wx.GBPosition( 5, 2 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )

		self.stProcess = wx.StaticText( self, wx.ID_ANY, u"Process", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.stProcess.Wrap( -1 )

		gbSizer1.Add( self.stProcess, wx.GBPosition( 6, 1 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )

		self.gaRun = wx.Gauge( self, wx.ID_ANY, 100, wx.DefaultPosition, wx.Size( 275,-1 ), wx.GA_HORIZONTAL )
		self.gaRun.SetValue( 0 )
		gbSizer1.Add( self.gaRun, wx.GBPosition( 6, 2 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )

		self.teShow = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 420,180 ), wx.TE_MULTILINE )
		gbSizer1.Add( self.teShow, wx.GBPosition( 7, 0 ), wx.GBSpan( 3, 3 ), wx.ALL, 5 )



		self.SetSizer( gbSizer1 )
		self.Layout()
		# self.Show(True)

		self.Centre( wx.BOTH )
		
		# Connect Events
		self.buFilePath.Bind( wx.EVT_BUTTON, self.ChoiceFilePath )
		self.buRun.Bind( wx.EVT_BUTTON, self.RunOperation )
		self.chUSBDBG.Bind( wx.EVT_CHOICE, self.ChoiceDevice )
		self.chOperation.Bind( wx.EVT_CHOICE, self.ChoiceOperation )
		self.chProject.Bind( wx.EVT_CHOICE, self.ChoiceProject )

	def __del__( self ):
		pass

	# Virtual event handlers, override them in your derived class

	def ChoiceProject(self,event0):
		if(self.chProject.GetString(self.chProject.GetSelection()) == "1.default"):
			self.changeFile(self.default)
			self.teShow.SetLabel("Project : default")
		elif(self.chProject.GetString(self.chProject.GetSelection()) == "2.gthome"):
			self.changeFile(self.gthome)
			self.teShow.SetLabel("Project : gthome")
		elif(self.chProject.GetString(self.chProject.GetSelection()) == "3.hanpin"):
			self.changeFile(self.hanpin)
			self.teShow.SetLabel("Project : hanpin")
		elif(self.chProject.GetString(self.chProject.GetSelection()) == "4.sugahk"):
			self.changeFile(self.gthome)
			self.teShow.SetLabel("Project : sugahk")

	def ChoiceDevice( self, event ):
		if  self.working == 0:
			self.qccflashlib.flmClose(self.devicenumber)
			#self.qccflashlib.flInit()
			self.qccflashlib = QCCFlashSPIDevice()
			(self.portsBuf,self.transBuf,self.numPortFound) = self.qccflashlib.flGetAvailablePorts()
			self.devicenumber = int(self.numPortFound)
			self.DeviceList = self.portsBuf.decode('utf-8').split(",")
			self.DeviceList[-1] = self.DeviceList[-1].rstrip("\x00")

			chUSBDBGChoices = self.DeviceList
			self.chUSBDBG.SetItems(chUSBDBGChoices)
			self.Refresh()
			# self.chUSBDBG = wx.Choice( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, chUSBDBGChoices, 0 )
			self.chUSBDBG.SetSelection( 0 )

		#self.RecoveryInterface()
		if self.chUSBDBG.GetString(self.chUSBDBG.GetSelection()) != " ":
			self.USBDBG = self.chUSBDBG.GetString(self.chUSBDBG.GetSelection())
			self.teShow.SetLabel(("Selected: "+ self.USBDBG))
			self.stConnect.SetLabel("Ready")
		else:
			self.stConnect.SetLabel("Connect")
		# if  self.working == 0:
		# 	#Clear GUI display data
		# 	#self.RecoveryInterface()
		# 	for i in range(8):
		# 		if i < self.devicenumber:
		# 			getattr(self, 'm_staticText' +str(i+3)).SetLabel(self.DeviceList[i]) 
		# 		else:
		# 			getattr(self, 'm_staticText' +str(i+3)).SetLabel("unknow") 

		# 	self.teShow.SetFont( wx.Font( 25, 70, 90, 90, False, wx.EmptyString ) ) 
		# self.teShow.SetForegroundColour('green')
		# self.teShow.SetLabel("DetectDrive refreshed successfully")
		# print("DetectDrive refreshed successfully")

	def ChoiceOperation( self, event ):
		if self.working == 0:
			self.working = 1
			self.teShow.SetLabel(("Operation: "+self.chOperation.GetString(self.chOperation.GetSelection())))
			self.working = 0

	def ChoiceFilePath( self, event ):
		if  self.working == 0:
			self.working = 1
			#Clear GUI display data
			# self.RecoveryInterface()
			#Specify read file type
			wildcard = "*.xuv|*.xuv|*.xpv|*.xpv" 
			dlg = wx.FileDialog(self, "Choose a file", os.getcwd(), "", wildcard, style = wx.FD_OPEN)

			if dlg.ShowModal() == wx.ID_OK:
				#Read successful return path 
				self.firmware = dlg.GetPath()
				self.teFilePath.SetLabel( self.firmware)
				dlg.Destroy() 
				# self.teShow.SetFont( wx.Font( 10, 70, 90, 90, False, wx.EmptyString ) ) 
				self.teShow.SetLabel("Select the burning file is:\n"+self.firmware)
				self.working = 0

	def changeFile(self,key):
		with open(r'C:\HCFData\key',"w") as f:
			f.write(key)	

	def DownloadProcess(self,firmware):
		if firmware == None:
					# self.teShow.SetFont( wx.Font( 15, 70, 90, 90, False, wx.EmptyString ) )
					# self.teShow.SetForegroundColour('red')
					self.teShow.SetLabel("\nPlease select the software you need to download!!!")
		else:
				#Turn on multi-burning
				Errordetect = []
				success = True
				StartTime = datetime.datetime.now()
				if(self.qccflashlib.flmOpen(self.devicenumber) == False):
					for i in range(self.devicenumber):
						Error = self.qccflashlib.flmGetDeviceError(i)
						self.qccflashlib.flmClose(self.devicenumber)
						self.teShow.SetLabel((Error))
					# 	if Error != 0:
					# 		getattr(self, 'teShow' +str(i+3)).SetForegroundColour( wx.Colour( 255, 0, 0 ) )
					# 		getattr(self, 'm_staticText' +str(i+3)).SetLabel(self.DeviceList[i])
					# 		Errordetect.append((self.DeviceList[i])[:16])
					# self.m_staticText1.SetForegroundColour( wx.Colour( 255, 0, 0 ) )
					# self.m_staticText1.SetFont( wx.Font( 10, 70, 90, 90, False, wx.EmptyString ) )
					# self.m_staticText1.SetLabel('Connection chip error.\nError Number:'+str(Errordetect)[:80]+'\n                     '+str(Errordetect)[80:])

				else:
					msg = "flmOpem successfully"
					self.teShow.SetLabel((msg))

					if(self.qccflashlib.flmReadProgramFiles(firmware.encode('utf-8')) != True):
						msg = "flmReadProgramFiles faild"
						self.teShow.SetLabel((msg))
						success = False

					if(self.qccflashlib.flmSetFlashType(self.devicenumber) != True):
							msg = "lSetFlashType faild"
							self.teShow.SetLabel((msg))
							success = False

					if(self.qccflashlib.flmSetSubsysBank(self.devicenumber) != True):
							msg = "flmSetSubsysBank faild"
							self.teShow.SetLabel((msg))
							success = False

					if(self.qccflashlib.flmProgramSpawn(self.devicenumber) != True):
						self.qccflashlib.flmClose(self.devicenumber)
						msg = "flmProgramSpawn faild"
						self.teShow.SetLabel((msg))
						success = False
						#self.m_staticText1.SetLabel("Download all Fail")

					if success :
						#Get the download progress bar
						ProgressValue = 0
						ProgressStop = False
						#Determine if all burning processes are 100%
						while ProgressStop== False :
							self.working = 1
							for i in range(self.devicenumber):
								time.sleep(0.3)
								ProgressValue  +=self.qccflashlib.flmGetDeviceProgress(i) 
								#Get progress parameters and set progress bar
								getattr(self, 'gaRun').SetValue(self.qccflashlib.flmGetDeviceProgress(i)) 
							#Get the total number of running processes
							if ProgressValue == (i+1)*100:
								ProgressStop= True
							ProgressValue = 0
						DeviceErrors = locals()
						#Access programming error drive
						ErrorText = []
						for i in range(self.devicenumber):
							DeviceErrors['Device_%s' % i] = self.qccflashlib.flmGetDeviceError(i)
							# print ("%s = %s"%(self.DeviceList[i],DeviceErrors['Device_%s' % i] ))
							#Determine if the returned value is 0
							if DeviceErrors['Device_%s' % i] != 0:
								#Error drive number plus 1
								self.DeviceErrorsNumber += 1
								# rint(self.DeviceList[i]+" Download Faild")
								#Error driver added to list
								# ErrorText.append((self.DeviceList[i]))
								# getattr(self, 'm_staticText' +str(i+3)).SetForegroundColour( wx.Colour( 255, 0, 0 ) )
								# getattr(self, 'm_staticText' +str(i+3)).SetLabel(self.DeviceList[i])
								# getattr(self, 'm_gauge' +str(i+1)).SetValue(0)     

						self.qccflashlib.flmClose(self.devicenumber)

						ListError = list(set(ErrorText))
						EndTime = datetime.datetime.now()
						alltime = (EndTime-StartTime).seconds
						if self.DeviceErrorsNumber != 0:
							#Set the text font size displayed by the GUI interface
							# self.teShow.SetFont( wx.Font( 10, 70, 90, 90, False, wx.EmptyString ) )
							# self.teShow.SetForegroundColour('blue')
							self.teShow.SetLabel('Download completed.\nError Number:'+str(ListError))
						else:
							# self.teShow.SetFont( wx.Font( 25, 70, 90, 90, False, wx.EmptyString ) )
							# self.teShow.SetForegroundColour('green')
							self.teShow.SetLabel("Download all passed. Spend time = "+str(alltime))



							self.DeviceErrorsNumber = 0 
							self.working = 0

					else:
						#Set the text font size displayed by the GUI interface
						# self.teShow.SetFont( wx.Font( 25, 70, 90, 90, False, wx.EmptyString ) )
						#self.teShow.SetForegroundColour('red')
						self.teShow.SetLabel('Download Faild!!!')
						self.qccflashlib.flmClose(self.devicenumber)

	def RunOperation( self, event ):
		if self.working == 0:
			self.working = 1
			getattr(self, 'gaRun').SetValue(0) 
			if(self.chOperation.GetString(self.chOperation.GetSelection()) == "1. Brun"):
				msg = "1. Brun"
				self.teShow.SetLabel((msg))
				try:
					_thread.start_new_thread(self.DownloadProcess,(self.firmware,))
				finally:
					self.working = 0

			elif (self.chOperation.GetString(self.chOperation.GetSelection()) == "2. Read  BtAddr"):
				msg = "2. Read  BtAddr"
				self.teShow.SetLabel((msg))
				try:
					qccLib = QCCUSBDevice()
					cfg_db_parm = "hydracore_config.sdb:QCC515X_CONFIG"

					qccLib.openTestEngineUSB("USBDBG100") 
					readBackAddr = qccLib.teReadBdAddr(qccLib.usbHandle,cfg_db_parm)

					self.teShow.SetLabel(("BtAddr : "+ readBackAddr))
					# g.serial = readBackAddr

					# msg = "readBackAdd : "+ readBackAddr
					# printGREEN('\n> ' + msg + '\n')
					# logger.info("%s,%s,%s,\"%s\"", module, g.station, g.serial, msg)
					# msg  = "readBackLicenseKey : "+ readBackLicense[:8] + "******"
					# printGREEN('> ' + msg+'\n')  
					# logger.info("%s,%s,%s,\"%s\"", module, g.station, g.serial, msg)

				except:
					msg = u'Faild Read Address and LicenseKey'
					self.teShow.SetLabel((msg))
					# logger.info("%s,%s,%s,\"%s\"", module, g.station, g.serial, msg) 
					# return [0, msg]   

				finally:
					qccLib.closeTestEngine(qccLib.usbHandle)
					self.working = 0

			elif (self.chOperation.GetString(self.chOperation.GetSelection()) == "3. Write  BtAddr"):
				address = self.teContent.GetValue()
				rex = re.compile('^[A-Fa-f0-9]{12}$')
				if rex.match(address):
					msg = "3. Write  BtAddr"
					self.teShow.SetLabel((msg))
					try:
						qccLib = QCCUSBDevice()
						cfg_db_parm = "hydracore_config.sdb:QCC515X_CONFIG"

						qccLib.openTestEngineUSB("USBDBG100") 
						qccLib.teWriteBdAddr(qccLib.usbHandle,cfg_db_parm,address)

						self.teShow.SetLabel(("Writing the address succeeded"))

					except:
						msg = u'Faild Write Address'
						self.teShow.SetLabel((msg))
						# logger.info("%s,%s,%s,\"%s\"", module, g.station, g.serial, msg) 
						# return [0, msg]   

					finally:
						qccLib.closeTestEngine(qccLib.usbHandle)
						self.working = 0
				else:
						msg = u'Please enter the Bluetooth address correctly!'
						self.teShow.SetLabel((msg))
						self.working = 0

			elif (self.chOperation.GetString(self.chOperation.GetSelection()) == "4. Read BtName"):
				msg = "4. Read BtName"
				self.teShow.SetLabel((msg))
				try:
					qccLib = QCCUSBDevice()
					cfg_db_parm = "hydracore_config.sdb:QCC515X_CONFIG"

					qccLib.openTestEngineUSB("USBDBG100") 
					readBackBtName = qccLib.getDeviceName(qccLib.usbHandle,cfg_db_parm)

					self.teShow.SetLabel(("BtName : "+ readBackBtName))

				except:
					msg = u'Faild Read BtName'
					self.teShow.SetLabel((msg))
					# logger.info("%s,%s,%s,\"%s\"", module, g.station, g.serial, msg) 
					# return [0, msg]   

				finally:
					qccLib.closeTestEngine(qccLib.usbHandle)
					self.working = 0

			elif (self.chOperation.GetString(self.chOperation.GetSelection()) == "5. Write BtName"):
				BtName = self.teContent.GetValue()
				if(BtName != ""):
					msg = "5. Write  BtName"
					self.teShow.SetLabel((msg))
					try:
						qccLib = QCCUSBDevice()
						cfg_db_parm = "hydracore_config.sdb:QCC515X_CONFIG"

						qccLib.openTestEngineUSB("USBDBG100") 
						qccLib.setDeviceName(qccLib.usbHandle,cfg_db_parm,BtName)

						self.teShow.SetLabel(("Writing the BtName succeeded"))

					except:
						msg = u'Faild Write BtName'
						self.teShow.SetLabel((msg))  

					finally:
						qccLib.closeTestEngine(qccLib.usbHandle)
						self.working = 0
				else:
						msg = u'Please enter the BtName correctly!'
						self.teShow.SetLabel((msg))
						self.working = 0

			elif (self.chOperation.GetString(self.chOperation.GetSelection()) == "6.Read License key"):
				msg = "6.Read License key"
				self.teShow.SetLabel((msg))
				try:
					qccLib = QCCUSBDevice()
					cfg_db_parm = "hydracore_config.sdb:QCC515X_CONFIG"

					qccLib.openTestEngineUSB("USBDBG100") 
					readBackLicenseKey = qccLib.teReadLicenseKey(qccLib.usbHandle,cfg_db_parm)

					self.teShow.SetLabel(("License key : "+ readBackLicenseKey))

				except:
					msg = u'Faild Read LicenseKey'
					self.teShow.SetLabel((msg))

				finally:
					qccLib.closeTestEngine(qccLib.usbHandle)
					self.working = 0

			elif (self.chOperation.GetString(self.chOperation.GetSelection()) == "7.Write License key"):
				LicenseKey = self.teContent.GetValue()
				if(LicenseKey != ""):
					msg = "7.Write License key"
					self.teShow.SetLabel((msg))
					LicenseKey = "["+LicenseKey+"]"
					try:
						qccLib = QCCUSBDevice()
						cfg_db_parm = "hydracore_config.sdb:QCC515X_CONFIG"

						qccLib.openTestEngineUSB("USBDBG100") 
						qccLib.teWriteFeatureLicenseKey(qccLib.usbHandle,cfg_db_parm,LicenseKey)

						self.teShow.SetLabel(("Writing the License key succeeded"))

					except:
						msg = u'Faild Write License key'
						self.teShow.SetLabel((msg))  

					finally:
						qccLib.closeTestEngine(qccLib.usbHandle)
						self.working = 0
				else:
						msg = u'Please enter the License key correctly!'
						self.teShow.SetLabel((msg))
						self.working = 0

if __name__ == '__main__':
  ex = wx.App() 
  WX_GUI = MyFrame1(None) 
  ex.MainLoop()

