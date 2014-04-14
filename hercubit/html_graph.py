from __future__ import division
import serial
import time
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import pickle
from os.path import join
import csv
import time
from hercubit import settings
from hercubit import device 
import mpld3


fig, ax = plt.subplots(3, sharex=True)
fig.subplots_adjust(hspace=.10)
fig.set_size_inches(4,4)
plots={'accel':ax[0],'gyro':ax[1],'magnet':ax[2]}

#Setup lines in graph
sensors=('accel','gyro','magnet')
axes=('x','y','z')
colors=('-r','-g','-b')
lines={}
for sensor in sensors:
    lines[sensor]={}
    for axis in axes:
        i=axes.index(axis)
        # print sensor+"("+axis+") : "+colors[i]
        lines[sensor][axis]=ax[sensors.index(sensor)].plot([], [],colors[i], lw=1)


for i in range(len(axes)):
    ax[i].grid()
    ax[i].set_xlim(0, 20)

ax[0].set_ylim(-2, 2)
ax[1].set_ylim(-30000, 30000)
ax[2].set_ylim(-2000, 2000)


ax[0].set_ylabel('acceleration (g)')
ax[1].set_ylabel('gyro (degrees/sec)')
ax[2].set_ylabel('magnetometer')
ax[2].set_xlabel('time (s)')

tdata=[]
all_data={}
for sensor in sensors:
    all_data[sensor]={'x':[],'y':[],'z':[]}

def reset():
    global fig,ax, tdata,all_data,sensors,axes,colors,lines, plots
    fig, ax = plt.subplots(3, sharex=True)
    fig.subplots_adjust(hspace=.10)
    fig.set_size_inches(4,4)

    plots={'accel':ax[0],'gyro':ax[1],'magnet':ax[2]}

    #Setup lines in graph
    sensors=('accel','gyro','magnet')
    axes=('x','y','z')
    colors=('-r','-g','-b')
    lines={}
    for sensor in sensors:
        lines[sensor]={}
        for axis in axes:
            i=axes.index(axis)
            # print sensor+"("+axis+") : "+colors[i]
            lines[sensor][axis]=ax[sensors.index(sensor)].plot([], [],colors[i], lw=1)


    for i in range(len(axes)):
        ax[i].grid()
        ax[i].set_xlim(0, 20)

    ax[0].set_ylim(-2, 2)
    ax[1].set_ylim(-30000, 30000)
    ax[2].set_ylim(-2000, 2000)


    ax[0].set_ylabel('acceleration (g)')
    ax[1].set_ylabel('gyro (degrees/sec)')
    ax[2].set_ylabel('magnetometer')
    ax[2].set_xlabel('time (s)')

    tdata=[]
    all_data={}
    for sensor in sensors:
        all_data[sensor]={'x':[],'y':[],'z':[]}

def run(data,t0):
    global lines, test
    # print data
    #override t to be count of seconds
    t=time.time()-t0
    tdata.append(t)

    for sensor in all_data:
        for axis in all_data[sensor]:
            if axis=="x":i=0
            if axis=="y":i=1
            if axis=="z":i=2
            # if test==0: print sensor+" ("+axis+")"
            all_data[sensor][axis].append(data[sensor][i])
            lines[sensor][axis][0].set_data(tdata, all_data[sensor][axis])
    # all_lines=[[axis for axis in sensor.values()] for sensor in lines.values()]
    # test=1
    #MOVING WINDOW
    xmin, xmax = ax[0].get_xlim()
    if t >= xmax-1: #once the line get's 9 10ths of the way...
        #move the window by 5 seconds forward
        
        xmin+=5
        xmax+=5
        for i in range(len(axes)):
            ax[i].set_xlim(xmin, xmax)
        # print 'test'
        ax[0].figure.canvas.draw()
        ax[1].figure.canvas.draw()
        ax[2].figure.canvas.draw()
    html=mpld3.fig_to_html(fig)
    # print html
    # mpld3.show(fig)
    return html
    # lines['magnet']['x'],lines['magnet']['y'],lines['magnet']['z']
    # ,lines['gyro']['x'],lines['accel']['x'],lines['gyro']['y'],lines['accel']['y'],lines['gyro']['z'],lines['accel']['z']


# ser,conn_type=device.connect(bluetooth_enabled=False)
# ani = animation.FuncAnimation(fig, run, device.sensor_stream(ser,conn_type), blit=False, interval=100,
#     repeat=False)
# def animate():
#     ani = animation.FuncAnimation(fig, run, device.sensor_stream,ser,conn_type, blit=False, interval=100,
#     repeat=False)
