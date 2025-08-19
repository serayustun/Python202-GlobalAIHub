# Python Kütüphane Yönetim Sistemi (CLI & API)

Bu proje, Python 202 Bootcamp kapsamında geliştirilmiş, üç aşamalı modern bir Python uygulamasıdır. Proje, basit bir komut satırı arayüzünden (CLI) başlayarak, harici bir API ile veri zenginleştirmesi yapar ve son olarak tüm bu mantığı FastAPI tabanlı bir RESTful API servisine dönüştürür.

Proje, Nesne Yönelimli Programlama (OOP), API entegrasyonu, veri kalıcılığı (JSON), otomatik testler (Pytest) ve web servisi geliştirme gibi temel modern yazılım prensiplerini kapsamaktadır.

## Temel Özellikler

*   **Komut Satırı Arayüzü (CLI):** Kitap ekleme, silme, listeleme ve arama işlemleri için kullanıcı dostu bir menü.
*   **Veri Kalıcılığı:** Kütüphanedeki tüm kitap verileri, uygulama kapatılıp açıldığında kaybolmayacak şekilde `library.json` dosyasında saklanır.
*   **Otomatik Veri Zenginleştirme:** Kullanıcıdan sadece kitabın ISBN numarası alınır, kitap başlığı ve yazar bilgileri **Open Library API**'sinden otomatik olarak çekilir.
*   **RESTful API:** Kütüphane verilerine web üzerinden erişim sağlayan, FastAPI ile geliştirilmiş modern bir API.
    *   `GET /books`: Tüm kitapları listeler.
    *   `POST /books`: ISBN ile yeni bir kitap ekler.
    *   `DELETE /books/{isbn}`: Belirli bir kitabı siler.
*   **Otomatik API Dokümantasyonu:** FastAPI'nin sunduğu Swagger UI (`/docs`) ile interaktif ve her zaman güncel bir API dokümantasyonu.
*   **Kapsamlı Testler:** Projenin tüm fonksiyonları ve API endpoint'leri, %100 başarılı olan 12 adet otomatik test ile `pytest` ve `pytest-mock` kullanılarak güvence altına alınmıştır.

## Kullanılan Teknolojiler

*   **Dil:** Python 3
*   **Web Framework:** FastAPI
*   **Veri Yönetimi:** Pydantic (Veri doğrulama için)
*   **Web Sunucusu:** Uvicorn
*   **HTTP İstemcisi:** httpx
*   **Test:** pytest, pytest-mock
*   **Versiyon Kontrolü:** Git & GitHub

## Tasarım Tercihleri ve Teknik Gerekçeler

Bu projede, belirli sorunları çözmek ve modern geliştirme pratiklerini uygulamak için bilinçli teknoloji ve desen tercihleri yapılmıştır.

*   **Neden `conftest.py`?**
    > **Sorun:** Testlerimizin (`test_stage1.py`, `test_stage2.py` vb.) birçoğunun, her testten önce temiz bir `Library` nesnesi oluşturması gerekiyordu. Bu hazırlık kodunu her test dosyasına kopyalamak, kod tekrarına yol açacak ve bakımı zorlaştıracaktı (DRY - Don't Repeat Yourself prensibinin ihlali).
    > **Çözüm:** `pytest`'in sihirli dosyası olan `conftest.py`'yi kullandık. Bu dosyada tanımlanan `fixture`'lar (`temp_library` gibi), `tests/` klasöründeki tüm test dosyaları tarafından otomatik olarak tanınır ve paylaşılır. Bu sayede, test hazırlık kodumuzu merkezi, yeniden kullanılabilir ve temiz bir yapıda tuttuk.

*   **Neden `pytest.ini`?**
    > **Sorun:** `pytest` komutu, `tests/` klasörünün içindeki bir test dosyasını çalıştırdığında, bu test dosyası bir üst dizindeki `library.py` modülünü bulamadığı için `ModuleNotFoundError` hatası alıyorduk.
    > **Çözüm:** Projenin kök dizinine, `pythonpath = .` direktifini içeren bir `pytest.ini` dosyası ekledik. Bu, `pytest`'e testleri çalıştırmadan önce projenin kök dizinini (`.`) Python'un modül arama yoluna eklemesini söyler. Bu sayede testlerimiz, projenin neresinde olurlarsa olsunlar, `library` gibi ana modüllere sorunsuzca erişebilirler.

*   **Neden Mocking (`pytest-mock`)?**
    > **Sorun:** API entegrasyonunu test ederken, testlerimizin her seferinde gerçek Open Library API'sine bağlanmasını istemedik. Bu, testleri yavaşlatır, internet bağlantısına bağımlı hale getirir ve dış servisin anlık durumuna göre başarısız olmalarına neden olabilirdi.
    > **Çözüm:** `pytest-mock` kütüphanesi ile `httpx.get` fonksiyonunu "taklit ettik" (mocking). Test sırasında gerçek bir ağ isteği yapmak yerine, fonksiyonun bizim önceden tanımladığımız sahte bir cevabı (başarılı veya hatalı) anında döndürmesini sağladık. Bu, testlerimizi hızlı, güvenilir ve tekrarlanabilir hale getirdi.

*   **Neden FastAPI ve Pydantic?**
    > **Sorun:** Kütüphane mantığımızı bir web servisi olarak sunarken, gelen isteklerin doğru formatta olduğundan emin olmalı ve API'nin nasıl kullanılacağını açıkça belgelemeliydik.
    > **Çözüm:** Yüksek performansı, modern yapısı ve harika geliştirici deneyimi için FastAPI'yi tercih ettik. Pydantic modelleri (`BookModel`, `ISBNModel`) kullanarak API'mizin beklediği veri yapılarını katı bir şekilde tanımladık. FastAPI, bu modelleri kullanarak otomatik olarak gelen verileri doğrular, hatalı istekleri reddeder ve en önemlisi `/docs` altında interaktif bir API dokümantasyonu oluşturur. Bu, daha az kodla daha güvenli ve daha iyi belgelenmiş bir API yazmamızı sağladı.

## Kurulum

Projeyi yerel makinenizde çalıştırmak için aşağıdaki adımları izleyin.

1.  **Projeyi Klonlayın:**
    ```bash
    git clone https://github.com/serayustun/Python202-GlobalAIHub.git
    cd Python202-GlobalAIHub
    ```

2.  **Sanal Ortam (Virtual Environment) Oluşturun ve Aktive Edin:**
    Bu, proje bağımlılıklarını sisteminizden izole etmek için önemlidir.
    ```bash
    # Sanal ortamı oluştur
    python -m venv venv

    # Sanal ortamı aktive et
    # Windows için:
    .\venv\Scripts\activate
    # macOS/Linux için:
    source venv/bin/activate
    ```

3.  **Gerekli Paketleri Kurun:**
    Projenin tüm bağımlılıkları `requirements.txt` dosyasında listelenmiştir.
    ```bash
    pip install -r requirements.txt
    ```

## Kullanım

Projenin iki farklı kullanım modu vardır:

### 1. Komut Satırı Uygulaması (CLI)

Kütüphaneyi terminal üzerinden yönetmek için aşağıdaki komutu çalıştırın:
```bash
python main.py
```
Karşınıza çıkan menüden istediğiniz işlemi seçebilirsiniz.

### 2. FastAPI Web API Sunucusu

Web servisini başlatmak için aşağıdaki komutu çalıştırın:
```bash
uvicorn api:app --reload
```
Bu komut, geliştirme modunda bir web sunucusu başlatacaktır. Sunucu çalışırken:
*   API'nin ana sayfasına `http://127.0.0.1:8000` adresinden erişebilirsiniz.
*   **İnteraktif API dokümantasyonuna** `http://127.0.0.1:8000/docs` adresinden erişebilir ve tüm endpoint'leri canlı olarak test edebilirsiniz.

## API Dokümantasyonu

Oluşturulan API aşağıdaki endpoint'lere sahiptir:

### `GET /books`
Kütüphanedeki tüm kitapların bir listesini JSON formatında döndürür.

### `POST /books`
Yeni bir kitap ekler. Gövdede (body) verilen ISBN numarasını kullanarak Open Library'den kitap bilgilerini çeker ve kütüphaneye kaydeder.

*   **Request Body Örneği:**
    ```json
    {
      "isbn": "9780451524935"
    }
    ```
*   **Başarılı Cevap (201 Created):** Eklenen kitabın bilgilerini içeren JSON nesnesi.
*   **Hatalı Cevap (404 Not Found):** Verilen ISBN ile kitap bulunamazsa.

### `DELETE /books/{isbn}`
URL'de belirtilen ISBN'e sahip kitabı kütüphaneden siler.

*   **Başarılı Cevap (200 OK):** Silme işlemini onaylayan bir mesaj.
*   **Hatalı Cevap (404 Not Found):** Silinecek kitap bulunamazsa.

## Testler

Projenin tüm işlevselliğini kapsayan otomatik testleri çalıştırmak için projenin ana dizininde aşağıdaki komutu çalıştırın:
```bash
pytest
```
Tüm 12 testin de başarıyla geçtiğini göreceksiniz.

## Proje Dosya Yapısı

```
├── tests/
│   ├── conftest.py         # Paylaşılan Pytest fixture'ları
│   ├── test_stage1.py      # OOP ve dosya işlemleri testleri
│   ├── test_stage2.py      # Harici API entegrasyonu testleri
│   └── test_stage3.py      # FastAPI endpoint testleri
├── library.py              # Book ve Library sınıfları (Uygulamanın beyni)
├── main.py                 # Komut satırı arayüzü
├── api.py                  # FastAPI uygulaması ve endpoint'ler
├── library.json            # Kitap verilerinin saklandığı dosya
├── pytest.ini              # Pytest yapılandırma dosyası
├── requirements.txt        # Proje bağımlılıkları
└── README.md               # Bu dosya
```
