from collections.abc import Mapping
from datetime import datetime, timedelta
from random import randint
import requests as rq
from time import sleep
import os

from flask import Flask, render_template, request, url_for, redirect, flash, send_from_directory
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship
from sqlalchemy import ForeignKey
from flask_login import LoginManager, UserMixin, login_user, login_required, current_user, logout_user
from flask_bootstrap import Bootstrap5
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, URL
from dateutil import parser
from forms import CreatePostForm, NewUser, LoginForm, CommentForm
from flask_gravatar import Gravatar
import psycopg2
import gunicorn


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


## Construct miners data base

class User(UserMixin, db.Model):
	__tablename__ = "users"
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(50), nullable=False)
	phone = db.Column(db.Text, nullable=False)
	email = db.Column(db.String(70), unique=True, nullable=False)
	password = db.Column(db.Text, nullable=False)
	verified = db.Column(db.Boolean, nullable=False)

	wallets = relationship("Wallet", back_populates="user")

	def __repr__(self):
		return f"User ID: {self.id}"


# db.create_all()


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


# db.create_all()

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


# Line below only required once, when creating DB.
# db.create_all()

def get_miners_data():
	headers = {
		"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.51 Safari/537.36",
	}

	# Get all hotspots in Israel
	israel_box = {
		"cursor": None,
		"swlat": 29.4255538961337,
		"swlon": 34.46116814079567,
		"nelat": 33.03202086923252,
		"nelon": 35.613699832312264,
	}

	url = "https://api.helium.io/v1/hotspots/location/box"
	try:
		response = rq.get(url, headers=headers, params=israel_box)
		response.raise_for_status()
	except Exception as ex:
		print(ex)
		sleep(60)
		get_miners_data()

	data = response.json()

	miners = data["data"]
	# print(miners)

	time = datetime.now()
	last_7_days = time - timedelta(days=7)
	last_30_days = time - timedelta(days=30)

	count = 0
	for m in miners:
		sleep(2)
		count += 1
		print(f"{count} - {m['name']}")

		url = f"https://api.helium.io/v1/hotspots/{m['address']}/rewards/sum"
		parameters = {
			"max_time": time.isoformat(),
			"min_time": last_7_days.isoformat(),
		}
		try:
			response = rq.get(url, headers=headers, params=parameters)
			response.raise_for_status()
		except Exception as ex:
			print(f"{ex} sleep 15 sec")
			sleep(15)
			try:
				response = rq.get(url, headers=headers, params=parameters)
				response.raise_for_status()
			except Exception as ex:
				print(f"{ex} continiue")
				continue

		data_7 = response.json()
		earining_7 = float(data_7["data"]['sum']) / 100000000
		print(earining_7)
		sleep(2)

		url = f"https://api.helium.io/v1/hotspots/{m['address']}/rewards/sum"
		parameters = {
			"max_time": time.isoformat(),
			"min_time": last_30_days.isoformat(),
		}

		try:
			response = rq.get(url, headers=headers, params=parameters)
			response.raise_for_status()
		except Exception as ex:
			print(f"{ex} sleep 15 sec")
			sleep(15)
			try:
				response = rq.get(url, headers=headers, params=parameters)
				response.raise_for_status()
			except Exception as ex:
				print(f"{ex} continiue")
				continue

		data_30 = response.json()
		earining_30 = float(data_30["data"]['sum']) / 100000000
		print(earining_30)
		sleep(2)

		if Miner.query.filter_by(name=m['name']).first() == None:
			if m['geocode']['long_country'] == None:
				country = "Israel"
			else:
				country = m['geocode']['long_country']

			miner = Miner(
				name=m['name'],
				address=m['address'],
				added=parser.parse(m['timestamp_added']),
				city=m['geocode']['long_city'],
				country=country,
				street=m['geocode']['long_street'],
				online=m['status']['online'],
				earnings_7=earining_7,
				earnings_30=earining_30,
				wallet_address=m["owner"],
			)
			db.session.add(miner)

			print(miner)
			print(f"{m['name']} - whole record was added to db\n-------------------------------------------------->")
		else:
			# break  #USE this break to only update the db with new miners
			miner = Miner.query.filter_by(name=m['name']).first()

			if m['geocode']['long_country'] == None:
				country = "Israel"
			else:
				country = m['geocode']['long_country']

			miner.city = m['geocode']['long_city']
			miner.country = country #m['geocode']['long_country']
			miner.street = m['geocode']['long_street']
			miner.online = m['status']['online']
			miner.earnings_7 = earining_7
			miner.earnings_30 = earining_30

			print(miner)
			print("db recored udpated\n-------------------------------------------------->")

		if Wallet.query.filter_by(address=m["owner"]).first() == None:
			new_wallet = Wallet(
				address=m["owner"],
				balance=0,
			)
			db.session.add(new_wallet)

		try:
			db.session.commit()
		except Exception as ex:
			print(ex)
			print(ex.args)
			continue


# get_miners_data()


def get_other_wallets_data():
	wallets = Wallet.query.all()

	headers = {
		"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.51 Safari/537.36",
	}

	count = 0
	for w in wallets:
		url = f"https://api.helium.io/v1/accounts/{w.address}"
		try:
			response = rq.get(url, headers=headers)
			response.raise_for_status()
		except Exception as ex:
			print(f"{ex} sleep 15 sec")
			sleep(15)
			try:
				response = rq.get(url, headers=headers)
				response.raise_for_status()
			except Exception as ex:
				print(f"{ex} continiue")
				continue

		wallet_data = response.json()
		balance = int(wallet_data["data"]["balance"]) / 100000000
		if balance == None:
			w.balance = "N/A"
		else:
			w.balance = balance

		count += 1
		print(f"{count} - updated balnace for {w}  is: {balance} HNT")
		sleep(2)

		url = f"https://api.helium.io/v1/accounts/{w.address}/hotspots"
		try:
			response = rq.get(url, headers=headers)
			response.raise_for_status()
		except Exception as ex:
			print(f"{ex} sleep 15 sec")
			sleep(15)
			try:
				response = rq.get(url, headers=headers)
				response.raise_for_status()
			except Exception as ex:
				print(f"{ex} continiue")
				continue

		miners_for_wallet = response.json()
		for m in miners_for_wallet["data"]:
			time = datetime.now()
			if Miner.query.filter_by(address=m["address"]).first() == None:
				new_miner = Miner(
					name=m['name'],
					address=m['address'],
					added=time,
					city=m['geocode']['long_city'],
					country=m['geocode']['long_country'],
					street=m['geocode']['long_street'],
					online=m['status']['online'],
					earnings_7=0.0,
					earnings_30=0.0,
					wallet_address=m["owner"],
				)
				db.session.add(new_miner)

				print(new_miner)
				print(
					f"{m['name']} - A new, non-israeli miner was added to db\n---------------------------------------------->")


		db.session.commit()


# get_other_wallets_data()


def get_oracle_price():
	response = rq.get("https://api.helium.io/v1/oracle/prices/current")
	response = response.json()
	price = str(response["data"]["price"])
	hnt = f"${price[:2]}.{price[2:4]}"
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

@app.route("/register", methods=["GET", "POST"])
def register():
	form = NewUser()

	if form.validate_on_submit():
		detected_user = User.query.filter_by(email=form.email.data).first()
		hash = generate_password_hash(form.password.data, method='pbkdf2:sha256', salt_length=randint(8, 16))

		if detected_user == None:
			new_user = User(
				name=form.name.data,
				phone=form.phone.data,
				email=form.email.data,
				password=hash,
				verified="0"
			)

			db.session.add(new_user)
			db.session.commit()

			login_user(new_user)
			# flash("Login successfully")
			print("Login successfully")

			return redirect(url_for("home"))

		flash("This email is already registered. Try logging in instead.")
		return redirect(url_for("login"))

	return render_template("register.html", form=form)

@app.route("/logout")
@login_required
def logout():
	logout_user()
	return redirect(url_for("home"))

@app.route("/dashboard")
@login_required
def dashboard():
	print(current_user.name)
	return "<p> My dashboard</p>"

@app.route("/contact")
def contact():
	return "<p> contact page</p>"

if __name__ == "__main__":
	app.run(debug=False)
