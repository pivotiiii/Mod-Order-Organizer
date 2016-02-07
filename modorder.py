import os
import glob
import time
import filedialog
import logging
import registry_access as reg
#import GUI_2 as gui


moprofilesdir=""
moprofilesdirbak="C:/"
moprofiles=[]
profiledirs=[]
templist = []
importlist = []
importmodlist = []
importactlist = []
exportlist = []
exportmodlist = []
exportactlist = []
backupvar = 0
radiovar = -1
profiledirsbak = []
profiledirsdis = []
activeprofiles = []
activeprofiles2 = []
timepassed = 0.0
tries = 0


def start(filedialogoutput):
    #print("--start--")
    #print(filedialogoutput)
    #print("end")
    logging.info("mo.start called sucessfully")
    logging.info("importing global variables")
    global moprofilesdir
    global moprofilesdirbak
    global moprofiles
    global profiledirs
    global profiledirsbak
    global profiledirsdis
    global tries
    try:
        reg.set_reg("profiles_dir_bak", moprofilesdir)
    except:
        a=0
    print("check 1")
    #print(filedialogoutput)
    logging.info("importing global variables done") 
    s = list(filedialogoutput)
    #file_loc = open("location.txt", "w", encoding="utf8")
    #file_loc.write(filedialogoutput)
    #file_loc.close()
    #logging.info(s)
    for i in range(0, len(s)):
        if s[i] == "\\":
            s[i]= "/"
    filedialogoutput = "".join(s)
    #moprofilesdirbak = moprofilesdir
    if filedialogoutput.endswith("/"):
        moprofilesdir = filedialogoutput
    else:
        moprofilesdir = filedialogoutput + "/"
    reg.set_reg("profiles_dir", moprofilesdir)
    try:
        if reg.get_reg("profiles_dir_bak") == None:
            reg.set_reg("profiles_dir_bak", moprofilesdir)

        elif reg.get_reg("profiles_dir_bak") == "":
            reg.set_reg("profiles_dir_bak", moprofilesdir)
    except:
        a=9
    logging.info("moprofilesdir: " + moprofilesdir)
    #print(moprofilesdir)
    moprofiles = []
    print("check 2")
    profiles_string = "profiles/"
    if moprofilesdir.endswith("rofiles/") or moprofilesdir.endswith("rofiles\\"):
        logging.info("--if statement went through")
        for entry in os.scandir(moprofilesdir):
            logging.info("----for statement went through")
            if not entry.name.startswith(".") and entry.is_dir():
                logging.info("------if not statement went through")
                moprofiles.append(entry.name)
                logging.info("--------moprofiles appended")
            else:
                logging.warning("------if not statement did not go through, maybe not a folder?")
        profiledirs = []
        #profiledirsbak = []

        for i in range(0,len(moprofiles)):
            profiledirs.append(moprofilesdir + moprofiles[i] + "/")

        logging.info("------profiledirs------")
        logging.info(profiledirs)
        logging.info("-----------------------")
        print("check 3")
        

    else:
        cache = tries
        tries = cache + 1
        if tries > 1:
            tries = 0
            if len(reg.get_reg("profiles_dir_bak")) < 8:
                start(reg.get_reg("profiles_dir_bak"))
            else:
                try:
                    start(filedialog.askdirectory(title="Open profiles directory - JUST DO IT", initialdir = last_location))
                except:
                    start(filedialog.askdirectory(title="Open profiles directory - JUST DO IT"))
        else:
            try:
                try:
                    start(reg.get_reg("profiles_dir_bak"))
                except:
                    start(filedialog.askdirectory(title="Open profiles directory - JUST DO IT", initialdir = last_location))
            except:
                start(filedialog.askdirectory(title="Open profiles directory - JUST DO IT"))
        #logging.warning("path does not end with rofiles/")
        #logging.warning("calling mo.start again")
        


def doimports(importdirectory):
    global exportlist
    global exportmodlist
    global exportactlist
    global importlist
    global importmodlist
    global importactlist
    importfile = importdirectory + "/modlist.txt"
    importlist= []
    importlistfile = open(importfile, "r", encoding="utf8")
    importlist = [line.strip() for line in importlistfile]
    importlistfile.close()
    importmodlist = []
    modnames(importlist, importmodlist)
    importactlist = []
    actives(importlist, importactlist)


def modnames(selectedlist, selectedmodlist):        #makes a list of modnames
    global exportlist
    global exportmodlist
    global exportactlist
    global importlist
    global importmodlist
    global importactlist
    for i in range(0,len(selectedlist)):        
        s = selectedlist[i]
        s = s[1:]
        selectedmodlist.append(s)
    #return selectedmodlist


def actives(selectedlist, selectedactlist):         #makes a list of + and - signs to show active mods
    global exportlist
    global exportmodlist
    global exportactlist
    global importlist
    global importmodlist
    global importactlist
    for i in range(0,len(selectedlist)):      
        s = selectedlist[i]
        s = s[:1]
        selectedactlist.append(s)
    #return selectedactlist


#def modsort2(selectedimportmodlist, selectedimportactlist, selectedexportmodlist, selectedexportactlist):        #sorts mods of exportmodlist like importmodlist
#    global exportlist
#    global exportmodlist
#    global exportactlist
#    global importlist
#    global importmodlist
#    global importactlist
#    for i in range(0, len(selectedimportmodlist)):
#        logging.info("--trying" + str(i))
#        try:
#            if selectedimportmodlist[i] != selectedexportmodlist[i]:
#                logging.info("----if statement went through")
#                modindex = selectedexportmodlist.index(selectedimportmodlist[i])
#                logging.info("got index of mod to sort from exportmodlist")
#                templist = selectedexportmodlist[modindex]
#                logging.info("saved mod at index to temp")
#                selectedexportmodlist[modindex] = selectedexportmodlist[i]
#                logging.info("mod @ i moved to mod @ index")
#                selectedexportmodlist[i] = templist
#                logging.info("mod in temp to mod @ i")
#                templist = selectedexportactlist[modindex]
#                logging.info("saved active state at index to temp")
#                selectedexportactlist[modindex] = selectedexportactlist[i]
#                logging.info("state @ i moved to state @ index")
#                selectedexportactlist[i] = templist
#                logging.info("state in temp to state @ i")
#        except ValueError:
#            logging.warning("an error occured during mo.modsort")
#            print(selectedimportmodlist[0])
#    #return exportmodlist

def modsort(selectedimportmodlist, selectedimportactlist, selectedexportmodlist, selectedexportactlist):        #sorts mods of exportmodlist like importmodlist
    global exportlist
    global exportmodlist
    global exportactlist
    global importlist
    global importmodlist
    global importactlist
    for i in range(0, len(selectedimportmodlist)):
        #logging.info("--trying" + str(i))
        if selectedimportmodlist[i] != selectedexportmodlist[i]:
            logging.info("----if statement went through")
            try:
                modindex = selectedexportmodlist.index(selectedimportmodlist[i])
            except ValueError:
                logging.info("Value Error Nr: 1")
                try:
                    test = selectedimportmodlist[i]
                    modindex = selectedexportmodlist.index(test[1:])
                except ValueError:
                    logging.info("Value Error Nr: 2")
                    k = str(i)
                    logging.warning(selectedimportmodlist[i])
                    logging.warning(selectedimportactlist[i])
                    logging.warning("there was simply no match in mo.modorder for mod: " + k + " = " + selectedimportmodlist[i])
                    raise ValueError
            logging.info("got index of mod to sort from exportmodlist")
            templist = selectedexportmodlist[modindex]
            logging.info("saved mod at index to temp")
            selectedexportmodlist[modindex] = selectedexportmodlist[i]
            logging.info("mod @ i moved to mod @ index")
            selectedexportmodlist[i] = templist
            logging.info("mod in temp to mod @ i")
            templist = selectedexportactlist[modindex]
            logging.info("saved active state at index to temp")
            selectedexportactlist[modindex] = selectedexportactlist[i]
            logging.info("state @ i moved to state @ index")
            selectedexportactlist[i] = templist
            logging.info("state in temp to state @ i")
        #except ValueError:
            #logging.warning("an error occured during mo.modsort")
            #print(selectedimportmodlist[0])
    #return exportmodlist

def comblists(selectedlist, selectedmodlist, selectedactlist):
    global exportlist
    global exportmodlist
    global exportactlist
    global importlist
    global importmodlist
    global importactlist
    for i in range(0,len(selectedlist)):
        selectedlist[i]=selectedactlist[i]+selectedmodlist[i]


def do_it(importdirectory):
    global exportlist
    global exportmodlist
    global exportactlist
    global importlist
    global importmodlist
    global importactlist
    global backupvar
    global radiovar
    global activeprofiles
    global moprofiles
    global timepassed
    t0 = time.time()
    logging.info("doing imports")
    doimports(importdirectory)
    logging.info("imports done")
    for i in range(0, len(profiledirs)):
        logging.info("-----trying" + moprofiles[i])
        if i == radiovar:
            logging.info(moprofiles[i] + ": master list wont get copied")
        else:
            if activeprofiles[i] == "disabled":
                logging.info(moprofiles[i] + ": disabled profiles wont get copied")
            else:
                modlistfile = profiledirs[i] + "modlist.txt"
                exportlist = []
                logging.info("opening modlist.txt")
                exportlistfile = open(modlistfile, "r", encoding="utf8")
                logging.info("making list out of modlist.txt")
                exportlist= [line.strip() for line in exportlistfile]
                exportlistfile.close()
                logging.info("closing modlist.txt")
                exportmodlist = []
                logging.info("getting modnames from list")
                modnames(exportlist, exportmodlist)
                logging.info("getting modnames from list done")
                exportactlist = []
                logging.info("getting actives from list")
                actives(exportlist, exportactlist)
                logging.info("getting actives from list done")
                logging.info("sorting mods")
                modsort(importmodlist, importactlist, exportmodlist, exportactlist)
                logging.info("sorting mods done")
                logging.info("combining actives + mods")
                comblists(exportlist, exportmodlist, exportactlist)
                logging.info("combining actives + mods done")
                logging.info("checking backupvar")
                if backupvar == 1:
                    logging.info("backupvar == 1")
                    os.rename(modlistfile, profiledirs[i] + "modlist-sorted_like_masterlist" + time.strftime("%d-%m-%Y-%H-%M-%S") + ".txt")
                    logging.info("backup done")
                else:
                    logging.info("backupvar == 0")
                logging.info("creating new/ editing existing modlist.txt")
                finalfile = open(profiledirs[i] + "modlist.txt", "w", encoding="utf8")
                logging.info("writing to modlist.txt")
                for item in exportlist:
                    finalfile.write("%s\n" % item)
                logging.info("writing to modlist.txt done")
                finalfile.close()
                logging.info("-----" + moprofiles[i] + ": done")
    timepassed= time.time() - t0
