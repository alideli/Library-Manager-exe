# Library Manager

A modern, user-friendly library management system built with Python and CustomTkinter.

## Features
- Add, edit, and remove users and books
- Borrow and return books with live stock tracking
- User registration and search (by last name, ID number, or user ID)
- Book search and filtering (by name, author, publisher, category, or ID)
- View borrowed books with borrow date, day limitation, and days left
- In-place editing and removal for users and books (double-click to edit)
- Operator and admin login management
- Automatic UI refresh after any operation
- Data stored in JSON files for easy backup and portability
- Multi-window dialogs for user and book management
- Day limitation for borrowing (7, 14, 21, 30, 60, 90 days, or Unlimited)
- Real-time validation for required fields and stock availability
- All actions are confirmed with dialog boxes for safety

## Project Structure
- `main.py`: Main application and user interface logic
- `data_manager.py`: Data management functions (user/book/operator CRUD, JSON operations)
- `utils.py`: Utility functions (window centering, book name lookup)
- `Users.json`: User data storage
- `Books.json`: Book data storage
- `Operators.json`: Operator data storage
- `icon/Library_icon.ico`: Application icon

## Requirements
- Python 3.10+
- customtkinter
- tkinter

## How to Run
1. Install requirements:
   ```bash
   pip install customtkinter
   ```
2. Run the application:
   ```bash
   python main.py
   ```

## Usage & Interface Overview

When you run the program, the main window appears with two main sections:

- **Book List (left):** Shows all books in the library. You can search, select, and double-click to view/edit details. The list updates automatically after any change.
- **Control Panel (right):** Contains all main action buttons for user and book management.

### Main Buttons

- **Login:** Login as admin or operator (admin: username `admin`, password `admin123`)
- **Add Operator:** Add a new operator (admin only)
- **Operators List:** View all operators (admin only)
- **New User:** Add a new user to the library
- **Find User:** Search for a user by last name, ID number, or user ID. If found, the user is selected for borrowing/returning books.
- **No User / [User Name]:** Shows information about the currently selected user
- **Borrow Book:** Borrow the selected book for the selected user. You must set a day limitation and select both a user and a book.
- **Day Limitation:** Set the borrowing period (7, 14, 21, 30, 60, 90 days, or Unlimited)
- **Return Book:** Return the selected book for the selected user
- **Users List:** Shows a list of all users. Double-click a user to view/edit/remove them.
- **Add Book:** Add a new book to the library
- **Remove Book:** Remove a book by entering its ID

### Book List Interactions
- **Search Box (top left):** Filter books by name, author, publisher, category, or ID
- **Double-click a book:** Opens the book information window for editing or removal
- **Selecting a book:** Updates the stock status and enables borrowing/returning

### User List Interactions
- **Double-click a user:** Opens the user information window for editing or removal

### Operator Management
- Only admin can add or view operators
- Operators can log in and perform standard operations

### Data Saving
- All changes (add, edit, remove) are saved automatically to `Users.json`, `Books.json`, and `Operators.json`
- Data is stored in JSON format for easy backup and portability

### Tips
- Always select a user and a book before borrowing or returning
- You can edit user and book information in their respective info windows
- The UI updates automatically after every operation
- Dialog boxes confirm all critical actions (add, edit, remove, borrow, return)




This project is provided for educational purposes.## License## License
This project is provided for educational and personal use.
