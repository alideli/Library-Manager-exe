import tkinter
import customtkinter
from customtkinter import *
from tkinter import messagebox

        
set_appearance_mode("System")
set_default_color_theme("blue")

def center_window(main, window_width, window_height):
    screen_width = main_window.winfo_screenwidth()
    screen_height = main_window.winfo_screenheight()
    x = int((screen_width - window_width) / 2)
    y = int((screen_height - window_height) / 2)
    main.geometry(f"{window_width}x{window_height}+{x}+{y}")
    
    
main_window = CTk()
main_window.title("Library Management")
center_window(main_window, 900, 600)
main_window.iconbitmap("./icon/Library_icon.ico")

#=====================================

def new_user_btn_window():
    new_user_window = CTkToplevel()
    center_window(new_user_window, 700, 317)
    new_user_window.title("New User")
    new_user_window.lift()
    new_user_window.grab_set()
    new_user_window.resizable(False,False)
    
    
    fields = ["First Name","Last Name", "ID Number", "Phone Number", "Address", "Date"]
    
    for i, field in enumerate(fields):
        fields_label_frame = CTkFrame(master = new_user_window, fg_color = '#1f6aa5', corner_radius = 6,
                                      width = 100, height = 27)
        fields_label = CTkLabel(master = fields_label_frame, text = field, bg_color = 'transparent', height = 27,
                                font = ("Arial", 15))
        fields_entry = CTkEntry(master = new_user_window, width = 580, height = 35)
        
        fields_label_frame.grid(row = i, column = 0, padx = 4, pady = (4), sticky = 'nsew')
        fields_label_frame.grid_rowconfigure(0, weight = 1)
        fields_label_frame.grid_columnconfigure(0, weight = 1)
        fields_label.grid(padx = 4, pady = 4, sticky = 'nsew')
        fields_entry.grid(row = i, column = 1)
    
    confirm_btn = CTkButton(master = new_user_window, text = "Confirm", font = ("Arial", 15), width = 100, height = 40)
    confirm_btn.place(x = 300, y = 265)
    
#===========================================

def find_user_btn_window():
    find_user_window = CTkToplevel()
    center_window(find_user_window, 495, 182)
    find_user_window.title("Find User")
    find_user_window.lift()
    find_user_window.grab_set()
    find_user_window.resizable(False,False)
    
    
    fields = ["Last Name", "ID Number", "User ID"]
    
    for i, field in enumerate(fields):
        fields_label_frame = CTkFrame(master = find_user_window, fg_color = '#1f6aa5', corner_radius = 6,
                                      width = 100, height = 27)
        fields_label = CTkLabel(master = fields_label_frame, text = field, bg_color = 'transparent', height = 27,
                                font = ("Arial", 15))
        fields_entry = CTkEntry(master = find_user_window, width = 400, height = 35)
        
        fields_label_frame.grid(row = i, column = 0, padx = 4, pady = (4), sticky = 'nsew')
        fields_label_frame.grid_rowconfigure(0, weight = 1)
        fields_label_frame.grid_columnconfigure(0, weight = 1)
        fields_label.grid(padx = 4, pady = 4, sticky = 'nsew')
        fields_entry.grid(row = i, column = 1)
    
    confirm_btn = CTkButton(master = find_user_window, text = "Confirm", font = ("Arial", 15), width = 100, height = 40)
    confirm_btn.place(x = 210, y = 132)

#===========================================

def Borrow_book_window():
    borrow_window = messagebox.askyesno("Borrow Confirm",f"Are you sure to Borrow Book \"x\" for user \"y\"")
    if(borrow_window):
        messagebox.showwarning("Confirmed","Book Borrowed")
    else:
        messagebox.showwarning("Not Confirmed","Canceled")


def Return_book_window():
    return_window = messagebox.askyesno("Return Confirm",f"Are you sure to return book \"x\" for user \"y\"")
    if(return_window):
        messagebox.showwarning("Confirmed","Book Returned")
    else:
        messagebox.showwarning("Not Confirmed","Canceled")
    
#===========================================
    
def User_name_window():
    username_window = CTkToplevel()
    center_window(username_window, 900, 800)
    username_window.title("Find User")
    username_window.lift()
    username_window.grab_set()
    username_window.resizable(False,False)
    
#===========================================

search_box_label = CTkFrame(master = main_window, border_color = '#1f6aa5', border_width = 2)
search_box_label.pack(fill = 'x', padx = 10, pady = 10)

search_box = CTkTextbox(master = search_box_label, font = ("Arial", 15), height = 1)
search_box.pack(fill = 'x', side = 'left', expand = True, padx = 2, pady = 3)

search_button = CTkButton(master = search_box_label, text = "Search", width = 12, font = ("Arial", 15))
search_button.pack(fill = 'x', expand = True, padx = (0,4), pady = 2)

#===========================================

borrow_frame = CTkFrame(master = main_window, border_color = '#1f6aa5', border_width = 2)
borrow_frame.pack(fill = 'y', padx = 10, pady = 10, side = 'right')

new_user_btn = CTkButton(master = borrow_frame, text = "New User", height = 40, font = ("Arial",15), command = new_user_btn_window)
new_user_btn.pack(fill = 'x', padx = 3, pady = 3)

find_user_btn = CTkButton(master = borrow_frame, text = "Find User", height = 40, font = ("Arial", 15), command = find_user_btn_window)
find_user_btn.pack(fill = 'x', padx = 3, pady = (0,3))

user_name_btn = CTkButton(master = borrow_frame, text = "username", height = 40, font = ("Arial", 15), command = User_name_window)
user_name_btn.pack(fill = 'x', padx = 3, pady = (0,3))

borrow_btn = CTkButton(master = borrow_frame, text = "Borrow Book", height = 40, font = ("Arial", 15), command = Borrow_book_window)
borrow_btn.pack(fill = 'x', padx = 3, pady = (0,3))

return_btn = CTkButton(master = borrow_frame, text = "Return Book", height = 40, font = ("Arial", 15), command = Return_book_window)
return_btn.pack(fill = 'x', padx = 3, pady = (0,3))

users_list_btn = CTkButton(master = borrow_frame, text = "Users List", height = 40, font = ("Arial", 15))
users_list_btn.pack(fill = 'x', padx = 3, pady = (0,3))

borrow_status_frame = CTkFrame(master = borrow_frame, corner_radius = 6, fg_color='#1f6aa5')
borrow_status_frame.pack(fill = 'x', padx = 3, pady = (0,3))

borrow_status = CTkLabel(master = borrow_status_frame, text = "Status:\nBorrowed", height = 40, font = ("Arial",15),
                         bg_color = "transparent")
borrow_status.pack()

add_btn = CTkButton(master = borrow_frame, text = "Add Book", height = 40, font = ("Arial",15))
add_btn.pack(fill = 'x',padx = 3, pady = (0,3))

remove_btn = CTkButton(master = borrow_frame, text = "Remove Book", height = 40, font = ("Arial",15))
remove_btn.pack(fill = 'x', padx = 3, pady = (0,3))

#===========================================

book_list_text_frame = CTkFrame(master = main_window)
book_list_text_frame.pack(fill = 'both', padx = 10, pady = 10, expand = True)

book_list_text = CTkTextbox(master = book_list_text_frame, height = 550, border_color = '#1f6aa5', border_width = 2)
book_list_text.pack(fill = 'both', expand = True)

#===========================================


    




main_window.mainloop()