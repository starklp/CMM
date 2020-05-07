# Be sure to test each potentiometer and add mathematical compensations to each channel value.
# Replace theoretical arm lengths with actual measured arm lengths

# Imports for calculations
import numpy as np
import math as m
from time import sleep

# imports for GPIO inputs
import RPi.GPIO as GPIO

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

# Assign GPIO pins
single_loop_pin = 32
cont_loop_pin = 38

# Create Functions for GPIO setup
def GPIO_setup():
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(single_loop_Pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(cont_loop_Pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)


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
arm_4_x = 155.966
arm_4_y = 0
arm_4_z = 0
arm_3_x = 286.746
arm_3_y = 0
arm_3_z = 0
arm_2_x = 366.875
arm_2_y = 0
arm_2_z = 0
arm_1_x = 0
arm_1_y = 292.925
arm_1_z = 0

# Create lists, values, and ranges needed in continuous loop
data_list = ''
fusion_list = ''

count_posrel_4 = range(0, 2)

count_1 = 0
count_2 = range(0, 3)
storage_1 = []
storage_2 = []

# Create continuous measurement loop
def continuous():
    global count_1
    global storage_1
    global storage_2
    while GPIO.input(cont_loop_pin) == GPIO.LOW:
        
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

        # Insert code to scale up coordinates so that they are in a 1:1 ratio in Fusion 360
        # a value of 1 will normally render as roughly 0.394
        render_posrel_1 = posrel_1.dot(2.539999983236)

        # Build CSV for Fusion
        for i in count_2:
            if i == len(render_posrel_1) - 1:
                fusion_list += str(render_posrel_1[i]).lstrip('[').rstrip(']')
            else:
                fusion_list += str(render_posrel_1[i]).lstrip('[').rstrip(']') + ','
        fusion_list += '\n'
        
        # Build CSV for reading raw data
        for i in count_2:
            if i == len(posrel_1) - 1:
                data_list += str(posrel_1[i]).lstrip('[').rstrip(']')
            else:
                data_list += str(posrel_1[i]).lstrip('[').rstrip(']') + ','
        data_list += '\n'
        
        # display current 3D coordinates
        print(posrel_1)
        sleep(0.01)
        break
    if GPIO.input(cont_loop_pin) == GPIO.HIGH:
        return data_list, fusion_list
    
    
# Create single meaurement
def single():
    global count_1
    global storage_1
    global storage_2
    
    # Define channels
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

    # Insert code to scale up coordinates so that they are in a 1:1 ratio in Fusion 360
    # a value of 1 will normally render as roughly 0.394
    render_posrel_1 = posrel_1.dot(2.539999983236)

    # Build CSV for Fusion
    for i in count_2:
        if i == len(render_posrel_1) - 1:
            fusion_list += str(render_posrel_1[i]).lstrip('[').rstrip(']')
        else:
            fusion_list += str(render_posrel_1[i]).lstrip('[').rstrip(']') + ','
    fusion_list += '\n'
    
    # Build CSV for reading raw data
    for i in count_2:
        if i == len(posrel_1) - 1:
            data_list += str(posrel_1[i]).lstrip('[').rstrip(']')
        else:
            data_list += str(posrel_1[i]).lstrip('[').rstrip(']') + ','
    data_list += '\n'
    
    return data_list, fusion_list
    
    
# Create single loop function
def single_loop():
    while GPIO.input(single_loop_pin) == GPIO.LOW:
        print('Release to take measurement')
        sleep(0.05)
        break
    if GPIO.input(single_loop_pin) == GPIO.HIGH:
        single()

# Create continuous loop funciton
def cont_loop():
    while GPIO.input(cont_loop_pin) == GPIO.LOW:
        continuous()

def program():
    GPIO_setup()
    if GPIO.input(single_loop_pin) == GPIO.LOW:
        single_loop()
    elif GPIO.input(cont_loop_pin) == GPIO.LOW:
        cont_loop()
    else: 
        print('When finished press Control + C')
        sleep(0.1)

# Create funciton to transfer append data when program is done.
def destory():
    with open('fusion.csv', 'a') as f:
        f.write(fusion_list)
    with open('data.csv', 'a') as f:
        f.write(data_list)

# Run the Program
if __name__ == '__main__':   # Program entrance
    print('Program is starting ... ')
    message = input('''Welcome to the Portable Actuating Coordinate Measuring Machine Arm CSV Creator
    
To take one measurement at a time:
Use Button 1.  The measurement will be taken upon the release of the button.

To take constant measurments:
Use Button 2.  The measurments will be taken every 0.01 seconds while the button is pressed

Press Control + C to end the program.

Make sure that you have created files "fusion.csv" and "data.csv".
If the files do not exist then the data has no place to be stored.

*This program only adds data to these files, not remove, so data removal must be done manually.*
*If you plan to use an empty file then be sure to remove all data and save the file.*
*Fusion 360 units must be set to milimeters for data to be displayed accurately*
Are you ready to start (y/n): '''
    if message == y:
        while True:
            try:
                program()
            except KeyboardInterrupt:  # Press Control + C
                destory()
                print('Closing Program...')
                exit()
    else:
        print('Closing Program...')
        exit()
