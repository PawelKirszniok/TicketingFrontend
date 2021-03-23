import secrets
import os

def save_picture(picture):
    random_hex = secrets.token_hex(8)
    _, file_extension = os.path.splitext(picture.filename)
    new_filename = random_hex + file_extension
    picture_path = os.path.join(app.root_path, 'static/profile_pictures', new_filename)
