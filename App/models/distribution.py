from App.database import db
from datetime import date

#Distributes a randomly selected group of user defined profiles from the database
class Distribution(db.Model):
    distributeId = db.Column(db.Integer, primary_key=True)
    numProfiles = db.Column(db.Integer, nullable=False)
    timeStamp = db.Column(db.Date , nullable=False)
    profileFeeds = db.relationship('ProfileFeed', backref='feeds',
                           lazy=True, cascade="all, delete-orphan")

    def __init__(self, numProfiles):
        self.numProfiles = numProfiles
        self.timeStamp = date.today()

    def toJSON(self):
        return{
            'profileId': self.profileId,
            'numProfiles':self.numProfiles,
            'timeStamp':self.timeStamp,
            'profileFeeds': [profileFeed.toJSON() for profileFeed in self.profileFeeds]
        }

    