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



spi = busio.SPI(clock=board.SCK, MISO=board.MISO, MOSI=board.MOSI)

cs = digitalio.DigitalInOut(board.D5)

mcp = MCP.MCP3008(spi, cs)
def run_loop():
    while True:
        chan_0 = AnalogIn(mcp, MCP.P0)
        chan_1 = AnalogIn(mcp, MCP.P1)
        chan_2 = AnalogIn(mcp, MCP.P2)
        chan_3 = AnalogIn(mcp, MCP.P3)
        chan_4 = AnalogIn(mcp, MCP.P4)

        deg_1 = 181.867
        # Be sure to test each potentiometer and add mathematical compensations to each channel value.


# Create Functions for calculating translation and rotation
# print((chan_1.value / 181.867) - 37.4776072)
