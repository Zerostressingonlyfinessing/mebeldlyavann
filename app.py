
from flask import Flask, render_template, request, redirect, url_for, abort
import sqlite3
import os

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.config['PASSWORD'] = 'SECRET123'

if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

DB_NAME = 'database.db'

def init_db():
    with sqlite3.connect(DB_NAME) as conn:
        conn.execute("""CREATE TABLE IF NOT EXISTS items (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            price TEXT,
            description TEXT,
            material TEXT,
            image_main TEXT,
            image_1 TEXT,
            image_2 TEXT,
            image_3 TEXT
        )""")

@app.route('/')
def index():
    with sqlite3.connect(DB_NAME) as conn:
        items = conn.execute('SELECT id, name, image_main FROM items ORDER BY id DESC').fetchall()
    return render_template('index.html', items=[{
        'id': item[0],
        'title': item[1],
        'image': url_for('static', filename=item[2]) if item[2] else ''
    } for item in items])

@app.route('/item/<int:item_id>')
def item(item_id):
    with sqlite3.connect(DB_NAME) as conn:
        item = conn.execute('SELECT * FROM items WHERE id = ?', (item_id,)).fetchone()
    if not item:
        abort(404)
    return render_template('item.html', item={
        'title': item[1],
        'price': item[2],
        'description': item[3],
        'materials': item[4],
        'image': url_for('static', filename=item[5]) if item[5] else '',
        'images': [
            url_for('static', filename=img) for img in [item[6], item[7], item[8]] if img
        ]
    })

@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        if request.form.get('password') != app.config['PASSWORD']:
            return 'Неверный пароль', 403

        name = request.form['title']
        price = request.form['price']
        description = request.form['description']
        material = request.form['materials']

        image_main = request.form['image']
        extra_images = [img.strip() for img in request.form.get('images', '').split(',')]
        image_1 = extra_images[0] if len(extra_images) > 0 else None
        image_2 = extra_images[1] if len(extra_images) > 1 else None
        image_3 = extra_images[2] if len(extra_images) > 2 else None

        with sqlite3.connect(DB_NAME) as conn:
            conn.execute("""INSERT INTO items (name, price, description, material, image_main, image_1, image_2, image_3)
                            VALUES (?, ?, ?, ?, ?, ?, ?, ?)""", 
                         (name, price, description, material, image_main, image_1, image_2, image_3))

        return redirect(url_for('index'))

    return render_template('add.html')

@app.route('/admin', methods=['GET', 'POST'])
def admin():
    if request.method == 'POST':
        if request.form.get('password') != app.config['PASSWORD']:
            return 'Неверный пароль', 403

        with sqlite3.connect(DB_NAME) as conn:
            items = conn.execute('SELECT id, name, image_main FROM items ORDER BY id DESC').fetchall()

        return render_template('admin.html', items=[{
            'id': item[0],
            'title': item[1],
            'image': url_for('static', filename=item[2]) if item[2] else ''
        } for item in items])

    return '''
    <h2>Вход в админку</h2>
    <form method="post">
        Пароль: <input type="password" name="password">
        <input type="submit" value="Войти">
    </form>
    <p><a href="/">← Назад</a></p>
    '''

@app.route('/delete/<int:item_id>', methods=['POST'])
def delete(item_id):
    with sqlite3.connect(DB_NAME) as conn:
        conn.execute('DELETE FROM items WHERE id = ?', (item_id,))
    return redirect(url_for('admin'))

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
