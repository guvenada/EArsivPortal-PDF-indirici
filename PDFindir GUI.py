"""

 Güven ADA tarafından E-arşiv portal sisteminden pdf dosyalarınızı indirmenize yarayan bir
araç olarak yazılmış ve iş yükünü büyük ölçüde azaltması hedeflenmiştir. Bu aracın kullanımında oluşan herhangi bir durumdan
tamamen siz sorumlusunuzdur, sorumluluk kabul etmemekteyim. Arayüz tasarımıyla birlikte güzel bir çalışma oldu.
Piyasadaki tek opensource proje olmasıyla birlikte bir eksikliği gidermektedir. İletişim için LinkedIn @guvenada hesabımdan ulaşabilirsiniz.

"""

import tkinter as tk
from tkinter import messagebox
import requests
import json
import os
import zipfile
import pdfkit
from tkinter import ttk
from tkcalendar import DateEntry
from PyPDF2 import PdfReader, PdfWriter

# PDF klasörünün var olup olmadığını kontrol et, yoksa oluştur
if not os.path.exists('pdfler'):
    os.makedirs('pdfler')

# Kullanıcı adı ve şifre dosyası yolu
credential_file = 'credentials.txt'

# GUI kurulum
root = tk.Tk()
root.title("E-Arşiv Portal PDF Aracı - Güven ADA")
root.configure(bg='#1e1e1e')  # Arka plan rengi siyah
root.geometry('400x300')  # Panel boyutunu ayarla

# Başlangıç ve bitiş tarih seçimi için widget'lar
tk.Label(root, text="Başlangıç Tarihi:", fg='white', bg='#1e1e1e').grid(row=0, column=0, padx=10, pady=10)
start_date_entry = DateEntry(root, width=12, background='darkblue', foreground='white', borderwidth=2)
start_date_entry.grid(row=0, column=1, padx=10, pady=10)

tk.Label(root, text="Bitiş Tarihi:", fg='white', bg='#1e1e1e').grid(row=1, column=0, padx=10, pady=10)
end_date_entry = DateEntry(root, width=12, background='darkblue', foreground='white', borderwidth=2)
end_date_entry.grid(row=1, column=1, padx=10, pady=10)

# Kullanıcı bilgileri girişi
tk.Label(root, text="Kullanıcı adı:", fg='white', bg='#1e1e1e').grid(row=2, column=0, padx=10, pady=10)
userid_entry = tk.Entry(root, bg='gray', fg='white', borderwidth=2)
userid_entry.grid(row=2, column=1, padx=10, pady=10)

tk.Label(root, text="Şifre:", fg='white', bg='#1e1e1e').grid(row=3, column=0, padx=10, pady=10)
sifre_entry = tk.Entry(root, show="*", bg='gray', fg='white', borderwidth=2)
sifre_entry.grid(row=3, column=1, padx=10, pady=10)

# Kaydet butonu işlevi
def save_credentials():
    userid = userid_entry.get()
    sifre = sifre_entry.get()
    
    if not userid or not sifre:
        messagebox.showerror("Hata", "Kullanıcı adı ve şifre boş olamaz!")
        return
    
    try:
        with open(credential_file, 'w') as f:
            f.write(f"{userid}\n{sifre}")
        messagebox.showinfo("Başarılı", "Kullanıcı adı ve şifre kaydedildi!")
    except Exception as e:
        messagebox.showerror("Hata", f"Kullanıcı adı ve şifre kaydedilirken bir hata oluştu: {e}")

# Kaydet butonu
tk.Button(root, text='Kullanıcı Adı ve Şifreyi Kaydet', command=save_credentials, bg='#4CAF50', fg='white').grid(row=4, columnspan=2, pady=10)

# Daha önce kaydedilen kullanıcı adı ve şifre varsa otomatik olarak doldurma işlemi
if os.path.exists(credential_file):
    with open(credential_file, 'r') as f:
        lines = f.readlines()
        if len(lines) == 2:
            saved_userid = lines[0].strip()
            saved_sifre = lines[1].strip()
            userid_entry.insert(0, saved_userid)
            sifre_entry.insert(0, saved_sifre)

# Giriş ve işlem butonu
def login_and_download():
    start_date = start_date_entry.get_date().strftime('%d/%m/%Y')
    end_date = end_date_entry.get_date().strftime('%d/%m/%Y')
    userid = userid_entry.get()
    sifre = sifre_entry.get()
    
    if not start_date or not end_date or not userid or not sifre:
        messagebox.showerror("Hata", "Lütfen tüm alanları doldurun!")
        return
    
    login_data = {
        "assoscmd": "anologin",
        "rtype": "json",
        "userid": userid,
        "sifre": sifre,
        "sifre2": sifre,  # Tek girişli şifre alanı
        "parola": "1"
    }
    
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8',
    }
    
    try:
        login_response = requests.post("https://earsivportal.efatura.gov.tr/earsiv-services/assos-login", data=login_data, headers=headers)
        
        if login_response.status_code != 200:
            messagebox.showerror("Hata", "Giriş başarısız!")
            return
        
        token = login_response.json().get('token')
        if not token:
            messagebox.showerror("Hata", "Token alınamadı!")
            return
        
        dispatch_data = {
            "callid": "",
            "token": token,
            "cmd": "EARSIV_PORTAL_TASLAKLARI_GETIR",
            "pageName": "RG_BASITTASLAKLAR",
            "jp": json.dumps({"baslangic": start_date, "bitis": end_date, "hangiTip": "5000/30000"})
        }
        
        dispatch_response = requests.post("https://earsivportal.efatura.gov.tr/earsiv-services/dispatch", data=dispatch_data, headers=headers)
        
        if dispatch_response.status_code != 200:
            messagebox.showerror("Hata", "Fatura listesi alınamadı!")
            return
        
        invoices = dispatch_response.json().get('data', [])
        
        for invoice in invoices:
            ettn = invoice.get('ettn')
            download_url = f"https://earsivportal.efatura.gov.tr/earsiv-services/download?token={token}&ettn={ettn}&belgeTip=FATURA&onayDurumu=Onaylandı&cmd=EARSIV_PORTAL_BELGE_INDIR&"
            download_response = requests.get(download_url, headers=headers)
            
            if download_response.status_code == 200:
                zip_filename = f"pdfler/{ettn}.zip"
                with open(zip_filename, 'wb') as f:
                    f.write(download_response.content)
                
                with zipfile.ZipFile(zip_filename, 'r') as zip_ref:
                    zip_ref.extractall('pdfler')
                
                os.remove(zip_filename)
        
        # Isim güncelleme ve HTML'leri PDF'ye dönüştürme işlemleri
        for root, _, files in os.walk('pdfler'):
            for file in files:
                if file.endswith('.html'):
                    html_path = os.path.join(root, file)
                    pdf_path = html_path.replace('.html', '.pdf')
                    
                    try:
                        config = pdfkit.configuration(wkhtmltopdf='C:\\Program Files\\wkhtmltopdf\\bin\\wkhtmltopdf.exe') // wkhtmltopdf toolunun calisitirilabilir versiyonunun lokasyonunu belirtiniz
                        pdfkit.from_file(html_path, pdf_path, configuration=config)
                        os.remove(html_path)  # HTML dosyasını sil
                        
                        # PDF isimlerini düzenle
                        find_and_replace_pdf('pdfler')
                        
                    except Exception as e:
                        messagebox.showwarning("Uyarı", f"{ettn} için PDF dönüşümü başarısız: {e}")
        
        # Klasördeki tüm .xml dosyalarını sil
        for root, _, files in os.walk('pdfler'):
            for file in files:
                if file.endswith('.xml'):
                    os.remove(os.path.join(root, file))
        
        messagebox.showinfo("Başarılı", "Faturalar indirildi ve dönüştürüldü!")
    
    except Exception as ex:
        messagebox.showerror("Hata", f"Bir hata oluştu: {ex}")

def find_and_replace_pdf(directory):
    for filename in os.listdir(directory):
        if filename.endswith(".pdf"):
            pdf_path = os.path.join(directory, filename)
            with open(pdf_path, "rb") as file:
                reader = PdfReader(file)
                writer = PdfWriter()

                for page_num in range(len(reader.pages)):
                    page = reader.pages[page_num]
                    text = page.extract_text()

                    if "SAYIN" in text:
                        index = text.index("SAYIN")
                        name_start = text.index("\n", index) + 1
                        name_end = text.index("\n", name_start)
                        name = text[name_start:name_end]

                        # Geçersiz karakterleri temizle
                        new_name = f"{name}.pdf".replace("\n", "").replace("/", "").replace("\\", "")
                        new_name = new_name.replace(" ", "_")  # Boşlukları alt çizgi ile değiştir

                        writer.add_page(page)
                        break

                for page_num in range(page_num + 2, len(reader.pages)):  
                    page = reader.pages[page_num]
                    writer.add_page(page)

            # Pdf okuyucuyu kapat
            file.close()

            # Dosyayı kapat
            reader.stream.close()

            # Yeni dosya adını oluştur
            new_pdf_path = os.path.join(directory, new_name)

            # Dosya adını değiştir
            try:
                os.rename(pdf_path, new_pdf_path)
                print(f"{pdf_path} dosyasının adı düzeltildi: {new_name}")
            except Exception as e:
                print(f"Dosya adı düzeltilirken bir hata oluştu: {e}")

# Giriş ve işlem butonu
tk.Button(root, text='Giriş Yap ve Faturaları İndir', command=login_and_download, bg='#4CAF50', fg='white').grid(row=5, columnspan=2, pady=10)

root.mainloop()
