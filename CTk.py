import tkinter
import customtkinter
from CTkListbox import CTkListbox
from customtkinter import *
from tkinter import messagebox
from func import add_new_user
from func import update_borrowed_books
from func import add_new_book
import json

selected_user_id = None
selected_borrowed_books = []
selected_book_id = None
        
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
    borrow_window = messagebox.askyesno(f"Borrow Confirm", f"Are you sure to Borrow Book for user?")
    if borrow_window:
        if selected_book_id is None:
            messagebox.showwarning("Error", "No book selected.")
            return
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
    return_window = messagebox.askyesno("Return Confirm", f"Are you sure to return book for user?")
    if return_window:
        if selected_book_id is None:
            messagebox.showwarning("Error", "No book selected.")
            return
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
    center_window(username_window, 712, 500)
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
        def get_book_name(book_id):
            for b in books:
                if str(b.get('book_id')) == str(book_id):
                    return b.get('book_name', str(book_id))
            return str(book_id)

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
                            # محاسبه روزهای باقی‌مانده
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
   
def User_list_window2(user):
    userlist_window2 = CTkToplevel()
    center_window(userlist_window2, 712, 500)
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
    def get_book_name(book_id):
        for b in books:
            if str(b.get('book_id')) == str(book_id):
                return b.get('book_name', str(book_id))
        return str(book_id)

    user_day_limit = None
    if 'day_limit' in user:
        user_day_limit = user['day_limit']
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
        
    # confirm_btn = CTkButton(master = userlist_window2, text = "Confirm", font = ("Arial", 15), width = 100, height = 40)
    # confirm_btn.place(x = 305, y = 350)
    # delete_user_btn = CTkButton(master = userlist_window2, text = "Remove User", font = ("Arial", 15), width = 100, height = 40)
    # delete_user_btn.place(x = 10, y = 350)
        
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
    center_window(add_book_window, 700, 303)
    add_book_window.title("Users Information")
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
        book = add_new_book(*values)
        messagebox.showinfo("Success", f"Book added!\nBook ID: {book['book_id']}")
        add_book_window.destroy()

    confirm_btn = CTkButton(master=add_book_window, text="Confirm", font=("Arial", 15), width=100, height=40, command=confirm)
    confirm_btn.place(x=300, y=258)
    
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
    
    def confirm():
        from func import remove_book_by_id, get_book_by_id
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
    
    
#===========================================

search_box_label = CTkFrame(master = main_window, border_color = '#1f6aa5', border_width = 2)
search_box_label.pack(fill = 'x', padx = 10, pady = 10)

search_box = CTkEntry(master = search_box_label, font = ("Arial", 15), height = 1)
search_box.pack(fill = 'x', side = 'left', expand = True, padx = 2, pady = 3)

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
    if book_list is None:
        book_list = all_books
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
        book_information_window(book)
        stock = book.get('stock', '-')
        stock_status.configure(text=f"Stock: {stock}")


def on_book_select(event=None):
    global selected_book_id
    selection = book_list_box.curselection()
    if selection is None:
        stock_status.configure(text="Stock: None Selected")
        selected_book_id = None
        return
    if isinstance(selection, (list, tuple)):
        if not selection:
            stock_status.configure(text="Stock: None Selected")
            selected_book_id = None
            return
        index = selection[0]
    else:
        index = selection
    try:
        index = int(index)
    except Exception:
        stock_status.configure(text="Stock: None Selected")
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
        stock_status.configure(text="Stock: None Selected")
        selected_book_id = None

book_list_box.bind('<Double-Button-1>', on_book_double_click)
book_list_box.bind('<<ListboxSelect>>', on_book_select)

stock_status.configure(text="Stock: None Selected")

search_books()

def book_information_window(book):
    book_info_window = CTkToplevel()
    center_window(book_info_window, 712, 420)
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

    for i, (label, key) in enumerate(fields):
        fields_label_frame = CTkFrame(master = book_info_window, fg_color = '#1f6aa5', corner_radius = 6, width = 100, height = 27)
        fields_label = CTkLabel(master = fields_label_frame, text = label, bg_color = 'transparent', height = 27, font = ("Arial", 15))
        fields_entry = CTkEntry(master = book_info_window, width = 580, height = 35)
        value = book.get(key, "-")
        fields_entry.insert(0, str(value))
        fields_entry.configure(state='readonly')

        fields_label_frame.grid(row = i, column = 0, padx = 4, pady = (4), sticky = 'nsew')
        fields_label_frame.grid_rowconfigure(0, weight = 1)
        fields_label_frame.grid_columnconfigure(0, weight = 1)
        fields_label.grid(padx = 4, pady = 4, sticky = 'nsew')
        fields_entry.grid(row = i, column = 1)
        
    confirm_btn = CTkButton(master = book_info_window, text = "Confirm", font = ("Arial", 15), width = 100, height = 40)
    confirm_btn.place(x = 305, y = 350)
    delete_user_btn = CTkButton(master = book_info_window, text = "Remove User", font = ("Arial", 15), width = 100, height = 40)
    delete_user_btn.place(x = 10, y = 350)

search_box.bind("<KeyRelease>", search_books)

main_window.mainloop()