@echo off
title RegistryCleanup


:: Check for elevated priviledge
:: Raise request if not exists
setlocal
set uac=~uac_permission_tmp_%random%
md "%SystemRoot%\system32\%uac%" 2>nul
if %errorlevel%==0 ( rd "%SystemRoot%\system32\%uac%" >nul 2>nul ) else (
    echo set uac = CreateObject^("Shell.Application"^)>"%temp%\%uac%.vbs"
    echo uac.ShellExecute "%~s0","","","runas",1 >>"%temp%\%uac%.vbs"
    echo WScript.Quit >>"%temp%\%uac%.vbs"
    "%temp%\%uac%.vbs" /f
    del /f /q "%temp%\%uac%.vbs" & exit )
endlocal


:: Start installation
DeviceCleanupCmd.exe -s -n -e:"USBDevice" "*VID_0A12*"
DeviceCleanupCmd.exe -s -n "SWD\MMDEV*"
DeviceCleanupCmd.exe -s -n "HYDRA\PRO_*"
DeviceCleanupCmd.exe -s -n "HID\VID_0A12*"


:end
@echo on
rem exit
