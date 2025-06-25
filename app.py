from flask import Flask, render_template, request, redirect, url_for
import sqlite3
import os

app = Flask(__name__)
UPLOAD_FOLDER = 'static/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

from models import init_db
init_db()

@app.route('/')
def index():
    category = request.args.get('category')
    conn = sqlite3.connect('database.db')
    cur = conn.cursor()
    if category:
        cur.execute("SELECT * FROM products WHERE category = ?", (category,))
    else:
        cur.execute("SELECT * FROM products")
    products = cur.fetchall()
    conn.close()
    return render_template('index.html', products=products)

@app.route('/product/<int:product_id>')
def product(product_id):
    conn = sqlite3.connect('database.db')
    cur = conn.cursor()
    cur.execute("SELECT * FROM products WHERE id = ?", (product_id,))
    product = cur.fetchone()
    conn.close()
    return render_template('product.html', product=product)

@app.route('/admin', methods=['GET', 'POST'])
def admin():
    if request.method == 'POST':
        title = request.form['title']
        desc = request.form['description']
        category = request.form['category']
        materials = request.form['materials']
        files = request.files.getlist('images')
        image_paths = []

        for file in files:
            path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            file.save(path)
            image_paths.append(path)

        conn = sqlite3.connect('database.db')
        cur = conn.cursor()
        cur.execute("INSERT INTO products (title, description, category, materials, images) VALUES (?, ?, ?, ?, ?)",
                    (title, desc, category, materials, ",".join(image_paths)))
        conn.commit()
        conn.close()

        return redirect(url_for('index'))

    return render_template('admin.html')
