import os
import errno
import requests
from urlparse import urlparse
from os.path import splitext, basename
from flask import current_app
from ..models import ListMedia

def mkdirs(directory):
    try:
        os.makedirs(directory)
    except OSError as err:
        if err.errno == errno.EEXIST and os.path.isdir(directory):
            pass

def get_filename(url):
    url_parts = urlparse(url)
    filename, file_ext = splitext(basename(url_parts.path))

    return "{0}{1}".format(filename, file_ext)

def download_image(list_meida_id, list_user_screen_name):
    row = ListMedia.query.get(list_meida_id)

    if row:
        image_path = current_app.config.get('IMAGE_DOWNLOAD_PATH')
        filename   = get_filename(row.media_url)
        save_path  = os.path.join(image_path, list_user_screen_name)
        save_file  = os.path.join(save_path, filename)

        if os.path.exists(save_file):
            return save_file
        else:
            response = requests.get("{0}:large".format(row.media_url), stream=True)

            if response.status_code == 200:
                mkdirs(save_path)

                with open(save_file, 'wb') as f:
                    for chunk in response.iter_content():
                        f.write(chunk)

                    return save_file
