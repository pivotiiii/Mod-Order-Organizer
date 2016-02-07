import tkinter as tk
import tkinter.ttk as ttk
import filedialog
import modorder_2 as mo
import mod_plugin_sort_MO as ps
import sys
import os
from PIL import Image, ImageTk
import logging
import time
import registry_access as reg
#import fileinput




class Application(tk.Frame):
    def __init__(self, master=None):
        try:
            find_debug = open("debug.log", "r")
            find_debug.close()
            self.timestamp=str(time.time())
            print("trying open")
            find_debug = open("debug.log", "a")
            print("file open")
            find_debug.write("|||||||||||||||||||||" + self.timestamp + "|||||||||||||||||||||" + "\n")
            find_debug.close()
            print("file closed")
            self.debugfilefound = 1
        except:
            self.debugfilefound = 0
        
        logging.basicConfig(filename="debug.log", level = logging.DEBUG)
        logging.info("--------------------------------------------------------------------------------------------------")
        logging.info("initalizing mainwindow")
        tk.Frame.__init__(self, master)
        self.pack(side="top", fill="both", expand=True)
        self.tabs = ttk.Notebook(self)
        self.tabs.pack(side="bottom", fill="both", expand=True)
        self.imageframe = tk.Frame(self)
        self.textframe = tk.Frame(master=self.tabs)
        self.textframe2 = tk.Frame(master=self.tabs)
        self.imageframe.pack(side="top", fill="both", expand=True)
        self.textframe.pack(side="bottom", fill="both", expand=True)
        self.textframe2.pack(side="bottom", fill="both", expand=True)
        self.tabs.add(self.textframe, text = "Sort modlist like another modlist")
        self.tabs.add(self.textframe2, text = "Sort modlist like pluginlist")
        self.textframe.columnconfigure(2, minsize=235)
        self.textframe2.columnconfigure(2, minsize=280)
        self.last_location = None
        self.last_master = None
        logging.info("initalizing mainwindow done")
        
        


    def afterinit(self):
        try:
            logging.info("mo.start gets called")
            try:
                logging.info("checking registry for past data")
                self.last_location = reg.get_reg("profiles_dir")
                print(self.last_location)
                self.last_master = int(reg.get_reg("last_master"))
                self.mods_dir = reg.get_reg("mods_dir")
                if len(self.last_location) < 3:
                    print("warum error?")
                    logging.info("last location empty?")
                    raise IOError
                logging.info("calling mo.start")
                logging.info(self.last_location)
                print("last location: " + str(self.last_location))
                mo.start(str(self.last_location))
                print("check 7")
            except:
                print("no reg data")
                logging.info("no registry data found / registry data has errors?")
                mo.start(filedialog.askdirectory(title="Open profiles directory"))
                self.last_master = 0
                self.mods_dir = ""

            self.importdir = ""
            self.profiledirsbak = mo.profiledirsbak
            self.activeprofiles = []
            self.activeprofiles2 = []
            for i in range(0, len(mo.moprofiles)):
                self.activeprofiles.append("disabled")
                self.activeprofiles2.append("disabled")
            print("check 4")
            mo.activeprofiles=self.activeprofiles
            mo.activeprofiles2=self.activeprofiles2
            logging.info("creating widgets")
            print("check widgets")
            self.createWidgets()
            print("check 5")
            logging.info("creating image")
            self.createImage()
            print("check 6")
        except:
            try:
                print("afterinit2")
                self.afterinit2()
            except:
                print("wtf")
                logging.warning("mo.start returned an error or there was a problem with the first afterinit") 
                self.exit()

    def afterinit2(self):
        logging.info("mo.start gets called")
        mo.start(filedialog.askdirectory(title="Open profiles directory"))
        self.importdir = ""
        self.last_master = 0
        self.profiledirsbak = mo.profiledirsbak
        self.activeprofiles = []
        self.activeprofiles2 = []
        for i in range(0, len(mo.moprofiles)):
            self.activeprofiles.append("disabled")
            self.activeprofiles2.append("disabled")
        mo.activeprofiles=self.activeprofiles
        mo.activeprofiles2=self.activeprofiles2
        self.refresh()
        self.createWidgets()
        self.createImage()
        ##logging.info("mo.start returned an error") 
        ##self.exit()
        
    


    def createWidgets(self):

        #tab 1

        if int(self.last_master) >= len(mo.moprofiles):
            self.last_master = 0
            reg.set_reg("last_master", "0")
        
        self.radiovar = tk.IntVar()
        self.radiovar.set(0)
        
        self.checkbuttons = []
        self.checkbuttonvars = []
        self.radiobuttons = []


        
        for i in range(0, len(mo.moprofiles)):
            self.checkbuttonvars.append(tk.StringVar())
            self.checkbuttonvars[i].set("disabled")
            self.checkbuttons.append(tk.Checkbutton(self.textframe, text=mo.moprofiles[i], onvalue = "enabled", offvalue = "disabled", variable = self.checkbuttonvars[i], command = lambda i=i: self.modifyprofiles(i)))
            self.checkbuttons[i].grid(column=2, row=i+1, sticky="W")
        self.checkbuttons[int(self.last_master)].config(state=tk.DISABLED)
        
        for i in range(0, len(mo.moprofiles)):
            self.radiobuttons.append(tk.Radiobutton(self.textframe, variable=self.radiovar, value = i, command= lambda i=i: self.radiocom(i)))
            self.radiobuttons[i].grid(column=1, row=i+1)
        self.radiobuttons[int(self.last_master)].select()
        
        self.importlabel=tk.Label(self.textframe, text="Master \n Order")
        self.importlabel.grid(column=1, row = 0, sticky = "W")
        self.exportlabel=tk.Label(self.textframe, text="Orders to override")
        self.exportlabel.grid(column=2, row = 0, sticky = "W")

        self.startbutton=tk.Button(self.textframe, text="Start", command=lambda: self.startmo())
        self.startbutton.grid(column=3, row=1, sticky = "N" + "W" + "S" + "E")

        self.filevar = tk.StringVar()
        self.filebutton=tk.Button(self.textframe, text="Choose profiles directory", command=lambda: self.afterinit2())
        self.filebutton.grid(column=3, row=2, sticky = "N" + "W" + "S" + "E")

        self.quitbutton = tk.Button(self.textframe, text="Quit", command=lambda: self.savelog())
        self.quitbutton.grid(column=3, row=3, sticky = "N" + "W" + "S" + "E")

        self.backupvar = tk.IntVar()
        self.backupbutton = tk.Checkbutton(self.textframe, text="Backup modlist.txt?", variable = self.backupvar, command= self.backup)
        self.backupbutton.grid(column=3, row=4, sticky = "N" + "W" + "S")
        self.backupbutton.invoke()

        self.logvar = tk.IntVar()
        self.logbutton = tk.Checkbutton(self.textframe, text="DEBUG", variable = self.logvar)
        self.logbutton.grid(column=3, row=5, sticky = "N" + "W" + "S")

        #tab 2

        #self.radiovar2 = tk.IntVar()
        #self.radiovar2.set(0)

        self.checkbuttons2 = []
        self.checkbuttonvars2 = []

        for i in range(0, len(mo.moprofiles)):
            self.checkbuttonvars2.append(tk.StringVar())
            self.checkbuttonvars2[i].set("disabled")
            self.checkbuttons2.append(tk.Checkbutton(self.textframe2, text=mo.moprofiles[i], onvalue = "enabled",
                                                     offvalue = "disabled", variable = self.checkbuttonvars2[i], command = lambda i=i: self.modifyprofiles2(i)))
            self.checkbuttons2[i].grid(column=2, row=i+1, sticky="W")
            
        #self.checkbuttons2[int(self.last_master)-1].config(state=tk.DISABLED)

        self.importlabel2=tk.Label(self.textframe2, text=" \n ")
        self.importlabel2.grid(column=1, row = 0, sticky = "W")

        self.exportlabel2=tk.Label(self.textframe2, text="Profiles to sort")
        self.exportlabel2.grid(column=2, row = 0, sticky = "W")

        self.startbutton2=tk.Button(self.textframe2, text="Start", command=lambda: self.startps())
        self.startbutton2.grid(column=3, row=1, sticky = "N" + "W" + "S" + "E")

        self.filevar2 = tk.StringVar()
        self.filebutton2=tk.Button(self.textframe2, text="  Choose mods directory  ",
                                   command=lambda : self.get_get_mods_dir())
        self.filebutton2.grid(column=3, row=2, sticky = "N" + "W" + "S" + "E")

        self.quitbutton2 = tk.Button(self.textframe2, text="Quit", command=lambda: self.savelog())
        self.quitbutton2.grid(column=3, row=3, sticky = "N" + "W" + "S" + "E")

        self.backupbutton2 = tk.Checkbutton(self.textframe2, text="Backup modlist.txt?", variable = self.backupvar, command= self.backup())
        self.backupbutton2.grid(column=3, row=4, sticky = "N" + "W" + "S")

        self.logbutton2 = tk.Checkbutton(self.textframe2, text="DEBUG", variable = self.logvar)
        self.logbutton2.grid(column=3, row=5, sticky = "N" + "W" + "S")

        
        
        

    def createImage(self):
        self.canvas = tk.Canvas(self.imageframe, height = 90)
        self.canvas.pack(side="top", fill="both", expand= True)
        
        self.headerpath = self.resource_path("header.gif")
        self.header = tk.PhotoImage(file = self.headerpath)
        self.canvas.create_image(-20,45, image=self.header, anchor="w")


    def modifyprofiles(self, button):
        mo.activeprofiles[button]=self.checkbuttonvars[button].get()
        print("---------------------")
        for i in range(0, len(self.checkbuttons)):
            print(mo.moprofiles[i] + ": " + self.checkbuttonvars[i].get())
        print("---------------------")

    def modifyprofiles2(self, button):
        mo.activeprofiles2[button]=self.checkbuttonvars2[button].get()
        print("---------------------")
        for i in range(0, len(self.checkbuttons2)):
            print(mo.moprofiles[i] + ": " + self.checkbuttonvars2[i].get())
        print("---------------------")


    def get_get_mods_dir(self):
        try:
            self.get_mods_dir(filedialog.askdirectory(title="Open mods directory", initialdir = self.mods_dir))
        except:
            self.get_mods_dir(filedialog.askdirectory(title="Open mods directory"))

    def get_mods_dir(self, filedialogoutput):
        if filedialogoutput.endswith("/"):
            self.mods_dir = filedialogoutput
        else:
            self.mods_dir = filedialogoutput + "/"
        self.mods_dir_bak = reg.get_reg("mods_dir_bak")
        if self.mods_dir.endswith("ods/"):
            reg.set_reg("mods_dir_bak", self.mods_dir)
            reg.set_reg("mods_dir", self.mods_dir)
        elif self.mods_dir[0].isalpha():
            self.get_mods_dir(filedialog.askdirectory(title="Open mods directory"))
        elif self.mods_dir == "/":
            if self.mods_dir_bak == "/":
                self.get_mods_dir(filedialog.askdirectory(title="Open mods directory"))
            else:
                self.mods_dir = reg.get_reg("mods_dir_bak")
        print(self.mods_dir)
        

        
    def backup(self):
        mo.backupvar = self.backupvar.get()
        ps.backupvar = self.backupvar.get()


    def refresh(self):
        for i in range(0, len(self.checkbuttons)):
            self.checkbuttons[i].grid_forget()
            self.radiobuttons[i].grid_forget()
            self.checkbuttons2[i].grid_forget()
        self.importlabel.grid_forget()
        self.exportlabel.grid_forget()
        self.startbutton.grid_forget()
        self.filebutton.grid_forget()
        self.quitbutton.grid_forget()
        self.backupbutton.grid_forget()
        self.logbutton.grid_forget()
        self.importlabel2.grid_forget()
        self.exportlabel2.grid_forget()
        self.startbutton2.grid_forget()
        self.filebutton2.grid_forget()
        self.quitbutton2.grid_forget()
        self.backupbutton2.grid_forget()
        self.logbutton2.grid_forget()
        self.canvas.pack_forget()
                       
        #if mo.start(filedialog.askdirectory(title="Open profiles directory")) == 2:
            #self.exit()
        #else:
        #self.afterinit2()            


    def savelog(self):
        print("called savelog")
        logging.info("self.savelog called")
        if self.logvar.get() == 0 and self.debugfilefound == 0:
            logging.info("no debug file and debug not checked")
            logger = logging.getLogger()
            logger.handlers[0].stream.close()
            logger.removeHandler(logger.handlers[0])
            logger.disabled = True
            os.remove("debug.log")
        if self.logvar.get() == 0 and self.debugfilefound == 1:
            logging.info("debug file found and debug not checked")
            logger = logging.getLogger()
            logger.handlers[0].stream.close()
            logger.removeHandler(logger.handlers[0])
            logger.disabled = True
            
            num_lines = sum(1 for line in open('debug.log'))
            #print(num_lines)
            time_line = self.get_line_number(self.timestamp, "debug.log")
            #print(time_line)

            with open("debug.log","r") as textobj:
                liste=list(textobj)

            #print(liste)

            for i in range(time_line, num_lines):
                del liste[time_line]
            del liste[time_line - 1]

            with open("debug.log", "w") as textobj:
                for n in liste:
                    textobj.write(n)
        self.exit()





    def exit(self):
        #if self.start_went_through():
        #    self.savelog()
        logging.info("exiting")
        self.grid_forget()
        self.master.destroy()

    def start_went_through(self):
        try:
            self.savelog()
            return True
        except:
            return False


    def get_line_number(self, phrase, file_name):
        with open(file_name) as f:
            for i, line in enumerate(f, 1):
                if phrase in line:
                    return i
        
    def radiocom(self, button):
        self.disablecb(button)
        self.importdir= mo.profiledirs[button]
        mo.radiovar= self.radiovar.get()
        reg.set_reg("last_master", str(button))
            
    def radiocom2(self, button):
        self.disablecb(button)
        self.importdir= mo.profiledirs[button]
        mo.radiovar= self.radiovar.get()
        
        location_file = open("location.txt", "r+")
        lines = [line.strip() for line in location_file]
        location_file.close()
        try:
            lines[1] = str(button)
        except:
            lines.append(str(button))
        location_file = open("location.txt", "w")
        for item in lines:
            location_file.write("%s\n" % item)
        location_file.close()
        #location_file.close()
            
        print("Current master: " + mo.moprofiles[button])


    def disablecb(self, button):
        for i in range(0, len(self.checkbuttons)):
            self.checkbuttons[i].config(state=tk.NORMAL)
        self.checkbuttons[button].deselect()
        self.checkbuttons[button].config(state=tk.DISABLED)


    def startps(self):
        try:
            if len(reg.get_reg("mods_dir")) > 1:
                a=1
        except:
            print("except")
            self.get_get_mods_dir()
        try:
            for i in range(0, len(self.checkbuttons2)):
                if self.checkbuttonvars2[i].get() == "enabled":
                    ps.do_it(self.mods_dir, mo.profiledirs[i])
            self.done("Done!", "Done!", 2, 20)
        except:
            raise ValueError


    def startmo(self):
        logging.info("starting mo.do_it")
        try:
            mo.do_it(mo.profiledirs[self.radiovar.get()])
            logging.info("mo.do_it done")
            logging.info("making popup")
            self.done("Done! \n in " + str(mo.timepassed)[:5] + " seconds", "Done!", 2, 20)
        except ValueError:
            logging.warning("mo.do_it or one of its subfunctions had a value error")
            logging.info("making error popup")
            self.done("ERROR: Please open each profile in Mod Organizer \n so the modlist.txt gets updated!", "ERROR!", 4, 40)
        

    def done(self, msg, title, h, w):
        popup = tk.Tk()
        popup.title(title)
        label = tk.Label(popup, text=msg, anchor = tk.CENTER, height = h, width = w)
        label.pack(side="top", fill="both", expand=True)
        B1 = tk.Button(popup, text="Okay", command = popup.destroy)
        B1.pack(side="bottom", fill="both", expand=True)
        popup.iconbitmap("icon.ico")
        popup.mainloop()

    def resource_path(self, relative_path):
        """ Get absolute path to resource, works for dev and for PyInstaller """
        try:
            # PyInstaller creates a temp folder and stores path in _MEIPASS
            base_path = sys._MEIPASS
        except Exception:
            base_path = os.path.abspath(".")

        return os.path.join(base_path, relative_path)
            

app = Application(0)
logging.info("configuring main window")
app.master.title('Mod Order Organizer')
app.master.protocol('WM_DELETE_WINDOW', app.savelog)
app.master.resizable(width = False, height = False)
app.master.iconbitmap(app.resource_path("icon.ico"))
deffont = ("Segoe UI", 12)
app.master.option_add("*Font", deffont)
logging.info("configuring main window done")
logging.info("starting afterinit")
app.afterinit()
logging.info("afterinit done")

app.mainloop()
