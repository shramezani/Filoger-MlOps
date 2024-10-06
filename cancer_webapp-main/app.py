from flask import Flask, render_template, redirect, url_for, request, flash , session , jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
import secrets 
import random
import os
from sqlalchemy import String , Integer , DATETIME , func
from sqlalchemy.orm import Mapped , mapped_column 
from datetime import datetime
from register import RegisterForm
#from dotenv import load_dotenv
#load_dotenv()



app = Flask(__name__)


# Session Configuration for Security
app.config['SESSION_COOKIE_SECURE'] = False  # Set to True in production
app.config['SESSION_COOKIE_HTTPONLY'] = True  # Prevents JavaScript access to cookies
app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'  # Prevents CSRF
#database config
app.config["SQLALCHEMY_DATABASE_URI"]= "sqlite:///example.sqlite"
# secret_key to manage cookie,password for security
##app.config['SECRET_KEY']= secrets.token_hex(32)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY',"$12345$") 
#initilize database
db = SQLAlchemy(app)
#make more safe
bcrypt = Bcrypt(app)

FIXED_VERIFICATION_CODE = "123456"



# Define User model
class User(db.Model):
    __tablename__ = 'user'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    username = mapped_column(String(32), unique=True, nullable=False)
    email = mapped_column(String(64), unique=True, nullable=False)
    password = mapped_column(String(128), unique=False, nullable=False)  # Increased length for bcrypt
    date: Mapped[DATETIME] = mapped_column(DATETIME, default=func.now())
    
    def __repr__(self):
        return f"user {self.id} : {self.username} - {self.email} - {self.date}"


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if request.method == "POST":
        print('Register POST method hit')
        if form.validate_on_submit():
            print('form is valid')
            try:
                register_form_username = form.username.data
                register_form_email = form.email.data
                register_form_password = form.password.data
                register_form_confirm_password = form.confirm_password.data

                # Check if the email already exists
                existing_user = User.query.filter_by(email=register_form_email).first()
                if existing_user:
                    print("user exist")
                    flash('This email already exists, please log in.', "warning")
                    return redirect(url_for("login"))

                # Check verification code (if applicable)
                entered_code = request.form.get('verification_code')
                sent_code = session.get('verification_code')
                if sent_code is None or entered_code != sent_code:
                    print("sent code has problem")
                    flash('Invalid or no verification code sent.', 'danger')
                    return render_template('register.html', form=form)
                
                if register_form_password != register_form_confirm_password :
                    flash('mismatch','warning')
                    return render_template('register.html', form=form)
                
                print("evrything is ok")
                # Hash the password
                hashed_password = bcrypt.generate_password_hash(register_form_password).decode('utf-8')
                # Add the new user
                new_user = User(username=register_form_username, email=register_form_email, password=hashed_password)
                db.session.add(new_user)
                app.logger.info(f"Adding new user: {new_user}")
                db.session.commit()
                app.logger.info(f"User {new_user.username} committed to database")
                flash(f"Welcome, {new_user.username}!", "success")
                return redirect(url_for("login"))

            except Exception as e:
                app.logger.error(f"Error during registration: {e}")
                flash("An error occurred during registration. Please try again.", "danger")
                return render_template('register.html', form=form)
        else:
            print('Form is not valid:', form.errors)
            # If form validation fails
            flash("Please correct the errors in the form.", "danger")
        
    return render_template('register.html', form=form)




# Route to send verification code
@app.route('/send_code', methods=['POST'])
def send_code():
    try:
        email = request.form.get('email')
        # Handle if the user didn't enter an email
        if not email:
            return jsonify({'status': 'error', 'message': 'Email is required'}), 400

        session['verification_code'] = FIXED_VERIFICATION_CODE
        return jsonify({'status': 'success', 'message': 'Verification code sent successfully'})

    except Exception as e:
        app.logger.error(f"Error in send_code route: {e}")
        return jsonify({'status': 'error', 'message': 'An unexpected error occurred.'}), 500



@app.route('/login' , methods=["GET" , "POST"])
def login():
    if request.method=='POST':
        login_email = request.form.get("email")
        login_password = request.form.get("password")
        login_password_hash = bcrypt.generate_password_hash(login_password).decode('utf-8')
        app.logger.info(f"Login attempt for email: {login_email}")
        exist_user = User.query.filter_by(email=login_email).first()
        
        if exist_user :
            app.logger.info(f"User found: {exist_user.email}")
            print(f"exist_user:{exist_user.password} ----{login_password}---{login_password_hash}")
            if bcrypt.check_password_hash(exist_user.password, login_password):
                print('yes')
                # Successfully logged in, set session for the user
                session['user_id'] = exist_user.id  
                flash("You logged in successfully!", "success")
                return redirect(url_for('Profile'))  
            else:
                print('no')
                flash("Invalid password. Please try again.", "warning")
        else:
            flash("No account found with this email. Please register first.", "warning")
    
    else:
        print("Not a POST request.")
    return render_template('login.html')
        
            
    


@app.route('/forgot_password', methods=['GET', 'POST'])
def forgot_password():
    if request.method=='POST':
        security_answer = request.form.get('securityAnswer')
        new_password = request.form.get('newPassword')
        new_confirm_password = request.form.get('confirmPassword')
        try:
            user = User.query.filter_by(email=security_answer).first()
            print(f"there is a user")
            if user:
                if new_password == new_confirm_password :
                    new_password_hash = bcrypt.generate_password_hash(new_password).decode('utf-8')
                    user.password = new_password_hash
                    db.session.commit()
                    print("Password update successful. Redirecting to login page.")
                    flash("Your password has been updated successfully!", "success")
                    return redirect(url_for('login'))
                else:
                    flash("New passwords do not match.", "danger")
                    print('New passwords do not match')
            else:
                flash("User not found.", "danger")
                print("User not found.")
        
        except Exception as e:
            app.logger.error(f"Error during password reset: {e}")
            flash("An error occurred. Please try again.", "danger")
    print("no post")        
    return render_template('forgot_password.html')        



@app.route('/profile')
def Profile():
    return "User profile page"
'''
@app.route('/input' , methods=['GET', 'POST'])
def input():
    return render_template("input.html")
'''




if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True,use_reloader=False)

