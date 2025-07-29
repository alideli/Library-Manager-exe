# ========== Imports ==========
import os
import json

# ========== User Management ==========
users = []
user_id_list = list(range(100, 1000001))
assigned_ids = set()

def load_users_info():
    """Load users from Users.json and update assigned_ids."""
    global users, assigned_ids
    assigned_ids.clear()
    if os.path.exists("./Users.json"):
        with open("./Users.json", "r", encoding="utf-8") as f:
            users = json.load(f)
            for user in users:
                assigned_ids.add(user['user_id'])
    else:
        users = []

def save_users_info():
    """Save users to Users.json."""
    with open("./Users.json", "w", encoding="utf-8") as f:
        json.dump(users, f, ensure_ascii=False, indent=4)

def add_new_user(FN, LN, ID, PHN, AD, RD):
    """Add a new user and return the user dict."""
    load_users_info()
    for uid in user_id_list:
        if uid not in assigned_ids:
            assigned_ids.add(uid)
            break
    else:
        raise Exception("No available user ID!")
    user_dict = {
        'first_name': FN,
        'last_name': LN,
        'id_number': ID,
        'phone_number': PHN,
        'address': AD,
        'register_date': RD,
        'user_id': uid,
        'borrowed_books': []
    }
    users.append(user_dict)
    save_users_info()
    return user_dict

def update_borrowed_books(user_id, new_borrowed_books):
    """Update the borrowed_books list for a user."""
    load_users_info()
    for user in users:
        if str(user['user_id']) == str(user_id):
            user['borrowed_books'] = new_borrowed_books
            break
    save_users_info()

# ========== Book Management ==========
books = []
assigned_book_ids = set()
book_id_list = list(range(1, 1000001))
books = []
assigned_book_ids = set()
book_id_list = list(range(1, 1000001))

def load_books_info():
    """Load books from Books.json and update assigned_book_ids."""
    global books, assigned_book_ids
    assigned_book_ids.clear()
    if os.path.exists("./Books.json"):
        with open("./Books.json", "r", encoding="utf-8") as f:
            books = json.load(f)
            for book in books:
                assigned_book_ids.add(book['book_id'])
    else:
        books = []

def save_books_info():
    """Save books to Books.json."""
    with open("./Books.json", "w", encoding="utf-8") as f:
        json.dump(books, f, ensure_ascii=False, indent=4)

def generate_sequential_book_id():
    """Generate a new unique book ID."""
    load_books_info()
    for bid in book_id_list:
        if bid not in assigned_book_ids:
            assigned_book_ids.add(bid)
            return bid
    raise Exception("No available book ID!")

def add_new_book(book_name, author, publisher, publish_date, stock, category):
    """Add a new book and return the book dict."""
    load_books_info()
    book_id = generate_sequential_book_id()
    book_dict = {
        "book_name": book_name,
        "author": author,
        "publisher": publisher,
        "publish_date": publish_date,
        "book_id": book_id,
        "stock": stock,
        "category": category
    }
    books.append(book_dict)
    save_books_info()
    return book_dict

def remove_book_by_id(book_id):
    """Remove a book from Books.json by its book_id. Returns True if removed, False if not found."""
    books_path = "./Books.json"
    if not os.path.exists(books_path):
        return False
    with open(books_path, "r", encoding="utf-8") as f:
        books = json.load(f)
    initial_len = len(books)
    books = [book for book in books if str(book.get('book_id')) != str(book_id)]
    if len(books) < initial_len:
        with open(books_path, "w", encoding="utf-8") as f:
            json.dump(books, f, ensure_ascii=False, indent=4)
        return True
    return False

def get_book_by_id(book_id):
    """Get a book dict by its book_id. Returns None if not found."""
    books_path = "./Books.json"
    if not os.path.exists(books_path):
        return None
    with open(books_path, "r", encoding="utf-8") as f:
        books = json.load(f)
    for book in books:
        if str(book.get('book_id')) == str(book_id):
            return book
    return None





