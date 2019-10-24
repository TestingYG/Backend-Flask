import json
import urllib.parse, urllib.request, urllib.error
from flask import render_template, url_for, flash, redirect, request, abort
from Samaritan_P import app, auth, db, storage
from Samaritan_P.forms import RegistrationForm, LoginForm, UpdateAccountForm, RequestResetForm, SearchForm

def logChecker():
    if auth.current_user == None:
        return False
    else:
        return True

@app.route("/")
@app.route("/home")
def home():

    return render_template('home.html', check = logChecker())

@app.route("/register", methods=['GET', 'POST'])
def register():
    request = None
    if auth.current_user:
        return redirect(url_for('home'))

    form = RegistrationForm()
    if form.validate_on_submit():
        try:
            user = auth.create_user_with_email_and_password(form.email.data, form.password.data)
            auth.send_email_verification(user['idToken'])
            flash('Your account has been created! You are now able to log in', 'success')
            return redirect(url_for('home'))
        except:
            flash('That email is taken. Please choose a different one.', 'danger')


    return render_template('register.html', title='Register', form=form)

@app.route("/login", methods=['GET', 'POST'])
def login():
    if auth.current_user:
        return redirect(url_for('home'))

    form = LoginForm()
    if form.validate_on_submit():
        try:
            auth.sign_in_with_email_and_password(form.email.data, form.password.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))

        except:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title='Login', form=form, check = logChecker())

@app.route("/logout")
def logout():
    auth.current_user = None
    flash('Logout successful', 'success')
    return redirect(url_for('home'))

@app.route("/account", methods=['GET', 'POST'])
def account():
    if auth.current_user == None:
        flash('Permission Denied. Please Login or Register an account', 'primary')
        return redirect(url_for('login'))
    else:
        form = UpdateAccountForm()
        something = auth.get_account_info(auth.current_user['idToken'])
        form.email.data = something['users'][0]['email']
        if form.validate_on_submit():
            my_data = dict()
            flash('Just Pretent your account has been update. This isnt working right now', 'success')
            return redirect(url_for('account'))

        return render_template('account.html', title='Account', form=form, check = logChecker())

@app.route("/passwordreset", methods=['GET', 'POST'])
def passwordreset():
    if auth.current_user == None:
        form = RequestResetForm()
        if form.validate_on_submit():
            try:
                auth.send_password_reset_email(form.email.data)
                flash('Please Check Your Email', 'success')
                next_page = request.args.get('next')
                return redirect(next_page) if next_page else redirect(url_for('home'))
            except:
                flash('Invalid Email', 'danger')

    else:
        form = RequestResetForm()
        something = auth.get_account_info(auth.current_user['idToken'])
        form.email.data = something['users'][0]['email']
        if form.validate_on_submit():
            try:
                auth.send_password_reset_email(form.email.data)
                flash('Please Check Your Email', 'success')
                next_page = request.args.get('next')
                return redirect(next_page) if next_page else redirect(url_for('home'))
            except:
                flash('Invalid Email', 'danger')

    return render_template('reset_request.html', title=passwordreset, form=form)

@app.route("/search", methods=['GET', 'POST'])
def search():
    #do the searching

    form = SearchForm()
    if form.validate_on_submit():
        if auth.current_user == None:
            something = "anonymous"
        else:
            something = auth.get_account_info(auth.current_user['idToken'])['users'][0]['email']

        my_dict = dict()
        my_dict['email'] = something
        my_dict['results'] = "AI OUT PUT WILL BE HERE"
        my_dict['Symptoms'] = form.search.data
        json_data= json.dumps(my_dict)
        db.child("searches").push(json_data)

    return render_template('search.html', title=search, form=form, check = logChecker())
