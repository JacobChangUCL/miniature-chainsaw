from flask import Flask, render_template, redirect, url_for, request, jsonify, flash, send_file
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine

app = Flask(__name__)

app.config['SECRET_KEY'] = 'my_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///userPasswd.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.String(20), nullable=False)


def login_1(username, password):
    user = User.query.filter_by(username=username).first()
    if user:
        if user.password == password:
            return "Login successful"
        else:
            return "Invalid password"
    else:
        return "User not found"


# engine = create_engine('sqlite:///hospital.db', connect_args={'multi': True})
#
# class User:
#     def __init__(self, username, password):
#         self.username = username
#         self.password = password

def print_all_users():
    try:
        users = User.query.all()
        print("Current users in the database:")
        for user in users:
            print(f"Username: {user.username}, Password: {user.password}")
            print('finished')
    except Exception as e:
        print(f"Error accessing the database: {e}")


@app.route('/login', methods=['GET', 'POST'])
def login():
    return render_template('login.html')

@app.route('/upload', methods=['GET', 'POST'])
def upload():
    return render_template('upload.html')

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
        captchaName = request.form.get('captchaName')
        if captchaName != 'panda':
            flash('Invalid captcha')
            return redirect(url_for('login'))
        result = login_1(username, password)
        if result == "Login successful":
            flash('Login successful')
            return redirect(url_for('upload'))
        else:
            flash('Invalid username or password')
            return redirect(url_for('login'))


def add_user(username, password):
    is_exist = User.query.filter_by(username=username).first()
    if is_exist:
        return "User already exists"
    else:
        new_user = User(username=username, password=password)
        db.session.add(new_user)
        db.session.commit()


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        add_user('admin', '123')
        print("User added successfully")
    app.run(debug=True)
