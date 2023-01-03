from flask import Blueprint, render_template, request, url_for, redirect, flash, jsonify, abort
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
import shutil
import os
import bleach
from datetime import datetime
from .forms import PostForm, CommentForm
from models import User, Post, Community, Media, Comment
from app import db, app

# ===== Blueprint ===== #

posts = Blueprint('posts', __name__, template_folder='templates')

ALLOWED_EXTENSIONS = set(['jpg', 'jpeg', 'png', 'svg', 'gif'])

# ===== Routes ===== #

@posts.route('/<slug>', methods=['POST', 'GET'])
def index(slug):
    if current_user.is_authenticated:
        user = User.query.filter_by(email=current_user.email).first()
    post = Post.query.filter_by(slug=slug).first_or_404()
    creator = post.creator.first()
    media = post.medias.first()
    comments = post.comments.order_by(Comment.created_on.desc()).all()
    if request.method == 'POST':
        cleaned_comment = bleach.clean(request.form['comment'], tags=bleach.sanitizer.ALLOWED_TAGS + ['p'])
        if cleaned_comment:
            comment = Comment(comment=cleaned_comment)
            comment.creator.append(user)
            comment.creator_id = user.id
            comment.post.append(post)
            comment.created_on = datetime.utcnow()
            db.session.commit()
            return redirect(url_for('posts.index', slug=post.slug))
    form = CommentForm()
    return render_template('posts/index.html', form=form, post=post, creator=creator, media=media, comments=comments)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

@posts.route('/create', methods=['POST', 'GET'])
def create():
    if current_user.is_authenticated:
        user = User.query.filter_by(email=current_user.email).first()
        userDir = 'app/static/uploads/[' + str(user.id) + ']'
        communities = Community.query.all()
        if request.method == 'POST':
            title = request.form['title']
            cleaned_content = bleach.clean(request.form['content'], tags=bleach.sanitizer.ALLOWED_TAGS + ['p', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6'])
            community = request.form.get('post_community')
            file = request.files['file']
            try:
                if cleaned_content:
                    post = Post(title=title,  content=cleaned_content)
                else:
                    post = Post(title=title)
                cat = Community.query.filter_by(name=community).first()
                if file:
                    name = file.filename
                    for i in range(len(name), -1, -1):
                        if name[i-1] == '.':
                            ext = name[i:]
                    file.filename = post.slug + '.' + ext
                    print()
                    if file and allowed_file(file.filename):
                        filename = secure_filename(file.filename)
                        file.save(os.path.join(userDir, filename))
                    media = Media(name=file.filename)
                    db.session.add(media)
                    post.medias.append(media)
                db.session.add(post)
                post.creator.append(user)
                post.creator_id = user.id
                post.community.append(cat)
                post.created_on = datetime.utcnow()
                db.session.commit()
            except:
                flash('Something went wrong! Try again!', 'fail')
                return redirect(url_for('posts.create', slug=post.slug))
            flash('The post was successfully created!', 'success')
            return redirect(url_for('posts.index', slug=post.slug))
        form = PostForm()
        return render_template('posts/create.html', form=form, communities=communities)
    flash("Please login to get access for creting posts!", 'ctrl')
    return redirect(url_for('index'))
            
@posts.route('/<slug>/update', methods=['POST', 'GET'])
def update(slug):
    if current_user.is_authenticated:
        post = Post.query.filter(Post.slug==slug).first_or_404()
        cur_user = User.query.filter_by(email=current_user.email).first()
        form = PostForm()
        if cur_user == post.creator.first():
            if request.method == 'POST':
                post.content = request.form['content']
                post.updated = True
                post.updated_on = datetime.utcnow()
                db.session.commit()
                flash('The post was successfully updated!', 'success')
                return redirect(url_for('posts.index', slug=post.slug))
            elif request.method == 'GET':
                form.content.data = post.content
            return render_template('posts/update.html', post=post, form=form)
    return abort(404)

@posts.route('/<slug>/delete')
def delete(slug):
    if current_user.is_authenticated:
        cur_user = User.query.filter_by(email=current_user.email).first()
        post = Post.query.filter_by(slug=slug).first()
        if cur_user == post.creator.first():
            db.session.delete(post)
            db.session.commit()
            flash('The post was successfully deleted!', 'success')
            return redirect(url_for('index'))
    return abort(404)

@posts.route('/<slug>/<action>/<cur>/<nav>', methods=['POST', 'GET'])
@login_required
def rate_post(slug, action, cur, nav):   
    if current_user.is_authenticated:
        cur_user = User.query.filter_by(email=current_user.email).first()
        post = Post.query.filter_by(slug=slug).first_or_404()
        body = {}
        if action == 'like':
            if cur_user.is_disliked(post):
                d = cur_user.dislike(post)
                db.session.add(d)
            l = cur_user.like(post)
            db.session.add(l)
            post.stats = post.rating()
            db.session.commit()
            post.stats = post.rating()
        if action == 'dislike':
            if cur_user.is_liked(post):
                l = cur_user.like(post)
                db.session.add(l)
            d = cur_user.dislike(post)
            db.session.add(d)
            post.stats = post.rating()
            db.session.commit()
        if cur == 'post':
            return redirect(url_for('posts.index', slug=slug))
        elif cur == 'index':
            return redirect(url_for('index'))
        elif cur == 'com':
            return redirect(url_for('communities.index', slug=nav))
        elif cur == 'profile':
            return redirect(url_for('profile.index', slug=nav, filter='new'))
    return abort(404)

@posts.route('/<slug>/save-unsave/<cur>/<nav>', methods=['POST', 'GET'])
@login_required
def save_post(slug, cur, nav):   
    if current_user.is_authenticated:
        user = User.query.filter_by(email=current_user.email).first()
        post = Post.query.filter_by(slug=slug).first_or_404()
        if current_user.is_authenticated:
            print('ok')
            act = user.save_unsave(post)
            db.session.add(act)
            db.session.commit()
            print('save-unsave')
        if cur == 'post':
            return redirect(url_for('posts.index', slug=slug))
        elif cur == 'index':
            return redirect(url_for('index'))
        elif cur == 'com':
            return redirect(url_for('communities.index', slug=nav))
        elif cur == 'profile':
            return redirect(url_for('profile.index', slug=nav, filter='new'))
    return abort(404)
