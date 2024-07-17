from flask import Flask, render_template, session, redirect, url_for, request, jsonify, flash, send_file
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy import create_engine

app = Flask(__name__)

app.config['SECRET_KEY'] = 'my_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///userPasswd.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)  # hash password


def login_1(username, password):
    user = User.query.filter_by(username=username).first()
    if user:
        print(user.password, password)
        print(check_password_hash(user.password, password))
        if check_password_hash(user.password, password):
            return True
        else:
            return False


@app.route('/login', methods=['GET', 'POST'])
def login():
    return render_template('login.html')


@app.route('/upload', methods=['GET', 'POST'])
def upload():
    return render_template('upload.html', username=session['username'])


@app.route('/')
def root():
    return redirect(url_for('login'))


@app.route('/captcha', methods=['GET', 'POST'])
def captcha():
    return send_file("static/image/captcha1.jpg", mimetype='image/jpeg')


@app.route('/login_cert', methods=['GET', 'POST'])
def login_check():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        login_result = login_1(username, password)
        if login_result:
            session['username'] = username
            flash('Login successful')
            return redirect(url_for('upload'))
        else:
            flash('Invalid username or password')
            return redirect(url_for('login'))
        captchaName = request.form.get('captchaName')
        # if captchaName != 'panda':
        #     flash('Invalid captcha')
        #     return redirect(url_for('login'))


def add_user(username, password):
    is_exist = User.query.filter_by(username=username).first()
    if is_exist:
        print( "User already exists")
    else:
        new_user = User(username=username, password=generate_password_hash(password))
        print(f"user add successfully,name={username},password={new_user.password}")
        db.session.add(new_user)
        db.session.commit()


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        add_user('admin', '123')
    app.run(debug=True)
