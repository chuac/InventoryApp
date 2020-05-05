import os
import secrets
from datetime import datetime
from decimal import Decimal
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


def calc_time_delta(last_updated_time):
    time_now = datetime.utcnow()

    difference = (time_now - last_updated_time)
    difference_in_s = int(difference.total_seconds()) # timedelta functionality to get seconds. cast from float to int to drop trailing decimal zero

    if difference_in_s < 60:
        return "less than a minute ago"
    elif 60 <= difference_in_s < 3600:
        minutes = divmod(difference_in_s, 60)[0] # 60 seconds in a minute
        if minutes == 1:
            return f"{minutes} minute ago" # for singular vs plural minute(s)
        else:
            return f"{minutes} minutes ago"
    elif 3600 <= difference_in_s < 86400:
        hours = divmod(difference_in_s, 3600)[0] # 3600 seconds in an hour
        if hours == 1:
            return f"{hours} hour ago"
        else:
            return f"{hours} hours ago"
    else:
        days = divmod(difference_in_s, 86400)[0] # 86400 seconds in a day
        if days == 1:
            return f"{days} day ago"
        else:
            return f"{days} days ago"


"""
Remove the exponent and trailing zeroes, losing significance, but keeping the value unchanged
https://docs.python.org/3/library/decimal.html#decimal-faq
"""
def remove_exponent(d):
    return d.quantize(Decimal(1)) if d == d.to_integral() else d.normalize()