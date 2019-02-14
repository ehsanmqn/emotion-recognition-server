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

### User authentication APIs
# Register new user
api.add_resource(resources.UserRegistration, '/api/register')
# Login with username and password
api.add_resource(resources.UserLogin, '/api/login')
# Logout user
api.add_resource(resources.UserLogoutAccess, '/api/logout/access')
# Logout refresh
api.add_resource(resources.UserLogoutRefresh, '/api/logout/refresh')
# Refresh token
api.add_resource(resources.TokenRefresh, '/api/token/refresh')
# List all the users
api.add_resource(resources.AllUsers, '/api/users')
# I dont know what is this!!!
api.add_resource(resources.SecretResource, '/api/secret')
# Check token validation 
api.add_resource(resources.TokenValidate, '/api/token/validate')

### Emotion analysis APIs
# Analyze file for emotions. File upload via POST. results will be added to db
api.add_resource(resources.PredictWithModel1, '/api/predict/model1')
# Analyze file for emotions. File upload via POST. results will not added to db
api.add_resource(resources.PredictWithModel1Test, '/api/predict/model1test')
# Analyze file for emotions. File read from local folder or NAS
# api.add_resource(resources.PredictWithModel1ForAVA, '/api/predict/avamodel1')

### Analytics APIs
# Add new row to analytics table
# api.add_resource(resources.AddAnalytics, '/api/analytics/add')
# List all the analytics
api.add_resource(resources.AllAnalytics, '/api/analytics/list/all')	
# List all the incoming calls analytics
api.add_resource(resources.AllAnalyticsIncomings, '/api/analytics/list/incomings')
# List all the outgoing call analytics
api.add_resource(resources.AllAnalyticsOutgoings, '/api/analytics/list/outgoings')
# List all the processed files in analytics
api.add_resource(resources.AllAnalyticsFiles, '/api/analytics/list/files')
# List all the extensions in analytics
api.add_resource(resources.AllAnalyticsExtensions, '/api/analytics/list/extensions')
# Filter analytics by a specific extension
api.add_resource(resources.AnalyticsByExtension, '/api/analytics/filter/extension')
# Filter analytics by a username
api.add_resource(resources.AnalyticsByUsername, '/api/analytics/filter/username')
# Filter analytics by a filename
api.add_resource(resources.AnalyticsByFilename, '/api/analytics/filter/filename')
# Filter analytics by a specific day
api.add_resource(resources.AnalyticsByDay, '/api/analytics/filter/day')
# Get average call duration in a specific day
api.add_resource(resources.AnalyticsByDayAverageDuration, '/api/analytics/filter/day/duration/average')
# Get average angry in a specific day
api.add_resource(resources.AnalyticsByDayAverageAngry, '/api/analytics/filter/day/angry/average')
# Get average happy in a specific day
api.add_resource(resources.AnalyticsByDayAverageHappy, '/api/analytics/filter/day/happy/average')
# Get average neutral in a specific day
api.add_resource(resources.AnalyticsByDayAverageNeutral, '/api/analytics/filter/day/neutral/average')
# Get average sad in a specific day
api.add_resource(resources.AnalyticsByDayAverageSad, '/api/analytics/filter/day/sad/average')
# Get average fear in a specific day
api.add_resource(resources.AnalyticsByDayAverageFear, '/api/analytics/filter/day/fear/average')
# Get average emotions in a specific day
api.add_resource(resources.AnalyticsByDayAverageEmotions, '/api/analytics/filter/day/emotions/average')
# Get total number of calls in a specific day
api.add_resource(resources.AnalyticsByDayTotalCalls, '/api/analytics/filter/day/call/total')
# Get total number of incoming calls in a specific day
api.add_resource(resources.AnalyticsByDayTotalIncomingCalls, '/api/analytics/filter/day/call/incoming')
# Get total number of outgoing calls in a specific day
api.add_resource(resources.AnalyticsByDayTotalOutgoingCalls, '/api/analytics/filter/day/call/outgoing')
# Get max call duration in a specific day
# api.add_resource(resources.AnalyticsByDayAverageDuration, '/api/analytics/filter/day/duration/max')
# Get min call duration in a specific day
# api.add_resource(resources.AnalyticsByDayAverageDuration, '/api/analytics/filter/day/duration/min')
# Filter analytics by a specific month
api.add_resource(resources.AnalyticsByMonth, '/api/analytics/filter/month')
# Get average call duration in a specific month
api.add_resource(resources.AnalyticsByMonthAverageDuration, '/api/analytics/filter/month/duration/average')
# Filter analytics by a specific year
api.add_resource(resources.AnalyticsByYear, '/api/analytics/filter/year')
# Get average call duration in a specific year
api.add_resource(resources.AnalyticsByYearAverageDuration, '/api/analytics/filter/year/duration/average')

if __name__ == '_main_':
	app.run(host='0.0.0.0',threaded=True)