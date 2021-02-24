from flask import Flask
from flask_admin import Admin
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from datetime import datetime
from jinja2 import Template



app = Flask(__name__)
app.config['SECRET_KEY'] = '40afad25b0a2f5cafb9b3ae1c608d52a5de854e070969dc0'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://c2102394:65853hp6S3QRw5y@csmysql.cs.cf.ac.uk:3306/c2102394_cmt120_flask'


db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)

from blog.site_apps import *

from blog import routes

from flask_admin import Admin
from blog.views import AdminView
from blog.models import User, Post, Comment
admin=Admin(app, name='Admin Panel', template_mode='bootstrap3')
admin.add_view(AdminView(User, db.session))
admin.add_view(AdminView(Post, db.session))
admin.add_view(AdminView(Comment, db.session))


# @app.context_processor
# def todaysDate():
#     blog_year=datetime.datetime.now().year
#     blog_date=datetime.datetime.now().day
#     blog_month=datetime.datetime.now().month
#     return f"Today's date is {blog_date}/{blog_month}/{blog_year}"


