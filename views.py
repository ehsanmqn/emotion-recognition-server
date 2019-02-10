from run import app
from flask import jsonify
from flask import Flask, url_for, send_from_directory, request
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager, jwt_required
import logging, os
from werkzeug import secure_filename
import sys

@app.route('/')
def index():
    return jsonify({'message': 'Hello, Saba is waiting for you!'})


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=False, threaded=True)