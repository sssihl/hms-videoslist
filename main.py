from tkinter import ttk
import tkinter as tk
import config

class App(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack()
        self.create_widgets()
    
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
        self.test_box = tk.Text(self.bottomFrame)
        self.test_box.pack()

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



if __name__ == "__main__":
    root = tk.Tk()
    root.title("Rec Save")
    app = App(master=root)
    app.mainloop()
