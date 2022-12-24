import json
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField
from wtforms.validators import InputRequired, EqualTo, DataRequired

class SignUp(FlaskForm):
    username = StringField("username", validators=[InputRequired()])
    password = PasswordField(
        "New Password",
        validators=[
            InputRequired(),
            EqualTo("confirm", message="Passwords must match")
        ]
    )
    confirm = PasswordField("Repeat Password")
    submit = SubmitField("Sign Up", render_kw={"class": "btn waves-effect waves-light white-text"})

class LogIn(FlaskForm):
    username = StringField("username", validators=[InputRequired()])
    password = PasswordField("password", validators=[InputRequired()])
    submit = SubmitField("Login", render_kw={"class": "btn white-text"})