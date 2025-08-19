import pytest
import os
from library import Book, Library

# "fixture", her test fonksiyonundan önce çalışan bir hazırlık fonksiyonudur.
# Bu fixture, her test için bize temiz bir Library nesnesi ve geçici bir test dosyası sağlar.
# Bu sayede testlerimiz ana library.json dosyamızı kirletmez.
@pytest.fixture
def temp_library(tmp_path):
    # tmp_path, pytest'in sağladığı, test bitince otomatik silinen geçici bir klasördür.
    test_file = tmp_path / "test_library.json"
    lib = Library(filename=str(test_file))
    return lib 