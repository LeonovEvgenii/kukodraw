#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov 18 12:16:49 2019

@author: dan
"""

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
            e = 0
            exp.write(BEGIN_GCODE)
            exp.write('G0 Z10\n')
            while 1:
                try:
                    _in = self._in.get(timeout=1)
                    assert _in != 'end'
                    x1, y1, x2, y2 = _in['line']
                    pos = (x2/3.2 + 10, y2/3.2 + 10)
                    pen = _in['pen']
                    if pen != old_pen:
                        if pen == 'up': exp.write('G0 Z1\n')
                        if pen == 'dn': exp.write('G1 Z0.1 S1\n')
                        old_pen = pen
                    if pen == 'up':
                        exp.write('G0 X%s Y%s\n' % pos)
                    if pen == 'dn':
                        e += d(old_pos, pos) / 10
                        exp.write('G1 X%s Y%s E%s\n' % (pos[0], pos[1], e))
                    old_pos = pos
                except Empty:
                    break
                except AssertionError:
                    exp.write(END_GCODE)
                    self.export_thread.join()
                    break              
        import sys
        print('export finished', file = sys.stderr)




        
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
    