from flask_wtf import FlaskForm
from flask import request, url_for, redirect
from wtforms import StringField, SubmitField, PasswordField, EmailField, HiddenField, BooleanField
from wtforms.validators import DataRequired, URL, Email
from flask_ckeditor import CKEditorField
from flask_login import UserMixin
from urllib.parse import urlparse, urljoin
# from urlparse2 import urlparse2
# from urlparse2 import urlparse1

# def is_safe_url(target):
#     ref_url = urlparse2.urlparse(request.host_url)
#     test_url = urlparse2.urlparse(urlparse2.urljoin(request.host_url, target))
#     return test_url.scheme in ('http', 'https') and \
#            ref_url.netloc == test_url.netloc

def is_safe_url(target):
    ref_url = urlparse(request.host_url)
    test_url = urlparse(urljoin(request.host_url, target))
    return test_url.scheme in ('http', 'https') and \
           ref_url.netloc == test_url.netloc

def get_redirect_target():
	for target in request.args.get('next'), request.referrer:
		if not target:
		    continue
		if is_safe_url(target):
			return target


class RedirectForm(FlaskForm):
	next = HiddenField()

	def __init__(self, *args, **kwargs):
		FlaskForm.__init__(self, *args, **kwargs)
		if not self.next.data:
			self.next.data = get_redirect_target() or ''

	def redirect(self, endpoint="home", **values):
		if is_safe_url(self.next.data):
			return redirect(self.next.data)
		target = get_redirect_target()
		return redirect(target or url_for(endpoint, **values))


##WTForm
class CreatePostForm(FlaskForm):
	title = StringField("Blog Post Title", validators=[DataRequired("Please enter title")])
	subtitle = StringField("Subtitle", validators=[DataRequired("Please enter subtitle")])
	img_url = StringField("Blog Image URL", validators=[DataRequired("Please enter url"), URL("Please enter a valid url")])
	body = CKEditorField("Blog Content", validators=[DataRequired("Please write somthing")])
	submit = SubmitField("Submit Post")


class NewUser(UserMixin, FlaskForm):
	name = StringField("Name:*", validators=[DataRequired("Please enter your name")])
	email = EmailField("Email:*", validators=[DataRequired("Please enter your email"),
	                                         Email("Please enter a valid email address")])
	phone = StringField("Phone:*", validators=[DataRequired("Please enter your password")])
	password = PasswordField("Password:*", validators=[DataRequired("Please enter your password")])
	allow_ads = BooleanField("Keep me updated (no spam, we promise)", default="checked", false_values="0")
	submit = SubmitField("Register")


class LoginForm(RedirectForm):
	email = EmailField("Email:", validators=[DataRequired("Please enter your email"),
	                                         Email("Please enter a valid email address")])
	password = PasswordField("Password:", validators=[DataRequired("Please enter your password")])
	submit = SubmitField("Register")

class CommentForm(FlaskForm):
	body = CKEditorField("Comment", validators=[DataRequired("Please write somthing")])
	submit = SubmitField("Submit Comment")

class Confirm2faForm(FlaskForm):
    token = StringField('Token')
    submit = SubmitField('Verify')