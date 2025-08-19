import json

class Book:
    """
    Tek bir kitabı temsil eden sınıf.
    Nitelikler (attributes): title, author, isbn
    """
    def __init__(self, title, author, isbn):
        self.title = title
        self.author = author
        self.isbn = isbn

    def __str__(self):
        return f'"{self.title}" by {self.author} (ISBN: {self.isbn})'

    def to_dict(self):
        return {"title": self.title, "author": self.author, "isbn": self.isbn}

class Library:
    """
    Kütüphane operasyonlarını yöneten sınıf.
    """
    def __init__(self, filename="library.json"):
        self.filename = filename
        self.books = self._load_books() 

    def _load_books(self):
        try:
            with open(self.filename, 'r') as f:
                books_data = json.load(f)
                return [Book(b['title'], b['author'], b['isbn']) for b in books_data]
        except (FileNotFoundError, json.JSONDecodeError):
            return []

    def _save_books(self):
        with open(self.filename, 'w') as f:
            json.dump([book.to_dict() for book in self.books], f, indent=4)

    def add_book(self, book):
        self.books.append(book)
        self._save_books()
        print(f"Başarıyla eklendi: {book}")

    def remove_book(self, isbn):
        book_to_remove = self.find_book(isbn)
        if book_to_remove:
            self.books.remove(book_to_remove)
            self._save_books()
            print(f"Başarıyla silindi: {book_to_remove}")
        else:
            print(f"Hata: {isbn} ISBN numaralı kitap bulunamadı.")

    def list_books(self):
        if not self.books:
            print("Kütüphanede hiç kitap yok.")
            return
        print("\n--- Kütüphanedeki Kitaplar ---")
        for book in self.books:
            print(book)
        print("----------------------------\n")

    def find_book(self, isbn):
        for book in self.books:
            if book.isbn == isbn:
                return book
        return None