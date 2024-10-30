from flask_wtf import FlaskForm
from wtforms import (
    BooleanField,
    DecimalField,
    EmailField,
    IntegerField,
    PasswordField,
    StringField,
    SubmitField,
)
from wtforms.validators import (
    DataRequired,
    Email,
    EqualTo,
    InputRequired,
    Length,
    Regexp,
)


class RegisterForm(FlaskForm):
    pass_regex = r"^(?=.*[A-Za-z])(?=.*\d)(?=.*[@$!%*?&#])[A-Za-z\d@$!%*?&#]{8,32}$"
    username = StringField(
        label="username", validators=[InputRequired(), Length(min=3, max=20)]
    )
    email = EmailField(label="email", validators=[InputRequired(), Email()])
    password = PasswordField(
        label="password",
        validators=[
            InputRequired(),
            Length(min=8, max=32),
            Regexp(
                regex=pass_regex,
                message="""
                        Password must contain at least 1 letter,
                        1 digit, and 1 special character.
                        """,
            ),
        ],
        filters=[lambda x: x.strip() if x else None],
    )
    confirm_password = PasswordField(
        label="confirm-password",
        validators=[
            DataRequired(),
            EqualTo("password", message="Passwords must match"),
        ],
        filters=[lambda x: x.strip() if x else None],
    )
    submit = SubmitField("Register")


class LoginForm(FlaskForm):
    email = EmailField(label="email", validators=[InputRequired(), Email()])
    password = PasswordField("password", validators=[InputRequired()])
    submit = SubmitField("Login")


class PredictionForm(FlaskForm):
    area = DecimalField("Area (Square meters)", validators=[InputRequired()])
    rooms = IntegerField("Number of Rooms", validators=[InputRequired()])
    parking = BooleanField("Has Parking")
    warehouse = BooleanField("Has Warehouse")
    elevator = BooleanField("Has Elevator")
    address = StringField("Address", validators=[InputRequired()])
    submit = SubmitField("Submit")
