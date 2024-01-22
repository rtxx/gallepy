# gallepy - simple gallery made with python

from flask import Flask, render_template_string
from datetime import timedelta
import os, logging
from PIL import Image, ImageOps
from .configs import *

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'hypermedia rocks'
    # session has a n minutes timeout
    app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=60)

    # init the thumbnails
    @app.cli.command("init-thumbnails")
    def init_thumbnails():
        gpath = GALLERY_PATH
        tpath = THUMBNAILS_PATH
        print(f"Searching '{gpath}' for images...")
        for file in os.listdir(gpath):
            current_file = f"{gpath}/{file}"
            # print(f"Found {file}, checking if thumbnail exists...")
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
                        <title>404</title>
                        <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bulma@0.9.4/css/bulma.min.css">
                      </head>
                      <body>
                        <div class="is-flex is-justify-content-center is-align-items-center" style=" height: 100vh;">
                          <div class="has-text-centered">
                            <h1 class="is-size-1 has-text-weight-bold has-text-primary">404</h1>
                            <p class="is-size-5 has-text-weight-medium"> <span class="has-text-danger">Ohh no!</span> Page not found.</p>
                            <p class="is-size-6 mb-2">
                              The page you’re looking for doesn’t exist.
                            </p>
                            <a href="/" class="button is-primary">Go Home</a>
                          </div>
                        </div>
                      </body>                  
                    </html>
        """
        return render_template_string(templ), 404

    return app


def make_thumbnails_single(image, tpath):
    # https://stackoverflow.com/a/8384786
    path, name_with_extension = os.path.split(image)
    img = Image.open(image)
    img = ImageOps.exif_transpose(img)
    img.thumbnail((512, 512), Image.Resampling.LANCZOS)
    img.save(f"{tpath}/{name_with_extension}")
