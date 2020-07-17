from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField, SelectField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from flask_login import current_user
from main.modles import User

class RegistrationForm(FlaskForm):
	usertype = SelectField('Login Type', choices = [('Admin', 'Admin'),('Manager', 'Manager')])
	username = StringField('username', 
		validators=[DataRequired(), Length(min=2, max=20)])
	email = StringField('Email', 
		validators=[DataRequired(), Email()])
	password = PasswordField('Password', 
		validators=[DataRequired()])
	confirm_password = PasswordField('Confirm Password',
		validators=[DataRequired(), EqualTo('password')])
	submit = SubmitField('sign up')
	def validate_username(self, username):
		user = User.query.filter_by(username=username.data).first()
		if user:
			raise ValidationError('That Username already tekan by another one')
	def validate_email(self, email):
		user = User.query.filter_by(email=email.data).first()
		if user:
			raise ValidationError('That Email Already tekan by someone, Please Choose Different one')



#############################################
class LoginForm(FlaskForm):
	
	usertype = SelectField('Login Type', choices = [('Admin', 'Admin'),('Manager', 'Manager')])
	email = StringField('Email', 
		validators=[DataRequired(), Email()])
	password = PasswordField('Password', 
		validators=[DataRequired()])
	remember = BooleanField('Remember Me')
	submit = SubmitField('Login')


class UpdateAccountForm(FlaskForm):
	username = StringField('username', 
		validators=[DataRequired(), Length(min=2, max=20)])
	email = StringField('Email', 
		validators=[DataRequired(), Email()])
	picture = FileField('Update Profile Picture', validators=[FileAllowed(['jpg', 'png'])])
	submit = SubmitField('Update')
	def validate_username(self, username):
		if username.data != current_user.username:
			user = User.query.filter_by(username=username.data).first()
			if user:
				raise ValidationError('That Username already tekan by another one')
	def validate_email(self, email):
		if email.data != current_user.email:
			user = User.query.filter_by(email=email.data).first()
			if user:
				raise ValidationError('That Email Already tekan by someone, Please Choose Different one')


class RequestResetForm(FlaskForm):
	email = StringField('Email', 
		validators=[DataRequired(), Email()])
	submit = SubmitField('Request Password Reset')

	def validate_email(self, email):
		user = User.query.filter_by(email=email.data).first()
		if user is None:
			raise ValidationError('There is no account with that email, You must register first.')

class ResetPasswordForm(FlaskForm):
		password = PasswordField('Password', 
			validators=[DataRequired()])
		confirm_password = PasswordField('Confirm Password',
			validators=[DataRequired(), EqualTo('password')])
		submit = SubmitField('Reset Passord')

class ResetPasswordDirectForm(FlaskForm):
		oldpassword = PasswordField('Old Password', 
			validators=[DataRequired()])
		password = PasswordField('New Password', 
			validators=[DataRequired()])
		confirm_password = PasswordField('Confirm New Password',
			validators=[DataRequired(), EqualTo('password')])
		submit = SubmitField('Reset Passord')

