from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.models import User

main_bp = Blueprint('main', __name__)

@main_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        if User.validate_login(username, password):
            return redirect(url_for('main.home'))
        else:
            flash('Invalid username or password')
    return render_template('login.html')

@main_bp.route('/home')
def home():
    return render_template('home.html')

