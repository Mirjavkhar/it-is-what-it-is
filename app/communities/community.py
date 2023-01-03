from flask import Blueprint, render_template, request, url_for, redirect, flash, abort
from flask_login import login_required, current_user
from models import User, Post, Community, Category
from .forms import CommunityCreateForm, CommunityCustomizeForm
from werkzeug.utils import secure_filename
from datetime import datetime
import random
import shutil
import os
from app import db

# ===== Blueprint ===== #

community = Blueprint('communities', __name__, template_folder='templates')

ALLOWED_EXTENSIONS = set(['jpg', 'jpeg', 'png', 'svg'])

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

def upload(file, com, comDir, num):
   if file:
      name = file.filename
      for i in range(len(name), -1, -1):
         if name[i-1] == '.':
            ext = name[i:]
      file.filename = 'com_' + str(num) + '_' + com.slug + '.' + ext
      if file and allowed_file(file.filename):
         filename = secure_filename(file.filename)
         file.save(os.path.join(comDir, filename))
      return file.filename
   return 0

# ===== Routes ===== #

@community.route('/<slug>/<filter>')
def index(slug, filter):
   categories = Category.query.all()
   random_category = random.choice(categories)
   random_category_communities = random_category.communities.order_by(Community.com_members.desc()).limit(5)
   community = Community.query.filter_by(slug=slug).first_or_404()
   if community.confirm:
      posts = []
      f = ''
      if filter == 'new':
         f = 'new'
         posts = community.posts.order_by(Post.created_on.desc()).all()
         return render_template('community/index.html', community=community, posts=posts, random_category_communities=random_category_communities, random_category=random_category, filter=f)
      elif filter == 'top':
         f = 'top'
         posts = community.posts.order_by(Post.stats.desc()).all()
         return render_template('community/index.html', community=community, posts=posts, random_category_communities=random_category_communities, random_category=random_category, filter=f)
   return abort(404)

@community.route('/create', methods=['POST', 'GET'])
def create():
   if current_user.is_authenticated:
      user = User.query.filter_by(email=current_user.email).first()
      comDir = 'app/static/img/communities'
      form = CommunityCreateForm()
      categories = Category.query.all()
      if request.method == 'POST':
         category = request.form.get('community_category')
         name = request.form['name']
         about = request.form['about']
         color = request.form.get('community_color')
         img = request.files['img']
         bgimg = request.files['bgimg']
         try:
            com = Community.query.filter_by(name=name).first()
            cat = Category.query.filter_by(name=category).first()
            if not category:
               form.about.data = about
               flash('Community category has not been selected! Please try again!', 'fail')
               return render_template('community/create.html', form=form, categories=categories)
            if com:
               form.about.data = about
               flash('The name ' + name + ' is taken. Please choose another name!', 'fail')
               return render_template('community/create.html', form=form, categories=categories)
            if color:
               community = Community(name=name, about=about, color=color)
            else:
               community = Community(name=name, about=about, color='blue')
            if img:
               uimg = upload(img, community, comDir, 1)
               community.img = uimg
            if bgimg:
               ubgimg = upload(bgimg, community, comDir, 2)
               community.bgimg = ubgimg
            db.session.add(community)
            community.com_members = 0
            community.created_on = datetime.utcnow()
            community.category.append(cat)
            community.creator_id = user.id
            community.creator.append(user)
            db.session.commit()
         except:
            form.name.data = name
            form.about.data = about
            flash('Something went wrong! Try again!', 'fail')
            return render_template('community/create.html', form=form, categories=categories)
         flash('The community was successfully created! Please wait untill administrator will verify your community!', 'success')
         return redirect(url_for('index'))
      return render_template('community/create.html', form=form, categories=categories)

@community.route('/customize/<slug>', methods=['POST', 'GET'])
def customize(slug):
   if current_user.is_authenticated:
      user = User.query.filter_by(email=current_user.email).first()
      community = Community.query.filter_by(slug=slug).first()
      if community:
         if user == community.creator.first():
            comDir = 'static/img/communities'
            form = CommunityCustomizeForm()
            if request.method == 'POST':
               about = request.form['about']
               color = request.form.get('community_color')
               img = request.files['img']
               bgimg = request.files['bgimg']
               try:
                  if about:
                     community.about = about
                  if color:
                     community.color = color
                  if img:
                     if community.img:
                        os.remove(comDir + '/' + community.img)
                     uimg = upload(img, community, comDir, 1)
                     community.img = uimg
                  if bgimg:
                     if community.bgimg:
                        os.remove(comDir + '/' + community.bgimg)
                     ubgimg = upload(bgimg, community, comDir, 2)
                     community.bgimg = ubgimg
                  db.session.commit()
               except:
                  form.about.data = about
                  flash('Something went wrong! Try again!', 'fail')
                  return render_template('community/customize.html', form=form, community=community)
               flash('The community was successfully customized!', 'success')
               return redirect(url_for('communities.index', slug=community.slug, filter='new'))
            if request.method == 'GET':
               form.about.data = community.about
            return render_template('community/customize.html', form=form, community=community)
   return abort(404)

@community.route('/<slug>/<action>/<cur>/<nav>', methods=['POST', 'GET'])
@login_required
def join_leave(slug, action, cur, nav):
   if current_user.is_authenticated:
      cur_user = User.query.filter_by(email=current_user.email).first()
      community = Community.query.filter_by(slug=slug).first()
      if action == 'join':
         if community == None:
            return redirect(url_for('communities.index', slug=slug, filter=filter))
         join = cur_user.join(community)
         db.session.add(join)
      elif action == 'leave':
         if community == None:
            return redirect(url_for('communities.index', slug=slug, filter=filter))
         leave = cur_user.leave(community)
         db.session.add(leave)
      db.session.commit()
      if cur == 'com':
         return redirect(url_for('communities.index', slug=slug, filter=nav))
      if cur == 'post':
         return redirect(url_for('posts.index', slug=nav))
   return abort(404)
