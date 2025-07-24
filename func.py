import random
import json
import os

class User:
    def __init__(self, FN, LN, ID, PHN, AD, RD, UID):
        self.fname = FN
        self.lname = LN
        self.id_number = ID
        self.phone_number = PHN
        self.address = AD
        self.register_date = RD
        self.user_id = UID
        self.borrowed_books = []
        
users = []
user_id_list = []
for i in range(100,1000000):
    user_id_list.append(i)
assigned_ids = set()

def load_users_info():
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
    with open("./Users.json", "w", encoding="utf-8") as f:
        json.dump(users, f, ensure_ascii=False, indent=4)

def add_new_user(FN, LN, ID, PHN, AD, RD):
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

