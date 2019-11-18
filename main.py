#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Nov 13 22:21:38 2019

@author: dan
"""

from tkinter import *
from tkinter import filedialog as fd
from ttk import Progressbar

from generate_lines import generate_lines, d

from gcode.settings import BEGIN_GCODE, END_GCODE

class KukaWindow(Tk):
    
    def __openfile(self):
        file_name = fd.askopenfilename(
            filetypes=(
                ("PNG files", "*.png"),
                ("JPG files", "*.jpg"),
                ("All files", "*.*"),
            )
        )
        self.after(50, self.__do_process_image, file_name)
        
    def __export(self):
        file_name = fd.asksaveasfilename(
            filetypes=(
                ("All files", "*.*"),
            )
        )
        self.after(50, self.__do_export, file_name)
    
    def __do_process_image(self, file_name):
        pass
    
    def __do_export(self, file_name):
        pass
    
    def __startupdate(self, e):
        pass
    
    def __checkcmdline(self, in_filename, out_filename):
        pass
    
    def __configure(self):
        self.A = IntVar()
        self.B = IntVar()
        self.A.set(100)
        self.B.set(200)
        self.__in_process = 0
        self._out = Queue()
        self._in  = Queue()
        self.__file_name = '[nofile]'

        self.topframe = Frame(self, height=20, bg='green')
        self.topframe.pack(side = TOP, expand=0, fill=X)
        self.mainframe = LabelFrame(self, text = 'Изображение', bg='yellow')
        self.mainframe.pack(side = BOTTOM, expand=1, fill=BOTH)
        Button(self.topframe, text='Загрузить файл', command=self.__openfile).pack(side = LEFT)
        Button(self.topframe, text='Экспорт',        command=self.__export  ).pack(side = LEFT)
        Scale(self.topframe, orient=HORIZONTAL, from_ = 0, to = 255, showvalue = 1, variable = self.A, command = self.__startupdate).pack(side = LEFT)
        Scale(self.topframe, orient=HORIZONTAL, from_ = 0, to = 255, showvalue = 1, variable = self.B, command = self.__startupdate).pack(side = LEFT)
        
        self.progress = Progressbar(self.topframe, orient=HORIZONTAL, mode="determinate")
        self.progress.pack(side = LEFT, expand = 1)
        
        self.canvas = Canvas(self.mainframe, width=640, height=480, bg='white')
        self.canvas.pack(expand=1, fill=BOTH)

        self.bind('<Escape>', lambda x : self.destroy())

        
    def __init__(self, in_filename, out_filename):
        super().__init__()
        self.__configure()
        
        self.after(100, self.__checkcmdline, in_filename, out_filename)

        
        
if __name__ == '__main__':
    from sys import argv
    kw = KukaWindow(
        argv[1] if len(argv) > 1 else None, 
        argv[2] if len(argv) > 2 else None
    )
    kw.mainloop()