import re
from flask_bcrypt import Bcrypt
from flask import Flask
app = Flask(__name__)
app.secret_key = 'keythatisasecret'
bcrypt = Bcrypt(app)

DATABASE = 'paintings_db'
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
PASSWORD_REGEX = re.compile(r'^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9])(?=.*?[#?!@$ %^&*-]).{8,}$')
NAME_REGEX = re.compile(r'^[a-zA-Z]+$')