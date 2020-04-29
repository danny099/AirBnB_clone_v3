#!/usr/bin/python3
"""Api rest"""
from os import getenv
from models import storage
from api.v1.views import app_views
from flask import Flask, Blueprint, make_response, jsonify


app = Flask(__name__)
app.register_blueprint(app_views)


@app.teardown_appcontext
def teardown(exception):
    storage.close()


@app.errorhandler(404)
def error_404(error):
    return make_response(jsonify(error='Not found'), 404)


if __name__ == "__main__":
    app.run(host=getenv('HBNB_API_HOST'), port=getenv('HBNB_API_PORT'),
            threaded=True),
