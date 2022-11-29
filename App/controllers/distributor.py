from App.database import db
from App.models import Distributor
from App.controllers.feed import get_feeds_by_sender, create_feed


def create_distributor(num_profiles):
    distributor = Distributor(num_profiles)
    db.session.add(distributor)
    db.session.commit()
    return distributor


def get_distributor(id):
    distributor = Distributor.query.get(id)
    return distributor


def get_distributor_json(id):
    distributor = Distributor.query.get(id)
    return distributor.to_json()


def get_all_distributors():
    distributors = Distributor.query.all()
    return distributors


def get_all_distributors_json():
    distributors = Distributor.query.all()
    return [distributor.to_json() for distributor in distributors]


def get_distributor_feeds(id):
    distributor = Distributor.query.get(id)
    if distributor:
        return distributor.feed
    return None


def distribute(dist_id):
    distributor = Distributor.query.get(dist_id)
    if distributor:
        for sender in range(1, distributor.num_profiles + 1):
            feeds = get_feeds_by_sender(sender)
            for receiver in range(1, distributor.num_profiles + 1):
                if receiver != sender:
                    if not any(feed.receiver_id == receiver for feed in feeds):
                        create_feed(sender, receiver, dist_id)
    return None
