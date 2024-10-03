from flask_wtf import FlaskForm
from wtforms import StringField , EmailField , PasswordField, SubmitField 
from wtforms.validators import InputRequired, DataRequired , Email , Length , Regexp , EqualTo

class RegisterForm(FlaskForm):
    username = StringField(label='username', validators=[InputRequired(), Length(min=3)])
    
    email = EmailField(label='email', validators=[InputRequired(), Email() ]) 
    
    password = PasswordField(label='password', validators=[InputRequired(),
                                            Length(min=8 , max=32),
                                            Regexp(regex=r"^(?=.*[A-Za-z])(?=.*\d)(?=.*[@$!%*?&#])[A-Za-z\d@$!%*?&#]{8,32}$",
                                                   message="Password must contain at least 1 letter, 1 digit, and 1 special character.")],
                            filters=[lambda x:x.strip() if x else None] )
    
    confirm_password = PasswordField(label='confirm-password', validators=[DataRequired(),
                                                                           EqualTo('password', message="Passwords must match")],
                                    filters=[lambda x:x.strip() if x else None] )
    
    submit = SubmitField('Register')

    