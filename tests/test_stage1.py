from library import Book, Library

def test_add_book_object(temp_library):
    # ARRANGE (Hazırlık): Gerekli nesneleri oluştur.
    book = Book("Test Title", "Test Author", "12345")
    
    # ACT (Eylem): Test edilecek metodu çalıştır.
    temp_library.add_book_object(book)
    
    # ASSERT (Doğrulama): Sonucun beklediğimiz gibi olup olmadığını kontrol et.
    assert len(temp_library.books) == 1
    assert temp_library.books[0].title == "Test Title"

def test_remove_book(temp_library):
    book = Book("Another Title", "Another Author", "67890")
    temp_library.add_book_object(book) 
    assert len(temp_library.books) == 1

    temp_library.remove_book("67890") 
    assert len(temp_library.books) == 0

def test_find_book_found(temp_library):
    book = Book("Find Me", "Finder", "abcde")
    temp_library.add_book_object(book)
    
    found_book = temp_library.find_book("abcde")
    
    assert found_book is not None 
    assert found_book.isbn == "abcde"

def test_find_book_not_found(temp_library):
    found_book = temp_library.find_book("xyz")
    assert found_book is None 

def test_persistence(tmp_path):
    test_file = tmp_path / "persistent_library.json"
    
    # 1. Kütüphane oluştur ve kitap ekle
    lib1 = Library(filename=str(test_file))
    book = Book("Persistent Book", "Durable Author", "55555")
    lib1.add_book_object(book) # BURASI GÜNCELLENDİ

    # 2. Yeni bir kütüphane nesnesi oluştur (aynı dosyayı kullanarak)
    lib2 = Library(filename=str(test_file))
    
    assert len(lib2.books) == 1
    assert lib2.books[0].title == "Persistent Book"