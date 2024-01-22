from flask import render_template, render_template_string, request, session, make_response, redirect, send_file
import bcrypt
from .db import *

bp = Blueprint('main', __name__)


# init db
images = init_images_db()
users = init_users_db()


# routes
# index
# renders index.html, which has the pages, gallery divs and some htmx triggers
@bp.route("/")
@bp.route("/index.html")
def route_root():
    return render_template("index.html")


# gallery
# renders gallery.
# it only renders if user is logged in and if user is allowed to view said album
@bp.route("/gallery", methods=['GET'])
def route_gallery():
    user = get_current_logged_user(users, session.get('username'))
    image_array = []
    if user is not None:
        for image in images:
            if image.album in user.albuns or user.type == "admin":
                image_array.append(image)
        return render_template("/partials/gallery/gallery.html", image_array=image_array)
    else:
        for image in images:
            if image.album == "public":
                image_array.append(image)
        return render_template("/partials/gallery/gallery.html", image_array=image_array)

# gallery-album
# renders gallery.
# it only renders if user is logged in and if user is allowed to view said album
@bp.route("/gallery/<album>", methods=['GET'])
def route_gallery_album(album):
    album = str(album)
    user = get_current_logged_user(users, session.get('username'))
    image_array = []

    if user is not None:
        for image in images:
            if image.album == album:
                image_array.append(image)
        return render_template("/partials/gallery/gallery.html", image_array=image_array)


# gallery - filter by album
# renders gallery filtered by album.
# it only renders if user is logged in and if user is allowed to view said album
@bp.route("/gallery/filter", methods=['POST'])
def route_gallery_filter_album():
    album = request.form['filterOptions']
    user = get_current_logged_user(users, session.get('username'))
    image_array = []

    if user is not None:
        for image in images:
            if image.album == album:
                image_array.append(image)

        return render_template("/partials/gallery/gallery.html", image_array=image_array)


# gets image thumbnail
@bp.route("/image/thumbnail/<number>", methods=['GET'])
def route_image(number):
    number = int(number)
    for image in images:
        if number == image.number:
            image = images[number]
            return render_template("/partials/gallery/image.html", image=image)


# gets full image
@bp.route("/image/full/<number>", methods=['GET'])
def route_image_full(number):
    number = int(number)
    for image in images:
        if number == image.number:
            image = images[number]
            return render_template("/partials/gallery/image-full.html", image=image)


# gets full image for the modal, so it won't flicker the background of the modal when switching
@bp.route("/image/full/<from_image_number>/<to_image_number>/modal", methods=['GET'])
def route_image_full_modal(from_image_number, to_image_number):
    from_image_number = int(from_image_number)
    to_image_number = int(to_image_number)

    if to_image_number >= len(images):
        to_image_number = len(images) - 1

    to_image = images[to_image_number]
    from_image = images[from_image_number]

    user = get_current_logged_user(users, session.get('username'))
    if user is not None:
        if to_image.album in user.albuns or user.type == "admin":
            return render_template("/partials/gallery/image-full-modal.html", image=to_image)
        else:
            return render_template("/partials/gallery/image-full-modal.html", image=from_image)
    else:
        if to_image.album == "public":
            return render_template("/partials/gallery/image-full-modal.html", image=to_image)
        else:
            return render_template("/partials/gallery/image-full-modal.html", image=from_image)


# gets full image for the modal, so it won't flicker the background of the modal when switching
@bp.route("/image/full/<number>/html", methods=['GET'])
def route_image_full_html(number):
    number = int(number)
    image = images[number]
    return render_template("/partials/gallery/image-full-html.html", image=image)


# this is prevent unauthorized access if not logged in
# if the image is 'public' then allows the download
@bp.route("/static/gallery/<image_name>.<extension>", methods=['GET'])
def route_image_full_check(image_name, extension):
    user = get_current_logged_user(users, session.get('username'))
    if user is not None:
        image_path = f"{GALLERY_PATH}/{image_name}.{extension}"
        return send_file(image_path, mimetype=f"image/{extension}")
    else:
        for i in range(0, len(images)):
            if images[i].name == f"{image_name}.{extension}":
                if images[i].album == "public":
                    image_path = f"{GALLERY_PATH}/{image_name}.{extension}"
                    return send_file(image_path, mimetype=f"image/{extension}")
        return redirect("/")


# this is prevent unauthorized access if not logged in, workaround for albuns routes
@bp.route("/static/gallery/<album>/<image_name>.<extension>", methods=['GET'])
def route_image_full_album_check(album, image_name, extension):
    user = get_current_logged_user(users, session.get('username'))
    if user is not None:
        image_path = f"{GALLERY_PATH}/{album}/{image_name}.{extension}"
        return send_file(image_path, mimetype=f"image/{extension}")
    else:
        for i in range(0, len(images)):
            if images[i].name == f"{image_name}.{extension}":
                if images[i].album == "public":
                    image_path = f"{GALLERY_PATH}/{album}/{image_name}.{extension}"
                    return send_file(image_path, mimetype=f"image/{extension}")
        return redirect("/")


# renders a blank page
@bp.route("/blank", methods=['GET'])
def route_blank():
    return render_template("/partials/blank.html")


# login
@bp.route("/login", methods=['GET'])
def route_login():
    user = get_current_logged_user(users, session.get('username'))
    if user is not None:
        return render_template("/partials/backoffice/backoffice.html", user=user)
    else:
        return render_template("/partials/login/login.html")


@bp.route("/login_request", methods=['POST'])
def route_login_request():
    username = request.form['username']
    password = request.form['password']
    for user in users:
        if username == user.username:
            password_bytes = password.encode('utf-8')
            check_hash = bcrypt.checkpw(password_bytes, user.hashed_password)
            if check_hash:
                session['username'] = user.username
                #r = make_response(render_template("/partials/login/login-successful.html", user=user))
                r =  make_response(render_template("/partials/backoffice/backoffice.html", user=user))
                r.headers.set("HX-Trigger", "login")
                return r
            else:
                return render_template("/partials/login/login-error.html", error_type="Login incorrect!")
    return render_template("/partials/login/login-error.html", error_type="Login incorrect!")


@bp.route("/logout", methods=['GET'])
def route_logout():
    user = get_current_logged_user(users, session.get('username'))
    session.pop('username', None)
    r = make_response(render_template("/partials/login/logout.html", username=user.username))
    r.headers.set("HX-Trigger", "logout")
    return r


# renders the about page
@bp.route("/about", methods=['GET'])
def route_about():
    return render_template("/about.html")


# backoffice pages
@bp.route("/backoffice", methods=['GET'])
def route_backoffice():
    user = get_current_logged_user(users, session.get('username'))
    if user is not None:
        return render_template("/partials/backoffice/backoffice.html", user=user)
    else:
        return render_template("/partials/login/login.html")


@bp.route("/backoffice/gallery", methods=['GET'])
def route_backoffice_gallery_tab():
    user = get_current_logged_user(users, session.get('username'))
    if user is not None:
        return render_template("/partials/backoffice/backoffice-gallery.html", user=user)
    else:
        return render_template("/partials/login/login.html")


@bp.route("/backoffice/settings", methods=['GET'])
def route_backoffice_settings_tab():
    user = get_current_logged_user(users, session.get('username'))
    if user is not None:
        return render_template("/partials/backoffice/backoffice-settings.html", user=user)
    else:
        return render_template("/partials/login/login.html")


def get_current_logged_user(db, username):
    for user in db:
        if username == user.username:
            return user
    else:
        return None