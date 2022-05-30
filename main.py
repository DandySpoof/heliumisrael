from datetime import datetime, timedelta
from collections.abc import Mapping
from functools import wraps
# from dateutil import parser
from random import randint
from time import sleep
import requests as rq
import os

from flask_login import LoginManager, UserMixin, login_user, login_required, current_user, logout_user, login_fresh, fresh_login_required
from flask import Flask, render_template, request, url_for, redirect, flash, send_from_directory, session, current_app
from flask_socketio import SocketIO, join_room, leave_room, emit, send, disconnect
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap5
from flask_session import Session
# from flask_wtf import FlaskForm

#Handle Client side Socket.io sessions
# import eventlet  ## will not work on Heroku
import gevent

from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.orm import relationship
from sqlalchemy import ForeignKey

# from wtforms import StringField, SubmitField
# from wtforms.validators import DataRequired, URL
# from rq import Queue
# from worker import conn
# import utils  ## will counse cyclic loading Error

from forms import CreatePostForm, NewUser, LoginForm, CommentForm, Confirm2faForm
from auth import request_verification_token, check_verification_token
from flask_gravatar import Gravatar
from twilio.rest import Client
import psycopg2
import gunicorn

# ESTABLISH CONNECTION TO WORKER
# q = Queue(connection=conn)


## --- CREATE and CONFING Flask APP
app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get("SECRET_KEY")
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get("DATABASE_URL", "sqlite:///helium-israel.db").replace(
	"postgres://", "postgresql://", 1)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SESSION_TYPE'] = "filesystem"

##ESTABLISH Database connection
db = SQLAlchemy(app)

## CONNECTING BOOTSTRAP5 TO FLASK
bootstrap = Bootstrap5(app)

## Establish Sessions managment
Session(app)
socketio = SocketIO(app, manage_session=False, logger=True, engineio_logger=True, cors_allowed_origins="*")

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
login_manager.refresh_view = "login"


@login_manager.user_loader
def load_user(user_id):
	return User.query.get(int(user_id))

# eventlet.monkey_patch()

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
	status = db.Column(db.Text)
	active_chats = db.Column(db.Text)

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
	chat_id = db.Column(db.Integer, ForeignKey("chats.id"))
	user_id = db.Column(db.Integer, ForeignKey("users.id"))
	body = db.Column(db.Text, nullable=False)
	time_stamp = db.Column(db.DateTime, nullable=False)
	recipient = db.Column(db.Integer, nullable=False) #recipiant user id
	read = db.Column(db.Boolean, nullable=False)

	chat = relationship("Chat", back_populates="messages")
	user = relationship("User", back_populates="messages")

	def __repr__(self):
		return f"(from user id: {self.user_id}, at: {str(self.time_stamp)[:16]}, chat id: {self.chat_id})"


class Chat(db.Model):
	__tablename__ = "chats"
	id = db.Column(db.Integer, primary_key=True, nullable=False)
	time_stamp = db.Column(db.DateTime, nullable=False)
	user_1 = db.Column(db.Integer, nullable=False)
	user_2 = db.Column(db.Integer, nullable=False)
	hide = db.Column(db.Boolean, nullable=False)
	l_time_stamp = db.Column(db.DateTime, nullable=False)

	messages = relationship("Message", back_populates="chat")

	def __repr__(self):
		return f"Chat id: {self.id}"


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
# db.create_all()


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

#Security gateway function that allows only admin (id=1) to enter defined routs
def admin_only(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        if current_user.is_active and current_user.role == "admin":
            return func(*args, **kwargs)
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
		print(detected_user)

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
			# print(phone)
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
				user.status = "online"
				db.session.commit()
				socketio.emit("user-login", current_user.get_id() ,broadcast=True)
				return form.redirect("/")

			flash("Email or Password is incorrect. Please try again")

		flash("Email or Password is incorrect. Please try again")

	return render_template("login.html", form=form)



@app.route("/logout")
@login_required
def logout():
	current_user.status = "offline"
	db.session.commit()
	socketio.emit("user-logout", current_user.get_id(), broadcast=True)

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
@fresh_login_required
@login_required
def dashboard():

	try:
		c_id = request.args.get("c_id")
		msgs =  Message.query.filter_by(chat_id=int(c_id)).all()
		unread_msgs = [msg for msg in msgs if msg.read == False and int(current_user.get_id()) != int(msg.user_id)]
		for msg in unread_msgs:
			msg.read = True
		db.session.commit()

		print(f"c_id - {c_id}")
		print(unread_msgs)
	except:
		pass

	# print(current_user.name)

	user_wallets = Wallet.query.filter_by(user_id=current_user.get_id()).all()
	user_posts = Post.query.filter_by(user_id=current_user.get_id()).all()
	user_messages = Message.query.filter_by(user_id=current_user.get_id()).all()
	as_user_1 = Chat.query.filter_by(user_1=current_user.get_id()).all()
	as_user_2 = Chat.query.filter_by(user_2=current_user.get_id()).all()
	user_chats = as_user_1 + as_user_2
	# print(current_user.get_id())

	chat_list = []
	for chat in user_chats:
		# print(chat)
		msgs = Message.query.filter_by(chat_id=chat.id).all()
		unread_msgs = 0
		for msg in msgs:
			if msg.read == False and int(msg.user_id) != int(current_user.get_id()):
				unread_msgs += 1

		if len(chat_list) == 0 :
			chat_list.append({"chat_object": chat, "unread_messages": unread_msgs})

		elif chat.l_time_stamp > chat_list[0]["chat_object"].l_time_stamp or unread_msgs > 0:
			chat_list.insert(0,{"chat_object": chat, "unread_messages": unread_msgs})

		else:
			chat_list.insert(1,{"chat_object": chat, "unread_messages": unread_msgs})

	print(chat_list)

	# print(user_chats)

	chat = 1

	return render_template("dashboard.html", user_wallets=user_wallets, user_posts=user_posts,
	                       user_messages=user_messages, miner_class=Miner, user_class=User, message_class=Message,
	                       user_chats=chat_list, chat=c_id, chat_class=Chat)

@app.route("/contact")
def contact():
	return "<p> contact page</p>"


def messageReceived(methods=['GET', 'POST']):
	print("Sucsess")
	return "console.log('message was received!!!')"

@socketio.on('my event')
def handle_my_custom_event(json, methods=['GET', 'POST']):
	try:
		print(f'new message event on chat id - {int(json["chat_id"])}' )
		print(json)
		chat = Chat.query.filter_by(id=int(json["chat_id"])).first()

		if int(current_user.get_id()) != int(chat.user_1):
			recipient = User.query.filter_by(id=chat.user_1).first()
		else:
			recipient = User.query.filter_by(id=chat.user_2).first()

		sender = User.query.filter_by(id=json["user_id"]).first()
		print(sender)
		json["sender_name"] = sender.name
		json["sender_mail"] = gravatar(sender.email)
		print(json)

		r_user = load_user(recipient.id)
		print(r_user)
		# TODO:handle disconnection of user from this chat


		print(json["sender_mail"])
		time_stamp = datetime.now()

		new_msg = Message(
		chat_id=int(json["chat_id"]),
		user_id=json["user_id"],
		body=json["message"],
		time_stamp=time_stamp,
		recipient=recipient.id,
		read=False
		)
		db.session.add(new_msg)

		chat.l_time_stamp = time_stamp

		db.session.commit()
	except:
		print(f'Chat entry event. User ID: {json["user_id"]} entered chat: {json["on_chat"]}')

		# TODO:handle disconnection od user
		pass


	socketio.emit('my response', json, callback=messageReceived)

@socketio.on('disconnect')
def test_disconnect():
    print('Client disconnected')

if __name__ == "__main__":
	socketio.run(app, debug=True)
	# app.run(debug=False)
