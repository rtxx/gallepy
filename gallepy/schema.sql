PRAGMA foreign_keys = ON;

DROP TABLE IF EXISTS ALBUM_PERMISSIONS;
DROP TABLE IF EXISTS ALBUM;
DROP TABLE IF EXISTS USERS;
DROP TABLE IF EXISTS GALLERY;

CREATE TABLE USERS (
    ID                  INTEGER PRIMARY KEY AUTOINCREMENT,
    NAME                TEXT                                NOT NULL,
    USERNAME            TEXT                                NOT NULL,
    HASHED_PASSWORD     TEXT                                NOT NULL,
    TYPE                TEXT                                NOT NULL
);

CREATE TABLE GALLERY (
    ID                  INTEGER PRIMARY KEY AUTOINCREMENT,
    NAME                TEXT                                NOT NULL,
    IMAGE_PATH          TEXT                                NOT NULL,
    THUMBNAIL_PATH      TEXT                                NOT NULL,
    ALBUM               INTEGER                             NOT NULL,
    IMAGE_WIDTH         INTEGER                             NOT NULL,
    IMAGE_HEIGHT        INTEGER                             NOT NULL,
    THUMBNAIL_WIDTH     INTEGER                             NOT NULL,
    THUMBNAIL_HEIGHT    INTEGER                             NOT NULL,
    FOREIGN KEY (ALBUM) REFERENCES ALBUM(ID) 
    ON UPDATE CASCADE
    ON DELETE CASCADE
);

CREATE TABLE ALBUM (
  	ID                  INTEGER PRIMARY KEY AUTOINCREMENT,
    NAME                TEXT 				                  NOT NULL
  	
);

CREATE TABLE ALBUM_PERMISSIONS (
  	ID                  INTEGER PRIMARY KEY AUTOINCREMENT,
  	USER_ID           	TEXT                     			NOT NULL,
    ALBUM_ID            TEXT                     			NOT NULL,
  	GRANTED				TEXT								NOT NULL,
    FOREIGN KEY (USER_ID) REFERENCES USERS(ID) 
    ON UPDATE CASCADE
    ON DELETE CASCADE
    FOREIGN KEY (ALBUM_ID) REFERENCES ALBUM(ID) 
    ON UPDATE CASCADE
    ON DELETE CASCADE
);

