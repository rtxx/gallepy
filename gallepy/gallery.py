import click
import os
from PIL import Image, ImageOps
from flask import current_app
from .config import LOG
from .db import get_db


class GalleryImage:

    def __init__(self, id, name, image_path, thumbnail_path, album, image_width, image_height, thumbnail_width, thumbnail_height):
        self.id = id or "null"
        self.name = name
        self.image_path = image_path
        self.thumbnail_path = thumbnail_path
        self.album = album
        self.image_width = image_width
        self.image_height = image_height
        self.thumbnail_width = thumbnail_width
        self.thumbnail_height = thumbnail_height
        # LOG.info(f"new image: {self.number} : {self.name}")

        
def init_app(app):
    app.cli.add_command(make_thumbnails_command)
    app.cli.add_command(make_gallery_command)


@click.command('make-gallery')
def make_gallery_command():
    init_album_table()
    make_gallery(current_app)
    init_album_permissions_table()
    return


@click.command('make-thumbnails')
def make_thumbnails_command():
    make_thumbnails()
    return


def make_thumbnails():
    gallery_path = current_app.config['GALLERY_PATH']
    thumbnails_path = current_app.config['THUMBNAILS_PATH']

    LOG.info(f"Searching '{gallery_path}' for images...")
    for file in os.listdir(gallery_path):
        current_file = f"{gallery_path}/{file}"
        # print(f"Found {file}, checking if thumbnail exists...")
        if os.path.isfile(current_file):
            img_thumbnail = f"{thumbnails_path}/{file}"
            if os.path.exists(img_thumbnail):
                LOG.warning(f"{current_file} : Thumbnail exists, continuing...")
            else:
                # print("Not found! Creating...")
                ext = os.path.splitext(current_file)[-1].lower()
                if ext == ".jpg" or ext == ".jpeg" or ext == ".png":
                    make_thumbnail(current_file, thumbnails_path)
                    LOG.info(f"{current_file} : Thumbnail created")
                else:
                    LOG.error(f"{current_file} : file is not a image, ignoring...")
        else:
            LOG.info(f"Album found - {current_file}")
            album_gallery_path = f"{gallery_path}/{file}"
            album_thumbnail_path = f"{thumbnails_path}/{file}"
            if not os.path.exists(album_thumbnail_path):
                os.mkdir(album_thumbnail_path)
                LOG.info(f"{current_file} : folder created")
            for album_img in os.listdir(album_gallery_path):
                current_gallery_img = f"{gallery_path}/{file}/{album_img}"
                current_thumbnail_img = f"{thumbnails_path}/{file}/{album_img}"
                if os.path.exists(current_thumbnail_img):
                    LOG.warning(f"{current_gallery_img} : Thumbnail exists, continuing...")
                else:
                    ext = os.path.splitext(current_gallery_img)[-1].lower()
                    if ext == ".jpg" or ext == ".jpeg" or ext == ".png":
                        make_thumbnail(current_gallery_img, album_thumbnail_path)
                        LOG.info(f"{current_gallery_img} : Thumbnail created")
                    else:
                        LOG.error(f"{current_gallery_img} : file is not a image, ignoring...")
    LOG.info("Done!")
    return


def make_thumbnail(image, thumbnails_path):
    # https://stackoverflow.com/a/8384786
    path, name_with_extension = os.path.split(image)
    img = Image.open(image)
    img = ImageOps.exif_transpose(img)
    img.thumbnail((512, 512), Image.Resampling.LANCZOS)
    img.save(f"{thumbnails_path}/{name_with_extension}")


def delete_gallery_data():
    db = get_db()
    try:
        db.execute(
            "DELETE FROM GALLERY;"
        )
        db.commit()
        LOG.info(f"Deleted all rows from GALLERY")
    except db.IntegrityError:
        LOG.error(f"{db.IntegrityError}: Something went wrong while removing all rows from GALLERY table.")
        LOG.error(f"Something went wrong, exiting...")
        return

    # https://www.designcise.com/web/tutorial/how-to-reset-autoincrement-number-sequence-in-sqlite
    # updating autoincrement to 0
    try:
        db.execute(
            "UPDATE `sqlite_sequence` SET `seq` = 0 WHERE `name` = 'GALLERY';"
        )
        db.commit()
        LOG.info(f"Resetting AUTOINCREMENT from GALLERY table")
    except db.IntegrityError:
        LOG.error(f"{db.IntegrityError}: Something went wrong while setting sqlite_sequence to 0.")
        LOG.error(f"Something went wrong, exiting...")
        return

    return


def insert_image_db(image):
    db = get_db()
    # LOG.info(f"Inserting {image.name} into db.")

    # it's inserting without checking if exists already
    try:
        db.execute(
            "INSERT INTO GALLERY (NAME, IMAGE_PATH, THUMBNAIL_PATH, ALBUM, IMAGE_WIDTH, IMAGE_HEIGHT, THUMBNAIL_WIDTH, THUMBNAIL_HEIGHT) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
            (image.name, image.image_path, image.thumbnail_path, image.album, image.image_width, image.image_height,
             image.thumbnail_height, image.thumbnail_height),
        )
        db.commit()
    except db.IntegrityError:
        LOG.error(f"{db.IntegrityError}: Something went wrong while inserting {image.name} into the db.")
        LOG.error(f"Something went wrong, exiting...")
        return
    return


# load gallery images into db
def make_gallery(app):
    gallery_path = app.config['GALLERY_PATH']
    relative_gallery_path = app.config['RELATIVE_GALLERY_PATH']
    thumbnails_path = app.config['THUMBNAILS_PATH']
    relative_thumbnails_path = app.config['RELATIVE_THUMBNAILS_PATH']

    delete_gallery_data()

    # image_list = []
    LOG.info(f"Searching '{gallery_path}' for images...")

    for file in os.listdir(gallery_path):
        current_file = f"{gallery_path}/{file}"
        if os.path.isfile(current_file):
            ext = os.path.splitext(current_file)[-1].lower()
            if ext == ".jpg" or ext == ".jpeg" or ext == ".png":
                # current_img_thumbnail = f"{THUMBNAILS_PATH}/{file}"
                temp = Image.open(f"{gallery_path}/{file}")
                image = GalleryImage(
                    "null",
                    file,
                    f"{relative_gallery_path}/{file}",
                    f"{relative_thumbnails_path}/{file}",
                    "ROOT",
                    temp.width,
                    temp.height,
                    512,
                    512,
                )
                insert_image_db(image)
                # image_list.append(image)
                # LOG.info(f"{image.name} : image added to 'db' as public")
            else:
                LOG.warning(f"{current_file} : file is not a image, ignoring...")
        else:
            LOG.info(f"Album found - {current_file}")
            album_name = file
            album_gallery_path = f"{gallery_path}/{album_name}"
            insert_new_album(album_name)
            for album_img in os.listdir(album_gallery_path):
                # current_thumbnail_img = f"{THUMBNAILS_PATH}/{file}/{album_img}"
                current_gallery_img = f"{gallery_path}/{album_name}/{album_img}"
                ext = os.path.splitext(current_gallery_img)[-1].lower()
                if ext == ".jpg" or ext == ".jpeg" or ext == ".png":
                    temp = Image.open(f"{gallery_path}/{album_name}/{album_img}")
                    image = GalleryImage(
                        "null",
                        album_img,
                        f"{relative_gallery_path}/{album_name}/{album_img}",
                        f"{relative_thumbnails_path}/{album_name}/{album_img}",
                        album_name,
                        temp.width,
                        temp.height,
                        512,
                        512
                    )
                    insert_image_db(image)
                    # image_list.append(image)
                    # LOG.info(f"{image.name} : image added of album '{album_name}'")
                else:
                    LOG.warning(f"{current_gallery_img} : file is not a image, ignoring...")

    LOG.info("Done!")
    return


# redundant function, just pass "ROOT" album name
def init_album_table():
    db = get_db()
    try:
        db.execute(
            "INSERT INTO ALBUM (NAME) SELECT (?) WHERE NOT EXISTS(SELECT 1 FROM ALBUM WHERE NAME=(?));",
            ("ROOT","ROOT")
        )
        db.commit()
        LOG.info(f"ALBUM table initialized")
    except db.IntegrityError:
        LOG.error(f"{db.IntegrityError}: Something went wrong while initializing ALBUM table.")
        return


def insert_new_album(album):
    db = get_db()
    try: 
        db.execute(
            "INSERT INTO ALBUM (NAME) SELECT (?) WHERE NOT EXISTS(SELECT 1 FROM ALBUM WHERE NAME=(?));",
            (album,album)
        )
        db.commit()
        LOG.info(f"New album added to table ALBUM: {album}")
    except db.IntegrityError:
        LOG.error(f"{db.IntegrityError}: Something went wrong while adding new album to ALBUM table.")
        return


def init_album_permissions_table():
    db = get_db()
    # assuming admin is user_id 1
    # loop all albums available
    # set GRANTED to TRUE
    LOG.info("Initializing ALBUM_PERMISSIONS table")
    albums = None
    try:
        query = db.execute(
            "SELECT * FROM ALBUM;"
        )
    except db.IntegrityError:
        LOG.error(f"{db.IntegrityError}: Something went wrong.")
        return
    albums = query.fetchall()
    try:
        for album in albums:
            db.execute(
                "INSERT INTO ALBUM_PERMISSIONS(USER_ID, ALBUM_ID, GRANTED) SELECT 1, (?), 'TRUE' WHERE NOT EXISTS(SELECT 1 FROM ALBUM_PERMISSIONS WHERE USER_ID=1 AND ALBUM_ID=(?) AND GRANTED='TRUE');",
                (album[1],album[1])
            )
            db.commit()
            #LOG.info(f"admin has {album[1]} permission")
    except db.IntegrityError:
        LOG.error(f"{db.IntegrityError}: Something went wrong while initializing ALBUM_PERMISSIONS table.")
        return
    LOG.info("Done!")
    return


