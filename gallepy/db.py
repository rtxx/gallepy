from flask import Blueprint
from PIL import Image, ImageOps
import os, bcrypt
# import sqlite3 as db
from .configs import *
bp = Blueprint('db', __name__)


class GalleryImage:
    number = -1

    def __init__(self, name, path, album, thumbnail):
        GalleryImage.number += 1
        self.number = GalleryImage.number
        self.name = name
        self.path = path
        self.thumbnail = thumbnail
        self.w = 1  # random.randrange(128,512)
        self.h = 1  # random.randrange(128,512)
        self.album = album or "private"


class User:
    id = -1

    def __init__(self, name, username, hashed_password, salt, type, albuns):
        User.id += 1
        self.id = User.id
        self.name = name
        self.username = username
        self.hashed_password = hashed_password
        self.salt = salt
        self.type = type
        self.albuns = albuns or ["public"]


def init_users_db():
    users = []

    password = "admin1234"
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
    user = User("admininistrator",
                "admin",
                hashed_password,
                salt,
                "admin",
                ["public","album1","album2","album3"]
                )
    users.append(user)

    password = "rui1234"
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
    user = User("user account",
                "user",
                hashed_password,
                salt,
                "user",
                ["public","album1"]
                )
    users.append(user)
    return users


# init dummy dd
def init_images_db():

    imgs = []
    print(f"Searching '{GALLERY_PATH}' for images...")
    for file in os.listdir(GALLERY_PATH):
        current_file = f"{GALLERY_PATH}/{file}"
        if os.path.isfile(current_file):
            ext = os.path.splitext(current_file)[-1].lower()
            if ext == ".jpg" or ext == ".jpeg" or ext == ".png":
                #current_img_thumbnail = f"{THUMBNAILS_PATH}/{file}"
                image = GalleryImage(file,
                                     f"{RELATIVE_GALLERY_PATH}/{file}",
                                     "public",
                                     f"{RELATIVE_THUMBNAILS_PATH}/{file}")
                temp = Image.open(f"{GALLERY_PATH}/{file}")
                image.w = temp.width
                image.h = temp.height
                del temp
                imgs.append(image)
                print(f"{image.name} : image added to 'db' as public")
            else:
                print(f"[ERROR] {current_file} : file is not a image, ignoring...")
        else:
            print(f"Album found - {current_file}")
            album_gallery_path = f"{GALLERY_PATH}/{file}"
            for album_img in os.listdir(album_gallery_path):
                #current_thumbnail_img = f"{THUMBNAILS_PATH}/{file}/{album_img}"
                current_gallery_img = f"{GALLERY_PATH}/{file}/{album_img}"
                ext = os.path.splitext(current_gallery_img)[-1].lower()
                if ext == ".jpg" or ext == ".jpeg" or ext == ".png":
                    image = GalleryImage(album_img,
                                         f"{RELATIVE_GALLERY_PATH}/{file}/{album_img}",
                                         file,
                                         f"{RELATIVE_THUMBNAILS_PATH}/{file}/{album_img}")
                    temp = Image.open(f"{GALLERY_PATH}/{file}/{album_img}")
                    image.w = temp.width
                    image.h = temp.height
                    del temp
                    imgs.append(image)
                    print(f"{image.name} : image added to 'db' as {file}")
                else:
                    print(f"[ERROR] {current_gallery_img} : file is not a image, ignoring...")

    return imgs
