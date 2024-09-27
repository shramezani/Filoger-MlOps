from flask import Flask, render_template, request, redirect, url_for, flash, session

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        pass
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        pass

    return render_template('login.html')

@app.route('/user_input', methods=['GET', 'POST'])
def user_input():
    if request.method == 'POST':
        pass

    return render_template('user_input.html')

@app.route('/result')
def result():
    return render_template('result.html')

@app.route('/history')
def history():
    return render_template('history.html')

if __name__ == '__main__':
    app.run(debug=True)
