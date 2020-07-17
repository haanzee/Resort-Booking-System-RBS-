# users/routes.py
from flask import render_template, url_for, flash, redirect, request, Blueprint
from flask_login import login_user, current_user, logout_user, login_required
from main import db, bcrypt
from main.modles import User, Post
from main.users.forms import (RegistrationForm, LoginForm, UpdateAccountForm,
                                   RequestResetForm, ResetPasswordForm, 
                                   ResetPasswordDirectForm)
from main.users.utils import save_picture, send_reset_email

from flask import Blueprint
users = Blueprint('users', __name__)


@users.route('/register', methods=['GET', 'POST'])
def register():
	if current_user.is_authenticated:
		return redirect(url_for('home'))
	form = RegistrationForm()
	if form.validate_on_submit():
			hashed_passowrd = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
			user = User(usertype=form.usertype.data, username=form.username.data, email=form.email.data, password=hashed_passowrd)
			db.session.add(user)
			db.session.commit()
			flash('Youer account now Creaated, Now You are login now', 'success')
			return redirect(url_for('main.home'))
	return render_template('register.html', title='Register', form=form)



@users.route('/login', methods=['GET', 'POST'])
def login():
	if current_user.is_authenticated:
		return redirect(url_for('main.home'))
	form = LoginForm()
	if form.validate_on_submit():
		user = User.query.filter_by(email=form.email.data).first()
		if user and bcrypt.check_password_hash(user.password, form.password.data):
			if	(login_user(user,remember=form.remember.data) and user.userauth=='Yes' and user.usertype=='Admin'):
				next_page  = request.args.get('next')
				return redirect(next_page) if next_page else  redirect(url_for('bhandler.dash_index'))
			elif (login_user(user,remember=form.remember.data) and user.userauth=='Yes'):
				next_page  = request.args.get('next')
				return redirect(next_page) if next_page else  redirect(url_for('main.about'))
			else:
				flash('Login Unsucessful. You are not authorised by admin', 'danger')
				logout_user()
				return render_template('login.html', title='Login', form=form)	

		else:
			flash('Login Unsucessful. Please check Email & Password', 'danger')
	return render_template('login.html', title='Login', form=form)

@users.route('/logout')
def logout():
	logout_user()
	return redirect(url_for('main.home'))




@users.route('/account' , methods=['GET', 'POST'])
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
		return redirect(url_for('users.account'))
	elif request.method == 'GET':
		form.username.data = current_user.username
		form.email.data = current_user.email
	image_file = url_for('static', filename='profile_pics/'+ current_user.image_file)
	return render_template('account.html', title='Account', 
		image_file=image_file, form=form)

@users.route("/user/<string:username>")
def user_posts(username):
    page = request.args.get('page', 1, type=int)
    user = User.query.filter_by(username=username).first_or_404()
    posts = Post.query.filter_by(author=user)\
        .order_by(Post.date_posted.desc())\
        .paginate(page=page, per_page=2)
    return render_template('user_post.html', posts=posts, user=user)

@users.route('/reset_password' , methods=['GET', 'POST'])
def reset_request():
	if current_user.is_authenticated:
		return redirect(url_for('main.home'))
	form = RequestResetForm()
	if form.validate_on_submit():
		user = User.query.filter_by(email=form.email.data).first()
		if (user.email == form.email.data and user.userauth == 'Yes'):
			send_reset_email(user)
			flash('An email has been sent with instructions to reset your password.', 'info')
			return redirect(url_for('users.login'))
		else:
			flash('You are not authorised by admin, Please contact admin.', 'danger')
			return redirect(url_for('users.login'))

	return render_template('reset_request.html', title='Reset Password', form=form)	

@users.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_token(token):
	if current_user.is_authenticated:
		return redirect(url_for('main.home'))
	user = User.verify_reset_token(token)
	if user is None:
		flash('That is an invalid or expired token', 'warning')
		return redirect(url_for('reset_request'))
	form = ResetPasswordForm()
	if form.validate_on_submit():
		hashed_passowrd = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
		user.password=hashed_passowrd
		db.session.add(user)
		db.session.commit()
		flash('Youer passowrd has been updated, Now You are login now', 'success')
		return redirect(url_for('users.login'))
	return render_template('reset_token.html', title='Reset Password', form=form)	

@users.route('/reset_pwd', methods=['GET', 'POST'])
@login_required
def reset_pwd():
	#if current_user.is_authenticated:
	#	return redirect(url_for('main.home'))
	user = current_user
	if user is None:
		flash('That is an invalid', 'warning')
		return redirect(url_for('reset_request'))
	form = ResetPasswordDirectForm()
	if form.validate_on_submit():
		user = User.query.filter_by(email=current_user.email).first()
		if user and bcrypt.check_password_hash(user.password, form.oldpassword.data):
			hashed_passowrd = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
			user.password=hashed_passowrd
			db.session.add(user)
			db.session.commit()
			flash('Your passowrd has been updated, Now You are login now', 'success')
			logout_user()
			return redirect(url_for('users.login'))
		else:
			flash('Please enter correct old passowrd, New password not match', 'warning')
			return redirect(url_for('users.reset_pwd'))
	return render_template('reset_pwd.html', title='Reset Password', form=form)	


