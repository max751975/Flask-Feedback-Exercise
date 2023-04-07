from flask import Flask, render_template, redirect, session, flash
from flask_debugtoolbar import DebugToolbarExtension
from models import connect_db, db, User, Feedback
from forms import UserForm, LoginForm, FeedbackForm
from sqlalchemy.exc import IntegrityError
from sqlalchemy import desc

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql:///feedback_db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_ECHO"] = True
app.config["SECRET_KEY"] = "abc123"

app.app_context().push()

connect_db(app)
db.create_all()

toolbar = DebugToolbarExtension(app)
app.config["DEBUG_TB_INTERCEPT_REDIRECTS"] = False

@app.route("/")
def home_page():
    feedbacks = Feedback.query.order_by(desc(Feedback.id)).all()
    return render_template('/index.html', feedbacks=feedbacks)

@app.route("/register", methods=["GET","POST"])
def user_sign_up():
    form = UserForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        email = form.email.data
        first_name = form.first_name.data
        last_name = form.last_name.data
        new_user = User.register(username, password, email, first_name, last_name)
        db.session.add(new_user)
        db.session.commit()
        # session['user_id'] = new_user.id
        # session['username'] = new_user.username
        return redirect('/login')
    return render_template('/register.html', form=form)

@app.route("/login", methods=["GET", "POST"])
def user_login():
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        
        user = User.authenticate(username, password)
        if user:
            flash(f"Welcome, { user.username }")
            session['user_id'] = user.id
            session['username'] = user.username
            return redirect(f"/users/{user.id}")
        else:
            form.username.errors = ['Invalid username/password']
    return render_template('/login.html', form=form)

@app.route("/users/<int:id>", methods=["GET", "POST"])
def user_info(id):
    form = FeedbackForm()
    user = User.query.get_or_404(id)
    all_user_feedbacks = Feedback.query.filter_by(username=user.username).order_by(Feedback.id).all()
    if form.validate_on_submit():
        title = form.title.data
        text = form.text.data
        new_feedback = Feedback(title=title, text=text, username=user.username)
        db.session.add(new_feedback)
        db.session.commit()
        return redirect(f'/users/{user.id}')
    return render_template('/user_info.html', form=form, user=user, feedbacks=all_user_feedbacks)

@app.route("/logout")
def user_logout():
    flash("Good Bye!")
    session.pop("user_id")
    session.pop("username")
    return redirect('/')

@app.route("/users/<int:user_id>/delete", methods=["POST"])
def remove_user(user_id):
    """Remove user and redirect to login."""
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    session.pop("username")
    session.pop("user_id")
    return redirect("/login")


@app.route("/feedback/<int:f_id>", methods=["GET", "POST"])
def show_feedback(f_id):
    feedback = Feedback.query.get_or_404(f_id)
    form = FeedbackForm(obj=feedback)
    if form.validate_on_submit():
        feedback.title = form.title.data
        feedback.text = form.text.data
        db.session.commit()
        return redirect(f"/feedback/{feedback.id}")
    return render_template("/show_feedback.html", form=form, feedback=feedback)

@app.route("/feedback/<int:f_id>/delete", methods=["POST"])
def delete_feedback(f_id):
    """Delete feedback."""

    feedback = Feedback.query.get(f_id)
    db.session.delete(feedback)
    db.session.commit()

    return redirect(f"/users/{feedback.user.id}")
    
# @app.route("/tweets/<int:id>", methods=['POST'])
# def delete_tweet(id):
#     if 'user_id' not in session:
#         flash("Please, login first")
#         return redirect('/')
        
#     tweet = Tweet.query.get_or_404(id)
#     if session['user_id'] == tweet.user.username:
#         db.session.delete(tweet)
#         db.session.commit()
#         return redirect('/tweets')
#     flash('You have no permission to delete tweets')
#     return redirect('/tweets')
    