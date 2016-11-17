import numpy as np
import numpy.linalg as la
import numpy.polynomial.polynomial as poly
import matplotlib.pyplot as plt
from scipy import ndimage
import cv2
from scipy import misc
from PIL import Image


im = Image.open('clock.jpg','r')
pix_val = list(im.getdata())
width,height = im.size
pix = im.load()
rmin = 70
rmax = 90
for w in xrange(width):
    for h in xrange(height):
        if np.sqrt((w-width/2)**2+(h-height/2)**2)>=rmin and np.sqrt((w-width/2)**2+(h-height/2)**2)<=rmax:
            pix[w,h] = 0
im.show()
