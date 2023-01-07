import pathlib
import os
import glob
import schedule
import time
import pdb
import tkinter as tk
from apscheduler.schedulers.background import BackgroundScheduler


def delete_text():
    return result_text.delete("1.0", "end")


def scheduler_f():
    scheduler = BackgroundScheduler()
    for folder_p in list_folders.values():
        folder_p = folder_p + "/"
        scheduler.add_job(delete_text, 'interval', seconds=5)
        time.sleep(1)
        scheduler.add_job(organise_all, args= (folder_p,), trigger='interval', seconds=5)
        scheduler.start()




def organise_all(folder_path):
    """This function add all types of extension into a list"""
    folder_files = pathlib.Path(folder_path)
    extensions = []
    for file_path in folder_files.rglob("*"):
        if os.path.splitext(file_path)[-1] != "":
            ext = (file_path.suffix).lower()
            if ext not in extensions:
                extensions.append(ext)
    info1 = ("Today your {} folder contains {} files that should be rearranged,\n\nThe file has {} KB of size".
          format(folder_path.split("/")[-2], len(glob.glob(folder_path + "*.*")), os.stat(folder_path).st_size/1000))
    result_text.insert(tk.END, info1)
    print(folder_path)
    print(extensions)
    return organise(extensions, folder_path)


def move_file(file_path, new_folder_path, file_name):
    """This function moves the new downloaded file to the designated folder"""
    return pathlib.Path(file_path).rename(new_folder_path + "/" + file_name)


def organise(extensions, folder_path):
    files_number = 0
    counter = 0
    folder_names = [directory for directory in os.listdir(folder_path) if os.path.isdir(folder_path+directory)]
    #print("This is the folder names: " + str(folder_names))
    for ext_type in extensions:

        all_files_path = glob.glob(folder_path + "*" + ext_type)
        print("all the files with a specific ext: " + str(all_files_path))
        for file_path in all_files_path:
            file_path = str(file_path).replace("\\", "/")
            print("The first file with the exte:" + str(file_path))
            new_folder_name = "Folder_containing_{}_files".format(ext_type[1:])
            print("This is the new folder name" + str(new_folder_name))
            new_folder_path = folder_path + new_folder_name
            file_name = os.path.basename(file_path)
            print("This is the folder names " + str(folder_names))
            print(folder_names)
            folder_names = [directory for directory in os.listdir(folder_path) if
                            os.path.isdir(folder_path + directory)]
            if new_folder_name not in folder_names:
                print("This is the new folder name: " + str(new_folder_name))
                print("This folder name: " + str(new_folder_name))
                print("does not exist in " + str(folder_names))
                new_folder_loc = folder_path
                location = os.path.join(new_folder_loc, new_folder_name)
                print("I create this folder" + str(location))
                os.mkdir(location)
                while os.path.exists(new_folder_path + "/" + file_name) is True:
                    file_name = str(counter) + "_" + file_name
                    counter += 1
                move_file(file_path, new_folder_path, file_name)
                files_number += 1
                print(folder_names)


            if new_folder_name in folder_names:
                print("This code was executed")
                while os.path.exists(new_folder_path + "/" + file_name):
                    file_name = str(counter) + "_" + file_name
                    counter += 1
                move_file(file_path, new_folder_path, file_name)
                files_number += 1
    info2 = ("\n{} files were moved\n".format(files_number))
    result_text.insert(tk.END, info2)


list_folders = {}
def autom_func():
    autom_folder_path = filedialog.askdirectory(initialdir="/", title="Choose a folder")
    autom_folder_name = os.path.basename(autom_folder_path)
    list_folders[autom_folder_name] = autom_folder_path


import tkinter as tk
from tkinter import ttk
from tkinter import *
from tkinter import filedialog

try:
    from ctypes import windll
    windll.shcore.SetProcessDpiAwarness(1)
except:
    pass


root = tk.Tk()
root.geometry("280x280")
root.title("Organise your Folders")
root.iconbitmap("dd.ico")

main = ttk.Frame(root, padding=(30, 15))
main.grid()

m = IntVar()
mode = m.set(0)

def mode(value):
    if value == 1:
        print("manual mode is chosen")
        upload_path["state"] = "normal"
        sheduler_button["state"] = "disabled"
        result_text.delete("1.0", "end")
    if value == 2:
        print("Automatic mode is chosen")
        upload_path["state"] = "disabled"
        sheduler_button["state"] = "normal"
        result_text.delete("1.0", "end")
        autom_func()
        result_text.insert(tk.END, str(list(list_folders.keys())) + "\n")


radio_but_1 = tk.Radiobutton(main, text="Manuel", variable=m, value=1, command=lambda: mode(m.get()))
radio_but_1.grid(row=1, column=3, sticky="W")

radio_but_2 = tk.Radiobutton(main, text="Automatic", variable=m, value=2, command=lambda: mode(m.get()))
radio_but_2.grid(row=2, column=3, sticky="W")


result_text = Text(root, height = 10, width = 34, relief="sunken")
result_text.grid(row=2, column=0)





def upload_file_path():
    main.upload_path = filedialog.askdirectory(initialdir="/", title="Choose a folder") + "/"
    organise_all(main.upload_path)
    info3 = ("\n\nThe chosen folder is: \n {}".format(main.upload_path))
    result_text.insert(tk.END, info3)






upload_path = tk.Button(main, text="Folder Name", height=2,
                        width=12, activebackground="gray", command=upload_file_path)
upload_path.grid(row=1, column=0)

sheduler_button = tk.Button(main, text="Start Scheduler", height=2, width=12, activebackground="gray",
                            command=scheduler_f)
sheduler_button.grid(row=2, column=0)




root.mainloop()