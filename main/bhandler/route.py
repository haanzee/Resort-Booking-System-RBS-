# bhandler/routes.py
from sqlalchemy import exc, extract
from main import db
from datetime import datetime, date, timedelta, time    
from flask import (render_template, url_for, flash,
                   redirect, request, abort, Blueprint)
from flask_login import current_user, login_required
from main.modles import Booking, User
from main.bhandler.forms import BookingForm, UpdateBookingForm, SBookingForm
from sqlalchemy import func, and_, cast, Date

from flask import Blueprint
bhandler = Blueprint('bhandler', __name__)


@bhandler.route('/booking', methods=['GET', 'POST'])
@login_required
def booking():
	form = BookingForm()
	if form.validate_on_submit():
		s_date = form.bdate.data
		sr_date = s_date.strftime("%d/%m/%Y")
		bresort = form.bresort.data
		res = db.session().query(Booking.id
			).filter(Booking.bresort== bresort
			).filter(Booking.bdaynight== form.bdaynight.data
			).filter(Booking.bdate >= datetime.strptime(sr_date, '%d/%m/%Y'),
		Booking.bdate <= datetime.strptime(sr_date, '%d/%m/%Y')).first()

		if res == None:
			booking = Booking(bname=form.bname.data, 
				baddress=form.baddress.data, 
				bcontact=form.bcontact.data, 
				bresort=form.bresort.data, 
				bref=form.bref.data, 
				bdate=form.bdate.data,
				bdaynight=form.bdaynight.data, 
				brentcat=form.brentcat.data,
				bcat=form.bcat.data,
				bcatveg=form.bcatveg.data,   
				bgathconf=form.bgathconf.data, 
				bnote=form.bnote.data, 
				author=current_user)
			db.session().add(booking)
			db.session().commit()
			flash('New Booking sucessfully Added', 'success')
			return redirect('/dash_index')
		else:
			flash('Date Already Booked', 'info')
			return redirect('/booking')
	return render_template('booking.html', title='Register', form=form)

@bhandler.route("/UpdateBooking/<string:id>" , methods=['GET', 'POST'])
@login_required
def UpdateBooking(id):
	entries = Booking.query.order_by(Booking.id.asc())
	entry = Booking.query.get(id)
	form = UpdateBookingForm(obj=entry)
	if form.validate_on_submit():
		s_date = form.bdate.data
		sr_date = s_date.strftime("%d/%m/%Y")
		bresort = form.bresort.data
		res = db.session().query(Booking.id, Booking.bauth
			).filter(Booking.bresort== bresort
			).filter(Booking.bdaynight== form.bdaynight.data
			).filter(Booking.bdate >= datetime.strptime(sr_date, '%d/%m/%Y'),
			Booking.bdate <= datetime.strptime(sr_date, '%d/%m/%Y'))
		if res.count() == 1 :
			booking = Booking.query.filter_by(id=id).first()
			booking.bname = request.form['bname']
			booking.baddress = request.form['baddress']
			booking.bcontact = request.form['bcontact']
			booking.bresort = request.form['bresort']
			booking.bref = request.form['bref']
			booking.bdate = form.bdate.data
			booking.bdaynight = request.form['bdaynight']
			booking.brentcat = request.form['brentcat']
			booking.bcat=request.form['bcat']
			booking.bcatveg = request.form['bcatveg']
			booking.bgathconf = request.form['bgathconf']
			booking.bnote = request.form['bnote']
			booking.bauth = 'No'
			db.session().commit()
			flash('Your account has been updated!', 'success')
			return redirect('/dash_index')
		else:
			flash('Date Already Booked ....', 'info')
			return redirect('/booking')
	return render_template('editbooking.html', entries=entries, form=form)


@bhandler.route("/show/")
@login_required
def show():
	booking = Booking.query.filter_by(bauth='No').all()
	return render_template('show.html', booking=booking)

@bhandler.route("/showAuthPending/<string:id>", methods = ['GET', 'POST'])
@login_required
def showAuthPending(id):
	rec = Booking.query.filter_by(id=id).first()
	return render_template('showAuthPending.html', rec=rec)


@bhandler.route("/auth/<string:id>", methods = ['GET', 'POST'])
@login_required
def auth(id):
	booking = Booking.query.filter_by(id=id).first()
	booking.bauth = 'Yes'
	db.session().commit()
	return redirect('/dash_index')

@bhandler.route("/un_auth/<string:id>", methods = ['GET', 'POST'])
@login_required
def un_auth(id):
	booking = Booking.query.filter_by(id=id).first()
	booking.bauth = 'No'
	db.session().commit()
	return redirect('/dash_index')


@bhandler.route("/Delete/<string:id>", methods = ['GET', 'POST'])
@login_required
def Delete(id):

	Booking.query.filter_by(id=id).delete()
	db.session().commit()
	flash('Booking sucessfully Deleted', 'success')
	return redirect('/dash_index')

@bhandler.route("/edit/<string:id>", methods = ['GET', 'POST'])
@login_required
def edit(id):
	editbkg = Booking.query.filter_by(id=id).first()
	return render_template('editbooking.html', editbkg=editbkg)


@bhandler.route("/edit_data/<string:id>", methods = ['GET', 'POST'])
@login_required
def edit_data(id):
	booking = Booking.query.filter_by(id=id).first()
	booking.bname = request.form['bname'] 
	booking.baddress = request.form['baddress'] 
	booking.bcontact = request.form['bcontact'] 
	booking.bresort = request.form['bresort'] 
	booking.bref = request.form['bref'] 
	booking.bdate = request.form['bdate']
	booking.bdaynight = request.form['bdaynight'] 
	booking.brentcat = request.form['brentcat']
	booking.bcat = request.form['bcat']
	booking.bcatveg = request.form['bcatveg']
	booking.bgathconf = request.form['bgathconf'] 
	booking.bnote = request.form['bnote']
	db.session().commit()
	flash('Booking Record has been updated!', 'success')
	return redirect('/dash_index')

@bhandler.route('/dash_index')
@login_required
def dash_index():
	res = db.session().query(Booking.bresort,Booking.bdate,
		func.count(Booking.bresort).label('count')
		).filter(Booking.bauth=='Yes'
		).filter(Booking.bdate >= datetime.now()
		).group_by(Booking.bresort
		).all()
	resno = db.session().query(Booking.bresort,Booking.bdate,
		func.count(Booking.bresort).label('count')
		).filter(Booking.bauth=='No'
		).filter(Booking.bdate >= datetime.now()
		).group_by(Booking.bresort
		).all()
	return render_template('dash_index.html', res=res, resno = resno)

# -------- without login
# -------- Group by Resort

@bhandler.route('/sindex')
def sindex():
	res = db.session().query(Booking.bresort,Booking.bdate,
		func.count(Booking.bresort).label('count')
		).filter(Booking.bauth=='Yes'
		).filter(Booking.bdate >= datetime.now()
		).group_by(Booking.bresort
		).all()
	return render_template('sindex.html', res=res)

#---------Group by Date Index

@bhandler.route("/sindexdate/")
@login_required
def sindexdate():
	bdate=request.args['bdate']
	bresort=request.args['bresort']	
	res = db.session().query(Booking.bresort,Booking.bdate,
	func.count(Booking.bdate).label('count')
	).filter(Booking.bauth=='Yes'
	).filter(Booking.bresort== bresort 
	).filter(Booking.bdate >= datetime.now() 
	).group_by(Booking.bdate
	).all()
	return render_template('sindexdate.html', res=res, bresort=bresort)

#---------Group by Month Index

@bhandler.route("/sindexmonth/<string:bresort>", methods = ['GET', 'POST'])
@login_required
def sindexmonth(bresort):
	res = db.session().query(Booking.bresort,Booking.bdate,
		func.count(Booking.bdate).label('count')
		).filter(Booking.bauth=='Yes'
		).filter(Booking.bresort== bresort
		).filter(Booking.bdate >= datetime.now() 
		).group_by(func.strftime('%m-%Y', Booking.bdate)
		).all()
	return render_template('sindexmonth.html', res=res, bresort=bresort)

# ----------One Date search detail

@bhandler.route("/sindexdateone/")
@login_required
def sindexdateone():
	bdate=request.args['bdate']
	bresort=request.args['bresort']
	res = db.session().query(Booking.id,Booking.bname,Booking.bdaynight,Booking.brentcat,Booking.bgathconf, Booking.bresort,Booking.bdate
		).filter(Booking.bauth=='Yes'
		).filter(Booking.bresort== bresort
		).filter(Booking.bdate >= datetime.strptime(bdate, '%d/%m/%Y'),
		Booking.bdate <= datetime.strptime(bdate, '%d/%m/%Y')).all()
	return render_template('sindexdateone.html', res=res, bresort=bresort)


@bhandler.route("/sindexdateoneshow/<string:id>", methods = ['GET', 'POST'])
@login_required
def sindexdateoneshow(id):
	res = Booking.query.filter_by(bauth='Yes').filter_by(id=id).all()
	return render_template('sindexdateoneshow.html', res=res, id=id)


@bhandler.route("/resort_index/<string:bresort>", methods = ['GET', 'POST'])
@login_required
def resort_index(bresort):
	res = Booking.query.filter_by(bauth='Yes'
	).filter(Booking.bdate >= datetime.now()
	).filter_by(bresort=bresort).all()
	return render_template('resort_index.html', res=res, bresort=bresort)

@bhandler.route("/resort_indexp/<string:bresort>", methods = ['GET', 'POST'])
@login_required
def resort_indexp(bresort):

	res = Booking.query.filter_by(bauth='No'
	).filter(Booking.bdate >= datetime.now()
	).filter_by(bresort=bresort).all()
	return render_template('resort_indexp.html', res=res, bresort=bresort)

@bhandler.route("/bkingAuthShow/<string:id>", methods = ['GET', 'POST'])
@login_required
def bkingAuthShow(id):
	res = Booking.query.filter_by(bauth='Yes').filter_by(id=id).all()
	return render_template('bkingAuthShow.html', res=res, id=id)

@bhandler.route('/sbooking', methods=['GET', 'POST'])
def sbooking():
	form = SBookingForm()
	if form.validate_on_submit():
		s_date = form.bdate.data
		sr_date = s_date.strftime("%Y-%m-%d")

		if form.bresort.data=='Sona Grand':
			rec = Booking.query.filter(Booking.bresort == 'Sona Grand'
				).filter(Booking.bauth == 'Yes'
				).filter(Booking.bdate >= datetime.strptime(sr_date, '%Y-%m-%d'),
                  Booking.bdate <= datetime.strptime(sr_date, '%Y-%m-%d')).all()
			recn = Booking.query.filter(Booking.bresort == 'Sona Grand'
				).filter(Booking.bauth == 'No'
				).filter(Booking.bdate >= datetime.strptime(sr_date, '%Y-%m-%d'),
                  Booking.bdate <= datetime.strptime(sr_date, '%Y-%m-%d')).all()
			return render_template('sbookingrec.html', rec=rec, recn=recn, sr_date=sr_date)
		elif form.bresort.data=='Siddhartha':
			rec = Booking.query.filter(Booking.bresort == 'Siddhartha'
				).filter(Booking.bauth == 'Yes'
				).filter(Booking.bdate >= datetime.strptime(sr_date, '%Y-%m-%d'),
                  Booking.bdate <= datetime.strptime(sr_date, '%Y-%m-%d')).all()
			recn = Booking.query.filter(Booking.bresort == 'Siddhartha'
				).filter(Booking.bauth == 'No'
				).filter(Booking.bdate >= datetime.strptime(sr_date, '%Y-%m-%d'),
                  Booking.bdate <= datetime.strptime(sr_date, '%Y-%m-%d')).all()
			return render_template('sbookingrec.html', rec=rec, recn=recn, sr_date=sr_date)
		else:
			rec = Booking.query.filter(Booking.bauth == 'Yes'
				).filter(Booking.bdate >= datetime.strptime(sr_date, '%Y-%m-%d'),
                  Booking.bdate <= datetime.strptime(sr_date, '%Y-%m-%d')).all()
			recn = Booking.query.filter(Booking.bauth == 'No'
				).filter(Booking.bdate >= datetime.strptime(sr_date, '%Y-%m-%d'),
                  Booking.bdate <= datetime.strptime(sr_date, '%Y-%m-%d')).all()
			return render_template('sbookingrec.html', rec=rec, recn=recn, sr_date=sr_date)
	return render_template('sbooking.html', title='Date Status',
		form=form, legend='Date Status')

@bhandler.route("/sbookingrec/<string:id>", methods = ['GET', 'POST'])
@login_required
def sbookingrec(id):
	res = Booking.query.filter_by(bauth='Yes').filter_by(id=id).all()
	return render_template('bkingAuthShow.html', res=res, id=id)
