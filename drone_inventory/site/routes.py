# This is the controller 

from flask import Blueprint, render_template 
from flask_login import login_required

site = Blueprint('site', __name__, template_folder='site_templates')


# decorator "@"
@site.route('/')
def home():
    return render_template('index.html') # this is looking for a folder/file with that specified name

@site.route('/profile')
@login_required 
def profile():
    return render_template('profile.html')
