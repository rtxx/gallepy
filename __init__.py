# gallepy - simple gallery made with python

from flask import Flask, render_template_string
import os, logging
from PIL import Image, ImageOps
from .configs import *


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'hypermedia rocks'

    # init the thumbnails
    init_thumbnails(GALLERY_PATH, THUMBNAILS_PATH)
    from . import main, db
    app.register_blueprint(main.bp)
    app.register_blueprint(db.bp)

    # route errors
    # 404 - NOT FOUND
    @app.errorhandler(404)
    def route_not_found(e):
        templ = f"""
        <!DOCTYPE html>
        <html lang="en">
            <head>
                <meta charset="UTF-8">
                <meta http-equiv="X-UA-Compatible" content="IE=edge">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
        		<link rel="stylesheet" type="text/css" href="/static/css/modern-normalize.css" />
        		<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/water.css@2/out/water.css">
                <title>404</title>
            </head>
            <body>
                <div style=" height: 100vh;">
                    <div>
                        <h1>404</h1>
                        <p><span>Opps!</span> Page not found.</p>
                        <p>The page you’re looking for doesn’t exist.</p>
                    </div>
                </div>
            </body>
        </html>
        """
        return render_template_string(templ), 404

    return app


def init_thumbnails(gpath, tpath):
    print(f"Searching '{gpath}' for images...")
    for file in os.listdir(gpath):
        current_file = f"{gpath}/{file}"
        #print(f"Found {file}, checking if thumbnail exists...")
        if os.path.isfile(current_file):
            img_thumbnail = f"{tpath}/{file}"
            if os.path.exists(img_thumbnail):
                print(f"{current_file} : Thumbnail exists, continuing...")
            else:
                # print("Not found! Creating...")
                ext = os.path.splitext(current_file)[-1].lower()
                if ext == ".jpg" or ext == ".jpeg" or ext == ".png":
                    make_thumbnails_single(current_file, tpath)
                    print(f"{current_file} : Thumbnail created")
                else:
                    print(f"[ERROR] {current_file} : file is not a image, ignoring...")

        else:
            print(f"Album found - {current_file}")
            album_gallery_path = f"{gpath}/{file}"
            album_thumbnail_path = f"{tpath}/{file}"
            if not os.path.exists(album_thumbnail_path):
                print(f"{current_file} : folder created")
                os.mkdir(album_thumbnail_path)
            for album_img in os.listdir(album_gallery_path):
                current_gallery_img = f"{gpath}/{file}/{album_img}"
                current_thumbnail_img = f"{tpath}/{file}/{album_img}"
                if os.path.exists(current_thumbnail_img):
                    print(f"{current_gallery_img} : Thumbnail exists, continuing...")
                else:
                    ext = os.path.splitext(current_gallery_img)[-1].lower()
                    if ext == ".jpg" or ext == ".jpeg" or ext == ".png":
                        make_thumbnails_single(current_gallery_img, album_thumbnail_path)
                        print(f"{current_gallery_img} : Thumbnail created")
                    else:
                        print(f"[ERROR] {current_gallery_img} : file is not a image, ignoring...")

def make_thumbnails_single(image, tpath):
    # https://stackoverflow.com/a/8384786
    path, name_with_extension = os.path.split(image)
    img = Image.open(image)
    img = ImageOps.exif_transpose(img)
    img.thumbnail((512, 512), Image.Resampling.LANCZOS)
    img.save(f"{tpath}/{name_with_extension}")
