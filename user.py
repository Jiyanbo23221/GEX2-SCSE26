from admin import load_library, save_library, find_book

def books_in_category(books, category):
    result = []
    cat_lower = category.strip().lower()
    for book_id, book in books.items():
        if book['category'].strip().lower() == cat_lower:
            result.append(book_id)
    return result

def search_by_title(books, search_text):
    result = []
    search_lower = search_text.strip().lower()
    for book_id, book in books.items():
        if search_lower in book['title'].strip().lower():
            result.append(book_id)
    return result

def borrow_book(books, loans, search_text, borrower):
    if not borrower or borrower.strip() == "":
        return "EMPTY_NAME"
    book_id = find_book(books, search_text)
    if book_id is None:
        return "BOOK_NOT_FOUND"
    book = books[book_id]
    if not book['available']:
        return "NOT_AVAILABLE"
    book['available'] = False
    loans.append({"book_id": book_id, "borrower": borrower.strip()})
    return "OK"

def return_book(books, loans, book_title, borrower):
    if not borrower or borrower.strip() == "":
        return "EMPTY_NAME"
    book_id = find_book(books, book_title)
    if book_id is None:
        return "BOOK_NOT_FOUND"
    loan_to_remove = None
    for loan in loans:
        if loan['book_id'] == book_id:
            loan_to_remove = loan
            break
    if loan_to_remove is None:
        return "NOT_ON_LOAN"
    loans.remove(loan_to_remove)
    books[book_id]['available'] = True
    return "OK"

def main():
    filename = "library.json"
    data = load_library(filename)
    print("LIBRARY USER SYSTEM")
    print("=" * 60)
    while True:
        print("\n=== LIBRARY USER MENU ===")
        print("1. Search by title")
        print("2. Search by category")
        print("3. Borrow a book")
        print("4. Return a book")
        print("5. Exit")
        choice = input("Enter your choice: ").strip()
        if choice == "1":
            search = input("Enter title (full or partial): ").strip()
            ids = search_by_title(data['books'], search)
            if ids:
                for bid in ids:
                    book = data['books'][bid]
                    status = "AVAILABLE" if book['available'] else "ON LOAN"
                    print(f"{bid} | {book['title']} | {book['category']} | {status}")
            else:
                print("No books found.")
        elif choice == "2":
            cat = input("Enter category: ").strip()
            ids = books_in_category(data['books'], cat)
            if ids:
                for bid in ids:
                    book = data['books'][bid]
                    status = "AVAILABLE" if book['available'] else "ON LOAN"
                    print(f"{bid} | {book['title']} | {book['category']} | {status}")
            else:
                print("No books found in this category.")
        elif choice == "3":
            search = input("Enter book title/author/ID to borrow: ").strip()
            borrower = input("Enter borrower name: ").strip()
            result = borrow_book(data['books'], data['loans'], search, borrower)
            if result == "OK":
                print("Book borrowed successfully.")
            elif result == "EMPTY_NAME":
                print("Error: Borrower name cannot be empty.")
            elif result == "BOOK_NOT_FOUND":
                print("Error: Book not found.")
            elif result == "NOT_AVAILABLE":
                print("Error: Book is not available.")
        elif choice == "4":
            title = input("Enter book title to return: ").strip()
            borrower = input("Enter borrower name: ").strip()
            result = return_book(data['books'], data['loans'], title, borrower)
            if result == "OK":
                print("Book returned successfully.")
            elif result == "EMPTY_NAME":
                print("Error: Borrower name cannot be empty.")
            elif result == "BOOK_NOT_FOUND":
                print("Error: Book not found.")
            elif result == "NOT_ON_LOAN":
                print("Error: Book is not on loan.")
        elif choice == "5":
            save_library(data, filename)
            print("Library data saved. Exiting.")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
