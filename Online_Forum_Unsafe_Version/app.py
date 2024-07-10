from flask import Flask, render_template, session,redirect, url_for, request, jsonify, flash, send_file
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
    """
    check if the username and password are correct
    """
    query = db.text(
        f"SELECT * FROM User WHERE username = '{username}' AND password = '{password}'"
    )
    user = db.session.execute(query).fetchone()
    print(user)
    if user:
        return True
    else:
        return False


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

@app.route('/')
def root():
    return redirect(url_for('login'))

@app.route('/upload', methods=['GET', 'POST'])
def upload():
    return render_template('upload.html',username=session['username'])


@app.route('/login_cert', methods=['GET', 'POST'])
def login_check():
    """
    check the correctness of the username and password,then return the result
    """
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
