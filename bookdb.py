import sqlite3
import tkinter as tk
from tkinter import messagebox, simpledialog

# Class to handle SQLite operations
class BookDatabase:
    def __init__(self):
        # Connect to the SQLite database or create one if it doesn't exist
        self.conn = sqlite3.connect('books.db')
        self.cursor = self.conn.cursor()

        # Create the 'books' table if it doesn't exist
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS books (id INTEGER PRIMARY KEY, title TEXT, author TEXT)
        ''')

    def add_book(self, title, author):
        # Insert a new book into the 'books' table
        self.cursor.execute("INSERT INTO books (title, author) VALUES (?, ?)", (title, author))
        self.conn.commit()

    def get_all_books(self):
        # Retrieve all books from the 'books' table
        self.cursor.execute("SELECT * FROM books")
        return self.cursor.fetchall()

    def search_books(self, keyword):
        # Search books where the title or author matches the keyword
        self.cursor.execute("SELECT * FROM books WHERE title LIKE ? OR author LIKE ?", (f"%{keyword}%", f"%{keyword}%"))
        return self.cursor.fetchall()

# Class to handle the tkinter GUI
class BookApp:
    def __init__(self, root):
        # Initialize the database
        self.db = BookDatabase()
        
        # Label for the title input
        self.title_label = tk.Label(root, text="Title")
        self.title_label.pack()

        # Entry widget for the title input
        self.title_entry = tk.Entry(root)
        self.title_entry.pack()

        # Label for the author input
        self.author_label = tk.Label(root, text="Author")
        self.author_label.pack()

        # Entry widget for the author input
        self.author_entry = tk.Entry(root)
        self.author_entry.pack()

        # Button to add a book to the database
        self.add_button = tk.Button(root, text="Add Book", command=self.add_book)
        self.add_button.pack()

        # Button to display all books
        self.list_button = tk.Button(root, text="List All Books", command=self.list_books)
        self.list_button.pack()

        # Entry widget to search for a book by title or author
        self.search_entry = tk.Entry(root)
        self.search_entry.pack()

        # Button to initiate the book search
        self.search_button = tk.Button(root, text="Search", command=self.search_books)
        self.search_button.pack()

        # Text widget to display the books
        self.output_text = tk.Text(root, width=50, height=10)
        self.output_text.pack()

    def add_book(self):
        # Get the title and author from the respective entry widgets
        title = self.title_entry.get()
        author = self.author_entry.get()

        # Add the book to the database
        self.db.add_book(title, author)

        # Clear the entry widgets
        self.title_entry.delete(0, tk.END)
        self.author_entry.delete(0, tk.END)

        # Notify the user
        messagebox.showinfo("Success", "Book added successfully!")

    def list_books(self):
        # Fetch all books from the database
        books = self.db.get_all_books()

        # Clear the current text in the output widget
        self.output_text.delete(1.0, tk.END)

        # Populate the output_text widget with the list of books
        for book in books:
            self.output_text.insert(tk.END, f"{book[1]} by {book[2]}\n")

    def search_books(self):
        # Fetch the keyword from the search entry widget
        keyword = self.search_entry.get()

        # Search for the books in the database
        books = self.db.search_books(keyword)

        # Clear the current text in the output widget
        self.output_text.delete(1.0, tk.END)

        # Populate the output_text widget with the search results
        for book in books:
            self.output_text.insert(tk.END, f"{book[1]} by {book[2]}\n")

# Main code to run the app
root = tk.Tk()
root.title("Book Management System")
app = BookApp(root)
root.mainloop()