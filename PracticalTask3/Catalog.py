import tkinter as tk
from tkinter import messagebox
from Book import Book


catalog = []

def add_book():
    global catalog
    add_window = tk.Toplevel(root)
    add_window.title("Add a New Book")
    add_window.geometry('400x200')

    fields = ['isbn', 'title', 'author', 'price']
    entries = {field: "" for field in fields}

    # 現在表示しているエントリーとラベルをクリアする内部関数
    def clear_fields():
        for widget in add_window.winfo_children():
            widget.destroy()

    # 各フィールドを表示する関数（idxは現在のフィールドのインデックス）
    def display_next_field(entry, idx):
        if entry is not None:
            field_name = fields[idx - 1]
            entries[field_name] = entry.get()  # 前のフィールドの値を保存

        clear_fields()  # 前のエントリーとラベルをクリア

        if idx < len(fields):
            field = fields[idx]

            # ラベルの設定
            label = tk.Label(add_window, text=f"Enter the book's {field}:")
            label.pack()

            # エントリーの生成
            next_entry = tk.Entry(add_window)
            next_entry.pack()
            next_entry.focus_set()

            # 次へボタンまたは保存ボタン
            next_button_text = 'Save' if idx == len(fields) - 1 else 'Next'
            next_button = tk.Button(add_window, text=next_button_text,
                                    command=lambda: display_next_field(next_entry, idx + 1))
            next_button.pack()
        else:
            # 全部のエントリーが終わったら保存処理をする
            save_and_close()

    # 本の情報を保存してカタログに追加する関数
    def save_and_close():
        try:
            # 入力された値を取得してtrim処理
            isbn = entries['isbn'].strip()
            title = entries['title'].strip()
            author = entries['author'].strip()

            # priceの入力が数値に変換できるかチェック
            try:
                price = float(entries['price'].strip())
            except ValueError:
                raise ValueError("Please enter a valid number for price.")

            # 全てのフィールドが入力されているかチェック
            if not isbn or not title or not author or not price:
                raise ValueError("All fields must be filled in!")

            # ISBNがすでにカタログ内に存在するかチェック
            for book in catalog:
                if book.isbn == isbn:
                    raise ValueError("A book with the same ISBN already exists in the catalog.")

            # Bookオブジェクトの作成
            new_book = Book(isbn, title, author, price)
            catalog.append(new_book)  # カタログに追加
            messagebox.showinfo('Success', 'Book added successfully')
            add_book.destroy()  # 成功メッセージの後、ウィンドウを閉じる
        except ValueError as ve:
            messagebox.showerror('Error', str(ve))
            add_book.destroy()  # エラーメッセージの後、ウィンドウを閉じる


    # 最初のフィールドを表示する
    display_next_field(None, 0)

def sort_and_display():
    if not catalog:
        messagebox.showinfo("Catalog", "There are no books in the catalog.")
        return

    # 価格でソート
    sorted_catalog = sorted(catalog, key=lambda book: book.price)
    catalog_str = '\n'.join([f"ISBN: {book.isbn}, Title: {book.title}, Author: {book.author}, Price: ${book.price}" for book in sorted_catalog])
    display_window = tk.Toplevel(root)
    display_window.title("Catalog Sorted by Price")
    display_window.geometry('400x200')

    tk.Label(display_window, text="Catalog Sorted by Price:").pack()
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
        search_title = title_entry.get().strip()
        if not search_title:  # テキストが空、または空白のみの場合
            messagebox.showinfo("Search Input Error", "The text has not been entered or only space.")
            return
        if not catalog:
            messagebox.showinfo("Search Result", "The catalog is empty.")
            return

        # 部分一致で書籍を検索
        found_books = [book for book in catalog if search_title.lower() in book.title.lower()]

        if found_books:
            result = '\n'.join([
                f"ISBN: {book.isbn}, Title: {book.title}, Author: {book.author}, Price: ${book.price}"
                for book in found_books
            ])
            messagebox.showinfo("Search Result", f"Books found:\n{result}")
        else:
            messagebox.showinfo("Search Result", "No books found with the given title.")

    tk.Button(search_window, text="Search", command=perform_search).pack()
    # 削除された重複するボタン
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
                messagebox.showinfo("Success", "Book HAS been deleted.")
                delete_window.destroy()  # ウィンドウを閉じる
            else:
                messagebox.showinfo("Cancelled", "Book has NOT been deleted.")
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
title_label = tk.Label(root, text="-----Holmesglen Book Store-----", font=("Arial", 16))
title_label.pack(side=tk.TOP, pady=(5, 10))

tk.Button(root, text="1. Add a Book", command=add_book).pack(fill=tk.X)
tk.Button(root, text="2. Sort and Display the Books by ISBN", command=sort_and_display).pack(fill=tk.X)
tk.Button(root, text="3. Search Books by Title", command=search_books).pack(fill=tk.X)
tk.Button(root, text="4. Delete a Book", command=delete_book).pack(fill=tk.X)
tk.Button(root, text="5. Display All Books", command=display_all_books).pack(fill=tk.X)
tk.Button(root, text="6. Exit", command=exit_program).pack(fill=tk.X)

# ユーザーの入力用エリア
entry_frame = tk.Frame(root)
entry_frame.pack(side=tk.TOP, pady=(5, 10))

entry_label = tk.Label(root, text="Enter menu choice:")
entry_label.pack(side=tk.LEFT, pady=(5, 10))
entry = tk.Entry(root)
entry.pack(side=tk.LEFT, expand=True, fill=tk.X, pady=(5, 10))

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