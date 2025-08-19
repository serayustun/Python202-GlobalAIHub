import pytest
import httpx
from library import Library

def test_add_book_api_success(temp_library, mocker):
    # ARRANGE
    isbn = "9780451524935" # "1984" romanının ISBN'i
    
    mock_api_response = {
        f"ISBN:{isbn}": {
            "title": "Nineteen Eighty-Four",
            "authors": [{"name": "George Orwell"}]
        }
    }
    
    mocker.patch(
        "httpx.get", 
        return_value=mocker.Mock(
            status_code=200, 
            json=lambda: mock_api_response,
            raise_for_status=lambda: None
        )
    )
    
    # ACT: Test edeceğimiz API'li metodu çağırıyoruz.
    added_book = temp_library.add_book_from_api(isbn) # <-- DEĞİŞEN SATIR BURASI
    
    # ASSERT
    assert len(temp_library.books) == 1
    assert added_book is not None
    assert temp_library.books[0].title == "Nineteen Eighty-Four"
    assert temp_library.books[0].author == "George Orwell"

def test_add_book_api_not_found(temp_library, mocker):
    # ARRANGE
    isbn = "0000000000000" # Geçersiz bir ISBN
    
    mock_response = mocker.Mock(status_code=404)
    mocker.patch(
        "httpx.get", 
        side_effect=httpx.HTTPStatusError(
            "Not Found", request=mocker.Mock(), response=mock_response
        )
    )

    # ACT
    added_book = temp_library.add_book_from_api(isbn) # <-- VE BURASI
    
    # ASSERT
    assert len(temp_library.books) == 0
    assert added_book is None