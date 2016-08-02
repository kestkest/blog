from flask_wtf import Form
from wtforms import StringField, IntegerField, TextAreaField, DateField, BooleanField, PasswordField
from wtforms.widgets import PasswordInput
from wtforms.validators import InputRequired, length, Email, DataRequired, Optional


class UserForm(Form):
    name = StringField("name", validators=[InputRequired(message="Enter your name"),
                                           length(max=20, message="Name length must be under 20")],
                       render_kw={"placeholder": "login"})
    password = PasswordField("password", validators=[InputRequired(message="Enter password please"),
                           length(min=6, message="password must be at least 6 characters long")],
                           render_kw={"placeholder": "Password"})
    email = StringField("email", validators=[Email(message="Enter valid email address"),
                                             InputRequired(message="No email entered")],
                        render_kw={"placeholder": "Email"})


class PostForm(Form):
    title = StringField("title", validators=[InputRequired(message="No title provided")])
    body = TextAreaField("body", validators=[InputRequired(message="Add something ffs")])


class TagForm(Form):
    name = StringField("tag", validators=[InputRequired(message="tag needs a name:)")])


class CategoryForm(Form):
    name = StringField("name", validators=[InputRequired(message="give category a name please")])


class LoginForm(Form):
    login = StringField("Login", validators=[InputRequired(message="Wrong login or email")],
                        render_kw={"placeholder": "Login or email"})
    password = PasswordField("Password", validators=[InputRequired(message="Wrong password")],
                             render_kw={"placeholder": "Password"})
    remember_me = BooleanField("remember_me", default=False)

