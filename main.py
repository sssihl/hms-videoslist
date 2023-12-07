import os, shutil
import mysql.connector, pymssql, oracledb , cv2
from tkinter import ttk
from datetime import datetime
import tkinter as tk
from PIL import Image, ImageTk
import json



class Config:
    def __init__(self):
        self.sync()
    
    def update(self):
        with open('config.json',"w") as f:
            json.dump(config.__dict__,f, indent=4)
    
    def sync(self):
        with open('config.json') as f:
            _dict = json.load(f)
            self.__dict__.update(_dict)
        

config = Config()
        





class App(tk.Frame):
    def __init__(self, master=None):
        # an App frame
        super().__init__(master)
        self.master = master
        self.pack(expand=True)
        # should be changed to 0,1,2... depending on capture device
        self._cam = cv2.VideoCapture(config.videoDevice)
        self._cam.set(cv2.CAP_PROP_FRAME_WIDTH, config.width)
        self._cam.set(cv2.CAP_PROP_FRAME_HEIGHT, config.height)

        # state for allowing the frames to be recorded
        self.is_recording = False;

        # creates all the text variables for accessing widget data
        self.create_vars()

        # creates all the widgets and puts them on the screen
        self.create_widgets()
        self.run_tests()
        self.preview_recorder()

    def run_tests(self):
        helper = DbHelper(self)
        if helper.ok:
            self.set_status("DB connected")
    
    def create_vars(self):
        self.id_var = tk.StringVar()
        self.date_var = tk.StringVar()
        self.source_var = tk.StringVar()
    
    def create_widgets(self):
    # STRUCTURE
    # - topFrame
    #     - inputFrame 
    #         - input_id
    #         - input_date
    #     - validateFrame / patientNotFound
    #         [contained in info as a list]
    #         - [0] Name (label)
    #         - [1] Age (label)
    #         - [2] Sex (label)
    # - bottomFrame
    #     - video_widget
    #     - choose_source - start - save - stop
    #     (stored as buttons [0]    [1]    [2])
    # - status_text

        # main frames
        self.topFrame = tk.Frame(self)
        self.bottomFrame = tk.Frame(self)
        self.topFrame.pack(fill=tk.X, expand=True)
        self.bottomFrame.pack(expand=True)

        # TOP FRAME ----------------------------------------------------

        self.inputFrame = tk.Frame(self.topFrame)
        self.inputFrame.pack(side=tk.LEFT, fill=tk.BOTH)
        self.validateFrame = tk.Frame(self.topFrame)
        self.patientNotFound = tk.Label(self.topFrame,text="No Patient with this ID")

        # input_id
        tk.Label(self.inputFrame,text="ID").grid(row = 0, column=0)
        self.input_id = tk.Entry(self.inputFrame, textvariable=self.id_var, justify="center")
        self.input_id.grid(row = 0, column = 1)
        self.id_var.trace_add('write',self.check_id)

        # input_date
        # TODO datepicker
        tk.Label(self.inputFrame,text="Date").grid(row = 1, column=0)
        self.input_date = tk.Entry(self.inputFrame, textvariable=self.date_var, justify="center")
        self.input_date.insert(0,str(datetime.now()).split()[0])
        self.input_date.grid(row=1, column=1)

        ## validate
        self.info = [tk.Label(self.validateFrame,text=text) for text in ["\tName\t: ","\tAge\t: ", "\tSex\t:", "\tDOB\t:"]]
        for i in self.info:
            i.pack(expand=True, anchor="w")

        
        # BOTTOM FRAME -----------------------------------------------

        # video_widget
        self.video_widget = tk.Label(self.bottomFrame)
        self.video_widget.pack()

        # choose_source
        self.choose_source = ttk.Combobox(
            self.bottomFrame, state="readonly", textvariable=self.source_var,
            values = config.videoTypes)
        self.choose_source.current(config.videoTypes.index(config.last_source))
        self.choose_source.pack(side=tk.LEFT)
        self.source_var.trace_add('write',self.change_source)
        print("DEV SOURCE VAR: ",self.source_var.get())

        # start stop save buttons
        self.buttons = {
            "start": tk.Button(self.bottomFrame,text="start recording", bg='#aaaaff'),
            "stop": tk.Button(self.bottomFrame,text="stop", bg = '#ffaaaa'),
            "save": tk.Button(self.bottomFrame,text="save",bg="#88ff88"),
        }

        self.buttons["start"]["command"] = self.start_recording
        self.buttons["stop"]["command"] = self.stop_recording
        self.buttons["save"]["command"] = self.save_recording

        self.buttons["start"].pack(side=tk.LEFT, )
        self.buttons["stop"].pack(side=tk.LEFT, )
        self.buttons["save"].pack(side=tk.RIGHT, expand = True )

        # status bar
        self.status_text = tk.Label(self,relief=tk.RAISED)
        # self.statusText["text"] = "this is just a test label"
        self.status_text.pack(side=tk.BOTTOM, fill=tk.X)


        # to enter last patient entry by default
        self.id_var.set(config.last_patient_id)
    
    def check_id(self, var, index, mode):
        val = self.id_var.get()
        
        if len(val) == 12: # what is id length
            self.validate_patient(val)
        else:
            self.patientNotFound.pack_forget()
            self.validateFrame.pack_forget()
    
    def change_source(self, var, index, mode):
        config.last_source = self.source_var.get()
        config.update()
    
        

    # callback for id
    
    def validate_patient(self, patient_id):
        self.helper = DbHelper(self)
        if self.helper.ok:
            patient_data = self.helper.get_patient_data(patient_id)
        else:
            self.set_status("Couldn't connect to Database! Please contact Admin","ERROR")
        self.helper.close()

        if patient_data:
            name = patient_data[1]
            age = datetime.now().year - patient_data[2].year
            sex = patient_data[3]
            dob = patient_data[2].strftime("%d/%m/%Y")
            config.last_patient_id = patient_id
            config.update()
            self.patientNotFound.pack_forget()
            self.validateFrame.pack(side=tk.RIGHT, fill=tk.X)
            self.info[0]["text"] = f"\tName\t:{name}"
            self.info[1]["text"] = f"\tAge\t:{age}y"
            self.info[2]["text"] = f"\tSex\t:{sex}"
            self.info[3]["text"] = f"\tDOB\t:{dob}"
            return True
        else:
            self.validateFrame.pack_forget()
            self.patientNotFound.pack(side=tk.RIGHT,fill=tk.BOTH, anchor="center")
            return False
            
    def preview_recorder(self):
    # self.frame to be used for all recording purposes

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
        self.video_widget.configure(image=self.photo_img)


        # label_widget
        self.video_widget.after(config.rate, self.preview_recorder) # 16 value needs testing
    
    def start_recording(self, filename = 'output.mp4'):
        if not self.is_recording:
            if self.ok:
                self.set_status("STARTED RECORDING","DEFAULT")
                print("STARTED RECORDING")
                # the resolution should be received from the VideoCapture module
                self._out= cv2.VideoWriter(filename, cv2.VideoWriter_fourcc(*'mp4v'), config.fps, (int(self._cam.get(3)),int(self._cam.get(4))))
                self.is_recording = True
            else:
                self.set_status("Failed to start recording.","ERROR")
        else:
            self.set_status("RECORDING has already STARTED!", "DEFAULT")
            
    
    def stop_recording(self):
        if self.is_recording:
            self.is_recording = False
            self._out.release()
            self.set_status("STOPPED RECORDING")
            print("STOPPED RECORDING")
        else:
            self.set_status("WARNING: NO recording in progress", "WARNING")
    
    def save_recording(self):

        if self.validate_patient(self.id_var.get()):
            self.helper = DbHelper(self)
            if self.helper.ok:
                self.helper.save(int(self.id_var.get()), self.source_var.get(), self.date_var.get())
            else:
                self.set_status("Couldn't connect to Database! Please contact Admin","ERROR")

            self.helper.close()
        else:
            self.set_status("Invalid Patient ID. Could not find patient", "ERROR")
    
    def set_status(self, text="", type=""):
    # types = DEFAULT, SUCCESS, ERROR
    # just call set_status() to clear status
        if type == "ERROR":
            self.status_text["fg"] = "#ffffff"
            self.status_text["bg"] = "#ff3333"
        elif type == "SUCCESS":
            self.status_text["fg"] = "#000000"
            self.status_text["bg"] = "#11ff11"
        elif type == "DEFAULT":
            self.status_text["fg"] = "#ffffff"
            self.status_text["bg"] = "#8888ff"
        elif type == "WARNING":
            self.status_text["bg"] = "#FFFF99"
            self.status_text["fg"] = "#000000"
        else:
            self.status_text["fg"] = "#000000"
            self.status_text["bg"] = "#ffffff"
        self.status_text["text"] = text

        


class DbHelper():
# should be instantiated, used and then cleaned by calling DbHelper().close()
    
    def __init__(self, app: App):
        self.app = app # to access the tkinter app from here
        v_options = {
            "host": os.getenv("V_SQL_HOST"),
            "port": os.getenv("V_SQL_PORT"),
            "user": os.getenv("V_SQL_USER"),
            "password": os.getenv("V_SQL_PASSWORD"),
            "database": os.getenv("V_SQL_DATABASE"),
        }
        # connect to the database, using .env file variables
        if os.getenv("V_SQL_PROVIDER") == "MSSQL":
            self.vprovider = pymssql
            v_options["as_dict"] = True
        elif os.getenv("V_SQL_PROVIDER") == "MYSQL":
            self.vprovider = mysql.connector
        else:
            self.app.set_status(f"INVALID V_SQL_PROVIDER", "ERROR")
            raise Exception("Invalid SQL provider. Edit in config.json")
            
        # TODO options for patients database too
        if os.getenv("P_SQL_PROVIDER") == "ORACLE":
            self.pprovider = oracledb
            self.pdbconnect_options = {
                "user": os.getenv("P_SQL_USER"),
                "password": os.getenv("P_SQL_PASSWORD"),
                "dsn": os.getenv("P_SQL_HOST")+r"/"+os.getenv("P_SQL_DATABASE"),

            }
        elif os.getenv("P_SQL_PROVIDER") == "MYSQL":
            self.pprovider = mysql.connector
            self.pdbconnect_options = {
                "host": os.getenv("P_SQL_HOST"),
                "port": os.getenv("P_SQL_PORT"),
                "user": os.getenv("P_SQL_USER"),
                "password": os.getenv("P_SQL_PASSWORD"),
                "database": os.getenv("P_SQL_DATABASE"),
            }

        else:
            self.app.set_status(f"INVALID V_SQL_PROVIDER", "ERROR")
            raise Exception("Invalid SQL provider. Edit in config.json")

        try:
            self.vdb = self.vprovider.connect(**v_options)
            self.ok = True
            # put table names in environment variables for convenience
            self.video_table = os.getenv("V_SQL_VIDEO_TABLE")
            self.patient_table= os.getenv("P_SQL_PATIENT_TABLE")
            self.cursor = self.vdb.cursor()
            self.saved = False
        except Exception as e:
            self.ok = False
            self.app.set_status(f"[DB ERROR] {e}", "ERROR")

    
    def save(self, *args):
    # args = (patient_id, video_type, date_of_visit) 

        # check whether something was recorded or not
        if not os.path.isfile('output.mp4'):
            self.app.set_status(f"WARNING: NO FILE RECORDED","WARNING")
            return

        filename = self.generate_filename(*args)

        status = self.save_to_server(*args,filename)

        if self.saved:
            self.update_db(*args,filename)
            self.app.set_status(f"Successfully saved as {filename} to the server!","SUCCESS")
        else:
            print(status) # write the status
            self.app.set_status(f"Failed to save with ERROR: {status}","ERROR")
    
    def save_to_server(self, patient_id, video_type, date_of_visit, filename):
        try:
            # TODO server saving logic
            os.makedirs(os.path.dirname(filename),exist_ok=True)
            try:
                shutil.copy('output.mp4',filename)
                self.saved = True
                os.remove('output.mp4')
                return f"saved file as {filename} successfully"
            except:
                self.saved = False
                return f"An error occured while copying the file to server"

        except Exception as e:
            self.saved = False
            # else
            return e

    def update_db(self, patient_id, video_type, date_of_visit, filename):
        self.saved = False
        try:
            self.cursor.execute(
                f"INSERT INTO `{self.video_table}` (patient_id, video_type, filename, date_of_visit) values (%s, %s, %s, %s)",
                (patient_id,video_type,filename, date_of_visit),)
            self.vdb.commit()
            print("DB UPDATE:",self.cursor.rowcount, "rows inserted, ID:", self.cursor.lastrowid);
        except Exception as e:
            print("ERROR UPDATE DB", e)
    
    def get_patient_data(self, patient_id):
        same =  os.getenv("P_SQL_DATABASE") == os.getenv("V_SQL_DATABASE")
        try:
            if (same):
                print('same database used')
                pcursor = self.cursor
                pcursor.execute(f"""
                SELECT `{config.patient_table_args["id"]}`, `{config.patient_table_args["name"]}`,
                `{config.patient_table_args["date_of_birth"]}`, `{config.patient_table_args["sex"]}`
                FROM {self.patient_table} where id={patient_id}""")
                print('I am here')
                result = pcursor.fetchall()
                print("FETCHED PATIENT DATA:", result)
            else:
                print('creating a new connection')
                pdb = self.pprovider.connect(**self.pdbconnect_options)
                pcursor = pdb.cursor()
                print('123412341234')
                pcursor.execute(f"""
                SELECT `{config.patient_table_args["id"]}`, `{config.patient_table_args["name"]}`,
                `{config.patient_table_args["date_of_birth"]}`, `{config.patient_table_args["sex"]}`
                FROM {self.patient_table} where id={patient_id}""")
                result = pcursor.fetchall()
                print("FETCHED PATIENT DATA:", result)
                pcursor.close()
                pdb.close()
            if result:
                return result[0]
            else:
                return False
        except Exception as e:
            print("ERROR PATIENT DATA",e)

    def generate_filename(self,*args):
        # get the latest filename form server
        patient_id, type, *_ = args
        self.cursor.execute(
            f""" select r.patient_id, r.video_type, r.filename, r.created from rec_save_videos r 
                inner join (
                    select patient_id, video_type, max(created) as MaxDate
                    from rec_save_videos
                    group by video_type, patient_id ) rm
                on  r.patient_id=rm.patient_id and
                    r.video_type=rm.video_type and
                    r.created=rm.MaxDate
                where r.patient_id=%s and r.video_type=%s
            """,(patient_id, type));  # date_of_visit argument not required
        result = self.cursor.fetchall()
        # extract last number and get next one (could have done better using regex)
        if result:
            # increment and format (we use -1 to take the last entry to prevent redundency, but our app will take care of it anyway)
            formatted_number = "%03d" % (int(result[-1][2].split(type)[1].split(".")[0])+1)
        else:
            # first video of this type
            formatted_number = "%03d" % 1
        # change "%03d" to %04d% for 4 digits
        return f"{config.fileServerLocation}/{patient_id}/{args[2].replace('-','')}/{type}{formatted_number}.mp4"
    
    def close(self):
        # can't keep the connection open else, other instances won't be able to use it.
        try:
            if self.vprovider.__name__ == "MSSQL":
                self.vdb.commit()
            self.vdb.close()
        except Exception as e:
            print("ERROR CLOSE", e)
        
        

        



        





if __name__ == "__main__":
    root = tk.Tk()
    root.title("Rec Save")
    app = App(master=root)
    app.mainloop()
    app._cam.release()
