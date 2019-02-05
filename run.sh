#!/bin/bash
export SECRET_KEY=thats-my-s3cr3tly-keeped-key
export FLASK_ENV=app.py
export FLASK_ENV=development

python3 -m flask run --host=0.0.0.0 --port=8080 --no-reload
