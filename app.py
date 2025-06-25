from flask import Flask, render_template
from models import init_db, get_message

app = Flask(__name__)

# Создаём базу данных при запуске (если её нет)
init_db()

@app.route('/')
def index():
    message = get_message()
    return render_template('index.html', message=message)
