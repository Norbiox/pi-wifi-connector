#!/bin/bash
export FLASK_ENV=app.py
export FLASK_ENV=production

python3 -m flask run --host=0.0.0.0 --port=8080 --no-reload
