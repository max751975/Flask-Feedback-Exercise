from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

db = SQLAlchemy()

bcrypt = Bcrypt()


def connect_db(app):
    """Connect to database."""

    db.app = app
    db.init_app(app)

class User(db.Model):
    """Site user."""

    __tablename__ = "users"

    id = db.Column(db.Integer, nullable=False, primary_key=True)
    username = db.Column(db.String(20), nullable=False, unique=True)
    password = db.Column(db.Text, nullable=False)
    email = db.Column(db.String(50), nullable=False)
    first_name = db.Column(db.String(30), nullable=False)
    last_name = db.Column(db.String(30), nullable=False)

    feedback = db.relationship("Feedback", backref="user", cascade="all,delete")
    
        # register user
    @classmethod
    def register(cls, username, pwd, email, first_name, last_name):
        """Register user with hashed password and return user"""
        hashed = bcrypt.generate_password_hash(pwd)
        # return is byte-string. Turn it to normal string
        hashed_utf8 = hashed.decode("utf8")
        
        # return instance of user with username and hashed pwd
        user = cls(username=username, password=hashed_utf8, email=email, first_name=first_name, last_name=last_name)
        return user
    
    
    # authenticate user
    @classmethod
    def authenticate(cls, username, pwd):
        """Validate existance of the user and check if password is correct.
        Return user if valid, else False"""
        
        u = User.query.filter_by(username=username).first()
        
        if u and bcrypt.check_password_hash(u.password, pwd):
            return u
        else:
            return False
        
class Feedback(db.Model):
    
    __tablename__ =  'feedback'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(100), nullable=False)
    text = db.Column(db.Text, nullable=False)
    username = db.Column(db.String(20), db.ForeignKey('users.username'), nullable=False)