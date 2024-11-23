from sqlalchemy import Column, Integer, ForeignKey, String, Float
from sqlalchemy.orm import relationship

from marketplace.models import db


class Ticket(db.Model):
    __tablename__ = 'tickets'
    id = Column(Integer, primary_key=True)
    event_id = Column(Integer, ForeignKey('events.id'), nullable=False)
    name = Column(String, nullable=False)
    price = Column(Float, nullable=False)
    quantity = Column(Integer, nullable=False)  # Limited quantity

    event = relationship('Event', back_populates='tickets')
    purchases = relationship('Purchase', back_populates='ticket')

    def to_dict(self):
        rv = {
            'id': self.id,
            'event_id': self.event_id,
            'name': self.name,
            'price': self.price,
            'quantity': self.quantity
        }
        return rv
