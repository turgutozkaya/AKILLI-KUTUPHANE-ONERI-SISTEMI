from database import connect
from utils import get_int_input

def smart_recommendation():
    user_id = get_int_input("Öneri almak isteyen Kullanıcı ID: ")
    
    conn = connect()
    cursor = conn.cursor()
    
    cursor.execute("""
    SELECT books.category, COUNT(*) as total
    FROM reads
    JOIN books ON books.id = reads.book_id
    WHERE reads.user_id = ?
    GROUP BY books.category
    ORDER BY total DESC
    LIMIT 1
    """, (user_id,))
    
    fav_category_row = cursor.fetchone()
    
    if not fav_category_row:
        print(" Henüz hiç kitap okumamışsınız. Size rastgele bir kitap öneremem, önce bir şeyler okuyun!")
        conn.close()
        return
        
    fav_category = fav_category_row[0]
    print(f"\n Analiz: En çok '{fav_category}' kategorisini okuyorsunuz.")
    
    # KULLANICININ OKUMADIĞI kitapları önerir
    cursor.execute("""
    SELECT title, author FROM books
    WHERE category = ? AND id NOT IN (
        SELECT book_id FROM reads WHERE user_id = ?
    )
    LIMIT 3
    """, (fav_category, user_id))
    
    recommendations = cursor.fetchall()
    
    if recommendations:
        print(" Size Özel Kitap Önerilerimiz:")
        for rec in recommendations:
            print(f" {rec[0]} (Yazar: {rec[1]})")
    else:
        print(" Vay canına! Bu kategorideki tüm kitaplarımızı okumuşsunuz.")
        
    conn.close()