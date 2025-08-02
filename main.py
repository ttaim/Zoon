import sqlite3
from flask import Flask, request, jsonify, send_from_directory
import os

app = Flask(__name__, static_folder='static')

# إنشاء مجلد static إذا لم يكن موجوداً
if not os.path.exists('static'):
    os.makedirs('static')

def init_db():
    conn = sqlite3.connect('products.db')
    cursor = conn.cursor()
    
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS products (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        name_en TEXT,
        price REAL NOT NULL,
        image TEXT,
        info TEXT,
        info_en TEXT,
        availability TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    ''')
    
    conn.commit()
    conn.close()

# Routes للصفحات الرئيسية
@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

@app.route('/admin')
def admin():
    return send_from_directory('.', 'admin.html')

# API endpoints
@app.route('/api/products', methods=['GET'])
def get_products():
    conn = sqlite3.connect('products.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM products')
    products = cursor.fetchall()
    conn.close()
    
    products_list = []
    for product in products:
        products_list.append({
            'id': product[0],
            'name': product[1],
            'name_en': product[2],
            'price': product[3],
            'image': product[4],
            'info': product[5],
            'info_en': product[6],
            'availability': product[7]
        })
    
    return jsonify(products_list)

@app.route('/api/products', methods=['POST'])
def add_product():
    data = request.json
    conn = sqlite3.connect('products.db')
    cursor = conn.cursor()
    
    cursor.execute('''
    INSERT INTO products (name, name_en, price, image, info, info_en, availability)
    VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', (
        data.get('name'),
        data.get('name_en', ''),
        data.get('price'),
        data.get('image'),
        data.get('info'),
        data.get('info_en', ''),
        data.get('availability', 'متوفر')
    ))
    
    conn.commit()
    conn.close()
    return jsonify({'success': True})

@app.route('/api/products/<int:product_id>', methods=['PUT'])
def update_product(product_id):
    data = request.json
    conn = sqlite3.connect('products.db')
    cursor = conn.cursor()
    
    cursor.execute('''
    UPDATE products 
    SET name = ?, name_en = ?, price = ?, image = ?, info = ?, info_en = ?, availability = ?
    WHERE id = ?
    ''', (
        data.get('name'),
        data.get('name_en', ''),
        data.get('price'),
        data.get('image'),
        data.get('info'),
        data.get('info_en', ''),
        data.get('availability', 'متوفر'),
        product_id
    ))
    
    conn.commit()
    conn.close()
    return jsonify({'success': True})

@app.route('/api/products/<int:product_id>', methods=['DELETE'])
def delete_product(product_id):
    conn = sqlite3.connect('products.db')
    cursor = conn.cursor()
    
    cursor.execute('DELETE FROM products WHERE id = ?', (product_id,))
    
    conn.commit()
    conn.close()
    return jsonify({'success': True})

# Serving static files
@app.route('/<path:filename>')
def serve_static(filename):
    return send_from_directory('.', filename)

if __name__ == '__main__':
    init_db()
    app.run(debug=True, port=5000)