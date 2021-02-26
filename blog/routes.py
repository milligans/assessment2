from itertools import filterfalse
from flask import render_template, url_for, request, redirect, flash
from flask.globals import session
from blog import app, db
from blog.models import User, Post, Comment
from blog.forms import RegistrationForm, LoginForm, CommentForm, SearchForm
from flask_login import login_user, logout_user, login_required, current_user
from datetime import datetime
from sqlalchemy import select



@app.route("/", methods = ['GET','POST'])
@app.route("/home", methods = ['GET', 'POST'])
def home():
  posts=Post.query.all()
  search = SearchForm(request.form)
  if request.method == 'POST':
      return search_results(search)
  return render_template('home.html',posts=posts, form=search)

#  search methods derived from https://www.blog.pythonlibrary.org/2017/12/13/flask-101-how-to-add-a-search-form/

@app.route('/results', methods = ['GET', 'POST'])
def search_results(search):
    results = []
    search_string = search.data['search']
    
    qry=db.session.query(Post).filter(Post.content.contains(search_string))
    qry2=db.session.query(Post).filter(Post.title.contains(search_string))
    qry3=db.session.query(Post).filter(Post.subtitle.contains(search_string))
    results = qry.all() + qry2.all() + qry3.all()
    
    if not results:
      flash('No results found!')
      return redirect('/')
    # else:
    #    # display results
    return render_template('results.html', results=results, search_string = search_string)

@app.route('/allposts')
def allposts():
  posts=Post.query.all()
  return render_template('allposts.html', posts=posts )

@app.route("/about")
def about():
  return render_template('about.html', title='About')

@app.route("/post/<int:post_id>")
def post(post_id):
  post = Post.query.get_or_404(post_id)
  comments = Comment.query.filter(Comment.post_id==post.id)
  form = CommentForm()
  return render_template('post.html',post=post,comments=comments,form=form)

@app.route('/post/<int:post_id>/comment',methods=['GET','POST'])
@login_required
def post_comment(post_id):
  post=Post.query.get_or_404(post_id)
  form=CommentForm()
  if form.validate_on_submit():
    db.session.add(Comment(content=form.comment.data,post_id=post.id,author_id=current_user.id))
    db.session.commit()
    flash("Your comment has been added to the post","success")
    return redirect(f'/post/{post.id}')
  comments=Comment.query.filter(Comment.post_id==post.id)
  return render_template('post.html',post=post,comments=comments,form=form)


@app.route("/register", methods=['GET', 'POST'])
def register():
  form = RegistrationForm()
  if form.validate_on_submit():
    user=User(username=form.username.data, email=form.email.data, password=form.password.data)
    db.session.add(user)
    db.session.commit()
    flash('Registration successful! Please login.')
    
    return redirect(url_for('home'))
  return render_template('register.html', title='Register', form=form)

@app.route("/thankyou", methods=['GET', 'POST'])
def thankyou():
  return render_template('thankyou.html', title = "Thank you for registering")

@app.route("/login", methods=['GET', 'POST'])
def login():
  form=LoginForm()
  if form.validate_on_submit():
    user=User.query.filter_by(email=form.email.data).first()
    if user is not None and user.verify_password(form.password.data):
      login_user(user)
      flash('Login Successful!')
      return redirect(url_for('home'))
    flash('Invalid email address or password.')
    return render_template('login.html', title='Login', form=form)
  return render_template('login.html',title='Login',form=form)


@app.route("/logout")
def logout():
  logout_user()
  return redirect(url_for('home'))

# reference for assistance with some of the code below - https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-vi-profile-page-and-avatars
# reference for assistance with database queries https://www.blog.pythonlibrary.org/2017/12/15/flask-101-filtering-searches-and-deleting-data/
@app.route('/user/<username>')
@login_required
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    qry=db.session.query(Post,Comment ).filter(Comment.post_id ==Post.id).filter(Comment.author_id==current_user.id )
    results = qry.all()

    return render_template('user.html', user=user,  results=results)
   
@app.route('/descposts', methods=['GET', 'POST'])
def descpost():
 posts = Post.query.order_by(Post.date.desc()).all()
 return render_template('allposts.html', posts=posts)

@app.route('/ascposts', methods=['GET', 'POST'])
def ascpost():
 posts = Post.query.order_by(Post.date.asc()).all()
 return render_template('allposts.html', posts=posts)