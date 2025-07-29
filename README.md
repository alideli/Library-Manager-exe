# Library Manager

A modern, user-friendly library management system built with Python and CustomTkinter.

## Features
- Add, edit, and remove users and books
- Borrow and return books with live stock tracking
- User registration and search
- Book search and filtering
- Borrowed books with borrow date, day limitation, and live days left
- In-place editing and removal for users and books
- Automatic UI refresh after any operation
- Data stored in JSON files for easy backup and portability

## Project Structure
- `main.py`: Main application and user interface logic
- `data_manager.py`: Data management functions (user/book CRUD, JSON operations)
- `utils.py`: Utility functions (window centering, book name lookup)
- `Users.json`: User data storage
- `Books.json`: Book data storage
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


## Usage & Buttons

When you run the program, the main window will appear with two main sections:

- **Book List (left):** Shows all books in the library. You can search, select, and double-click to view/edit details.
- **Control Panel (right):** Contains all main action buttons:

### Buttons:

- **New User**: Opens a form to add a new user to the library.
- **Find User**: Search for a user by last name, ID number, or user ID. If found, the user is selected for borrowing/returning books.
- **No User / [User Name]**: Shows information about the currently selected user.
- **Borrow Book**: Borrows the selected book for the selected user. You must set a day limitation and select both a user and a book.
- **Day Limitation**: Set the borrowing period (7, 14, 21, 30, 60, 90 days, or Unlimited).
- **Return Book**: Returns the selected book for the selected user.
- **Users List**: Shows a list of all users. Double-click a user to view/edit/remove them.
- **Add Book**: Opens a form to add a new book to the library.
- **Remove Book**: Remove a book by entering its ID.

### Book List Interactions:
- **Search Box (top left):** Filter books by name, author, publisher, category, or ID.
- **Double-click a book:** Opens the book information window for editing or removal.
- **Selecting a book:** Updates the stock status and enables borrowing/returning.

### User List Interactions:
- **Double-click a user:** Opens the user information window for editing or removal.

### Data Saving:
- All changes (add, edit, remove) are saved automatically to `Users.json` and `Books.json`.

### Tips:
- Always select a user and a book before borrowing or returning.
- You can edit user and book information in their respective info windows.
- The UI updates automatically after every operation.

## License
This project is provided for educational and personal use.
