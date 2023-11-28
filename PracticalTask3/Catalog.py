import sys
from Book import Book

def main():
    catalog = [
        Book("0553296981", "The Diary of a Young Girl", "Anne Frank", 16.50),
        Book("1400082773", "Dreams from My Father", "Barack Obama", 24.99)
    ]

    while True:
        print_menu()
        option = input("Enter option number: ")
        if option == "1":
            add_book(catalog)
        elif option == "2":
            display_sorted(catalog)
        elif option == "3":
            search_books(catalog)
        elif option == "4":
            delete_book(catalog)
        elif option == "5":
            display_books(catalog)
        elif option == "6":
            if confirm_exit():
                print("Exiting the program.")
                sys.exit()
        else:
            print("Invalid option, please try again.")

# Function definitions for add_book, display_sorted, search_books, delete_book, display_books, print_menu, confirm_exit...

if __name__ == "__main__":
    main()