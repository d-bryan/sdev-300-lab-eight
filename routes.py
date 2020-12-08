"""
File: routes.py
Author: Dylan Bryan
Date: 11/22/20, 1:29 PM
Project: Lab-7
Purpose: Routes for the site separate from
the main application file
"""
import datetime
import json
import re
import socket
import requests
from requests.exceptions import HTTPError
from passlib.hash import sha256_crypt as crypt
from flask import render_template, \
    url_for, flash, request as req, \
    make_response, redirect, \
    abort
from user import User
from app import app

# secret key for application
# crypt.hash("university")
# $5$rounds=535000$osNJ.twdderpZGFU$GU7MeFemBbhFCogblp7NBGUPu2A5lZdNkuYSv3j2wN5
# usually we never would wan to do this, it would be kept secret in
# a .env file so that it is not exposed to the public
app.secret_key = "twdderpZGFU$GU7MeFemBbhFCogblp7NBGUPu2A5lZdNkuYSv3j2wN5"


def call_api(num_users):
    """
    Calls the Random User API for templates
    of users to add to the web application
    REFERENCE -> https://randomuser.me/
    :param num_users: INTEGER number of users
                    to request to the API
    :return: JSON object to parse
    """
    try:
        rand_user_api = "https://randomuser.me/api/?"
        nat = "nat=us"
        results = "results={}".format(num_users)
        response = requests.get(rand_user_api + nat + "&" + results)
        json_response = response.json()
    except HTTPError as http_err:
        print(f'HTTP error occurred: {http_err}')
    return json_response['results']
# end call_api function


def check_registered(username):
    """
    Check file for registered user
    :param username: STRING username
    :return BOOLEAN: true/false
    """
    registered_users = open('registered_user.txt', 'r')
    # if the file is empty
    if registered_users == "":
        return False
    # otherwise loop over the file
    else:
        # split the values line by line
        for line in registered_users:
            values = line.split()
            if len(values) > 1:
                # get JSON value
                current_line = json.loads(line)
                # check for username in lines
                if username == current_line['username']:
                    return True
    # close the file
    registered_users.close()
    return False
# end check_registered function


def register_user(user_info):
    """
    Register the current user and write
    their information to the JSON file
    :param user_info: JSON object
    :return BOOLEAN: true/false
    """
    # open the file and write the current file over
    with open('registered_user.txt', 'a') as file:
        file.write("\n")  # add blank line between users
        # append new user info
        file.writelines(user_info)
        return True
    return False
# end register_user function


def update_user_information(user_data):
    """
    Updates the user information in the
    registered_user.txt file
    :return BOOLEAN: true/false
    """
    registered_users = open('registered_user.txt', 'r')
    line_to_edit = registered_users.readlines()
    registered_users = open('registered_user.txt', 'r')
    line_counter = 0
    target_line = None
    user_data = json.loads(user_data)

    # read the file to fine which line needs edited
    for line in registered_users:
        # increment the line counter
        values = line.split()
        if len(values) > 1:
            line_counter += 1
            current_line = json.loads(line)
            current_user = current_line['username']
            # check for username in lines
            if user_data['username'] == current_user:
                # get the target line and close file
                target_line = line_counter - 1
                # read.close()
                break

    # edit the line which needs updating
    line_to_edit[target_line] = json.dumps(user_data) + "\n"
    # open file for writing
    registered_users = open('registered_user.txt', 'w')
    # write the new user data in the file
    registered_users.writelines(line_to_edit)
    # close the file and return
    registered_users.close()
    return True
# end update_user_information function


def confirm_username_password(username, password):
    """
    Reads the registered users file and confirms the
    username with the hashed password
    :param username: STRING username
    :param password: STRING hashed password
    :return BOOLEAN: true/false
    """
    registered_users = open('registered_user.txt', 'r')
    # if the file is empty
    if registered_users == "":
        return False
    # otherwise loop over the file
    else:
        # split the values line by line
        for line in registered_users:
            values = line.split()
            if len(values) > 1:
                current_line = json.loads(line)
                current_user = current_line['username']
                # check for username and password in lines
                if username == current_user:
                    verified = crypt.verify(password, current_line['password'])
                    if username == current_user and verified:
                        return True

    # close the file
    registered_users.close()
    return False
# end confirm_username_password function


def get_user_data(username):
    """
    Set the user data to the cookie
    :return: DICT user data
    """
    registered_users = open('registered_user.txt', 'r')
    # loop over file
    for line in registered_users:
        # skip the heading and blank lines
        values = line.split()
        if len(values) > 1:
            current_user = json.loads(line)
            # check for username lines
            if username == current_user['username']:
                # return a dictionary for use in user profile
                return dict(user_id=current_user['user_id'],
                            username=username, password=current_user['password'],
                            confirmed_password=current_user['confirmed_password'],
                            first_name=current_user['first_name'],
                            last_name=current_user['last_name'],
                            favorite_color=current_user['favorite_color'],
                            favorite_animal=current_user['favorite_animal'],
                            area_of_study=current_user['area_of_study'],
                            years_of_study=current_user['years_of_study'])
# end get_user_data function


def confirm_updated_password(user_password):
    """
    Compares updated password to passwords in file and
    passes it through strong regex pattern for extra
    security to ensure no vulnerabilities
    :param user_password: STRING users updated password
    :return:
    """
    # regex for complex password
    strong_password = re.compile("^(?=.{12}$)(?=.*?[a-z])(?=.*?[A-Z])(?=.*?[0-9])(?=.*?[!|@|#|$|%]).*$")
    # common passwords file
    file = open('CommonPassword.txt', 'r')

    # loop over the file and compare password
    # to the current line
    for line in file:
        if user_password in line:
            return False

    # finally compare password to regex pattern
    matches = strong_password.match(user_password)
    return matches
# end confirm_updated_password function


def hash_and_verify_password(password, confirmed):
    """
    Hashes the new user password and verifies the
    confirmed password against the newly hashed password
    :param password: STRING password
    :param confirmed: STRING confirmed password
    :return: DICT dictionary
    """
    # hash the user password
    hashed_password = crypt.hash(password)
    # verify the confirmed password
    verified = crypt.verify(confirmed, hashed_password)
    if verified is False:
        return None

    # create a new dictionary and return with values set to hashed password
    return dict(password=hashed_password, confirmed_password=hashed_password)
# end hash_and_verify_password function


def logger():
    """
    Appends a failed login attempt to the
    failed_login_attempts.txt file with the
    current date, time, and IP address of client
    """
    # get the date
    current_date = datetime.datetime.now()
    current_date = "{}-{}-{} {}".format(current_date.month,
                                        current_date.day,
                                        current_date.year,
                                        current_date.time())
    # gather the IP address and host name
    host_name = socket.gethostname()
    host_ip = socket.gethostbyname(host_name)
    # create a dictionary to append to the file
    current_attempt = dict(host_name=host_name,
                           host_ip=host_ip,
                           date=current_date)
    # convert to json
    current_attempt = json.dumps(current_attempt)
    # open the login attempts file
    log = open('failed_login_attempts.txt', 'a+')
    log.write("\r" + current_attempt)  # write the attempt
    log.close()  # close the file
# end logger function


@app.route('/', methods=['GET'])
def home():
    """
    Uses the request package to call the random
    users api for user templates and adds them
    as speakers for the home page along with
    custom dictionaries added
    :return: Rendered template for Home page
    """
    # get current user
    current_user = req.cookies.get('username')
    if current_user is not None:
        nav = [{'name': 'Home', 'url': url_for('home')},
               {'name': 'About', 'url': url_for('about')},
               {'name': 'Team', 'url': url_for('team')},
               {'name': 'Logout', 'url': url_for('logout')},
               {'name': 'User Profile', 'url': url_for('user_profile')},
               {'name': 'Update Password', 'url': url_for('update_password')}]
    else:
        nav = [{'name': 'Home', 'url': url_for('home')},
               {'name': 'About', 'url': url_for('about')},
               {'name': 'Team', 'url': url_for('team')},
               {'name': 'Register', 'url': url_for('register')},
               {'name': 'Login', 'url': url_for('login')}]
    # home page topic items
    home_page_items = [
        {'topic': 'Nuclear Energy',
         'img': url_for('static', filename='img/physics_1.jpg'),
         'alt_desc': 'Atomic Nucleus reacting on black background',
         'link': 'https://en.wikipedia.org/wiki/Nuclear_power'},
        {'topic': 'Quantum Mechanics',
         'img': url_for('static', filename='img/physics_2.jpeg'),
         'alt_desc': 'Light refracting through a glass prism',
         'link': 'https://en.wikipedia.org/wiki/Quantum_mechanics'},
        {'topic': 'Special Relativity',
         'img': url_for('static', filename='img/physics_3.jpeg'),
         'alt_desc': 'Static electricity moving through a generator',
         'link': 'https://en.wikipedia.org/wiki/Special_relativity'}
    ]
    # create a date time object for when even is
    event_date = datetime.datetime(2020, 12, 18)  # December 12th, 2020
    event_date = "{}/{}/{}".format(event_date.month,
                                   event_date.day,
                                   event_date.year)
    # favicon for site
    favicon = url_for('static', filename='img/white_favicon.ico')
    # call the api and add the results to the speakers list
    result = call_api(3)
    top_speakers = []
    for key, value in enumerate(result):
        current = {'name': {
            'first': value['name']['first'],
            'last': value['name']['last'],
        }, 'tenure_at': value['location']['state'],
            'picture': value['picture']['large']
        }
        top_speakers.append(current)
    # end for loop

    return render_template('home.html',
                           nav=nav,
                           favicon=favicon,
                           title="Physics Leadership Conference",
                           description="Bringing the natural world to you "
                                       "in new and wonderful ways.",
                           event_date=event_date,
                           home_page_list=home_page_items,
                           top_speakers=top_speakers)
# end home route


@app.route('/about', methods=['GET'])
def about():
    """
    Adds a mission statement for the conference to
    the website and renders a template
    :return: Rendered template for About page
    """
    # get current user
    current_user = req.cookies.get('username')
    if current_user is not None:
        nav = [{'name': 'Home', 'url': url_for('home')},
               {'name': 'About', 'url': url_for('about')},
               {'name': 'Team', 'url': url_for('team')},
               {'name': 'Logout', 'url': url_for('logout')},
               {'name': 'User Profile', 'url': url_for('user_profile')},
               {'name': 'Update Password', 'url': url_for('update_password')}]
    else:
        nav = [{'name': 'Home', 'url': url_for('home')},
               {'name': 'About', 'url': url_for('about')},
               {'name': 'Team', 'url': url_for('team')},
               {'name': 'Register', 'url': url_for('register')},
               {'name': 'Login', 'url': url_for('login')}]
    # mission list for ordered list
    mission_list = [
        'Educate the world about the need for physics',
        'Assist the youth to rise in their careers',
        'Spread knowledge through practice',
        'Experiment often and share results',
        'Mentor the next generation to take over'
    ]
    # favicon for site
    favicon = url_for('static', filename='img/white_favicon.ico')
    return render_template('about.html',
                           nav=nav,
                           favicon=favicon,
                           title="Our Mission",
                           mission_list=mission_list)
# end about route


@app.route('/team', methods=['GET'])
def team():
    """
    Uses the request package to call the
    random users api for user templates and
    adds them as team members for the team page
    :return: Rendered template for Team page
    """
    # get current user
    current_user = req.cookies.get('username')
    if current_user is not None:
        nav = [{'name': 'Home', 'url': url_for('home')},
               {'name': 'About', 'url': url_for('about')},
               {'name': 'Team', 'url': url_for('team')},
               {'name': 'Logout', 'url': url_for('logout')},
               {'name': 'User Profile', 'url': url_for('user_profile')},
               {'name': 'Update Password', 'url': url_for('update_password')}]
    else:
        nav = [{'name': 'Home', 'url': url_for('home')},
               {'name': 'About', 'url': url_for('about')},
               {'name': 'Team', 'url': url_for('team')},
               {'name': 'Register', 'url': url_for('register')},
               {'name': 'Login', 'url': url_for('login')}]
    # call the api and store results in team list
    result = call_api(9)
    team_list = []
    for key, value in enumerate(result):
        current = {'name': {
            'first': value['name']['first'],
            'last': value['name']['last'],
        }, 'email': value['email'],
            'phone': value['phone'],
            'picture': value['picture']['large']
        }
        team_list.append(current)
    # end for loop
    favicon = url_for('static', filename='img/white_favicon.ico')
    return render_template('team.html',
                           nav=nav,
                           favicon=favicon,
                           title="Meet Our Team Leaders",
                           team_list=team_list)
# end team route


@app.route('/register', methods=['GET', 'POST'])
def register():
    """
    Allows the user to register to the application
    and store their information in the registered_users.txt
    file
    :return: Rendered Template for register user
    """
    # get current user
    current_user = req.cookies.get('username')
    if current_user is not None:
        nav = [{'name': 'Home', 'url': url_for('home')},
               {'name': 'About', 'url': url_for('about')},
               {'name': 'Team', 'url': url_for('team')},
               {'name': 'Logout', 'url': url_for('logout')},
               {'name': 'User Profile', 'url': url_for('user_profile')},
               {'name': 'Update Password', 'url': url_for('update_password')}]
    else:
        nav = [{'name': 'Home', 'url': url_for('home')},
               {'name': 'About', 'url': url_for('about')},
               {'name': 'Team', 'url': url_for('team')},
               {'name': 'Register', 'url': url_for('register')},
               {'name': 'Login', 'url': url_for('login')}]
    # animal options
    favorite_animals = [{'name': 'Please Select Your Favorite', 'value': ''},
                        {'name': 'Dog', 'value': 'dog'},
                        {'name': 'Cat', 'value': 'cat'},
                        {'name': 'Mouse', 'value': 'mouse'},
                        {'name': 'Snake', 'value': 'snake'},
                        {'name': 'Horse', 'value': 'horse'}]
    # years experience options
    years_exp = [{'name': 'Please Select Your Experience', 'value': ''},
                 {'name': '0 - 1', 'value': '0-1'},
                 {'name': '1 - 3', 'value': '1-3'},
                 {'name': '3 - 5', 'value': '3-5'},
                 {'name': '5 +', 'value': '5+'}]
    favicon = url_for('static', filename='img/white_favicon.ico')

    # if a new user registers to the site
    if req.method == 'POST':
        # check the file for username
        if check_registered(req.form['username']):
            flash("Username already registered", category="message")
        else:
            # create new user object
            username = req.form.get('username')
            password = req.form.get('password')
            confirm_password = req.form.get('password-confirmation')
            first_name = req.form.get('first-name')
            last_name = req.form.get('last-name')
            favorite_color = req.form.get('favorite-color')
            favorite_animal = req.form.get('favorite-animal')
            area_of_study = req.form.get('area-of-study')
            years_of_study = req.form.get('years-of-study')
            # create new user object
            current_user = User(username, password, confirm_password, first_name,
                                last_name, favorite_color, favorite_animal,
                                area_of_study, years_of_study)
            current_data = current_user.to_string_json()
            # create new user and add to file
            if register_user(current_data):
                resp = make_response(redirect(url_for('user_profile')))
                resp.set_cookie(key='username', value=current_data, max_age=86400, expires=86400)
                return resp
            else:
                # else reload current page
                return redirect(req.url)
    # render the register template
    return render_template('register.html',
                           title="User Registration",
                           description="Please enter all of your user information",
                           nav=nav,
                           favicon=favicon,
                           favorite_animals=favorite_animals,
                           years_exp=years_exp)
# end register route


@app.route('/login', methods=['GET', 'POST'])
def login():
    # get current user
    current_user = req.cookies.get('username')
    if current_user is not None:
        nav = [{'name': 'Home', 'url': url_for('home')},
               {'name': 'About', 'url': url_for('about')},
               {'name': 'Team', 'url': url_for('team')},
               {'name': 'Logout', 'url': url_for('logout')},
               {'name': 'User Profile', 'url': url_for('user_profile')},
               {'name': 'Update Password', 'url': url_for('update_password')}]
    else:
        nav = [{'name': 'Home', 'url': url_for('home')},
               {'name': 'About', 'url': url_for('about')},
               {'name': 'Team', 'url': url_for('team')},
               {'name': 'Register', 'url': url_for('register')},
               {'name': 'Login', 'url': url_for('login')}]
    favicon = url_for('static', filename='img/white_favicon.ico')

    # if the user is attempting to login
    if req.method == "POST":
        if current_user is not None:
            # if someone is logged in remove cookie
            resp = make_response(None)
            resp.set_cookie('username', max_age=0)
        # get user information
        username = req.form.get('username')
        password = req.form.get('password')
        # if username and password do match
        if confirm_username_password(username=username, password=password):
            current_user_data = json.dumps(get_user_data(username))
            resp = make_response(redirect(url_for('user_profile')))
            resp.set_cookie(key='username', value=current_user_data, max_age=86400, expires=86400)
            #  redirect user to user profile
            return resp
        else:
            # otherwise flash error message and redirect user to login page
            flash("Username and Password don't match", category="message")
            logger()  # log the failed attempt
            return redirect(url_for('login'))
    else:
        # render the login page
        return render_template('login.html',
                               title="Login",
                               nav=nav,
                               favicon=favicon)
# end login route


@app.route('/profile', methods=['GET'])
def user_profile():
    """
    User profile page with custom data from registration
    dynamically added into the page
    :return: Render user profile template
    """
    # get current user
    current_user = req.cookies.get('username')

    if current_user is not None:
        nav = [{'name': 'Home', 'url': url_for('home')},
               {'name': 'About', 'url': url_for('about')},
               {'name': 'Team', 'url': url_for('team')},
               {'name': 'Logout', 'url': url_for('logout')},
               {'name': 'User Profile', 'url': url_for('user_profile')},
               {'name': 'Update Password', 'url': url_for('update_password')}]
        favicon = url_for('static', filename='img/white_favicon.ico')
        # load cookie data into current user
        current_user = json.loads(current_user)
        # create data to pass into table information
        table_info = [{'title': 'User ID', 'body': current_user['user_id']},
                      {'title': 'Username', 'body': current_user['username']},
                      {'title': 'First Name', 'body': current_user['first_name']},
                      {'title': 'Last Name', 'body': current_user['last_name']},
                      {'title': 'Favorite Color', 'body': current_user['favorite_color']},
                      {'title': 'Favorite Animal', 'body': current_user['favorite_animal']},
                      {'title': 'Area of Study', 'body': current_user['area_of_study']},
                      {'title': 'Years of Study', 'body': current_user['years_of_study']}]
        title = current_user['first_name'] + "'s Profile"
        description = "Wonderful facts about " + current_user['first_name']

        return render_template('user_profile.html',
                               nav=nav,
                               favicon=favicon,
                               title=title,
                               description=description,
                               table_info=table_info)
    else:
        # unauthorized attempt to access page
        return abort(403)
# end user page route


@app.route('/update-password', methods=['GET', 'POST'])
def update_password():
    """
    Allows the user to update their password
    with specific parameters, and as long as
    the password does not match CommonPasswords.txt
    list of passwords
    :return:
    """
    # get current user
    current_user = req.cookies.get('username')
    if current_user is not None:
        nav = [{'name': 'Home', 'url': url_for('home')},
               {'name': 'About', 'url': url_for('about')},
               {'name': 'Team', 'url': url_for('team')},
               {'name': 'Logout', 'url': url_for('logout')},
               {'name': 'User Profile', 'url': url_for('user_profile')},
               {'name': 'Update Password', 'url': url_for('update_password')}]
        favicon = url_for('static', filename='img/white_favicon.ico')

        if req.method == "POST":
            current_user = json.loads(current_user)
            # get information from the form
            password = req.form.get('password')
            confirmed_password = req.form.get('confirm-password')
            # compare the user password to list and regex
            if confirm_updated_password(password) is not None:
                # update and hash passwords
                updated_passwords = hash_and_verify_password(password, confirmed_password)
                # set the new passwords
                current_user['password'] = updated_passwords['password']
                current_user['confirmed_password'] = updated_passwords['confirmed_password']
                # create a json object
                current_user_data = json.dumps(current_user)
                # update passwords for the user
                if update_user_information(current_user_data):
                    resp = make_response(redirect(url_for('user_profile')))
                    resp.set_cookie(key='username', value=current_user_data, max_age=86400, expires=86400)
                    return resp
                else:  # internal server error
                    abort(500)
                # else:  # otherwise user does not exist
                #     flash("Username Does Not Exist", category="message")
            else:  # otherwise password needs to be corrected
                flash("Must have 12 characters in length, 1 lower, upper case, number and special character",
                      category="message")
                return render_template('update-password.html',
                                       nav=nav,
                                       favicon=favicon,
                                       title="Update Your Password")

        # otherwise render the form
        elif req.method == "GET":
            return render_template('update-password.html',
                                   nav=nav,
                                   favicon=favicon,
                                   title="Update Your Password")
    else:
        # unauthorized attempted password change
        abort(403)
# end update_password route


@app.route('/logout')
def logout():
    """
    Logs the user out and redirects to home page
    :return: Redirect to home page
    """
    # remove the cookie from the browser
    resp = make_response(redirect(url_for('home')))
    resp.set_cookie('username', max_age=0)
    # redirect to home page
    return resp
# end logout route


@app.errorhandler(403)
def unauthorized(e):
    """
    Custom 403 error page
    :return: Rendered template 403 error page
    """
    # get current user
    current_user = req.cookies.get('username')
    if current_user is not None:
        nav = [{'name': 'Home', 'url': url_for('home')},
               {'name': 'About', 'url': url_for('about')},
               {'name': 'Team', 'url': url_for('team')},
               {'name': 'Logout', 'url': url_for('logout')},
               {'name': 'User Profile', 'url': url_for('user_profile')}]
    else:
        nav = [{'name': 'Home', 'url': url_for('home')},
               {'name': 'About', 'url': url_for('about')},
               {'name': 'Team', 'url': url_for('team')},
               {'name': 'Register', 'url': url_for('register')},
               {'name': 'Login', 'url': url_for('login')}]
    favicon = url_for('static', filename='img/white_favicon.ico')

    return render_template('403.html',
                           nav=nav,
                           favicon=favicon,
                           title="You Are Not Authorized To Access This Page")
# end unauthorized route


@app.errorhandler(404)
def not_found(e):
    """
    Custom 404 error page
    :return: Rendered template 404 error page
    """
    # get current user
    current_user = req.cookies.get('username')
    if current_user is not None:
        nav = [{'name': 'Home', 'url': url_for('home')},
               {'name': 'About', 'url': url_for('about')},
               {'name': 'Team', 'url': url_for('team')},
               {'name': 'Logout', 'url': url_for('logout')},
               {'name': 'User Profile', 'url': url_for('user_profile')}]
    else:
        nav = [{'name': 'Home', 'url': url_for('home')},
               {'name': 'About', 'url': url_for('about')},
               {'name': 'Team', 'url': url_for('team')},
               {'name': 'Register', 'url': url_for('register')},
               {'name': 'Login', 'url': url_for('login')}]
    favicon = url_for('static', filename='img/white_favicon.ico')

    return render_template('404.html',
                           nav=nav,
                           favicon=favicon,
                           title="Page Not Found")
# end not found route


@app.errorhandler(500)
def internal_server_error(e):
    """
    Custom 500 error page
    :return: Rendered template for 500 error
    """
    # get current user
    current_user = req.cookies.get('username')
    if current_user is not None:
        nav = [{'name': 'Home', 'url': url_for('home')},
               {'name': 'About', 'url': url_for('about')},
               {'name': 'Team', 'url': url_for('team')},
               {'name': 'Logout', 'url': url_for('logout')},
               {'name': 'User Profile', 'url': url_for('user_profile')}]
    else:
        nav = [{'name': 'Home', 'url': url_for('home')},
               {'name': 'About', 'url': url_for('about')},
               {'name': 'Team', 'url': url_for('team')},
               {'name': 'Register', 'url': url_for('register')},
               {'name': 'Login', 'url': url_for('login')}]
    favicon = url_for('static', filename='img/white_favicon.ico')

    return render_template('500.html',
                           nav=nav,
                           favicon=favicon,
                           title="Oops, It looks like something went wrong")
# end internal_server_error route
