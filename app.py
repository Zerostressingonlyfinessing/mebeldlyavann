from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)

# Config for SQLite
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///furniture.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize DB
db = SQLAlchemy(app)

# Define model for items
class FurnitureItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False)
    category = db.Column(db.String(100), nullable=False)
    material = db.Column(db.String(150), nullable=True)
    description = db.Column(db.Text, nullable=True)
    main_image = db.Column(db.String(300), nullable=False)
    images = db.Column(db.Text, nullable=True)  # comma-separated image paths

# Routes
@app.route('/')
def index():
    category_filter = request.args.get('category')
    if category_filter:
        items = FurnitureItem.query.filter_by(category=category_filter).all()
    else:
        items = FurnitureItem.query.all()
    categories = ['тумба', 'столешница', 'шкаф', 'шкаф над инсталляцией', 'зеркальный шкаф', 'под стиральную машину']
    return render_template('index.html', items=items, categories=categories, selected=category_filter)

@app.route('/item/<int:item_id>')
def item_detail(item_id):
    item = FurnitureItem.query.get_or_404(item_id)
    image_list = item.images.split(',') if item.images else []
    return render_template('item.html', item=item, image_list=image_list)

@app.route('/add', methods=['GET', 'POST'])
def add_item():
    if request.method == 'POST':
        title = request.form['title']
        category = request.form['category']
        material = request.form['material']
        description = request.form['description']
        main_image = request.form['main_image']
        images = request.form['images']

        new_item = FurnitureItem(
            title=title,
            category=category,
            material=material,
            description=description,
            main_image=main_image,
            images=images
        )
        db.session.add(new_item)
        db.session.commit()
        return redirect(url_for('index'))

    categories = ['тумба', 'столешница', 'шкаф', 'шкаф над инсталляцией', 'зеркальный шкаф', 'под стиральную машину']
    return render_template('add.html', categories=categories)

# Run app
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
