#
# This file contains API endpoits
#

from flask_restful import Resource
from flask_restful import Resource, reqparse
from models import UserModel, RevokedTokenModel
from flask_jwt_extended import (create_access_token, create_refresh_token, jwt_required, jwt_refresh_token_required, get_jwt_identity, get_raw_jwt)
from run import app
from flask import jsonify
from flask import Flask, url_for, send_from_directory, request
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager, jwt_required
from werkzeug import secure_filename
import sys
import logging, os
import scipy.io.wavfile
import Vokaturi
import process
from setting import APP_STATIC

Vokaturi.load("./emotion-lib-linux64.so")

parser = reqparse.RequestParser()
parser.add_argument('username', help = 'This field cannot be blank', required = True)
parser.add_argument('password', help = 'This field cannot be blank', required = True)

file_handler = logging.FileHandler('server.log')
app.logger.addHandler(file_handler)
app.logger.setLevel(logging.INFO)


class UserRegistration(Resource):
    def post(self):
        data = parser.parse_args()
        if UserModel.find_by_username(data['username']):
            return {'message': 'User {} already exists'. format(data['username'])}

        new_user = UserModel(
            username = data['username'],
            password = UserModel.generate_hash(data['password'])
        )
        try:
            new_user.save_to_db()
            access_token = create_access_token(identity = data['username'])
            refresh_token = create_refresh_token(identity = data['username'])
            return {
                'message': 'User {} was created'.format(data['username']),
                'access_token': access_token,
                'refresh_token': refresh_token
                }
        except:
            return {'message': 'Something went wrong'}, 500


class UserLogin(Resource):
    def post(self):
        data = parser.parse_args()
        current_user = UserModel.find_by_username(data['username'])
        if not current_user:
            return {'message': 'User {} doesn\'t exist'.format(data['username'])}
        
        if UserModel.verify_hash(data['password'], current_user.password):
            access_token = create_access_token(identity = data['username'])
            refresh_token = create_refresh_token(identity = data['username'])
            return {
                'message': 'Logged in as {}'.format(current_user.username),
                'access_token': access_token,
                'refresh_token': refresh_token
                }
        else:
            return {'message': 'Wrong credentials'}
      
      
class UserLogoutAccess(Resource):
    @jwt_required
    def post(self):
        jti = get_raw_jwt()['jti']
        try:
            revoked_token = RevokedTokenModel(jti = jti)
            revoked_token.add()
            return {'message': 'Access token has been revoked'}
        except:
            return {'message': 'Something went wrong'}, 500
      
      
class UserLogoutRefresh(Resource):
    @jwt_refresh_token_required
    def post(self):
        jti = get_raw_jwt()['jti']
        try:
            revoked_token = RevokedTokenModel(jti = jti)
            revoked_token.add()
            return {'message': 'Refresh token has been revoked'}
        except:
            return {'message': 'Something went wrong'}, 500
      
      
class TokenRefresh(Resource):
    @jwt_refresh_token_required
    def post(self):
        current_user = get_jwt_identity()
        access_token = create_access_token(identity = current_user)
        return {'access_token': access_token}
      
      
class AllUsers(Resource):
    def get(self):
        return UserModel.return_all()
    
    def delete(self):
        return UserModel.delete_all()
      
      
class SecretResource(Resource):
    @jwt_required
    def get(self):
        return {
            'answer': 42
        }

class PredictWithModel1(Resource):
    # @jwt_required
    def post(self):
        files = request.files['file']
        PROJECT_HOME = os.path.dirname(os.path.realpath(__file__))
        UPLOAD_FOLDER = '{}/uploads/'.format(PROJECT_HOME)
        ALLOWED_EXTENSIONS = set(['wav'])
        app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
        _dir = os.path.join(UPLOAD_FOLDER)
        if not os.path.isdir(_dir):
            os.mkdir(_dir)
        filename = secure_filename(files.filename)
        print (filename)
        to_path = os.path.join(_dir, filename)
        files.save(to_path)
        result = process.model1GetResult(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        return jsonify(result)

class PredictWithModel1ForAVA(Resource):
    # @jwt_required
    def post(self):
        files = request.form['file']
        _dir =""
        with open(os.path.join(APP_STATIC, 'saba.conf')) as f:
            _dir = f.read()
        if not os.path.isdir(_dir[:-1]):
            result = "<saba><request>failed</request><model>1</model><result>Directory not found</result></saba>"
            return result
        filename = secure_filename(files)
        app.config['UPLOAD_FOLDER'] = _dir
        result = process.model1GetResultForAVA(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        return result