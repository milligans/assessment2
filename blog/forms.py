from flask_wtf import FlaskForm
from wtforms import  StringField, PasswordField, SubmitField, SelectField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError, Regexp, InputRequired
from blog.models import User, Post

# adding a placeholder reference: https://stackoverflow.com/questions/9749742/wtforms-can-i-add-a-placeholder-attribute-when-i-init-a-field

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=3, max=15)],  render_kw={'placeholder':'username'})
    email = StringField('Email', validators=[DataRequired(), Email()], render_kw={'placeholder':'email'})
    firstname = StringField('First Name', validators=[DataRequired(), Length(max=30)],  render_kw={'placeholder':'first name'})
    lastname = StringField('Last Name', validators=[DataRequired(), Length(max=30)],  render_kw={'placeholder':'last name'})
    password = PasswordField('Password', validators=[DataRequired(), Regexp('^.{6,30}$', message='Your password should be between 6 and 15 characters long and contain at least one number.')],  render_kw={'placeholder':'password'})
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password', message = 'Passwords do not match.')],  render_kw={'placeholder':'confirm password'})
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Username already exists. Please choose a different one.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('That email is already registered. Please choose a different one.')




class LoginForm(FlaskForm):
    email=StringField('Email', validators=[DataRequired(), Email()])
    password=PasswordField('Password', validators=[DataRequired()])
    submit=SubmitField('Login')

class CommentForm(FlaskForm):
    comment = StringField('Comment', validators=[InputRequired()], render_kw={'placeholder':'Please enter a comment'})
    submit = SubmitField('Post comment')

# search form concept from https://www.blog.pythonlibrary.org/2017/12/13/flask-101-how-to-add-a-search-form/

class SearchForm(FlaskForm):
    search = StringField('Search Text:', validators=[InputRequired()], render_kw={'placeholder': 'Please enter search terms'})