#Settings for Hercubit

import os
import serial
from platform import system

####  #Serial Connection

#uncomment the following line to see all serial ports
# print serial.tools.list_ports()



# Note : bluetooth pairing code is '1234'

######  Peak Detection Preference Variables  ######
sampleRate=.100 #this should match the rate from the code on Arduino
max_rep_window=5 #seconds
min_rep_window=.4 #seconds
initialize_time=1 #second
dominant_axis=3