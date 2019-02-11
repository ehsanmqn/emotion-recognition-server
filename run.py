from flask import Flask
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager

app = Flask(__name__)
api = Api(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'some-secret-string'

db = SQLAlchemy(app)

from models import AnalyticsModel, UserModel

@app.before_first_request
def create_tables():
    db.create_all()
    db.session.commit()

app.config['JWT_SECRET_KEY'] = 'jwt-secret-string'
jwt = JWTManager(app)


app.config['JWT_BLACKLIST_ENABLED'] = True
app.config['JWT_BLACKLIST_TOKEN_CHECKS'] = ['access', 'refresh']

@jwt.token_in_blacklist_loader
def check_if_token_in_blacklist(decrypted_token):
    jti = decrypted_token['jti']
    return models.RevokedTokenModel.is_jti_blacklisted(jti)

import views, models, resources

# User authentication APIs
api.add_resource(resources.UserRegistration, '/api/register')
api.add_resource(resources.UserLogin, '/api/login')
api.add_resource(resources.UserLogoutAccess, '/api/logout/access')
api.add_resource(resources.UserLogoutRefresh, '/api/logout/refresh')
api.add_resource(resources.TokenRefresh, '/api/token/refresh')
api.add_resource(resources.AllUsers, '/api/users')
api.add_resource(resources.SecretResource, '/api/secret')

# Emotion analysis APIs
api.add_resource(resources.PredictWithModel1, '/api/predict/model1')
api.add_resource(resources.PredictWithModel1ForAVA, '/api/predict/avamodel1')

# Analytics APIs
api.add_resource(resources.AddAnalytics, '/api/analytics/add')
api.add_resource(resources.AllAnalytics, '/api/analytics/list/all')
api.add_resource(resources.AllAnalyticsIncomings, '/api/analytics/list/incomings')
api.add_resource(resources.AllAnalyticsOutgoings, '/api/analytics/list/outgoings')
api.add_resource(resources.AllAnalyticsFiles, '/api/analytics/list/files')
api.add_resource(resources.AllAnalyticsExtensions, '/api/analytics/list/extensions')
api.add_resource(resources.AnalyticsByExtension, '/api/analytics/filter/byextension')
api.add_resource(resources.AnalyticsByUsername, '/api/analytics/filter/byusername')
api.add_resource(resources.AnalyticsByFilename, '/api/analytics/filter/byfilename')
api.add_resource(resources.AnalyticsByMonth, '/api/analytics/filter/bymonth')
api.add_resource(resources.AnalyticsByDay, '/api/analytics/filter/byday')
api.add_resource(resources.AnalyticsByYear, '/api/analytics/filter/byyear')
# api.add_resource(resources.AnalyticsByFilename, '/api/analytics/byfilename')

if __name__ == '_main_':
	app.run(host='0.0.0.0',threaded=True)