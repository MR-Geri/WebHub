import account_user
from flask import Flask, render_template, url_for, request
from flask_sqlalchemy import SQLAlchemy

from models.users import Users


app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///posts.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)  # Важная для работы базы данных строка
from account_user import login_manager

login_manager.init_app(app)
app.register_blueprint(account_user.blueprint)


def update_class(line: str) -> str:
    if 'style=' in line:
        r_line = line[line.find('style="') + 7:].find('"') + line.find('style="') + 8
        line = line[:line.find('"') - 6] + line[r_line:]
    if 'class=' in line:
        r_line = line[line.find('class="') + 7:].find('"') + line.find('class="') + 8
        line = line[:line.find('"') - 6] + line[r_line:]
    if '<img' in line:
        line = line.replace('<img ', '<img class="rounded mx-auto d-block mt-3 img-fluid" ')
    return line


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/about')
def about():
    return render_template('about.html')


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8000)
