import sqlite3
from database import connect
from utils import get_int_input

def add_user():
    name = input("Kullanıcı Adı: ")
    conn = connect()
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO users (name) VALUES (?)", (name,))
        conn.commit()
        print(f" '{name}' sisteme başarıyla eklendi!")
    except sqlite3.IntegrityError:
        print(" Bu kullanıcı zaten mevcut.")
    finally:
        conn.close()

def add_book():
    title = input("Kitap Adı: ")
    category = input("Kategorisi: ")
    author = input("Yazarı: ")
    
    conn = connect()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO books (title, category, author) VALUES (?, ?, ?)", (title, category, author))
    conn.commit()
    print(f" '{title}' kütüphaneye eklendi!")
    conn.close()

def search_book():
    keyword = input("Aramak istediğiniz kitabın adı: ")
    conn = connect()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM books WHERE title LIKE ?", (f'%{keyword}%',))
    results = cursor.fetchall()
    conn.close()
    
    if results:
        print("\n Arama Sonuçları:")
        for row in results:
            print(f"ID: {row[0]} | Kitap: {row[1]} | Kategori: {row[2]} | Yazar: {row[3]}")
    else:
        print(" Eşleşen kitap bulunamadı.")

def read_a_book():
    user_id = get_int_input("Kullanıcı ID'niz: ")
    book_id = get_int_input("Okuduğunuz Kitap ID'si: ")
    rating = get_int_input("Kitaba puanınız (1-10): ")
    
    conn = connect()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO reads (user_id, book_id, rating) VALUES (?, ?, ?)", (user_id, book_id, rating))
    conn.commit()
    print(" Okuma geçmişine kaydedildi!")
    conn.close()

def user_profile_analysis():
    user_id = get_int_input("Profilini görmek istediğiniz Kullanıcı ID: ")
    
    conn = connect()
    cursor = conn.cursor()
    
    cursor.execute("SELECT COUNT(*) FROM reads WHERE user_id = ?", (user_id,))
    total_reads = cursor.fetchone()[0]
    
    if total_reads == 0:
        print(" Bu kullanıcının okuma geçmişi yok.")
        conn.close()
        return
        
    cursor.execute("""
    SELECT books.category, COUNT(*) 
    FROM reads
    JOIN books ON books.id = reads.book_id
    WHERE reads.user_id = ?
    GROUP BY books.category
    """, (user_id,))
    
    categories = cursor.fetchall()
    
    cursor.execute("SELECT name FROM users WHERE id = ?", (user_id,))
    user_row = cursor.fetchone()
    user_name = user_row[0] if user_row else "Bilinmeyen Kullanıcı"
    
    print(f"\n --- {user_name} PROFİL ANALİZİ ---")
    print(f"Toplam Okunan Kitap: {total_reads}")
    for cat in categories:
        category_name = cat[0]
        read_count = cat[1]
        percentage = (read_count / total_reads) * 100
        print(f" {category_name}: %{percentage:.1f} ({read_count} kitap)")
        
    conn.close()

def top_statistics():
    conn = connect()
    cursor = conn.cursor()
    print("\n KÜTÜPHANE İSTATİSTİKLERİ ")
    
    cursor.execute("""
    SELECT books.title, COUNT(*) as okunma_sayisi
    FROM reads
    JOIN books ON reads.book_id = books.id
    GROUP BY book_id
    ORDER BY okunma_sayisi DESC
    LIMIT 1
    """)
    top_read = cursor.fetchone()
    if top_read:
        print(f" En Çok Okunan Kitap: {top_read[0]} ({top_read[1]} kez okundu)")
        
    cursor.execute("""
    SELECT books.title, AVG(reads.rating) as ortalama_puan
    FROM reads
    JOIN books ON reads.book_id = books.id
    GROUP BY book_id
    ORDER BY ortalama_puan DESC
    LIMIT 1
    """)
    top_rated = cursor.fetchone()
    if top_rated:
        print(f" En Yüksek Puanlı Kitap: {top_rated[0]} ({top_rated[1]:.1f} Puan)")
        
    conn.close()