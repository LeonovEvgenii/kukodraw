#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Nov 14 12:52:05 2019

@author: dan
"""
import numpy as np
import cv2 as cv

def read_resize(fname):
    img = cv.imread(fname,0)
    x, y = img.shape
    if x < y:
        print(x, y, (640, y * 640 // x))
        img = cv.resize(img, (640, y * 640 // x))
    else:
        print(x, y, (x * 480 // y, 480))
        img = cv.resize(img, (x * 480 // y, 480))
    return img

def d(A, B):
    x0, y0 = A
    x1, y1 = B
    return ((x1-x0)**2 + (y1-y0)**2)**(1/2)

def generate_lines(_in, _out):
    fname  = _in.get()
    A, B = _in.get()
    img = read_resize(fname)
    contours,hierarchy = cv.findContours(cv.Canny(img,A,B), cv.RETR_LIST, cv.CHAIN_APPROX_TC89_KCOS)
    pen = 'up'
    p = (0,0)
    n = 0
    try:
        for a in contours:
            for b in a:
                for x,y in b:
                    pen = 'up' if d(p, (x,y)) > 20 else 'dn'
                    _out.put({'pen':pen, 'line':(p[0], p[1], x, y)})
                    n += 1
                    assert n < 10000
                    p = (x,y)
    except AssertionError:
        pass
    _out.put('end')

    
    
if __name__ == '__main__':
    from queue import Queue, Empty
    from threading import Thread
    q1 = Queue()
    q2 = Queue()
    t = Thread(target=generate_lines, args=[q1, q2])
    q1.put('img/4.png')
    q1.put((100, 200))
    t.start()
    
    while 1:
        try:
            pass # print(q2.get(timeout=1))
        except Empty:
            break
    t.join()