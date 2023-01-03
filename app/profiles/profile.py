from flask import Blueprint, render_template, request, url_for, redirect, flash, abort
from flask_login import login_required, current_user
from flask_mail import Message
from itsdangerous import SignatureExpired, BadTimeSignature
from werkzeug.security import generate_password_hash, check_password_hash
from models import User, Post
from .forms import ProfileEditForm, ChangePassForm, ChangeEmailForm
from werkzeug.utils import secure_filename
import shutil
from app import db, serializer, mail
import os

# ===== Blueprint ===== #

profiles = Blueprint('profile', __name__, template_folder='templates')

ALLOWED_EXTENSIONS = set(['jpg', 'jpeg', 'png', 'svg'])

# ===== Routes ===== #

@profiles.route('/<slug>/<filter>')
def index(slug, filter):
    user = User.query.filter_by(slug=slug).first()
    posts = ''
    if filter == 'new':
        posts = user.posts.order_by(Post.created_on.desc()).all()
    elif filter == 'top':
        posts = user.posts.order_by(Post.stats.desc()).all()
    elif filter == 'saved-posts':
        if user == current_user:
            posts = user.saved_posts.order_by(Post.created_on.desc()).all()
    else: 
        return abort(404)
    return render_template('profile/index.html', user=user, posts=posts, filter=filter)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

@profiles.route('/<slug>/edit', methods=['POST', 'GET'])
def edit(slug):
    if current_user.is_authenticated:
        user = User.query.filter_by(slug=slug).first()
        posts = user.posts.order_by(Post.created_on.desc()).all()
        if current_user == user:
            form = ProfileEditForm()
            udir = 'app/static/uploads/[' + str(user.id) + ']'
            if request.method == 'POST':
                avatar = request.files['avatar']
                about = request.form['about']
                del_ava = request.form.get('del_ava')
                if avatar:
                    name = avatar.filename
                    for i in range(len(name), -1, -1):
                        if name[i-1] == '.':
                            ext = name[i:]
                    avatar.filename = 'ava.' + ext
                    if avatar and allowed_file(avatar.filename):
                        filename = secure_filename(avatar.filename)
                        if user.avatar:
                            os.remove(os.path.join(udir, user.avatar))
                        user.avatar = avatar.filename
                        avatar.save(os.path.join(udir, filename))
                if del_ava:
                    if user.avatar:
                        os.remove(udir + '/' + user.avatar)
                        user.avatar = ''
                if about:
                    user.about = about
                db.session.commit()
                flash("Your profile successfuly updated!", 'success')
                return render_template('profile/index.html', user=user, posts=posts, slug=slug, filter='new')
            if request.method == 'GET':
                form.about.data = user.about
            return render_template('profile/edit.html', form=form, user=user)
        return redirect(url_for('profile.index', slug=slug, filter='new'))
    return abort(404)

@profiles.route('/<slug>/followers')
def user_followers(slug):
    user = User.query.filter_by(slug=slug).first()
    followers_list = user.followers_list()
    followers = []
    for i in followers_list:
        follower = User.query.filter_by(id=i[0]).first()
        followers.append(follower)
    return render_template('profile/followers.html', user=user, followers=followers)

@profiles.route('/<slug>/following')
def user_following(slug):
    user = User.query.filter_by(slug=slug).first()
    following_list = user.following_list()
    followings = []
    for i in following_list:
        follower = User.query.filter_by(id=i[1]).first()
        followings.append(follower)
    return render_template('profile/following.html', user=user, followings=followings)

@profiles.route('/<slug>/follow')
def follow(slug):
    if current_user.is_authenticated:
        cur_user = User.query.filter_by(email=current_user.email).first()
        user = User.query.filter_by(slug=slug).first()
        if user == None:
            flash('User ' + user.name + ' not found.', 'fail')
            return redirect(url_for('profile.index', slug=slug, filter='new'))
        if user == cur_user:
            flash('You cannot follow yourself!', 'fail')
            return redirect(url_for('profile.index', slug=slug, filter='new'))
        u = cur_user.follow(user)
        if u is None:
            flash('Cannot follow ' + user.name + '.', 'fail')
            return redirect(url_for('profile.index', slug=slug, filter='new'))
        db.session.add(u)
        db.session.commit()
        return redirect(url_for('profile.index', slug=slug, filter='new'))
    return abort(404)

@profiles.route('/<slug>/unfollow')
def unfollow(slug):
    if current_user.is_authenticated:
        cur_user = User.query.filter_by(email=current_user.email).first()
        user = User.query.filter_by(slug=slug).first()
        if user == None:
            flash('User ' + user.name + ' not found.', 'fail')
            return redirect(url_for('profile.index', slug=slug, filter='new'))
        if user == cur_user:
            flash('You cannot unfollow yourself!', 'fail')
            return redirect(url_for('profile.index', slug=slug, filter='new'))
        u = cur_user.unfollow(user)
        if u is None:
            flash('Cannot unfollow ' + user.name + '.', 'fail')
            return redirect(url_for('profile.index', slug=slug, filter='new'))
        db.session.add(u)
        db.session.commit()
        return redirect(url_for('profile.index', slug=slug, filter='new'))
    return abort(404)


@profiles.route('/<slug>/change-pass/', methods=['POST', 'GET'])
def change_pass(slug):
    form = ChangePassForm()
    if current_user.is_authenticated:
        cur_user = User.query.filter_by(email=current_user.email).first()
        if request.method == 'POST':
            password_initial = request.form['password_initial']
            password = request.form['password']
            password_confirm = request.form['password_confirm']
            if check_password_hash(cur_user.password, password_initial):
                if password == password_confirm:
                    cur_user.password = generate_password_hash(password, method='sha256')
                    db.session.commit()
                    flash('The pass was successfully updated!', 'success')
                    return redirect(url_for('profile.index', slug=slug, filter='new'))
                else:
                    form.password.data = password
                    form.password_confirm.data = password_confirm
                    flash('Entered passwords does not mach!', 'fail')
            else:
                flash('Initial password is wrong!', 'fail')
    return render_template('profile/change_pass.html', form=form, user=cur_user)

@profiles.route('/<slug>/change-email', methods=['POST', 'GET'])
def change_email(slug):
    if current_user.is_authenticated:
        user = User.query.filter_by(slug=slug).first()
        if user == current_user:
            form = ChangeEmailForm()
            if request.method == 'POST':
                email = request.form['email']
                email_confirm = request.form['email_confirm']
                password = request.form['password']
                if email == email_confirm:
                    if check_password_hash(user.password, password):
                        user.email = email
                        db.session.commit()
                        flash('The email was successfully updated!', 'success')
                        return redirect(url_for('profile.index', slug=slug, filter='new'))
                    else:
                        form.email.data = email
                        flash('Entered password is incorrect!', 'fail')
                else:
                    form.email.data = email
                    flash('Entered emails are different!', 'fail')
            return render_template('profile/change_email.html', form=form, user=user)
        return redirect(url_for('profile.index', slug=user.slug, filter='new'))
    return abort(404)
