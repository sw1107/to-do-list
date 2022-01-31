from datetime import date
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, DateField
from wtforms.validators import DataRequired


class TaskForm(FlaskForm):
    task_description = StringField("Task", validators=[DataRequired()])
    due_date = DateField("Due Date", default=date.today())
    submit = SubmitField("Submit")


class NewListForm(FlaskForm):
    list_name = StringField("List", validators=[DataRequired()])
    submit = SubmitField("Submit")
