import numpy as np
import cv2 as cv
from matplotlib import pyplot as plt
import sys

from tkinter import *
img = cv.imread(sys.argv[1],0)
edges = cv.Canny(img,100,200)
contours,hierarchy = cv.findContours(edges, 1, 2)

def d(A, B):
    x0, y0 = A
    x1, y1 = B
    return ((x1-x0)**2 + (y1-y0)**2)**(1/2)

plines = []
root = Tk()
root.bind('<Escape>', lambda x : root.destroy())
c = Canvas(root, width=640, height=480, bg='white')
c.pack()
pen = 'up'
p = (0,0)
for a in contours:
    pline = []
    for b in a:
        for x,y in b:
            pen = 'up' if d(p, (x,y)) > 20 else 'dn'
            if pen == 'dn':
                c.create_line(p[0], p[1], x, y)
            p = (x,y)
                
#print(plines)
root.mainloop()
"""
            D = d(p, (x,y))
#            print(D)
            if 2 < D <= 40:
                print("%s %s" % p)
                pline += [p]
            elif D > 40:
                plines += [pline]
                pline = []
            p = (x,y)
"""