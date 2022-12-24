from flask import Blueprint, redirect, render_template, request, send_from_directory

from App.controllers import (
    SignUp,
    LogIn,
    create_user
)

index_views = Blueprint('index_views', __name__, template_folder='../templates')

@index_views.route('/', methods=['GET'])
def index_page():
    return render_template('index.html')

@index_views.route('/signuptwo', methods=['GET'])
def signup_get_page():
    form = SignUp()
    return render_template('signup.html', form=form)

@index_views.route("/signuptwo", methods=["POST"])
def signup_post_page():
    form = SignUp()
    if form.validate_on_submit():
        data = request.form
        user = create_user(data["username"], data["password"])
        if user:
            flash("Account Created!")
            return redirect('url_for("index_views.index_page")')
    return redirect(url_for("index_views.signup_get_page"))

@index_views.route('/login', methods=['GET'])
def login_page():
    form = LogIn()
    return render_template('login.html', form=form)