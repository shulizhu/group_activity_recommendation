from flask_mongoengine import MongoEngine


_db = MongoEngine()


def initialize_db(app):
    global _db
    _db.init_app(app)


def fetch_db():
    global _db
    return _db
