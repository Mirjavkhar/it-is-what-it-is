from flask import Blueprint, render_template, request, url_for, redirect, flash
from flask_login import login_required
from models import User
from app import db

# ===== Blueprint ===== #

chats = Blueprint('chat', __name__, template_folder='templates')

# ===== Routes ===== #

@chats.route('/')
def index():
    pass