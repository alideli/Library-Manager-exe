"""
Utility functions for Library Manager
"""

def center_window(main, window_width, window_height):
    """Center a window on the screen."""
    screen_width = main.winfo_screenwidth()
    screen_height = main.winfo_screenheight()
    x = int((screen_width - window_width) / 2)
    y = int((screen_height - window_height) / 2)
    main.geometry(f"{window_width}x{window_height}+{x}+{y}")

def get_book_name(book_id):
    """Get book name by book_id from Books.json."""
    import json
    try:
        with open("./Books.json", "r", encoding="utf-8") as f:
            books = json.load(f)
    except Exception:
        books = []
    for b in books:
        if str(b.get('book_id')) == str(book_id):
            return b.get('book_name', str(book_id))
    return str(book_id)
