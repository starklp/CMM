# import libraries
import numpy as np
import math as m
sin = m.sin
cos = m.cos
pi = m.pi
# Create functions
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
