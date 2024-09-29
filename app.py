from flask import Flask, render_template, redirect, url_for, session, request
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SECRET_KEY'] = os.urandom(24)
db = SQLAlchemy(app)
@app.route('/')
def index():
    return redirect('/login')  # هدایت کاربر به صفحه ورود

# مدل کاربر
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), nullable=False, unique=True)
    email = db.Column(db.String(150), nullable=False, unique=True)
    password = db.Column(db.String(150), nullable=False)

# ایجاد پایگاه‌داده
with app.app_context():
    db.create_all()

# مسیر ثبت‌نام
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']

        # هش کردن رمز عبور
        hashed_password = generate_password_hash(password, method='sha256')

        # ذخیره کاربر در پایگاه‌داده
        new_user = User(username=username, email=email, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()

        return redirect(url_for('login'))

    return render_template('register.html')

# مسیر ورود به سیستم
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        user = User.query.filter_by(email=email).first()

        if user and check_password_hash(user.password, password):
            session['user_id'] = user.id
            return redirect(url_for('home'))
        else:
            return 'Invalid email or password'

    return render_template('login.html')

# مسیر صفحه اصلی (پس از ورود)
@app.route('/home')
def home():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    return render_template('home.html')

# خروج از سیستم
@app.route('/logout')
def logout():
    session.pop('user_id', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
