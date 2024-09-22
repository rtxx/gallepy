

# gallepy
> Photo gallery made with flask and htmx

**gallepy** is a simple gallery that I made in an attempt to learn [python](https://www.python.org/), [flask](https://flask.palletsprojects.com/en/3.0.x/) and [htmx](https://htmx.org/).

To use it, simply put your photos on the gallery folder and that's it!

It has some features, like:

- Thumbnails are created for each image automatically
- Create albums with permissions per user
- Lazy loading with infinite scroll
- Smooth CSS animations
- Made with [Bulma CSS](https://bulma.io/)

Check [here](https://gallery.ducknexus.com/) to see in action.
![Main Page](https://cloud.ducknexus.com/s/bfYLqRaBpFdZnXx/download/gallepy1.png)
![User page](https://cloud.ducknexus.com/s/XDbnjsLGy422erW/download/gallepy3.png)
## Python requirements

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
> If you need to create albums, they are just sub-folders of ```gallepy/static/images/gallery```

- Start ```gallepy``` with the ```start_server.sh``` and follow the these steps:
  - Copy the default password from the terminal and login with the ```admin``` user
    - This will be the first and last time the default password will appear, so make sure you store it safely, or change it on first login!
  - Go to ```Settings``` and click on ```Make thumbnails``` and ```Remake gallery```
  - That's it!

### Alternative, you can also follow the following steps
- Init the database: 
```
cd [root of the git folder]
flask --app gallepy init-db
```
> Make sure the get the ```admin``` login, otherwise you will need to ```init-db``` again

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

- Login with the ```admin``` user and go the ```Settings``` tab
- After creating the new user, use ```Update album permissions``` to add or remove permissions from the available albums


