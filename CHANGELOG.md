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

