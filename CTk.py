import tkinter
import customtkinter
from customtkinter import *
from tkinter import messagebox
from func import add_new_user
import json
        
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
    entries = []
    
    for i, field in enumerate(fields):
        fields_label_frame = CTkFrame(master = new_user_window, fg_color = '#1f6aa5', corner_radius = 6,
                                      width = 100, height = 27)
        fields_label = CTkLabel(master = fields_label_frame, text = field, bg_color = 'transparent', height = 27,
                                font = ("Arial", 15))
        fields_entry = CTkEntry(master = new_user_window, width = 580, height = 35)
        entries.append(fields_entry)

        fields_label_frame.grid(row = i, column = 0, padx = 4, pady = (4), sticky = 'nsew')
        fields_label_frame.grid_rowconfigure(0, weight = 1)
        fields_label_frame.grid_columnconfigure(0, weight = 1)
        fields_label.grid(padx = 4, pady = 4, sticky = 'nsew')
        fields_entry.grid(row = i, column = 1)
        
    def confirm():
        values = []
        for entry in entries:
            values.append(entry.get())
        user = add_new_user(*values)
        messagebox.showinfo("Success", f"User added successfully\nUser ID: {user['user_id']}")
        new_user_window.destroy()
        
    confirm_btn = CTkButton(master = new_user_window, text = "Confirm", font = ("Arial", 15), width = 100, height = 40, command = confirm)
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
    entries = []
    
    for i, field in enumerate(fields):
        fields_label_frame = CTkFrame(master = find_user_window, fg_color = '#1f6aa5', corner_radius = 6,
                                      width = 100, height = 27)
        fields_label = CTkLabel(master = fields_label_frame, text = field, bg_color = 'transparent', height = 27,
                                font = ("Arial", 15))
        fields_entry = CTkEntry(master = find_user_window, width = 400, height = 35)
        entries.append(fields_entry)
        
        fields_label_frame.grid(row = i, column = 0, padx = 4, pady = (4), sticky = 'nsew')
        fields_label_frame.grid_rowconfigure(0, weight = 1)
        fields_label_frame.grid_columnconfigure(0, weight = 1)
        fields_label.grid(padx = 4, pady = 4, sticky = 'nsew')
        fields_entry.grid(row = i, column = 1)
        
    def confirm():
        global user_name_btn
        users = []
        try:
            with open("./Users.json", "r", encoding="utf-8") as f:
                users = json.load(f)
        except:
            pass
        values = []
        for entry in entries:
            values.append(entry.get())
        found_user = None
        for user in users:
            if(values[0] and user['last_name'] == values[0]) or (values[1] and user['id_number'] == values[1]) or (values[2] and str(user['user_id']) == values[2]):
                found_user = user
                break
        if found_user:
            user_name_btn.configure(text = f"{found_user['first_name']} {found_user['last_name']}")
            messagebox.showinfo("User Found",f"User: {found_user['first_name']} {found_user['last_name']}")
            find_user_window.destroy()
        else:
            messagebox.showwarning("Not Found", "User not found")
                
    confirm_btn = CTkButton(master = find_user_window, text = "Confirm", font = ("Arial", 15), width = 100, height = 40, command = confirm)
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
    center_window(username_window, 850, 550)
    username_window.title("Users Information")
    username_window.lift()
    username_window.grab_set()
    username_window.resizable(False,False)
    
    search_box_label = CTkFrame(master = username_window, border_color = '#1f6aa5', border_width = 2)
    search_box_label.pack(fill = 'x', padx = 10, pady = 10)

    search_box = CTkTextbox(master = search_box_label, font = ("Arial", 15), height = 1)
    search_box.pack(fill = 'x', side = 'left', expand = True, padx = 2, pady = 3)

    search_button = CTkButton(master = search_box_label, text = "Search", width = 12, font = ("Arial", 15))
    search_button.pack(fill = 'x', expand = True, padx = (0,4), pady = 2)
    
    book_list_text_frame = CTkFrame(master = username_window)
    book_list_text_frame.pack(fill = 'both', padx = 10, pady = 10, expand = True)

    book_list_text = CTkTextbox(master = book_list_text_frame, height = 450, border_color = '#1f6aa5', border_width = 2)
    book_list_text.pack(fill = 'both', expand = True)
    
#===========================================
    
def User_list_window():
    userlist_window = CTkToplevel()
    center_window(userlist_window, 900, 800)
    userlist_window.title("Users Information")
    userlist_window.lift()
    userlist_window.grab_set()
    userlist_window.resizable(False,False)
    
    search_box_frame = CTkFrame(master = userlist_window, border_color = '#1f6aa5', border_width = 2)
    search_box_frame.pack(fill = 'x', padx = 10, pady = 10)

    search_box = CTkTextbox(master = search_box_frame, font = ("Arial", 15), height = 1)
    search_box.pack(fill = 'x', side = 'left', expand = True, padx = 2, pady = 3)

    search_button = CTkButton(master = search_box_frame, text = "Search", width = 12, font = ("Arial", 15))
    search_button.pack(fill = 'x', expand = True, padx = (0,4), pady = 2)
    
    users_list_text_frame = CTkFrame(master = userlist_window)
    users_list_text_frame.pack(fill = 'both', padx = 10, pady = 10, expand = True)

    users_list_text = CTkTextbox(master = users_list_text_frame, height = 550, border_color = '#1f6aa5', border_width = 2)
    users_list_text.pack(fill = 'both', expand = True)
    
#===========================================
    
def Add_book_window():
    add_book_window = CTkToplevel()
    center_window(add_book_window, 700, 350)
    add_book_window.title("Users Information")
    add_book_window.lift()
    add_book_window.grab_set()
    add_book_window.resizable(False,False)
    
    fields = ["Book Name", "Author", "Publisher Name", "Publish Date", "Book ID", "Stock", "Category"]
    
    for i,field in enumerate(fields):
        fields_label_frame = CTkFrame(master = add_book_window, fg_color = '#1f6aa5', corner_radius = 6,
                                      width = 100, height = 27)
        fields_label = CTkLabel(master = fields_label_frame, text = field, bg_color = 'transparent', height = 27,
                                font = ("Arial", 15))
        fields_entry = CTkEntry(master = add_book_window, width = 575, height = 35)
        
        fields_label_frame.grid(row = i, column = 0, padx = 4, pady = (4), sticky = 'nsew')
        fields_label_frame.grid_rowconfigure(0, weight = 1)
        fields_label_frame.grid_columnconfigure(0, weight = 1)
        fields_label.grid(padx = 4, pady = 4, sticky = 'nsew')
        fields_entry.grid(row = i, column = 1)
    
    confirm_btn = CTkButton(master = add_book_window, text = "Confirm", font = ("Arial", 15), width = 100, height = 40)
    confirm_btn.place(x = 300, y = 302)
    
    #===========================================
    
def Remove_book_window():
    remove_book_window = CTkToplevel()
    center_window(remove_book_window, 472, 90)
    remove_book_window.title("Users Information")
    remove_book_window.lift()
    remove_book_window.grab_set()
    remove_book_window.resizable(False,False)
    
    book_id_label_frame = CTkFrame(master = remove_book_window, fg_color = '#1f6aa5', corner_radius = 6,
                                      width = 100, height = 27)
    book_id_label = CTkLabel(master = book_id_label_frame, text = "Book ID", bg_color = 'transparent', height = 27,
                                font = ("Arial", 15))
    book_id_entry = CTkEntry(master = remove_book_window, width = 400, height = 35)
    book_id_label_frame.grid(row = 0, column = 0, padx = 4, pady = (4), sticky = 'nsew')
    book_id_label_frame.grid_rowconfigure(0, weight = 1)
    book_id_label_frame.grid_columnconfigure(0, weight = 1)
    book_id_label.grid(padx = 4, pady = 4, sticky = 'nsew')
    book_id_entry.grid(row = 0, column = 1)
    
    confirm_btn = CTkButton(master = remove_book_window, text = "Confirm", font = ("Arial", 15), width = 100, height = 40)
    confirm_btn.place(x = 186, y = 43)

    #===========================================
    
def Day_limitation_window():
    day_limit_window = CTkToplevel()
    center_window(day_limit_window, 472, 200)
    day_limit_window.title("Day Limitation")
    day_limit_window.lift()
    day_limit_window.grab_set()
    day_limit_window.resizable(False,False)

    fields = ["1 Week", "2 Weeks", "3 Weeks", "1 Month", "2 Months", "3 Months", "Unlimited"]
    from customtkinter import StringVar, CTkRadioButton
    selected_limit = StringVar(value=fields[0])

    for col in range(3):
        day_limit_window.grid_columnconfigure(col, weight=1)

    for col, field in enumerate(fields[:3]):
        radio_btn = CTkRadioButton(master=day_limit_window, text=field, variable=selected_limit, value=field)
        radio_btn.grid(row=0, column=col, sticky="ew", padx=35, pady=10)

    for col, field in enumerate(fields[3:6]):
        radio_btn = CTkRadioButton(master=day_limit_window, text=field, variable=selected_limit, value=field)
        radio_btn.grid(row=1, column=col, sticky="ew", padx=35, pady=10)

    radio_btn = CTkRadioButton(master=day_limit_window, text=fields[6], variable=selected_limit, value=fields[6])
    radio_btn.grid(row=2, column=1, sticky="ew", padx=35, pady=10)

    confirm_btn = CTkButton(master=day_limit_window, text="Confirm", font=("Arial", 15), width=120, height=40)
    confirm_btn.grid(row=3, column=0, columnspan=3, pady=(20,10))
    
    
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

user_name_btn = CTkButton(master = borrow_frame, text = "No User", height = 40, font = ("Arial", 15), command = User_name_window)
user_name_btn.pack(fill = 'x', padx = 3, pady = (0,3))

borrow_btn = CTkButton(master = borrow_frame, text = "Borrow Book", height = 40, font = ("Arial", 15), command = Borrow_book_window)
borrow_btn.pack(fill = 'x', padx = 3, pady = (0,3))

return_btn = CTkButton(master = borrow_frame, text = "Return Book", height = 40, font = ("Arial", 15), command = Return_book_window)
return_btn.pack(fill = 'x', padx = 3, pady = (0,3))

users_list_btn = CTkButton(master = borrow_frame, text = "Users List", height = 40, font = ("Arial", 15), command = User_list_window)
users_list_btn.pack(fill = 'x', padx = 3, pady = (0,3))

borrow_status_frame = CTkFrame(master = borrow_frame, corner_radius = 6, fg_color='#1f6aa5')
borrow_status_frame.pack(fill = 'x', padx = 3, pady = (0,3))

borrow_status = CTkLabel(master = borrow_status_frame, text = "Status:\nBorrowed", height = 40, font = ("Arial",15),
                         bg_color = "transparent")
borrow_status.pack()

stock_status_frame = CTkFrame(master = borrow_frame, corner_radius = 6, fg_color='#1f6aa5')
stock_status_frame.pack(fill = 'x', padx = 3, pady = (0,3))

stock_status = CTkLabel(master = stock_status_frame, text = "Stock: 4", height = 40, font = ("Arial",15),
                         bg_color = "transparent")
stock_status.pack()

day_limit_btn = CTkButton(master = borrow_frame, text = "Day Limitation", height = 40, font = ("Arial",15), command = Day_limitation_window)
day_limit_btn.pack(fill = 'x',padx = 3, pady = (0,3))

add_btn = CTkButton(master = borrow_frame, text = "Add Book", height = 40, font = ("Arial",15), command = Add_book_window)
add_btn.pack(fill = 'x',padx = 3, pady = (0,3))

remove_btn = CTkButton(master = borrow_frame, text = "Remove Book", height = 40, font = ("Arial",15), command = Remove_book_window)
remove_btn.pack(fill = 'x', padx = 3, pady = (0,3))

#===========================================

book_list_text_frame = CTkFrame(master = main_window)
book_list_text_frame.pack(fill = 'both', padx = 10, pady = 10, expand = True)

book_list_text = CTkTextbox(master = book_list_text_frame, height = 550, border_color = '#1f6aa5', border_width = 2)
book_list_text.pack(fill = 'both', expand = True)

#===========================================


    




main_window.mainloop()