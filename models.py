from database import db
from datetime import datetime
import hashlib
import uuid

class Name(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    gender = db.Column(db.Integer)
    predicted = db.Column(db.Integer)
    created_at = db.Column(db.DateTime)

    def __init__(self, name, gender, predicted):
        self.name = name
        self.gender = gender
        self.predicted = predicted
        self.created_at = datetime.today()

    def __repr__(self):
        return '<Name %s - %s>' % (self.name, 'Male' if self.gender else 'Female')