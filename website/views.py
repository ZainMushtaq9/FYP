from flask import Blueprint, render_template, request, session, redirect, url_for
from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_sqlalchemy import SQLAlchemy
from .models import User, Messages
from . import db
import functools

app_views = Blueprint('app_views', __name__)



@app_views.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate, post-check=0, pre-check=0"
    return response

def login_required(func):
    @functools.wraps(func)
    def secure_function(*args, **kwargs):
        if "username" not in session:
            return redirect(url_for("app_views.login", next=request.url))
        return func(*args, **kwargs)
    return secure_function

@app_views.route("/", methods=["GET", "POST"])
def home():
    return redirect(url_for("app_views.login"))  # Redirect to login by default

@app_views.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username")
        email = request.form.get("email")
        password = request.form.get("password")
        confirm_password = request.form.get("confirm_password")  # Get confirm password

        if password != confirm_password:
            flash("Passwords do not match.")  # Use flash for errors
            return render_template("flip_login.html")

        if User.query.filter_by(email=email).first():
            flash("Email already exists.")
            return render_template("flip_login.html")

        if User.query.filter_by(username=username).first(): # Check if username exists
            flash("Username already exists.")
            return render_template("flip_login.html")


        new_user = User(username=username, email=email) # Include username
        new_user.set_password(password)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for("app_views.login"))

    return render_template("flip_login.html")

@app_views.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        identifier = request.form.get("identifier") # Can be username or email
        password = request.form.get("password")

        user = User.query.filter_by(username=identifier).first()  # Try username first
        if not user:
            user = User.query.filter_by(email=identifier).first() # Try email if username fails

        if user and user.check_password(password):
            session["user_id"] = user.id
            session["username"] = user.username # Store username in session
            return redirect(url_for("app_views.base"))
        else:
            flash("Invalid username/email or password.") # Use flash for errors
            return render_template("flip_login.html")

    return render_template("flip_login.html")
@app_views.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("app_views.login"))

@app_views.route('/about')
def about():
    return render_template('about.html')

























@app_views.route("/base")
def base():
    return render_template("base.html")

@app_views.route("/kidney")
def kidney():
    return render_template(r'kidney_index.html')

@app_views.route("/kidney_form")
def kidney_form():
    return render_template(r'kidney.html')

@app_views.route("/liver")
def liver():
    return render_template(r'liver_index.html')

@app_views.route("/liver_form")
def liver_form():
    return render_template(r'liver.html')

@app_views.route("/heart")
def heart():
    return render_template(r'heart_index.html')

@app_views.route("/heart_form")
def heart_form():
    return render_template(r'heart.html')

@app_views.route("/stroke")
def stroke():
    return render_template(r'stroke_index.html')

@app_views.route("/stroke_form")
def stroke_form():
    return render_template(r'stroke.html')

@app_views.route("/diabete")
def diabete():
    return render_template(r'diabete_index.html')

@app_views.route("/diabete_form")
def diabete_form():
    return render_template(r'diabete.html')

@app_views.route("/pneumonia")
def pneumonia():
    return render_template(r'pneumonia_index.html')

@app_views.route("/pneumonia_form")
def pneumonia_form():
    return render_template(r'pneumonia.html')
