from flask import Blueprint, redirect, render_template, request, send_from_directory

from App.controllers import (
    SignUp,
    LogIn
)

index_views = Blueprint('index_views', __name__, template_folder='../templates')

@index_views.route('/', methods=['GET'])
def index_page():
    return render_template('index.html')

@index_views.route('/signuptwo', methods=['GET'])
def signup_page():
    form = SignUp()
    return render_template('signup.html', form=form)

@index_views.route('/login', methods=['GET'])
def login_page():
    form = LogIn()
    return render_template('login.html', form=form)