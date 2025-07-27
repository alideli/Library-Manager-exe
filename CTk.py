import tkinter
import customtkinter
from CTkListbox import CTkListbox
from customtkinter import *
from tkinter import messagebox
from func import add_new_user
from func import update_borrowed_books
import json

selected_user_id = None
selected_borrowed_books = []
        
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
    center_window(new_user_window, 705, 317)
    new_user_window.title("New User")
    new_user_window.lift()
    new_user_window.grab_set()
    new_user_window.resizable(False,False)
    
    
    fields = ["First Name","Last Name", "ID Number", "Phone Number", "Address", "Date Registered"]
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
    center_window(find_user_window, 490, 180)
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
        global user_name_btn, selected_user_id, selected_borrowed_books
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
            if (values[0] and user['last_name'] == values[0]) or (values[1] and user['id_number'] == values[1]) or (values[2] and str(user['user_id']) == values[2]):
                found_user = user
                break
        if found_user:
            user_name_btn.configure(text = f"{found_user['first_name']} {found_user['last_name']}")
            selected_user_id = str(found_user['user_id'])
            selected_borrowed_books = found_user['borrowed_books']
            messagebox.showinfo("User Found",f"User: {found_user['first_name']} {found_user['last_name']}")
            find_user_window.destroy()
        else:
            messagebox.showwarning("Not Found", "User not found")
                
    confirm_btn = CTkButton(master = find_user_window, text = "Confirm", font = ("Arial", 15), width = 100, height = 40, command = confirm)
    confirm_btn.place(x = 195, y = 132)

#===========================================

def Borrow_book_window():
    global selected_user_id, selected_borrowed_books
    borrow_window = messagebox.askyesno(f"Borrow Confirm",f"Are you sure to Borrow Book \"x\" for user \"y\"")
    if(borrow_window):
        book_id = "Book_id_sample"
        selected_borrowed_books.append(book_id)
        update_borrowed_books(selected_user_id, selected_borrowed_books)
        messagebox.showwarning("Confirmed","Book Borrowed")
            
    else:
        messagebox.showwarning("Not Confirmed","Canceled")


def Return_book_window():
    global selected_user_id, selected_borrowed_books
    return_window = messagebox.askyesno("Return Confirm",f"Are you sure to return book \"x\" for user \"y\"")
    if(return_window):
        book_id = "Book_id_sample"
        if book_id in selected_borrowed_books:
            selected_borrowed_books.remove(book_id)
            update_borrowed_books(selected_user_id, selected_borrowed_books)
        messagebox.showwarning("Confirmed","Book Returned")
    else:
        messagebox.showwarning("Not Confirmed","Canceled")
    
#===========================================
    
def User_name_window():
    global selected_user_id
    
    username_window = CTkToplevel()
    center_window(username_window, 712, 345)
    username_window.title("Users Information")
    username_window.lift()
    username_window.grab_set()
    username_window.resizable(False,False)
    
    fields = [
        ("First Name", "first_name"),
        ("Last Name", "last_name"),
        ("ID Number", "id_number"),
        ("Phone Number", "phone_number"),
        ("Address", "address"),
        ("Date Registered", "register_date"),
        ("User_ID", "user_id"),
        ("Borrowed_Books", "borrowed_books")
    ]

    entries = []
    for i, (label_text, _) in enumerate(fields):
        fields_label_frame = CTkFrame(master=username_window, fg_color='#1f6aa5', corner_radius=6, width=100, height=27)
        fields_label = CTkLabel(master=fields_label_frame, text=label_text, bg_color='transparent', height=27, font=("Arial", 15))
        fields_entry = CTkEntry(master=username_window, width=580, height=35)
        entries.append(fields_entry)

        fields_label_frame.grid(row=i, column=0, padx=4, pady=(4), sticky='nsew')
        fields_label_frame.grid_rowconfigure(0, weight=1)
        fields_label_frame.grid_columnconfigure(0, weight=1)
        fields_label.grid(padx=4, pady=4, sticky='nsew')
        fields_entry.grid(row=i, column=1)

    user_info = None
    try:
        with open("./Users.json", "r", encoding="utf-8") as f:
            users = json.load(f)
            for user in users:
                if str(user['user_id']) == str(selected_user_id):
                    user_info = user
                    break
    except Exception as e:
        pass

    if user_info:
        for i, (_, key) in enumerate(fields):
            value = user_info.get(key, "-")
            if key == "borrowed_books" and isinstance(value, list):
                value = ', '.join(str(v) for v in value) if value else '---'
            entries[i].insert(0, str(value))
            entries[i].configure(state='readonly')
    else:
        for entry in entries:
            entry.insert(0, "None")
            entry.configure(state='readonly')
#===========================================
   
def User_list_window2(user):
    userlist_window2 = CTkToplevel()
    center_window(userlist_window2, 712, 420)
    userlist_window2.title("Users Information")
    userlist_window2.lift()
    userlist_window2.grab_set()
    userlist_window2.resizable(False,False)

    fields = [
        ("First Name", "first_name"),
        ("Last Name", "last_name"),
        ("ID Number", "id_number"),
        ("Phone Number", "phone_number"),
        ("Address", "address"),
        ("Date Registered", "register_date"),
        ("User ID", "user_id"),
        ("Borrowed Books", "borrowed_books")
    ]

    for i, (label, key) in enumerate(fields):
        fields_label_frame = CTkFrame(master = userlist_window2, fg_color = '#1f6aa5', corner_radius = 6, width = 100, height = 27)
        fields_label = CTkLabel(master = fields_label_frame, text = label, bg_color = 'transparent', height = 27, font = ("Arial", 15))
        fields_entry = CTkEntry(master = userlist_window2, width = 580, height = 35)
        value = user.get(key, "-")
        if key == "borrowed_books" and isinstance(value, list):
            value = ', '.join(str(v) for v in value) if value else '---'
        fields_entry.insert(0, str(value))
        fields_entry.configure(state='readonly')

        fields_label_frame.grid(row = i, column = 0, padx = 4, pady = (4), sticky = 'nsew')
        fields_label_frame.grid_rowconfigure(0, weight = 1)
        fields_label_frame.grid_columnconfigure(0, weight = 1)
        fields_label.grid(padx = 4, pady = 4, sticky = 'nsew')
        fields_entry.grid(row = i, column = 1)
        
    confirm_btn = CTkButton(master = userlist_window2, text = "Confirm", font = ("Arial", 15), width = 100, height = 40)
    confirm_btn.place(x = 305, y = 350)
    delete_user_btn = CTkButton(master = userlist_window2, text = "Remove User", font = ("Arial", 15), width = 100, height = 40)
    delete_user_btn.place(x = 10, y = 350)
        
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
    
    users_list_box_frame = CTkFrame(master = userlist_window)
    users_list_box_frame.pack(fill = 'both', padx = 10, pady = 10, expand = True)

    users_list_box = CTkListbox(master = users_list_box_frame, height = 550, border_color = '#1f6aa5', border_width = 2)
    users_list_box.pack(fill = 'both', expand = True)

    try:
        with open("./Users.json", "r", encoding="utf-8") as f:
            users = json.load(f)
    except:
        users = []

    current_user_list = users.copy()

    def fill_listbox(user_list):
        users_list_box.delete(0, 'end')
        for user in user_list:
            preview = f"{user.get('first_name','')} {user.get('last_name','')} | ID: {user.get('user_id','')}"
            users_list_box.insert('end', preview)

    fill_listbox(current_user_list)


    def search_users(event=None):
        query = search_box.get("1.0", "end").strip().lower()
        if not query:
            filtered = users
        else:
            filtered = []
            for user in users:
                # Concatenate all user values into a single string for multi-word search
                user_text = ' '.join(str(value) for value in user.values()).lower()
                if query in user_text:
                    filtered.append(user)
        current_user_list.clear()
        current_user_list.extend(filtered)
        fill_listbox(current_user_list)

    search_button.configure(command=search_users)
    search_box.bind("<KeyRelease>", search_users)


    def on_user_double_click(event=None):
        selection = users_list_box.curselection()
        if selection is None or selection == '':
            return
        index = selection
        if 0 <= index < len(current_user_list):
            user = current_user_list[index]
            User_list_window2(user)

    users_list_box.bind('<Double-Button-1>', on_user_double_click)


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