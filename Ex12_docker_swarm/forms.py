from flask_wtf import FlaskForm
from wtforms import StringField , EmailField , PasswordField, SubmitField , FloatField
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


# ** this form related to model predict **
class PredictionForm(FlaskForm):
    worst_area = FloatField('Worst Area', default=2019.0, validators=[DataRequired()])
    worst_concave_points = FloatField('Worst Concave Points', default=0.2654, validators=[DataRequired()])
    mean_concave_points = FloatField('Mean Concave Points', default=0.14710, validators=[DataRequired()])
    worst_radius = FloatField('Worst Radius', default=25.380, validators=[DataRequired()])
    mean_concavity = FloatField('Mean Concavity', default=0.30010, validators=[DataRequired()])
    submit = SubmitField('Predict')