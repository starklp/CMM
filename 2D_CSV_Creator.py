#!/usr/bin/env python3
#############################################################################
# Filename    : ADC.py
# Description : Analog and Digital Conversion, ADC and DAC
# Author      : www.freenove.com
# modification: 2019/12/27
########################################################################
import smbus
import time
import math as m    # for use of pi (Added)
import numpy as np
import csv
########################################################################
pi = m.pi
sin = m.sin
cos = m.cos
########################################################################
address = 0x48  # default address of PCF8591
bus = smbus.SMBus(1)
cmd = 0x40        # command, 0100 0000
########################################################################
results = ''
########################################################################
def analogRead(chn):  # read ADC value,chn:0,1,2,3
    value = bus.read_byte_data(address, cmd+chn)
    return value

def analogWrite(value):  # write DAC value
    bus.write_byte_data(address, cmd, value)

def rad(ang):
    return ang * pi / 180

def pos(x, y, z=1):
    return np.matrix([[x], [y], [z]])

def rot(ang):
    theta = rad(ang)
    return np.matrix([[cos(theta), -sin(theta), 0], [sin(theta), cos(theta), 0], [0, 0, 1]])

def trans_2d(ang_old, ang_new, x_offset, y_offset):
    theta = rad((ang_old - ang_new))
    return np.matrix([[cos(theta), sin(theta), x_offset], [sin(theta), cos(theta), y_offset], [0, 0, 1]])

########################################################################
dx_1 = 3.125
dy_1 = 0
########################################################################
def loop():
    while True:
        global results
        amount = range(0, 3)
        # with open('collect.csv', 'a', newline='\n') as f:
        value_1 = analogRead(0)    # read the ADC value of channel 0
        # The bread board is running 3.3 Volts.  If all 3.3 Volts are running through the chip then the chip gives us 255 (and 0 at 0 volts).
        # If 300 degrees is our max rotation and 255 is our max value then the ratio between the two will allow us to get degrees (0.85).
        deg_1 = (value_1 / 0.85) + 37.647
        # Use matrix Functions to solve transformation
        end_pos = rot(deg_1).dot(pos(dx_1, dy_1))
        ###############################################
        for i in amount:
            if i == len(end_pos) - 1:
                results += str(end_pos[i]).lstrip('[').rstrip(']')
            else:
                results += str(end_pos[i]).lstrip('[').rstrip(']') + ','
        results += '\n'
        time.sleep(0.05)  # Pause for a second before next read
        print(end_pos)


def destroy():
    with open('collect.csv', 'a') as f:
        f.write(results)
    bus.close()

if __name__ == '__main__':   # Program entrance
    print('Program is starting ... ')
    try:
        loop()
    except KeyboardInterrupt:  # Press ctrl-c to end the program.
        destroy()