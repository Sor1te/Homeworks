import requests
from flask import (Flask, request, render_template, redirect, abort,
                   make_response, jsonify)
from flask_login import LoginManager, login_user, login_required, logout_user, \
    current_user
from requests import get

from data import db_session, jobs_api, users_api
from data.users import User
from data.jobs import Jobs
from data.category import Department
from forms.user import RegisterForm, LoginForm, JobsForm, DepartmentsForm

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'

login_manager = LoginManager()
login_manager.init_app(app)


@app.route('/departments_shower', methods=['GET', 'POST'])
@login_required
def departments_shower():
    db_sess = db_session.create_session()
    if current_user.is_authenticated:
        departments = db_sess.query(Department).all()
    else:
        departments = []
    return render_template('index_departments.html', title='Департаменты',
                           departments=departments
                           )


@app.route('/departments', methods=['GET', 'POST'])
@login_required
def add_departments():
    form = DepartmentsForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        departments = Department()
        departments.title = form.title.data
        departments.chief = form.chief.data
        departments.members = form.members.data
        departments.email = form.email.data
        db_sess.add(departments)
        db_sess.merge(current_user)
        db_sess.commit()
        return redirect('/departments_shower')
    return render_template('departments_add.html',
                           title='Добавление департамента',
                           form=form
                           )


@app.route('/departments/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_departments(id):
    form = DepartmentsForm()
    if request.method == "GET":
        db_sess = db_session.create_session()
        departments = db_sess.query(Department).filter(
            Department.id == id,
            (Department.user == current_user) |
            (current_user.id == 1)
        ).first()
        if departments:
            form.title.data = departments.title
            form.chief.data = departments.chief
            form.members.data = departments.members
            form.email.data = departments.email
        else:
            abort(404)
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        departments = db_sess.query(Department).filter(
            Department.id == id,
            (Department.user == current_user) |
            (current_user.id == 1)
        ).first()
        if departments:
            form.title.data = departments.title
            form.chief.data = departments.chief
            form.members.data = departments.members
            form.email.data = departments.email
            db_sess.commit()
            return redirect('/departments_shower')
        else:
            abort(404)
    return render_template('departments_add.html',
                           title='Редактирование департамента',
                           form=form
                           )


@app.route('/delete_departments/<int:id>', methods=['GET', 'POST'])
@login_required
def departments_delete(id):
    db_sess = db_session.create_session()
    departments = db_sess.query(Department).filter(Department.id == id,
                                                   (
                                                           Department.user == current_user) |
                                                   (current_user.id == 1)
                                                   ).first()
    if departments:
        db_sess.delete(departments)
        db_sess.commit()
    else:
        abort(404)
    return redirect('/departments_shower')


@app.route('/jobs', methods=['GET', 'POST'])
@login_required
def add_job():
    form = JobsForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        jobs = Jobs()
        jobs.job = form.job.data
        jobs.team_leader = form.team_leader.data
        jobs.collaborators = form.collaborators.data
        jobs.work_size = form.work_size.data
        jobs.is_finished = form.is_finished.data
        db_sess.add(jobs)
        db_sess.merge(current_user)
        db_sess.commit()
        return redirect('/')
    return render_template('add_job.html', title='Добавление работы',
                           form=form
                           )


@app.route('/jobs/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_jobs(id):
    form = JobsForm()
    if request.method == "GET":
        db_sess = db_session.create_session()
        jobs = db_sess.query(Jobs).filter(Jobs.id == id,
                                          (Jobs.user == current_user) |
                                          (current_user.id == 1)
                                          ).first()
        if jobs:
            form.job.data = jobs.job
            form.team_leader.data = jobs.team_leader
            form.collaborators.data = jobs.collaborators
            form.work_size.data = jobs.work_size
            form.is_finished.data = jobs.is_finished
        else:
            abort(404)
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        jobs = db_sess.query(Jobs).filter(Jobs.id == id,
                                          (Jobs.user == current_user) |
                                          (current_user.id == 1)
                                          ).first()
        if jobs:
            form.job.data = jobs.job
            form.team_leader.data = jobs.team_leader
            form.collaborators.data = jobs.collaborators
            form.work_size.data = jobs.work_size
            form.is_finished.data = jobs.is_finished
            db_sess.commit()
            return redirect('/')
        else:
            abort(404)
    return render_template('edit_job.html',
                           title='Редактирование работы',
                           form=form
                           )


@app.route('/delete_jobs/<int:id>', methods=['GET', 'POST'])
@login_required
def jobs_delete(id):
    db_sess = db_session.create_session()
    jobs = db_sess.query(Jobs).filter(Jobs.id == id,
                                      (Jobs.user == current_user) |
                                      (current_user.id == 1)
                                      ).first()
    if jobs:
        db_sess.delete(jobs)
        db_sess.commit()
    else:
        abort(404)
    return redirect('/')


@app.route('/register', methods=['GET', 'POST'])
def reqister():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Пароли не совпадают")
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.email == form.email.data).first():
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Такой пользователь уже есть")
        user = User(
            surname=form.surname.data,
            name=form.name.data,
            age=form.age.data,
            position=form.position.data,
            speciality=form.speciality.data,
            address=form.address.data,
            email=form.email.data
        )
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        return redirect('/login')
    return render_template('register.html', title='Регистрация', form=form)


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(
            User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        return render_template('login.html',
                               message="Неправильный логин или пароль",
                               form=form)
    return render_template('login.html', title='Авторизация', form=form)


def main():
    db_session.global_init("db/blogs.db")
    app.register_blueprint(jobs_api.blueprint)
    app.register_blueprint(users_api.blueprint)
    app.run(debug=True, port=8080, host='127.0.0.1')


@app.route("/")
def index():
    db_sess = db_session.create_session()
    if current_user.is_authenticated:
        jobs = db_sess.query(Jobs).all()
    else:
        jobs = []
    return render_template("index.html", jobs=jobs)


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


@app.errorhandler(400)
def bad_request(_):
    return make_response(jsonify({'error': 'Bad Request'}), 400)


if __name__ == '__main__':
    main()
