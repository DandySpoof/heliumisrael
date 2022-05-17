from datetime import datetime, timedelta
from collections.abc import Mapping
from functools import wraps
from random import randint
from time import sleep
import requests as rq
import os

from flask import Flask, render_template, request, url_for, redirect, flash, send_from_directory
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship
from sqlalchemy import ForeignKey
from flask_login import LoginManager, UserMixin, login_user, login_required, current_user, logout_user, login_fresh
from flask_bootstrap import Bootstrap5
# from flask_wtf import FlaskForm
# from wtforms import StringField, SubmitField
# from wtforms.validators import DataRequired, URL

# from rq import Queue
# from worker import conn
# import utils

from dateutil import parser
from forms import CreatePostForm, NewUser, LoginForm, CommentForm, Confirm2faForm
from auth import request_verification_token, check_verification_token
from flask_gravatar import Gravatar
import psycopg2
import gunicorn
from twilio.rest import Client


# ESTABLISH CONNECTION TO WORKER
# q = Queue(connection=conn)

# --- CREATE and CONFING Flask APP
app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get("SECRET_KEY")

# CONNECT and CONFING DB
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get("DATABASE_URL", "sqlite:///helium-israel.db").replace(
	"postgres://", "postgresql://", 1)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

## CONNECTING BOOTSTRAP5 TO FLASK
bootstrap = Bootstrap5(app)

## CONNECTING AND CONFIGURING GRAVATAR
gravatar = Gravatar(app,
                    size=30,
                    rating='g',
                    default='retro',
                    force_default=False,
                    force_lower=False,
                    use_ssl=False,
                    base_url=None)


## ESTABLISH USER SESSIONS MANAGMENT
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"
login_manager.login_message = u"To view this page, you must login first"



@login_manager.user_loader
def load_user(user_id):
	return User.query.get(int(user_id))


## Construct data base tables

class Prices(db.Model):
	__tablename__ = "prices"
	id = db.Column(db.Integer, primary_key=True, nullable=False)
	date = db.Column(db.Text, nullable=False)
	price = db.Column(db.Float, nullable=False)

	def __repr__(self):
		return f"date: {self.date} - Price: {self.price}"


class User(UserMixin, db.Model):
	__tablename__ = "users"
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(50), nullable=False)
	phone = db.Column(db.Text, nullable=False)
	email = db.Column(db.String(70), unique=True, nullable=False)
	password = db.Column(db.Text, nullable=False)
	verified = db.Column(db.Boolean, nullable=False)
	allow_ads = db.Column(db.Boolean, nullable=False)
	role = db.Column(db.Text)
	time_stamp = db.Column(db.DateTime, nullable=False)

	wallets = relationship("Wallet", back_populates="user")
	posts = relationship("Post", back_populates="user")
	comments = relationship("Comment", back_populates="user")
	messages = relationship("Message", back_populates="user")

	def __repr__(self):
		return f"User ID: {self.id}"


class Wallet(db.Model):
	__tablename__ = "wallets"
	id = db.Column(db.Integer, primary_key=True, nullable=False)
	address = db.Column(db.Text, unique=True, nullable=False)
	balance = db.Column(db.Float)

	miners = relationship("Miner", back_populates="wallet")

	user_id = db.Column(db.Integer, ForeignKey("users.id"))
	user = relationship("User", back_populates="wallets")

	def __repr__(self):
		return f"Wallet: {self.address}"


class Post(db.Model):
	__tablename__ = "posts"
	id = db.Column(db.Integer, primary_key=True, nullable=False)
	category = db.Column(db.String(20), nullable=False)
	title = db.Column(db.String(40), nullable=False) #TODO Add input validation on front end / form
	subtitle = db.Column(db.String(60))
	body = db.Column(db.Text, nullable=False)
	approved = db.Column(db.Boolean, nullable=False)
	time_stamp = db.Column(db.DateTime, nullable=False)

	comments = relationship("Comment", back_populates="post")

	user_id = db.Column(db.Integer, ForeignKey("users.id"))
	user = relationship("User", back_populates="posts")

	def __repr__(self):
		return f"User {self.user_id} - post tile {self.title}"


class Comment(db.Model):
	__tablename__ = "comments"
	id = db.Column(db.Integer, primary_key=True, nullable=False)
	body = db.Column(db.Text, nullable=False) #TODO Add input validation on front end / form
	approved = db.Column(db.Boolean, nullable=False)
	time_stamp = db.Column(db.DateTime, nullable=False)

	user_id = db.Column(db.Integer, ForeignKey("users.id"))
	user = relationship("User", back_populates="comments")

	post_id = db.Column(db.Integer, ForeignKey("posts.id"))
	post = relationship("Post", back_populates="comments")


class Message(db.Model):
	__tablename__ = "messages"
	id = db.Column(db.Integer, primary_key=True, nullable=False)
	title = db.Column(db.String(120), nullable=False)  # TODO Add input validation on front end / form
	body = db.Column(db.Text, nullable=False) # TODO Add input validation on front end / form
	time_stamp = db.Column(db.DateTime, nullable=False)
	recipient = db.Column(db.Integer, nullable=False) #user id

	user_id = db.Column(db.Integer, ForeignKey("users.id"))
	user = relationship("User", back_populates="messages")


class Miner(db.Model):
	__tablename__ = "miners"
	id = db.Column(db.Integer, primary_key=True, nullable=False)
	name = db.Column(db.String(100), unique=True, nullable=False)
	address = db.Column(db.Text, nullable=False)
	added = db.Column(db.DateTime, nullable=False)
	city = db.Column(db.Text)
	country = db.Column(db.Text)
	street = db.Column(db.Text)
	online = db.Column(db.String(20))
	earnings_7 = db.Column(db.Float)
	earnings_30 = db.Column(db.Float)

	wallet_address = db.Column(db.Text, ForeignKey("wallets.address"))
	wallet = relationship("Wallet", back_populates="miners")

	def __repr__(self):
		return f"name: {self.name} - City: {self.city}"


class Activity(db.Model):
	__tablename__ = "activity_log"
	id = db.Column(db.Integer, primary_key=True, nullable=False)
	time_stamp = db.Column(db.DateTime, nullable=False)
	event = db.Column(db.Text, nullable=False)
	user_id = db.Column(db.Integer, primary_key=True, nullable=False)



# Line below only required once, for creating DB.
db.create_all()


##Security gateway function that allows only un-verified users (verified=0) to enter the verify route
def only_not_verified(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        if current_user.is_active and current_user.verified == False:
            return func(*args, **kwargs)
        print(type(current_user.verified))
        print("abort 403")
        return abort(403)

    return decorated_function


def get_oracle_price():
	try:
		response = rq.get("https://api.helium.io/v1/oracle/prices/current")
		response.raise_for_status()
	except:
		return 0
	response = response.json()
	price = str(response["data"]["price"])
	hnt = round(int(price) / 100000000 , 2)
	return hnt


## Construct APP structure
@app.route("/")
def home():
	hnt = get_oracle_price()
	print(hnt)

	def other_miners(wallet_address):
		""" This function returns the count of miners for the tested wallet .
		This function is activated from within the front-end templae."""
		wallet = Wallet.query.filter_by(address=wallet_address).first()
		owner_miners_count = len(wallet.miners)
		return owner_miners_count

	seven_days_backward = datetime.now() - timedelta(days=7)
	all_miners = Miner.query.all()
	latest_miners = [miner for miner in all_miners if miner.added > seven_days_backward and miner.country == "Israel"
	                 and miner.online == "online"]
	latest_miners_count = len(latest_miners)

	miners = Miner.query.filter_by(online="online", country="Israel").all()
	total_online_miners = len(miners)
	total_wallets_count = len(Wallet.query.all())

	return render_template("index.html", oracle_price=hnt, miners=miners, other_miners=other_miners,
	                       miners_count=total_online_miners, t_wallets=total_wallets_count, latest=latest_miners_count)


@app.route("/wallets")
def wallets():
	wallets = Wallet.query.all()
	hnt = get_oracle_price()

	def other_miners(wallet_address):
		""" This function returns the count of miners for the tested wallet .
		This function is activated from within the front-end templae."""
		wallet = Wallet.query.filter_by(address=wallet_address).first()
		owner_miners_count = len(wallet.miners)
		return owner_miners_count

	seven_days_backward = datetime.now() - timedelta(days=7)
	all_miners = Miner.query.all()
	latest_miners = [miner for miner in all_miners if miner.added > seven_days_backward and miner.country == "Israel"
	                 and miner.online == "online"]
	latest_miners_count = len(latest_miners)

	miners = Miner.query.filter_by(online="online", country="Israel").all()
	total_online_miners = len(miners)
	total_wallets_count = len(Wallet.query.all())


	return render_template("wallets.html", oracle_price=hnt, wallets=wallets, other_miners=other_miners, t_wallets=total_wallets_count,
	                       miners_count=total_online_miners, latest=latest_miners_count)


@app.route("/latest")
def latest_miners():
	hnt = get_oracle_price()

	def other_miners(wallet_address):
		""" This function returns the count of miners for the tested wallet .
		This function is activated from within the front-end templae."""
		wallet = Wallet.query.filter_by(address=wallet_address).first()
		owner_miners_count = len(wallet.miners)
		return owner_miners_count

	seven_days_backward = datetime.now() - timedelta(days=7)
	all_miners = Miner.query.all()
	latest_miners = [miner for miner in all_miners if miner.added > seven_days_backward and miner.country == "Israel"
	                 and miner.online == "online"]
	latest_miners_count = len(latest_miners)

	miners = Miner.query.filter_by(online="online", country="Israel").all()
	total_online_miners = len(miners)
	total_wallets_count = len(Wallet.query.all())


	return render_template("latest.html", oracle_price=hnt, miners=latest_miners, other_miners=other_miners,
	                       miners_count=total_online_miners, t_wallets=total_wallets_count, latest=latest_miners_count)


@app.route("/wallet/<address>")
def wallet(address):
	wallet = Wallet.query.filter_by(address=address).first()

	israel_miners = []
	abroad_miners = []
	for miner in wallet.miners:
		if miner.country == "Israel":
			israel_miners.append(miner)
		else:
			abroad_miners.append(miner)

	return render_template("wallet.html", miners=israel_miners, miners_abroad=abroad_miners, wallet=wallet)


@app.route("/register", methods=["GET", "POST"])
def register():
	form = NewUser()
	print(form.phone.data)
	if form.validate_on_submit():
		detected_user = User.query.filter_by(email=form.email.data).first()
		#TODO: need phone field cleanup for standardization

		if detected_user == None:
			hash = generate_password_hash(form.password.data, method='pbkdf2:sha256', salt_length=randint(8, 16))

			new_user = User(
				name=form.name.data,
				phone=form.phone.data,
				email=form.email.data,
				password=hash,
				verified=0,
				allow_ads=form.allow_ads.data,
				time_stamp=datetime.now(),
			)

			db.session.add(new_user)
			db.session.commit()

			login_user(new_user)
			# flash("Login successfully")
			print(f"New registration - {new_user}")

			phone = new_user.phone.strip().replace("-", "")
			request_verification_token(phone)

			return redirect(url_for("verify"))

		flash("This email is already registered. Try logging in instead.")
		return redirect(url_for("login"))

	return render_template("register.html", form=form)


@app.route("/verify", methods=["GET", "POST"])
@login_required
@only_not_verified
def verify():
	print(current_user)
	form = Confirm2faForm()

	if form.validate_on_submit():
		phone = current_user.phone.strip().replace("-", "")
		token = form.token.data
		# print(token)
		verification = check_verification_token(phone,token)
		# print(verification)

		if verification:
			current_user.verified = True
			db.session.commit()
			print("verified")
			return redirect(url_for("home"))
		else:
			flash("Wrong token - please try again.")
			print("Wrong token")

	return render_template("verify.html", form=form)


@app.route("/login", methods=["GET", "POST"])
def login():
	form = LoginForm()

	if form.validate_on_submit():
		user = User.query.filter_by(email=form.email.data).first()

		if user != None:
			if check_password_hash(user.password, form.password.data):
				login_user(user)
				return form.redirect("/")

			flash("Email or Password is incorrect. Please try again")

		flash("Email or Password is incorrect. Please try again")

	return render_template("login.html", form=form)



@app.route("/logout")
@login_required
def logout():
	logout_user()
	return redirect(url_for("home"))


@app.route("/price")
def price_chart():
	prices = Prices.query.all()
	tdy_avg = round(prices[-1].price,2)
	print(tdy_avg)
	hnt = get_oracle_price()

	return render_template("prices.html", prices=prices, oracle_price=hnt, daily_avarage=tdy_avg)


@app.route("/dashboard")
@login_required
def dashboard():
	# print(current_user.name)
	# return f"<p> {current_user.name} dashboard</p>"
	return render_template("dashboard.html")


@app.route("/contact")
def contact():
	return "<p> contact page</p>"



if __name__ == "__main__":
	app.run(debug=False)
