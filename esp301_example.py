'''
The "Python Example" given at https://www.newport.com/medias/sys_master/images/images/hd1/hec/8797091332126/ESP301-Command-Interface-Manual.pdf,
but with most of the bugs and typos ironed out, and updated to Python 3.8

Note that at the time of writing (06/01/2021), Python 3.9 is not compatible with pythonnet, so Python 3.8 must be used.
The clr module is NOT provided by the clr package, but rather the pythonnet package. Install this with pip.

This should work for you assuming you are using default settings and have installed the software from https://www.newport.com/p/ESP301-3N
You may need to change the instrumet port and/or the path to the Newport.ESP301.CommandInterface DLL.
Also note that axis 2 is used for the axis arguments here. Change this according to your setup.

All commands can be found in the "Command Interface Manual" at the above link.

Hopefully this ends up helping someone so they don't have to go through what I did.

DISCLAIMER: This code is essentially an adaptation of the example code provided by Newport. I do not claim to own any part of this,
and am solely providing it as a reference for those who may wish to control the ESP 301 controller with Python.
'''


#===================================================================== 
#Initialization Start 
#The script within Initialization Start and Initialization End  
#is needed for properly initializing Command  #Interface for ESP301 instrument. 
#The user should copy this code as is and specify correct paths here. 
import sys 

#Command Interface DLL can be found here. 
print("Adding location of Newport.ESP301.CommandInterface.dll to sys.path")
sys.path.append(r'C:\Newport\MotionControl\ESP301\Bin') 


# The CLR module provide functions for interacting with the underlying  
# .NET runtime 
import clr
# Add reference to assembly and import names from namespace
clr.AddReference("Newport.ESP301.CommandInterface") 

#from Newport.ESP301.CommandInterface import *
from CommandInterfaceESP301 import * 

import System 
#===================================================================== 
# Instrument Initialization 
# The key should have double slashes since 
# (one of them is escape character) 
instrument="COM4"  ##TODO: Change this to the applicable port for your device.
BAUDRATE = 921600 
print('Instrument Key=>', instrument)
# create an ESP301 instance 
ESP301Device = ESP301() 

# Open communication 
ret = ESP301Device.OpenInstrument(instrument, BAUDRATE);  
# Get positive software limit

#Due to the fact that we are using .NET functions, we still need to pass response and errString as arguments,
# even though we are also taking them as an output.
response = 0
errString = ""
result, response, errString = ESP301Device.SR_Get(2, response, errString)
if result == 0 : 
    print('positive software limit=>', response)
else:
    print('Error=>', errString, result)

# Get controller revision information
responseStr = ""; #We can't use 'response' for every response, as the data types are different
result, responseStr, errString = ESP301Device.VE(responseStr, errString) 
if result == 0 :
    print('controller revision=>', response)
else:
    print('Error=>',errString)

# Get current position 
result, response, errString = ESP301Device.TP(2, response, errString) 
if result == 0 : 
    print('position=>', response)
else: 
    print('Error=>',errString)

    
##Move the stage on axis 2 to a position of 10mm. All above methods do not actually modify the setup,
    #But this one does. 
'''
result, errString = ESP301Device.PA_Set(2, 10, errString)
if result == 0:
    print('position=>', response)
else:
    print('Error=>', errString)
'''

# Close communication 
ESP301Device.CloseInstrument();
