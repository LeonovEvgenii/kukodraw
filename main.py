#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Nov 13 22:21:38 2019

@author: dan
"""

from tkinter import *
from tkinter import filedialog as fd
from generate_lines import generate_lines, d
from threading import Thread
from queue import Queue, Empty

class KukaWindow(Tk):
    
    def __from_rgb(self, rgb):
        return "#%02x%02x%02x" % rgb 
    
    def __openfile(self):
        self.__file_name = fd.askopenfilename(
            filetypes=(
                ("PNG files", "*.png"),
                ("JPG files", "*.jpg"),
                ("All files", "*.*"),
            )
        )
        self.__startupdate(None)
        
    def __export(self):
        exp_file_name = fd.asksaveasfilename(
            filetypes=(
                ("All files", "*.*"),
            )
        )
        self.after(500, self.__do_export, exp_file_name)
    
    def __do_export(self, exp_file_name):
        self.export_thread = Thread(target = generate_lines, args = [self._out, self._in])
        self._out.put(self.__file_name)
        self._out.put((self.A.get(), self.B.get()))
        self.export_thread.start()
        with open(exp_file_name, 'w') as exp:
            old_pen = 'up'
            old_pos = (0,0)
            exp.write('G0 Z10\n')
            while 1:
                try:
                    _in = self._in.get(timeout=1)
                    assert _in != 'end'
                    x1, y1, x2, y2 = _in['line']
                    pos = (x2/3.2 + 10, y2/3.2 + 10)
                    pen = _in['pen']
                    if pen != old_pen:
                        if pen == 'up': exp.write('G0 Z10\n')
                        if pen == 'dn': exp.write('G1 Z0 S1\n')
                        old_pen = pen
                    if pen == 'up':
                        exp.write('G0 X%s Y%s\n' % pos)
                    if pen == 'dn':
                        e = d(old_pos, pos) / 10
                        exp.write('G1 X%s Y%s E%s\n' % (pos[0], pos[1], e))
                    old_pos = pos
                except Empty:
                    break
                except AssertionError:
                    self.__in_process = 0
                    self.update_thread.join()
                    break              
        import sys
        print('export finished', file = sys.stderr)

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
        Button(self.topframe, text='Экспорт',        command=self.__export  ).pack(side = LEFT)
        Scale(self.topframe, orient=HORIZONTAL, from_ = 0, to = 255, showvalue = 1, variable = self.A, command = self.__startupdate).pack(side = LEFT)
        Scale(self.topframe, orient=HORIZONTAL, from_ = 0, to = 255, showvalue = 1, variable = self.B, command = self.__startupdate).pack(side = LEFT)
        self.canvas = Canvas(self.mainframe, width=640, height=480, bg='white')
        self.canvas.pack(fill=BOTH)
        
        
    def __startupdate(self, e):
        if self.__file_name != '[nofile]':
            if not self.__in_process:
                self.__in_process = 1
                
                self.canvas.delete("all")
                self.update_thread = Thread(target = generate_lines, args = [self._out, self._in])
                self._out.put(self.__file_name)
                self._out.put((self.A.get(), self.B.get()))
                self.update_thread.start()
                self.after(500, self.__update_canvas)
            
    def __update_canvas(self):
        r, g, b = 255, 255, 0
        while 1:
            try:
                _in = self._in.get(timeout=0.1)
                assert _in != 'end'
                x1, y1, x2, y2 = _in['line']
                pen = _in['pen']
                if pen == 'dn':
                    self.canvas.create_line(x1, y1, x2, y2, fill = self.__from_rgb((int(r), int(g), int(b))))
                    g -= 0.1 if g > 0 else 0
                    r -= 0.1 if g < 0.2 and r > 0 else 0
            except Empty:
                self.after(500, self.__update_canvas)
                break
            except AssertionError:
                self.__in_process = 0
                self.update_thread.join()
                break
            
    def __checkcmdline(self, in_filename, out_filename):
        try:
            assert in_filename != None
            open(in_filename, 'rb').read(1)
            self.__file_name = in_filename
            self.__startupdate(None)
            assert out_filename != None
            open(out_filename, 'wb').write(b'\n')
            self.__do_export(out_filename)
        except AssertionError:
            pass
        except IOError as e:
            print(e)
    
    def __init__(self, in_filename, out_filename):
        super().__init__()
        self.__configure()
        self.__bind_events()
        
        self.after(100, self.__checkcmdline, in_filename, out_filename)

        
        
if __name__ == '__main__':
    from sys import argv
    kw = KukaWindow(
        argv[1] if len(argv) > 0 else None, 
        argv[2] if len(argv) > 1 else None
    )
    kw.mainloop()