# -*- coding: utf-8 -*-
# WARNING: This is a simplified zoom example.
# You should use more advanced techniques to not cram the memory
# with a huge resized image for the large zooms.
import random
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk

class AutoScrollbar(ttk.Scrollbar):
    ''' A scrollbar that hides itself if it's not needed.
        Works only if you use the grid geometry manager '''
    def set(self, lo, hi):
        self.grid()
        ttk.Scrollbar.set(self, lo, hi)

    def pack(self, **kw):
        raise tk.TclError('Cannot use pack with this widget')

    def place(self, **kw):
        raise tk.TclError('Cannot use place with this widget')

class Zoom(ttk.Frame):
    ''' Simple zoom with mouse wheel '''
    def __init__(self, mainframe):
        ''' Initialize the main Frame '''
        ttk.Frame.__init__(self, master=mainframe)
        #self.master.title('Simple zoom with mouse wheel')
        # Vertical and horizontal scrollbars for canvas
        vbar = AutoScrollbar(self.master, orient='vertical')
        hbar = AutoScrollbar(self.master, orient='horizontal')
        vbar.grid(row=1, column=4, rowspan=2 ,sticky='ns')
        hbar.grid(row=3, column=0, columnspan=4 ,sticky='we')
        # Open image
        self.image = Image.new('RGB', (650, 650),color=(255,255,255,0))
        # Create canvas and put image on it
        self.canvas = tk.Canvas(self.master, highlightthickness=0,
                                xscrollcommand=hbar.set, yscrollcommand=vbar.set,width=650, height=650)
        self.canvas.grid(column=0, row=1,columnspan=4,rowspan=2, sticky='nswe')
        vbar.configure(command=self.canvas.yview)  # bind scrollbars to the canvas
        hbar.configure(command=self.canvas.xview)
        # Make the canvas expandable
        self.master.rowconfigure(0, weight=1)
        self.master.columnconfigure(0, weight=1)
        # Bind events to the Canvas
        self.canvas.bind('<ButtonPress-1>', self.move_from)
        self.canvas.bind('<B1-Motion>',     self.move_to)
        self.canvas.bind('<MouseWheel>', self.wheel)  # with Windows and MacOS, but not Linux
        self.canvas.bind('<Button-5>',   self.wheel)  # only with Linux, wheel scroll down
        self.canvas.bind('<Button-4>',   self.wheel)  # only with Linux, wheel scroll up
        # Show image and plot some random test rectangles on the canvas
        self.imscale = 1.0
        self.imageid = None
        self.delta = 0.75
        width, height = self.image.size
        # Text is used to set proper coordinates to the image. You can make it invisible.
        self.text = self.canvas.create_text(0, 0, anchor='nw', text='Scroll to zoom')
        self.show_image()
        self.canvas.configure(scrollregion=self.canvas.bbox('all'))

    def move_from(self, event):
        ''' Remember previous coordinates for scrolling with the mouse '''
        self.canvas.scan_mark(event.x, event.y)

    def move_to(self, event):
        ''' Drag (move) canvas to the new position '''
        self.canvas.scan_dragto(event.x, event.y, gain=1)

    def wheel(self, event):
        ''' Zoom with mouse wheel '''
        scale = 1.0
        # Respond to Linux (event.num) or Windows (event.delta) wheel event
        if event.num == 5 or event.delta == -120:
            scale        *= self.delta
            self.imscale *= self.delta
        if event.num == 4 or event.delta == 120:
            scale        /= self.delta
            self.imscale /= self.delta
        # Rescale all canvas objects
        x = self.canvas.canvasx(event.x)
        y = self.canvas.canvasy(event.y)
        self.canvas.scale('all', x, y, scale, scale)
        self.show_image()
        self.canvas.configure(scrollregion=self.canvas.bbox('all'))
    def open_image(self,filename):
        self.image=Image.open(filename)
        self.show_image()
    def show_image(self):
        ''' Show image on the Canvas '''
        if self.imageid:
            self.canvas.delete(self.imageid)
            self.imageid = None
            self.canvas.imagetk = None  # delete previous image from the canvas
        width, height = self.image.size
        new_size = int(self.imscale * width), int(self.imscale * height)
        imagetk = ImageTk.PhotoImage(self.image.resize(new_size))
        # Use self.text object to set proper coordinates
        self.imageid = self.canvas.create_image(self.canvas.coords(self.text),
                                                anchor='nw', image=imagetk)
        self.canvas.lower(self.imageid)  # set it into background
        self.canvas.imagetk = imagetk  # keep an extra reference to prevent garbage-collection

#path = '5.tif'  # place path to your image here
#root = tk.Tk()
#app = Zoom(root, path=path)
#root.mainloop()