# creating item model
from db import db


class ItemModel(db.Model):
    __tablename__ = 'items'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    price = db.Column(db.Float(precision=2))

    # for the properties of the items, we are defining __init__
    def __init__(self, name, price):
        self.name = name
        self.price = price

    def json(self):
        return {'name': self.name, 'price': self.price}

    @classmethod
    def find_by_name(cls, name):
        return cls.query.filter_by(name=name).first()  # Select * from items where name=name LIMIT 1

    def save_to_db(self):   # this will insert and update as well.
        # session is the collection of object that we are going to write into the database
        db.session.add(self)    # self is having the current change.
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
