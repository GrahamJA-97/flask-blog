from flask import render_template, flash, redirect, url_for, request
from flask_login import current_user, login_user, logout_user, login_required
from app import app, db
from app.forms import LoginForm, RegistrationForm, EditProfileForm, PostForm, CommentForm
from app.models import User, Post, Comment
from werkzeug.urls import url_parse
from datetime import datetime


# HOME PAGE
@app.route('/')
@app.route('/index')
def index():
    posts = Post.query.order_by(Post.timestamp.desc()).limit(32).all()
    return render_template('index.html', title='Home Page', posts=posts)


# LOGIN PAGE
@app.route('/login', methods=['GET', 'POST'])
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


# LOGOUT PAGE
@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


# REGISTRATION PAGE
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

# INVALID PERMISSIONS PAGE
@app.route('/perm_error')
def perm_error():
    return render_template('perm_error.html', title="ERROR")


# VIEW USER PAGE
@app.route('/user/<username>')
@login_required
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    posts = Post.query.filter_by(user_id=user.id).all()
    return render_template('user.html', user=user, posts=posts)

# EDIT PROFILE PAGE
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


# VIEW POST PAGE
@app.route('/post/<post_id>')
def post(post_id):
    post = Post.query.filter_by(id=post_id).first_or_404()
    comments = Comment.query.filter_by(post_id=post_id).order_by(Comment.timestamp).limit(32).all()

    return render_template('view_post.html', post=post, comments=comments)


# NEW POST PAGE
@app.route('/new_post', methods=['GET', 'POST'])
@login_required
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        user = User.query.filter_by(
            username=current_user.username).first_or_404()
        post = Post(title=form.title.data, subtitle=form.subtitle.data,
                    body=form.body.data, user_id=user.id)
        db.session.add(post)
        db.session.commit()
        flash('Your new post has been saved.')
        # go to new post when done
        return redirect(url_for('post', post_id=post.id))
    return render_template('edit_post.html', title="New Post", form=form)


# EDIT POST PAGE
@app.route('/edit_post/<post_id>', methods=['GET', 'POST'])
@login_required
def edit_post(post_id):
    user = User.query.filter_by(username=current_user.username).first_or_404()
    post = Post.query.filter_by(id=post_id).first_or_404()
    if user.id != post.user_id:  # Check user is allowed to edit post
        return redirect(url_for('perm_error'))

    form = PostForm()
    if form.validate_on_submit():  # On submission update the record
        post.title = form.title.data
        post.subtitle = form.subtitle.data
        post.body = form.body.data
        post.timestamp = datetime.utcnow()
        db.session.commit()
        flash('Your changes have been saved.')
        return redirect(url_for('post', post_id=post.id))
    elif request.method == 'GET':  # on arrival fill the page values
        form.fill_form(post_id)
    return render_template('edit_post.html', title="Edit Post", form=form)

# NEW COMMENT PAGE
@app.route('/new_comment/<post_id>', methods=['GET', 'POST'])
@login_required
def new_comment(post_id):
    form = CommentForm()
    if form.validate_on_submit():
        user = User.query.filter_by(
            username=current_user.username).first_or_404()
        comment = Comment(body=form.body.data, user_id=user.id, post_id=post_id)
        db.session.add(comment)
        db.session.commit()
        flash('Your new comment has been saved.')
        # go to new comment when done
        return redirect(url_for('post', post_id=post_id))
    return render_template('edit_comment.html', title="New Comment", form=form)

# EDIT COMMENT PAGE
@app.route('/edit_comment/<post_id>/<comment_id>', methods=['GET', 'POST'])
@login_required
def edit_comment(post_id, comment_id):
    user = User.query.filter_by(username=current_user.username).first_or_404()
    comment = Comment.query.filter_by(id=comment_id).first_or_404()
    if user.id != comment.user_id:  # Check user is allowed to edit comment
        return redirect(url_for('perm_error'))

    form = CommentForm()
    if form.validate_on_submit():
        comment.body = form.body.data
        comment.timestamp = datetime.utcnow()
        db.session.commit()
        flash('Your changes have been saved.')
        return redirect(url_for('post', post_id=post_id))
    elif request.method == 'GET':  # on arrival fill the page values
        form.fill_form(comment_id)
    return render_template('edit_comment.html', title="Edit Comment", form=form)


@app.before_request  # Function is executed before the view function
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()  # update the last_seen variable
        # user will already be in the session so no need to re-add, just commit
        db.session.commit()
