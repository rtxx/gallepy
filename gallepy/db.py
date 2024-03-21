import os
import bcrypt
import click
import secrets
import sqlite3
from flask import current_app, g
from . import LOG


def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)
    app.cli.add_command(check_database)


# workaround for script usage, meaning run this command first then the app itself
@click.command('check-db')
def check_database():
    LOG.info("Database check")
    # database check
    if not os.path.exists(current_app.config['DATABASE']):
        LOG.error("NOT FOUND, creating a new one...")
        """Clear the existing data and create new tables."""
        LOG.info("Initializing database")
        init_db()

        # https://stackoverflow.com/a/61471228
        # creating new admin with random password
        db = get_db()

        admin_name = "Administrator"
        admin_username = "admin"
        password_length = 14
        password = secrets.token_urlsafe(password_length)
        salt = bcrypt.gensalt()
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)

        try:
            db.execute(
                "INSERT INTO USERS (NAME,USERNAME,HASHED_PASSWORD,TYPE) VALUES (?, ?, ?, ?)",
                (admin_name, admin_username, hashed_password, "admin"),
            )
            db.commit()
            LOG.info(f"Admin created: {admin_username} / {password}")

        except db.OperationalError as error:
            raise Exception('Could not perform query on the database: ''{}'.format(error))
        except db.IntegrityError:
            # this will never be reached,*I think*
            LOG.info(f"{admin_name} is already registered.")
        LOG.info("Done!")
    else:
        LOG.error("Database found, nothing to see here.")
        LOG.info("Done!")
    return


@click.command('init-db')
def init_db_command():
    """Clear the existing data and create new tables."""
    LOG.info("Initializing database")
    init_db()

    # https://stackoverflow.com/a/61471228
    # creating new admin with random password
    db = get_db()

    admin_name = "Administrator"
    admin_username = "admin"
    password_length = 14
    password = secrets.token_urlsafe(password_length)
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)

    try:
        db.execute(
            "INSERT INTO USERS (NAME,USERNAME,HASHED_PASSWORD,TYPE) VALUES (?, ?, ?, ?)",
            (admin_name, admin_username, hashed_password, "admin"),
        )
        db.commit()
        LOG.info(f"Admin created: { admin_username } / { password }")
    except db.OperationalError as error:
        raise Exception('Could not perform query on the database: ''{}'.format(error))
    except db.IntegrityError:
        # this will never be reached,*I think*
        LOG.info = f"{ admin_name } is already registered."
    LOG.info = "Done!"


def init_db():
    db = get_db()
    with current_app.open_resource('schema.sql') as f:
        db.executescript(f.read().decode('utf8'))


def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(
            current_app.config['DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row
    return g.db


def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        db.close()
