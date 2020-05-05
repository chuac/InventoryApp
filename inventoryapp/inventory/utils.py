import os
import secrets
from PIL import Image
from flask import url_for, current_app


# future improvements: check if picture with name of the random hex already exists in db. Unlikely but could cause issues
def save_picture(form_picture): # new pic we received from the form
    random_hex = secrets.token_hex(8) # generate random hex so we don't store pics under the name the user uploaded with
    f_name, f_ext = os.path.splitext(form_picture.filename) # grab the file extension though, we need that. Python convention would be to name the name part of the split string "_" since it is not used
    new_pic_name = random_hex + f_ext # concatenate the new hex plus the file extension
    picture_path = os.path.join(current_app.root_path, 'static/inventory_pics', new_pic_name)

    #form_picture.save(picture_path) # we no longer want this to save all pictures at any size the users upload to the server

    output_size = (125, 125) # our css would resize pics to 125x125px anyways
    img = Image.open(form_picture) # Image is imported from Pillow (PIL) library
    img.thumbnail(output_size)
    img.save(picture_path)

    return new_pic_name