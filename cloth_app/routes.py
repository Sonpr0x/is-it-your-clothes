from flask import render_template, redirect, url_for, request, flash, send_file, abort
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, current_user, login_required
from app import app, db, login_manager
from models import User, Image
import os

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        hashed_password = generate_password_hash(password)
        new_user = User(username=username, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        flash('Registration successful!')
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for('index'))
        flash('Invalid login credentials!')
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/', methods=['GET', 'POST'])
@login_required
def index():
    if request.method == 'POST':
        person_image = request.files['person_image']
        cloth_image = request.files['cloth_image']

        if person_image and cloth_image:
            # Save the images to local storage
            person_image_path = save_image(person_image, 'person')
            cloth_image_path = save_image(cloth_image, 'cloth')

            # Save metadata (path) to the database
            person_image_record = Image(user_id=current_user.id, image_type='person', image_path=person_image_path)
            cloth_image_record = Image(user_id=current_user.id, image_type='cloth', image_path=cloth_image_path)
            db.session.add(person_image_record)
            db.session.add(cloth_image_record)
            db.session.commit()
            flash('Images uploaded successfully!')

    uploaded_images = Image.query.filter_by(user_id=current_user.id).all()
    return render_template('index.html', images=uploaded_images)

@app.route('/image/<int:image_id>')
@login_required
def get_image(image_id):
    image = Image.query.get_or_404(image_id)
    try:
        return send_file(image.image_path)  # Serve the image from its path
    except FileNotFoundError:
        abort(404)

def save_image(image, image_type):
    upload_folder = os.path.join('uploads', str(current_user.id), image_type)
    os.makedirs(upload_folder, exist_ok=True)
    image_path = os.path.join(upload_folder, image.filename)
    image.save(image_path)
    return image_path
