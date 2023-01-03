from flask import render_template, redirect, url_for, request, flash, abort, session
from sqlalchemy.sql.expression import func, select
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
import shutil
import os
from datetime import datetime
from app import app, db
from models import User, Post, Community, Category, Report
from forms import ReportForm
import random

# ===== Functions ===== #

def delete_duplicates(array):
   return list(dict.fromkeys(array))

def post_sorting_algorithm(user):
   data = []
   dataTop = []
   community_posts = []
   top_communities = Community.query.order_by(Community.com_members.desc()).limit(10)
   for community in top_communities:
      community_posts.extend(community.posts.limit(10))
   dataTop.extend(community_posts)
   if current_user.is_authenticated:
      featured_communities = []
      user_followed_communities = []
      user_followed_posts = user.followed_posts().order_by(Post.created_on.desc()).all()
      for community in user.followed_community:
         user_followed_communities.append(community)
      if user_followed_posts or user_followed_communities:
         data.extend(user_followed_posts)
         for post in user_followed_posts:
            featured_communities.append(post.community.first())
         featured_communities.extend(user_followed_communities)
         featured_communities = delete_duplicates(featured_communities)
         for community in featured_communities:
            community_posts.extend(community.posts.all())
         data.extend(community_posts)
         data.extend(dataTop)
         data = delete_duplicates(data)
         sorted_posts = data # random.sample(data, len(data))
         return sorted_posts
   return dataTop

# ===== Routes ===== #

@app.before_request
def before_request():
   if current_user.is_authenticated:
      current_user.last_seen = datetime.utcnow()
      db.session.commit()

@app.route('/')
def index():
   categories = Category.query.all()
   random_category = random.choice(categories)
   random_category_communities = random_category.communities.order_by(Community.com_members.desc()).limit(5)
   top_communities = Community.query.order_by(Community.com_members.desc()).limit(5)
   q = request.args.get('q')
   if q:
      communities = Community.query.filter(Community.name.contains(q) | Community.slug.contains(q)).all()
      posts = Post.query.filter(Post.title.contains(q) | Post.slug.contains(q) | Post.content.contains(q)).all()
      users = User.query.filter(User.name.contains(q) | User.slug.contains(q)).all()
      fil_users = []
      for i in users:
         if 'admin' not in i.roles:
            fil_users.append(i)
      return render_template('search.html', communities=communities, posts=posts, users=fil_users)
   if current_user.is_authenticated and current_user.name in session:
      cur_user = User.query.filter_by(name=session[current_user.name]).first()
      permission = True
      communities = cur_user.followed_community.all()
      posts = post_sorting_algorithm(cur_user)
      return render_template('index.html', communities=communities, posts=posts, top_communities=top_communities, random_category_communities=random_category_communities, random_category=random_category, permission=permission)
   posts = post_sorting_algorithm(current_user)
   return render_template('index.html', posts=posts, top_communities=top_communities, random_category_communities=random_category_communities, random_category=random_category)

@app.route('/top/')
def top():
   pass

@app.route('/recent/')
def recent():
   pass

ALLOWED_EXTENSIONS = set(['jpg', 'jpeg', 'png', 'svg', 'gif'])

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS
   
@app.route('/report-form/', methods=['POST', 'GET'])
def report():
   if current_user.is_authenticated:
      user = User.query.filter_by(email=current_user.email).first()
      form = ReportForm()
      if request.method == 'POST':
         reportDir = 'static/report/'
         title = request.form['title']
         content = request.form['content']
         rType = request.form.get('report_type')
         file = request.files['file']
         if rType is None:
            form.title.data = title
            form.content.data = content
            flash("Please fill out all missed blanks!", 'ctrl')
            return render_template('report.html', form=form, user=user)
         report = Report(title=title, content=content)
         db.session.add(report)
         db.session.commit()
         if file:
            name = file.filename
            for i in range(len(name), -1, -1):
                  if name[i-1] == '.':
                     ext = name[i:]
            file.filename = str(report.id) + '_' + user.slug + '.' + ext
            if file and allowed_file(file.filename):
                  filename = secure_filename(file.filename)
                  file.save(os.path.join(reportDir, filename))
         report.rType = rType
         report.created_on = datetime.utcnow()
         report.creator_id = user.id
         report.creator.append(user)
         db.session.commit()
         flash("Thank you for your report!", 'ctrl')
         return redirect(url_for('index'))
      return render_template('report.html', form=form, user=user)
   flash("Log in or sign up to report!", 'ctrl')
   return redirect(url_for('index'))

@app.route('/admin/')
def admin():
   return abort(404)

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html', page='404'), 404

         

   

   