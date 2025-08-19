from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List

# İsim çakışmasını önlemek için Book sınıfını LibraryBook olarak adlandıralım.
from library import Library, Book as LibraryBook

# --- Pydantic Modelleri ---
# Pydantic, API'mizin ne tür veri alıp ne tür veri döndüreceğini tanımlamamızı sağlar.
# Bu, otomatik veri doğrulama ve dokümantasyon oluşturur.

class BookModel(BaseModel):
    title: str
    author: str
    isbn: str

class ISBNModel(BaseModel):
    isbn: str

# --- FastAPI Uygulaması ---

# FastAPI nesnesini oluşturuyoruz. Bütün API mantığımız bu 'app' nesnesi etrafında dönecek.
app = FastAPI(
    title="Kütüphane API",
    description="Python 202 Bootcamp Projesi için basit bir kütüphane yönetim API'si.",
    version="1.0.0"
)

# Kütüphane nesnesini global olarak bir kere oluşturuyoruz.
# Sunucu çalıştığı sürece bu nesne hafızada kalacak ve verileri yönetecek.
library = Library()

# --- API Endpoint'leri ---

# @app.get("/books") bir "decorator"dır.
# Altındaki fonksiyonun, /books adresine bir GET isteği geldiğinde çalışacağını söyler.
@app.get("/books", response_model=List[BookModel])
def get_all_books():
    """Kütüphanedeki tüm kitapları listeler."""
    return library.books

# /books adresine POST isteği geldiğinde çalışır.
@app.post("/books", response_model=BookModel, status_code=201) # 201: Created
def add_new_book(item: ISBNModel):
    """
    Verilen ISBN ile Open Library'den kitap bilgilerini çeker ve kütüphaneye ekler.
    """
    added_book = library.add_book_from_api(item.isbn)
    
    if added_book is None:
        # Eğer kitap eklenemediyse, 404 Not Found hatası döndür.
        raise HTTPException(status_code=404, detail="Bu ISBN ile kitap bulunamadı veya API hatası.")
        
    return added_book

# /books/{isbn} adresine DELETE isteği geldiğinde çalışır.
@app.delete("/books/{isbn}", status_code=200)
def delete_book_by_isbn(isbn: str):
    """
    Belirtilen ISBN'e sahip kitabı kütüphaneden siler.
    """
    book_to_delete = library.find_book(isbn)
    
    if book_to_delete is None:
        raise HTTPException(status_code=404, detail="Silinecek kitap bulunamadı.")
    
    library.remove_book(isbn)
    # Silme işleminde genellikle silinen nesne değil, bir onay mesajı döndürülür.
    return {"message": f"'{book_to_delete.title}' başlıklı kitap başarıyla silindi."}

# Sunucuyu çalıştırdığımızda bir "hoş geldin" mesajı için.
@app.get("/")
def read_root():
    return {"message": "Kütüphane API'sine hoş geldiniz! Dokümantasyon için /docs adresini ziyaret edin."}