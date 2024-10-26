from flask import Flask, render_template, redirect, url_for, session, request
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Boolean, Float, Integer, String

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///real_estate.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Define User model
class User(db.Model):
    id = db.Column(Integer, primary_key=True)
    username = db.Column(String(80), nullable=False, unique=True)
    email = db.Column(String(120), nullable=False, unique=True)
    password = db.Column(String(120), nullable=False)

# Define Prediction History model
class PredictionHistory(db.Model):
    id = db.Column(Integer, primary_key=True)
    user_id = db.Column(Integer, db.ForeignKey('user.id'), nullable=False)
    area = db.Column(Float, nullable=False)
    rooms = db.Column(Integer, nullable=False)
    parking = db.Column(Boolean, nullable=False)
    warehouse = db.Column(Boolean, nullable=False)
    elevator = db.Column(Boolean, nullable=False)
    address = db.Column(String(255), nullable=False)
    price = db.Column(Float)

    # Relationship to connect user and prediction history
    user = db.relationship('User', backref=db.backref('predictions', lazy=True))

# Initialize the database and create tables
with app.app_context():
    db.create_all()

print("Database and tables created successfully!")


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
