import json

def load_library(filename):
    with open(filename, 'r', encoding='utf-8') as f:
        return json.load(f)

def save_library(data, filename):
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4)

def find_book(books, search_text):
    search_lower = search_text.strip().lower()
    for book_id, book in books.items():
        if (search_lower in book_id.lower() or
            search_lower in book['title'].lower() or
            search_lower in book['author'].lower()):
            return book_id
    return None

def display_books(books):
    print("BOOK CATALOGUE")
    print("-" * 60)
    for book_id, book in books.items():
        status = "AVAILABLE" if book['available'] else "ON LOAN"
        print(f"{book_id} | {book['title']} | {book['category']} | {status}")

def display_loans(loans, books):
    print("CURRENT LOANS")
    print("-" * 60)
    for loan in loans:
        book_id = loan['book_id']
        if book_id in books:
            title = books[book_id]['title']
        else:
            title = "Unknown"
        print(f"{book_id} | {title} | Borrower: {loan['borrower']}")

def library_statistics(books):
    total = len(books)
    available = sum(1 for book in books.values() if book['available'])
    borrowed = total - available
    return total, available, borrowed

def main():
    data = load_library("library.json")
    print("LIBRARY ADMINISTRATION")
    print("=" * 60)
    lib = data['library']
    print(f"Library: {lib['name']}")
    print(f"Branch: {lib['branch']}")
    print(f"Year: {lib['year']}")
    print(f"Categories: {', '.join(data['categories'])}")
    print()
    display_books(data['books'])
    print()
    display_loans(data['loans'], data['books'])
    print()
    total, available, borrowed = library_statistics(data['books'])
    print("STATISTICS")
    print("-" * 60)
    print(f"Total books: {total}")
    print(f"Available: {available}")
    print(f"Borrowed: {borrowed}")

if __name__ == "__main__":
    main()
