import os
import logging as LOG
from datetime import timedelta

SECRET_KEY = 'change_me_on_prod_pls'

# Database path
DATABASE = os.path.join(".", "gallepy/db.sqlite")

# Paths, to the gallery and thumbnails
GALLERY_PATH = f"{os.getcwd()}/gallepy/static/images/gallery"
RELATIVE_GALLERY_PATH = "./static/images/gallery"

THUMBNAILS_PATH = f"{os.getcwd()}/gallepy/static/images/thumbnails"
RELATIVE_THUMBNAILS_PATH = "./static/images/thumbnails"

# Session timeout
PERMANENT_SESSION_LIFETIME = timedelta(minutes=60)

# log config
LOG.basicConfig(format='%(asctime)s | %(levelname)-8s | %(message)s',
                datefmt='%Y-%m-%d %H:%M:%S',
                level=LOG.INFO)
