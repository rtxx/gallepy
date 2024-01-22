

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
![Main Page](https://cloud.ducknexus.com/s/bfYLqRaBpFdZnXx/download/gallepy1.png)![User page](https://cloud.ducknexus.com/s/XDbnjsLGy422erW/download/gallepy3.png)
## Python requirments

- flask
- pillow
- bcrypt
- sqlite3

Optional but **recommended**:
- gunicorn

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

- Then generate the thumbnails: 
```
cd [root of the git folder]
flask --app gallepy init-thumbnails
```

- Finally run it:
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

> The default login is ```admin/admin1234``` and ```user/user1234```

## Create users
> Attention! This is a WIP feature and it's in pre-alpha quality if you can even call it that.

- Go to ```gallepy/db.py``` and create your new users by adding them on the ```init_users_db()``` function
- Remember that you need to define the albuns that the new user can view. To do that, just specify the name of the album


