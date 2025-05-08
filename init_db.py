import sqlite3
import os

def init_db():
    """Khởi tạo cấu trúc database nếu chưa tồn tại"""
    conn = sqlite3.connect('notes.db')
    cursor = conn.cursor()
    
    # Bảng ghi chú (notes)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS notes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            content TEXT,
            created_at TEXT NOT NULL
        )
    ''')
    
    # Bảng danh mục (categories) - phân loại ghi chú
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS categories (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE NOT NULL
        )
    ''')
    
    # Bảng liên kết ghi chú và danh mục (note_categories) - quan hệ nhiều-nhiều
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS note_categories (
            note_id INTEGER,
            category_id INTEGER,
            FOREIGN KEY (note_id) REFERENCES notes(id) ON DELETE CASCADE,
            FOREIGN KEY (category_id) REFERENCES categories(id) ON DELETE CASCADE,
            PRIMARY KEY (note_id, category_id)
        )
    ''')
    
    # Bảng tags (thẻ) - gắn nhãn cho ghi chú
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS tags (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE NOT NULL
        )
    ''')
    
    # Bảng liên kết ghi chú và tags (note_tags) - quan hệ nhiều-nhiều
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS note_tags (
            note_id INTEGER,
            tag_id INTEGER,
            FOREIGN KEY (note_id) REFERENCES notes(id) ON DELETE CASCADE,
            FOREIGN KEY (tag_id) REFERENCES tags(id) ON DELETE CASCADE,
            PRIMARY KEY (note_id, tag_id)
        )
    ''')

    conn.commit()
    conn.close()

def add_sample_data():
    """Thêm dữ liệu mẫu nếu database trống"""
    conn = sqlite3.connect('notes.db')
    cursor = conn.cursor()
    
    # Kiểm tra xem đã có dữ liệu chưa
    cursor.execute("SELECT COUNT(*) FROM notes")
    note_count = cursor.fetchone()[0]
    
    if note_count == 0:  # Chỉ thêm dữ liệu nếu không có ghi chú nào
        # Thêm dữ liệu mẫu
        sample_notes = [
            ('Ghi chú quan trọng', 'Họp nhóm lúc 14:00 ngày mai.', '2025-05-07 09:00:00'),
            ('Ý tưởng mới', 'Nghiên cứu về AI cho dự án.', '2025-05-07 10:30:00'),
            ('Danh sách mua sắm', 'Sữa, bánh mì, trứng.', '2025-05-07 12:15:00')
        ]
        cursor.executemany('INSERT INTO notes (title, content, created_at) VALUES (?, ?, ?)', sample_notes)
        
        sample_categories = [
            ('Công việc',),
            ('Cá nhân',),
            ('Dự án',),
        ]
        cursor.executemany('INSERT INTO categories (name) VALUES (?)', sample_categories)
        
        sample_tags = [
            ('Quan trọng',),
            ('Gấp',),
            ('Ý tưởng',),
        ]
        cursor.executemany('INSERT INTO tags (name) VALUES (?)', sample_tags)
        
        # Ví dụ về liên kết ghi chú và danh mục
        cursor.execute('INSERT INTO note_categories (note_id, category_id) VALUES (?, ?)', (1, 1)) # Ghi chú 1 thuộc danh mục Công việc
        cursor.execute('INSERT INTO note_categories (note_id, category_id) VALUES (?, ?)', (2, 3)) # Ghi chú 2 thuộc danh mục Dự án
        cursor.execute('INSERT INTO note_categories (note_id, category_id) VALUES (?, ?)', (3, 2)) # Ghi chú 3 thuộc danh mục Cá nhân
        
        # Ví dụ về liên kết ghi chú và tags
        cursor.execute('INSERT INTO note_tags (note_id, tag_id) VALUES (?, ?)', (1, 1)) # Ghi chú 1 có tag Quan trọng
        cursor.execute('INSERT INTO note_tags (note_id, tag_id) VALUES (?, ?)', (1, 2)) # Ghi chú 1 có tag Gấp
        cursor.execute('INSERT INTO note_tags (note_id, tag_id) VALUES (?, ?)', (2, 3)) # Ghi chú 2 có tag Ý tưởng
        
        print("Đã thêm dữ liệu mẫu vào database!")
    else:
        print("Database đã có dữ liệu, không thêm dữ liệu mẫu.")

    conn.commit()
    conn.close()

def setup_database():
    """Thiết lập database: tạo cấu trúc và thêm dữ liệu mẫu nếu cần"""
    # Kiểm tra xem database đã tồn tại chưa
    db_exists = os.path.exists('notes.db')
    
    # Khởi tạo cấu trúc database
    init_db()
    
    # Nếu database mới được tạo, thêm dữ liệu mẫu
    if not db_exists:
        add_sample_data()
        print("Cơ sở dữ liệu mới đã được khởi tạo thành công!")
    else:
        print("Cơ sở dữ liệu đã tồn tại, chỉ cập nhật cấu trúc nếu cần.")

if __name__ == '__main__':
    setup_database()