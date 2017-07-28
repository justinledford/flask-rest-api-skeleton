from models import db

class Foo(db.Model):
    __tablename__ = 'foo'

    id = db.Column(db.Integer, primary_key=True,
                   nullable=False, autoincrement=True)
    name = db.Column(db.String(255), nullable=False)

