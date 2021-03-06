from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, ValidationError, Email, EqualTo, Length
from flask_wtf import FlaskForm
from app.models import User, Post, Comment


class LoginForm(FlaskForm):  # Form for users to login to the blog
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')


class RegistrationForm(FlaskForm):  # Form for users to register to the blog
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField('Repeat Password', validators=[
                              DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Please use a different username.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Please use a different email address.')


class EditProfileForm(FlaskForm):  # Form for editing a profile
    username = StringField('Username', validators=[DataRequired()])
    about_me = TextAreaField('About me', validators=[Length(min=0, max=140)])
    submit = SubmitField('Submit')

    # overloaded constructor to help handle duplicate usernames
    def __init__(self, original_username, *args, **kwargs):
        super(EditProfileForm, self).__init__(*args, **kwargs)
        self.original_username = original_username

    # Could cause race conditions if app is super busy with traffic as several users could try to change to the same name
    def validate_username(self, username):
        if username.data != self.original_username:
            user = User.query.filter_by(username=self.username.data).first()
            if user is not None:
                raise ValidationError('Please use a different username.')


class PostForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    subtitle = StringField('Subtitle')
    body = TextAreaField('Say something', validators=[
                         DataRequired(), Length(min=1, max=1500)])
    submit = SubmitField('Submit')

    # used to fill in a post that is already created
    def fill_form(self, post_id):
        post = Post.query.filter_by(id=post_id).first()
        self.title.data = post.title
        self.subtitle.data = post.subtitle
        self.body.data = post.body


class CommentForm(FlaskForm):
    body = TextAreaField('Say something', validators=[
                         DataRequired(), Length(min=1, max=1500)])
    submit = SubmitField('Submit')

    # used to fill in a comment that is already created
    def fill_form(self, comment_id):
        post = Comment.query.filter_by(id=comment_id).first()
        self.body.data = post.body
