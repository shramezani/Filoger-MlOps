from flask import Flask, render_template, redirect, url_for, request, flash , session , jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
import secrets 
import random
import os
from sqlalchemy import String , Integer , DATETIME , func , ForeignKey
from sqlalchemy.orm import Mapped , mapped_column , relationship
from datetime import datetime
from register import RegisterForm , PredictionForm
#from dotenv import load_dotenv
#load_dotenv()
from functools import wraps
from ML.predict import predict_cancer
import numpy as np
from typing import List



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
    # Establish relationship with PredictionHistory
    predictions: Mapped[List['PredictionHistory']] = relationship(back_populates='user')

    def __repr__(self):
        return f"user {self.id} : {self.username} - {self.email} - {self.date}"

# Define store database
class PredictionHistory(db.Model):
    __tablename__ = 'prediction_history'
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey('user.id'), nullable=False)
    worst_area: Mapped[str] = mapped_column(String(50), nullable=False)
    worst_concave_points: Mapped[str] = mapped_column(String(50), nullable=False)
    mean_concave_points: Mapped[str] = mapped_column(String(50), nullable=False)
    worst_radius: Mapped[str] = mapped_column(String(50), nullable=False)
    mean_concavity: Mapped[str] = mapped_column(String(50), nullable=False)
    prediction: Mapped[str] = mapped_column(String(20), nullable=False)
    explanation: Mapped[str] = mapped_column(String(500), nullable=False)
    timestamp: Mapped[DATETIME] = mapped_column(DATETIME, default=func.now())
    # Establish relationship with User
    user: Mapped['User'] = relationship(back_populates='predictions')

    def __repr__(self):
        return f"<PredictionHistory {self.id} - User {self.user_id} - {self.prediction}>"




def login_required(f):
    @wraps(f)
    def decorator_function(*args,**kwargs):
        if 'user_id' not in session:
            flash(f"you must first login to access this page",'warning')
            return redirect(url_for('login'))
        return f(*args ,**kwargs)
    return decorator_function



# **route for main page**
@app.route('/')
@login_required
def profile():
    " home page has 3 options: input feature to see result , history , logout"
    return render_template("home.html")




# **register route**
@app.route('/register', methods=['GET', 'POST'])
def register():
    """all the new members must first register to add their information in sqlite"""
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


# **Route to send verification code**
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


# **route for login**
@app.route('/login' , methods=["GET" , "POST"])
def login():
    """after register, must login to access profile"""
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
                return redirect(url_for('profile'))  
            else:
                print('no')
                flash("Invalid password. Please try again.", "warning")
        else:
            flash("No account found with this email. Please register first.", "warning")
    
    else:
        print("Not a POST request.")
    return render_template('login.html')
        
            
    
# ** route for forget password**
@app.route('/forgot_password', methods=['GET', 'POST'])
@login_required
def forgot_password():
    "when you logn, may forgot password. click  to recover"
    if request.method=='POST':
        security_answer = request.form.get('securityAnswer')
        new_password = request.form.get('newPassword')
        new_confirm_password = request.form.get('confirmPassword')
        try:
            user = User.query.filter_by(email=security_answer).first()
            print(f"there is a user")
            app.logger.info(f'User lookup for email: {security_answer}, User found: {user}')
            if user:
                if new_password == new_confirm_password :
                    new_password_hash = bcrypt.generate_password_hash(new_password).decode('utf-8')
                    user.password = new_password_hash
                    db.session.commit()
                    app.logger.info('Password updated successfully for user')
                    flash("Your password has been updated successfully!", "success")
                    return redirect(url_for('login'))
                else:
                    flash("New passwords do not match.", "danger")
                    app.logger.warning('Passwords do not match')
            else:
                flash("User not found.", "danger")
                app.logger.warning('User not found with provided email')
        
        except Exception as e:
            app.logger.error(f"Error during password reset: {e}")
            flash("An error occurred. Please try again.", "danger")
    return render_template('forgot_password.html')        




# ** User Input Route **
@app.route('/user_input', methods=['GET', 'POST'])
@login_required
def user_input():
    """The model uses 5 engineered features for prediction."""
    form = PredictionForm()
    
    if form.validate_on_submit():
        app.logger.info("Form user input is valid")
        
        # Gather features from form input
        features = np.array([[
            form.worst_area.data,
            form.worst_concave_points.data,
            form.mean_concave_points.data,
            form.worst_radius.data,
            form.mean_concavity.data
        ]])
        
        try:
            # Make prediction
            predictions = predict_cancer(features)
            if not predictions:
                raise ValueError("Empty prediction result.")
            prediction = predictions[0]
            app.logger.info(f"Prediction result: {prediction}")
        
            if prediction == 1:
                cancer_type = 'Malignant'
                explanation = (
                    "Malignant tumors are cancerous. They can grow quickly and spread to other "
                    "parts of the body. Early detection and treatment are crucial."
                )
            else:
                cancer_type = 'Benign'
                explanation = (
                    "Benign tumors are not cancerous and usually grow slowly. They don't spread to "
                    "other parts of the body and are less harmful, but monitoring is still important."
                )

            # Save prediction to the database
            user_id = session['user_id']
            
            new_prediction = PredictionHistory(
                user_id = user_id,
                worst_area = form.worst_area.data,
                worst_concave_points = form.worst_concave_points.data,
                mean_concave_points = form.mean_concave_points.data,
                worst_radius = form.worst_radius.data,
                mean_concavity = form.mean_concavity.data,
                prediction = cancer_type,
                explanation = explanation
            )
            db.session.add(new_prediction)
            db.session.commit()
            app.logger.info(f"Saved prediction history: {new_prediction}")
            
            # Redirect to result page, passing the prediction type and explanation
            return redirect(url_for('result', prediction=cancer_type, explanation=explanation))
        
        except Exception as e:
            app.logger.error(f"Error during prediction: {e}")
            flash("An error occurred during prediction. Please try again.", "danger")
            return render_template('user_input.html', form=form)
    
    elif request.method == 'POST':
        # Form was submitted but failed validation
        app.logger.warning("Form validation failed")
        flash("Please correct the errors in the form.", "danger")
    
    # For GET requests or failed form submissions, render the input form
    return render_template('user_input.html', form=form)



# ** see result **
@app.route('/result')
@login_required
def result():
    # Get the prediction and explanation from the query parameters
    prediction = request.args.get('prediction', 'No prediction available')
    explanation = request.args.get('explanation', '')
    
    # Render the result page with the prediction and explanation
    return render_template('result.html', prediction=prediction, explanation=explanation)




# ** History Route **
@app.route('/history')
@login_required
def history():
    """Displays the user's prediction history."""
    user_id = session['user_id']
    try:
        # Retrieve all predictions made by the user, ordered by most recent
        predictions = PredictionHistory.query.filter_by(user_id=user_id).order_by(PredictionHistory.timestamp.desc()).all()
        app.logger.info(f"Retrieved {len(predictions)} predictions for user_id {user_id}")
    except Exception as e:
        app.logger.error(f"Error retrieving prediction history: {e}")
        flash("An error occurred while retrieving your history. Please try again.", "danger")
        predictions = []
    
    return render_template('history.html', predictions=predictions)



# ** logout. need to login again **
@app.route('/logout')
@login_required
def logout():
    """Logs the user out and redirects to the login page."""
    session.pop("user_id", None)
    flash("You have been logged out.", 'info')
    app.logger.info("User logged out.")
    return redirect(url_for('login'))
    



if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True,use_reloader=False)

