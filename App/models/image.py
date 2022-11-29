from App.database import db


class Image(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    url = db.Column(db.String(120), nullable=False)

    def __init__(self, user_id, url):
        self.user_id = user_id
        self.url = url

    # Accessors
    def get_id(self):
        return self.id

    def get_user_id(self):
        return self.user_id

    def get_url(self):
        return self.url

    def set_url(self, url):
        self.url = url

    def set_user_id(self, user_id):
        self.user_id = user_id

    def to_json(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "rank": self.rank,
            "url": self.url,
        }
