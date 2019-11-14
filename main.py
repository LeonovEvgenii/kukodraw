#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Nov 13 22:21:38 2019

@author: dan
"""

from tkinter import *
from tkinter import filedialog as fd

class KukaWindow(Tk):
    
    def __openfile(self):
        self.img_name = fd.asksaveasfilename(
            filetypes=(
                ("Image files", "*.png;*.jpeg;*.jpg"),
                ("All files", "*.*"),
            )
        )

    def __bind_events(self):
        self.bind('<Escape>', lambda x : self.destroy())

    def __configure(self):
        self.topframe = Frame(self, height=20)
        self.topframe.pack(side = TOP, expand=1, fill=X)
        self.mainframe = LabelFrame(self, text = 'Изображение', bg='yellow')
        self.mainframe.pack(side = BOTTOM, expand=1, fill=BOTH)
        Button(self.topframe, text='Загрузить файл', command=self.__openfile).pack(side = LEFT)
        Button(self.topframe, text='Экспорт').pack(side = LEFT)
        Canvas(self.mainframe, width=640, height=480, bg='white').pack(fill=BOTH)
        
    def __init__(self):
        super().__init__()
        self.__configure()
        self.__bind_events()

        
        
if __name__ == '__main__':
    kw = KukaWindow()
    kw.mainloop()