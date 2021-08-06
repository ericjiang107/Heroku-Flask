from flask import Blueprint, render_template, request, redirect, url_for
from flask.helpers import flash
from flask_login import login_user
from flask_login.utils import login_required, logout_user
from drone_inventory.forms import UserLoginForm
from drone_inventory.models import User, db, check_password_hash

auth = Blueprint('auth',__name__, template_folder='auth_templates')

@auth.route('/signup', methods = ['GET', 'POST'])
# method
def signup():
    form = UserLoginForm()
    if request.method == 'POST' and form.validate_on_submit(): # The form.validate returns a boolean value 
        email = form.email.data # data because in the form.email comment, we used data as key but generally we use .data
        password = form.password.data
        print([email, password])

        # Creating a new user instance and adding that user to the User Table
        user = User(email, password)

        db.session.add(user) # Add this to the database session
        db.session.commit() # Push everything from database session to databse uri

        # Flashed message for successful signup
        flash(f'You have successfully created a user account {email}', 'user-created') # The 'user-created' is a category

        # Redirecting to home page
        return redirect(url_for('site.home'))

    return render_template('signup.html', form = form)


@auth.route('/signin', methods = ['GET', 'POST'])
def signin():
    form = UserLoginForm()
    if request.method == 'POST' and form.validate_on_submit():
        email = form.email.data # data because in the form.email comment, we used data as key but generally we use .data
        password = form.password.data
        print([email, password])

        logged_user = User.query.filter(User.email == email).first()
        if logged_user and check_password_hash(logged_user.password, password):
            login_user(logged_user)
            flash('You are successfully logged in.', 'auth-sucess')
            return redirect(url_for('site.home'))
        else:
            flash('Your Email/Password is incorrect', 'auth-failed')
            return redirect(url_for('auth.signin'))
    return render_template('signin.html', form=form)


# form.email = {data: "ericjiang107@gmail.com"}
# form.password = {data: "1234"}


@auth.route('/logout')
@login_required 
def logout():
    logout_user()
    return redirect(url_for('site.home'))