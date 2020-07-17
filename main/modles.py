from datetime import datetime
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from main import db, login_manager, app
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
	return User.query.get(int(user_id))


class User(db.Model, UserMixin):
	id = db.Column(db.Integer, primary_key=True)
	usertype = db.Column(db.String(20), nullable=False, default='Admin')
	username = db.Column(db.String(20), unique=True, nullable=False)
	email = db.Column(db.String(120), unique=True, nullable=False)
	image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
	password = db.Column(db.String(60), nullable=False)
	userauth = db.Column(db.String(3), nullable=False, default='No')
	posts = db.relationship('Post', backref='author', lazy=True)
	booking = db.relationship('Booking', backref='author', lazy=True)

	def get_reset_token(self, expires_sec=1800):
		s = Serializer(app.config['SECRET_KEY'], expires_sec)
		return s.dumps({'user_id': self.id}).decode('utf-8')

	@staticmethod	
	def verify_reset_token(token):
		s = Serializer(app.config['SECRET_KEY'])
		try:
			user_id = s.loads(token)['user_id']
		except:
			return Nune

		return User.query.get(user_id)
		

	def __repr__(self):
		return f"User('{self.username}',{self.usertype}', '{self.email}','{self.image_file}',{self.userauth}' )"

class Post(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	title = db.Column(db.String(100), nullable=False)
	date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
	content = db.Column(db.Text, nullable=False) 
	user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

	def __repr__(self):
		return f"Post('{self.title}', '{self.date_posted}', '{self.content}')"


class Booking(db.Model):
#	__abstract__ = True
	id = db.Column(db.Integer, primary_key=True)
	bname = db.Column(db.String(50), nullable=False)
	baddress = db.Column(db.Text, nullable=False)
	bcontact = db.Column(db.String, nullable=False)
	bresort = db.Column(db.String, nullable=False)
	bref = db.Column(db.String, nullable=False, default='Self')
	bdate = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
	bdaynight = db.Column(db.String, nullable=False)
	brentcat = db.Column(db.String, nullable=False)
	bcat = db.Column(db.String, nullable=False, default='Self')
	bcatveg = db.Column(db.String, nullable=False, default='Veg')
	bgathconf = db.Column(db.Integer,nullable=False)
	bnote = db.Column(db.Text, nullable=False) 
	bauth = db.Column(db.String(10), nullable=False, default='No')
	user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

	def __repr__(self):
		return f"Booking('{self.bname}'),'{self.baddress}','{self.bcontact}','{self.bref}', '{self.bdate}', '{self.bdaynight}', '{self.brentcat}','{self.bcat}','{self.bcatveg}','{self.bgathconf}', '{self.bnote}')"
'''
			
'''
db.create_all()
