rem clean CP2110 devices
DeviceCleanupCmd *VID_10C4*

rem clean VMware USB Device
rem DeviceCleanupCmd *Vid_0E0F*

rem clean FT230X
rem DeviceCleanupCmd *Vid_0403*

rem clean USB 2.0 Hub
rem DeviceCleanupCmd *VID_1A40*

rem clean qcc device
DeviceCleanupCmd.exe -s -n -e:"USBDevice" "*VID_0A12*"
DeviceCleanupCmd.exe -s -n "SWD\MMDEV*"
