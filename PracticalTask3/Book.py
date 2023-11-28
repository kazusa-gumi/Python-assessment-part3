class Book:
    def __init__(self, isbn, title, author, price):
        self.isbn = isbn
        self.title = title
        self.author = author
        self.price = price

    def display(self):
        return f"ISBN: {self.isbn}, Title: {self.title}, Author: {self.author}, Price: {self.price}"