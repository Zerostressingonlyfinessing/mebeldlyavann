
from flask import Flask, render_template
from models import init_db, get_message

app = Flask(__name__)

@app.route('/')
def index():
    message = get_message()
    return render_template('index.html', message=message)

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
