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
from forms import CreatePostForm, NewUser, Login, CommentForm
from flask_gravatar import Gravatar

# --- CREATE and CONFING Flask APP
app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get("SECRET_KEY")

#CONNECT and CONFING DB
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get("DATABASE_URL", "sqlite:///helium-israel.db").replace("postgres://", "postgresql://", 1)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

## CONNECTING BOOTSTRAP5 TO FLASK
bootstrap = Bootstrap5(app)

## CONNECTING AND CONFIGURING GRAVATAR
gravatar = Gravatar(app,
                    size=100,
                    rating='g',
                    default='retro',
                    force_default=False,
                    force_lower=False,
                    use_ssl=False,
                    base_url=None)


## ESTABLISH USER SESSIONS MANAGMENT
login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


## Construct miners data base

class User(UserMixin, db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    phone = db.Column(db.Text)
    email = db.Column(db.String(70), unique=True, nullable=False)
    password = db.Column(db.Text, nullable=False)

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

db.create_all()


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

	wallet_address = db.Column(db.Integer, ForeignKey("wallets.address"))
	wallet = relationship("Wallet", back_populates="miners")

	def __repr__(self):
		return f"name: {self.name} - City: {self.city} - earining 30 days: {self.earnings_30}"


# Line below only required once, when creating DB.
db.create_all()

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
	response = rq.get(url, headers=headers, params=israel_box)
	response.raise_for_status()
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
		response = rq.get(url, headers=headers, params=parameters)
		response.raise_for_status()
		data_7 = response.json()
		earining_7 = float(data_7["data"]['sum']) / 100000000
		print(earining_7)
		sleep(2)

		url = f"https://api.helium.io/v1/hotspots/{m['address']}/rewards/sum"
		parameters = {
			"max_time": time.isoformat(),
			"min_time": last_30_days.isoformat(),
		}
		response = rq.get(url, headers=headers, params=parameters)
		response.raise_for_status()
		data_30 = response.json()
		earining_30 = float(data_30["data"]['sum']) / 100000000
		print(earining_30)
		sleep(2)

		if Miner.query.filter_by(name=m['name']).first() == None:
			miner = Miner(
				name=m['name'],
				address=m['address'],
				added=parser.parse(m['timestamp_added']),
				city=m['geocode']['long_city'],
				country=m['geocode']['long_country'],
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
			miner = Miner(
				city=m['geocode']['long_city'],
				country=m['geocode']['long_country'],
				street=m['geocode']['long_street'],
				online=m['status']['online'],
				earnings_7=earining_7,
				earnings_30=earining_30,
			)

			print(miner)
			print("db recored udpated\n-------------------------------------------------->")

		if Wallet.query.filter_by(address=m["owner"]).first() == None:
			wallet = Wallet(
				address=m["owner"],
			)
			db.session.add(wallet)

		db.session.commit()


get_miners_data()



## Construct APP structure
@app.route("/")
def home():
	response = rq.get("https://api.helium.io/v1/oracle/prices/current")
	response = response.json()
	price = str(response["data"]["price"])
	hnt = f"${price[:2]}.{price[2:4]}"
	print(hnt)

	def other_miners(wallet_address):
		""" This function checks if an owner (wallet) of a miner own other miners and returns the count of miners
		associated with this wallet. This function is activated from within the front-end templae."""
		wallet = Wallet.query.filter_by(address=wallet_address).first()
		owner_miners_count = len(wallet.miners)
		return owner_miners_count

	miners = Miner.query.filter_by(online="online").all()
	total_online_miners = len(miners)
	total_wallets_count = len(Wallet.query.all())

	return render_template("index.html", oracle_price=hnt, miners=miners, other_miners=other_miners,
	                       miners_count=total_online_miners, wallets=total_wallets_count)


@app.route("/wallet/<address>")
def wallet(address):
	wallet = Wallet.query.filter_by(address=address).first()
	miners = wallet.miners
	print(miners)

	return render_template("wallet.html", miners=miners, wallet=wallet)


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
				password=hash)

			db.session.add(new_user)
			db.session.commit()

			login_user(new_user)
			# flash("Login successfully")
			print("Login successfully")

			return form.redirect('home')

		flash("This email is already registered. Try logging in instead.")
		form.redirect("login")

	return render_template("register.html", form=form)



if __name__ == "__main__":
	app.run(debug=False)