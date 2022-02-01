from datetime import date
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, DateField, PasswordField
from wtforms.validators import DataRequired


class TaskForm(FlaskForm):
    task_description = StringField("Task", validators=[DataRequired()])
    due_date = DateField("Due Date", default=date.today())
    submit = SubmitField("Submit")


class NewListForm(FlaskForm):
    list_name = StringField("List", validators=[DataRequired()])
    submit = SubmitField("Submit")


class RegisterForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Register")


class LoginForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Log In")
