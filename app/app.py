from flask import Flask, redirect, url_for, request, render_template, abort, session
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager
from flask_admin import Admin, AdminIndexView
from flask_admin.contrib.sqla import ModelView
from flask_security import SQLAlchemyUserDatastore, Security
from itsdangerous import URLSafeTimedSerializer
from flask_login import LoginManager, current_user
from flask_mail import Mail
from config import Configuration
from datetime import timedelta
import flask_sijax, os

# ===== App ===== #

app = Flask(__name__)
app.config.from_object(Configuration)

app.permanent_session_lifetime = timedelta(days=1)

app.jinja_env.globals.update(zip=zip)

# ===== Upload Settings ===== #

ALLOWED_EXTENSIONS = set(['jpg', 'jpeg', 'png', 'svg'])
UPLOAD_FOLDER = 'static/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# ===== DB ===== #

db = SQLAlchemy(app)

migrate = Migrate(app, db)
manager = Manager(app)
manager.add_command('db', MigrateCommand)

# ===== Mail ===== #

mail = Mail(app)

# ===== Token ===== #

serializer = URLSafeTimedSerializer(app.config['SECRET_KEY'])

# ===== Filters ===== #

@app.template_filter('dtf_m_d_y')
def dtf_m_d_y(value, format='%B %d, %Y'):
    return value.strftime(format)

@app.template_filter('dtf_m_d')
def dtf_m_d(value, format='%B %d'):
    return value.strftime(format)

@app.template_filter('dtf_H_M_m_d')
def dtf_H_M_m_d(value, format='%H:%M %B %d'):
    return value.strftime(format)

# ===== Admin ===== #

from models import *

class AdminMixin:
    def is_accessible(self):
        if current_user.is_authenticated:
            return current_user.has_role('admin')

    def inaccessible_callback(self, name, **kwargs):
        return abort(404)

class BaseModelView(ModelView):
    def on_model_change(self, form, model, is_created):
        return super(ModelView, self).on_model_change(form, model, is_created)

class AdminView(AdminMixin, ModelView):
    pass

class HomeAdminView(AdminMixin, AdminIndexView):
    pass

class PostAdminView(AdminMixin, BaseModelView):
    form_columns = ['title', 'content', 'community']

class CommunityAdminView(AdminMixin, BaseModelView):
    form_columns = ['name', 'about', 'confirm']

class ReportsAdminView(AdminMixin, BaseModelView):
    form_columns = ['id', 'creator_id', 'created_on', 'rType', 'title', 'content']

class CommentsAdminView(AdminMixin, BaseModelView):
    form_columns = ['id', 'creator_id', 'comment']

class MediaAdminView(AdminMixin, BaseModelView):
    form_columns = ['id', 'name']

admin = Admin(app, 'iiwii', url='/', index_view=HomeAdminView(name='Home'))
admin.add_view(PostAdminView(Post, db.session))
admin.add_view(CommunityAdminView(Community, db.session))
admin.add_view(ReportsAdminView(Report, db.session))
admin.add_view(CommentsAdminView(Comment, db.session))
admin.add_view(MediaAdminView(Media, db.session))
admin.add_view(AdminView(User, db.session))
admin.add_view(AdminView(Role, db.session))

# ===== Flask Security ===== #

user_datastore = SQLAlchemyUserDatastore(db, User, Role)
security = Security(app, user_datastore)

# ===== Flask Login ===== #

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.session_protection = "strong"

from models import User

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

