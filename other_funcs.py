import subprocess
import tkinter as tk
from tkinter import messagebox
from tkinter import simpledialog

password = ""

def get_users_for_module(module_name,listb, filename = "command_output.txt",command = "modinfo"):
    # Initialize a variable to store the number of users

    # Open the file and read it line by line
    with open(filename, 'r') as file:
        for line in file:
            # Split the line into words using spaces as separators
            words = line.split()

            # Check if the line contains at least 4 words and the module name matches
            if len(words) == 4 and words[0] == module_name:
                splited = words[3].split(",")  # Move this inside the loop
                for index in range(listb.size()):
                    for word in splited:
                        if listb.get(index) == word:
                            # Configure the background color of the matching item to green
                            listb.itemconfig(index, {'bg': 'green'})
                return f"({len(splited)})  {words[3]} "
def get_dep(listb,module_name,command = "modinfo"):
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

          

def on_closing(app):
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
    result = subprocess.run(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, input=passwd)
    if result.returncode != 0:
        messagebox.showerror("Error", result.stderr)
        return False
    else:
        messagebox.showinfo("Info",f"{mod_name} was succesfully inserted.")
        return True



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
        while True:
            line = file.readline()
            if not line:
                break
            columns = line.strip().split('\t')
            
            for column in columns:
                word = ""
                for char in column:
                    if char.isspace() or char == '':
                        if word:
                            gathered_words.append(word)
                        break
                    word += char
                else:
                    if word:
                        gathered_words.append(word)
    return gathered_words                   



def remove_and_shift_columns(filename, column_index = 1):
    lines = []
    
    with open(filename, 'r') as file:
        for line in file:
            columns = line.strip().split('\t')
            if column_index < len(columns):
                del columns[column_index]
            new_line = '\t'.join(columns)
            lines.append(new_line)
    
    with open(filename, 'w') as file:
        for line in lines[1:]:
            file.write(line + '\n')