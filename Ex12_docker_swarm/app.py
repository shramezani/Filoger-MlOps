from flask import Flask, render_template, redirect, url_for, request
from register import RegisterForm , PredictionForm

app = Flask(__name__)

app.config['SECRET_KEY'] = 'some-random-text'

@app.route('/')
def home():
  return render_template('home.html')

@app.route('/profile')
def profile():
  return render_template('profile.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
  if request.method == 'POST':
    return redirect(url_for('profile'))
  else:
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
  form = RegisterForm()
  if request.method == 'POST':
    return redirect(url_for('login'))
  else:
    return render_template('register.html', form = form)
  

@app.route('/forgot_password', methods=['GET', 'POST'])
def forgot_password():
  if request.method == 'POST':
    return redirect(url_for('login'))
  else:
    return render_template('forgot_password.html')
  
@app.route('/user_input', methods=['GET', 'POST'])
def user_input():
  if request.method == 'POST':
    return redirect(url_for('result'))
  else:
    return render_template('user_input.html')
  
@app.route('/result')
def result():
  return render_template('result.html')

if __name__ == '__main__':
  app.run(debug=True)