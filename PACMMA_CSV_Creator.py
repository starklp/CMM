# Imports for calculations
import numpy as np
import math as m
import time

# Imports for MCP3008 ADC
import busio
import digitalio
import board
import adafruit_mcp3xxx.mcp3008 as MCP
from adafruit_mcp3xxx.analog_in import AnalogIn

# Simplify math import values
sin = m.sin
cos = m.cos
pi = m.pi

# Create Functions for calculating translation and rotation
def cur_pos(x, y, z):
    return np.matrix([[x], [y], [z], [1]])

def transform_3d_y(x, y, z, ang):
    rad = ang*pi/180
    return np.matrix([[cos(rad), 0, sin(rad), x], [0, 1, 0, y], [-sin(rad), 0, cos(rad), z], [0, 0, 0, 1]])

def transform_3d_z(x, y, z, ang):
    rad = ang*pi/180
    return np.matrix([[cos(rad), -sin(rad), 0, x], [sin(rad), cos(rad), 0, y], [0, 0, 1, z], [0, 0, 0, 1]])

def transform_3d_x(x, y, z, ang):
    rad = ang*pi/180
    return np.matrix([[1, 0, 0, x], [0, cos(rad), -sin(rad), y], [0, sin(rad), cos(rad), z], [0, 0, 0, 1]])

def rot_3d_x(ang):
    rad = ang*pi/180
    return np.matrix([[1, 0, 0, 0], [0, cos(rad), -sin(rad), 0], [0, sin(rad), cos(rad), 0], [0, 0, 0, 1]])
    
# Utilize imports

spi = busio.SPI(clock=board.SCK, MISO=board.MISO, MOSI=board.MOSI)
cs = digitalio.DigitalInOut(board.D5)
mcp = MCP.MCP3008(spi, cs)

# Offsets of arms

arm_4_x = # insert length of arm 4
arm_4_y = 0
arm_4_z = 0
arm_3_x = # insert length of arm 3
arm_3_y = 0
arm_3_z = 0
arm_2_x = # insert length of arm 2
arm_2_y = 0
arm_2_z = 0
arm_1_x = 0
arm_1_y = # insert height of arm 1
arm_1_z =0

# Create lists, values, and ranges needed in continuous loop

csv_list = ''

count_posrel_4 = range(0, 2)

count_1 = 0
count_2 = range(0, 3)
storage_1 = []
storage_2 = []

# Create continuous measurement loop

def cont_loop():
    global count_1
    global storage_1
    global storage_2
    while True:
        # define channels
        chan_0 = AnalogIn(mcp, MCP.P0)
        chan_1 = AnalogIn(mcp, MCP.P1)
        chan_2 = AnalogIn(mcp, MCP.P2)
        chan_3 = AnalogIn(mcp, MCP.P3)
        chan_4 = AnalogIn(mcp, MCP.P4)

        # define angles # THESE CANNOT BE USED UNTIL CALIBRATED
        deg_1 = chan_0.value / 181.867 # Rotation of Base
        storage_1.append(deg_1)
        deg_2 = chan_1.value / 181.867 # Second arm
        angle_3 = chan_2.value / 181.867 # Third arm
        if deg_1 > 0 or deg_1 < 360:  # If the potentiometer is on 
            if angle_3 == 180:
                deg_3 = deg_2
            elif angle_3 > 180:
                deg_3 = deg_2 + (angle_3 - 180)
            else:
                deg_3 = deg_2 - (180 - angle_3)
        deg_4 = chan_3.value / 181.867 # X axis rotation of end effector
        storage_2.append(deg_4)
        angle_5 = chan_4.value / 181.867 # end effector
        if deg_1 > 0 or deg_1 < 360:  # If the potentiometer is on
            if angle_5 == 180:
                deg_5 = deg_3
            elif angle_5 > 180:
                deg_5 = deg_3 + (angle_5 - 180)
            else:
                deg_5 = deg_3 - (180 - angle_5)

        # define end effectors position relative to each arm
        posrel_4 = cur_pos(arm_4_x, arm_4_y, arm_4_z)
        posrel_3_part_1 = transform_3d_z(arm_3_x, arm_3_y, arm_3_z, deg_5 - deg_3).dot(posrel_5)
        if count_1 == 0:
            posrel_3 = rot_3d_x(deg_4).dot(posrel_4_part_1)
        else:
            posrel_3 = rot_3d_x(deg_4 - storage_2[-1]).dot(posrel_3_part_1)
        posrel_2 = transform_3d_z(arm_2_x, arm_2_y, arm_2_z, deg_3 - deg_2).dot(porsel_3)
        if count_1 == 0:
            posrel_1 = transform_3d_y(arm_1_x, arm_1_y, arm_1_z, deg_1).dot(posrel_2)
        else:
            posrel_1 = transform_3d_y(arm_1_x, arm_1_y, arm_1_z, deg_1 - storage_1[-1]).dot(posrel_2)
        count += 1
        
        #########################################################
        # Insert code to scale up coordinates so that they are in a 1:1 ratio in Fusion 360
        #########################################################
        
        # Build CSV
        for i in count_2:
            if i == len(posrel_1) - 1:
                csv_list += str(posrel_1[i]).lstrip('[').rstrip(']')
            else:
                csv_list += str(posrel_1[i]).lstrip('[').rstrip(']') + ','
        csv_list += '\n'

# Be sure to test each potentiometer and add mathematical compensations to each channel value.
# Add inputs to control start and stop of function.
# Also add inputs
# Create function for singular measurments
