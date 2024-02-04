## [0.2] - 2024-02-04

There is **alot** of changes on this release, beginning with a major restructure of the code, including a *proper* database system for the users and new commands.

The code still makes an italian person blush with all the spaghetti, but it's better than it was.

### Added

- Database: ```db.sqlite schema.sql``` added
  - A sqlite db is now added to the mix:
    - Stores the images paths, thumbnails paths, etc...
    - Stores users data
    - Stores users permission data

- New file```config.py```: It has some useful configurations, like databse path and such
- New file```gallery.py```: Functions relating to the gallery, like ```make-gallery```
- New command ```init-db```: Initializes the database with a new admin account
- New command ```make-thumbnails```: Makes thumbnails for the images
- New command ```make-gallery```: Makes the gallery, by inserting the images and albums into the db
- A default admin account is now created when the database is initialized
- User creating is now possible in the backoffice page
- User permissions on the albums is now possible in the backoffice page
- Users can now update their passwords
- Added basic client-side verification on login form with hyperscript
- Added ```requirements.txt``` for pip

### Fixed

- Fixed bug where when swiping through the gallery, if the initial image was not loaded, it displayed the thumbnail instead of the full image 

### Changed

- Log to console should be now better, with the ```logging``` module
- Forms with passwords have now a "Show password" checkbox
- About page updated
- Some images have a weird aspect ratio, must investigate
- README.md updated

### Deleted

- Command ```init-thumbnails``` is no longer avaiable
- File```configs.py``` is no longer available, it is now renamed ```config.py```
- Template partials ```image.full image-full-html image-full-modal``` are no longer available

### Known Bugs

- On user creation, existing users are not checked so be careful with duplicates
- Filter by album is not working
- Login form notification is off-center
- If new images are added, ```make-gallery``` is needed to load them this is will result in deleting the user permissions table. Its annoying but in the future will fix this

## [0.1.1-UNRELEASED] - 2024

### Added

- Added HTML templates for 401, 404, 418 and 500 HTTP errors and respective routes.

### Fixed

- Fixed bug where it was possible to access restricted image without login. Note: This is tied to the path from ```config.py```, need to found a solution for that.

### Changed

- Changed ```about.html``` to have gallepy version

### Removed

## [0.1-hotfix2] - 2024-01-22

### Added

- Add to remove dist/ from .gitignore because PhotoSwipe is on a folder called dist 
- Added 2 images to the gallery so when gallepy is launched it has something to display.

## [0.1-hotfix1] - 2024-01-22

### Changed

- Changed README.md, CHANGELOG.md and LICENSE to root folder

## [0.1] - 2024-01-22

This is not the 1st version of this project, but it will be from now on.

### Added

- Added this changelog to *try* to keep changes across versions.
- Added [PhotoSwipe](https://github.com/dimsemenov/PhotoSwipe) as the gallery viewer.
- Added a startup script `start_server.sh`, to make it easier to start `gallepy`.

### Changed

- The file layout of this repo was changed to be easier to start as a `flask` application.
- The gallery and thumbnails images folder are now on a different path, to make it easier to update.
- `README.md` updated.

### Known Bugs

- When swiping through the gallery, if the initial image was not loaded, it will show the thumbnail instead of the full image resolution. To fix it, scroll to the image in question and click it again.

