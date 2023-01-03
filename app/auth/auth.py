from flask import Blueprint, render_template, request, url_for, redirect, flash, session
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, login_required, current_user
from .forms import LoginForm, SignUpForm
from slugify import slugify
from models import User, Role, Rank
from app import db
import os

# ===== Blueprint ===== #

auth = Blueprint('authorization', __name__, template_folder='templates')

# ===== Routes ===== #

@auth.route('/signin', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        user = User.query.filter_by(email=email).first()
        if not user or not check_password_hash(user.password, password):
            flash('Please check your login details and try again.', 'fail')
            return redirect(url_for('authorization.login')) 
        session.permanent = True
        session[user.name] = user.name
        login_user(user)
        return redirect(url_for('index'))
    form = LoginForm()
    return render_template('/login.html', form=form)

@auth.route('/signup', methods=['POST', 'GET'])
def signup():
    if request.method == 'POST':
        uname = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        userEmail = User.query.filter_by(email=email).first()
        userName = User.query.filter_by(slug=slugify(uname)).first()
        if userEmail:
            flash('Email address already exists.', 'fail')
            return redirect(url_for('authorization.signup'))
        if userName:
            flash('This name is already taken.', 'fail')
            return redirect(url_for('authorization.signup'))
        role = Role.query.filter_by(name='user').first()
        rank = Rank.query.filter_by(name='newbie').first()
        new_user = User(name=uname, email=email, password=generate_password_hash(password, method='sha256'))
        db.session.add(new_user)
        new_user.roles.append(role)
        new_user.rank.append(rank)
        db.session.commit()
        file_path = 'app/static/uploads/[' + str(new_user.id) + ']'
        if not os.path.exists(file_path):
            os.makedirs('app/static/uploads/[' + str(new_user.id) + ']')
        login_user(new_user)
        return redirect(url_for('index'))
    form = SignUpForm()
    return render_template('/signup.html', form=form)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('authorization.login'))
