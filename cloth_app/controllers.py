from flask import render_template
from app.models import *


@main_bp.route('/login', method=['GET'])
def index():
    
    return render_template('home.html')

@main_bp.route('/upload_person', method=['POST'])
def upload_person():
    data = Upload_person()
    return render_template('home.html', data=data)


@main_bp.route('/upload_cloth', method=['POST'], data=data)
def upload_cloth():
    data = Upload_cloth()
    return render_template('home.html')


@main_bp.route('/process', method=['POST'])
def process():
    data = Process()
    return render_template('home.html', data=data)


