from other_funcs import *
import tkinter as tk
from tkinter import messagebox
from tkinter import simpledialog

flnm = 'command_output.txt'  

#functions that needs to be in this file in order to prevent some confusion

#insert selected module's information into info text widget
#does insertation of module info and markment of users of selected module
def insert_list(event):
     if event.widget == modules_list:
        #clear selection before
        for item in range(modules_list.size()):
            modules_list.itemconfig(item,{'bg' : "white"})
        #clear info text    
        info_text.delete("1.0", tk.END)
        #get selected item
        selected_index = modules_list.curselection()
        if selected_index:
            #convert to text
            selected_text = modules_list.get(selected_index[0])
            #insert modinfo output of the module to info text  
            info_text.insert(tk.END,modinfo(selected_text))
            users_text.configure(state="normal")
            users_text.delete("1.0",tk.END)
            #insert users to users text and mark users of the module
            users_text.insert(tk.END,f"used by: {get_users_for_module(selected_text,modules_list)}")
            users_text.configure(state="disabled")
            get_dep(modules_list,selected_text)

def update_modules_list():
    modules_list.delete(0, tk.END)  # Clear the current items in the list
    get_modules()
    words = read_modname(flnm)  # Get the updated list of modules
    insert_w(words)  # Insert the updated list into the listbox


def unins():
    selected_index = modules_list.curselection()
    if selected_index:
        selected_text = modules_list.get(selected_index[0])  
        if rmmod(selected_text,password):
            update_modules_list()                  
            messagebox.showinfo("Info",f"{selected_text} was succesfuly uninserted.")

def insrt():
     manuel_mod_name = simpledialog.askstring("Manualy Insert","Enter an module name. Modules are often stored in /lib/modules/(your kernel version)/(file ending with .ko)")
     if manuel_mod_name:
      if modprobe(manuel_mod_name,password):
          update_modules_list()

        
          

def insert_w():
    get_modules()  
    words= read_modname(flnm)
    for word in words:
        modules_list.insert(tk.END, word)


#get root acces by asking password  (if your user is not in sudo/sudoers group, it will not work)
password = get_password()


#window options
window = tk.Tk()
window.resizable(False,False)
window.title("ModSeeker")
window.protocol("WM_DELETE_WINDOW", on_closing(window))

#widgets
modules_list = tk.Listbox(window,height=23)
modules_list.grid(row=0,column=1,padx=5,pady=0,sticky="N",rowspan=20)
modules_list.bind("<<ListboxSelect>>", insert_list)


info_text = tk.Text(window)
info_text.grid(row=0,column=2,padx=5,sticky="N", rowspan=20)


users_text = tk.Text(window,width=30,height=2)
users_text.grid(row=21, column=1, padx=5, pady=0, columnspan=2, rowspan=1, sticky='WE')
users_text.configure(state="disabled")

#insert list into listbox (had to put it in here because modules list was non-existent before)
insert_w()

rmmod_bt = tk.Button(window,text="Uninsert",command=unins,width=4)
rmmod_bt.grid(row=0,column=0,padx=5,sticky="N")
admod_bt = tk.Button(window,text="Insert",command=insrt,width=4)
admod_bt.grid(row=1,column=0,padx=5,sticky="N")
admod_bt1 = tk.Button(window,text="Insert",command=insrt,width=4)
intelliadd = tk.Button(window, text="L. All", command=lambda: get_modules_from_lib(window,info_text,modules_list), width=4)
intelliadd.grid(row=2,column=0,padx=5,sticky="N")

window.columnconfigure(1,weight=20)
window.columnconfigure(2,weight=80)


window.mainloop()