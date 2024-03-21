import bcrypt
import functools
from flask import Blueprint, render_template, render_template_string, g, session, request, make_response, send_file, current_app
from .db import get_db
from . import LOG
from .gallery import make_thumbnails, make_gallery, update_album_permissions_table, init_album_table

bp = Blueprint('main', __name__)


# routes
# from https://github.com/pallets/flask/blob/3.0.1/examples/tutorial/flaskr/auth.py
@bp.before_app_request
def load_logged_in_user():
    """If a user id is stored in the session, load the user object from
    the database into ``g.user``."""
    user_id = session.get("user_id")

    if user_id is None:
        g.user = None
    else:
        g.user = (
            get_db().execute("SELECT * FROM USERS WHERE ID = ?", (user_id,)).fetchone()
        )


# index
# renders index.html, which has the pages, gallery divs and some htmx triggers
@bp.route("/")
@bp.route("/index.html")
def route_root():
    return render_template("index.html")


@bp.route("/navbar", methods=['GET'])
def route_navbar():
    return render_template("/partials/navbar/navbar.html")


# gallery
# renders gallery
@bp.route("/gallery", methods=['GET'])
def route_gallery():
    images = []
    for row in get_images():
        # image = GalleryImage(*row)
        images.append(row)
    return render_template("/partials/gallery/gallery.html", image_list=images)


@bp.route("/gallery2", methods=['GET'])
def route_gallery2():
    images = []
    for row in get_images():
        # image = GalleryImage(*row)
        images.append(row)
    return render_template("/partials/gallery/gallery2.html", image_list=images)


# gets image thumbnail
@bp.route("/image/thumbnail/<int:id>", methods=['GET'])
def route_get_image(id):
    image = get_image_by_id(id)
    return render_template("/partials/gallery/image.html", image=image)


@bp.route("/image/thumbnail2/<int:id>", methods=['GET'])
def route_get_image2(id):
    image = get_image_by_id(id)
    return render_template("/partials/gallery/image2.html", image=image)


# login section
# from https://github.com/pallets/flask/blob/3.0.1/examples/tutorial/flaskr/auth.py
def login_required(view):
    """View decorator that redirects anonymous users to the login page."""
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            error = 401
            error_desc = "The page you’re looking for needs authentication, please login or refresh the page."
            return render_template("/errors/error.html", error=error, error_desc=error_desc)
            # return render_template("/errors/401.html")
            # return redirect(url_for("errors.401"))
        return view(**kwargs)
    return wrapped_view


@bp.route("/login", methods=['GET'])
def route_login():
    return render_template("/partials/login/login.html")


@bp.route("/login_request", methods=['POST'])
def route_login_request():
    username = request.form['username']
    password = request.form['password']
    db = get_db()

    try:
        user = db.execute("SELECT * FROM USERS WHERE USERNAME = ?", (username,)).fetchone()
    except db.OperationalError as error:
        raise Exception('Could not perform query on the database: ''{}'.format(error))
    except db.IntegrityError:
        LOG.error(f"{db.IntegrityError}: Something went wrong...")
        return render_template("/partials/login/login-error.html",
                               error_type=f"{ db.IntegrityError }: Something went wrong...")

    if user is None:
        return render_template("/partials/login/login-error.html", error_type=f"Login incorrect!")
    else:
        password_bytes = password.encode('utf-8')
        check_hash = bcrypt.checkpw(password_bytes, user["hashed_password"])
        if check_hash:
            # store the user id in a new session
            session.clear()
            session["user_id"] = user["id"]
            r = make_response(render_template("/partials/backoffice/backoffice.html", user=user))
            r.headers.set("HX-Trigger", "login")
            return r
        else:
            return render_template("/partials/login/login-error.html", error_type=f"Login incorrect!")


@bp.route("/logout", methods=['GET'])
def route_logout():
    session.clear()
    r = make_response(render_template("/partials/login/logout.html"))
    r.headers.set("HX-Trigger", "logout")
    return r


# backoffice pages
@bp.route("/backoffice", methods=['GET'])
@login_required
def route_backoffice():
    return render_template("/partials/backoffice/backoffice.html", user=g.user)


@bp.route("/backoffice/test", methods=['GET'])
@login_required
def route_backoffice_testing_tab():
    return render_template("/partials/backoffice/backoffice-test.html", user=g.user)


@bp.route("/backoffice/gallery", methods=['GET'])
@login_required
def route_backoffice_gallery_tab():
    return render_template("/partials/backoffice/backoffice-gallery.html", user=g.user)


@bp.route("/backoffice/gallery/list/albums", methods=['GET'])
@login_required
def route_backoffice_gallery_list_albums():
    db = get_db()
    try:
        granted_albums = db.execute(
            "SELECT ALBUM_ID FROM ALBUM_PERMISSIONS WHERE USER_ID=(?) AND GRANTED='TRUE';",
            (g.user[0],)
        ).fetchall()
    except db.OperationalError as error:
        raise Exception(f"Could not perform query on the database: {error}")
    except db.IntegrityError:
        LOG.info = f"{db.IntegrityError}: Something went wrong..."
        templ = f""" 
                <a>ERROR: {db.IntegrityError}</a>
                """
        return render_template_string(templ)
    options = ""
    for item in granted_albums:
        options += f"<option value={item[0]}>{item[0]}</option>"
    templ = f"""
            <select form="filter_form" name="filterOptions">
                {options}
            </select>
            """
    return render_template_string(templ)


@bp.route("/backoffice/gallery/filter/album/", methods=['POST'])
@login_required
def route_backoffice_gallery_filter_by_album():
    album = request.form['filterOptions']
    db = get_db()
    try:
        images = db.execute(
            f"SELECT * FROM GALLERY WHERE ALBUM=(?) ORDER BY LENGTH(NAME), NAME;",
            (album,)
        ).fetchall()
    except db.OperationalError as error:
        raise Exception(f"Could not perform query on the database: {error}")
    except db.IntegrityError:
        LOG.error(f"{db.IntegrityError}: Something went wrong.")
        return

    image_list = []
    for row in images:
        image_list.append(row)
    return render_template("/partials/gallery/gallery.html", image_list=image_list)


@bp.route("/backoffice/settings", methods=['GET'])
@login_required
def route_backoffice_settings_tab():
    return render_template("/partials/backoffice/backoffice-settings.html", user=g.user)


@bp.route("/backoffice/settings/change_password", methods=['POST'])
@login_required
def route_backoffice_settings_change_password():
    current_password = request.form['current_password']
    new_password = request.form['new_password']

    current_password_bytes = current_password.encode('utf-8')
    check_hash = bcrypt.checkpw(current_password_bytes, g.user["hashed_password"])
    if check_hash:
        db = get_db()
        salt = bcrypt.gensalt()
        hashed_new_password = bcrypt.hashpw(new_password.encode('utf-8'), salt)

        try:
            db.execute(
                "UPDATE USERS SET HASHED_PASSWORD=(?) WHERE USERNAME=(?);",
                (hashed_new_password, g.user["username"])
            )
            db.commit()
        except db.OperationalError as error:
            raise Exception('Could not perform query on the database: ''{}'.format(error))
        except db.IntegrityError:
            LOG.info = f"{ db.IntegrityError }: Something went wrong..."
            templ = f""" 
                    <a>ERROR: { db.IntegrityError }</a>
                    """
            return render_template_string(templ)
    else:
        templ = """
                <button class="button is-error is-static">Current password is incorrect! Refresh to try again</button>
                """
        return render_template_string(templ)
    templ = """
            <button class="button is-success is-static">Success!</button>
            """
    return render_template_string(templ)


@bp.route("/backoffice/settings/create_new_user", methods=['POST'])
@login_required
def route_backoffice_settings_create_new_user():
    # TODO: need to check if user exists 1st 
    new_user = request.form['new_user']
    new_username = request.form['new_username']
    new_password = request.form['new_password']
    salt = bcrypt.gensalt()
    hashed_new_password = bcrypt.hashpw(new_password.encode('utf-8'), salt)

    db = get_db()
    try:
        db.execute(
            "INSERT INTO USERS (NAME,USERNAME,HASHED_PASSWORD,TYPE) VALUES (?, ?, ?, ?)",
            (new_user, new_username, hashed_new_password, "user"),
        )
        db.commit()
    except db.OperationalError as error:
        raise Exception('Could not perform query on the database: ''{}'.format(error))
    except db.IntegrityError:
        LOG.info(f"{ db.IntegrityError }: Something went wrong...")
        templ = f""" 
        <a>ERROR { db.IntegrityError }</a>
        """
        return render_template_string(templ)

    templ = """
            <button class="button is-success is-static">Success!</button>
            """
    return render_template_string(templ)


@bp.route("/backoffice/settings/update_album_permissions/album_select", methods=['GET'])
@login_required
def route_backoffice_settings_update_album_permissions_album_select():
    db = get_db()
    try:
        albums = db.execute(
            "SELECT * FROM ALBUM;"
        )
        db.commit()
    except db.OperationalError as error:
        raise Exception('Could not perform query on the database: ''{}'.format(error))
    except db.IntegrityError:
        LOG.info(f"{ db.IntegrityError }: Something went wrong...")
        templ = f"""
                <select>
                    <option>Error... Please try again</option>
                </select>
                """
        return render_template_string(templ)

    select_options = ""
    for album in albums.fetchall():
        select_options = select_options + f"<option>{ album[1] }</option>"
    templ = f"""
            <select form="update_permissions_form" name="update_permissions_form_select">
                <option>Choose...</option>
                { select_options }
            </select>
            """
    return render_template_string(templ)


@bp.route("/backoffice/settings/update_album_permissions", methods=['POST'])
@login_required
def route_backoffice_settings_update_album_permissions():
    username = request.form['update_permissions_form_username']
    selected_album = request.form['update_permissions_form_select']
    granted = request.form['update_permissions_form_granted']

    # get all album
    # get user id from username
    # create new rule, if exists updates it
    db = get_db()
    try:
        album_query = db.execute(
            "SELECT * FROM ALBUM;"
        )
        db.commit()
    except db.OperationalError as error:
        raise Exception('Could not perform query on the database: ''{}'.format(error))
    except db.IntegrityError:
        LOG.info(f"{ db.IntegrityError }: Something went wrong...")
        templ = f"""
                <button class="button is-error is-static">Error: { db.IntegrityError }</button>
                """
        return render_template_string(templ)

    try:
        user_query = db.execute(
            "SELECT ID FROM USERS WHERE USERNAME=( ? );",
            (username,),
        )
        db.commit()
    except db.OperationalError as error:
        raise Exception('Could not perform query on the database: ''{}'.format(error))
    except db.IntegrityError:
        LOG.info(f"{ db.IntegrityError }: Something went wrong...")
        templ = f"""
                <button class="button is-error is-static">Error: { db.IntegrityError }</button>
                """
        return render_template_string(templ)

    albums = album_query.fetchall()
    user = user_query.fetchone()

    check_if_rule_exists = db.execute("SELECT 1 FROM ALBUM_PERMISSIONS WHERE USER_ID=(?) AND ALBUM_ID=(?);",
                                      (user['ID'], selected_album)
                                      )
    if check_if_rule_exists.fetchone() is None:
        try:
            db.execute(
                "INSERT INTO ALBUM_PERMISSIONS(USER_ID, ALBUM_ID, GRANTED) VALUES (?, ?, ?);",
                (user['ID'], selected_album, granted)
            )
            db.commit()
        except db.OperationalError as error:
            raise Exception('Could not perform query on the database: ''{}'.format(error))
        except db.IntegrityError:
            templ = f"""
                    <button class="button is-error is-static">Error: { db.IntegrityError }</button>
                    """
            return render_template_string(templ)
    else:
        try:
            db.execute(
                "UPDATE ALBUM_PERMISSIONS SET GRANTED=(?) WHERE USER_ID=(?) AND ALBUM_ID=(?);",
                (granted, user['ID'], selected_album)
            )
            db.commit()
        except db.OperationalError as error:
            raise Exception('Could not perform query on the database: ''{}'.format(error))
        except db.IntegrityError:
            LOG.error(f"{ db.IntegrityError }: Something went wrong while adding ALBUM_PERMISSIONS table.")
            templ = f"""
                    <button class="button is-error is-static">Error: { db.IntegrityError }</button>
                    """
            return render_template_string(templ)

    templ = f"""
            <button class="button is-success is-static">Success!</button>
            """
    return render_template_string(templ)


#
@bp.route("/backoffice/settings/update_album_permissions/make_thumbnails", methods=['GET'])
@login_required
def route_make_thumbnails():
    make_thumbnails()
    templ = f"""
                <button class="button is-success is-static">Success!</button>
                """
    return render_template_string(templ)


@bp.route("/backoffice/settings/update_album_permissions/make_gallery", methods=['GET'])
@login_required
def route_make_gallery():
    init_album_table()
    make_gallery(current_app)
    update_album_permissions_table()
    templ = f"""
                <button class="button is-success is-static">Success!</button>
                """
    return render_template_string(templ)


# renders a blank page
@bp.route("/blank", methods=['GET'])
def route_blank():
    return render_template("/partials/blank.html")


# renders the about page
@bp.route("/about", methods=['GET'])
def route_about():
    return render_template("/about.html")


# this is to prevent unauthorized access if not logged in
# @bp.route("/static/images/gallery/<image_name>.<extension>", methods=['GET'])
@bp.route("/static/images/gallery/<album>/<image_name>.<extension>", methods=['GET'])
def route_image_full_check(album, image_name, extension):
    if g.user is None:
        return render_template("/errors/401.html")
    else:
        db = get_db()
        try:
            granted_albums = db.execute(
                "SELECT ALBUM_ID FROM ALBUM_PERMISSIONS WHERE USER_ID=(?) AND GRANTED='TRUE';",
                (g.user[0],)
            )
        except db.OperationalError as error:
            raise Exception('Could not perform query on the database: ''{}'.format(error))
        except db.IntegrityError:
            LOG.error(f"{ db.IntegrityError }: Something went wrong.")
            return

        for db_album in granted_albums:
            if db_album[0] == album:
                image_path = f"{current_app.config['GALLERY_PATH']}/{album}/{image_name}.{extension}"
                return send_file(image_path, mimetype=f"image/{extension}")

        return render_template("/errors/401.html")


@bp.route("/teapot", methods=['GET'])
def route_teapot():
    return render_template("/errors/418.html")


# functions
def get_images():
    # https://stackoverflow.com/a/50252485 - sql natural sorting, not perfect but will do for now
    db = get_db()
    if g.user is None:
        try:
            images = db.execute(
                "SELECT * FROM GALLERY WHERE ALBUM='ROOT' ORDER BY LENGTH(NAME), NAME;"
            )
        except db.OperationalError as error:
            raise Exception('Could not perform query on the database: ''{}'.format(error))
        except db.IntegrityError:
            LOG.error(f"{ db.IntegrityError }: Something went wrong.")
            return
        return images.fetchall()
    else:
        try:
            granted_albums = db.execute(
                "SELECT ALBUM_ID FROM ALBUM_PERMISSIONS WHERE USER_ID=(?) AND GRANTED='TRUE';",
                (g.user[0],)
            )
            total_granted_albums = db.execute(
                "SELECT COUNT(ALBUM_ID) FROM ALBUM_PERMISSIONS WHERE USER_ID=(?) AND GRANTED='TRUE';",
                (g.user[0],)
            )
        except db.OperationalError as error:
            raise Exception('Could not perform query on the database: ''{}'.format(error))
        except db.IntegrityError:
            LOG.error(f"{ db.IntegrityError }: Something went wrong.")
            return

        sql_query = ""
        total = total_granted_albums.fetchone()[0]
        i = 0
        for album in granted_albums:
            i = i + 1
            if not i <= total - 1:
                sql_query = sql_query + "ALBUM='" + album[0] + "'"
            else:
                sql_query = sql_query + "ALBUM='" + album[0] + "' OR "
        try:
            images = db.execute(
                f"SELECT * FROM GALLERY WHERE { sql_query } ORDER BY LENGTH(NAME), NAME;"
            )
        except db.OperationalError as error:
            raise Exception('Could not perform query on the database: ''{}'.format(error))
        except db.IntegrityError:
            LOG.error(f"{ db.IntegrityError }: Something went wrong.")
            return

        return images.fetchall()


def get_image_by_id(id):
    db = get_db()
    try:
        image = db.execute(
            "SELECT * FROM GALLERY WHERE ID = ?;",
            (id,)
        )
    except db.OperationalError as error:
        raise Exception('Could not perform query on the database: ''{}'.format(error))
    except db.IntegrityError:
        LOG.error(f"{ db.IntegrityError }: Something went wrong.")
        return
    return image.fetchone()


