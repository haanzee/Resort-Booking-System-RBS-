date 04/10/2019

dealing with passowrd
=======================

pip install flask-bcrypt

go to pyhon shell

from flask_bcrypt import Bcrypt

bcrypt= Bcrypt()
bcrypt.generate_password_hash('testing')
bcrypt.generate_passowrd_hash('testing').decode('utf-8')
hashed_pw = bcrypt.generate_passowrd_hash('testing').decode('utf-8')
bcrypt.check_password_hash(hashed_pw, 'testing')


form validation

login system {19:47}

pip install flask-login



