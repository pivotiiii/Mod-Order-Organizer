import modorder_2 as mo
import os
import winreg
import time
import logging


#problem: grad nix??


plugins = dict()
all_mods = []
mods_without_plugin = []
mods_with_plugin = []
loadorder = []
pluginorder = []
plugins_in_data_folder = []
exportmodlist = []
exportactlist = []
delete_list = []
sorted_modlist = []
sorted_actlist = []
cor_mod = ""
plugin_list = []
plugin_list_un = []
backupvar = 1
plugins_to_ignore= []


def get_data_path():
    logging.info("getting data path from registry")
    try:
        logging.info("looking in WOW6432Node")
        root_key=winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r'SOFTWARE\WOW6432Node\bethesda softworks\skyrim', 0, winreg.KEY_READ)
        [Pathname,regtype]=(winreg.QueryValueEx(root_key,"installed path"))
        winreg.CloseKey(root_key)
        logging.info("found it")
        return Pathname + "data\\"
    except:
        try:
            logging.info("looking outside of WOW6432Node")
            root_key=winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r'SOFTWARE\bethesda softworks\skyrim', 0, winreg.KEY_READ)
            [Pathname,regtype]=(winreg.QueryValueEx(root_key,"installed path"))
            winreg.CloseKey(root_key)
            logging.info("found it")
            return Pathname + "data\\"
        except:
            logging.info("no data path found in registry")
            raise WindowsError
    print(Pathname)


def get_loadorder(profiledir):
    global loadorder
    logging.info("getting loadorder")
    loadorder_file_location = profiledir + "/loadorder.txt"
    loadorder = []
    loadorderfile = open(loadorder_file_location, "r", encoding="utf8")
    loadorder = [line.strip() for line in loadorderfile]
    loadorderfile.close()
    logging.info("loadorder found")
    #return loadorder

def get_plugins(profiledir):
    global pluginorder
    logging.info("getting plugins")
    pluginorder_file_location = profiledir + "/plugins.txt"
    pluginorder = []
    pluginorderfile = open(pluginorder_file_location, "r", encoding="utf8")
    pluginorder = [line.strip() for line in pluginorderfile]
    pluginorderfile.close()
    logging.info("plugins found")

def get_unmanaged_plugins():
    global plugins
    global plugins_in_data_folder

    logging.info("getting unmanaged plugins")
    data_plugins = get_plugins_in_data()
    plugins_in_mods_folder = list(plugins.values())
    plugins_in_data_folder = list(set(data_plugins) - set(plugins_in_mods_folder))
    for k in range(0, len(plugins_in_data_folder)):
        plugins["Unmanaged: " + plugins_in_data_folder[k][:-4]] = plugins_in_data_folder[k]
        all_mods.append("Unmanaged: " + plugins_in_data_folder[k][:-4])
    logging.info("found unmanaged plugins")


    
def get_plugins_in_data():
    logging.info("getting plugins in data folder")
    data_path = get_data_path()
    data_plugins = [i for i in os.listdir(data_path) if (i.endswith(".esp") or i.endswith(".esm"))]
    logging.info("found plugins in data folder")
    return data_plugins


def run_through_MO():
    global loadorder

    logging.info("run_through_MO called??? wtf")
    if len(get_plugins_from_data()) == (len(pluginorder) - 1):
        return True
    else:
        return False

 
def get_plugin_locations(modsdir):
    global plugins
    global all_mods
    global loadorder
    global plugins_to_ignore

    logging.info("getting plugin locations")

    plugins_to_ignore = []

    s = list(modsdir)
    
    for i in range(0, len(s)):
        if s[i] == "\\":
            s[i] = "/"
    all_mods = os.listdir("".join(s))
    
    for j in range(0, len(all_mods)):
        multi_esp_index = []
        current_modpath = str(modsdir + "\\" + all_mods[j] + "\\")
        files_esp_esm = [i for i in os.listdir(current_modpath) if (i.endswith(".esp") or i.endswith(".esm"))]
        lowest_plugin = get_lowest_plugin(files_esp_esm)
        plugins[all_mods[j]] = lowest_plugin

    #print("plugins to ignore: " + str(plugins_to_ignore))
    logging.info("got plugin locations")


def get_lowest_plugin(multiple_plugin_list):
    global loadorder
    global plugins_to_ignore

    logging.info("getting lowest plugin from list: " + str(multiple_plugin_list))
    multi_esp_index = []
    
    if len(multiple_plugin_list) > 1:            
            for k in range(0, len(multiple_plugin_list)):
                
                try:
                    multi_esp_index.append(loadorder.index(multiple_plugin_list[k]))            
                except:
                    multi_esp_index.append(10000)

            lowest_esp_index = min(multi_esp_index)
            chosen_esp_index = multi_esp_index.index(lowest_esp_index)
            cache = multiple_plugin_list[chosen_esp_index]
            for p in range(0, len(multiple_plugin_list)):
                if not multiple_plugin_list[p] == cache:
                    plugins_to_ignore.append(multiple_plugin_list[p])
            multiple_plugin_list = []
            multiple_plugin_list.append(cache)
    else:
        a=1

    try:
        logging.info("returning lowest plugin")
        return multiple_plugin_list[0]
    except:
        logging.info("lowest plugin empty --> mod has no plugin")
        return ""


def remove_nilo_plugins():
    global loadorder
    global plugins
    global all_mods
    global mods_without_plugin
    global mods_with_plugin

    logging.info("removing plugins nilo")

    mods_without_plugin = []
    mods_with_plugin = []

    for i in range(0, len(all_mods)):
        if plugins[all_mods[i]] in loadorder:
            mods_with_plugin.append(all_mods[i])
        else:
            mods_without_plugin.append(all_mods[i])

    logging.info("successfully removed plugins nilo")


def sort_active_mods(modlist, actlist):
    global loadorder
    global plugins
    global exportmodlist
    global exportactlist
    global plugins_in_data_folder
    global mods
    global delete_list
    global plugin_list
    global plugin_list_un
    global plugins_to_ignore

    logging.info("sorting active mods")
    
    sorted_modlist = []
    sorted_actlist = []
    cor_mod = ""

    plugin_list = loadorder
    plugin_list_un = []

    mods = {v:k for k, v in plugins.items()}

    mods["# This file was automatically generated by Mod Organizer."] = " This file was automatically generated by Mod Organizer."
    plugins[" This file was automatically generated by Mod Organizer."] = "# This file was automatically generated by Mod Organizer."


    print("\n ")
    print("länge modlist: " + str(len(modlist)))

    modlist_length = len(modlist)
    duplicate_amount = 0
    

    print("loadorder länge: " + str(len(loadorder)))
    print("modlist länge: " + str(len(modlist)))

        
    actual_sorting(0, len(modlist), modlist, actlist)



    print("anzahl duplikate: " + str(duplicate_amount))
    print("länge delete liste: " + str(len(delete_list)))

    logging.info("sorting active mods done")


def actual_sorting(start, end, modlist, actlist):
    global loadorder
    global plugins
    global exportmodlist
    global exportactlist
    global plugins_in_data_folder
    global mods
    global delete_list
    global plugin_list_un
    global plugins_to_ignore
    global importmodlist
    global importactlist
    global mods_with_plugin

    logging.info("---starting actual sorting")

    loadorder_single = []

    logging.info("making single loadorder")

    for plugin in loadorder:
        if not plugin in plugins_to_ignore:
            loadorder_single.append(plugin)

    print("loadorder_single länge: " + str(len(loadorder_single)))

    logging.info("sorting mods acording to single pluginlist")

    logging.info("length loadorder_single = " + str(len(loadorder_single)))
    logging.info("length mods_with_plugin = " + str(len(mods_with_plugin)))
    logging.info("length plugins_in_data_folder = " + str(len(plugins_in_data_folder)))

    for i in range(0, len(loadorder_single)):
        if loadorder_single[i] in plugins_in_data_folder:
            sorted_modlist.append("Unmanaged: " + loadorder_single[i][:-4])
            sorted_actlist.append("*")
            logging.info("run: " + str(i) + " --- Unmanaged: " + loadorder_single[i])


        else:
            print(mods[loadorder_single[i]])
            plugin_index = importmodlist.index(mods[loadorder_single[i]])
            sorted_modlist.append(importmodlist[plugin_index])
            sorted_actlist.append(importactlist[plugin_index])
            logging.info("run: " + str(i) + " --- " + importactlist[plugin_index] + mods[loadorder_single[i]])
            

    #print(sorted_modlist)
    exportmodlist = sorted_modlist
    exportactlist = sorted_actlist

    logging.info("---actual sorting done")
                    


    

def sort_modlist_like_plugins(importdirectory):
    global exportmodlist
    global exportactlist
    global mods_without_plugin
    global plugins_in_data_folder
    global exportlist
    global importlist
    global amount_sorted
    global importmodlist
    global importactlist

    logging.info("---sorting modlist like plugins")

    logging.info("doing imports")
    mo.doimports(importdirectory)
    importlist = mo.importlist
    importmodlist = mo.importmodlist
    importactlist = mo.importactlist

    importmodlist.append("Unmanaged: Skyrim")
    importactlist.append("*")
    importmodlist.append("Unmanaged: Update")
    importactlist.append("*")

    logging.info("looking for duplicate spacer folders")
    
    try:
        dupli_spacer = duplicates(importmodlist, "▇▇▇▇▇▇ SORTED UNTIL HERE ▇▇▇▇▇▇")
        del importmodlist[dupli_spacer[-1]]
        del importactlist[dupli_spacer[-1]]
        logging.info("duplicate spacer folder found and removed from modlists")
    except:
        a=1
        logging.info("no duplicate spacer folder found")
        #print("▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇")


    exportmodlist = []
    exportactlist = []
    exportlist = []

    logging.info("adding mods with plugin to the to-be-sorted-list")

    for mod, plugin in plugins.items():
        if plugin in loadorder:
            try:
                if mod in exportmodlist:
                    a=1
                else:
                    modindex = importmodlist.index(mod)
                    exportmodlist.append(importmodlist[modindex])
                    exportactlist.append(importactlist[modindex])
            except:
                if mod[1:] in exportmodlist:
                    a=1
                else:
                    modindex = importmodlist.index(mod[1:])
                    exportmodlist.append(importmodlist[modindex])
                    exportactlist.append(importactlist[modindex])
    
    print("exportmodlist länge vor active_sort: " + str(len(exportmodlist)))
    logging.info("calling sort_active_mods")
    sort_active_mods(exportmodlist, exportactlist)
    logging.info("sort_active_mods done")
    print("exportmodlist länge nach active_sort: " + str(len(exportmodlist)))

    amount_sorted = len(exportmodlist) - exportmodlist.count("DELETE")

    
    
    #missing_mods = list(set(importmodlist) - set(exportmodlist))

    logging.info("doing index sorcery to get missing mods")
    
    sorted_indexes = []

    for mod in exportmodlist:
        cur_index = importmodlist.index(mod)
        sorted_indexes.append(cur_index)

    all_indexes = []

    for i in range(0, len(importmodlist)):
        all_indexes.append(i)

    unsorted_indexes = []

    for index in all_indexes:
        if not index in sorted_indexes:
            unsorted_indexes.append(index)

    missing_mods_enabled = []
    missing_mods_disabled = []

    for index in unsorted_indexes:
        if importactlist[index] == "-":
            missing_mods_disabled.append(importmodlist[index])
        else:
            missing_mods_enabled.append(importmodlist[index])
                                    
            
        
        

    missing_mods = missing_mods_enabled + missing_mods_disabled

    #print(missing_mods)
    logging.info("adding missing mods to exportlist")
    
    for m in range(0, len(missing_mods)):
        modindex = importmodlist.index(missing_mods[m])
        exportmodlist.append(importmodlist[modindex])
        exportactlist.append(importactlist[modindex])

    for k in range(0, len(exportmodlist)):
        exportlist.append(exportactlist[k] + exportmodlist[k])

    print("anzahl missing mods: " + str(len(missing_mods)))

    logging.info("---sorting modlist like plugins done")
    
    
    

def duplicates(lst, item):
    logging.info("getting duplicates in list")
    return [i for i , x in enumerate(lst) if x == item]

            
def write_modlist(profiledir, modsdir):
    global exportlist
    global reversed_exportlist
    global backupvar

    logging.info("writing modlist")

    reversed_exportlist = []

    exportlist.insert(amount_sorted, "-▇▇▇▇▇▇ SORTED UNTIL HERE ▇▇▇▇▇▇")
    create_spacer_folder(modsdir)

    

    for i in range(0, len(exportlist)):
        reversed_exportlist.append(exportlist[-i])

    check_skse()


    print("exportlänge final : " + str(len(exportlist)))
    print("importlänge: " + str(len(importmodlist)))

    while reversed_exportlist.count("*Unmanaged: Skyrim") > 0:
        reversed_exportlist.remove("*Unmanaged: Skyrim")
        
    while reversed_exportlist.count("*Unmanaged: Update") > 0:
        reversed_exportlist.remove("*Unmanaged: Update")

    modlistfile_location = profiledir + "/modlist.txt"
    
    if backupvar == 1:
        logging.info("backing up old modlist.txt")
        os.rename(modlistfile_location, profiledir + "/modlist-sorted_like_plugins" + time.strftime("%d-%m-%Y-%H-%M-%S") + ".txt")
    
    modlistfile = open(modlistfile_location, "w", encoding = "utf8")
    for item in reversed_exportlist:
        modlistfile.write("%s\n" % item)
    modlistfile.close()

    logging.info("writing modlist done")

def check_skse():
    global reversed_exportlist

    logging.info("checking for skse")
    
    skse_instances = [s for s in reversed_exportlist if ("skse" or "SKSE" or "Skse") in s]
    print(skse_instances)
    if len(skse_instances) > 0:
        logging.info("skse instance found")
        skse = skse_instances[0]
        reversed_exportlist.remove(skse)
        reversed_exportlist.append(skse)

    logging.info("checking for skse done")
        


def spacer_folder_exists(modsdir):
    logging.info("checking for spacer folder")
    if os.path.exists(modsdir + "/▇▇▇▇▇▇ SORTED UNTIL HERE ▇▇▇▇▇▇"):
        logging.info("spacer folder exists")
        return True
    else:
        logging.info("spacer folder does not exist")
        return False

def delete_spacer_folder(modsdir):
    logging.info("deleting spacer folder")
    if spacer_folder_exists(modsdir) == True:
        os.rmdir(modsdir + "/▇▇▇▇▇▇ SORTED UNTIL HERE ▇▇▇▇▇▇")
        logging.info("deleted spacer folder")
    else:
        logging.info("no spacer folder to delete found")

def create_spacer_folder(modsdir):
    logging.info("creating spacer folder")
    os.makedirs(modsdir + "/▇▇▇▇▇▇ SORTED UNTIL HERE ▇▇▇▇▇▇")
    logging.info("creating spacer folder done")
    
    
def do_it(modsdir, profiledir):
    global plugins
    global all_mods
    global mods_without_plugin
    global mods_with_plugin
    global loadorder
    global pluginorder
    global plugins_in_data_folder
    global exportmodlist
    global exportactlist
    global delete_list
    global sorted_modlist
    global sorted_actlist
    global cor_mod
    global plugin_list
    global plugin_list_un
    global backupvar
    global plugins_to_ignore
    logging.info("ps.do_it started")

    plugins = dict()
    all_mods = []
    mods_without_plugin = []
    mods_with_plugin = []
    loadorder = []
    pluginorder = []
    plugins_in_data_folder = []
    exportmodlist = []
    exportactlist = []
    delete_list = []
    sorted_modlist = []
    sorted_actlist = []
    cor_mod = ""
    plugin_list = []
    plugin_list_un = []
    backupvar = 1
    plugins_to_ignore= []
    
    logging.info("modsdir: " + modsdir)
    logging.info("profiledir: " + profiledir)
    delete_spacer_folder(modsdir)
    get_loadorder(profiledir)
    get_plugin_locations(modsdir)
    remove_nilo_plugins()
    get_unmanaged_plugins()
    sort_modlist_like_plugins(profiledir)
    write_modlist(profiledir, modsdir)
    logging.info("ps.do_it done")



#do_it("C:\Program Files (x86)\Steam\steamapps\common\skyrim\Mods", "P:\Mod Organizer\profiles\Survival - Kopie")
