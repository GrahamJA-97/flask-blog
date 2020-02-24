from flask import render_template, flash, redirect, url_for, request
from flask_login import current_user, login_user, logout_user, login_required
from app import app, db
from app.forms import LoginForm, RegistrationForm, EditProfileForm, PostForm
from app.models import User, Post
from werkzeug.urls import url_parse
from datetime import datetime


################### HOME PAGE
@app.route('/')
@app.route('/index')
@login_required
def index():
    # posts = [
    #     {
    #         'author': {'username': 'John'},
    #         'body': 'Quadsort is pretty neat!'
    #     },
    #     {
    #         'author': {'username': 'Jane'},
    #         'body': 'Is quicksort a thing of the past?'
    #     }
    # ]
    # .order_by(Post.timestamp)
    posts = Post.query.limit(5).all()
    return render_template('index.html', title='Home Page', posts=posts)


################### LOGIN PAGE
@app.route('/login', methods=['GET', 'POST'])
@login_required
def login():
    # if the user is already logged in go back to index
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)


################### LOGOUT PAGE
@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


################### REGISTRATION PAGE
@app.route('/register', methods=['GET', 'POST'])
def register():
    # if the user is already logged in go back to index
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


################### VIEW USER PAGE
@app.route('/user/<username>')
@login_required
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    posts = [
        {'author': user, 'body': 'Test post #1'},
        {'author': user, 'body': 'Test post #2'}
    ]
    return render_template('user.html', user=user, posts=posts)

################### EDIT PROFILE PAGE
@app.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm(current_user.username)
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.about_me = form.about_me.data
        db.session.commit()
        flash('Your changes have been saved.')
        return redirect(url_for('edit_profile'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.about_me.data = current_user.about_me
    return render_template('edit_profile.html', title='Edit Profile', form=form)


################### VIEW POST PAGE
@app.route('/post/<post_id>')
def post(post_id):
    post = Post.query.filter_by(id=post_id).first_or_404()

    return render_template('view_post.html', post=post)


################### NEW POST PAGE
@app.route('/new_post', methods=['GET', 'POST'])
@login_required
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=current_user.username).first_or_404()
        post = Post(title=form.title.data, subtitle=form.subtitle.data, body=form.body.data, user_id=user.id)
        db.session.add(post)
        db.session.commit()
        flash("Post ADDED!!")
        return redirect(url_for('index'))
    return render_template('new_post.html', title="", form=form)


################### EDIT POST PAGE
# @app.route('/edit_post/<post_id>', methods=['GET', 'POST'])
# @login_required
# def edit_post(post_id):
#     form = PostForm()
#     if form.validate_on_submit():
#         user = User.query.filter_by(username=current_user.username).first_or_404()
#         post = Post(title=form.title.data, subtitle=form.subtitle.data, body=form.body.data, user_id=user.id)
#         db.session.add(post)
#         db.session.commit()
#         flash("Post ADDED!!")
#         return redirect(url_for('index'))
#     return render_template('edit_post.html', title="Edit", form=form)

@app.before_request  # Function is executed before the view function
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow() # update the last_seen variable
        # user will already be in the session so no need to re-add, just commit
        db.session.commit()
