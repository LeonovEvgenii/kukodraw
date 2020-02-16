#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Nov 13 22:21:38 2019

@author: dan
"""
template = """
DECL E6POS XP%s={X %s,Y %s,Z 0.0,A -179.997406,B 0.00397241442,C 179.999054,S 2,T 8,E1 0.0,E2 0.0,E3 0.0,E4 0.0,E5 0.0,E6 0.0}
DECL FDAT FP%s={TOOL_NO 1,BASE_NO 0,IPO_FRAME #BASE,POINT2[] " "}
DECL LDAT LCPDAT%s={VEL 2.00000,ACC 100.000,APO_DIST 500.000,APO_FAC 50.0000,AXIS_VEL 100.000,AXIS_ACC 100.000,ORI_TYP #VAR,CIRC_TYP #BASE,JERK_FAC 50.0000,GEAR_JERK 100.000,EXAX_IGN 0}
"""

from tkinter import *
from tkinter import filedialog as fd
from ttk import Progressbar

from generate_lines import generate_lines, d
from cv_wrapper import get_contours

from gcode.settings import BEGIN_GCODE, END_GCODE

class KukaWindow(Tk):
    msg_n = 0
    active_messages = []
    
    def __message(self, text):
        def __hide(t, text):
            self.canvas.delete(t) 
            self.msg_n -= 1
            self.active_messages.remove(text)
            
        if text not in self.active_messages:
            self.active_messages += [text]
            t = self.canvas.create_text(0, 0, text = text)
            x1, y1, x2, y2 = self.canvas.bbox(t)
            w, h = x2 - x1, y2 - y1
            self.canvas.move(t, 635 - w/2, 475 - h - self.msg_n * h * 1.5)
            self.msg_n += 1
            self.after(5000, __hide, t, text)
        
    def __openfile(self, file_name = None):
        if file_name == None:
            self.__file_name = fd.askopenfilename(
                filetypes=(
                    ("PNG files", "*.png"),
                    ("JPG files", "*.jpg"),
                    ("All files", "*.*"),
                )
            )
        else:
            self.__file_name = file_name
            
        self.__start_process_contours(self.__file_name, self.A.get(), self.B.get())

    def __export(self):
        file_name = fd.asksaveasfilename(
            filetypes=(
                ("All files", "*.*"),
            )
        )
        lines = self.canvas.find_withtag('drawing')
        self.progress["maximum"] = len(lines)
        self.export_data = []
        self.after(50, self.__do_export, file_name, lines, 0, len(lines))
        
    def __start_process_contours(self, file_name, A, B):
        try:
            contours = get_contours(file_name, A, B)
            self.__file_name = file_name
            self.canvas.delete('all')
            self.after(50, self.__process_contours, 0, contours)
            self.ncontour = 0
        except ValueError as e:
            self.__message(e.args[0])
    
    def __process_contours(self, i, contours):
        try:
            contour = contours[i]
            i += 1
            points = []
            for point in contour:
                points += [point[0][0],point[0][1]]
            try:
                self.canvas.create_line(points, width = 2, tags = ('drawing',))
            except TclError:
                pass
            self.after(1, self.__process_contours, i, contours)
        except IndexError:
            self.__message('Отрисовано.')
        
    def __do_export(self, file_name, lines, n, N):
        try:
            if n == 0: self.__message('Экспорт в "%s"...' % file_name)
            coords = self.canvas.coords(lines[n])
            line_length = len(coords) // 2 - 2
            pline = []
            for i in range(line_length):
                x1, y1 = coords[i*2+0], coords[i*2+1]
                x2, y2 = coords[i*2+2], coords[i*2+3]
                pline += [((x1,y1),(x2,y2))]
                # print(template % (i, x1, y1, i, i))
            n += 1

            self.export_data += [pline]

            self.progress.step()
            self.after(10, self.__do_export, file_name, lines, n, N)
        except IndexError:
            from json import dump
            dump(self.export_data, open(file_name, 'w'),  indent=4)
            self.__message('Экспортировано в "%s".' % file_name)
            
    def __startupdate(self, e):
        try:
            open(self.__file_name, 'rb').read(1)
            self.__start_process_contours(self.__file_name, self.A.get(), self.B.get())
        except IOError as e:
            self.__message('"%s": %s' % (e.filename, e.strerror))
        
    
    def __checkcmdline(self, in_filename, out_filename, AB):
        try:
            assert in_filename != None
            open(in_filename, 'rb').read(1)
            self.__openfile(in_filename)
            self.__startupdate(None)
            assert AB != None
            A, B = AB[0], AB[1]
            self.A.set(A) 
            self.B.set(B)
            assert out_filename != None
            open(out_filename, 'wb').write(b'\n')
            self.__do_export(out_filename)
            
        except AssertionError:
            pass
        except IOError as e:
            self.__message(e)
    
    def __configure(self):
        self.A = IntVar()
        self.B = IntVar()
        self.A.set(100)
        self.B.set(200)
        self.__in_process = 0
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

        
    def __init__(self, in_filename, out_filename, AB):
        super().__init__()
        self.__configure()
        
        self.after(100, self.__checkcmdline, in_filename, out_filename, AB)

        self.__message('Кванториум "Фотоника". Рисуем на KUKA')
        
if __name__ == '__main__':
    from sys import argv
    kw = KukaWindow(
        argv[1] if len(argv) > 1 else None, 
        argv[2] if len(argv) > 2 else None,
        (argv[3], argv[4]) if len(argv) > 4 else None,
    )
    kw.mainloop()
