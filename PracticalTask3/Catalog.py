import tkinter as tk
from tkinter import messagebox
from Book import Book

# スタート時にカタログに本を追加します
catalog = [
    Book("123456789", "Book A", "Author A", 9.99),
    Book("987654321", "Book B", "Author B", 14.99),
]

def add_book():
    add_window = tk.Toplevel(root)
    add_window.title("Add a New Book")
    add_window.geometry('400x200')
    fields = ['isbn', 'title', 'author', 'price']
    entries = {}
    index = 0

    def display_next_field(idx):
        for widget in add_window.winfo_children():
            widget.destroy()

        label_text = fields[idx] if idx != len(fields) - 1 else "Enter the book's " + fields[idx] + " (numeric value):"
        label = tk.Label(add_window, text=label_text)
        label.pack()

        entry = tk.Entry(add_window)
        entry.pack()
        entries[fields[idx]] = entry
        entry.focus_set()

        if idx < len(fields) - 1:
            next_button = tk.Button(add_window, text='OK', command=lambda: save_and_next(idx))
            next_button.pack()
        else:
            save_button = tk.Button(add_window, text='Save', command=save_and_close)
            save_button.pack()

        cancel_button = tk.Button(add_window, text='Cancel', command=add_window.destroy)
        cancel_button.pack()

    def save_and_next(idx):
        if not entries[fields[idx]].get().strip():
            messagebox.showwarning("Warning", "Please do not leave the field empty.")
        else:
            if idx < len(fields) - 1:
                display_next_field(idx + 1)

def save_and_close():
    try:
        isbn = entries['isbn'].get().strip()
        title = entries['title'].get().strip()
        author = entries['author'].get().strip()
        price_str = entries['price'].get().strip()

        if not (isbn and title and author and price_str):
            messagebox.showwarning("Warning", "Please fill in all fields.")
            return

        price = float(price_str)
        new_book = Book(isbn, title, author, price)
        catalog.append(new_book)

        messagebox.showinfo('Success', f'Book "{new_book.title}" has been added to the catalog.')
    except ValueError:
        messagebox.showerror('Error', 'Invalid price. Please enter a numeric value.')
        return
    except Exception as e:
        messagebox.showerror('Error', f'An error occurred: {e}')
        return
    finally:
        if add_book.winfo_exists():
            add_book.destroy()


    display_next_field(index)

def sort_and_display():
    if not catalog:
        messagebox.showinfo("Catalog", "There are no books in the catalog.")
        return

    # ISBNでソート
    sorted_catalog = sorted(catalog, key=lambda book: book.isbn)
    catalog_str = '\n'.join([f"ISBN: {book.isbn}, Title: {book.title}, Author: {book.author}, Price: ${book.price}" for book in sorted_catalog])
    display_window = tk.Toplevel(root)
    display_window.title("Catalog Sorted by ISBN")

    tk.Label(display_window, text="Catalog Sorted by ISBN:").pack()
    tk.Label(display_window, text=catalog_str, justify='left').pack(side="top", fill="both", expand=True)
    tk.Button(display_window, text="Close", command=display_window.destroy).pack()



def search_books():
    search_window = tk.Toplevel(root)
    search_window.title("Search a Book by Title")
    search_window.geometry('400x200')

    tk.Label(search_window, text="Enter the book's title:").pack()

    title_entry = tk.Entry(search_window)
    title_entry.pack()
    title_entry.focus_set()

    def perform_search():
        search_title = title_entry.get().strip().lower()
        if not catalog:
            messagebox.showinfo("Search Result", "The catalog is empty.")
            return

        # 部分一致で書籍を検索
        found_books = [book for book in catalog if search_title in book.title.lower()]

        if found_books:
            result = '\n'.join([f"ISBN: {book.isbn}, Title: {book.title}, Author: {book.author}, Price: ${book.price}" for book in found_books])
            messagebox.showinfo("Search Result", f"Books found:\n{result}")
        else:
            messagebox.showinfo("Search Result", "No books found with the given title.")

    tk.Button(search_window, text="Search", command=perform_search).pack()
    tk.Button(search_window, text="Close", command=search_window.destroy).pack()



def delete_book():
    delete_window = tk.Toplevel(root)
    delete_window.title("Delete a Book")
    delete_window.geometry('400x150')

    tk.Label(delete_window, text="Enter the book's ISBN to delete:").pack()

    isbn_entry = tk.Entry(delete_window)
    isbn_entry.pack()
    isbn_entry.focus_set()

    def confirm_and_delete():
        isbn_to_delete = isbn_entry.get().strip()
        book_to_delete = None

        for book in catalog:
            if book.isbn == isbn_to_delete:
                book_to_delete = book
                break

        if book_to_delete:
            confirm = messagebox.askyesno("Confirm", f"Are you sure you want to delete '{book_to_delete.title}'?")
            if confirm:
                catalog.remove(book_to_delete)
                messagebox.showinfo("Success", "The book has been deleted.")
            else:
                messagebox.showinfo("Cancelled", "Book deletion cancelled.")
        else:
            messagebox.showinfo("Not Found", "No book found with the given ISBN.")

    tk.Button(delete_window, text="Delete", command=confirm_and_delete).pack()
    tk.Button(delete_window, text="Close", command=delete_window.destroy).pack()

def display_all_books():
    if not catalog:
        messagebox.showinfo("Catalog", "There are no books in the catalog.")
        return

    display_window = tk.Toplevel(root)
    display_window.title("All Books in Catalog")
    display_window.geometry('500x300')

    books_str = '\n'.join([f"ISBN: {book.isbn}, Title: {book.title}, Author: {book.author}, Price: ${book.price}" for book in catalog])
    tk.Label(display_window, text="All Books in Catalog:", justify='left').pack()
    tk.Label(display_window, text=books_str, justify='left').pack(side="top", fill="both", expand=True)
    tk.Button(display_window, text="Close", command=display_window.destroy).pack()


def exit_program():
    root.destroy()  # GUIウィンドウを閉じてプログラムを終了

# tkinter ウィンドウを作成
root = tk.Tk()
root.title("Book Catalog")

# メニューボタンを作成
button_frame = tk.Frame(root)
button_frame.pack(side=tk.TOP, pady=(10, 0))

tk.Button(button_frame, text="1. Add a Book", command=add_book).pack(fill=tk.X)
tk.Button(button_frame, text="2. Sort and Display the Books by Price", command=sort_and_display).pack(fill=tk.X)
tk.Button(button_frame, text="3. Search Books by Title", command=search_books).pack(fill=tk.X)
tk.Button(button_frame, text="4. Delete a Book", command=delete_book).pack(fill=tk.X)
tk.Button(button_frame, text="5. Display All Books", command=display_all_books).pack(fill=tk.X)
tk.Button(button_frame, text="6. Exit", command=exit_program).pack(fill=tk.X)

# ユーザーの入力用エリア
entry_frame = tk.Frame(root)
entry_frame.pack(side=tk.TOP, pady=(5, 10))

entry_label = tk.Label(entry_frame, text="Enter menu choice:")
entry_label.pack(side=tk.LEFT)
entry = tk.Entry(entry_frame)
entry.pack(side=tk.LEFT, expand=True, fill=tk.X)

def exit_program():
    confirm = messagebox.askyesno("Confirm Exit", "Are you sure you want to exit?")
    if confirm:
        root.destroy()  # ユーザーが確認した場合、GUIウィンドウを閉じてプログラムを終了


# ユーザーのメニュー選択に応じて関数を呼び出す
def execute_choice(event=None):
    choice = entry.get()
    if choice == "1":
        add_book()
    elif choice == "2":
        sort_and_display()
    elif choice == "3":
        search_books()
    elif choice == "4":
        delete_book()
    elif choice == "5":
        display_all_books()
    elif choice == "6":
        exit_program()
    else:
        tk.messagebox.showwarning("Warning", "Please enter a valid menu option (1-6).")

entry.bind("<Return>", execute_choice)  # Enterキーが押された時に execute_choice 関数を実行

# GUIを実行
root.mainloop()