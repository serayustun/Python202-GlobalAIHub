from fastapi.testclient import TestClient
import pytest
import httpx
# api'den hem app'i hem de paylaşılan library nesnesini TEK SATIRDA import edelim
from api import app, library as api_library

# Test istemcisini oluşturuyoruz.
client = TestClient(app)

def test_read_root():
    """Ana endpoint'in çalıştığını test et."""
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Kütüphane API'sine hoş geldiniz! Dokümantasyon için /docs adresini ziyaret edin."}

def test_get_books_initially_empty():
    """Başlangıçta kitap listesinin boş geldiğini test et."""
    # Teste başlamadan önce kütüphanenin boş olduğundan emin olalım.
    api_library.books = [] 
    
    response = client.get("/books")
    assert response.status_code == 200
    assert response.json() == []

def test_add_book_api_success(mocker):
    """API üzerinden başarıyla kitap eklendiğini test et."""
    isbn = "9780451524935" # 1984
    
    mock_api_response = {
        f"ISBN:{isbn}": {"title": "Nineteen Eighty-Four", "authors": [{"name": "George Orwell"}]}
    }
    mocker.patch(
        "httpx.get", 
        return_value=mocker.Mock(status_code=200, json=lambda: mock_api_response, raise_for_status=lambda: None)
    )
    
    response = client.post("/books", json={"isbn": isbn})
    
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "Nineteen Eighty-Four"
    
    # Kütüphanede gerçekten 1 kitap olduğundan emin ol
    assert len(api_library.books) == 1 

def test_add_book_api_not_found(mocker):
    """Bulunamayan bir ISBN için doğru hata döndüğünü test et."""
    isbn = "0000000000000"
    
    mocker.patch(
        "httpx.get", 
        side_effect=httpx.HTTPStatusError("Not Found", request=mocker.Mock(), response=mocker.Mock(status_code=404))
    )
    
    response = client.post("/books", json={"isbn": isbn})
    assert response.status_code == 404
    assert "bulunamadı" in response.json()["detail"]

def test_delete_book():
    """Kitap silme endpoint'inin çalıştığını test et."""
    isbn_to_delete = "9780451524935"
    
    response = client.delete(f"/books/{isbn_to_delete}")
    assert response.status_code == 200
    assert "başarıyla silindi" in response.json()["message"]
    
    # Kütüphanenin artık boş olduğundan emin ol
    assert len(api_library.books) == 0 