import json
import os

from data import db_session

from data.catalog_form import get_catalog_form
from data.login_form import LoginForm
from data.register_form import RegisterForm
from data.add_catalog_page_form import CatalogPageForm

from data.catalog_page import CatalogPage
from data.process import Process
from data.user import User

from flask import Flask, render_template, redirect, request, url_for
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from werkzeug.utils import secure_filename

from catalog_generate import get_catalog
from config import *

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
app.config['UPLOAD_PATH'] = UPLOAD_PATH
app.instance_path = ''

login_manager = LoginManager(app)


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


@login_manager.unauthorized_handler
def unauthorized_callback():
    return redirect('/login?next=' + request.path)


@app.route('/')
def default():
    return render_template('main.html', catalog=get_catalog())


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/login', methods=["POST", "GET"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == form.username.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            next_value = request.args.get('next')
            if next_value:
                return redirect(next_value)
            return redirect("/")
        return render_template('login.html',
                               message="Неправильный логин или пароль",
                               form=form)
    return render_template('login.html', form=form)


@app.route('/register', methods=["POST", "GET"])
def register():
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
                                   message="Пользователь с таким Email уже зарегистрирован!")
        user = User()
        if not db_sess.query(User).count():
            user.is_admin = True
        user.email = form.email.data
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        login_user(user, remember=True)
        return redirect("/")
    return render_template('register.html', form=form)


@app.route('/catalog/<int:index>', methods=["POST", "GET"])
@login_required
def catalog_routes(index):
    catalog = get_catalog()
    user_processes = list(filter(lambda x: x.catalog_id == index, current_user.processes))[::-1]
    form_class = get_catalog_form(catalog[index]['form_value'])
    form = form_class()
    if form.validate_on_submit():
        photo_count = len(list(filter(lambda x: not x.startswith('_'), form_class.__dict__.keys()))) - 1
        data = []
        for i in range(photo_count):
            f = getattr(form, f'file{i}').data
            filename = secure_filename(f.filename)
            f.save(os.path.join(
                app.instance_path, app.config['UPLOAD_PATH'], filename
            ))
            data.append(f"{app.config['UPLOAD_PATH']}/{filename}")
        db_sess = db_session.create_session()
        process = Process()
        process.catalog_id = index
        process.request_data = json.dumps(data)
        current_user.processes.append(process)
        db_sess.merge(current_user)
        db_sess.commit()
        return redirect(url_for('catalog_routes', index=index))
    return render_template('catalog_page.html', data=catalog[index], form=form, processes=user_processes)


@app.route('/profile')
@login_required
def profile():
    user_processes = current_user.processes[::-1]
    return render_template('profile.html', processes=user_processes, type_needed=True, catalog=catalog)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


@app.route('/catalog', methods=["POST", "GET"])
@login_required
def add_catalog_page():
    form = CatalogPageForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()

        catalog_page = CatalogPage()
        catalog_page.title = form.title.data
        catalog_page.description = form.description.data

        f = form.icon.data
        filename = secure_filename(f.filename)
        f.save(os.path.join(
            app.instance_path, app.config['UPLOAD_PATH'], filename
        ))
        catalog_page.icon = f"{USER_PHOTOS_FOLDER}/{filename}"

        catalog_page.fields_type = form.fields_type.data
        catalog_page.request_data = form.request_data.data
        catalog_page.url = form.url.data
        catalog_page.form_value = form.form_value.data
        current_user.pages.append(catalog_page)
        db_sess.merge(current_user)
        db_sess.commit()
        return redirect('/profile')

    return render_template('add_catalog_page.html', form=form)


if __name__ == '__main__':
    db_session.global_init(DB_FILE)
    print(get_catalog())
    print(get_catalog())
    app.run(host=HOST, port=PORT)
