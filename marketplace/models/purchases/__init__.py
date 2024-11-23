from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship

from marketplace.models import db


class Purchase(db.Model):
    __tablename__ = 'purchases'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    ticket_id = Column(Integer, ForeignKey('tickets.id'), nullable=False)
    quantity = Column(Integer, nullable=False)

    user = relationship('User', back_populates='purchases')
    ticket = relationship('Ticket', back_populates='purchases')

    def to_dict(self):
        rv = {
            'id': self.id, 
            'user_id': self.user_id, 
            'ticket_id': self.ticket_id,
            'quantity': self.quantity
        }
        return rv