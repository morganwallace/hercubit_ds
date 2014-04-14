import serial
from time import time
from time import sleep
import settings
from ast import literal_eval
import os
import serial
from platform import system

t0=time()

def connect(bluetooth_enabled=True):
    conn_type=""
    if system()== 'Darwin': # Mac OSX
        
        ### FIRST TRY USB
        # USB
        possible_USBs=["/dev/tty.usbmodem1421","/dev/tty.usbmodem1411","/dev/tty.usbmodem1422","/dev/tty.usbmodemfd121","/dev/tty.usbmodemfd111","/dev/tty.usbmodemfd122"]
        for usb_path in possible_USBs:
            if os.path.exists(usb_path):
                print "Attempting to connect to "+usb_path+"...\n"
                SERIAL_PORT=usb_path
                SERIAL_SPEED=9600
                ser = serial.Serial(SERIAL_PORT, SERIAL_SPEED)
                conn_type="usb"
        
        if conn_type=="":
            print "No USB connection"

            if bluetooth_enabled==True: 
                try:
                    ####
                    # Bluetooth attempts to connect
                    ####
                    print "Attempting to connect to bluetooth...\n"
                    #SERIAL_PORTS=['/dev/tty.HC-06-DevB','/dev/tty.HC-06-DevB-1','/dev/tty.HC-06-DevB-2','/dev/tty.HC-06-DevB-3','/dev/tty.OpenPilot-BT-DevB']
                    SERIAL_PORTS=['/dev/tty.HC-06-DevB-2']
                    SERIAL_SPEED=57600
                    for port in SERIAL_PORTS:
                        try:
                            ser = serial.Serial(port, SERIAL_SPEED)
                            print"\nBluetooth Connected!"
                            conn_type="bluetooth"
                            SERIAL_PORT=port
                            break
                        except:
                            pass
                except:
                    print "No bluetooth connection"
                    pass
            else: #if bluetooth is not enabled
                print 'bluetooth disabled - change by passing "bluetooth_enabled=True" into device.connect()'


    elif system() =="Windows": # Windows * CHARLES- PLEASE FILL THIS IN
        try:
            # Bluetooth
            pass
        except:
            # USB
            pass


        
        
    try:
        ser
        print "using serial port:  " + SERIAL_PORT
    
    #Archive
    except:
     #if no serial connection available simulate with old file
        # import pickle
        print "\nNo serial connection available. Falling back on archived data..."
        conn_type="archive"
        backup_path=os.path.join('Python viz','saved_animations_and_data','backup','2014-03-14__15-36-14_bicep curl.csv')
        if os.getcwd()[os.getcwd().rfind('/'):]=='/Website2':   
            archive=os.path.join(os.path.dirname(os.getcwd()),backup_path)
            ser=open(archive)
        else:
            archive=os.getcwd()
            while archive[archive.rfind('/'):] != '/Fitness-Tracking':
                archive=os.path.dirname(archive)    
            archive=os.path.join(archive,backup_path)
            ser=open(archive)
        print archive
    return ser, conn_type



def sensor_stream(ser,conn_type,sensor="all", simulate_sample_rate=True):
    """Generator for streaming sensor data.
    If the argument is 'all' then Acceleromater, Gyro, and Magetometer data are
    all returned.
    Otherwise the argument will return just one type"""

    global t0, settings
    # Ensure we don't read too fastf
    while t0+settings.sampleRate>time():
        sleep(settings.sampleRate)
    t0=time()
    # ser, conn_type=connect(bluetooth_enabled=bluetooth_enabled)
    if conn_type =="archive":
        ser.readline()
        while True:
            line=ser.readline()
            if line is not None:
                if simulate_sample_rate==True: sleep(settings.sampleRate) # simulate actual sample rate
                s= [float(i) for i in line.split(",")[-10:]]
                formatted_sample= {'time':s[0],'accel':(s[1],s[2],s[3]),'gyro':(s[4],s[5],s[6]),'magnet':(s[7],s[8],s[9])}
                yield formatted_sample
            else: break
    else:
        while True:

            # Read a line from the serial port and convert it to a python dictioary object
            try:
                sample =literal_eval(ser.readline())
            except:
                sample= {'accel':(0,0,0),'gyro':(0,0,0),'magnet':(0,0,0)}            
            sample['time']=round(time(),2)
            # If just one sensor type is requested...
            if sensor !="all": # sensor could be 'accel', 'gyro', or 'magnet'
                yield list(sample[sensor])
            else: 
                yield sample
            


def run():
    """Use this code as the starting point 
    in scripts that import this module"""
    ser,conn_type=connect(bluetooth_enabled=True)
    sensor_generator=sensor_stream(ser,conn_type)
    while True:    
        print sensor_generator.next()

if __name__ == '__main__':
    run()
