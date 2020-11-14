from shared import db
import datetime
from sqlalchemy.sql import func


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(32), index = True)
    password = db.Column(db.String(128))
    fio = db.Column(db.String(32), default=None)

    def to_dict(self):
        return {
            'username': self.username,
            'fio': self.fio,
        }

    @staticmethod
    def current():
        id =  1
        return User.query.get(id)


    def verify_password(self, password):
        # TODO: Hash password in future
        return password == self.password



class Files(db.Model):
    id: int
    name: str
    filename: str
    created_date: datetime

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    name = db.Column(db.String(256))
    filename = db.Column(db.String(256))
    filename_norm = db.Column(db.String(256), default=None)
    status = db.Column(db.String(20))
    processed = db.Column(db.Integer, default= 0)
    failed = db.Column(db.Integer, default= 0)

    created_date = db.Column(db.DateTime(timezone=True), server_default=func.now())
    finish_date = db.Column(db.DateTime(timezone=True), default=None)


    def as_dict(self):
        d = {}
        for c in self.__table__.columns:
            d[c.name] = getattr(self, c.name)
            if c.name == 'created_date':
                d[c.name] = d[c.name].isoformat()
        return d


db.create_all()
db.session.commit()