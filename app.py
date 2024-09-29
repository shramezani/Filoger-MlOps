from flask import Flask, request, render_template, redirect, session
import sqlite3
import os

app = Flask(__name__)

@app.route('/')
def index():
    return redirect('/login')  # هدایت کاربر به صفحه ورود


# تابع ایجاد پایگاه‌داده SQLite
def create_db():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    # ایجاد جدول کاربران
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE,
        password TEXT,
        email TEXT
    )
    ''')

    # ایجاد جدول پیش‌بینی‌ها
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS predictions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        input_data TEXT,
        prediction_result TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY(user_id) REFERENCES users(id)
    )
    ''')

    conn.commit()
    conn.close()


# اجرای تابع ایجاد پایگاه داده در زمان شروع برنامه
create_db()


# مسیر ورود به سیستم
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM users WHERE username=? AND password=?', (username, password))
        user = cursor.fetchone()
        conn.close()

        if user:
            session['user_id'] = user[0]
            return redirect('/history')
        else:
            return 'نام کاربری یا رمز عبور اشتباه است'

    return render_template('login.html')


# مسیر ارسال داده‌ها و پیش‌بینی
@app.route('/submit', methods=['GET', 'POST'])
def submit_prediction():
    if request.method == 'POST':
        input_data = request.form['input_data']
        prediction_result = "Positive"  # فرضی برای مثال

        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        cursor.execute('INSERT INTO predictions (user_id, input_data, prediction_result) VALUES (?, ?, ?)',
                       (session['user_id'], input_data, prediction_result))
        conn.commit()
        conn.close()

        return 'پیش‌بینی ثبت شد'

    return render_template('submit.html')


# مسیر نمایش تاریخچه پیش‌بینی‌ها
@app.route('/history')
def history():
    user_id = session.get('user_id')

    if not user_id:
        return redirect('/login')

    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('SELECT input_data, prediction_result, created_at FROM predictions WHERE user_id=?', (user_id,))
    predictions = cursor.fetchall()
    conn.close()

    return render_template('history.html', predictions=predictions)


if __name__ == '__main__':
    app.run(debug=True)
