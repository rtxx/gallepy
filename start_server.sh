#!/bin/bash
#uwsgi --http 0.0.0.0:5000 --master -p 4 -w 'gallepy:create_app()'
# flask --app gallepy init-thumbnails
gunicorn -w 4 -b 0.0.0.0:5000 'gallepy:create_app()' --access-logfile -