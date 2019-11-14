#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Nov 13 22:21:38 2019

@author: dan
"""

from tkinter import *
from tkinter import filedialog as fd
from generate_lines import generate_lines
from threading import Thread
from queue import Queue, Empty

class KukaWindow(Tk):
    
    def __openfile(self):
        self.__file_name = fd.askopenfilename(
            filetypes=(
                ("PNG files", "*.png"),
                ("JPG files", "*.jpg"),
                ("All files", "*.*"),
            )
        )
        self.__startupdate(None)

    def __bind_events(self):
        self.bind('<Escape>', lambda x : self.destroy())

    def __configure(self):
        self.A = IntVar()
        self.B = IntVar()
        self.A.set(100)
        self.B.set(200)
        self.__in_process = 0
        self._out = Queue()
        self._in  = Queue()
        self.__file_name = '[nofile]'

        self.topframe = Frame(self, height=20)
        self.topframe.pack(side = TOP, expand=1, fill=X)
        self.mainframe = LabelFrame(self, text = 'Изображение', bg='yellow')
        self.mainframe.pack(side = BOTTOM, expand=1, fill=BOTH)
        Button(self.topframe, text='Загрузить файл', command=self.__openfile).pack(side = LEFT)
        Button(self.topframe, text='Экспорт').pack(side = LEFT)
        Scale(self.topframe, orient=HORIZONTAL, from_ = 0, to = 255, showvalue = 1, variable = self.A, command = self.__startupdate).pack(side = LEFT)
        Scale(self.topframe, orient=HORIZONTAL, from_ = 0, to = 255, showvalue = 1, variable = self.B, command = self.__startupdate).pack(side = LEFT)
        self.canvas = Canvas(self.mainframe, width=640, height=480, bg='white')
        self.canvas.pack(fill=BOTH)
        
    def __startupdate(self, e):
        if self.__file_name != '[nofile]':
            print(self.__file_name)
            if not self.__in_process:
                self.__in_process = 1
                
                self.canvas.delete("all")
                self.update_thread = Thread(target = generate_lines, args = [self._out, self._in])
                self._out.put(self.__file_name)
                self._out.put((self.A.get(), self.B.get()))
                self.update_thread.start()
                self.after(500, self.__update_canvas)
            
    def __update_canvas(self):
        while 1:
            try:
                _in = self._in.get(timeout=0.1)
                assert _in != 'end'
                x1, y1, x2, y2 = _in['line']
                pen = _in['pen']
                if pen == 'dn':
                    self.canvas.create_line(x1, y1, x2, y2)
            except Empty:
                self.after(500, self.__update_canvas)
                break
            except AssertionError:
                self.__in_process = 0
                self.update_thread.join()
                break
        
    
    def __init__(self):
        super().__init__()
        self.__configure()
        self.__bind_events()

        
        
if __name__ == '__main__':
    kw = KukaWindow()
    kw.mainloop()