from library import Library, Book

def main_menu():
    lib = Library() # Kütüphane nesnemizi oluşturuyoruz.

    while True:
        print("\nKütüphane Yönetim Sistemi")
        print("1. Kitap Ekle")
        print("2. Kitap Sil")
        print("3. Kitapları Listele")
        print("4. Kitap Ara")
        print("5. Çıkış")

        choice = input("Seçiminizi yapın (1-5): ")

        if choice == '1':
            title = input("Kitap başlığı: ")
            author = input("Yazar: ")
            isbn = input("ISBN: ")
            new_book = Book(title, author, isbn)
            lib.add_book(new_book)
        
        elif choice == '2':
            isbn = input("Silmek istediğiniz kitabın ISBN'ini girin: ")
            lib.remove_book(isbn)

        elif choice == '3':
            lib.list_books()

        elif choice == '4':
            isbn = input("Aramak istediğiniz kitabın ISBN'ini girin: ")
            book = lib.find_book(isbn)
            if book:
                print(f"Bulunan Kitap: {book}")
            else:
                print("Bu ISBN ile bir kitap bulunamadı.")
        
        elif choice == '5':
            print("Programdan çıkılıyor...")
            break
        
        else:
            print("Geçersiz seçim. Lütfen 1-5 arasında bir sayı girin.")

if __name__ == "__main__":
    main_menu()