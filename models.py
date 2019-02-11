from run import db
from passlib.hash import pbkdf2_sha256 as sha256

class UserModel(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(120), unique = True, nullable = False)
    password = db.Column(db.String(120), nullable = False)
    
    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def find_by_username(cls, username):
        return cls.query.filter_by(username = username).first()

    @classmethod
    def return_all(cls):
        def to_json(x):
            return {
                'username': x.username,
                'password': x.password
            }
        return {'users': list(map(lambda x: to_json(x), UserModel.query.all()))}

    @classmethod
    def delete_all(cls):
        try:
            num_rows_deleted = db.session.query(cls).delete()
            db.session.commit()
            return {'message': '{} row(s) deleted'.format(num_rows_deleted)}
        except:
            return {'message': 'Something went wrong'}

    @staticmethod
    def generate_hash(password):
        return sha256.hash(password)

    @staticmethod
    def verify_hash(password, hash):
        return sha256.verify(password, hash)


class RevokedTokenModel(db.Model):
    __tablename__ = 'revoked_tokens'
    id = db.Column(db.Integer, primary_key = True)
    jti = db.Column(db.String(120))
    
    def add(self):
        db.session.add(self)
        db.session.commit()
    
    @classmethod
    def is_jti_blacklisted(cls, jti):
        query = cls.query.filter_by(jti = jti).first()
        return bool(query)

class AnalyticsModel(db.Model):
    __tablename__ = 'analytics'

    id = db.Column(db.Integer, primary_key = True)
    extension = db.Column(db.Integer, nullable = False)
    username = db.Column(db.String(120), nullable = False)
    filename = db.Column(db.String(250), unique = True, nullable = False)
    time = db.Column(db.DateTime, nullable = False)
    day = db.Column(db.Integer, nullable = False)
    month = db.Column(db.Integer, nullable = False)
    year = db.Column(db.Integer, nullable = False)
    duration = db.Column(db.Integer, nullable = False)
    direction = db.Column(db.Integer, nullable = False)
    location = db.Column(db.String(120), nullable = False)
    status = db.Column(db.Integer, nullable = False)
    angry = db.Column(db.Float, nullable = False)
    happy = db.Column(db.Float, nullable = False)
    neutral = db.Column(db.Float, nullable = False)
    sad = db.Column(db.Float, nullable = False)
    fear = db.Column(db.Float, nullable = False)
    
    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def findByExtension(cls, extension):
        return cls.query.filter_by(extension = extension).first()

    @classmethod
    def findByFilename(cls, filename):
        return cls.query.filter_by(filename = filename).first()

    @classmethod
    def ReturnAll(cls):
        def to_json(x):
            return {
                'extension': x.extension,
                'username': x.username,
                'filename': x.filename,
                # 'time': x.time,
                'day': x.day,
                'month': x.month,
                'year': x.year,
                'duration': x.duration,
                'direction': x.direction,
                'location': x.location,
                'status': x.status,
                'angry': x.angry,
                'happy': x.happy,
                'neutral': x.neutral,
                'sad': x.sad,
                'fear': x.fear
            }

        return {'result': list(map(lambda x: to_json(x), AnalyticsModel.query.all()))}

    @classmethod
    def ReturnAllFilenames(cls):
        def to_json(x):
            return {
                'filename': x.filename,
            }

        return {'result': list(map(lambda x: to_json(x), AnalyticsModel.query.all()))}

    @classmethod
    def ReturnAllExtensions(cls):
        def to_json(x):
            return {
                'extension': x.extension,
            }

        return {'result': list(map(lambda x: to_json(x), AnalyticsModel.query.all()))}

    @classmethod
    def ReturnAllIncomings(cls):
        def to_json(x):
            return {
                'extension': x.extension,
                'username': x.username,
                'filename': x.filename,
                # 'time': x.time,
                'day': x.day,
                'month': x.month,
                'year': x.year,
                'duration': x.duration,
                'direction': x.direction,
                'location': x.location,
                'status': x.status,
                'angry': x.angry,
                'happy': x.happy,
                'neutral': x.neutral,
                'sad': x.sad,
                'fear': x.fear
            }

        return {'result': list(map(lambda x: to_json(x), AnalyticsModel.query.filter_by(direction = 1).all()))}

    @classmethod
    def ReturnAllOutgoings(cls):
        def to_json(x):
            return {
                'extension': x.extension,
                'username': x.username,
                'filename': x.filename,
                # 'time': x.time,
                'day': x.day,
                'month': x.month,
                'year': x.year,
                'duration': x.duration,
                'direction': x.direction,
                'location': x.location,
                'status': x.status,
                'angry': x.angry,
                'happy': x.happy,
                'neutral': x.neutral,
                'sad': x.sad,
                'fear': x.fear
            }

        return {'result': list(map(lambda x: to_json(x), AnalyticsModel.query.filter_by(direction = 0).all()))}

    @classmethod
    def DeleteAll(cls):
        try:
            num_rows_deleted = db.session.query(cls).delete()
            db.session.commit()
            return {'message': '{} row(s) deleted'.format(num_rows_deleted)}
        except:
            return {'message': 'Something went wrong'}

    @classmethod
    def AnalyticsByExtension(cls, extension):
        print(cls)
        def to_json(x):
            return {
                'extension': x.extension,
                'username': x.username,
                'filename': x.filename,
                # 'time': x.time,
                'day': x.day,
                'month': x.month,
                'year': x.year,
                'duration': x.duration,
                'direction': x.direction,
                'location': x.location,
                'status': x.status,
                'angry': x.angry,
                'happy': x.happy,
                'neutral': x.neutral,
                'sad': x.sad,
                'fear': x.fear
            }

        return {'result': list(map(lambda x: to_json(x), AnalyticsModel.query.filter_by(extension = extension).all()))}

    @classmethod
    def AnalyticsByUsername(cls, username):
        print(cls)
        def to_json(x):
            return {
                'extension': x.extension,
                'username': x.username,
                'filename': x.filename,
                # 'time': x.time,
                'day': x.day,
                'month': x.month,
                'year': x.year,
                'duration': x.duration,
                'direction': x.direction,
                'location': x.location,
                'status': x.status,
                'angry': x.angry,
                'happy': x.happy,
                'neutral': x.neutral,
                'sad': x.sad,
                'fear': x.fear
            }

        return {'result': list(map(lambda x: to_json(x), AnalyticsModel.query.filter_by(username = username).all()))}

    @classmethod
    def AnalyticsByFilename(cls, filename):
        print(cls)
        def to_json(x):
            return {
                'extension': x.extension,
                'username': x.username,
                'filename': x.filename,
                # 'time': x.time,
                'day': x.day,
                'month': x.month,
                'year': x.year,
                'duration': x.duration,
                'direction': x.direction,
                'location': x.location,
                'status': x.status,
                'angry': x.angry,
                'happy': x.happy,
                'neutral': x.neutral,
                'sad': x.sad,
                'fear': x.fear
            }

        return {'result': list(map(lambda x: to_json(x), AnalyticsModel.query.filter_by(filename = filename).all()))}

    @classmethod
    def AnalyticsByDay(cls, day, month, year):
        print(cls)
        def to_json(x):
            return {
                'extension': x.extension,
                'username': x.username,
                'filename': x.filename,
                # 'time': x.time,
                'day': x.day,
                'month': x.month,
                'year': x.year,
                'duration': x.duration,
                'direction': x.direction,
                'location': x.location,
                'status': x.status,
                'angry': x.angry,
                'happy': x.happy,
                'neutral': x.neutral,
                'sad': x.sad,
                'fear': x.fear
            }

        return {'result': list(map(lambda x: to_json(x), AnalyticsModel.query.filter_by(day = day).filter_by(month = month).filter_by(year = year).all()))}

    @classmethod
    def AnalyticsByMonth(cls, month, year):
        print(cls)
        def to_json(x):
            return {
                'extension': x.extension,
                'username': x.username,
                'filename': x.filename,
                # 'time': x.time,
                'day': x.day,
                'month': x.month,
                'year': x.year,
                'duration': x.duration,
                'direction': x.direction,
                'location': x.location,
                'status': x.status,
                'angry': x.angry,
                'happy': x.happy,
                'neutral': x.neutral,
                'sad': x.sad,
                'fear': x.fear
            }

        return {'result': list(map(lambda x: to_json(x), AnalyticsModel.query.filter_by(month = month).filter_by(year = year).all()))}

    @classmethod
    def AnalyticsByYear(cls, year):
        print(cls)
        def to_json(x):
            return {
                'extension': x.extension,
                'username': x.username,
                'filename': x.filename,
                # 'time': x.time,
                'day': x.day,
                'month': x.month,
                'year': x.year,
                'duration': x.duration,
                'direction': x.direction,
                'location': x.location,
                'status': x.status,
                'angry': x.angry,
                'happy': x.happy,
                'neutral': x.neutral,
                'sad': x.sad,
                'fear': x.fear
            }

        return {'result': list(map(lambda x: to_json(x), AnalyticsModel.query.filter_by(year = year).all()))}

