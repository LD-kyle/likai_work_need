# -*- coding: utf-8 -*-
"""
Created on Sat Aug 11 20:25:20 2018

@author: Administrator
"""

from PIL import Image
import numpy as np

f= Image.open(r'C:\Users\Administrator\announce_test\img310\AAA5040JGKJ5_310_00.jpg')
data = np.asarray(f)
print(f.bits, f.size, f.format)
f.getbands()
pixels = f.load() # this is not a list, nor is it list()'able
width, height = f.size

all_pixels = []
for x in range(width):
    for y in range(height):
        cpixel = pixels[x, y]
        all_pixels.append(cpixel)