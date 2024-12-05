# E-Arşiv Portal PDF Aracı - Güven ADA

## Proje Tanımı
Bu araç, **E-Arşiv Portalı** üzerinden PDF formatındaki belgeleri indirmenize ve iş yükünüzü azaltmanıza yardımcı olmak amacıyla geliştirilmiştir. Arayüz, kullanıcı dostu olacak şekilde tasarlanmış ve süreçleri otomatikleştirmiştir. Piyasadaki tek açık kaynaklı proje olmasıyla bir eksikliği gidermektedir.

**Not**: Araç, kullanıcı sorumluluğunda kullanılmalıdır. Oluşabilecek hatalardan yazılım geliştirici sorumlu değildir.

---

## Özellikler

- Başlangıç ve bitiş tarihine göre PDF belgelerini indirme.
- Belgeleri otomatik olarak dönüştürme ve yeniden adlandırma.
- Kullanıcı adı ve şifreyi güvenli şekilde saklama. # Güncel olarak Encryption sistemi yapılmadığı için güvenilir değildir. Güvenlik size aittir!
- Arayüz üzerinden kolay işlem yapma imkanı.

---

## Gerekli Kurulumlar ve Bağımlılıklar

### 1. **Python Gereksinimleri**
Proje Python 3.7+ sürümünde çalışmaktadır. Aşağıdaki modülleri kurmanız gerekmektedir:

```bash
pip install requests
pip install tk
pip install tkcalendar
pip install PyPDF2
pip install pdfkit
```

### 2. **wkhtmltopdf Aracı**
PDF dönüştürme işlemleri için `wkhtmltopdf` aracına ihtiyaç duyulmaktadır.

- [wkhtmltopdf İndir](https://wkhtmltopdf.org/downloads.html) ve bilgisayarınıza kurun.
- Kurulum sonrası, `wkhtmltopdf` aracının **yolu** kod içinde doğru bir şekilde belirtilmelidir:

```python
config = pdfkit.configuration(wkhtmltopdf='C:\\Program Files\\wkhtmltopdf\\bin\\wkhtmltopdf.exe')
```

Bu satırda, `wkhtmltopdf`'in tam yolu doğru olarak ayarlanmalıdır.

---

## Kurulum Adımları

1. **Kod Dosyalarını İndirin**
Projenin tüm kod dosyalarını bir klasöre kopyalayın.

2. **Bağımlılıkları Yükleyin**
Yukarıda belirtilen Python modüllerini yükleyin.

3. **PDF Klasörünü Oluşturun**
Kod, indirdiği PDF dosyalarını `pdfler` klasörüne kaydeder. Eğer bu klasör otomatik olarak oluşturulmazsa, manuel olarak oluşturabilirsiniz.

4. **Kullanıcı Bilgilerini Kaydedin**
- Arayüzde kullanıcı adı ve şifre alanını doldurarak bilgilerinizi kaydedebilirsiniz.
- Kaydedilen bilgiler, **`credentials.txt`** dosyasına güvenli bir şekilde saklanacaktır. # Güncel olarak Encryption sistemi yapılmadığı için güvenilir değildir. Güvenlik size aittir!

---

## Kullanım Talimatları

1. Programı başlatmak için `python PDFindir GUI.py` komutunu çalıştırın.
2. Açılan gui tasarımında:
- İndirmek istediğiniz faturalarınızın **Başlangıç** ve **Bitiş Tarihi**'ni seçin.
- Kullanıcı adı ve şifrenizi girin.
- "Kullanıcı Adı ve Şifreyi Kaydet" butonuyla her seferinde tekrar girmemek adına local sisteminize bilgilerinizi kaydedebilir fakat encryptelenmediği için güvenli değildir.
- "Giriş Yap ve Faturaları İndir" butonunuyla E-arşiv portal hesabınıza giriş yapılacak ve faturalarınızın indirme işlemi tamamlanacak.
3. Belgeleriniz otomatik olarak **`pdfler`** klasörüne kaydedilecektir.

---

## Dosya Yapısı

- `PDFindir GUI.py` : Ana uygulama kodu.
- `credentials.txt` : Kullanıcı bilgilerini saklayan dosya.
- `pdfler/` : İndirilen ve dönüştürülen PDF belgelerinin saklandığı klasör.

---

## Karşılaşılan Sorunlar ve Çözümler

### 1. **wkhtmltopdf Hatası**
- Eğer PDF dönüştürme işlemi sırasında hata alıyorsanız, `wkhtmltopdf` aracının doğru yüklendiğinden ve yolun doğru belirtildiğinden emin olun.

### 2. **Bağlantı veya Giriş Hatası**
- Kullanıcı adı ve şifre bilgilerinizin doğru olduğundan emin olun.
- İnternet bağlantınızı kontrol edin.

### 3. **Eksik Modüller**
- Gerekli modüllerin eksik olması durumunda, yukarıdaki `pip install` komutlarını tekrar çalıştırın.

---

## İletişim
Herhangi bir sorun veya öneri için [LinkedIn @guvenada](https://linkedin.com/in/guvenada) hesabından iletişime geçebilirsiniz.

---

**Bu araç açık kaynaklıdır ve sürekli geliştirme sürecinde olup tüm sorumluluk size aittir. Bu program sizlerin geliştirmesine açıktır.**
