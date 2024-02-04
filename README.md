

# gallepy
> Photo gallery made with flask and htmx

**gallepy** is a simple gallery that I made in an atempt to learn [python](https://www.python.org/), [flask](https://flask.palletsprojects.com/en/3.0.x/) and [htmx](https://htmx.org/).

To use it, simply put your photos on the gallery folder and that's it!

It has some features, like:

- Thumbnails are created for each image automatically
- Create albuns with permissions per user
- Lazy loading with infinite scroll
- Smooth CSS animations
- Made with [Bulma CSS](https://bulma.io/)

Check [here](https://photos.ruiteixeira.me) to see in action.
![Main Page](https://cloud.ducknexus.com/s/bfYLqRaBpFdZnXx/download/gallepy1.png)
![User page](https://cloud.ducknexus.com/s/XDbnjsLGy422erW/download/gallepy3.png)
## Python requirments

- flask
- pillow
- bcrypt

Optional but **recommended**:
- gunicorn

> For convenience, there is a ```requirements.txt```

## How to use it

- (Optional but **recommended**) Create a new venv for this project

- Clone this repo:
```
clone git https://github.com/rtxx/gallepy.git
```

- Copy the images to the gallery folder:
```
gallepy/static/images/gallery
```
> If you need to create albuns, they are just subfolders of ```gallepy/static/images/gallery```

- Init the database: 
```
cd [root of the git folder]
flask --app gallepy init-db
```
> Make sure the get the admin login, otherwise you will need to ```init-db``` again

- Generate the thumbnails: 
```
cd [root of the git folder]
flask --app gallepy make-thumbnails
```

- Make the gallery: 
```
cd [root of the git folder]
flask --app gallepy make-gallery
```
> After adding or removing images from the gallery folder, use this command to refresh the database

- Run it:
```
cd [root of the git folder]
bash start_server.sh
```

- If you don't want to use a WSGI server like [gunicorn](https://gunicorn.org/), you can use the flask built-in server:
```
cd [root of the git folder]
flask --app gallepy run --host=0.0.0.0
```

- You can now go to ```localhost:5000```


## Creating users and adding permissions to them

Login to with the admin user and go the settings tab

