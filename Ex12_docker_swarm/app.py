from flask import Flask, render_template, redirect, url_for, request, flash, session


from forms import RegisterForm, LoginForm, PredictionForm
from models import db, User
from utils import login_required

app = Flask(__name__)

app.config["SECRET_KEY"] = "some-random-text"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///site.db"

db.init_app(app)


@app.route("/")
def home():
    return render_template("home.html")


@app.route("/profile")
@login_required
def profile():
    return render_template("profile.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.check_password(form.password.data):
            session["user_id"] = user.id
            flash("Logged in successfully!", "success")
            return redirect(url_for("home"))
        else:
            flash("Invalid username or password", "danger")
    return render_template("login.html", form=form)


@app.route("/logout")
def logout():
    session.pop("user_id", None)
    flash("You have been logged out.", "info")
    return redirect(url_for("home"))


@app.route("/register", methods=["GET", "POST"])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        if (
            User.query.filter_by(username=form.username.data).first()
            or User.query.filter_by(email=form.email.data).first()
        ):
            flash("Username or email already exists", "danger")
        else:
            user = User(username=form.username.data, email=form.email.data)
            user.set_password(form.password.data)

            db.session.add(user)
            db.session.commit()
            session["user_id"] = user.id
            flash("Your account has been created! You can now log in.", "success")
            return redirect(url_for("home"))
    elif request.method == "GET":
        return render_template("register.html", form=form)
    return render_template("register.html", form=form)


@app.route("/forgot_password", methods=["GET", "POST"])
def forgot_password():
    if request.method == "POST":
        return redirect(url_for("login"))
    else:
        return render_template("forgot_password.html")


@app.route("/user_input", methods=["GET", "POST"])
@login_required
def user_input():
    form = PredictionForm()
    if request.method == "POST":
        return redirect(url_for("result"))
    else:
        return render_template("user_input.html", form=form)


@app.route("/result")
@login_required
def result():
    return render_template("result.html")


if __name__ == "__main__":
    app.run(debug=True)
