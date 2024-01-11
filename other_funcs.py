import subprocess
import tkinter as tk
from tkinter import messagebox
from tkinter import simpledialog
import os.path as ph


password = ""
comprl = [".zts",".bz2",".gz",".xz","","",""]
islistingall = False

def important():
    messagebox.showwarning("Important","If you don't have any idea about what you are doing, LEAVE the app.")
def list_to_spaced(list):
    a = ""
    for i in list:
        a += i +" "
    return a


#get all modules on the computer 
#note that due to updates, modules stored in the computer might get deleted/renamed or new modules can be added. so, that makes the else statement impractical
def get_modules_from_lib(widget2, command="""find /lib/modules/$(uname -r)/ -type f -name "*.ko*" | xargs -I {} basename {}"""):
    global islistingall 
    result = []
    modules_in_use = []
    if islistingall == False:
        #list used in else statement
        #working directory location
        pwd = subprocess.run("pwd", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True).stdout.split()[0]+ "/"
        #if the file isnt there(because command takes time to complete)
        if ph.exists(pwd + "allmods.txt") == False:
            result = subprocess.run(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True).stdout.splitlines()
            result = sorted(result)
            #write output to file without their ".ko" part
            with open("allmods.txt","w") as file:
                for i in result:
                    word = i.split(".")[0]+"\n"
                    file.write(word)

            #store names of modules that are currently in use
            for i in range(widget2.size()):
                modules_in_use.append(widget2.get(i)) 

            widget2.delete(0, tk.END)
            with open("allmods.txt","r") as file:
             for line in file:
                line = line.split()[0]
                green_flags = [line == module for module in modules_in_use]
                green = any(green_flags)
                if green:
                    widget2.insert(tk.END, line)
                    widget2.itemconfig(tk.END,{'fg':'red'})
                else:
                    widget2.insert(tk.END, line)
            islistingall = True
                
        #if its there
        else:
            #store names of modules that are currently in use
            for i in range(widget2.size()):
                modules_in_use.append(widget2.get(i))
            #read line by line and append to result list and mark
            widget2.delete(0, tk.END)
            with open("allmods.txt","r") as file:
             for line in file:
                line = line.split()[0]
                green_flags = [line == module for module in modules_in_use]
                green = any(green_flags)
                if green:
                    widget2.insert(tk.END, line)
                    widget2.itemconfig(tk.END,{'fg':'red'})
                else:
                    widget2.insert(tk.END, line)
            islistingall = True   

def res():
     global islistingall 
     islistingall = False 

#both returns users of selected module to users_text and marks matched items in the  listbox
def get_users_for_module(module_name,listb, filename = "command_output.txt"):
    # Open the file and read it line by line
    with open(filename, 'r') as file:
        for line in file:
            # Split the line against words using spaces as separators
            words = line.split()

            # Check if the line contains at least 4 words and the module name matches
            if len(words) == 4 and words[0] == module_name:
                splited = words[3].split(",")  # Move this inside the loop
                for index in range(listb.size()):
                    for word in splited:
                        if listb.get(index) == word:
                            # Configure the background color of the matching item to green
                            listb.itemconfig(index, {'bg': 'green'})    
                #return number of users and users of it                              
                return f"Used by: ({len(splited)})  {words[3]} "
    return "Used by: None "               


#both returns depencies of selected module to users_text and marks matched items in the  listbox    
def get_dep(listb,module_name,command = "modinfo"):
    #both returns depencies and inserts the module's info
    result = subprocess.run(command + " " + module_name, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    with open("modinf.txt", 'w') as f:
        f.write(result.stdout)
    with open("modinf.txt", "r") as file:
     for line in file:
        words = line.split()
        if len(words) == 2 and words[0] == "depends:":
            depends_on = words[1].split(",")
            for index in range(listb.size()):
                for word in depends_on:
                    if listb.get(index) == word:
                        # Configure the background color of the matching item to green
                        listb.itemconfig(index, {'bg': 'red3'})
            #return number of depencies and depencies of it 
            return f"Depends: ({len(depends_on)}) {words[1]}"            
    return "Depends: None"              

def on_closing():
    # Run the command before closing the application
    subprocess.run(["sudo", "-k"])
    #app.destroy()

def get_password():
    password = simpledialog.askstring("Password", "Enter your password for root acces:", show='*')
    if password is None:
        password = ""  
        return password

    return password

def rmmod(mod_name,passwd):
    
    command = f"sudo -S rmmod {mod_name}"
    result = subprocess.run(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, input=passwd)
    if result.returncode != 0:
        messagebox.showerror("Error", result.stderr)
        return False
    return True

def modprobe(mod_name,passwd):
    command = f"sudo -S modprobe {mod_name}"    
    print(mod_name)
    print(command)    
    result = subprocess.run(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, input=passwd)
    if result.returncode != 0:
        messagebox.showerror("Error", result.stderr)
        return False
    else:
        if len(mod_name.split()) > 1:
            messagebox.showinfo("Info",f"{mod_name} were succesfully inserted.")
        else:
            messagebox.showinfo("Info",f"{mod_name} was succesfully inserted.")
        return True
def getsize(selected_text,flnm="command_output.txt"):
    with open(flnm,'r') as file:
        for line in file:
            words = line.split()
            if words[0] == selected_text:
                bytes = int(words[1])
                megabytes = round(bytes / (1024* 1024),1)
                return megabytes 

def modinfo(mod_name):
    command = f"modinfo {mod_name}"
    result = subprocess.run(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    return result.stdout

def get_modules():
    command = "lsmod"
    result = subprocess.run(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    
    # Write the command output to a file
    with open("command_output.txt", "w") as file:
       file.write(result.stdout)
       remove_and_shift_columns(filename="command_output.txt")

def read_modname(filename):
    gathered_words = []
    
    with open(filename, 'r') as file:
        for line in file:
            gathered_words.append(line.split()[0])
    return gathered_words     
                  
def remove_and_shift_columns(filename, column_index = 1):
    lines = []
    
    with open(filename,"r") as file:
        for line in file:
            lines.append(line)
    with open(filename,"w") as file:   
        for i in lines[1:]:
            file.write(i)   
