from flask import Flask, jsonify, request
from flask_cors import CORS
import sqlite3
from datetime import datetime
import math  # Thêm thư viện math để tính toán phân trang
from init_db import setup_database # Import setup_database thay vì init_db

app = Flask(__name__)
CORS(app)

# Gọi setup_database() để khởi tạo database khi ứng dụng chạy
with app.app_context():
    setup_database()

# Hàm kết nối cơ sở dữ liệu
def connect_db():
    return sqlite3.connect('notes.db')

# Helper function để thực hiện truy vấn SQL
def execute_query(query, args=()):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute(query, args)
    conn.commit()
    conn.close()
    return cursor

# Helper function để lấy dữ liệu từ truy vấn SQL
def fetch_data(query, args=()):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute(query, args)
    data = cursor.fetchall()
    conn.close()
    return data

# API: Lấy tất cả ghi chú
@app.route('/api/notes', methods=['GET'])
def get_notes():
    page = request.args.get('page', default=1, type=int)
    per_page = request.args.get('per_page', default=10, type=int)
    search_query = request.args.get('search', default='', type=str)
    category_id = request.args.get('category', default=None, type=int)
    tag_id = request.args.get('tag', default=None, type=int)

    query = """
        SELECT DISTINCT n.id, n.title, n.content, n.created_at
        FROM notes n
        LEFT JOIN note_categories nc ON n.id = nc.note_id
        LEFT JOIN note_tags nt ON n.id = nt.note_id
        WHERE (n.title LIKE ? OR n.content LIKE ?)
    """
    args = ('%' + search_query + '%', '%' + search_query + '%')

    if category_id:
        query += " AND nc.category_id = ?"
        args += (category_id,)
    if tag_id:
        query += " AND nt.tag_id = ?"
        args += (tag_id,)

    query += " ORDER BY n.created_at DESC"

    # Tính toán phân trang
    total_items = len(fetch_data(query, args))
    total_pages = math.ceil(total_items / per_page)

    query += " LIMIT ? OFFSET ?"
    args += (per_page, (page - 1) * per_page)
    notes = fetch_data(query, args)
    results = [{'id': n[0], 'title': n[1], 'content': n[2], 'created_at': n[3]} for n in notes]

    return jsonify({
        'items': results,
        'page': page,
        'per_page': per_page,
        'total_items': total_items,
        'total_pages': total_pages
    })

# API: Thêm ghi chú mới
@app.route('/api/notes', methods=['POST'])
def add_note():
    data = request.get_json()
    title = data.get('title')
    content = data.get('content')
    created_at = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    category_ids = data.get('category_ids', [])  # Nhận danh sách category_ids
    tag_ids = data.get('tag_ids', [])  # Nhận danh sách tag_ids

    if not title:
        return jsonify({'error': 'Title is required'}), 400

    query = 'INSERT INTO notes (title, content, created_at) VALUES (?, ?, ?)'
    cursor = execute_query(query, (title, content, created_at))
    new_note_id = cursor.lastrowid

    # Thêm liên kết danh mục
    for category_id in category_ids:
        execute_query('INSERT INTO note_categories (note_id, category_id) VALUES (?, ?)', (new_note_id, category_id))

    # Thêm liên kết tag
    for tag_id in tag_ids:
        execute_query('INSERT INTO note_tags (note_id, tag_id) VALUES (?, ?)', (new_note_id, tag_id))

    return jsonify({'id': new_note_id, 'title': title, 'content': content, 'created_at': created_at}), 201

# API: Sửa ghi chú
@app.route('/api/notes/<int:id>', methods=['PUT'])
def update_note(id):
    data = request.get_json()
    title = data.get('title')
    content = data.get('content')
    category_ids = data.get('category_ids', [])  # Nhận danh sách category_ids
    tag_ids = data.get('tag_ids', [])  # Nhận danh sách tag_ids

    if not title:
        return jsonify({'error': 'Title is required'}), 400

    query = 'UPDATE notes SET title = ?, content = ? WHERE id = ?'
    cursor = execute_query(query, (title, content, id))
    if cursor.rowcount == 0:
        return jsonify({'error': 'Note not found'}), 404

    # Cập nhật liên kết danh mục (xóa cũ, thêm mới)
    execute_query('DELETE FROM note_categories WHERE note_id = ?', (id,))
    for category_id in category_ids:
        execute_query('INSERT INTO note_categories (note_id, category_id) VALUES (?, ?)', (id, category_id))

    # Cập nhật liên kết tag (xóa cũ, thêm mới)
    execute_query('DELETE FROM note_tags WHERE note_id = ?', (id,))
    for tag_id in tag_ids:
        execute_query('INSERT INTO note_tags (note_id, tag_id) VALUES (?, ?)', (id, tag_id))

    return jsonify({'id': id, 'title': title, 'content': content})

# API: Xóa ghi chú
@app.route('/api/notes/<int:id>', methods=['DELETE'])
def delete_note(id):
    query = 'DELETE FROM notes WHERE id = ?'
    cursor = execute_query(query, (id,))
    if cursor.rowcount == 0:
        return jsonify({'error': 'Note not found'}), 404
    return jsonify({'message': 'Note deleted'})

# API: Lấy tất cả danh mục
@app.route('/api/categories', methods=['GET'])
def get_categories():
    categories = fetch_data('SELECT * FROM categories')
    return jsonify([{'id': c[0], 'name': c[1]} for c in categories])

# API: Thêm danh mục mới
@app.route('/api/categories', methods=['POST'])
def add_category():
    data = request.get_json()
    name = data.get('name')
    if not name:
        return jsonify({'error': 'Category name is required'}), 400
    try:
        cursor = execute_query('INSERT INTO categories (name) VALUES (?)', (name,))
        new_category_id = cursor.lastrowid
        return jsonify({'id': new_category_id, 'name': name}), 201
    except sqlite3.IntegrityError:
        return jsonify({'error': 'Category name already exists'}), 400

# API: Lấy tất cả tags
@app.route('/api/tags', methods=['GET'])
def get_tags():
    tags = fetch_data('SELECT * FROM tags')
    return jsonify([{'id': t[0], 'name': t[1]} for t in tags])

# API: Thêm tag mới
@app.route('/api/tags', methods=['POST'])
def add_tag():
    data = request.get_json()
    name = data.get('name')
    if not name:
        return jsonify({'error': 'Tag name is required'}), 400
    try:
        cursor = execute_query('INSERT INTO tags (name) VALUES (?)', (name,))
        new_tag_id = cursor.lastrowid
        return jsonify({'id': new_tag_id, 'name': name}), 201
    except sqlite3.IntegrityError:
        return jsonify({'error': 'Tag name already exists'}), 400

if __name__ == '__main__':
    app.run(debug=True)