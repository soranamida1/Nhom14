import mysql.connector

def get_conn():
    return mysql.connector.connect(host="localhost", user="root", password="", database="news_db")

def get_or_create_source_id(conn, source_name):
    """Lấy ID của nguồn dựa trên tên; nếu chưa có, chèn mới và trả về ID."""
    cur = conn.cursor()
    cur.execute("SELECT id FROM sources WHERE name = %s", (source_name,))
    result = cur.fetchone()
    
    if result:
        source_id = result[0]
    else:
        cur.execute("INSERT INTO sources (name) VALUES (%s)", (source_name,))
        conn.commit()
        source_id = cur.lastrowid
        
    cur.close()
    return source_id

def save_article(title, link, content, source_name,published_date):
    """Lưu bài báo. source_name là TÊN NGUỒN."""
    conn = get_conn()
    
    source_id = get_or_create_source_id(conn, source_name)
    
    if source_id is None:
        conn.close()
        print("Lỗi: Không thể lấy hoặc tạo ID nguồn.")
        return

    cur = conn.cursor()
    
    
    cur.execute("SELECT id FROM articles WHERE link=%s", (link,))
    if not cur.fetchone():
       
        cur.execute("INSERT INTO articles (title, link, content, source_id,published_date) VALUES (%s,%s,%s,%s,%s)",
                    (title, link, content, source_id,published_date)) 
        conn.commit()
        print(title)
        
    cur.close()
    conn.close()

    

