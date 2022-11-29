from App.database import db
from datetime import datetime


class Distributor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    num_profiles = db.Column(db.Integer, nullable=False)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    def __init__(self, num_profiles):
        self.num_profiles = num_profiles

    # Accessors
    def get_id(self):
        return self.id

    def get_num_profiles(self):
        return self.num_profiles

    def get_timestamp(self):
        return self.timestamp

    # TODO - distribution algorithm
    def distribute(self):
        pass

    def to_json(self):
        return {
            "id": self.id,
            "num_profiles": self.num_profiles,
            "timestamp": self.timestamp,
        }
