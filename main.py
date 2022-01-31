from flask import Flask, render_template, redirect, url_for
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship
from forms import TaskForm, NewListForm

app = Flask(__name__)

Bootstrap(app)

app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///to-do-list.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

app.config['SECRET_KEY'] = 'secretsecretsecret'


class List(db.Model):
    __tablename__ = "lists"
    id = db.Column(db.Integer, primary_key=True)
    list_name = db.Column(db.String(250), nullable=True)
    task = relationship("Task", back_populates="parent_list")


class Task(db.Model):
    __tablename__ = "tasks"
    id = db.Column(db.Integer, primary_key=True)
    is_completed = db.Column(db.Boolean)
    task_description = db.Column(db.String(1000), nullable=False)
    due_date = db.Column(db.Date)
    list_id = db.Column(db.Integer, db.ForeignKey("lists.id"), nullable=False)
    parent_list = relationship("List", back_populates="task")

# db.create_all()


# TODO: improve website styling
# TODO: add date completed
# TODO: add in conformation before deleting list
# TODO: add ability to sort by date
# TODO: change overdue tasks to red
# TODO: add ability to log in/create users
# TODO: add in reminders (maybe email?)
# TODO: change to using environment variables
# TODO: write README, add requirements file
# TODO: Update db to be able to publish


@app.route('/', methods=["GET", "POST"])
def home():
    all_lists = List.query.all()
    return render_template("index.html", all_lists=all_lists)


@app.route('/view-list/<int:list_id>', methods=["GET", "POST"])
def view_list(list_id):
    task_form = TaskForm()
    incomplete_tasks = Task.query.filter_by(list_id=list_id, is_completed=False).all()
    complete_tasks = Task.query.filter_by(list_id=list_id, is_completed=True).all()
    if task_form.validate_on_submit():
        new_task = Task(
            is_completed=False,
            task_description=task_form.task_description.data,
            due_date=task_form.due_date.data,
            list_id=list_id
        )
        db.session.add(new_task)
        db.session.commit()
        return redirect(url_for('view_list', list_id=list_id))
    return render_template("view-list.html",
                           list_id=list_id,
                           incomplete_tasks=incomplete_tasks,
                           complete_tasks=complete_tasks,
                           task_form=task_form)


@app.route('/mark-complete/<int:list_id>/<int:task_id>')
def mark_complete(list_id, task_id):
    post_to_mark_complete = Task.query.get(task_id)
    post_to_mark_complete.is_completed = True
    db.session.commit()
    return redirect(url_for('view_list', list_id=list_id))


@app.route('/create-new-list', methods=["GET", "POST"])
def create_new_list():
    new_list_form = NewListForm()
    if new_list_form.validate_on_submit():
        new_list = List(
            list_name=new_list_form.list_name.data
        )
        db.session.add(new_list)
        db.session.commit()
        return redirect('/')
    return render_template("create-new-list.html", new_list_form=new_list_form)


@app.route('/delete-task/<int:list_id>/<int:task_id>')
def delete_task(list_id, task_id):
    task_to_delete = Task.query.get(task_id)
    db.session.delete(task_to_delete)
    db.session.commit()
    return redirect(url_for('view_list', list_id=list_id))


@app.route('/delete_list/<int:list_id>')
def delete_list(list_id):
    Task.query.filter_by(list_id=list_id).delete()
    List.query.filter_by(id=list_id).delete()
    db.session.commit()
    return redirect('/')


if __name__ == '__main__':
    app.run(debug=True)