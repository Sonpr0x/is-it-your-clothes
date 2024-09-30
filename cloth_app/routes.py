from flask import render_template, redirect, url_for, request, flash, send_file, abort
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, current_user, login_required
from app import app, db, login_manager
from models import User, Image
from gradio_client import Client, handle_file
import os, uuid
from PIL import Image as Image_process

# Load and store session.
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


# Register
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        # Check exist user.
        existing_user = User.query.filter_by(username=username).first()

        if existing_user:
            flash('Username already exists. Please choose a different one.', 'error')
            return redirect(url_for('register'))
        
        # Hash and create user.
        hashed_password = generate_password_hash(password)
        new_user = User(username=username, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        flash('Registration successful!')

        return redirect(url_for('login'))
    
    return render_template('register.html')


# Login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for('main'))
        flash('Invalid login credentials!')
    return render_template('login.html')

# Logout
@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))


# Main
@app.route('/app', methods=['GET', 'POST'])
@login_required
def main():

    # Process images
    if request.method == 'POST':
        person_image = request.files['person_image']
        cloth_image = request.files['cloth_image']
        try_on_option = request.form.get('try_on_option')

        # Check if the files have valid names and extensions
        if cloth_image and allowed_file(cloth_image.filename) and person_image and allowed_file(person_image.filename):
            
            
            # Save the images to local storage
            person_image_path = save_image(person_image, 'person')
            cloth_image_path = save_image(cloth_image, 'cloth', try_on_option)

            # Save metadata (path) to the database
            person_image_record = Image(user_id=current_user.id, image_type='person', image_path=person_image_path)
            cloth_image_record = Image(user_id=current_user.id, image_type=try_on_option, image_path=cloth_image_path)

            db.session.add(person_image_record)
            db.session.add(cloth_image_record)
            db.session.commit()
            flash('Images uploaded successfully!')

            # Init api
            client = Client("zhengchong/CatVTON")

            person = client.predict(
		        image_path=handle_file(person_image_path),
		        api_name="/person_example_fn"
            )

            # background img
            data_bg = handle_file(person['background'])

            # Create mask
            input_image = Image_process.open(person_image_path)
            layer0 = Image_process.new("L", input_image.size, color=0)

            mask_folder = os.path.join('uploads', str(current_user.id), "temp_mask.png")
            layer0.save(mask_folder)

            # Create new dict

            new_person_dict = {
                'background': data_bg,
                'layers': [handle_file(mask_folder)],
                'composite': data_bg,
		        'id' : person['id']
            }

            # Call api

            result = client.predict(
		        person_image=new_person_dict,
		        cloth_image=handle_file(cloth_image_path),
		        cloth_type=try_on_option,
		        num_inference_steps=50,
		        guidance_scale=2.5,
		        seed=42,
		        show_type="result only",
		        api_name="/submit_function"
            )


            return send_file(result, mimetype='image/jpeg')


    # Load images of user
    uploaded_images = Image.query.filter_by(user_id=current_user.id).all()

    return render_template('index.html', images=uploaded_images)



# Get image api
@app.route('/image/<int:image_id>')
@login_required
def get_image(image_id):
    image = Image.query.get_or_404(image_id)

    # Block unauthorized
    if image.user_id != current_user.id:
        abort(403)

    try:
        return send_file(image.image_path)  # Serve the image from its path
    except FileNotFoundError:
        abort(404)


### Addtional functions
def save_image(image, image_type, try_on_option=None):
    
    # Set default path to save image.
    if try_on_option:
        upload_folder = os.path.join('uploads', str(current_user.id), image_type, try_on_option)
    else:
        upload_folder = os.path.join('uploads', str(current_user.id), image_type)

    # Make folder.
    os.makedirs(upload_folder, exist_ok=True)

    # Set new uniq image name
    _, ext = os.path.splitext(image.filename)
    unique_id = uuid.uuid4().hex
    unique_file_name = f"{unique_id}{ext}"

    # Set image relative path
    image_path = os.path.join(upload_folder, unique_file_name)

    # Save image to local
    image.save(image_path)
    return image_path


def allowed_file(filename):
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
