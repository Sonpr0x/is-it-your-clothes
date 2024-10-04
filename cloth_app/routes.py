from flask import render_template, redirect, url_for, request, flash, send_file, abort, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, current_user, login_required
from app import app, db, login_manager
from models import User, Image
from gradio_client import Client, handle_file
import os, uuid, base64, io
from PIL import Image as Image_process

# Load and store session.
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


############ Admin route ##############

# Admin login
@app.route('/admin', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = User.query.filter_by(username=username, admin=True).first()
        if user and check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for('admin_dashboard'))
        flash('Invalid admin login credentials!')
    return render_template('admin.html')

# Admin dashboard
@app.route('/admin/dashboard')
@login_required
def admin_dashboard():
    if not current_user.admin:
        abort(403)
    
    users = User.query.all()
    return render_template('admin_dashboard.html', users=users)


# Create user
@app.route('/create_user', methods=['POST'])
@login_required
def create_user():
    if not current_user.admin:
        abort(403)
    
    username = request.form.get('username')
    password = request.form.get('password')

    existing_user = User.query.filter_by(username=username).first()
    if existing_user:
        return jsonify({'success': False, 'message': 'Username already exists.'})

    hashed_password = generate_password_hash(password)
    new_user = User(username=username, password=hashed_password, admin=False)
    db.session.add(new_user)
    db.session.commit()


    return jsonify({'success': True})

# Delete user
@app.route('/delete_user', methods=['POST'])
@login_required
def delete_user():
    if not current_user.admin:
        abort(403)
    
    username = request.form.get('username')
    user = User.query.filter_by(username=username).first()
    if user:
        db.session.delete(user)
        db.session.commit()
        return jsonify({'success': True})
    return jsonify({'success': False, 'message': 'User  not found.'})


############# User and app route ##############


# Route root to login page
@app.route('/')
def root():
    return redirect(url_for('login'))

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
        new_user = User(username=username, password=hashed_password, admin=False)
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
@app.route('/app')
@login_required
def main():

    # Load images of user
    uploaded_images = Image.query.filter_by(user_id=current_user.id).all()

    return render_template('index.html', images=uploaded_images)

# Try-on function
@app.route('/process', methods=['POST'])
@login_required
def process():

    # Process images
    if request.method == 'POST':

        # img data
        person_image = request.files['person_image']
        cloth_image = request.files['cloth_image']
        

        # Get obj
        person_image_obj = Image.query.filter_by(id=request.form.get('person_image_id')).first()
        cloth_image_obj = Image.query.filter_by(id=request.form.get('cloth_image_id')).first()

        # Get img path
        person_image_path = person_image_obj.image_path
        cloth_image_path = cloth_image_obj.image_path
        try_on_option = request.form.get('try_on_option')



        # Save and process image
        if allowed_file(cloth_image.filename) and allowed_file(person_image.filename):
            
            person_image_path = save_image(person_image, 'person')
            cloth_image_path = save_image(cloth_image, 'cloth', try_on_option)

            create_image_record(person_image_path)
            create_image_record(cloth_image_path, try_on_option)

            image_path = image_process(person_image_path, cloth_image_path, try_on_option)
            
            result = Image_process.open(image_path)
            return image_to_base64(result)

        elif person_image_path and cloth_image_path:
            print(person_image_path)
            print(cloth_image_path)
            image_path = image_process(person_image_path, cloth_image_path, try_on_option)
            result = Image_process.open(image_path)
            return image_to_base64(result)
        
        elif person_image_path and allowed_file(cloth_image.filename):
            cloth_image_path = save_image(cloth_image, 'cloth', try_on_option)
            create_image_record(cloth_image_path, try_on_option)

            image_path = image_process(person_image_path, cloth_image_path, try_on_option)
            result = Image_process.open(image_path)
            return image_to_base64(result)
        
        elif allowed_file(person_image.filename) and cloth_image_path:
            person_image_path = save_image(person_image, 'person')
            create_image_record(person_image_path)

            image_path = image_process(person_image_path, cloth_image_path, try_on_option)
            result = Image_process.open(image_path)
            return image_to_base64(result)


# Get image
@app.route('/image/<int:image_id>')
@login_required
def get_image(image_id):
    # Query img
    image = Image.query.get_or_404(image_id)

    # Block unauthorized
    if image.user_id != current_user.id:
        abort(403)

    try:
        return send_file(image.image_path)  # Serve the image from its path
    except FileNotFoundError:
        abort(404)


@app.route('/delete_image/<int:image_id>', methods=['POST'])
@login_required
def delete_image(image_id):
    image = Image.query.get_or_404(image_id)

    # Ensure the current user owns the image
    if image.user_id != current_user.id:
        abort(403)

    # Delete the image file from the local storage
    try:
        os.remove(image.image_path)
    except FileNotFoundError:
        pass 

    # Delete the image record from the database
    db.session.delete(image)
    db.session.commit()

    return jsonify({'success': True})


######### Image functions ##########


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

# Check allow extension file
def allowed_file(filename):
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def image_process(person_image_path, cloth_image_path, try_on_option):

        # Create mask
        input_image = Image_process.open(person_image_path)
        layer0 = Image_process.new("L", input_image.size, color=0)

        mask = os.path.join('uploads', str(current_user.id), "temp_mask.png")
        layer0.save(mask)

        # Handle data type for api
        new_person_dict = {
            'background': handle_file(person_image_path),
            'layers': [handle_file(mask)],
            'composite': handle_file(person_image_path)
        }

        # Call api
        client = Client("zhengchong/CatVTON")

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

        # Remove mask data
        os.remove(mask)

        print(result)

        return result

def create_image_record(img_path, try_on_option=None):
    if ('person' in img_path):
        person_image_record = Image(user_id=current_user.id, image_type='person', image_path=img_path)
        db.session.add(person_image_record)

    else:
        cloth_image_record = Image(user_id=current_user.id, image_type=try_on_option, image_path=img_path)
        db.session.add(cloth_image_record)
    
    db.session.commit()

def image_to_base64(image):
    """
    Convert a PIL Image to a base64-encoded string.

    :param image: PIL Image object
    :return: Base64-encoded string
    """
    img_byte_arr = io.BytesIO()
    image.save(img_byte_arr, format='PNG')
    img_byte_arr = img_byte_arr.getvalue()
    return base64.b64encode(img_byte_arr).decode('utf-8')

        