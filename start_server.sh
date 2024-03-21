#!/bin/bash
# uwsgi --http 0.0.0.0:5000 --master -p 4 -w 'gallepy:create_app()'
# flask --app gallepy run --host=0.0.0.0 --port=5000
flask --app gallepy check-db && gunicorn -w 1 -b 0.0.0.0:5000 'gallepy:create_app()' --timeout 240 --access-logfile -


