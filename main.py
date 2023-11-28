from flask import render_template, render_template_string, request, session, make_response, redirect, send_file
from .db import *

bp = Blueprint('main', __name__)


# init db
images = init_db()


# routes
# index
# renders index.html, which has the pages, gallery divs and some htmx triggers
@bp.route("/")
@bp.route("/index.html")
def route_root():
    return render_template("index.html")


# gallery
# renders gallery. it groups the images in page_size size, the idea being of have pages like 1 to 5 and loads
# accordingly (it does nothing as of now)
# it only renders if user is logged in
@bp.route("/gallery", methods=['GET'])
def route_gallery():
    username = session.get('username')
    if username is not None:
        image_array = []
        for image in images:
            image_array.append(image)
        return render_template("/partials/gallery/gallery.html", image_array=image_array)
    else:
        image_array = []
        for image in images:
            if image.album == "public":
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
@bp.route("/image/full/<number>/modal", methods=['GET'])
def route_image_full_modal(number):
    number = int(number)
    image = images[number]
    return render_template("/partials/gallery/image-full-modal.html", image=image)


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
    username = session.get('username')
    if username is not None:
        image_path = f"{GALLERY_PATH}/{image_name}.{extension}"
        return send_file(image_path, mimetype=f"image/{extension}")
    else:
        for i in range(0, len(images)):
            if images[i].name == f"{image_name}.{extension}":
                if images[i].album == "public":
                    image_path = f"{GALLERY_PATH}/{image_name}.{extension}"
                    return send_file(image_path, mimetype=f"image/{extension}")
        return redirect("/")

@bp.route("/static/gallery/<album>/<image_name>.<extension>", methods=['GET'])
def route_image_full_album_check(album, image_name, extension):
    username = session.get('username')
    if username is not None:
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


# renders the about page
@bp.route("/about", methods=['GET'])
def route_about():
    return render_template("/about.html")


@bp.route("/login", methods=['GET'])
def route_login():
    username = session.get('username')
    if username is not None:
        return render_template("backoffice/backoffice.html", username=username)
    return render_template("/partials/login/login.html")


@bp.route("/login_request", methods=['POST'])
def route_login_request():
    username = request.form['username']
    password = request.form['password']
    if username == "admin" and password == "admin1234!!##":
        session['username'] = username
        # return render_template("backoffice/backoffice.html", username=username)
        templ = f"""            
            <p>welcome back, <bold>{username}</bold>! loading your backoffice...</p>
            <a id="btn_login"
               href=""
               align="right"
               hx-get="/backoffice"
               hx-trigger="click"
               hx-target="#pages"
               hx-swap="innerHTML settle:175ms">
                click here to continue if not redirected...
            </a>
            """
        r = make_response(render_template_string(templ))
        r.headers.set("HX-Trigger", "login")
        return r

    else:
        templ = """
            <form hx-post="/login_request" hx-target="#login_form" hx-swap="innerHTML">
                <input type="text" title="username" name="username" placeholder="username" required/>
                <input type="password" title="username" name="password" placeholder="password" required />
                <button type="submit">Login</button>
            </form>
            <p>incorrect credencials</p>
            """
        return render_template_string(templ)


@bp.route("/backoffice", methods=['GET'])
def route_backoffice():
    username = session.get('username')
    if username is not None:
        return render_template("backoffice/backoffice.html", username=username)
    else:
        return render_template("/partials/login/login.html")


@bp.route("/logout", methods=['GET'])
def route_logout():
    username = session.get('username')
    session.pop('username', None)
    r = make_response(render_template("/partials/login/logout.html", username=username))
    r.headers.set("HX-Trigger", "logout")
    return r
    # return render_template("/partials/login/logout.html", username=username)
