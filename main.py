import os
import subprocess
from database import setup_database
from operations import add_user, add_book, search_book, read_a_book, user_profile_analysis, top_statistics
from recommendation import smart_recommendation

# Program başlarken tabloları kontrol et ve oluştur
setup_database()

while True:
    subprocess.run('cls' if os.name == 'nt' else 'clear', shell=True)
    print("\n" + "="*30)
    print("  AKILLI KÜTÜPHANE SİSTEMİ  ")
    print("="*30)
    print("1- Kullanıcı Ekle")
    print("2- Kitap Ekle")
    print("3- Kitap Ara (LIKE)")
    print("4- Kitap Oku (Puan Ver)")
    print("5-  Akıllı Öneri Al")
    print("6-  Kullanıcı Profili Çıkar")
    print("7-  Kütüphane İstatistikleri (En iyiler)")
    print("8- Çıkış")
    
    secim = input("Seçiminiz (1-8): ")
    
    if secim == '1':
        add_user()
    elif secim == '2':
        add_book()
    elif secim == '3':
        search_book()
    elif secim == '4':
        read_a_book()
    elif secim == '5':
        smart_recommendation()
    elif secim == '6':
        user_profile_analysis()
    elif secim == '7':
        top_statistics()
    elif secim == '8':
        print(" Sistemden çıkılıyor... İyi okumalar!")
        break
    else:
        print(" Geçersiz seçim, lütfen tekrar deneyin.")
        
    # TAM BURAYA EKLİYORSUN (else ile aynı hizada)
    input("\nAna menüye dönmek için Enter'a basın...")