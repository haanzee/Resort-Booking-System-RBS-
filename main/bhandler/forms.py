import os
from datetime import datetime, date, timedelta    
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField, SelectField, TextAreaField, IntegerField, DateField
#from wtforms.fields.html5 import DateField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from flask_login import current_user
from main.modles import User

class BookingForm(FlaskForm):

	bname = StringField('Booking Name',
			 validators=[DataRequired(), Length(min=5, max=30)])
	baddress = TextAreaField('Addess', validators=[DataRequired()])
	bcontact = StringField('Contact Number',
			 validators=[DataRequired(), Length(min=5, max=30)])
	bresort = SelectField('Booking For', choices = [('Sona Grand', 'Sona Grand'),('Siddhartha', 'Siddhartha')])	 
	bref = StringField('Booking Reference')	
	bdate = DateField('Booking Date (dd/mm/yyyy)',format='%d/%m/%Y')	
	bdaynight = SelectField('Booking', choices = [('Day', 'Day'),('Night', 'Night')])	 
	brentcat = SelectField('Booking Type', choices = [('Catering', 'Catering'),('Rent', 'Rent')])	
	bcat =	SelectField('Booking Catter', choices = [('Self', 'Self'),('Out-Door', 'Out-Door')])
	bcatveg = SelectField('Booking Menu Type', choices = [('Veg', 'Veg'),('Non-Veg', 'Non-Veg')])
	bgathconf = IntegerField('Confirm Gathering')
	bnote = TextAreaField('Notes', validators=[DataRequired()])
	submit = SubmitField('Booking')
'''
	def validate_bdate(form, field):
		if field.data < datetime.utcnow:
			raise ValidationError("End date must not be earlier than start date.")
'''

class UpdateBookingForm(FlaskForm):

	bname = StringField('Booking Name',
			 validators=[DataRequired(), Length(min=5, max=30)])
	baddress = TextAreaField('Addess', validators=[DataRequired()])
	bcontact = StringField('Contact Number',
			 validators=[DataRequired(), Length(min=5, max=30)])
	bresort = SelectField('Booking For', choices = [('Sona Grand', 'Sona Grand'),('Siddhartha', 'Siddhartha')])	 
	bref = StringField('Booking Reference')	
	bdate = DateField('Booking Date (dd/mm/yyyy',format='%d/%m/%Y')	
	bdaynight = SelectField('Booking', choices = [('Day', 'Day'),('Night', 'Night')])	 
	brentcat = SelectField('Booking Type', choices = [('Catering', 'Catering'),('Rent', 'Rent')])	
	bcat =	SelectField('Booking Catter', choices = [('Self', 'Self'),('Out-Door', 'Out-Door')])
	bcatveg = SelectField('Booking Menu Type', choices = [('Veg', 'Veg'),('Non-Veg', 'Non-Veg')])
	bgathconf = IntegerField('Confirm Gathering')
	bnote = TextAreaField('Notes', validators=[DataRequired()])
	submit = SubmitField('Update Booking')
	
class SBookingForm(FlaskForm):
	bdate = DateField('Search Date (dd/mm/yyyy)',format='%d/%m/%Y')	
	bresort = SelectField('Booking For', choices = [('Sona Grand', 'Sona Grand'),('Siddhartha', 'Siddhartha'), ('Both', 'Both') ])	 
	submit = SubmitField(' Search ')
