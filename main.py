from datetime import date
from dotenv import load_dotenv
from flask import Flask, render_template, redirect, url_for, flash
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, LoginManager, login_user, current_user, logout_user
from sqlalchemy.orm import relationship
from forms import TaskForm, NewListForm, RegisterForm, LoginForm
from werkzeug.security import generate_password_hash, check_password_hash
import os

load_dotenv()

app = Flask(__name__)

Bootstrap(app)

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL').replace("postgres://", "postgresql://")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

postgres://

app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')

login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class List(db.Model):
    __tablename__ = "lists"
    id = db.Column(db.Integer, primary_key=True)
    list_name = db.Column(db.String(250), nullable=True)
    task = relationship("Task", back_populates="parent_list")
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    parent_user = relationship("User", back_populates="list")


class Task(db.Model):
    __tablename__ = "tasks"
    id = db.Column(db.Integer, primary_key=True)
    is_completed = db.Column(db.Boolean)
    task_description = db.Column(db.String(1000), nullable=False)
    due_date = db.Column(db.Date)
    list_id = db.Column(db.Integer, db.ForeignKey("lists.id"), nullable=False)
    parent_list = relationship("List", back_populates="task")


class User(UserMixin, db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(250), unique=True, nullable=False)
    password = db.Column(db.String(250), nullable=False)
    list = relationship("List", back_populates="parent_user")


# db.create_all()


# TODO: Update db to be able to publish


@app.route('/', methods=["GET", "POST"])
def home():
    if current_user.is_authenticated:
        all_lists = List.query.filter_by(user_id=current_user.id).all()
    else:
        all_lists = []
    return render_template("index.html",
                           all_lists=all_lists,
                           current_user=current_user)


@app.route('/view-list/<int:list_id>', methods=["GET", "POST"])
def view_list(list_id):
    task_form = TaskForm()
    incomplete_tasks = Task.query.filter_by(list_id=list_id, is_completed=False).order_by(Task.due_date).all()
    complete_tasks = Task.query.filter_by(list_id=list_id, is_completed=True).all()
    list_name = List.query.get(list_id).list_name
    date_today = date.today()
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
                           date_today=date_today,
                           list_name=list_name,
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
            list_name=new_list_form.list_name.data,
            user_id=current_user.id
        )
        db.session.add(new_list)
        db.session.commit()
        return redirect(url_for('view_list', list_id=new_list.id))
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
    flash('List Deleted')
    return redirect(url_for('home'))


@app.route('/delete_check/<int:list_id>')
def delete_check(list_id):
    list_to_delete = List.query.filter_by(id=list_id).first()
    return render_template("delete_check.html", list_to_delete=list_to_delete)


@app.route('/register', methods=["GET", "POST"])
def register():
    register_form = RegisterForm()
    if register_form.validate_on_submit():
        user_exists = User.query.filter_by(username=register_form.username.data).first()
        if user_exists:
            flash("User already registered")
            return redirect(url_for('register'))
        else:
            new_user = User(
                username=register_form.username.data,
                password=generate_password_hash(register_form.password.data)
            )
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user)
            return redirect(url_for('home'))
    return render_template('register.html', register_form=register_form)


@app.route('/login', methods=["GET", "POST"])
def login():
    login_form = LoginForm()
    if login_form.validate_on_submit():
        # check user exists
        user_to_login = User.query.filter_by(username=login_form.username.data).first()
        if user_to_login:
            if check_password_hash(user_to_login.password, login_form.password.data):
                login_user(user_to_login)
                return redirect(url_for('home'))
            else:
                flash("Incorrect password")
                return redirect(url_for('login'))
        else:
            flash("User doesn't exist")
            return redirect(url_for('login'))
    return render_template('login.html', login_form=login_form)


@app.route('/logout')
def logout():
    logout_user()
    flash("User logged out")
    return redirect(url_for('home'))


if __name__ == '__main__':
    app.run(debug=True)
