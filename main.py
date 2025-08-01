import tkinter
import customtkinter
from CTkListbox import CTkListbox
from customtkinter import *
from tkinter import messagebox
import json

import ast
import datetime
from data_manager import add_new_user, update_borrowed_books, add_new_book
from utils import center_window, get_book_name

selected_user_id = None
selected_borrowed_books = []
selected_book_id = None
is_admin_logged_in = False
        
set_appearance_mode("System")
set_default_color_theme("blue")

main_window = CTk()
main_window.title("Library Management")
center_window(main_window, 900, 638)
main_window.iconbitmap("./icon/Library_icon.ico")


#=====================================

def new_user_btn_window():
    new_user_window = CTkToplevel()
    center_window(new_user_window, 705, 317)
    new_user_window.title("New User")
    new_user_window.lift()
    new_user_window.grab_set()
    new_user_window.resizable(False,False)
    
    import datetime
    fields = ["First Name","Last Name", "ID Number", "Phone Number", "Address", "Date Registered"]
    entries = []
    now_str = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    for i, field in enumerate(fields):
        fields_label_frame = CTkFrame(master = new_user_window, fg_color = '#1f6aa5', corner_radius = 6,
                                      width = 100, height = 27)
        fields_label = CTkLabel(master = fields_label_frame, text = field, bg_color = 'transparent', height = 27,
                                font = ("Arial", 15))
        fields_entry = CTkEntry(master = new_user_window, width = 580, height = 35)
        if field == "Date Registered":
            fields_entry.insert(0, now_str)
            fields_entry.configure(state='readonly')
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
        for i, field in enumerate(fields):
            if field != "Date Registered" and (not values[i] or str(values[i]).strip() == ""):
                messagebox.showerror("Error", f"Field '{field}' is required.")
                return
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
            pass
                
    confirm_btn = CTkButton(master = find_user_window, text = "Confirm", font = ("Arial", 15), width = 100, height = 40, command = confirm)
    confirm_btn.place(x = 195, y = 132)

#===========================================

def Borrow_book_window():
    global selected_user_id, selected_borrowed_books, selected_book_id

    if day_limit_btn.cget("text") == "Day Limitation":
        messagebox.showwarning("Error", "Please set the day limitation before borrowing a book.")
        return
    if selected_book_id is None:
        messagebox.showwarning("Error", "No book selected.")
        return

    book_name = "-"
    first_name = "-"
    last_name = "-"
    book_stock = None
    try:
        with open("./Books.json", "r", encoding="utf-8") as f:
            books = json.load(f)
        for book in books:
            if str(book.get('book_id')) == str(selected_book_id):
                book_name = book.get('book_name', '-')
                try:
                    book_stock = int(book.get('stock', 0))
                except Exception:
                    book_stock = 0
                break
    except Exception:
        pass

    if book_stock is not None and book_stock <= 0:
        messagebox.showerror("Error", "Stock is 0 and can't borrow")
        return

    already_borrowed = False
    if selected_borrowed_books:
        for b in selected_borrowed_books:
            if isinstance(b, dict):
                if str(b.get("book_id")) == str(selected_book_id):
                    already_borrowed = True
                    break
            else:
                if str(b) == str(selected_book_id):
                    already_borrowed = True
                    break
    if already_borrowed:
        if first_name == "-" or last_name == "-":
            try:
                with open("./Users.json", "r", encoding="utf-8") as f:
                    users = json.load(f)
                for user in users:
                    if str(user.get('user_id')) == str(selected_user_id):
                        first_name = user.get('first_name', '-')
                        last_name = user.get('last_name', '-')
                        break
            except Exception:
                pass
        messagebox.showerror("Error", f"This book is already borrowed by user: {first_name} {last_name}")
        return

    try:
        with open("./Users.json", "r", encoding="utf-8") as f:
            users = json.load(f)
        for user in users:
            if str(user.get('user_id')) == str(selected_user_id):
                first_name = user.get('first_name', '-')
                last_name = user.get('last_name', '-')
                break
    except Exception:
        pass

    borrow_window = messagebox.askyesno(
        "Borrow Confirm",
        f"Are you sure to Borrow Book '{book_name}' for user {first_name} {last_name}?"
    )
    if borrow_window:
        book_id = selected_book_id
        try:
            with open("./Books.json", "r", encoding="utf-8") as f:
                books = json.load(f)
        except Exception:
            books = []
        book_found = False
        for book in books:
            if str(book.get('book_id')) == str(book_id):
                try:
                    stock = int(book.get('stock', 0))
                except Exception:
                    stock = 0
                if stock > 0:
                    book['stock'] = stock - 1
                    stock_status.configure(text=f"Stock: {book['stock']}")
                    book_found = True
                else:
                    messagebox.showwarning("Error", "No stock available for this book.")
                    return
        if book_found:
            with open("./Books.json", "w", encoding="utf-8") as f:
                json.dump(books, f, ensure_ascii=False, indent=2)
        import datetime
        now_str = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        day_limit_value = day_limit_btn.cget('text').replace('Day Limit: ', '').strip()
        if selected_borrowed_books and isinstance(selected_borrowed_books[0], dict):
            selected_borrowed_books.append({"book_id": book_id, "borrow_date": now_str, "day_limit": day_limit_value})
        else:
            selected_borrowed_books = [b if isinstance(b, dict) else {"book_id": b, "borrow_date": now_str, "day_limit": day_limit_value} for b in selected_borrowed_books]
            selected_borrowed_books.append({"book_id": book_id, "borrow_date": now_str, "day_limit": day_limit_value})
        update_borrowed_books(selected_user_id, selected_borrowed_books)
        messagebox.showinfo("Confirmed", "Book Borrowed")
    else:
        pass


def Return_book_window():
    global selected_user_id, selected_borrowed_books, selected_book_id
    if not selected_user_id:
        messagebox.showwarning("Error", "Please select a user first using 'Find User'.")
        return
    if selected_book_id is None:
        messagebox.showwarning("Error", "No book selected.")
        return
    return_window = messagebox.askyesno("Return Confirm", f"Are you sure to return book for user?")
    if return_window:
        book_id = selected_book_id
        removed = False
        if selected_borrowed_books and isinstance(selected_borrowed_books[0], dict):
            for b in selected_borrowed_books:
                if str(b.get("book_id")) == str(book_id):
                    selected_borrowed_books.remove(b)
                    removed = True
                    break
        else:
            if book_id in selected_borrowed_books:
                selected_borrowed_books.remove(book_id)
                removed = True
        if removed:
            update_borrowed_books(selected_user_id, selected_borrowed_books)
            messagebox.showinfo("Confirmed", "Book Returned")
        else:
            messagebox.showwarning("Error", "Selected book is not in the borrowed list.")
    else:
        pass
    
#===========================================
    
def User_name_window():
    global selected_user_id
    
    username_window = CTkToplevel()
    center_window(username_window, 712, 486)
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
    for i, (label_text, key) in enumerate(fields):
        fields_label_frame = CTkFrame(master=username_window, fg_color='#1f6aa5', corner_radius=6, width=100, height=27)
        fields_label = CTkLabel(master=fields_label_frame, text=label_text, bg_color='transparent', height=27, font=("Arial", 15))
        if key == "borrowed_books":
            fields_entry = CTkTextbox(master=username_window, width=580, height=180)
        else:
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
        try:
            with open("./Books.json", "r", encoding="utf-8") as f:
                books = json.load(f)
        except Exception:
            books = []


        user_day_limit = None
        if 'day_limit' in user_info:
            user_day_limit = user_info['day_limit']
        elif hasattr(globals().get('day_limit_btn', None), 'cget'):
            user_day_limit = day_limit_btn.cget('text').replace('Day Limit: ', '')
        for i, (_, key) in enumerate(fields):
            value = user_info.get(key, "-")
            if key == "borrowed_books":
                if value is None or value == '' or value == '-':
                    value = []
                elif isinstance(value, str):
                    try:
                        import ast
                        value = ast.literal_eval(value)
                        if not isinstance(value, list):
                            value = [value]
                    except Exception:
                        value = [value]
                import datetime
                display_lines = []
                if isinstance(value, list) and value:
                    for v in value:
                        if isinstance(v, dict):
                            book_id = v.get("book_id", "-")
                            borrow_date = v.get("borrow_date", "-")
                            day_limit = v.get("day_limit", user_day_limit if user_day_limit else '-')
                            days_left = '-'
                            if borrow_date != '-' and day_limit != '-' and day_limit.lower() != 'unlimited':
                                try:
                                    dt_borrow = datetime.datetime.strptime(borrow_date, "%Y-%m-%d %H:%M:%S")
                                    limit_days = int(day_limit.split()[0])
                                    delta = (dt_borrow + datetime.timedelta(days=limit_days)) - datetime.datetime.now()
                                    days_left = max(delta.days, 0)
                                except Exception:
                                    days_left = '-'
                            elif day_limit.lower() == 'unlimited':
                                days_left = 'Unlimited'
                            display_lines.append(f"{get_book_name(book_id)} (ID:{book_id})\nBorrowed: {borrow_date}\nLimit: {day_limit}\nDays left: {days_left}\n-------------------")
                        else:
                            display_lines.append(f"{get_book_name(v)} (ID:{v})\n-\n-\n-\n-------------------")
                    value = '\n'.join(display_lines)
                else:
                    value = '---'
                entries[i].insert("1.0", str(value))
                entries[i].configure(state='disabled')
            else:
                entries[i].insert(0, str(value))
                entries[i].configure(state='readonly')
    else:
        for i, entry in enumerate(entries):
            if fields[i][1] == "borrowed_books":
                entry.insert("1.0", "None")
                entry.configure(state='disabled')
            else:
                entry.insert(0, "None")
                entry.configure(state='readonly')
#===========================================
   
def User_list_window2(user, refresh_callback=None):
    userlist_window2 = CTkToplevel()
    center_window(userlist_window2, 712, 533)
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

    try:
        with open("./Books.json", "r", encoding="utf-8") as f:
            books = json.load(f)
    except Exception:
        books = []


    user_day_limit = None
    if 'day_limit' in user:
        user_day_limit = user['day_limit']

    entries = []
    for i, (label, key) in enumerate(fields):
        fields_label_frame = CTkFrame(master = userlist_window2, fg_color = '#1f6aa5', corner_radius = 6, width = 100, height = 27)
        fields_label = CTkLabel(master = fields_label_frame, text = label, bg_color = 'transparent', height = 27, font = ("Arial", 15))
        if key == "borrowed_books":
            fields_entry = CTkTextbox(master = userlist_window2, width = 580, height = 180)
        else:
            fields_entry = CTkEntry(master = userlist_window2, width = 580, height = 35)
        value = user.get(key, "-")
        if key == "borrowed_books":
            if value is None or value == '' or value == '-':
                value = []
            elif isinstance(value, str):
                try:
                    value = ast.literal_eval(value)
                    if not isinstance(value, list):
                        value = [value]
                except Exception:
                    value = [value]
            display_lines = []
            if isinstance(value, list) and value:
                for v in value:
                    if isinstance(v, dict):
                        book_id = v.get("book_id", "-")
                        borrow_date = v.get("borrow_date", "-")
                        day_limit = v.get("day_limit", user_day_limit if user_day_limit else '-')
                        days_left = '-'
                        if borrow_date != '-' and day_limit != '-' and day_limit.lower() != 'unlimited':
                            try:
                                dt_borrow = datetime.datetime.strptime(borrow_date, "%Y-%m-%d %H:%M:%S")
                                limit_days = int(day_limit.split()[0])
                                delta = (dt_borrow + datetime.timedelta(days=limit_days)) - datetime.datetime.now()
                                days_left = max(delta.days, 0)
                            except Exception:
                                days_left = '-'
                        elif day_limit.lower() == 'unlimited':
                            days_left = 'Unlimited'
                        display_lines.append(f"Book Name:{get_book_name(book_id)} (ID:{book_id})\nBorrowed: {borrow_date}\nLimit: {day_limit}\nDays left: {days_left}\n-------------------")
                    else:
                        display_lines.append(f"{get_book_name(v)} (ID:{v})\n-\n-\n-\n-------------------")
                value = '\n'.join(display_lines)
            else:
                value = '---'
            fields_entry.insert("1.0", str(value))
            fields_entry.configure(state='disabled')
        else:
            fields_entry.insert(0, str(value))
            fields_entry.configure(state='readonly')

        fields_label_frame.grid(row = i, column = 0, padx = 4, pady = (4), sticky = 'nsew')
        fields_label_frame.grid_rowconfigure(0, weight = 1)
        fields_label_frame.grid_columnconfigure(0, weight = 1)
        fields_label.grid(padx = 4, pady = 4, sticky = 'nsew')
        if key == "borrowed_books":
            fields_entry.grid(row = i, column = 1, sticky='w')
        else:
            fields_entry.grid(row = i, column = 1)
        entries.append(fields_entry)

    editable_keys = ["first_name", "last_name", "id_number", "phone_number", "address"]
    entry_widgets = {}
    for i, (label, key) in enumerate(fields):
        entry_widgets[key] = entries[i]

    def set_editable(state=True):
        for key in editable_keys:
            widget = entry_widgets.get(key)
            if widget:
                if state:
                    widget.configure(state="normal")
                else:
                    widget.configure(state="readonly")

    def confirm_edit():
        new_data = {}
        for key in editable_keys:
            widget = entry_widgets.get(key)
            if widget:
                new_data[key] = widget.get().strip()
        user_id = user.get('user_id', None)
        if user_id is None:
            messagebox.showwarning("Error", "User ID not found.")
            return
        try:
            with open("./Users.json", "r", encoding="utf-8") as f:
                users = json.load(f)
        except Exception:
            users = []
        updated = False
        for u in users:
            if str(u.get('user_id')) == str(user_id):
                for k, v in new_data.items():
                    u[k] = v
                updated = True
                break
        if updated:
            try:
                with open("./Users.json", "w", encoding="utf-8") as f:
                    json.dump(users, f, ensure_ascii=False, indent=2)
            except Exception as e:
                messagebox.showwarning("Error", f"Could not update user.\n{e}")
                return
            messagebox.showinfo("Success", "User information updated.")
            set_editable(False)
            if refresh_callback:
                refresh_callback()
        else:
            messagebox.showwarning("Error", "User not found in file.")

    confirm_btn = CTkButton(master=userlist_window2, text="Confirm", font=("Arial", 15), width=100, height=40, command=confirm_edit)
    confirm_btn.place(x=305, y=485)

    def remove_user_action():
        answer = messagebox.askyesno("Confirm Remove", f"Are you sure you want to remove this user?\n\nName: {user.get('first_name','-')} {user.get('last_name','-')}\nID: {user.get('user_id','-')}")
        if answer:
            try:
                with open("./Users.json", "r", encoding="utf-8") as f:
                    users = json.load(f)
            except Exception:
                users = []
            user_id = user.get('user_id', None)
            if user_id is not None:
                users = [u for u in users if str(u.get('user_id')) != str(user_id)]
                try:
                    with open("./Users.json", "w", encoding="utf-8") as f:
                        json.dump(users, f, ensure_ascii=False, indent=2)
                except Exception as e:
                    messagebox.showwarning("Error", f"Could not remove user from file.\n{e}")
                    return
                messagebox.showinfo("Success", "User removed successfully.")
                userlist_window2.destroy()
                if refresh_callback:
                    refresh_callback()
            else:
                messagebox.showwarning("Error", "User ID not found.")

    remove_user_btn = CTkButton(master=userlist_window2, text="Remove User", font=("Arial", 15), width=100, height=40, command=remove_user_action)
    remove_user_btn.place(x=5, y=485)

    def edit_user_action():
        set_editable(True)

    edit_user_btn = CTkButton(master=userlist_window2, text="Edit User", font=("Arial", 15), width=100, height=40, command=edit_user_action)
    edit_user_btn.place(x=603, y=485)
        
#===========================================   

def User_list_window():
    userlist_window = CTkToplevel()
    center_window(userlist_window, 712, 486)
    userlist_window.title("Users Information")
    userlist_window.lift()
    userlist_window.grab_set()
    userlist_window.resizable(False,False)
    
    search_box_frame = CTkFrame(master = userlist_window, border_color = '#1f6aa5', border_width = 2)
    search_box_frame.pack(fill = 'x', padx = 10, pady = 10)

    search_box = CTkEntry(master = search_box_frame, font = ("Arial", 15), height = 1)
    search_box.pack(fill = 'x', side = 'left', expand = True, padx = 2, pady = 3)

    
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
        users_list_box.delete(0, users_list_box.size())
        for user in user_list:
            preview = f"{user.get('first_name','')} {user.get('last_name','')} | ID: {user.get('user_id','')}"
            users_list_box.insert(users_list_box.size(), preview)

    fill_listbox(current_user_list)


    def search_users(event=None):
        query = search_box.get().strip().lower()
        if not query:
            filtered = users
        else:
            filtered = []
            for user in users:
                user_text = ' '.join(str(value) for value in user.values()).lower()
                if query in user_text:
                    filtered.append(user)
        current_user_list.clear()
        current_user_list.extend(filtered)
        fill_listbox(current_user_list)

    search_box.bind("<KeyRelease>", search_users)


    def refresh_user_list():
        nonlocal users, current_user_list
        try:
            with open("./Users.json", "r", encoding="utf-8") as f:
                users = json.load(f)
        except:
            users = []
        current_user_list.clear()
        current_user_list.extend(users)
        fill_listbox(current_user_list)

    def on_user_double_click(event=None):
        selection = users_list_box.curselection()
        if selection is None or selection == '':
            return
        index = selection
        if 0 <= index < len(current_user_list):
            user = current_user_list[index]
            User_list_window2(user, refresh_callback=refresh_user_list)

    users_list_box.bind('<Double-Button-1>', on_user_double_click)


#===========================================

def Add_book_window():
    add_book_window = CTkToplevel()
    center_window(add_book_window, 700, 303)
    add_book_window.title("Add Book")
    add_book_window.lift()
    add_book_window.grab_set()
    add_book_window.resizable(False,False)
    
    fields = ["Book Name", "Author", "Publisher Name", "Publish Date", "Stock", "Category"]
    entries = []
    
    for i,field in enumerate(fields):
        fields_label_frame = CTkFrame(master = add_book_window, fg_color = '#1f6aa5', corner_radius = 6,
                                      width = 100, height = 27)
        fields_label = CTkLabel(master = fields_label_frame, text = field, bg_color = 'transparent', height = 27,
                                font = ("Arial", 15))
        fields_entry = CTkEntry(master = add_book_window, width = 575, height = 35)
        entries.append(fields_entry)
        
        fields_label_frame.grid(row = i, column = 0, padx = 4, pady = (4), sticky = 'nsew')
        fields_label_frame.grid_rowconfigure(0, weight = 1)
        fields_label_frame.grid_columnconfigure(0, weight = 1)
        fields_label.grid(padx = 4, pady = 4, sticky = 'nsew')
        fields_entry.grid(row = i, column = 1)
    
    def confirm():
        values = [entry.get() for entry in entries]
        for i, field in enumerate(fields):
            if not values[i] or str(values[i]).strip() == "":
                messagebox.showerror("Error", f"Field '{field}' is required.")
                return
        stock_index = 4  # index of Stock in fields
        if len(values) > stock_index and (values[stock_index] is None or str(values[stock_index]).strip() == ""):
            values[stock_index] = "1"
        book = add_new_book(*values)
        messagebox.showinfo("Success", f"Book added!\nBook ID: {book['book_id']}")
        add_book_window.destroy()
        fill_book_list_box()

    confirm_btn = CTkButton(master=add_book_window, text="Confirm", font=("Arial", 15), width=100, height=40, command=confirm)
    confirm_btn.place(x=300, y=258)
    
    #===========================================
    
def Remove_book_window():
    remove_book_window = CTkToplevel()
    center_window(remove_book_window, 472, 90)
    remove_book_window.title("Remove Book")
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
    
    def confirm():
        from data_manager import remove_book_by_id, get_book_by_id
        book_id = book_id_entry.get().strip()
        if not book_id:
            messagebox.showwarning("Error", "Please enter a Book ID.")
            return
        book = get_book_by_id(book_id)
        if not book:
            messagebox.showwarning("Not Found", f"Book with ID {book_id} not found.")
            return
        book_name = book.get('book_name', '-')
        answer = messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete this book?\n\nName: {book_name}\nID: {book_id}")
        if answer:
            removed = remove_book_by_id(book_id)
            if removed:
                messagebox.showinfo("Success", f"Book with ID {book_id} removed.")
                remove_book_window.destroy()
                fill_book_list_box()
            else:
                messagebox.showwarning("Error", f"Book with ID {book_id} could not be removed.")
                
    confirm_btn = CTkButton(master = remove_book_window, text = "Confirm", font = ("Arial", 15), width = 100, height = 40, command=confirm)
    confirm_btn.place(x = 186, y = 43)

    #===========================================
    
def Day_limitation_window():
    global day_limit_btn
    day_limit_window = CTkToplevel()
    center_window(day_limit_window, 472, 200)
    day_limit_window.title("Day Limitation")
    day_limit_window.lift()
    day_limit_window.grab_set()
    day_limit_window.resizable(False,False)

    fields = ["7 Days", "14 Days", "21 Days", "30 Days", "60 Days", "90 Days", "Unlimited"]
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

    def confirm():
        value = selected_limit.get()
        if day_limit_btn is not None:
            day_limit_btn.configure(text=f"Day Limit: {value}")
        day_limit_window.destroy()

    confirm_btn = CTkButton(master=day_limit_window, text="Confirm", font=("Arial", 15), width=120, height=40, command=confirm)
    confirm_btn.grid(row=3, column=0, columnspan=3, pady=(20,10))
    
#======================================

def login():
    global day_limit_btn, is_admin_logged_in, login_btn, add_op
    login_window = CTkToplevel()
    center_window(login_window, 472, 138)
    login_window.title("Admin Login")
    login_window.lift()
    login_window.grab_set()
    login_window.resizable(False,False)

    fields = ["Username","Password"]
    entries = []
    for i,field in enumerate(fields):
        fields_label_frame = CTkFrame(master = login_window, fg_color = '#1f6aa5', corner_radius = 6,
                                      width = 100, height = 27)
        fields_label = CTkLabel(master = fields_label_frame, text = field, bg_color = 'transparent', height = 27,
                                font = ("Arial", 15))
        fields_entry = CTkEntry(master = login_window, width = 385, height = 35, show='*' if field=="Password" else None)
        entries.append(fields_entry)
        fields_label_frame.grid(row = i, column = 0, padx = 4, pady = (4), sticky = 'nsew')
        fields_label_frame.grid_rowconfigure(0, weight = 1)
        fields_label_frame.grid_columnconfigure(0, weight = 1)
        fields_label.grid(padx = 4, pady = 4, sticky = 'nsew')
        fields_entry.grid(row = i, column = 1)

    def confirm():
        global is_admin_logged_in
        username = entries[0].get().strip()
        password = entries[1].get().strip()
        # Admin credentials (hardcoded for now)
        admin_username = "admin"
        admin_password = "admin123"
        if username == admin_username and password == admin_password:
            is_admin_logged_in = True
            login_btn.configure(text="Admin")
            add_op.configure(state="normal")
            op_list_btn.configure(state="normal")
            messagebox.showinfo("Success", "Admin logged in successfully.")
            login_window.destroy()
            return
        import os, json
        op_file = os.path.join(os.path.dirname(__file__), 'Operators.json')
        try:
            with open(op_file, "r", encoding="utf-8") as f:
                ops = json.load(f)
        except Exception:
            ops = []
        found_op = None
        for op in ops:
            if op.get("Username", "") == username and op.get("Password", "") == password:
                found_op = op
                break
        if found_op:
            is_admin_logged_in = False  # Not admin, but operator
            full_name = f"{found_op.get('First Name','')} {found_op.get('Last Name','')}"
            login_btn.configure(text=full_name)
            add_op.configure(state="disabled")
            op_list_btn.configure(state="disabled")
            messagebox.showinfo("Success", f"Operator logged in: {full_name}")
            login_window.destroy()
        else:
            messagebox.showerror("Error", "Invalid credentials.")

    confirm_btn = CTkButton(master = login_window, text = "Confirm", font = ("Arial", 15), width = 120, height=40, command=confirm)
    confirm_btn.grid(row=3, column=0, columnspan=3, pady=(3))
    
#=====================================

def add_operator():
    global day_limit_btn, is_admin_logged_in
    if not is_admin_logged_in:
        messagebox.showwarning("Access Denied", "Only admin can add a new operator. Please login as admin.")
        return
    from data_manager import get_next_operator_id, add_new_operator
    add_op_window = CTkToplevel()
    center_window(add_op_window, 550, 223)
    add_op_window.title("Add Operator")
    add_op_window.lift()
    add_op_window.grab_set()
    add_op_window.resizable(False,False)

    fields = ["First Name","Last Name","Username","Password"]
    entries = []
    for i, field in enumerate(fields):
        fields_label_frame = CTkFrame(master=add_op_window, fg_color='#1f6aa5', corner_radius=6, width=100, height=27)
        fields_label = CTkLabel(master=fields_label_frame, text=field, bg_color='transparent', height=27, font=("Arial", 15))
        fields_entry = CTkEntry(master=add_op_window, width=460, height=35)
        entries.append(fields_entry)
        fields_label_frame.grid(row=i, column=0, padx=4, pady=(4), sticky='nsew')
        fields_label_frame.grid_rowconfigure(0, weight=1)
        fields_label_frame.grid_columnconfigure(0, weight=1)
        fields_label.grid(padx=4, pady=4, sticky='nsew')
        fields_entry.grid(row=i, column=1)

    def confirm():
        values = [entry.get() for entry in entries]
        for i, field in enumerate(fields):
            if not values[i] or str(values[i]).strip() == "":
                messagebox.showerror("Error", f"Field '{field}' is required.")
                return
        try:
            operator_id = get_next_operator_id()
            operator = add_new_operator(values[0], values[1], operator_id, values[2], values[3])
        except ValueError as e:
            messagebox.showerror("Error", str(e))
            return
        messagebox.showinfo("Success", f"Operator added successfully\nOperator ID: {operator['Operator ID']}")
        add_op_window.destroy()

    confirm_btn = CTkButton(master=add_op_window, text="Confirm", font=("Arial", 15), width=120, height=40, command=confirm)
    confirm_btn.grid(row=len(fields), column=0, columnspan=3, pady=(3))
    
#====================================

def operator_list():
    from data_manager import get_all_operators
    op_list_window = CTkToplevel()
    center_window(op_list_window, 712, 533)
    op_list_window.title("Operators List")
    op_list_window.lift()
    op_list_window.grab_set()
    op_list_window.resizable(False,False)

    search_box_label = CTkFrame(master=op_list_window, border_color='#1f6aa5', border_width=2)
    search_box_label.pack(fill='x', padx=10, pady=10)

    search_box = CTkEntry(master=search_box_label, font=("Arial", 15), height=1)
    search_box.pack(fill='x', side='left', expand=True, padx=2, pady=3)

    op_list_box_frame = CTkFrame(master=op_list_window)
    op_list_box_frame.pack(fill='both', padx=10, pady=10, expand=True)

    op_list_box = CTkListbox(master=op_list_box_frame, height=550, border_color='#1f6aa5', border_width=2)
    op_list_box.pack(fill='both', expand=True)

    try:
        operators = get_all_operators()
    except Exception:
        operators = []
    current_op_list = operators.copy()

    def fill_listbox(op_list):
        op_list_box.delete(0, op_list_box.size())
        for op in op_list:
            preview = f"{op.get('First Name','')} {op.get('Last Name','')} | ID: {op.get('Operator ID','')} | Username: {op.get('Username','')}"
            op_list_box.insert(op_list_box.size(), preview)

    fill_listbox(current_op_list)

    def search_ops(event=None):
        query = search_box.get().strip().lower()
        if not query:
            filtered = operators
        else:
            filtered = []
            for op in operators:
                op_text = ' '.join(str(value) for value in op.values()).lower()
                if query in op_text:
                    filtered.append(op)
        current_op_list.clear()
        current_op_list.extend(filtered)
        fill_listbox(current_op_list)

    search_box.bind("<KeyRelease>", search_ops)

    def refresh_op_list():
        nonlocal operators, current_op_list
        try:
            operators = get_all_operators()
        except Exception:
            operators = []
        current_op_list.clear()
        current_op_list.extend(operators)
        fill_listbox(current_op_list)

    def on_op_double_click(event=None):
        selection = op_list_box.curselection()
        if selection is None or selection == '':
            return
        index = selection
        if 0 <= index < len(current_op_list):
            op = current_op_list[index]
            operator_info_window(op)

    op_list_box.bind('<Double-Button-1>', on_op_double_click)

#===================================
def operator_info_window(operator):
    op_info_window = CTkToplevel()
    center_window(op_info_window, 500, 265)
    op_info_window.title("Operators Information")
    op_info_window.lift()
    op_info_window.grab_set()
    op_info_window.resizable(False,False)

    import os
    import json
    fields = [
        ("First Name", "First Name"),
        ("Last Name", "Last Name"),
        ("Operator ID", "Operator ID"),
        ("Username", "Username"),
        ("Password", "Password")
    ]
    entries = []
    for i, (label, key) in enumerate(fields):
        fields_label_frame = CTkFrame(master=op_info_window, fg_color='#1f6aa5', corner_radius=6, width=100, height=27)
        fields_label = CTkLabel(master=fields_label_frame, text=label, bg_color='transparent', height=27, font=("Arial", 15))
        fields_entry = CTkEntry(master=op_info_window, width=405, height=35)
        value = operator.get(key, "-")
        fields_entry.insert(0, str(value))
        if key == "Operator ID":
            fields_entry.configure(state='readonly')
        else:
            fields_entry.configure(state='readonly')
        fields_label_frame.grid(row=i, column=0, padx=4, pady=4, sticky='nsew')
        fields_label_frame.grid_rowconfigure(0, weight=1)
        fields_label_frame.grid_columnconfigure(0, weight=1)
        fields_label.grid(padx=4, pady=4, sticky='nsew')
        fields_entry.grid(row=i, column=1)
        entries.append(fields_entry)

    editable_keys = ["First Name", "Last Name", "Username", "Password"]
    entry_widgets = {key: entries[i] for i, (_, key) in enumerate(fields)}

    def set_editable(state=True):
        for key in editable_keys:
            widget = entry_widgets.get(key)
            if widget:
                if state:
                    widget.configure(state="normal")
                else:
                    widget.configure(state="readonly")

    def confirm_edit():
        new_data = {}
        for key in editable_keys:
            widget = entry_widgets.get(key)
            if widget:
                new_data[key] = widget.get().strip()
        operator_id = operator.get('Operator ID', None)
        if operator_id is None:
            messagebox.showwarning("Error", "Operator ID not found.")
            return
        op_file = os.path.join(os.path.dirname(__file__), 'Operators.json')
        if not os.path.exists(op_file):
            messagebox.showwarning("Error", "Operators file not found.")
            return
        try:
            with open(op_file, "r", encoding="utf-8") as f:
                ops = json.load(f)
        except Exception:
            ops = []
        updated = False
        for op in ops:
            if str(op.get('Operator ID')) == str(operator_id):
                for k, v in new_data.items():
                    op[k] = v
                updated = True
                break
        if updated:
            try:
                with open(op_file, "w", encoding="utf-8") as f:
                    json.dump(ops, f, ensure_ascii=False, indent=2)
            except Exception as e:
                messagebox.showwarning("Error", f"Could not update operator.\n{e}")
                return
            messagebox.showinfo("Success", "Operator information updated.")
            set_editable(False)
        else:
            messagebox.showwarning("Error", "Operator not found in file.")

    def remove_operator_action():
        answer = messagebox.askyesno("Confirm Remove", f"Are you sure you want to remove this operator?\n\nName: {operator.get('First Name','-')} {operator.get('Last Name','-')}\nID: {operator.get('Operator ID','-')}")
        if answer:
            op_file = os.path.join(os.path.dirname(__file__), 'Operators.json')
            if not os.path.exists(op_file):
                messagebox.showwarning("Error", "Operators file not found.")
                return
            try:
                with open(op_file, "r", encoding="utf-8") as f:
                    ops = json.load(f)
            except Exception:
                ops = []
            operator_id = operator.get('Operator ID', None)
            if operator_id is not None:
                ops = [op for op in ops if str(op.get('Operator ID')) != str(operator_id)]
                try:
                    with open(op_file, "w", encoding="utf-8") as f:
                        json.dump(ops, f, ensure_ascii=False, indent=2)
                except Exception as e:
                    messagebox.showwarning("Error", f"Could not remove operator from file.\n{e}")
                    return
                messagebox.showinfo("Success", "Operator removed successfully.")
                op_info_window.destroy()
            else:
                messagebox.showwarning("Error", "Operator ID not found.")

    confirm_btn = CTkButton(master=op_info_window, text="Confirm", font=("Arial", 15), width=100, height=40, command=confirm_edit)
    confirm_btn.place(x=200, y=220)

    remove_op_btn = CTkButton(master=op_info_window, text="Remove Operator", font=("Arial", 15), width=120, height=40, command=remove_operator_action)
    remove_op_btn.place(x=3, y=220)

    def edit_operator_action():
        set_editable(True)

    edit_op_btn = CTkButton(master=op_info_window, text="Edit Operator", font=("Arial", 15), width=120, height=40, command=edit_operator_action)
    edit_op_btn.place(x=375, y=220)

#===========================================

search_box_label = CTkFrame(master = main_window, border_color = '#1f6aa5', border_width = 2)
search_box_label.pack(fill = 'x', padx = 10, pady = 10)

search_box = CTkEntry(master = search_box_label, font = ("Arial", 15), height = 1)
search_box.pack(fill = 'x', side = 'left', expand = True, padx = 2, pady = 3)

#===========================================

borrow_frame = CTkFrame(master = main_window, border_color = '#1f6aa5', border_width = 2)
borrow_frame.pack(fill = 'y', padx = 10, pady = 10, side = 'right')


login_btn = CTkButton(master = borrow_frame, text = "Login", height = 40, font = ("Arial", 15), command = login)
login_btn.pack(fill = 'x', padx = 3, pady = (3,0))

add_op= CTkButton(master = borrow_frame, text = "Add Operator", height = 40, font = ("Arial", 15), command = add_operator, state="disabled")
add_op.pack(fill = 'x', padx = 3, pady = (3,0))

op_list_btn = CTkButton(master = borrow_frame, text = "Operators List", height = 40, font = ("Arial", 15), command = operator_list, state="disabled")
op_list_btn.pack(fill = 'x', padx = 3, pady = (3,0))

new_user_btn = CTkButton(master = borrow_frame, text = "New User", height = 40, font = ("Arial",15), command = new_user_btn_window)
new_user_btn.pack(fill = 'x', padx = 3, pady = 3)

find_user_btn = CTkButton(master = borrow_frame, text = "Find User", height = 40, font = ("Arial", 15), command = find_user_btn_window)
find_user_btn.pack(fill = 'x', padx = 3, pady = (0,3))

user_name_btn = CTkButton(master = borrow_frame, text = "No User", height = 40, font = ("Arial", 15), command = User_name_window)
user_name_btn.pack(fill = 'x', padx = 3, pady = (0,3))

borrow_btn = CTkButton(master = borrow_frame, text = "Borrow Book", height = 40, font = ("Arial", 15), command = Borrow_book_window)
borrow_btn.pack(fill = 'x', padx = 3, pady = (0,3))

day_limit_btn = CTkButton(master = borrow_frame, text = "Day Limitation", height = 40, font = ("Arial",15), command = Day_limitation_window)
day_limit_btn.pack(fill = 'x',padx = 3, pady = (0,3))

return_btn = CTkButton(master = borrow_frame, text = "Return Book", height = 40, font = ("Arial", 15), command = Return_book_window)
return_btn.pack(fill = 'x', padx = 3, pady = (0,3))

users_list_btn = CTkButton(master = borrow_frame, text = "Users List", height = 40, font = ("Arial", 15), command = User_list_window)
users_list_btn.pack(fill = 'x', padx = 3, pady = (0,3))

stock_status_frame = CTkFrame(master = borrow_frame, corner_radius = 6, fg_color='#1f6aa5')
stock_status_frame.pack(fill = 'x', padx = 3, pady = (0,3))

stock_status = CTkLabel(master = stock_status_frame, text = "Stock: 4", height = 40, font = ("Arial",15),
                         bg_color = "transparent")
stock_status.pack()

add_btn = CTkButton(master = borrow_frame, text = "Add Book", height = 40, font = ("Arial",15), command = Add_book_window)
add_btn.pack(fill = 'x',padx = 3, pady = (0,3))

remove_btn = CTkButton(master = borrow_frame, text = "Remove Book", height = 40, font = ("Arial",15), command = Remove_book_window)
remove_btn.pack(fill = 'x', padx = 3, pady = (0,3))

#===========================================

book_list_box_frame = CTkFrame(master = main_window)
book_list_box_frame.pack(fill = 'both', padx = 10, pady = 10, expand = True)

book_list_box = CTkListbox(master = book_list_box_frame, height = 550, border_color = '#1f6aa5', border_width = 2)
book_list_box.pack(fill = 'both', expand = True)

try:
    with open("./Books.json", "r", encoding="utf-8") as f:
        all_books = json.load(f)
except:
    all_books = []


def fill_book_list_box(book_list=None):
    global all_books, filtered_books
    try:
        with open("./Books.json", "r", encoding="utf-8") as f:
            all_books = json.load(f)
    except:
        all_books = []
    if book_list is None:
        book_list = all_books
    filtered_books = book_list
    book_list_box.delete(0, book_list_box.size())
    for book in book_list:
        name = book.get('book_name', '-')
        code = book.get('book_id', '-')
        stock = book.get('stock', '-')
        book_list_box.insert(book_list_box.size(), f"{name} | ID: {code} | Stock: {stock}")

fill_book_list_box()


filtered_books = []

def search_books(event=None):
    global filtered_books
    query = search_box.get().strip().lower()
    try:
        with open("./Books.json", "r", encoding="utf-8") as f:
            books = json.load(f)
    except:
        books = []
    if not query:
        filtered_books = books
    else:
        filtered_books = []
        for book in books:
            book_text = f"{book.get('book_name','')} {book.get('author','')} {book.get('book_id','')} {book.get('publisher','')} {book.get('category','')}".lower()
            if query in book_text:
                filtered_books.append(book)
    book_list_box.delete(0, book_list_box.size())
    for book in filtered_books:
        name = book.get('book_name', '-')
        code = book.get('book_id', '-')
        stock = book.get('stock', '-')
        book_list_box.insert(book_list_box.size(), f"{name} | ID: {code} | Stock: {stock}")


def on_book_double_click(event=None):
    selection = book_list_box.curselection()
    if selection is None:
        return
    if isinstance(selection, (list, tuple)):
        if not selection:
            return
        index = selection[0]
    else:
        index = selection
    try:
        index = int(index)
    except Exception:
        return
    if 0 <= index < len(filtered_books):
        book = filtered_books[index]
        def refresh_books():
            fill_book_list_box()
        book_information_window(book, refresh_callback=refresh_books)
        stock = book.get('stock', '-')
        stock_status.configure(text=f"Stock: {stock}")


def on_book_select(event=None):
    global selected_book_id
    selection = book_list_box.curselection()
    if selection is None:
        stock_status.configure(text="Stock: None")
        selected_book_id = None
        return
    if isinstance(selection, (list, tuple)):
        if not selection:
            stock_status.configure(text="Stock: None")
            selected_book_id = None
            return
        index = selection[0]
    else:
        index = selection
    try:
        index = int(index)
    except Exception:
        stock_status.configure(text="Stock: None")
        selected_book_id = None
        return
    if 0 <= index < len(filtered_books):
        book = filtered_books[index]
        selected_book_id = book.get('book_id', None)
        try:
            with open("./Users.json", "r", encoding="utf-8") as f:
                users = json.load(f)
        except Exception:
            users = []
        total_borrowed = 0
        for user in users:
            borrowed = user.get('borrowed_books', [])
            if isinstance(borrowed, str):
                try:
                    import ast
                    borrowed = ast.literal_eval(borrowed)
                    if not isinstance(borrowed, list):
                        borrowed = [borrowed]
                except Exception:
                    borrowed = [borrowed]
            if isinstance(borrowed, list):
                total_borrowed += sum(1 for b in borrowed if str(b) == str(selected_book_id))
        try:
            initial_stock = int(book.get('initial_stock', book.get('stock', 0)))
        except Exception:
            initial_stock = 0
        available_stock = initial_stock - total_borrowed
        if available_stock < 0:
            available_stock = 0
        stock_status.configure(text=f"Stock: {available_stock}")
    else:
        stock_status.configure(text="Stock: None")
        selected_book_id = None

book_list_box.bind('<Double-Button-1>', on_book_double_click)
book_list_box.bind('<<ListboxSelect>>', on_book_select)

stock_status.configure(text="Stock: None")

search_books()

def book_information_window(book, refresh_callback=None):
    book_info_window = CTkToplevel()
    center_window(book_info_window, 705, 350)
    book_info_window.title("Books Information")
    book_info_window.lift()
    book_info_window.grab_set()
    book_info_window.resizable(False,False)

    fields = [
        ("Book Name", "book_name"),
        ("Author", "author"),
        ("Publisher Name", "publisher"),
        ("Publish Date", "publish_date"),
        ("Book ID", "book_id"),
        ("Stock", "stock"),
        ("Category", "category")
    ]

    entries = []
    for i, (label, key) in enumerate(fields):
        fields_label_frame = CTkFrame(master=book_info_window, fg_color='#1f6aa5', corner_radius=6, width=100, height=27)
        fields_label = CTkLabel(master=fields_label_frame, text=label, bg_color='transparent', height=27, font=("Arial", 15))
        fields_entry = CTkEntry(master=book_info_window, width=580, height=35)
        value = book.get(key, "-")
        fields_entry.insert(0, str(value))
        fields_entry.configure(state='readonly')
        fields_label_frame.grid(row=i, column=0, padx=4, pady=4, sticky='nsew')
        fields_label_frame.grid_rowconfigure(0, weight=1)
        fields_label_frame.grid_columnconfigure(0, weight=1)
        fields_label.grid(padx=4, pady=4, sticky='nsew')
        fields_entry.grid(row=i, column=1)
        entries.append(fields_entry)

    editable_keys = ["book_name", "author", "publisher", "publish_date", "stock", "category"]
    entry_widgets = {}
    for i, (label, key) in enumerate(fields):
        entry_widgets[key] = entries[i]

    def set_editable(state=True):
        for key in editable_keys:
            widget = entry_widgets.get(key)
            if widget:
                if state:
                    widget.configure(state="normal")
                else:
                    widget.configure(state="readonly")

    def confirm_edit():
        new_data = {}
        for key in editable_keys:
            widget = entry_widgets.get(key)
            if widget:
                new_data[key] = widget.get().strip()
        book_id = book.get('book_id', None)
        if book_id is None:
            messagebox.showwarning("Error", "Book ID not found.")
            return
        try:
            with open("./Books.json", "r", encoding="utf-8") as f:
                books = json.load(f)
        except Exception:
            books = []
        updated = False
        for b in books:
            if str(b.get('book_id')) == str(book_id):
                for k, v in new_data.items():
                    b[k] = v
                updated = True
                break
        if updated:
            try:
                with open("./Books.json", "w", encoding="utf-8") as f:
                    json.dump(books, f, ensure_ascii=False, indent=2)
            except Exception as e:
                messagebox.showwarning("Error", f"Could not update book.\n{e}")
                return
            messagebox.showinfo("Success", "Book information updated.")
            set_editable(False)
            if refresh_callback:
                refresh_callback()
        else:
            messagebox.showwarning("Error", "Book not found in file.")

    def remove_book_action():
        answer = messagebox.askyesno("Confirm Remove", f"Are you sure you want to remove this book?\n\nName: {book.get('book_name','-')}\nID: {book.get('book_id','-')}")
        if answer:
            try:
                with open("./Books.json", "r", encoding="utf-8") as f:
                    books = json.load(f)
            except Exception:
                books = []
            book_id = book.get('book_id', None)
            if book_id is not None:
                books = [b for b in books if str(b.get('book_id')) != str(book_id)]
                try:
                    with open("./Books.json", "w", encoding="utf-8") as f:
                        json.dump(books, f, ensure_ascii=False, indent=2)
                except Exception as e:
                    messagebox.showwarning("Error", f"Could not remove book from file.\n{e}")
                    return
                messagebox.showinfo("Success", "Book removed successfully.")
                book_info_window.destroy()
                if refresh_callback:
                    refresh_callback()
            else:
                messagebox.showwarning("Error", "Book ID not found.")

    def edit_book_action():
        set_editable(True)

    confirm_btn = CTkButton(master=book_info_window, text="Confirm", font=("Arial", 15), width=100, height=40, command=confirm_edit)
    confirm_btn.place(x=305, y=303)
    remove_book_btn = CTkButton(master=book_info_window, text="Remove Book", font=("Arial", 15), width=100, height=40, command=remove_book_action)
    remove_book_btn.place(x=6, y=303)
    edit_book_btn = CTkButton(master=book_info_window, text="Edit Book", font=("Arial", 15), width=100, height=40, command=edit_book_action)
    edit_book_btn.place(x=598, y=303)

search_box.bind("<KeyRelease>", search_books)

if __name__ == "__main__":
    main_window.mainloop()