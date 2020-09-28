# Routes, have all the routes of our web page
import os
import secrets
from PIL import Image
from application_files import app, db
from application_files.forms import RegistrationForm, LoginForm, UpdateAccountForm, SendMsgForm
from application_files.model import User, Post

from flask import render_template, url_for, flash, redirect, request, abort
from flask_login import login_required, login_user, current_user, logout_user
from passlib.hash import pbkdf2_sha256
from sqlalchemy import and_


@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html')


@app.route("/about")
def about():
    return render_template('about.html', title='About')


@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    # print(form.validate_on_submit())
    if form.validate_on_submit():
        username = form.username.data
        email = form.email.data
        password = form.password.data

        # Hash password
        hashed_pswd = pbkdf2_sha256.hash(password)

        # Add username & hashed password to DB
        user = User(username=username, email=email, password=hashed_pswd)
        db.session.add(user)
        db.session.commit()

        flash(f'Account created for {form.username.data}! You are now able to log in', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    # print(form.validate_on_submit())
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            # if next page exist, redirect there, otherwise redirect homepage
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash(f'Login Unsuccessful with {form.email.data}. Please check email and password!', 'danger')
    return render_template('login.html', title='Login', form=form)


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))


@app.route("/account", methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Your account has been updated!', 'success')
        return redirect(url_for('account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
    return render_template('account.html', title='Account', image_file=image_file, form=form)


def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    f_name, f_ext = os.path.splitext(form_picture.filename)
    picture_filename = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/profile_pics', picture_filename)

    output_size = (125, 125)
    img = Image.open(form_picture)
    img.thumbnail(output_size)
    img.save(picture_path)

    return picture_filename


'''
1. Send Message: send a message from a login user to another one
• Input:
• Message: the message to be sent
• Output:
• Nothing
'''


@app.route('/send', methods=["GET", 'POST'])
@login_required
def send_msg():
    form = SendMsgForm()

    subject = form.subject.data
    content = form.content.data
    receiver = form.receiver.data

    if form.validate_on_submit():
        post = Post(subject=subject, content=content, receiver=receiver, author=current_user)
        db.session.add(post)
        db.session.commit()
        flash('Your message was sent successfully', 'success')
        return redirect(url_for('home'))
    return render_template('send_msg.html', title='Send Message', form=form)


'''
2. Get all messages: Get all messages for a specific user
• Input:
• Nothing
• Output:
• List of all messages of a specific user
'''


@app.route('/search', methods=["GET", 'POST'])
@login_required
def search():
    checkIfMessagesExist = (bool(Post.query.filter_by(receiver=current_user.username).first()))
    if not checkIfMessagesExist:
        print('No messages inside :)')
        return render_template('search.html')
    allMessages = Post.query.filter_by(receiver=current_user.username)
    print('Printing all messages for the user :)')
    return render_template('search.html', posts=allMessages)


'''
3. Get all unread messages: Get all unread messages for a specific user
• Input:
• Nothing
• Output:
• List of all unread messages of a specific user
'''


@app.route('/searchunread', methods=["GET", 'POST'])
@login_required
def searchunread():
    allUnreadMessages = Post.query.filter(and_(Post.open_message == False, Post.receiver == current_user.username)).all()
    return render_template('search.html', posts=allUnreadMessages)


'''
4. Read message: return one message
• Input:
• Id of a specific message
• Output:
• The selected message
'''


@app.route('/read/<int:post_id>', methods=["GET", 'POST'])
@login_required
def read(post_id):
    msg = Post.query.get_or_404(post_id)
    msg.open_message = True
    db.session.commit()
    return render_template('read_msg.html', title='Read message', post=msg)

'''
5. Delete message: delete the selected message
• Input:
• Id of selected message
• Output:
• Nothing
'''

@app.route('/delete/<int:post_id>', methods=["GET", 'POST'])
@login_required
def delete(post_id):
    msg = Post.query.get_or_404(post_id)
    db.session.delete(msg)
    db.session.commit()
    flash('Your post has been deleted!', 'success')
    return redirect(url_for('search'))
