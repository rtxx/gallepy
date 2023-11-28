# gallepy
photo gallery made with flask and htmx

gallepy is a simple gallery made with python and htmx that I made in an atempt to learn python, flask and htmx.

To use it, simply put your photos on the gallery folder and that's it!

It has some features, like:

- Thumbnails are created for each image automatically
- Albuns with permissions per user (eventually)
- Lazy loading
- Infinite scroll
- Smooth CSS animations
- No javascript! (apart from htmx and hyperscript)

Check [here](https://photos.ruiteixeira.me) to see in action.

To run it:
```
flask --app gallepy --debug run --host=0.0.0.0
```

