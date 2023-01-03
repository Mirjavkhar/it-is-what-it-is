from flask import Blueprint, render_template, request, url_for, redirect, flash, abort
from flask_login import login_required, current_user
from models import Community, Category
from app import db
import random

# ===== Blueprint ===== #

leaderboard = Blueprint('leaderboards', __name__, template_folder='templates')

# ===== Routes ===== #

@leaderboard.route('/')
def index():
   categories = Category.query.all()
   random_category = random.choice(categories)
   random_category_communities = random_category.communities.order_by(Community.com_members.desc()).limit(5)
   communities = Community.query.order_by(Community.com_members.desc()).all()
   com_len = len(communities)
   return render_template('leaderboards/index.html', categories=categories, communities=communities, com_len=com_len, random_category=random_category, random_category_communities=random_category_communities)

@leaderboard.route('/<slug>/')
def category(slug):
   categories = Category.query.all()
   random_category = random.choice(categories)
   random_category_communities = random_category.communities.order_by(Community.com_members.desc()).limit(5)
   current_category = Category.query.filter_by(slug=slug).first()
   if category:
      communities = current_category.communities.order_by(Community.com_members.desc()).all()
      com_len = len(communities)
      return render_template('leaderboards/index.html', categories=categories, current_category=current_category, communities=communities, com_len=com_len, random_category=random_category, random_category_communities=random_category_communities)
   return abort(404)