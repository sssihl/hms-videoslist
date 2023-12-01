import numpy as np
from tkinter import ttk
import cv2
import tkinter as tk
import config
from PIL import Image, ImageTk

# should be changed to 0,1,2... depending on capture device
vid = cv2.VideoCapture('../assets/discourse.mp4')

vid.set(cv2.CAP_PROP_FRAME_WIDTH, config.width)
vid.set(cv2.CAP_PROP_FRAME_HEIGHT, config.height)


class App(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack()
        self.create_widgets()
        self.open_recorder()
    
    def create_widgets(self):
        # main frames
        self.topFrame = tk.Frame(self)
        self.bottomFrame = tk.Frame(self)
        self.topFrame.pack(fill=tk.X, expand=True)
        self.bottomFrame.pack()

        # top frames
        self.inputFrame = tk.Frame(self.topFrame)
        self.inputFrame.pack(side=tk.LEFT, fill=tk.Y)
        self.validateFrame = tk.Frame(self.topFrame)
        self.validateFrame.pack(side=tk.LEFT)

        # input
        tk.Label(self.inputFrame,text="ID").grid(row = 0, column=0)
        self.input_id = tk.Entry(self.inputFrame)
        self.input_id.grid(row = 0, column = 1)
            # TODO datepicker
        tk.Label(self.inputFrame,text="Date").grid(row = 1, column=0)
        self.input_date = tk.Entry(self.inputFrame)
        self.input_date.grid(row=1, column=1)

        ## validate
        self.info = [tk.Label(self.validateFrame,text=text) for text in ["\tName\t: ","\tAge\t: ", "\tSex\t: "]]
        for i in self.info:
            i.pack(expand=True)

        
        # bottom frame

        # TODO video frame
        self.videoWidget = tk.Label(self.bottomFrame)
        self.videoWidget.pack()

        self.choose_source = ttk.Combobox(
            self.bottomFrame, state="readonly",
            values = config.videoTypes)
        self.choose_source.pack(side=tk.LEFT)

        tk.Button(self.bottomFrame,text="select"),
        self.buttons = [
            tk.Button(self.bottomFrame,text="start", bg='#aaaaff'),
            tk.Button(self.bottomFrame,text="stop", bg = '#ffaaaa'),
            tk.Button(self.bottomFrame,text="save",bg="#88ff88"),
        ]
        self.buttons[0].pack(side=tk.LEFT, )
        self.buttons[1].pack(side=tk.LEFT, )
        self.buttons[2].pack(side=tk.RIGHT, expand = True )

        self.statusText = tk.Label(self,relief=tk.RAISED)
        # self.statusText["text"] = "this is just a test label"
        self.statusText.pack(side=tk.BOTTOM, fill=tk.X)
    
    def open_recorder(self):

        # capture frame by frame
        ok, frame = vid.read()


        # convert image colorspace
        opencv_img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)

        # capture latest frame
        captured_img = Image.fromarray(opencv_img)

        # convert captured to photoimage
        self.photo_img = ImageTk.PhotoImage(image=captured_img)

        # Display photoimage in Label
        self.videoWidget.configure(image=self.photo_img)

        # label_widget
        self.videoWidget.after(10, self.open_recorder)





if __name__ == "__main__":
    root = tk.Tk()
    root.title("Rec Save")
    app = App(master=root)
    app.mainloop()
