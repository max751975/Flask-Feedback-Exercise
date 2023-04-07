from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, EmailField, TextAreaField
from wtforms.validators import InputRequired, Length

class UserForm(FlaskForm):
    """User registration form"""
    
    username = StringField("Username", validators=[InputRequired(), Length(max=20)], render_kw={'autofocus': True})
    password = PasswordField("Password", validators=[InputRequired(), Length(max=55)])
    email = EmailField("E-mail", validators=[InputRequired()])
    first_name = StringField("First Name", validators=[InputRequired(), Length(max=30)])
    last_name = StringField("Last Name", validators=[InputRequired(), Length(max=30)])

    
class LoginForm(FlaskForm):
    """User login form"""
    
    username = StringField("Username", validators=[InputRequired()], render_kw={'autofocus': True})
    password = PasswordField("Password", validators=[InputRequired()])

    
class FeedbackForm(FlaskForm):
    """Add feedback form."""

    title = StringField("Title",validators=[InputRequired(), Length(max=100)], render_kw={'autofocus': True})
    text = TextAreaField("Content", validators=[InputRequired()])