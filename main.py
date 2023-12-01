import os
import mysql.connector
from tkinter import ttk
import cv2
import tkinter as tk
import config
from PIL import Image, ImageTk



class App(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack()
        # should be changed to 0,1,2... depending on capture device
        self._cam = cv2.VideoCapture(config.discourse)
        self._cam.set(cv2.CAP_PROP_FRAME_WIDTH, config.width)
        self._cam.set(cv2.CAP_PROP_FRAME_HEIGHT, config.height)

        self.is_recording = False;

        self.create_widgets()
        self.preview_recorder()
        self.helper = DbHelper()
    
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

        # input_id
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
        self.buttons = {
            "start": tk.Button(self.bottomFrame,text="start", bg='#aaaaff'),
            "stop": tk.Button(self.bottomFrame,text="stop", bg = '#ffaaaa'),
            "save": tk.Button(self.bottomFrame,text="save",bg="#88ff88"),
        }
        self.buttons["start"]["command"] = self.start_recording
        self.buttons["stop"]["command"] = self.stop_recording
        self.buttons["save"]["command"] = self.save_recording

        self.buttons["start"].pack(side=tk.LEFT, )
        self.buttons["stop"].pack(side=tk.LEFT, )
        self.buttons["save"].pack(side=tk.RIGHT, expand = True )

        self.statusText = tk.Label(self,relief=tk.RAISED)
        # self.statusText["text"] = "this is just a test label"
        self.statusText.pack(side=tk.BOTTOM, fill=tk.X)
    
    def preview_recorder(self):
    # self.opencv_img to be used for all recording purposes

        # capture frame by frame
        self.ok, self.frame = self._cam.read()

        if self.is_recording:
            self._out.write(self.frame)

        # convert image colorspace
        self.opencv_img = cv2.cvtColor(self.frame, cv2.COLOR_BGR2RGBA)

        # capture latest frame
        captured_img = Image.fromarray(self.opencv_img)

        # convert captured to photoimage
        self.photo_img = ImageTk.PhotoImage(image=captured_img)

        # Display photoimage in Label
        self.videoWidget.configure(image=self.photo_img)


        # label_widget
        self.videoWidget.after(16, self.preview_recorder) # 16 value needs testing
    
    def start_recording(self, filename = 'output.mp4'):
        if self.ok:
            # TODO show on status
            print("Started recording")

        # the resolution should be received from the VideoCapture module
        self._out= cv2.VideoWriter(filename, cv2.VideoWriter_fourcc(*'DIVX'), 30, (int(self._cam.get(3)),int(self._cam.get(4))))
        self.is_recording = True
    
    def stop_recording(self):
        # TODO show on status
        print("Stopped recording")
        self.is_recording = False
        self._out.release()
    
    def save_recording(self):
        self.helper.save(12345, "OCT", "/server/12345/OCT008.mp4")
        


class DbHelper():
    
    def __init__(self):
        self.db = mysql.connector.connect(
            host=os.getenv("MYSQL_HOST"),
            port=os.getenv("MYSQL_PORT"),
            user=os.getenv("MYSQL_USER"),
            password=os.getenv("MYSQL_PASSWORD"),
            database=os.getenv("MYSQL_DATABASE")
        )

        self.table = os.getenv("MYSQL_TABLE")
        self.cursor = self.db.cursor()
        self.saved = False
    
    def save(self, *args):
        # patient_id, video_type, filename = args
        status = self.save_to_server(*args)
        if self.saved:
            self.update_db(*args)
        else:
            # TODO status message and output error
            print(status) # write the status
    
    def save_to_server(self, patient_id, video_type, filename):
        self.saved = True
        return "unable to save the file"

    def update_db(self, patient_id, video_type, filename):
        self.saved = False
        try:
            self.cursor.execute(
                f"INSERT INTO `{self.table}` (patient_id, video_type, filename) values (%s, %s, %s)",
                (patient_id,video_type,filename),)
            self.db.commit()
            print(self.cursor.rowcount, "rows inserted, ID:", self.cursor.lastrowid);
        except Exception as e:
            # TODO status message and output error
            print("Dev Error:", e)

        
        
        



        





if __name__ == "__main__":
    root = tk.Tk()
    root.title("Rec Save")
    app = App(master=root)
    app.mainloop()
    app._cam.release()
