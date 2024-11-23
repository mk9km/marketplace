from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship

from marketplace.models import db

class Event(db.Model):
    __tablename__ = 'events'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    name = Column(String, nullable=False)
    date = Column(DateTime, nullable=False)
    description = Column(String, nullable=False)

    tickets = relationship('Ticket', back_populates='event')

    def to_dict(self):
        rv = {
            'id': self.id,
            'user_id': self.user_id,
            'name': self.name,
            'date': repr(self.date),
            'description': self.description
        }
        return rv